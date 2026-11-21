use anyhow::{Context, Result, ensure};
use serde::{Deserialize, Serialize};
use std::path::{Component, Path, PathBuf};

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(default, deny_unknown_fields)]
pub struct Config {
    pub concurrency: usize,
    pub cache_ttl_seconds: u64,
    pub max_download_bytes: usize,
    pub timeout_seconds: u64,
    pub attachment_directory: Option<PathBuf>,
}
impl Default for Config {
    fn default() -> Self {
        Self {
            concurrency: 4,
            cache_ttl_seconds: 86400,
            max_download_bytes: 20 * 1024 * 1024,
            timeout_seconds: 30,
            attachment_directory: None,
        }
    }
}
impl Config {
    pub fn load(path: Option<&Path>) -> Result<Self> {
        let value: Self = match path {
            Some(p) => serde_json::from_slice(
                &std::fs::read(p).with_context(|| format!("read config {}", p.display()))?,
            )?,
            None => Self::default(),
        };
        ensure!(
            (1..=64).contains(&value.concurrency),
            "concurrency must be 1..64"
        );
        ensure!(
            (1..=120).contains(&value.timeout_seconds),
            "timeout must be 1..120 seconds"
        );
        ensure!(
            (1..=64 * 1024 * 1024).contains(&value.max_download_bytes),
            "download limit must be 1..64 MiB"
        );
        Ok(value)
    }
    /// Resolve Obsidian's root-relative, note-relative and subfolder attachment settings.
    pub fn attachment_dir(&self, vault: &Path, note: &Path) -> Result<PathBuf> {
        safe_relative(note)?;
        let configured = if let Some(p) = &self.attachment_directory {
            p.clone()
        } else {
            let settings = vault.join(".obsidian/app.json");
            if settings.exists() {
                let v: serde_json::Value = serde_json::from_slice(&std::fs::read(settings)?)?;
                PathBuf::from(
                    v.get("attachmentFolderPath")
                        .and_then(|x| x.as_str())
                        .unwrap_or("assets"),
                )
            } else {
                PathBuf::from("assets")
            }
        };
        safe_relative(&configured)?;
        let text = configured.to_string_lossy().replace('\\', "/");
        let parent = note.parent().unwrap_or(Path::new(""));
        Ok(if text == "." || text == "./" {
            parent.to_path_buf()
        } else if let Some(suffix) = text.strip_prefix("./") {
            parent.join(suffix)
        } else {
            configured
        })
    }
}
pub fn safe_relative(path: &Path) -> Result<()> {
    ensure!(!path.is_absolute(), "absolute vault paths are forbidden");
    ensure!(
        !path.to_string_lossy().contains([':', '\0']),
        "invalid vault path"
    );
    ensure!(
        !path.components().any(|c| matches!(
            c,
            Component::ParentDir | Component::RootDir | Component::Prefix(_)
        )),
        "vault path escapes root"
    );
    // Backslashes must not disguise traversal on Unix.
    ensure!(
        !path.to_string_lossy().split(['/', '\\']).any(|s| s == ".."),
        "vault path escapes root"
    );
    Ok(())
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn honors_note_relative_attachment_setting() -> Result<()> {
        let dir = tempfile::tempdir()?;
        std::fs::create_dir(dir.path().join(".obsidian"))?;
        std::fs::write(
            dir.path().join(".obsidian/app.json"),
            r#"{"attachmentFolderPath":"./figures"}"#,
        )?;
        assert_eq!(
            Config::default().attachment_dir(dir.path(), Path::new("topic/chapter.md"))?,
            PathBuf::from("topic/figures")
        );
        assert!(safe_relative(Path::new("a\\..\\secret")).is_err());
        Ok(())
    }
}
