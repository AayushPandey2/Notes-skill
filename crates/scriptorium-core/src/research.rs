//! Concurrent retrieval of supplied source URLs, not model reasoning or source discovery.
use crate::{
    cache::{Cache, hash, now},
    config::Config,
    network::{DownloadPolicy, fetch_resource, validate_url},
};
use anyhow::{Context, Result, ensure};
use serde::{Deserialize, Serialize};
use std::{path::PathBuf, time::Instant};
use tokio::task::JoinSet;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SourceRecord {
    pub requested_url: String,
    pub final_url: String,
    pub mime: String,
    pub retrieved_at: u64,
    pub sha256: String,
    pub text: String,
    pub cached: bool,
}
#[derive(Debug, Serialize)]
pub struct SourceResult {
    pub url: String,
    pub record: Option<SourceRecord>,
    pub error: Option<String>,
}
#[derive(Debug, Serialize)]
pub struct ResearchReport {
    pub sources: Vec<SourceResult>,
    pub elapsed_ms: u128,
    pub complete: bool,
}

pub async fn retrieve(
    urls: Vec<String>,
    config: Config,
    cache_root: PathBuf,
) -> Result<ResearchReport> {
    ensure!(
        !urls.is_empty() && urls.len() <= 1000,
        "supply 1..1000 source URLs"
    );
    ensure!(
        (1..=64).contains(&config.concurrency),
        "concurrency must be 1..64"
    );
    for url in &urls {
        validate_url(url)?;
    }
    let started = Instant::now();
    let mut pending = urls.into_iter().enumerate();
    let mut tasks = JoinSet::new();
    let mut results = Vec::new();
    loop {
        while tasks.len() < config.concurrency {
            let Some((index, url)) = pending.next() else {
                break;
            };
            let settings = config.clone();
            let root = cache_root.clone();
            tasks.spawn(async move {
                let result = retrieve_one(&url, &settings, root).await;
                (
                    index,
                    SourceResult {
                        url,
                        record: result.as_ref().ok().cloned(),
                        error: result.err().map(|e| format!("{e:#}")),
                    },
                )
            });
        }
        let Some(result) = tasks.join_next().await else {
            break;
        };
        results.push(result.context("source worker failed")?);
    }
    results.sort_by_key(|(index, _)| *index);
    let sources: Vec<_> = results.into_iter().map(|(_, s)| s).collect();
    let complete = sources.iter().all(|s| s.error.is_none());
    Ok(ResearchReport {
        sources,
        complete,
        elapsed_ms: started.elapsed().as_millis(),
    })
}
async fn retrieve_one(url: &str, config: &Config, cache_root: PathBuf) -> Result<SourceRecord> {
    let cache = Cache::new(cache_root, config.cache_ttl_seconds)?;
    let key = format!("source-v1:{}:{url}", config.max_download_bytes);
    if let Some(mut record) = cache.get::<SourceRecord>(&key)? {
        ensure!(record.requested_url == url, "cached source URL mismatch");
        validate_url(&record.final_url)?;
        ensure!(
            record.sha256 == hash(record.text.as_bytes()),
            "source cache integrity failure"
        );
        record.cached = true;
        return Ok(record);
    }
    let policy = DownloadPolicy {
        max_bytes: config.max_download_bytes,
        timeout_seconds: config.timeout_seconds,
        max_redirects: 3,
    };
    let mut last = None;
    for attempt in 0..3 {
        match fetch_resource(url, &policy).await {
            Ok(response) => {
                ensure!(
                    [
                        "text/plain",
                        "text/html",
                        "application/json",
                        "text/markdown",
                        "application/xhtml+xml"
                    ]
                    .contains(&response.mime.as_str()),
                    "unsupported research response type {}",
                    response.mime
                );
                let text = String::from_utf8(response.bytes).context(
                    "source text must be UTF-8; PDF extraction requires an explicit adapter",
                )?;
                let record = SourceRecord {
                    requested_url: url.into(),
                    final_url: response.final_url,
                    mime: response.mime,
                    retrieved_at: now()?,
                    sha256: hash(text.as_bytes()),
                    text,
                    cached: false,
                };
                cache.put(&key, &record)?;
                return Ok(record);
            }
            Err(e) => last = Some(e),
        }
        if attempt < 2 {
            tokio::time::sleep(std::time::Duration::from_millis(200 * (1 << attempt))).await;
        }
    }
    Err(last.context("retrieval failed")?)
}
#[cfg(test)]
mod tests {
    use super::*;
    #[tokio::test]
    async fn rejects_private_sources_before_scheduling() {
        let dir = tempfile::tempdir().unwrap();
        assert!(
            retrieve(
                vec!["https://127.0.0.1/".into()],
                Config::default(),
                dir.path().to_path_buf()
            )
            .await
            .is_err()
        );
    }
    #[tokio::test]
    async fn cache_hit_preserves_provenance_without_network() -> Result<()> {
        let dir = tempfile::tempdir()?;
        let config = Config::default();
        let url = "https://example.org/paper";
        let record = SourceRecord {
            requested_url: url.into(),
            final_url: url.into(),
            mime: "text/plain".into(),
            retrieved_at: now()?,
            sha256: hash(b"evidence"),
            text: "evidence".into(),
            cached: false,
        };
        Cache::new(dir.path(), 60)?.put(
            &format!("source-v1:{}:{url}", config.max_download_bytes),
            &record,
        )?;
        let report = retrieve(vec![url.into()], config, dir.path().to_path_buf()).await?;
        assert!(report.complete);
        assert!(report.sources[0].record.as_ref().unwrap().cached);
        Ok(())
    }
}
