//! Content-addressed local images and explicit provenance attestations.
use crate::rendering::RenderedArtifact;
use anyhow::{Context, Result, ensure};
use image::{ImageFormat, ImageReader, Limits};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::{
    fs,
    io::{Cursor, Read, Write},
    path::{Component, Path, PathBuf},
    time::{SystemTime, UNIX_EPOCH},
};

pub const MAX_BYTES: usize = 8 * 1024 * 1024;
pub const MAX_PIXELS: u64 = 4_000_000;
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Provenance {
    pub source_page: String,
    pub image_url: String,
    pub creator: String,
    pub license: String,
    /// Evidence-backed attestation supplied by the caller, not a license inference.
    pub permission_basis: String,
    pub relevance: String,
    pub original_filename: String,
    pub retrieved_at: u64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub final_url: Option<String>,
}
impl Provenance {
    pub fn validate(&self) -> Result<()> {
        for value in [
            &self.source_page,
            &self.creator,
            &self.license,
            &self.permission_basis,
            &self.relevance,
            &self.original_filename,
        ] {
            ensure!(
                !value.trim().is_empty(),
                "missing provenance/permission/relevance field"
            );
        }
        ensure!(self.retrieved_at > 0, "missing retrieval timestamp");
        Ok(())
    }
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct AssetRecord {
    pub local_path: PathBuf,
    pub sha256: String,
    pub mime: String,
    pub width: u32,
    pub height: u32,
    pub bytes: usize,
    pub provenance: Provenance,
}
#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub struct ImageInspection {
    pub width: u32,
    pub height: u32,
}

pub fn inspect_image(bytes: &[u8], mime: &str) -> Result<ImageInspection> {
    ensure!(
        !bytes.is_empty() && bytes.len() <= MAX_BYTES,
        "image byte limit"
    );
    if mime == "image/svg+xml" {
        return crate::rendering::inspect_svg(bytes);
    }
    let expected = match mime {
        "image/png" => ImageFormat::Png,
        "image/jpeg" => ImageFormat::Jpeg,
        "image/webp" => ImageFormat::WebP,
        _ => anyhow::bail!("unsupported image MIME"),
    };
    ensure!(
        image::guess_format(bytes)? == expected,
        "MIME/content mismatch"
    );
    let mut reader = ImageReader::with_format(Cursor::new(bytes), expected);
    let mut limits = Limits::default();
    limits.max_image_width = Some(10_000);
    limits.max_image_height = Some(10_000);
    limits.max_alloc = Some(64 * 1024 * 1024);
    reader.limits(limits);
    let (w, h) = ImageReader::with_format(Cursor::new(bytes), expected).into_dimensions()?;
    ensure!(
        w > 0 && h > 0 && w as u64 * h as u64 <= MAX_PIXELS,
        "image pixel limit"
    );
    let decoded = reader.decode().context("image decode/integrity failure")?;
    ensure!(
        decoded.width() == w && decoded.height() == h,
        "decoded dimensions mismatch"
    );
    Ok(ImageInspection {
        width: w,
        height: h,
    })
}

pub struct AssetStore {
    vault: PathBuf,
    attachment: PathBuf,
}
impl AssetStore {
    pub fn new(vault: impl AsRef<Path>, attachment_dir: impl AsRef<Path>) -> Result<Self> {
        ensure!(vault.as_ref().is_dir(), "vault must exist");
        let vault = fs::canonicalize(vault)?;
        let attachment = attachment_dir.as_ref().to_path_buf();
        validate_relative(&attachment)?;
        let store = Self { vault, attachment };
        store.checked_target(&store.attachment, true)?;
        Ok(store)
    }
    /// Relative attachment paths only. Existing symlinks are rejected, including
    /// ones pointing into the vault, to avoid ambiguous ownership and writes.
    fn checked_target(&self, relative: &Path, create_dirs: bool) -> Result<PathBuf> {
        validate_relative(relative)?;
        let mut target = self.vault.clone();
        for part in relative.components() {
            target.push(part);
            match fs::symlink_metadata(&target) {
                Ok(meta) => ensure!(
                    !meta.file_type().is_symlink()
                        && fs::canonicalize(&target)?.starts_with(&self.vault),
                    "asset symlink/path escape"
                ),
                Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                    if create_dirs {
                        fs::create_dir(&target)?;
                    }
                }
                Err(e) => return Err(e.into()),
            }
        }
        Ok(target)
    }
    pub fn store_bytes(
        &self,
        bytes: &[u8],
        mime: &str,
        provenance: Provenance,
    ) -> Result<AssetRecord> {
        provenance.validate()?;
        ensure!(
            mime != "image/svg+xml",
            "external SVG is not accepted; use validated deterministic rendering"
        );
        if !provenance.image_url.is_empty() {
            crate::network::validate_url(&provenance.image_url)?;
        }
        if let Some(url) = &provenance.final_url {
            crate::network::validate_url(url)?;
        }
        self.persist(bytes, mime, provenance)
    }
    pub fn store_generated(
        &self,
        artifact: &RenderedArtifact,
        concept: &str,
    ) -> Result<AssetRecord> {
        ensure!(
            !concept.trim().is_empty(),
            "generated visual needs concept/objective"
        );
        ensure!(
            artifact.mime == "image/svg+xml",
            "asset storage supports image artifacts only"
        );
        self.persist(
            &artifact.bytes,
            &artifact.mime,
            Provenance {
                source_page: "original deterministic rendering".into(),
                image_url: String::new(),
                creator: "Scriptorium".into(),
                license: "original; input data rights remain with their owners".into(),
                permission_basis: "original SVG from caller-supplied rendering inputs".into(),
                relevance: concept.into(),
                original_filename: format!("{}.svg", artifact.renderer),
                retrieved_at: SystemTime::now().duration_since(UNIX_EPOCH)?.as_secs(),
                final_url: None,
            },
        )
    }
    fn persist(&self, bytes: &[u8], mime: &str, provenance: Provenance) -> Result<AssetRecord> {
        let info = inspect_image(bytes, mime)?;
        let sha256 = hex::encode(Sha256::digest(bytes));
        let extension = match mime {
            "image/png" => "png",
            "image/jpeg" => "jpg",
            "image/webp" => "webp",
            "image/svg+xml" => "svg",
            _ => anyhow::bail!("unsupported asset"),
        };
        let relative = self.attachment.join(format!("{sha256}.{extension}"));
        let directory = self.checked_target(&self.attachment, true)?;
        let target = self.checked_target(&relative, false)?;
        if target.exists() {
            ensure!(
                read_bounded(&target, bytes.len())? == bytes,
                "content-address collision/corruption"
            );
        } else {
            let mut temporary = tempfile::NamedTempFile::new_in(&directory)?;
            temporary.write_all(bytes)?;
            temporary.as_file().sync_all()?;
            match temporary.persist_noclobber(&target) {
                Ok(_) => (),
                Err(error) if error.error.kind() == std::io::ErrorKind::AlreadyExists => ensure!(
                    read_bounded(&target, bytes.len())? == bytes,
                    "concurrent content collision"
                ),
                Err(error) => return Err(error.error.into()),
            }
        }
        Ok(AssetRecord {
            local_path: relative,
            sha256,
            mime: mime.into(),
            width: info.width,
            height: info.height,
            bytes: bytes.len(),
            provenance,
        })
    }
    pub fn verify(&self, record: &AssetRecord) -> Result<()> {
        record.provenance.validate()?;
        let path = self.checked_target(&record.local_path, false)?;
        ensure!(
            record.local_path.starts_with(&self.attachment),
            "asset outside attachment directory"
        );
        let meta = fs::metadata(&path)?;
        ensure!(meta.len() <= MAX_BYTES as u64, "asset byte limit");
        let bytes = read_bounded(&path, MAX_BYTES)?;
        ensure!(
            hex::encode(Sha256::digest(&bytes)) == record.sha256 && bytes.len() == record.bytes,
            "asset hash/length mismatch"
        );
        let info = inspect_image(&bytes, &record.mime)?;
        ensure!(
            info.width == record.width && info.height == record.height,
            "asset dimensions mismatch"
        );
        Ok(())
    }
    pub fn embed(&self, record: &AssetRecord, alt: &str) -> Result<String> {
        self.verify(record)?;
        ensure!(!alt.trim().is_empty(), "image needs alternative text");
        // Obsidian vault-relative wiki embeds; all asset path components are safe.
        Ok(format!(
            "![[{}|{}]]",
            record.local_path.to_string_lossy().replace('\\', "/"),
            alt.replace(['|', ']', '\n', '\r'], " ")
        ))
    }
}
fn validate_relative(path: &Path) -> Result<()> {
    // Empty means the vault root for Obsidian's root attachment setting.
    for component in path.components() {
        let Component::Normal(part) = component else {
            anyhow::bail!("asset path must be relative without traversal");
        };
        let value = part.to_str().context("non-UTF8 path")?;
        ensure!(
            !value.is_empty()
                && !value.ends_with(['.', ' '])
                && !value
                    .chars()
                    .any(|c| c.is_control() || ":<>\"|?*[]#\\".contains(c)),
            "unsafe asset path component"
        );
        let stem = value.split('.').next().unwrap_or("").to_ascii_uppercase();
        ensure!(
            !matches!(
                stem.as_str(),
                "CON"
                    | "PRN"
                    | "AUX"
                    | "NUL"
                    | "COM1"
                    | "COM2"
                    | "COM3"
                    | "COM4"
                    | "COM5"
                    | "COM6"
                    | "COM7"
                    | "COM8"
                    | "COM9"
                    | "LPT1"
                    | "LPT2"
                    | "LPT3"
                    | "LPT4"
                    | "LPT5"
                    | "LPT6"
                    | "LPT7"
                    | "LPT8"
                    | "LPT9"
            ),
            "reserved filename"
        );
    }
    Ok(())
}
fn read_bounded(path: &Path, limit: usize) -> Result<Vec<u8>> {
    let file = fs::File::open(path)?;
    ensure!(
        file.metadata()?.len() <= limit as u64,
        "existing asset exceeds expected byte limit"
    );
    let mut bytes = Vec::new();
    file.take(limit as u64 + 1).read_to_end(&mut bytes)?;
    ensure!(
        bytes.len() <= limit,
        "existing asset changed/exceeds byte limit"
    );
    Ok(bytes)
}

#[cfg(test)]
mod tests {
    use super::*;
    fn png() -> Vec<u8> {
        let mut out = Cursor::new(Vec::new());
        image::DynamicImage::new_rgb8(64, 32)
            .write_to(&mut out, ImageFormat::Png)
            .unwrap();
        out.into_inner()
    }
    fn provenance() -> Provenance {
        Provenance {
            source_page: "https://example.org/source".into(),
            image_url: "https://example.org/a.png".into(),
            creator: "Author".into(),
            license: "CC0".into(),
            permission_basis: "Source page explicitly marks figure CC0".into(),
            relevance: "shows required concept".into(),
            original_filename: "a.png".into(),
            retrieved_at: 1,
            final_url: None,
        }
    }
    #[test]
    fn decoding_and_corruption() {
        let bytes = png();
        assert_eq!(inspect_image(&bytes, "image/png").unwrap().width, 64);
        assert!(inspect_image(&bytes, "image/jpeg").is_err());
        assert!(inspect_image(&bytes[..20], "image/png").is_err());
        assert!(inspect_image(b"<html>", "image/png").is_err());
    }
    #[test]
    fn dedup_tampering_and_paths() {
        let dir = tempfile::tempdir().unwrap();
        let store = AssetStore::new(dir.path(), "attachments/topic").unwrap();
        let one = store
            .store_bytes(&png(), "image/png", provenance())
            .unwrap();
        let two = store
            .store_bytes(&png(), "image/png", provenance())
            .unwrap();
        assert_eq!(one.local_path, two.local_path);
        store.verify(&one).unwrap();
        assert!(
            store
                .embed(&one, "Figure")
                .unwrap()
                .starts_with("![[attachments/topic/")
        );
        fs::write(dir.path().join(&one.local_path), b"bad").unwrap();
        assert!(store.verify(&one).is_err());
        for path in ["../escape", "/absolute", "CON", "a:b", "a/../b"] {
            assert!(AssetStore::new(dir.path(), path).is_err(), "{path}");
        }
    }
    #[test]
    fn missing_permission_rejected() {
        let mut p = provenance();
        p.permission_basis.clear();
        assert!(p.validate().is_err());
    }
}
