//! Bounded HTTPS acquisition. Every redirect gets fresh, validated, pinned DNS.
use anyhow::{Context, Result, bail, ensure};
use reqwest::{Client, header, redirect::Policy};
use serde::{Deserialize, Serialize};
use std::{
    collections::HashSet,
    net::{IpAddr, SocketAddr},
    time::Duration,
};
use url::Url;

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct DownloadPolicy {
    pub max_bytes: usize,
    pub timeout_seconds: u64,
    pub max_redirects: usize,
}
impl Default for DownloadPolicy {
    fn default() -> Self {
        Self {
            max_bytes: 8 * 1024 * 1024,
            timeout_seconds: 20,
            max_redirects: 3,
        }
    }
}
pub struct DownloadedImage {
    pub bytes: Vec<u8>,
    pub mime: String,
    pub final_url: String,
}

pub fn validate_url(value: &str) -> Result<Url> {
    ensure!(
        !value
            .chars()
            .any(|c| c.is_whitespace() || c.is_control() || "<>\\()".contains(c)),
        "unsafe URL characters"
    );
    let url = Url::parse(value)?;
    ensure!(
        url.scheme() == "https"
            && url.host_str().is_some()
            && url.username().is_empty()
            && url.password().is_none()
            && url.fragment().is_none()
            && url.port_or_known_default() == Some(443),
        "requires HTTPS on port 443 without credentials or fragments"
    );
    if let Some(host) = url.host() {
        match host {
            url::Host::Ipv4(ip) => ensure!(public_ip(IpAddr::V4(ip)), "nonpublic image address"),
            url::Host::Ipv6(ip) => ensure!(public_ip(IpAddr::V6(ip)), "nonpublic image address"),
            _ => (),
        }
    }
    Ok(url)
}

pub fn public_ip(ip: IpAddr) -> bool {
    match ip {
        IpAddr::V4(ip) => {
            let [a, b, c, _] = ip.octets();
            !(a == 0
                || a == 10
                || a == 127
                || a >= 224
                || (a == 100 && (64..=127).contains(&b))
                || (a == 169 && b == 254)
                || (a == 172 && (16..=31).contains(&b))
                || (a == 192 && (b == 168 || b == 0 || (b == 88 && c == 99) || (b == 2 && c == 0)))
                || (a == 198 && (b == 18 || b == 19 || (b == 51 && c == 100)))
                || (a == 203 && b == 0 && c == 113))
        }
        IpAddr::V6(ip) => {
            let s = ip.segments();
            // Global unicast only; exclude transition, protocol and documentation ranges.
            (s[0] & 0xe000) == 0x2000
                && !(s[0] == 0x2001 && (s[1] < 0x0200 || s[1] == 0x0db8))
                && s[0] != 0x2002
                && !(s[0] == 0x3fff && s[1] < 0x1000)
        }
    }
}

pub async fn fetch_image(value: &str, policy: &DownloadPolicy) -> Result<DownloadedImage> {
    let downloaded = fetch_resource(value, policy).await?;
    ensure!(
        matches!(
            downloaded.mime.as_str(),
            "image/png" | "image/jpeg" | "image/webp"
        ),
        "external images must be supported raster formats"
    );
    crate::assets::inspect_image(&downloaded.bytes, &downloaded.mime)?;
    Ok(downloaded)
}
pub async fn fetch_resource(value: &str, policy: &DownloadPolicy) -> Result<DownloadedImage> {
    ensure!(
        policy.max_bytes > 0
            && policy.max_bytes <= 64 * 1024 * 1024
            && (1..=120).contains(&policy.timeout_seconds)
            && policy.max_redirects <= 10,
        "invalid download limits"
    );
    tokio::time::timeout(
        Duration::from_secs(policy.timeout_seconds),
        fetch_inner(value, policy),
    )
    .await
    .context("image acquisition timeout")?
}
async fn fetch_inner(value: &str, policy: &DownloadPolicy) -> Result<DownloadedImage> {
    let mut current = validate_url(value)?;
    let mut seen = HashSet::new();
    for step in 0..=policy.max_redirects {
        ensure!(seen.insert(current.to_string()), "redirect loop");
        let host = current
            .host_str()
            .context("missing host")?
            .trim_matches(['[', ']']);
        let addresses: Vec<SocketAddr> = tokio::net::lookup_host((host, 443))
            .await
            .context("image DNS lookup")?
            .collect();
        ensure!(
            !addresses.is_empty() && addresses.iter().all(|a| public_ip(a.ip())),
            "DNS must resolve exclusively to public addresses"
        );
        let client = Client::builder()
            .https_only(true)
            .no_proxy()
            .redirect(Policy::none())
            .timeout(Duration::from_secs(policy.timeout_seconds))
            .resolve_to_addrs(host, &addresses)
            .build()?;
        let mut response = client
            .get(current.clone())
            .header(header::ACCEPT, "*/*")
            .header(header::ACCEPT_ENCODING, "identity")
            .header(header::USER_AGENT, "Scriptorium-Rust/5.1")
            .send()
            .await?;
        if matches!(response.status().as_u16(), 301 | 302 | 303 | 307 | 308) {
            ensure!(step < policy.max_redirects, "redirect limit");
            let target = response
                .headers()
                .get(header::LOCATION)
                .context("redirect without Location")?
                .to_str()?;
            current = validate_url(current.join(target)?.as_str())?;
            continue;
        }
        ensure!(
            response.status().as_u16() == 200,
            "image HTTP status {}",
            response.status()
        );
        ensure!(
            response
                .headers()
                .get(header::CONTENT_ENCODING)
                .map(|v| v == "identity")
                .unwrap_or(true),
            "compressed transport not allowed"
        );
        let mime = response
            .headers()
            .get(header::CONTENT_TYPE)
            .context("missing Content-Type")?
            .to_str()?
            .split(';')
            .next()
            .unwrap_or("")
            .trim()
            .to_ascii_lowercase();
        if let Some(length) = response.content_length() {
            ensure!(
                length <= policy.max_bytes as u64,
                "image exceeds byte limit"
            );
        }
        let expected = response.content_length();
        let mut bytes = Vec::new();
        while let Some(chunk) = response.chunk().await? {
            ensure!(
                bytes.len().saturating_add(chunk.len()) <= policy.max_bytes,
                "image exceeds byte limit"
            );
            bytes.extend_from_slice(&chunk);
        }
        if let Some(length) = expected {
            ensure!(bytes.len() as u64 == length, "truncated response");
        }
        return Ok(DownloadedImage {
            bytes,
            mime,
            final_url: current.to_string(),
        });
    }
    bail!("redirect limit")
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn unsafe_urls_and_addresses() {
        for value in [
            "http://example.org/a.png",
            "https://127.0.0.1/a",
            "https://[::1]/a",
            "https://u:p@example.org/a",
            "https://example.org:8443/a",
            "https://example.org/a#x",
        ] {
            assert!(validate_url(value).is_err(), "{value}");
        }
        for value in [
            "10.1.2.3",
            "100.64.0.1",
            "192.0.2.1",
            "198.51.100.1",
            "169.254.169.254",
            "::ffff:8.8.8.8",
            "2001:db8::1",
            "2002:0808:0808::1",
        ] {
            assert!(!public_ip(value.parse().unwrap()), "{value}");
        }
        assert!(public_ip("8.8.8.8".parse().unwrap()));
        assert!(public_ip("2606:4700:4700::1111".parse().unwrap()));
    }
    #[tokio::test]
    async fn rejects_unsafe_before_request() {
        assert!(
            fetch_image("https://127.0.0.1/x", &DownloadPolicy::default())
                .await
                .is_err()
        );
    }
}
