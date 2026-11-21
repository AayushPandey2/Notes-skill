use anyhow::{Result, ensure};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::{
    io::Write,
    path::{Path, PathBuf},
    time::{SystemTime, UNIX_EPOCH},
};

const VERSION: u32 = 1;
pub fn hash(bytes: &[u8]) -> String {
    hex::encode(Sha256::digest(bytes))
}
pub fn now() -> Result<u64> {
    Ok(SystemTime::now().duration_since(UNIX_EPOCH)?.as_secs())
}
#[derive(Serialize, Deserialize)]
struct Entry {
    version: u32,
    created: u64,
    key: String,
    digest: String,
    value: serde_json::Value,
}
pub struct Cache {
    root: PathBuf,
    ttl: u64,
}
impl Cache {
    pub fn new(root: impl AsRef<Path>, ttl: u64) -> Result<Self> {
        std::fs::create_dir_all(root.as_ref())?;
        Ok(Self {
            root: root.as_ref().canonicalize()?,
            ttl,
        })
    }
    fn path(&self, key: &str) -> PathBuf {
        self.root.join(format!("{}.json", hash(key.as_bytes())))
    }
    pub fn get<T: serde::de::DeserializeOwned>(&self, key: &str) -> Result<Option<T>> {
        let path = self.path(key);
        if !path.exists() {
            return Ok(None);
        }
        ensure!(
            !std::fs::symlink_metadata(&path)?.file_type().is_symlink(),
            "cache symlink rejected"
        );
        let parsed: Entry = match serde_json::from_slice(&std::fs::read(path)?) {
            Ok(e) => e,
            Err(_) => return Ok(None),
        };
        if parsed.version != VERSION
            || parsed.key != key
            || now()?.saturating_sub(parsed.created) >= self.ttl
            || parsed.created > now()?
        {
            return Ok(None);
        }
        if hash(&serde_json::to_vec(&parsed.value)?) != parsed.digest {
            return Ok(None);
        }
        Ok(Some(serde_json::from_value(parsed.value)?))
    }
    pub fn put<T: Serialize>(&self, key: &str, value: &T) -> Result<()> {
        let value = serde_json::to_value(value)?;
        let entry = Entry {
            version: VERSION,
            created: now()?,
            key: key.into(),
            digest: hash(&serde_json::to_vec(&value)?),
            value,
        };
        let path = self.path(key);
        if path.exists() {
            ensure!(
                !std::fs::symlink_metadata(&path)?.file_type().is_symlink(),
                "cache symlink rejected"
            );
        }
        let mut temp = tempfile::NamedTempFile::new_in(&self.root)?;
        temp.write_all(&serde_json::to_vec(&entry)?)?;
        temp.as_file().sync_all()?;
        temp.persist(path)?;
        Ok(())
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn cache_integrity_expiry_and_invalidation() -> Result<()> {
        let dir = tempfile::tempdir()?;
        let cache = Cache::new(dir.path(), 60)?;
        cache.put("source:v1", &vec![1, 2, 3])?;
        assert_eq!(cache.get::<Vec<u32>>("source:v1")?, Some(vec![1, 2, 3]));
        assert!(cache.get::<Vec<u32>>("source:v2")?.is_none());
        let mut value: serde_json::Value =
            serde_json::from_slice(&std::fs::read(cache.path("source:v1"))?)?;
        value["value"] = serde_json::json!([9]);
        std::fs::write(cache.path("source:v1"), serde_json::to_vec(&value)?)?;
        assert!(cache.get::<Vec<u32>>("source:v1")?.is_none());
        cache.put("source:v1", &vec![1])?;
        assert!(
            Cache::new(dir.path(), 0)?
                .get::<Vec<u32>>("source:v1")?
                .is_none()
        );
        Ok(())
    }
}
