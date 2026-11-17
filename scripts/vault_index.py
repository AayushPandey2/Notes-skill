#!/usr/bin/env python3
"""Content-aware, vault-aware, read-only Obsidian metadata, template & tag indexer.

Supports:
  - Legacy compact note-array output:
      python3 scripts/vault_index.py "<vault_path>" [--topic "<filter>"]
  - Compact topic-scoped discovery bundle (templates, tags, collisions, placement):
      python3 scripts/vault_index.py "<vault_path>" --discover [--topic "<filter>"]
  - Full registry export (all templates & tags):
      python3 scripts/vault_index.py "<vault_path>" --full-registry

Security & read-only guarantees:
  - Resolves vault canonically; rejects '..' traversal and symlinks escaping vault.
  - Excludes .git, .trash, scratchpad, node_modules, __pycache__, and .obsidian
    note scanning (reads only .obsidian/templates.json and templater data.json).
  - Never executes plugin JavaScript, Templater JS, or Dataview queries.
  - Stores index cache outside the vault (~/.cache/scriptorium/) unless --cache-dir is set.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

import yaml

INDEX_VERSION = 2

EXCLUDED_DIRS = {".git", ".trash", ".obsidian", "scratchpad", "node_modules", "__pycache__"}
COMMON_TEMPLATE_DIRS = {"templates", "_templates", "meta/templates", "00 - templates", "00-templates"}

TEMPLATER_RE = re.compile(r"<%[\s\S]*?%>")
CORE_TEMPLATE_RE = re.compile(r"\{\{(?:date|time|title|folder|author)(?::[^}]*)?\}\}", flags=re.IGNORECASE)
DATAVIEW_FENCE_RE = re.compile(r"```dataview(?:js)?\b", flags=re.IGNORECASE)
DATAVIEW_INLINE_RE = re.compile(r"`=[^`]+`")


# ---------------------------------------------------------------------------
# Vault Path Resolution & Containment
# ---------------------------------------------------------------------------

def resolve_vault_root(explicit_path: str | Path | None = None) -> Path:
    """Resolve and validate vault root from explicit arg, env, or ~/.scriptorium-config.json."""
    candidate = explicit_path or os.environ.get("SCRIPTORIUM_VAULT_PATH")
    if not candidate:
        cfg = Path.home() / ".scriptorium-config.json"
        if cfg.is_file():
            try:
                data = json.loads(cfg.read_text(encoding="utf-8"))
                candidate = data.get("vault_path")
            except (OSError, json.JSONDecodeError) as exc:
                raise ValueError(f"Failed reading vault config '{cfg}': {exc}") from exc
    if not candidate:
        raise ValueError("Vault path not provided and neither SCRIPTORIUM_VAULT_PATH nor ~/.scriptorium-config.json is set.")

    raw = Path(os.path.expanduser(str(candidate)))
    if not raw.exists():
        raise FileNotFoundError(f"Vault path does not exist: {raw}")
    resolved = Path(os.path.realpath(raw))
    if not resolved.is_dir():
        raise NotADirectoryError(f"Vault path is not a directory: {resolved}")
    return resolved


def is_within_vault(vault_root: Path, target: Path) -> bool:
    """Verify target resolves strictly inside vault_root (no symlink escape)."""
    try:
        real_root = os.path.realpath(vault_root)
        real_target = os.path.realpath(target)
        return os.path.commonpath([real_root, real_target]) == real_root
    except ValueError:
        return False


def _iter_vault_markdown(vault_root: Path) -> tuple[list[Path], list[str]]:
    """Walk vault_root safely without following escaping symlinks or excluded dirs."""
    md_files: list[Path] = []
    warnings: list[str] = []
    for dirpath, dirnames, filenames in os.walk(vault_root, followlinks=False):
        kept: list[str] = []
        for d in sorted(dirnames):
            if d.lower() in EXCLUDED_DIRS or d.startswith("."):
                continue
            cand_dir = Path(dirpath) / d
            if cand_dir.is_symlink() and not is_within_vault(vault_root, cand_dir):
                warnings.append(f"Skipped escaping directory symlink: {cand_dir.relative_to(vault_root).as_posix()}")
                continue
            kept.append(d)
        dirnames[:] = kept

        for fname in sorted(filenames):
            if not fname.lower().endswith(".md"):
                continue
            full = Path(dirpath) / fname
            if full.is_symlink() and not is_within_vault(vault_root, full):
                warnings.append(f"Skipped escaping file symlink: {full.relative_to(vault_root).as_posix()}")
                continue
            md_files.append(full)

    md_files.sort(key=lambda p: p.relative_to(vault_root).as_posix().lower())
    return md_files, warnings


# ---------------------------------------------------------------------------
# Frontmatter, Headings, Tags & Links Extraction
# ---------------------------------------------------------------------------

def _split_frontmatter(text: str) -> tuple[str | None, int]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 0
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "\n".join(lines[1:idx]), idx + 1
    return None, 0


def _as_str_or_none(val: Any) -> str | None:
    if val is None:
        return None
    if isinstance(val, list):
        items = [str(x).strip() for x in val if x is not None and str(x).strip()]
        return items[0] if len(items) == 1 else (", ".join(items) if items else None)
    s = str(val).strip()
    return s if s else None


def _as_str_list(val: Any) -> list[str]:
    if not isinstance(val, list):
        if isinstance(val, str) and val.strip():
            return [x.strip() for x in re.split(r"[,;\s]+", val.strip()) if x.strip()]
        return []
    return [str(x).strip() for x in val if x is not None and str(x).strip()]


def _extract_yaml_tags(meta: dict[str, Any]) -> list[str]:
    raw_tags: list[str] = []
    for key in ("tags", "tag"):
        val = meta.get(key)
        if isinstance(val, list):
            for item in val:
                if item is not None:
                    s = str(item).strip().lstrip("#")
                    if s:
                        raw_tags.append(s)
        elif isinstance(val, str) and val.strip():
            for part in re.split(r"[,\s]+", val.strip()):
                s = part.strip().lstrip("#")
                if s:
                    raw_tags.append(s)
    return list(dict.fromkeys(raw_tags))


def _extract_body_structure(text: str, start_idx: int) -> dict[str, Any]:
    """Extract H2 headings, inline tags, wikilinks, and block IDs safely."""
    lines = text.splitlines()[start_idx:]
    headings: list[str] = []
    inline_tags: list[str] = []
    links: list[str] = []
    block_ids: list[str] = []

    in_fence = False
    fence_char = ""
    fence_len = 0
    in_comment = False

    for raw_line in lines:
        stripped = raw_line.strip()
        m_fence = re.match(r"^\s*(`{3,}|~{3,})", raw_line)
        if m_fence:
            marker = m_fence.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_len = len(marker)
                continue
            if marker[0] == fence_char and len(marker) >= fence_len and stripped[len(marker) :].strip() == "":
                in_fence = False
                continue
        if in_fence:
            continue

        if in_comment:
            if "-->" in raw_line:
                in_comment = False
            continue
        if stripped.startswith("<!--"):
            if "-->" not in stripped[4:]:
                in_comment = True
            # Strip inline comments on same line
            raw_line = re.sub(r"<!--.*?-->", " ", raw_line)

        m_h2 = re.match(r"^##\s+(.+?)\s*$", raw_line)
        if m_h2:
            headings.append(m_h2.group(1).strip())

        m_blk = re.search(r"(?:^|\s)\^([A-Za-z0-9-]+)\s*$", raw_line)
        if m_blk:
            block_ids.append(m_blk.group(1))

        # Collect wikilinks
        for m_wl in re.finditer(r"\[\[([^\]]+)\]\]", raw_line):
            target = re.split(r"\\?\|", m_wl.group(1), maxsplit=1)[0].split("#", 1)[0].strip()
            if target:
                links.append(target)

        # Inline tags: skip Markdown heading lines, strip inline comments, code, URLs, link destinations, escaped \#
        if re.match(r"^\s*#{1,6}\s+", raw_line):
            continue
        line_clean = re.sub(r"<!--.*?-->", " ", raw_line)
        line_clean = re.sub(r"`[^`]*`", " ", line_clean)
        line_clean = re.sub(r"https?://\S+", " ", line_clean)
        line_clean = re.sub(r"\]\([^)]+\)", "]()", line_clean)
        line_clean = line_clean.replace(r"\#", "  ")
        for m_tag in re.finditer(r"(?:^|(?<=[\s(\[{]))#([^\s#.,;:!?()\[\]{}\"']+)", line_clean, flags=re.UNICODE):
            tag = m_tag.group(1).strip("/")
            # Obsidian tags must contain at least one non-numeric character
            if tag and not tag.isdigit() and any(ch.isalpha() or ch in "-_/" for ch in tag):
                inline_tags.append(tag)

    return {
        "headings": headings,
        "inline_tags": inline_tags,
        "links": list(dict.fromkeys(links)),
        "block_ids": list(dict.fromkeys(block_ids)),
    }


def _normalize_tag_key(tag: str) -> str:
    """Normalized comparison key for collision detection (never mutates original tag)."""
    k = tag.strip().lower().replace("_", "-")
    if len(k) > 3 and k.endswith("s") and not k.endswith("ss"):
        k = k[:-1]
    return k


def _tag_style(tag: str) -> str:
    if "/" in tag:
        return "nested"
    if "_" in tag:
        return "snake"
    if "-" in tag:
        return "kebab"
    if any(c.isupper() for c in tag[1:]) and tag[0].islower():
        return "camel"
    return "plain"


# ---------------------------------------------------------------------------
# Template Discovery (Read-Only, Never Executes JS)
# ---------------------------------------------------------------------------

def _read_obsidian_template_configs(vault_root: Path) -> tuple[list[tuple[str, str]], list[str]]:
    """Read core templates.json and Templater data.json safely. Returns ([(folder_rel, source)], warnings)."""
    dirs: list[tuple[str, str]] = []
    warnings: list[str] = []

    core_cfg = vault_root / ".obsidian" / "templates.json"
    if core_cfg.is_file() and is_within_vault(vault_root, core_cfg):
        try:
            data = json.loads(core_cfg.read_text(encoding="utf-8"))
            folder = str(data.get("folder", "")).strip().strip("/")
            if folder:
                dirs.append((folder, "core_templates_config"))
        except (OSError, json.JSONDecodeError) as exc:
            warnings.append(f"Invalid .obsidian/templates.json: {exc}")

    templater_cfg = vault_root / ".obsidian" / "plugins" / "templater-obsidian" / "data.json"
    if templater_cfg.is_file() and is_within_vault(vault_root, templater_cfg):
        try:
            data = json.loads(templater_cfg.read_text(encoding="utf-8"))
            tf = str(data.get("templates_folder", "")).strip().strip("/")
            if tf:
                dirs.append((tf, "templater_config"))
            for ft in data.get("folder_templates") or []:
                if isinstance(ft, dict) and ft.get("template"):
                    dirs.append((str(ft["template"]).strip(), "templater_folder_mapping"))
        except (OSError, json.JSONDecodeError) as exc:
            warnings.append(f"Invalid templater data.json: {exc}")

    return dirs, warnings


def _inspect_template_file(md_file: Path, vault_root: Path, source: str, confidence: str) -> dict[str, Any]:
    text = md_file.read_text(encoding="utf-8", errors="ignore")
    content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    yaml_raw, body_idx = _split_frontmatter(text)
    meta: dict[str, Any] = {}
    if yaml_raw:
        try:
            loaded = yaml.safe_load(yaml_raw)
            if isinstance(loaded, dict):
                meta = loaded
        except yaml.YAMLError:
            pass

    body_info = _extract_body_structure(text, body_idx)
    templater_exprs = TEMPLATER_RE.findall(text)
    core_exprs = CORE_TEMPLATE_RE.findall(text)
    has_dataview = bool(DATAVIEW_FENCE_RE.search(text) or DATAVIEW_INLINE_RE.search(text))
    unsupported_dynamic = [e[:60] for e in templater_exprs]

    note_types = []
    if meta.get("note_type"):
        note_types.append(str(meta["note_type"]).strip())
    if meta.get("type"):
        note_types.append(str(meta["type"]).strip())

    return {
        "path": md_file.relative_to(vault_root).as_posix(),
        "title": _as_str_or_none(meta.get("title")) or md_file.stem,
        "candidate_note_types": list(dict.fromkeys(note_types)),
        "discovery_source": source,
        "confidence": confidence,
        "frontmatter_keys": sorted(str(k) for k in meta.keys()),
        "headings": body_info["headings"],
        "content_hash": content_hash,
        "dynamic_syntax": {
            "core_placeholders": sorted(set(core_exprs)),
            "unsupported_templater": unsupported_dynamic,
            "has_dataview": has_dataview,
        },
    }


def discover_templates(vault_root: Path, all_md: list[Path]) -> tuple[list[dict[str, Any]], list[str]]:
    """Discover candidate templates from Obsidian configs, template folders, and metadata."""
    cfg_entries, warnings = _read_obsidian_template_configs(vault_root)
    candidates: dict[str, dict[str, Any]] = {}

    for entry_rel, source in cfg_entries:
        target = vault_root / entry_rel
        if not is_within_vault(vault_root, target):
            warnings.append(f"Ignored template config path outside vault: {entry_rel}")
            continue
        if target.is_file() and target.suffix.lower() == ".md":
            rel = target.relative_to(vault_root).as_posix()
            candidates[rel] = _inspect_template_file(target, vault_root, source, "high")
        elif target.is_dir():
            for p in sorted(target.rglob("*.md")):
                if is_within_vault(vault_root, p):
                    rel = p.relative_to(vault_root).as_posix()
                    candidates[rel] = _inspect_template_file(p, vault_root, source, "high")

    for md_file in all_md:
        rel = md_file.relative_to(vault_root).as_posix()
        if rel in candidates:
            continue
        parts_lower = [pt.lower() for pt in md_file.relative_to(vault_root).parts[:-1]]
        rel_dir = "/".join(parts_lower)
        if any(td in rel_dir for td in COMMON_TEMPLATE_DIRS):
            candidates[rel] = _inspect_template_file(md_file, vault_root, "common_folder", "medium")
            continue

        text = md_file.read_text(encoding="utf-8", errors="ignore")
        yaml_raw, _ = _split_frontmatter(text)
        if yaml_raw:
            try:
                loaded = yaml.safe_load(yaml_raw)
                if isinstance(loaded, dict) and str(loaded.get("note_type", loaded.get("type", ""))).lower() == "template":
                    candidates[rel] = _inspect_template_file(md_file, vault_root, "metadata_heuristic", "medium")
                    continue
            except yaml.YAMLError:
                pass
        if "template" in md_file.stem.lower():
            candidates[rel] = _inspect_template_file(md_file, vault_root, "filename_heuristic", "low")

    return sorted(candidates.values(), key=lambda t: ({"high": 0, "medium": 1, "low": 2}[t["confidence"]], t["path"])), warnings


# ---------------------------------------------------------------------------
# Caching & Full Index Builder
# ---------------------------------------------------------------------------

def _default_cache_path(vault_root: Path, cache_dir: Path | None) -> Path:
    base = cache_dir or (Path.home() / ".cache" / "scriptorium")
    digest = hashlib.sha256(str(vault_root).encode("utf-8")).hexdigest()[:16]
    return base / f"vault_index_{digest}.json"


def _config_fingerprint(vault_root: Path) -> str:
    h = hashlib.sha256()
    for rel in (".obsidian/templates.json", ".obsidian/plugins/templater-obsidian/data.json"):
        p = vault_root / rel
        if p.is_file() and is_within_vault(vault_root, p):
            st = p.stat()
            h.update(f"{rel}:{st.st_mtime_ns}:{st.st_size}".encode("utf-8"))
    return h.hexdigest()[:16]


def build_or_load_index(
    vault_path: Path,
    *,
    use_cache: bool = True,
    cache_dir: Path | None = None,
) -> dict[str, Any]:
    vault_root = resolve_vault_root(vault_path)
    md_files, walk_warnings = _iter_vault_markdown(vault_root)
    cfg_fp = _config_fingerprint(vault_root)

    cache_file = _default_cache_path(vault_root, cache_dir)
    cached_notes: dict[str, dict[str, Any]] = {}
    cached_templates: list[dict[str, Any]] | None = None
    cache_cfg_match = False

    if use_cache and cache_file.is_file():
        try:
            c_data = json.loads(cache_file.read_text(encoding="utf-8"))
            if c_data.get("index_version") == INDEX_VERSION and c_data.get("vault_root") == str(vault_root):
                cached_notes = c_data.get("notes_by_file") or {}
                if c_data.get("config_fingerprint") == cfg_fp:
                    cached_templates = c_data.get("templates")
                    cache_cfg_match = True
        except (OSError, json.JSONDecodeError):
            pass

    notes_by_file: dict[str, dict[str, Any]] = {}
    warnings: list[str] = list(walk_warnings)
    all_reused = True
    completeness = "complete"

    for md_file in md_files:
        rel = md_file.relative_to(vault_root).as_posix()
        try:
            st = md_file.stat()
        except OSError as exc:
            warnings.append(f"Unreadable stat '{rel}': {exc}")
            completeness = "partial"
            continue

        prev = cached_notes.get(rel)
        if prev and prev.get("mtime_ns") == st.st_mtime_ns and prev.get("size") == st.st_size:
            notes_by_file[rel] = prev
            continue

        all_reused = False
        try:
            text = md_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            warnings.append(f"Unreadable file '{rel}': {exc}")
            completeness = "partial"
            continue

        yaml_raw, body_idx = _split_frontmatter(text)
        meta: dict[str, Any] = {}
        if yaml_raw is not None:
            try:
                loaded = yaml.safe_load(yaml_raw)
                if isinstance(loaded, dict):
                    meta = loaded
                elif loaded is not None:
                    warnings.append(f"Non-mapping YAML frontmatter in '{rel}'")
            except yaml.YAMLError as exc:
                warnings.append(f"Malformed YAML frontmatter in '{rel}': {exc}")

        body_info = _extract_body_structure(text, body_idx)
        yaml_tags = _extract_yaml_tags(meta)
        all_tags_occ = yaml_tags + body_info["inline_tags"]

        notes_by_file[rel] = {
            "mtime_ns": st.st_mtime_ns,
            "size": st.st_size,
            "file": rel,
            "id": _as_str_or_none(meta.get("id")),
            "title": _as_str_or_none(meta.get("title")),
            "aliases": _as_str_list(meta.get("aliases")),
            "base_domain": _as_str_or_none(meta.get("base_domain")),
            "master_topic": _as_str_or_none(meta.get("master_topic")),
            "topic": _as_str_or_none(meta.get("topic")),
            "note_type": _as_str_or_none(meta.get("note_type")),
            "depends_on": _as_str_list(meta.get("depends_on")),
            "next_topic": _as_str_or_none(meta.get("next_topic")),
            "status": _as_str_or_none(meta.get("status")),
            "review_log": _as_str_list(meta.get("review_log")),
            "headings": body_info["headings"],
            "yaml_tags": yaml_tags,
            "inline_tags": body_info["inline_tags"],
            "tags_unique": list(dict.fromkeys(all_tags_occ)),
            "links": body_info["links"],
            "block_ids": body_info["block_ids"],
        }

    # Detect deletions/moves
    if set(cached_notes.keys()) != set(notes_by_file.keys()):
        all_reused = False

    if cache_cfg_match and all_reused and cached_templates is not None:
        templates = cached_templates
        cache_hit = True
    else:
        templates, tpl_warnings = discover_templates(vault_root, md_files)
        warnings.extend(tpl_warnings)
        cache_hit = False

    # Build Tag Registry across all indexed notes
    tag_stats: dict[str, dict[str, Any]] = {}
    for rel, nrec in notes_by_file.items():
        # Count occurrences per tag in this note
        occ_counts: dict[str, int] = {}
        for t in nrec["yaml_tags"] + nrec["inline_tags"]:
            occ_counts[t] = occ_counts.get(t, 0) + 1
        for t, cnt in occ_counts.items():
            entry = tag_stats.setdefault(
                t,
                {
                    "tag": t,
                    "norm_key": _normalize_tag_key(t),
                    "note_count": 0,
                    "occurrence_count": 0,
                    "parent_hierarchy": t.rsplit("/", 1)[0] if "/" in t else None,
                    "observed": True,
                    "representative_notes": [],
                    "naming_style": _tag_style(t),
                },
            )
            entry["note_count"] += 1
            entry["occurrence_count"] += cnt
            if len(entry["representative_notes"]) < 3:
                entry["representative_notes"].append(rel)

    # Detect candidate tag collisions
    by_norm: dict[str, list[str]] = {}
    for t, info in tag_stats.items():
        by_norm.setdefault(info["norm_key"], []).append(t)
    tag_collisions = [
        {"norm_key": nk, "variants": sorted(vars_list)}
        for nk, vars_list in sorted(by_norm.items())
        if len(vars_list) > 1
    ]

    if use_cache and not cache_hit:
        try:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(
                json.dumps(
                    {
                        "index_version": INDEX_VERSION,
                        "vault_root": str(vault_root),
                        "config_fingerprint": cfg_fp,
                        "notes_by_file": notes_by_file,
                        "templates": templates,
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
        except OSError as exc:
            warnings.append(f"Cache write skipped: {exc}")

    return {
        "index_version": INDEX_VERSION,
        "completeness": completeness,
        "cache_hit": cache_hit,
        "vault_root": str(vault_root),
        "notes": [notes_by_file[k] for k in sorted(notes_by_file.keys(), key=str.lower)],
        "templates": templates,
        "tag_registry": [tag_stats[k] for k in sorted(tag_stats.keys(), key=str.lower)],
        "tag_collisions": tag_collisions,
        "warnings": warnings,
    }


def _filter_notes_by_topic(notes: list[dict[str, Any]], topic_filter: str | None) -> list[dict[str, Any]]:
    if not topic_filter:
        return notes
    norm_filter = re.sub(r"\s+", " ", topic_filter.strip().lower())
    slug_filter = re.sub(r"[^a-z0-9]+", "-", norm_filter).strip("-")
    matched_notes: list[dict[str, Any]] = []
    for rec in notes:
        candidates = [
            rec.get("topic"),
            rec.get("master_topic"),
            rec.get("title"),
            rec.get("id"),
            *(rec.get("aliases") or []),
        ]
        top_folder = Path(rec["file"]).parts[0].lower() if len(Path(rec["file"]).parts) > 1 else ""
        if any(
            c is not None
            and (
                str(c).lower() == norm_filter
                or re.sub(r"[^a-z0-9]+", "-", str(c).lower()).strip("-") == slug_filter
            )
            for c in candidates
        ) or (slug_filter and top_folder == slug_filter):
            matched_notes.append(rec)
    return matched_notes


def _legacy_record(rec: dict[str, Any]) -> dict[str, Any]:
    return {
        "file": rec["file"],
        "id": rec["id"],
        "title": rec["title"],
        "aliases": rec["aliases"],
        "topic": rec["topic"],
        "master_topic": rec["master_topic"],
        "note_type": rec["note_type"],
        "depends_on": rec["depends_on"],
        "next_topic": rec["next_topic"],
        "status": rec["status"],
        "review_log": rec["review_log"],
        "headings": rec["headings"],
    }


def _placement_evidence(notes: list[dict[str, Any]], topic_filter: str | None) -> dict[str, Any]:
    matched = _filter_notes_by_topic(notes, topic_filter)
    folder_counts: dict[str, int] = {}
    numbered_prefixes: list[str] = []
    for rec in matched:
        parent = Path(rec["file"]).parent.as_posix()
        folder_counts[parent] = folder_counts.get(parent, 0) + 1
        m_num = re.match(r"^(\d{1,3})[-_.]", Path(rec["file"]).stem)
        if m_num:
            numbered_prefixes.append(m_num.group(1))

    if folder_counts:
        ranked = sorted(folder_counts.items(), key=lambda x: (-x[1], x[0]))
        status = "existing_destination" if len(ranked) == 1 else "ambiguous_existing_destinations"
        candidates = [{"folder": f, "note_count": c} for f, c in ranked]
    else:
        slug = re.sub(r"[^a-z0-9]+", "-", (topic_filter or "topic").strip().lower()).strip("-")
        status = "proposed_new_folder"
        candidates = [{"folder": slug, "note_count": 0}]

    return {
        "status": status,
        "candidates": candidates,
        "existing_numbering": sorted(numbered_prefixes),
    }


def index_vault(vault_path: Path, topic_filter: str | None = None, *, use_cache: bool = True) -> list[dict[str, Any]]:
    """Legacy API returning compact note metadata records."""
    full = build_or_load_index(vault_path, use_cache=use_cache)
    filtered = _filter_notes_by_topic(full["notes"], topic_filter)
    return [_legacy_record(r) for r in filtered]


def format_compact_json(records: list[dict[str, Any]]) -> str:
    if not records:
        return "[]"
    lines = [json.dumps(rec, ensure_ascii=False, separators=(",", ": ")) for rec in records]
    return "[\n" + ",\n".join(lines) + "\n]"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Content-aware & vault-aware Obsidian metadata indexer.")
    parser.add_argument("vault_path", help="Path to the Obsidian vault root directory.")
    parser.add_argument("--topic", default=None, help="Case-insensitive topic filter.")
    parser.add_argument("--discover", action="store_true", help="Output compact topic-scoped discovery bundle.")
    parser.add_argument("--full-registry", action="store_true", help="Output full tag and template registries.")
    parser.add_argument("--no-cache", action="store_true", help="Bypass local index cache.")
    args = parser.parse_args(argv)

    try:
        vault_root = resolve_vault_root(args.vault_path)
    except (ValueError, FileNotFoundError, NotADirectoryError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    full = build_or_load_index(vault_root, use_cache=not args.no_cache)
    for w in full["warnings"]:
        print(f"WARNING: {w}", file=sys.stderr)

    if args.full_registry:
        print(
            json.dumps(
                {
                    "index_version": full["index_version"],
                    "completeness": full["completeness"],
                    "cache_hit": full["cache_hit"],
                    "templates": full["templates"],
                    "tag_registry": full["tag_registry"],
                    "tag_collisions": full["tag_collisions"],
                    "warnings": full["warnings"],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    if args.discover:
        relevant = _filter_notes_by_topic(full["notes"], args.topic)
        relevant_tags = sorted({t for r in relevant for t in r["tags_unique"]})
        tag_cands = [t for t in full["tag_registry"] if t["tag"] in relevant_tags] if relevant_tags else full["tag_registry"][:25]
        print(
            json.dumps(
                {
                    "index_version": full["index_version"],
                    "completeness": full["completeness"],
                    "cache_hit": full["cache_hit"],
                    "templates": full["templates"],
                    "relevant_notes": [_legacy_record(r) for r in relevant],
                    "placement_conventions": _placement_evidence(full["notes"], args.topic),
                    "tag_candidates": tag_cands,
                    "tag_collisions": full["tag_collisions"],
                    "warnings": full["warnings"],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    records = [_legacy_record(r) for r in _filter_notes_by_topic(full["notes"], args.topic)]
    print(format_compact_json(records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
