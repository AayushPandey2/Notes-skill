#!/usr/bin/env python3
"""Lightweight, read-only Obsidian vault metadata indexer for Scriptorium.

Extracts compact YAML metadata and level-2 (##) headings from Markdown notes
without emitting full note bodies into the LLM context.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

import yaml


def _split_frontmatter(text: str) -> tuple[str | None, int]:
    """Return raw YAML frontmatter text (if present) and 1-based body start index."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 0
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "\n".join(lines[1:idx]), idx + 1
    return None, 0


def _extract_h2_headings(text: str, start_line_idx: int) -> list[str]:
    """Extract level-2 (##) Markdown headings outside fenced code blocks."""
    headings: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    for raw_line in text.splitlines()[start_line_idx:]:
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
        m_h2 = re.match(r"^##\s+(.+?)\s*$", raw_line)
        if m_h2:
            headings.append(m_h2.group(1).strip())
    return headings


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
        return [str(val).strip()] if isinstance(val, str) and val.strip() else []
    return [str(x).strip() for x in val if x is not None and str(x).strip()]


def _iter_markdown_files(vault_root: Path) -> list[Path]:
    """Walk vault_root without following directory symlinks; exclude scratchpad/ and hidden dirs."""
    md_files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(vault_root, followlinks=False):
        dirnames[:] = sorted(
            d for d in dirnames if not d.startswith(".") and d.lower() != "scratchpad"
        )
        for fname in sorted(filenames):
            if fname.lower().endswith(".md"):
                full = Path(dirpath) / fname
                if not full.is_symlink():
                    md_files.append(full)
    return sorted(md_files, key=lambda p: p.relative_to(vault_root).as_posix().lower())


def index_vault(vault_path: Path, topic_filter: str | None = None) -> list[dict[str, Any]]:
    """Return compact metadata records for all matching Markdown notes in vault_path."""
    vault_root = vault_path.resolve()
    records: list[dict[str, Any]] = []
    norm_filter = re.sub(r"\s+", " ", topic_filter.strip().lower()) if topic_filter else None
    slug_filter = re.sub(r"[^a-z0-9]+", "-", norm_filter).strip("-") if norm_filter else None

    for md_file in _iter_markdown_files(vault_root):
        rel_path = md_file.relative_to(vault_root).as_posix()
        try:
            text = md_file.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"WARNING: Skipping unreadable file '{rel_path}': {exc}", file=sys.stderr)
            continue

        yaml_raw, body_idx = _split_frontmatter(text)
        meta: dict[str, Any] = {}
        if yaml_raw is not None:
            try:
                loaded = yaml.safe_load(yaml_raw)
                if isinstance(loaded, dict):
                    meta = loaded
                elif loaded is not None:
                    print(f"WARNING: Non-mapping YAML frontmatter in '{rel_path}'", file=sys.stderr)
            except yaml.YAMLError as exc:
                print(f"WARNING: Malformed YAML frontmatter in '{rel_path}': {exc}", file=sys.stderr)

        record: dict[str, Any] = {
            "file": rel_path,
            "id": _as_str_or_none(meta.get("id")),
            "title": _as_str_or_none(meta.get("title")),
            "aliases": _as_str_list(meta.get("aliases")),
            "topic": _as_str_or_none(meta.get("topic")),
            "master_topic": _as_str_or_none(meta.get("master_topic")),
            "depends_on": _as_str_list(meta.get("depends_on")),
            "next_topic": _as_str_or_none(meta.get("next_topic")),
            "status": _as_str_or_none(meta.get("status")),
            "headings": _extract_h2_headings(text, body_idx),
        }

        if norm_filter is not None:
            candidates = [
                record["topic"],
                record["master_topic"],
                record["title"],
                record["id"],
                *record["aliases"],
            ]
            # Also allow matching the top-level topic folder slug deterministically
            top_folder = Path(rel_path).parts[0].lower() if len(Path(rel_path).parts) > 1 else ""
            matched = any(
                c is not None
                and (
                    c.lower() == norm_filter
                    or re.sub(r"[^a-z0-9]+", "-", c.lower()).strip("-") == slug_filter
                )
                for c in candidates
            ) or (slug_filter is not None and top_folder == slug_filter)
            if not matched:
                continue

        records.append(record)

    return records


def format_compact_json(records: list[dict[str, Any]]) -> str:
    """Format JSON array with one compact object per physical line."""
    if not records:
        return "[]"
    lines = [json.dumps(rec, ensure_ascii=False, separators=(",", ": ")) for rec in records]
    return "[\n" + ",\n".join(lines) + "\n]"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build a compact, read-only metadata index of an Obsidian vault."
    )
    parser.add_argument("vault_path", help="Path to the Obsidian vault root directory.")
    parser.add_argument(
        "--topic",
        default=None,
        help="Optional case-insensitive filter matching topic, master_topic, title, aliases, id, or topic folder.",
    )
    args = parser.parse_args(argv)

    vault_path = Path(args.vault_path)
    if not vault_path.is_dir():
        print(f"ERROR: Vault path is not an existing directory: {vault_path}", file=sys.stderr)
        return 2

    records = index_vault(vault_path, topic_filter=args.topic)
    print(format_compact_json(records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
