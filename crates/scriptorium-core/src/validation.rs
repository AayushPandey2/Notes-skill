//! Local artifact audit and create-only transactional collection publication.
//! Structural checks do not replace scientific, license, or pedagogical review.
use crate::planning::{KnowledgePlan, VisualState, build_plan};
use anyhow::{Context, Result, anyhow, bail, ensure};
use pulldown_cmark::{Event, Parser, Tag};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::{
    collections::{BTreeMap, BTreeSet},
    fs,
    io::Write,
    path::{Component, Path, PathBuf},
};

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct VisualReceipt {
    pub visual_id: String,
    /// Local path relative to the vault root, regardless of note link policy.
    pub local_path: PathBuf,
    pub sha256: String,
    pub provenance: serde_json::Value,
    pub state: VisualState,
}

#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct AuditReport {
    pub planned_visuals: usize,
    pub verified_assets: usize,
    pub embedded_visuals: usize,
    pub fulfilled_visual_ids: Vec<String>,
    pub missing_representations: Vec<String>,
    pub errors: Vec<String>,
    pub warnings: Vec<String>,
    pub artifact_complete: bool,
    /// This engine checks artifact contracts, not the truth of educational claims.
    pub educational_review_required: bool,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct NoteDraft {
    pub path: PathBuf,
    pub content: String,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct PublicationManifest {
    pub schema_version: u32,
    pub collection_path: PathBuf,
    pub plan_sha256: String,
    pub notes: BTreeMap<PathBuf, String>,
    pub visuals: Vec<VisualReceipt>,
    pub audit: AuditReport,
    pub publication_state: String,
}

/// Reject absolute paths on every platform, including Windows syntax on Unix.
pub fn relative_path(path: &Path) -> Result<()> {
    let text = path.to_string_lossy();
    ensure!(
        !text.is_empty()
            && !text.contains([':', '\0', '\n', '\r'])
            && (cfg!(windows) || !text.contains('\\')),
        "unsafe relative path"
    );
    ensure!(
        path.components().all(|c| matches!(c, Component::Normal(_))),
        "path must have only normal relative components"
    );
    Ok(())
}

/// Resolve existing ancestors too: a not-yet-existing leaf may not escape via a
/// symlinked directory. Canonicalization also handles Windows junctions.
pub fn safe_path(vault: &Path, relative: &Path, must_exist: bool) -> Result<PathBuf> {
    relative_path(relative)?;
    let root = vault.canonicalize().context("vault must exist")?;
    let target = root.join(relative);
    let mut ancestor = target.as_path();
    loop {
        match fs::symlink_metadata(ancestor) {
            Ok(_) => break,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                ancestor = ancestor.parent().ok_or_else(|| anyhow!("invalid path"))?;
            }
            Err(e) => return Err(e.into()),
        }
    }
    ensure!(
        ancestor.canonicalize()?.starts_with(&root),
        "path escapes vault through a symlink"
    );
    if must_exist {
        let resolved = target
            .canonicalize()
            .context("local artifact does not exist")?;
        ensure!(resolved.starts_with(&root), "artifact escapes vault");
        return Ok(resolved);
    }
    Ok(target)
}

fn hash(bytes: &[u8]) -> String {
    hex::encode(Sha256::digest(bytes))
}

struct Properties(BTreeMap<String, serde_yaml_ng::Value>);
impl<'de> Deserialize<'de> for Properties {
    fn deserialize<D: serde::Deserializer<'de>>(d: D) -> std::result::Result<Self, D::Error> {
        struct Visitor;
        impl<'de> serde::de::Visitor<'de> for Visitor {
            type Value = Properties;
            fn expecting(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
                f.write_str("unique YAML property mapping")
            }
            fn visit_map<M: serde::de::MapAccess<'de>>(
                self,
                mut map: M,
            ) -> std::result::Result<Self::Value, M::Error> {
                let mut out = BTreeMap::new();
                while let Some((k, v)) = map.next_entry::<String, serde_yaml_ng::Value>()? {
                    if out.insert(k.clone(), v).is_some() {
                        return Err(serde::de::Error::custom(format!("duplicate property {k}")));
                    }
                }
                Ok(Properties(out))
            }
        }
        d.deserialize_map(Visitor)
    }
}

pub fn validate_properties(markdown: &str) -> Result<()> {
    let mut lines = markdown.lines();
    ensure!(
        lines.next() == Some("---"),
        "note must start with YAML Properties on line one"
    );
    let mut yaml = String::new();
    let mut closed = false;
    for line in lines {
        if line == "---" {
            closed = true;
            break;
        }
        yaml.push_str(line);
        yaml.push('\n');
    }
    ensure!(closed, "unterminated YAML Properties");
    let properties: Properties =
        serde_yaml_ng::from_str(&yaml).context("invalid YAML Properties")?;
    let p = properties.0;
    let legacy = ["id", "aliases", "topic", "tags", "nexttopics"];
    let modern = ["topic", "tags", "master_topic", "domain", "note_type"];
    let legacy_mode = p.len() == 5 && legacy.iter().all(|key| p.contains_key(*key));
    let keys = if legacy_mode { &legacy } else { &modern };
    for key in keys {
        let v = p
            .get(*key)
            .ok_or_else(|| anyhow!("missing required property {key}"))?;
        if ["tags", "aliases", "nexttopics"].contains(key) {
            let items = v
                .as_sequence()
                .ok_or_else(|| anyhow!("{key} must be a YAML sequence"))?;
            ensure!(
                items
                    .iter()
                    .all(|x| x.as_str().is_some_and(|s| !s.trim().is_empty())),
                "{key} must contain nonempty strings"
            );
        } else {
            ensure!(
                v.as_str().is_some_and(|s| !s.trim().is_empty()),
                "{key} must be a nonempty string"
            );
        }
    }
    if let Some(kind) = p.get("note_type").and_then(|v| v.as_str()) {
        ensure!(
            [
                "deep-notes",
                "study-notes",
                "quick-reference",
                "worked-solutions",
                "implementation-guide",
                "assessment",
                "synthesis-revision",
                "index"
            ]
            .contains(&kind),
            "unsupported note_type"
        );
    }
    Ok(())
}

/// Extract standard inline/reference images and Obsidian embeds while ignoring
/// fenced and inline code examples. HTML embeds are deliberately unsupported.
pub fn image_targets(markdown: &str) -> Result<Vec<String>> {
    let mut targets = Vec::new();
    let mut code = Vec::new();
    let mut block_start = None;
    for (event, range) in Parser::new(markdown).into_offset_iter() {
        match event {
            Event::Start(Tag::Image { dest_url, .. }) => targets.push(dest_url.to_string()),
            Event::Start(Tag::CodeBlock(_)) => block_start = Some(range.start),
            Event::End(pulldown_cmark::TagEnd::CodeBlock) => {
                if let Some(start) = block_start.take() {
                    code.push(start..range.end);
                }
            }
            Event::Code(_) => code.push(range),
            Event::Html(html) | Event::InlineHtml(html) => {
                let lower = html.to_ascii_lowercase();
                ensure!(
                    !lower.contains("<img")
                        && !lower.contains("<object")
                        && !lower.contains("<iframe")
                        && !lower.contains("<svg"),
                    "HTML media embeds require an explicit supported local artifact adapter"
                );
            }
            _ => (),
        }
    }
    let mut offset = 0;
    while let Some(i) = markdown[offset..].find("![[") {
        let start = offset + i;
        if let Some(block) = code.iter().find(|r| r.contains(&start)) {
            offset = block.end;
            continue;
        }
        let escapes = markdown[..start]
            .bytes()
            .rev()
            .take_while(|b| *b == b'\\')
            .count();
        if escapes % 2 == 1 {
            offset = start + 3;
            continue;
        }
        if let Some(end) = markdown[start + 3..].find("]]") {
            let finish = start + 3 + end;
            if !code.iter().any(|r| r.contains(&start)) {
                let target = markdown[start + 3..finish]
                    .split('|')
                    .next()
                    .unwrap_or("")
                    .trim();
                ensure!(!target.is_empty(), "empty Obsidian embed");
                targets.push(target.into());
            }
            offset = finish + 2;
        } else {
            bail!("unterminated Obsidian embed");
        }
    }
    targets.sort();
    targets.dedup();
    Ok(targets)
}

fn decode_path(target: &str) -> Result<PathBuf> {
    ensure!(
        !target.starts_with(['#', '/', '\\']),
        "image must reference a vault-local file"
    );
    ensure!(
        !target.contains("://") && !target.starts_with("data:"),
        "remote image hotlinks are forbidden"
    );
    let target = target.split('#').next().unwrap_or("");
    let bytes = target.as_bytes();
    let mut decoded = Vec::new();
    let mut i = 0;
    while i < bytes.len() {
        if bytes[i] == b'%' {
            ensure!(i + 2 < bytes.len(), "invalid URL encoding");
            let nibble = |b: u8| -> Result<u8> {
                match b {
                    b'0'..=b'9' => Ok(b - b'0'),
                    b'a'..=b'f' => Ok(b - b'a' + 10),
                    b'A'..=b'F' => Ok(b - b'A' + 10),
                    _ => bail!("invalid URL encoding"),
                }
            };
            decoded.push(nibble(bytes[i + 1])? * 16 + nibble(bytes[i + 2])?);
            i += 3;
        } else {
            decoded.push(bytes[i]);
            i += 1;
        }
    }
    let path = PathBuf::from(String::from_utf8(decoded).context("image path is not UTF-8")?);
    let text = path.to_string_lossy();
    ensure!(
        !text.is_empty()
            && !text.contains([':', '\0', '\n', '\r'])
            && (cfg!(windows) || !text.contains('\\')),
        "unsafe image link path"
    );
    ensure!(
        path.components().all(|c| matches!(
            c,
            Component::Normal(_) | Component::ParentDir | Component::CurDir
        )),
        "image link must be relative"
    );
    Ok(path)
}

fn note_relative(note: &Path, link: &Path) -> Result<PathBuf> {
    let mut result = note.parent().unwrap_or(Path::new("")).to_path_buf();
    for c in link.components() {
        match c {
            Component::Normal(c) => result.push(c),
            Component::CurDir => (),
            Component::ParentDir => ensure!(result.pop(), "image link escapes vault root"),
            _ => bail!("image link must be relative"),
        }
    }
    relative_path(&result)?;
    Ok(result)
}

fn resolve_image(vault: &Path, note: &Path, target: &str) -> Result<PathBuf> {
    let relative = decode_path(target)?;
    // Obsidian root-relative links and standard note-relative Markdown links.
    let root = safe_path(vault, &relative, true).ok();
    let nearby = note_relative(note, &relative)
        .and_then(|p| safe_path(vault, &p, true))
        .ok();
    match (root, nearby) {
        (Some(a), Some(b)) => {
            ensure!(a == b, "ambiguous image link {target}");
            Ok(a)
        }
        (Some(a), None) | (None, Some(a)) => Ok(a),
        _ => bail!("missing or unsafe local image {target}"),
    }
}

fn inspect_local(path: &Path) -> Result<Vec<u8>> {
    ensure!(
        fs::metadata(path)?.len() <= crate::assets::MAX_BYTES as u64,
        "local image exceeds byte limit"
    );
    let bytes = fs::read(path)?;
    let mime = match path
        .extension()
        .and_then(|x| x.to_str())
        .map(str::to_ascii_lowercase)
        .as_deref()
    {
        Some("png") => "image/png",
        Some("jpg" | "jpeg") => "image/jpeg",
        Some("webp") => "image/webp",
        Some("svg") => "image/svg+xml",
        _ => bail!("unsupported local image format"),
    };
    crate::assets::inspect_image(&bytes, mime)?;
    Ok(bytes)
}

fn verified_receipt_path(vault: &Path, receipt: &VisualReceipt) -> Result<PathBuf> {
    ensure!(
        receipt.state >= VisualState::Verified,
        "asset has not reached verified stage"
    );
    let provenance: crate::assets::Provenance =
        serde_json::from_value(receipt.provenance.clone()).context("invalid asset provenance")?;
    provenance.validate()?;
    let path = safe_path(vault, &receipt.local_path, true)?;
    let bytes = inspect_local(&path)?;
    ensure!(
        hash(&bytes) == receipt.sha256,
        "asset content hash mismatch"
    );
    Ok(path)
}

fn atomic_json_new(path: &Path, value: &impl Serialize) -> Result<()> {
    let parent = path
        .parent()
        .ok_or_else(|| anyhow!("manifest requires a parent directory"))?;
    let mut staged = tempfile::NamedTempFile::new_in(parent)?;
    staged.write_all(&serde_json::to_vec_pretty(value)?)?;
    staged.as_file().sync_all()?;
    staged.persist_noclobber(path).map_err(|e| e.error)?;
    Ok(())
}

fn audit(
    vault: &Path,
    plan: &KnowledgePlan,
    receipts: &[VisualReceipt],
    drafts: &BTreeMap<PathBuf, String>,
) -> Result<AuditReport> {
    let plan = build_plan(plan.clone())?;
    let mut report = AuditReport {
        planned_visuals: plan.visuals.len(),
        warnings: plan.planning_warnings.clone(),
        educational_review_required: true,
        ..AuditReport::default()
    };
    let mut records = BTreeMap::new();
    for receipt in receipts {
        ensure!(
            records.insert(&receipt.visual_id, receipt).is_none(),
            "duplicate visual receipt {}",
            receipt.visual_id
        );
        ensure!(
            plan.visuals.iter().any(|v| v.need.id == receipt.visual_id),
            "receipt refers to unplanned visual"
        );
    }
    let mut note_paths: BTreeSet<PathBuf> = plan
        .visuals
        .iter()
        .map(|v| PathBuf::from(&v.need.placement))
        .collect();
    note_paths.extend(drafts.keys().cloned());
    note_paths.extend(plan.notes.iter().map(PathBuf::from));
    if note_paths.is_empty() {
        report
            .errors
            .push("No note paths supplied; an empty audit cannot establish publication".into());
    }
    let registered_paths: BTreeSet<_> = receipts
        .iter()
        .filter_map(|r| verified_receipt_path(vault, r).ok())
        .collect();
    let mut embeds = BTreeMap::new();
    for note in note_paths {
        relative_path(&note)?;
        let result: Result<_> = (|| {
            let content = if let Some(content) = drafts.get(&note) {
                content.clone()
            } else {
                fs::read_to_string(safe_path(vault, &note, true)?)?
            };
            validate_properties(&content)?;
            image_targets(&content)?.iter().map(|t| {
                let path = resolve_image(vault, &note, t)?;
                inspect_local(&path)?;
                ensure!(registered_paths.contains(&path), "embedded image has no verified registry record with matching hash and provenance: {t}");
                Ok(path)
            }).collect::<Result<BTreeSet<_>>>()
        })();
        match result {
            Ok(paths) => {
                embeds.insert(note, paths);
            }
            Err(e) => report.errors.push(format!("{}: {e:#}", note.display())),
        }
    }
    let mut hashes = BTreeMap::new();
    for visual in &plan.visuals {
        let result: Result<_> = (|| {
            let r = records
                .get(&visual.need.id)
                .ok_or_else(|| anyhow!("no fulfillment receipt"))?;
            let asset = verified_receipt_path(vault, r)?;
            report.verified_assets += 1;
            if let Some(old) = hashes.insert(r.sha256.clone(), visual.need.id.clone()) {
                report.warnings.push(format!(
                    "{} and {} share one asset; review whether representations are complementary",
                    old, visual.need.id
                ));
            }
            ensure!(
                embeds
                    .get(Path::new(&visual.need.placement))
                    .is_some_and(|s| s.contains(&asset)),
                "asset is not embedded at its required placement"
            );
            Ok(())
        })();
        match result {
            Ok(()) => {
                report.embedded_visuals += 1;
                report.fulfilled_visual_ids.push(visual.need.id.clone());
            }
            Err(e) if visual.need.required => {
                report.missing_representations.push(visual.need.id.clone());
                report.errors.push(format!("{}: {e:#}", visual.need.id));
            }
            Err(e) => report
                .warnings
                .push(format!("optional {}: {e:#}", visual.need.id)),
        }
    }
    report.artifact_complete = report.errors.is_empty();
    Ok(report)
}

pub fn audit_collection(
    vault: &Path,
    plan: &KnowledgePlan,
    receipts: &[VisualReceipt],
) -> Result<AuditReport> {
    audit(vault, plan, receipts, &BTreeMap::new())
}

/// Publish a fresh collection directory with one atomic rename. Existing
/// collections require a separately reviewed incremental-update operation.
/// A prepared manifest is a crash-recovery journal, never a completion claim.
pub fn publish_collection(
    vault: &Path,
    destination: &Path,
    plan: &KnowledgePlan,
    receipts: &[VisualReceipt],
    drafts: &[NoteDraft],
) -> Result<PublicationManifest> {
    ensure!(!drafts.is_empty(), "cannot publish an empty collection");
    let destination_path = safe_path(vault, destination, false)?;
    ensure!(
        !destination_path.exists(),
        "publication destination already exists; refusing to overwrite"
    );
    let mut contents = BTreeMap::new();
    for draft in drafts {
        relative_path(&draft.path)?;
        ensure!(
            draft.path.starts_with(destination) && draft.path != destination,
            "draft must be inside collection destination"
        );
        ensure!(
            draft.path.extension().is_some_and(|e| e == "md"),
            "draft is not Markdown"
        );
        ensure!(
            contents
                .insert(draft.path.clone(), draft.content.clone())
                .is_none(),
            "duplicate draft path"
        );
    }
    for v in &plan.visuals {
        let placement = Path::new(&v.need.placement);
        ensure!(
            placement.starts_with(destination),
            "visual placement must be inside published collection"
        );
        if v.need.required {
            ensure!(
                contents.contains_key(placement),
                "required visual placement is not among submitted drafts"
            );
        }
    }
    let audit = audit(vault, plan, receipts, &contents)?;
    ensure!(
        audit.artifact_complete,
        "publication blocked: {}",
        audit.errors.join("; ")
    );
    let plan_sha256 = hash(&serde_json::to_vec(plan)?);
    let note_hashes = contents
        .iter()
        .map(|(p, c)| (p.clone(), hash(c.as_bytes())))
        .collect::<BTreeMap<_, _>>();
    let mut manifest = PublicationManifest {
        schema_version: 1,
        collection_path: destination.into(),
        plan_sha256,
        notes: note_hashes,
        visuals: receipts.to_vec(),
        audit,
        publication_state: "prepared".into(),
    };
    let registry = safe_path(vault, Path::new(".scriptorium/manifests"), false)?;
    fs::create_dir_all(&registry)?;
    let registry = safe_path(vault, Path::new(".scriptorium/manifests"), true)?;
    let identity = hash(&serde_json::to_vec(&(
        destination,
        &manifest.notes,
        &manifest.plan_sha256,
    ))?);
    let prepared_path = registry.join(format!("{identity}.prepared.json"));
    let committed_path = registry.join(format!("{identity}.json"));
    ensure!(
        !prepared_path.exists() && !committed_path.exists(),
        "publication journal already exists; inspect prior attempt"
    );
    let parent = destination_path
        .parent()
        .ok_or_else(|| anyhow!("invalid destination parent"))?;
    fs::create_dir_all(parent)?;
    safe_path(vault, destination, false)?;
    let stage = tempfile::Builder::new()
        .prefix(".scriptorium-publish-")
        .tempdir_in(parent)?;
    for (path, content) in &contents {
        let staged = stage.path().join(path.strip_prefix(destination)?);
        fs::create_dir_all(
            staged
                .parent()
                .ok_or_else(|| anyhow!("invalid draft path"))?,
        )?;
        let mut file = fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(staged)?;
        file.write_all(content.as_bytes())?;
        file.sync_all()?;
    }
    atomic_json_new(&prepared_path, &manifest)?;
    // Both paths are on the same filesystem. Never merge directories or replace
    // existing notes. Prepared journal remains inspectable after a crash.
    ensure!(
        !destination_path.exists(),
        "publication destination appeared during staging"
    );
    fs::rename(stage.path(), &destination_path)
        .context("atomic collection rename failed; prepared journal retained")?;
    manifest.publication_state = "published".into();
    for receipt in &mut manifest.visuals {
        if manifest
            .audit
            .fulfilled_visual_ids
            .contains(&receipt.visual_id)
        {
            receipt.state = VisualState::Published;
        }
    }
    atomic_json_new(&committed_path, &manifest).context(
        "notes published but committed manifest could not be persisted; inspect prepared journal",
    )?;
    fs::remove_file(prepared_path)?;
    Ok(manifest)
}

#[cfg(test)]
mod tests {
    use super::*;
    fn note() -> String {
        "---\ntopic: Circuits\ntags: [topic/circuits]\nmaster_topic: Physics\ndomain: Engineering\nnote_type: deep-notes\n---\n# Current\n".into()
    }
    fn plan() -> KnowledgePlan {
        serde_json::from_value(serde_json::json!({"topic":"Circuits", "concepts":[{"id":"current","title":"Current", "objectives":["Explain current"]}]})).unwrap()
    }
    #[test]
    fn properties_are_typed_and_unique() {
        validate_properties(&note()).unwrap();
        assert!(
            validate_properties(&note().replace("tags: [topic/circuits]", "tags: circuits"))
                .is_err()
        );
        assert!(
            validate_properties(
                &note().replace("topic: Circuits", "topic: Circuits\ntopic: Duplicate")
            )
            .is_err()
        );
        validate_properties(
            "---\nid: note\naliases: []\ntopic: Circuits\ntags: []\nnexttopics: []\n---\n",
        )
        .unwrap();
    }
    #[test]
    fn parser_ignores_code_and_handles_reference_images() {
        let s = "![plot][p]\n\n[p]: assets/plot.png\n\n`![[fake.png]]`\n```md\n![[fake2.png]]\n```\n![[assets/local.png|400]]";
        assert_eq!(
            image_targets(s).unwrap(),
            vec!["assets/local.png", "assets/plot.png"]
        );
        assert!(
            image_targets("`![[unfinished`\n\\![[escaped.png]]")
                .unwrap()
                .is_empty()
        );
    }
    #[test]
    fn rejects_hotlinks_and_encoded_traversal() {
        assert!(decode_path("https://example.org/image.png").is_err());
        assert!(
            note_relative(
                Path::new("root.md"),
                &decode_path("%2e%2e/secret.png").unwrap()
            )
            .is_err()
        );
        assert!(decode_path("C:%5csecret.png").is_err());
    }
    #[test]
    fn permits_contained_parent_relative_image_paths() {
        let vault = tempfile::tempdir().unwrap();
        fs::create_dir(vault.path().join("assets")).unwrap();
        fs::write(vault.path().join("assets/plot.png"), b"resolved path only").unwrap();
        let path = resolve_image(
            vault.path(),
            Path::new("Topic/note.md"),
            "../assets/plot.png",
        )
        .unwrap();
        assert_eq!(
            path,
            vault.path().join("assets/plot.png").canonicalize().unwrap()
        );
        assert!(
            resolve_image(
                vault.path(),
                Path::new("Topic/note.md"),
                "../../outside.png"
            )
            .is_err()
        );
    }
    #[test]
    fn missing_embeds_block_publication_and_fresh_publish_is_atomic() {
        let vault = tempfile::tempdir().unwrap();
        let drafts = vec![NoteDraft {
            path: "Collection/01.md".into(),
            content: note() + "![missing](assets/missing.png)",
        }];
        assert!(
            publish_collection(vault.path(), Path::new("Collection"), &plan(), &[], &drafts)
                .is_err()
        );
        assert!(!vault.path().join("Collection").exists());
        let drafts = vec![NoteDraft {
            path: "Collection/01.md".into(),
            content: note(),
        }];
        let result =
            publish_collection(vault.path(), Path::new("Collection"), &plan(), &[], &drafts)
                .unwrap();
        assert_eq!(result.publication_state, "published");
        assert!(vault.path().join("Collection/01.md").is_file());
        assert!(
            publish_collection(vault.path(), Path::new("Collection"), &plan(), &[], &drafts)
                .is_err()
        );
    }
    #[test]
    fn required_placements_must_belong_to_submitted_collection() {
        let vault = tempfile::tempdir().unwrap();
        let mut p = plan();
        p.visuals.push(serde_json::from_value(serde_json::json!({
            "id":"outside", "concept_id":"current", "objective":"Trace flow", "category":"information_flow",
            "description":"Trace current", "required_information":["Flow direction"], "renderer":"graph", "family":"engineering_systems",
            "verification_method":"Review graph", "placement":"Outside/note.md"
        })).unwrap());
        let drafts = vec![NoteDraft {
            path: "Collection/01.md".into(),
            content: note(),
        }];
        assert!(
            publish_collection(vault.path(), Path::new("Collection"), &p, &[], &drafts)
                .unwrap_err()
                .to_string()
                .contains("inside published collection")
        );
        p.visuals[0].need.placement = "Collection/missing.md".into();
        assert!(
            publish_collection(vault.path(), Path::new("Collection"), &p, &[], &drafts)
                .unwrap_err()
                .to_string()
                .contains("not among submitted drafts")
        );
    }
    #[test]
    fn safe_paths_reject_foreign_absolute_paths() {
        for path in [
            "../secret",
            "/secret",
            "C:/secret",
            "\\\\host\\share",
            "a/../b",
        ] {
            assert!(relative_path(Path::new(path)).is_err());
        }
    }
    #[test]
    fn an_empty_audit_cannot_claim_a_collection_exists() {
        let vault = tempfile::tempdir().unwrap();
        assert!(
            !audit_collection(vault.path(), &plan(), &[])
                .unwrap()
                .artifact_complete
        );
        let mut p = plan();
        p.notes.push("Missing/01.md".into());
        assert!(
            !audit_collection(vault.path(), &p, &[])
                .unwrap()
                .artifact_complete
        );
    }
    #[test]
    fn a_valid_image_without_provenance_cannot_be_published() {
        let vault = tempfile::tempdir().unwrap();
        fs::create_dir(vault.path().join("assets")).unwrap();
        let mut bytes = std::io::Cursor::new(Vec::new());
        image::DynamicImage::new_rgb8(16, 16)
            .write_to(&mut bytes, image::ImageFormat::Png)
            .unwrap();
        fs::write(
            vault.path().join("assets/unregistered.png"),
            bytes.into_inner(),
        )
        .unwrap();
        let drafts = vec![NoteDraft {
            path: "Topic/01.md".into(),
            content: note() + "![unregistered](assets/unregistered.png)",
        }];
        let err = publish_collection(vault.path(), Path::new("Topic"), &plan(), &[], &drafts)
            .unwrap_err();
        assert!(err.to_string().contains("no verified registry record"));
        assert!(!vault.path().join("Topic").exists());
    }
    #[test]
    fn manifest_creation_never_overwrites_an_existing_journal() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("manifest.json");
        let original = serde_json::json!({"state":"published","notes":["one.md"]});
        atomic_json_new(&path, &original).unwrap();
        assert!(atomic_json_new(&path, &serde_json::json!({"state":"different"})).is_err());
        let actual: serde_json::Value = serde_json::from_slice(&fs::read(path).unwrap()).unwrap();
        assert_eq!(actual, original);
    }
    #[test]
    fn complementary_assets_are_published_and_tampering_is_detected() {
        let vault = tempfile::tempdir().unwrap();
        let store = crate::assets::AssetStore::new(vault.path(), "attachments/circuits").unwrap();
        let specifications = [
            serde_json::json!({"renderer":"scientific","objective":"Voltage scales current","data":{"resistor":[[0,0],[1,2],[2,4]]},"xlabel":"Current","ylabel":"Voltage","units":"A and V","interpretation":"The slope is resistance"}),
            serde_json::json!({"renderer":"graph","objective":"Trace circuit flow","nodes":[{"id":"source","label":"Voltage source"},{"id":"load","label":"Resistive load"}],"edges":[{"source":"source","target":"load"}]}),
        ];
        let mut p = plan();
        p.concepts[0].complexity = 4;
        let mut receipts = Vec::new();
        let mut content = note();
        for (i, spec) in specifications.iter().enumerate() {
            let id = format!("current.visual-{i}");
            let rendered = crate::rendering::render(spec).unwrap();
            let record = store
                .store_generated(&rendered, spec["objective"].as_str().unwrap())
                .unwrap();
            content.push_str(
                &store
                    .embed(&record, spec["objective"].as_str().unwrap())
                    .unwrap(),
            );
            content.push('\n');
            p.visuals.push(serde_json::from_value(serde_json::json!({
                "id":id,"concept_id":"current","objective":spec["objective"],
                "category":if i==0 {"numerical_plot"} else {"information_flow"},
                "description":"An explicit educational representation", "required_information":["Current direction and voltage relation"],
                "renderer":spec["renderer"], "family":"engineering_systems", "verification_method":"Inspect validated rendering inputs and decoded local file",
                "placement":"Circuits/01.md", "required":true
            })).unwrap());
            receipts.push(VisualReceipt {
                visual_id: id,
                local_path: record.local_path,
                sha256: record.sha256,
                provenance: serde_json::to_value(record.provenance).unwrap(),
                state: VisualState::Verified,
            });
        }
        let p = build_plan(p).unwrap();
        assert!(p.planning_warnings.is_empty());
        let drafts = vec![NoteDraft {
            path: "Circuits/01.md".into(),
            content,
        }];
        let published =
            publish_collection(vault.path(), Path::new("Circuits"), &p, &receipts, &drafts)
                .unwrap();
        assert_eq!(published.audit.embedded_visuals, 2);
        assert!(
            published
                .visuals
                .iter()
                .all(|r| r.state == VisualState::Published)
        );
        assert!(
            audit_collection(vault.path(), &p, &receipts)
                .unwrap()
                .artifact_complete
        );
        let first = vault.path().join(&receipts[0].local_path);
        fs::write(first, b"broken").unwrap();
        assert!(
            !audit_collection(vault.path(), &p, &receipts)
                .unwrap()
                .artifact_complete
        );
        assert!(
            !audit_collection(vault.path(), &p, &[])
                .unwrap()
                .artifact_complete
        );
    }
}
