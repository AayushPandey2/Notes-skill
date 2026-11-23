#!/usr/bin/env python3
r"""Template-aware, scoped, read-by-default Obsidian vault validator with safe --fix.

Supports:
  - Legacy vault/folder scan:
      python3 scripts/verify_vault_notes.py "<vault_path>" [target_folder] [--fix]
  - Scoped file validation & repair (leaves unrelated notes untouched):
      python3 scripts/verify_vault_notes.py "<vault_path>" --files note1.md note2.md [--fix]
  - Manifest-backed schema & pre-generation tag snapshot validation:
      python3 scripts/verify_vault_notes.py "<vault_path>" --manifest manifest.json [--fix]
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

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
for _p in (str(REPO_ROOT), str(SCRIPT_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from scriptorium.layout import ROUTES
from scriptorium.models import (
    STRICT_KEYS as MANDATORY_TOPIC_KEYS,
    heading_slug as _heading_slug,
    is_within_vault as _is_within_vault,
    split_frontmatter_lines as _split_frontmatter_lines,
)

RAW_LATEX_IN_YAML_RE = re.compile(
    r"\\(?:mathbb|mathbf|mathcal|mathrm|text|operatorname|sum|prod|int|frac|dfrac|"
    r"hat|widehat|bar|tilde|vec|left|right|ge|le|geq|leq|neq|approx|equiv|to|"
    r"implies|iff|land|lor|forall|exists|in|notin|theta|alpha|beta|gamma|delta|"
    r"lambda|sigma|omega|eta|rho|lVert|rVert|lvert|rvert|mid|sqrt|cdot|times)\b"
)

PLACEHOLDER_RE = re.compile(r"(?:<exact-url>|<source-anchor>|PLACEHOLDER_URL|\[\[none\]\])")
UNRESOLVED_TPL_RE = re.compile(r"(?:<%[\s\S]*?%>|\{\{(?:date|time|title|folder|author)(?::[^}]*)?\}\})", flags=re.IGNORECASE)
BANNED_S6_LABELS_RE = re.compile(
    r"\b(?:I\s+Do|We\s+Do|You\s+Do|Worked\s+Trace|Faded\s+Variation|Drill\s+[AB])\b",
    flags=re.IGNORECASE,
)

EXCLUDED_DIRS = {".git", ".trash", ".obsidian", "scratchpad", "node_modules", "__pycache__"}


def _clean_title_for_alias(title: str) -> str:
    cleaned = title.strip()
    cleaned = re.sub(r"^\d{1,3}\s*(?:[-–—.]\s*|\s+-\s+)", "", cleaned).strip()
    return cleaned


def _normalize_tag_key(tag: str) -> str:
    k = tag.strip().lower().replace("_", "-")
    if len(k) > 3 and k.endswith("s") and not k.endswith("ss"):
        k = k[:-1]
    return k


def _extract_anchors_and_blocks(text: str) -> tuple[set[str], set[str]]:
    anchors: set[str] = set()
    blocks: set[str] = set()
    lines = text.splitlines()
    _, body_idx = _split_frontmatter_lines(lines)
    in_fence = False
    for line in lines[body_idx:]:
        if re.match(r"^\s*(`{3,}|~{3,})", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m_h = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if m_h:
            raw = m_h.group(1).strip()
            anchors.add(raw.lower())
            slug = _heading_slug(raw)
            anchors.add(slug)
            anchors.add(re.sub(r"-{2,}", "-", slug))
        m_blk = re.search(r"(?:^|\s)\^([A-Za-z0-9-]+)\s*$", line)
        if m_blk:
            blocks.add(m_blk.group(1).lower())
    return anchors, blocks


def _iter_markdown_files(vault_root: Path, scan_root: Path) -> list[Path]:
    md_files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(scan_root, followlinks=False):
        dirnames[:] = sorted(
            d
            for d in dirnames
            if d.lower() not in EXCLUDED_DIRS
            and not d.startswith(".")
            and _is_within_vault(vault_root, Path(dirpath) / d)
        )
        for fname in sorted(filenames):
            if fname.lower().endswith(".md"):
                full = Path(dirpath) / fname
                if _is_within_vault(vault_root, full):
                    md_files.append(full)
    return sorted(md_files, key=lambda p: p.relative_to(vault_root).as_posix().lower())


def build_vault_index(vault_root: Path) -> dict[str, Any]:
    """Index stems, titles, aliases, IDs, headings, block IDs, and tags across the vault."""
    stems: dict[str, Path] = {}
    titles: dict[str, Path] = {}
    aliases: dict[str, Path] = {}
    ids_map: dict[str, Path] = {}
    ids_to_files: dict[str, list[Path]] = {}
    anchors_by_file: dict[Path, set[str]] = {}
    blocks_by_file: dict[Path, set[str]] = {}
    existing_tags: dict[str, str] = {}  # norm_key -> representative exact tag
    syllabi: dict[str, dict[str, Any]] = {}  # topic_dir_rel -> {moc_rel, allowed}

    for md_file in _iter_markdown_files(vault_root, vault_root):
        stems[md_file.stem.lower()] = md_file
        rel_no_ext = md_file.relative_to(vault_root).with_suffix("").as_posix().lower()
        stems[rel_no_ext] = md_file

        try:
            text = md_file.read_text(encoding="utf-8")
        except OSError:
            continue

        anchors, blocks = _extract_anchors_and_blocks(text)
        anchors_by_file[md_file] = anchors
        blocks_by_file[md_file] = blocks

        lines = text.splitlines()
        yaml_lines, _ = _split_frontmatter_lines(lines)
        if yaml_lines is not None:
            try:
                y_obj = yaml.safe_load("\n".join(yaml_lines))
                if isinstance(y_obj, dict):
                    fid = y_obj.get("id")
                    if isinstance(fid, str) and fid.strip():
                        ids_map[fid.strip().lower()] = md_file
                        ids_to_files.setdefault(fid.strip(), []).append(md_file)
                    ftitle = y_obj.get("title")
                    if isinstance(ftitle, str) and ftitle.strip():
                        titles[ftitle.strip().lower()] = md_file
                    for a in y_obj.get("aliases") or []:
                        if isinstance(a, str) and a.strip():
                            aliases[a.strip().lower()] = md_file
                    raw_tags = y_obj.get("tags") or y_obj.get("tag") or []
                    if isinstance(raw_tags, str):
                        raw_tags = [x.strip() for x in re.split(r"[,\s]+", raw_tags) if x.strip()]
                    if isinstance(raw_tags, list):
                        for t in raw_tags:
                            ts = str(t).strip().lstrip("#")
                            if ts:
                                existing_tags.setdefault(_normalize_tag_key(ts), ts)
                    if md_file.name.upper().startswith("00-MOC-") or (
                        str(y_obj.get("note_type", "")).strip().lower() == "syllabus" and y_obj.get("scope_locked")
                    ):
                        raw_allowed = y_obj.get("allowed_subtopics") or re.findall(
                            r"^\s*\d+\.\s+`([^`]+\.md)`", text, flags=re.MULTILINE
                        )
                        if isinstance(raw_allowed, list) and raw_allowed:
                            dir_rel = md_file.parent.relative_to(vault_root).as_posix()
                            syllabi[dir_rel] = {
                                "moc_rel": md_file.relative_to(vault_root).as_posix(),
                                "allowed": {str(x).strip().lower() for x in raw_allowed if str(x).strip()},
                            }
            except yaml.YAMLError:
                pass

    return {
        "stems": stems,
        "titles": titles,
        "aliases": aliases,
        "ids_map": ids_map,
        "ids_to_files": ids_to_files,
        "anchors_by_file": anchors_by_file,
        "blocks_by_file": blocks_by_file,
        "existing_tags": existing_tags,
        "syllabi": syllabi,
    }


# ---------------------------------------------------------------------------
# Mechanical Auto-Repairs (--fix only)
# ---------------------------------------------------------------------------

def _repair_inline_math_whitespace_in_line(line: str) -> tuple[str, bool]:
    out: list[str] = []
    i = 0
    n = len(line)
    changed = False
    while i < n:
        ch = line[i]
        if ch == "\\" and i + 1 < n:
            out.append(line[i : i + 2])
            i += 2
            continue
        if ch == "`":
            run = 1
            while i + run < n and line[i + run] == "`":
                run += 1
            close = line.find("`" * run, i + run)
            if close != -1:
                out.append(line[i : close + run])
                i = close + run
                continue
            out.append(line[i : i + run])
            i += run
            continue
        if ch == "$" and i + 1 < n and line[i + 1] == "$":
            close = line.find("$$", i + 2)
            if close != -1:
                out.append(line[i : close + 2])
                i = close + 2
                continue
            out.append("$$")
            i += 2
            continue
        if ch == "$":
            j = i + 1
            close = -1
            while j < n:
                if line[j] == "\\" and j + 1 < n:
                    j += 2
                    continue
                if line[j] == "$":
                    close = j
                    break
                j += 1
            if close != -1:
                inner = line[i + 1 : close]
                trimmed = inner.strip()
                if trimmed and inner != trimmed:
                    changed = True
                    out.append(f"${trimmed}$")
                else:
                    out.append(line[i : close + 1])
                i = close + 1
                continue
        out.append(ch)
        i += 1
    return "".join(out), changed


def _ensure_title_alias_in_yaml_lines(yaml_lines: list[str]) -> tuple[list[str], bool]:
    try:
        y_obj = yaml.safe_load("\n".join(yaml_lines))
    except yaml.YAMLError:
        return yaml_lines, False
    if not isinstance(y_obj, dict):
        return yaml_lines, False

    raw_title = y_obj.get("title")
    if not isinstance(raw_title, str) or not raw_title.strip():
        return yaml_lines, False
    clean_alias = _clean_title_for_alias(raw_title)
    if not clean_alias:
        return yaml_lines, False

    existing_aliases = y_obj.get("aliases")
    if isinstance(existing_aliases, list):
        if any(isinstance(a, str) and a.strip().lower() == clean_alias.lower() for a in existing_aliases):
            return yaml_lines, False

    new_lines = list(yaml_lines)
    quoted_alias = f'"{clean_alias.replace(chr(34), chr(92) + chr(34))}"'

    for idx, yl in enumerate(new_lines):
        m_flow = re.match(r"^aliases\s*:\s*\[(.*)\]\s*$", yl.strip())
        if m_flow:
            inner = m_flow.group(1).strip()
            new_lines[idx] = f"aliases: [{quoted_alias}]" if not inner else f"aliases: [{inner}, {quoted_alias}]"
            return new_lines, True

    for idx, yl in enumerate(new_lines):
        if re.match(r"^aliases\s*:\s*$", yl.strip()):
            insert_at = idx + 1
            while insert_at < len(new_lines) and re.match(r"^\s+-\s+", new_lines[insert_at]):
                insert_at += 1
            new_lines.insert(insert_at, f"  - {quoted_alias}")
            return new_lines, True

    insert_at = len(new_lines)
    for idx, yl in enumerate(new_lines):
        if re.match(r"^title\s*:", yl):
            insert_at = idx + 1
            break
    new_lines.insert(insert_at, f"  - {quoted_alias}")
    new_lines.insert(insert_at, "aliases:")
    return new_lines, True


def apply_mechanical_fixes(
    md_file: Path,
    vault_root: Path,
    *,
    enforce_builtin_style: bool = True,
) -> list[tuple[str, int, str]]:
    """Apply safe mechanical repairs in-place; return [(rel_file, line, code)]."""
    raw_bytes = md_file.read_bytes()
    newline = "\r\n" if b"\r\n" in raw_bytes else "\n"
    text = raw_bytes.decode("utf-8")
    had_trailing_nl = text.endswith("\n")
    lines = text.splitlines()
    rel_file = md_file.relative_to(vault_root).as_posix()
    repairs: list[tuple[str, int, str]] = []

    yaml_lines, body_idx = _split_frontmatter_lines(lines)
    if yaml_lines is not None and enforce_builtin_style:
        new_yaml, alias_added = _ensure_title_alias_in_yaml_lines(yaml_lines)
        if alias_added:
            alias_line_no = 2
            for k, yl in enumerate(new_yaml, start=2):
                if yl.strip().startswith("aliases:"):
                    alias_line_no = k
                    break
            lines = [lines[0], *new_yaml, "---", *lines[body_idx:]]
            body_idx = len(new_yaml) + 2
            repairs.append((rel_file, alias_line_no, "TITLE_ALIAS_ADDED"))

    in_fence = False
    fence_char = ""
    fence_len = 0
    in_display = False

    for idx in range(body_idx, len(lines)):
        raw_line = lines[idx]
        line_no = idx + 1
        stripped = raw_line.strip()

        m_fence = re.match(r"^\s*(`{3,}|~{3,})", raw_line)
        if m_fence and not in_display:
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

        body_check = re.sub(r"^\s*>\s?", "", raw_line).strip()
        if body_check == "$$":
            in_display = not in_display
            continue
        if in_display:
            continue

        m_qh = re.match(r"^(\s*)[\"'`]+(#{1,6})[\"'`]+(\s+.*)$", raw_line)
        if m_qh:
            lines[idx] = f"{m_qh.group(1)}{m_qh.group(2)}{m_qh.group(3)}"
            repairs.append((rel_file, line_no, "QUOTED_HEADING_FIXED"))

        fixed_line, math_changed = _repair_inline_math_whitespace_in_line(lines[idx])
        if math_changed:
            lines[idx] = fixed_line
            repairs.append((rel_file, line_no, "INLINE_MATH_NORMALIZED"))

        if lines[idx].lstrip().startswith("|") and "[[" in lines[idx]:
            new_table_line = re.sub(
                r"\[\[([^\]\r\n\\|]+)\|([^\]\r\n]+)\]\]",
                r"[[\1\\|\2]]",
                lines[idx],
            )
            if new_table_line != lines[idx]:
                lines[idx] = new_table_line
                repairs.append((rel_file, line_no, "TABLE_WIKILINK_PIPE_ESCAPED"))

    if enforce_builtin_style:
        i = body_idx
        in_fence = False
        while i < len(lines):
            if re.match(r"^\s*(`{3,}|~{3,})", lines[i]):
                in_fence = not in_fence
                i += 1
                continue
            if in_fence:
                i += 1
                continue
            if lines[i].lstrip().startswith("> [!example]-"):
                j = i + 1
                while j < len(lines):
                    if lines[j].lstrip().startswith(">"):
                        j += 1
                        continue
                    if lines[j].strip() == "":
                        k = j + 1
                        while k < len(lines) and lines[k].strip() == "":
                            k += 1
                        if k < len(lines) and lines[k].lstrip().startswith(">") and not re.match(r"^\s*>\s*\[!", lines[k]):
                            lines[j] = ">"
                            repairs.append((rel_file, j + 1, "CALLOUT_LINES_NORMALIZED"))
                            j += 1
                            continue
                    break
                i = j
                continue
            i += 1

    if repairs:
        out_text = newline.join(lines) + (newline if had_trailing_nl else "")
        md_file.write_bytes(out_text.encode("utf-8"))
    return repairs


# ---------------------------------------------------------------------------
# Schema-Aware & Scoped Validation
# ---------------------------------------------------------------------------

def _scan_yaml_for_latex(obj: Any, yaml_lines: list[str]) -> list[tuple[int, str, str]]:
    hits: list[tuple[int, str, str]] = []

    def _find_line(val_snippet: str, key_hint: str) -> int:
        top_key = key_hint.split(".")[0].split("[")[0]
        for off, yl in enumerate(yaml_lines, start=2):
            if val_snippet and val_snippet[:18] in yl:
                return off
        for off, yl in enumerate(yaml_lines, start=2):
            if re.match(rf"^{re.escape(top_key)}\s*:", yl.strip()):
                return off
        return 2

    def _walk(node: Any, prefix: str) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                _walk(v, f"{prefix}.{k}" if prefix else str(k))
        elif isinstance(node, list):
            for idx, item in enumerate(node):
                _walk(item, f"{prefix}[{idx}]")
        elif isinstance(node, str):
            if RAW_LATEX_IN_YAML_RE.search(node) or "$" in node or any(ord(c) < 32 for c in node):
                hits.append((_find_line(node, prefix), prefix, node))

    _walk(obj, "")
    return hits


def _resolve_note_schema(
    rel_file: str,
    y_obj: dict[str, Any] | None,
    manifest: dict[str, Any] | None,
) -> str:
    """Resolve schema: 'custom' | 'builtin_deep' | 'builtin_cheatsheet' | 'builtin_comparison' | 'generic'."""
    if manifest and rel_file in (manifest.get("outputs") or []):
        ttype = str(manifest.get("template_type", "")).strip().lower()
        if ttype in {"custom", "builtin_deep", "builtin_cheatsheet", "builtin_comparison", "generic"}:
            return ttype

    if Path(rel_file).name.upper().startswith("00-MOC-"):
        return "builtin_syllabus"

    if y_obj:
        if set(y_obj.keys()) == set(MANDATORY_TOPIC_KEYS):
            return "routed"
        if y_obj.get("template") in ROUTES:
            return "routed"
        nt = str(y_obj.get("note_type", "")).strip().lower()
        if nt == "cheatsheet":
            return "builtin_cheatsheet"
        if nt == "comparison":
            return "builtin_comparison"
        if nt == "syllabus":
            return "builtin_syllabus"

    parts = Path(rel_file).parts
    if parts and parts[0].lower() == "comparison":
        return "builtin_comparison"
    if "topics" in parts and manifest is None:
        return "builtin_deep"
    return "generic"


def _check_syllabus_boundary(
    md_file: Path,
    rel_file: str,
    vault_root: Path,
    index: dict[str, Any],
    y_obj: dict[str, Any] | None,
    schema: str,
) -> list[dict[str, Any]]:
    """Enforce locked 00-MOC syllabus allowlists on generated topic folders."""
    syllabi = index.get("syllabi") or {}
    rel_parts = {p.lower() for p in Path(rel_file).parts[:-1]}
    specialized = bool(rel_parts & {"practice sets", "atomic notes", "cheatsheets", "comparison"}) or (
        y_obj and y_obj.get("template") in ("practice", "atomic", "cheat-sheet", "comparison")
    )
    if (
        not syllabi
        or specialized
        or schema in {"builtin_syllabus", "builtin_cheatsheet", "builtin_comparison"}
        or md_file.name.upper().startswith("00-MOC-")
    ):
        return []

    matched_contract = None
    for cand_dir in (md_file.parent, md_file.parent.parent):
        if _is_within_vault(vault_root, cand_dir):
            cand_rel = cand_dir.relative_to(vault_root).as_posix()
            if cand_rel in syllabi:
                matched_contract = syllabi[cand_rel]
                break
    if matched_contract is None:
        return []

    allowed = matched_contract["allowed"]
    fname_low = md_file.name.lower()
    rel_low = rel_file.lower()
    if fname_low in allowed or rel_low in allowed or any(rel_low.endswith("/" + a) for a in allowed):
        return []
    return [
        {
            "file": rel_file,
            "line": 1,
            "level": "ERROR",
            "code": "OUT_OF_SCOPE_NOTE_CREATED",
            "message": (
                f"Note '{md_file.name}' is outside the locked syllabus allowlist "
                f"in '{matched_contract['moc_rel']}'."
            ),
        }
    ]


def _check_frontmatter_rules(
    rel_file: str,
    y_obj: dict[str, Any],
    yaml_lines: list[str] | None,
    ids_to_files: dict[str, list[Path]],
    pre_tags: dict[str, str],
    schema: str,
    is_builtin: bool,
    manifest: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    """Validate YAML metadata keys, LaTeX leakage, tag similarity, and duplicate IDs."""
    findings: list[dict[str, Any]] = []
    if is_builtin:
        for lno, key_path, val in _scan_yaml_for_latex(y_obj, yaml_lines or []):
            findings.append({
                "file": rel_file,
                "line": lno,
                "level": "ERROR",
                "code": "LATEX_IN_FRONTMATTER",
                "message": f"Raw LaTeX or '$' in YAML '{key_path}': {val[:60]!r}",
            })
    if "review_log" in y_obj and not isinstance(y_obj["review_log"], list):
        findings.append({
            "file": rel_file,
            "line": 2,
            "level": "ERROR",
            "code": "INVALID_REVIEW_LOG",
            "message": "Optional 'review_log' YAML property must be a list.",
        })
    fid = y_obj.get("id")
    if isinstance(fid, str) and len(ids_to_files.get(fid.strip(), [])) > 1:
        findings.append({
            "file": rel_file,
            "line": 2,
            "level": "ERROR",
            "code": "DUPLICATE_YAML_ID",
            "message": f"Duplicate YAML id '{fid}' across vault.",
        })

    raw_tags = y_obj.get("tags") or y_obj.get("tag") or []
    if isinstance(raw_tags, str):
        raw_tags = [x.strip() for x in re.split(r"[,\s]+", raw_tags) if x.strip()]
    if isinstance(raw_tags, list):
        for t in raw_tags:
            ts = str(t).strip().lstrip("#")
            if not ts:
                continue
            nk = _normalize_tag_key(ts)
            if nk in pre_tags and pre_tags[nk] != ts:
                findings.append({
                    "file": rel_file,
                    "line": 2,
                    "level": "WARNING",
                    "code": "NEAR_DUPLICATE_TAG",
                    "message": f"Tag '{ts}' closely resembles existing vault tag '{pre_tags[nk]}'.",
                })

    if schema == "builtin_deep":
        for req in MANDATORY_TOPIC_KEYS:
            if req not in y_obj:
                findings.append({
                    "file": rel_file,
                    "line": 2,
                    "level": "ERROR",
                    "code": "MISSING_YAML_KEY",
                    "message": f"Missing mandatory key '{req}' in YAML frontmatter.",
                })
        raw_title = y_obj.get("title")
        if isinstance(raw_title, str) and raw_title.strip():
            clean_alias = _clean_title_for_alias(raw_title)
            existing_a = [str(a).strip().lower() for a in (y_obj.get("aliases") or [])]
            if clean_alias and clean_alias.lower() not in existing_a:
                findings.append({
                    "file": rel_file,
                    "line": 2,
                    "level": "ERROR",
                    "code": "MISSING_TITLE_ALIAS",
                    "message": f"Clean title '{clean_alias}' missing from YAML aliases.",
                })

    if schema == "custom" and manifest and manifest.get("template_frontmatter_keys"):
        for req in manifest["template_frontmatter_keys"]:
            if req not in y_obj:
                findings.append({
                    "file": rel_file,
                    "line": 2,
                    "level": "WARNING",
                    "code": "CUSTOM_TEMPLATE_KEY_MISSING",
                    "message": f"Key '{req}' from selected custom template is absent.",
                })
    return findings


def _check_inline_math_delimiters(
    raw_line: str,
    stripped: str,
    rel_file: str,
    line_no: int,
) -> list[dict[str, Any]]:
    """Audit inline '$' pairing, leading/trailing spaces, and unescaped table pipes."""
    findings: list[dict[str, Any]] = []
    masked = re.sub(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$", " ", raw_line)
    masked = re.sub(r"`[^`]*`", " ", masked)
    is_table = stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 1
    i = 0
    n = len(masked)
    while i < n:
        if masked[i] == "\\" and i + 1 < n:
            i += 2
            continue
        if masked[i] != "$":
            i += 1
            continue
        j = i + 1
        close_pos = -1
        while j < n:
            if masked[j] == "\\" and j + 1 < n:
                j += 2
                continue
            if masked[j] == "$":
                close_pos = j
                break
            j += 1
        if close_pos == -1:
            findings.append({
                "file": rel_file,
                "line": line_no,
                "level": "ERROR",
                "code": "DELIMITER_IMBALANCE",
                "message": f"Unbalanced inline '$' delimiter on line {line_no}.",
            })
            break
        expr = masked[i + 1 : close_pos]
        if expr and (expr[0].isspace() or expr[-1].isspace()):
            findings.append({
                "file": rel_file,
                "line": line_no,
                "level": "ERROR",
                "code": "INLINE_MATH_WHITESPACE",
                "message": f"Whitespace immediately inside inline math delimiters: '${expr}$'.",
            })
        if is_table and re.search(r"(?<!\\)\|", expr):
            findings.append({
                "file": rel_file,
                "line": line_no,
                "level": "ERROR",
                "code": "TABLE_RAW_PIPE_IN_MATH",
                "message": f"Unescaped '|' inside inline math in Markdown table: '${expr}$'.",
            })
        i = close_pos + 1
    return findings


def _check_wikilink_line(
    raw_line: str,
    rel_file: str,
    line_no: int,
    md_file: Path,
    vault_root: Path,
    index: dict[str, Any],
) -> list[dict[str, Any]]:
    """Verify wikilinks, image embeds, heading anchors, and block anchors on one line."""
    findings: list[dict[str, Any]] = []
    stems = index["stems"]
    titles = index["titles"]
    aliases = index["aliases"]
    ids_map = index["ids_map"]
    anchors_by_file = index["anchors_by_file"]
    blocks_by_file = index["blocks_by_file"]

    for m_wl in re.finditer(r"\[\[([^\]]+)\]\]", raw_line):
        inner = m_wl.group(1)
        target_full = re.split(r"\\?\|", inner, maxsplit=1)[0].strip()
        if Path(target_full).suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp", ".pdf"}:
            asset = target_full.lstrip("/")
            if not ((vault_root / asset).is_file() or any(vault_root.rglob(Path(asset).name))):
                findings.append({
                    "file": rel_file,
                    "line": line_no,
                    "level": "ERROR",
                    "code": "UNRESOLVED_IMAGE_EMBED",
                    "message": f"Unresolved image embed '![[{inner}]]'.",
                })
            continue
        if "#" in target_full:
            target_part, anchor_part = (p.strip() for p in target_full.split("#", 1))
        else:
            target_part, anchor_part = target_full, ""

        if not target_part:
            resolved_target = md_file
        else:
            key = target_part.lower()
            key_stem = Path(target_part).stem.lower()
            resolved_target = (
                stems.get(key)
                or stems.get(key_stem)
                or aliases.get(key)
                or titles.get(key)
                or ids_map.get(key)
            )
            if resolved_target is None:
                findings.append({
                    "file": rel_file,
                    "line": line_no,
                    "level": "ERROR",
                    "code": "UNRESOLVED_WIKILINK",
                    "message": f"Unresolved wikilink '[[{inner}]]'.",
                })
                continue

        if anchor_part:
            if anchor_part.startswith("^"):
                blk_id = anchor_part[1:].lower()
                if blk_id not in blocks_by_file.get(resolved_target, set()):
                    findings.append({
                        "file": rel_file,
                        "line": line_no,
                        "level": "ERROR",
                        "code": "UNRESOLVED_BLOCK_ANCHOR",
                        "message": f"Block anchor '#^{anchor_part[1:]}' not found in '{resolved_target.name}'.",
                    })
            else:
                valid_anchors = anchors_by_file.get(resolved_target, set())
                a_norm = anchor_part.lower()
                a_slug = _heading_slug(anchor_part)
                if (
                    a_norm not in valid_anchors
                    and a_slug not in valid_anchors
                    and re.sub(r"-{2,}", "-", a_slug) not in valid_anchors
                ):
                    findings.append({
                        "file": rel_file,
                        "line": line_no,
                        "level": "ERROR",
                        "code": "UNRESOLVED_HEADING_ANCHOR",
                        "message": f"Heading anchor '#{anchor_part}' not found in '{resolved_target.name}'.",
                    })
    return findings


def _check_builtin_schema_rules(
    rel_file: str,
    schema: str,
    body_text: str,
    body_idx: int,
    has_key_equations: bool,
    s5_line: int,
    s5_impl_count: int,
    q_blocks: list[tuple[int, str, bool]],
) -> list[dict[str, Any]]:
    """Apply product-level callout, section, and Q&A checks for built-in schemas."""
    findings: list[dict[str, Any]] = []
    if schema == "builtin_cheatsheet":
        if "> [!abstract] Core Formula Snapshot" not in body_text:
            findings.append({
                "file": rel_file,
                "line": body_idx + 1,
                "level": "ERROR",
                "code": "MISSING_CHEATSHEET_SNAPSHOT",
                "message": "Cheatsheet missing '> [!abstract] Core Formula Snapshot' callout.",
            })
        for sec_h in ("## 1. Definition", "## 2. Theory", "## 3. Formulas", "## 4. Glossary", "## 5. Extra Knowledge"):
            if sec_h not in body_text:
                findings.append({
                    "file": rel_file,
                    "line": body_idx + 1,
                    "level": "ERROR",
                    "code": "MISSING_CHEATSHEET_SECTION",
                    "message": f"Cheatsheet missing required section '{sec_h}'.",
                })
        for sec_h, lo, hi in (("## 1. Definition", 25, 30), ("## 2. Theory", 50, 60)):
            m_sec = re.search(rf"^{re.escape(sec_h)}\s*\n(.*?)(?=\n<!--|\n## |\Z)", body_text, flags=re.MULTILINE | re.DOTALL)
            if m_sec:
                wc = len(re.findall(r"\S+", m_sec.group(1).strip()))
                if not (lo <= wc <= hi):
                    findings.append({
                        "file": rel_file,
                        "line": body_idx + 1,
                        "level": "WARNING",
                        "code": "CHEATSHEET_WORD_BUDGET",
                        "message": f"{sec_h} word count is {wc} (target {lo}-{hi} words).",
                    })

    if schema == "builtin_comparison":
        if "> [!abstract] Core Trade-Off Verdict" not in body_text:
            findings.append({
                "file": rel_file,
                "line": body_idx + 1,
                "level": "ERROR",
                "code": "MISSING_COMPARISON_VERDICT",
                "message": "Comparison note missing '> [!abstract] Core Trade-Off Verdict' callout.",
            })
        for sec_h in (
            "## 1. Conceptual & Mathematical Divergence",
            "## 2. Multi-Dimensional Trade-Off Matrix",
            "## 3. Failure Regimes & Edge-Case Behavior",
            "## 4. Decision Rules & Transfer Scenarios",
        ):
            if sec_h not in body_text:
                findings.append({
                    "file": rel_file,
                    "line": body_idx + 1,
                    "level": "ERROR",
                    "code": "MISSING_COMPARISON_SECTION",
                    "message": f"Comparison note missing required section '{sec_h}'.",
                })

    if schema == "builtin_deep":
        if not has_key_equations:
            findings.append({
                "file": rel_file,
                "line": body_idx + 1,
                "level": "ERROR",
                "code": "MISSING_KEY_EQUATIONS_CALLOUT",
                "message": "Missing required '> [!abstract] Key Equations' callout.",
            })
        if s5_impl_count > 3:
            findings.append({
                "file": rel_file,
                "line": s5_line or body_idx + 1,
                "level": "WARNING",
                "code": "TOO_MANY_SECTION_5_IMPLEMENTATIONS",
                "message": f"Section 5 should include at most 3 distinct implementations; found {s5_impl_count}.",
            })
        if len(q_blocks) < 5:
            findings.append({
                "file": rel_file,
                "line": body_idx + 1,
                "level": "ERROR",
                "code": "INSUFFICIENT_SECTION_6_QA",
                "message": f"Section 6 requires at least 5 #### Question blocks; found {len(q_blocks)}.",
            })
        for q_line, q_title, has_c in q_blocks:
            if not has_c:
                findings.append({
                    "file": rel_file,
                    "line": q_line,
                    "level": "ERROR",
                    "code": "MISSING_ANSWER_CALLOUT",
                    "message": f"Question '{q_title}' missing '> [!example]-' answer callout.",
                })
    return findings


def validate_file(
    md_file: Path,
    vault_root: Path,
    index: dict[str, Any],
    *,
    manifest: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    rel_file = md_file.relative_to(vault_root).as_posix()
    text = md_file.read_text(encoding="utf-8")
    lines = text.splitlines()

    pre_tags: dict[str, str] = dict(index["existing_tags"])
    if manifest and isinstance(manifest.get("pre_generation_tags"), list):
        pre_tags = {_normalize_tag_key(str(t)): str(t) for t in manifest["pre_generation_tags"] if str(t).strip()}

    yaml_lines, body_idx = _split_frontmatter_lines(lines)
    y_obj: dict[str, Any] | None = None
    if yaml_lines is not None:
        try:
            loaded = yaml.safe_load("\n".join(yaml_lines))
            if isinstance(loaded, dict):
                y_obj = loaded
        except yaml.YAMLError as exc:
            findings.append({
                "file": rel_file,
                "line": 2,
                "level": "ERROR",
                "code": "YAML_SYNTAX_ERROR",
                "message": f"Invalid YAML frontmatter: {exc}",
            })

    schema = _resolve_note_schema(rel_file, y_obj, manifest)
    findings.extend(_check_syllabus_boundary(md_file, rel_file, vault_root, index, y_obj, schema))

    if schema == "routed":
        from validate_note import validate_text

        v_findings = validate_text(text, vault=vault_root, target=md_file, index=index)
        if not (len(v_findings) == 1 and "do not match any built-in template" in v_findings[0][1]):
            findings.extend(
                {"file": rel_file, "line": line, "level": "ERROR", "code": "ROUTED_NOTE_INVALID", "message": message}
                for line, message in v_findings
            )
            return findings
        schema = "builtin_deep" if "topics" in Path(rel_file).parts and manifest is None else "generic"
    is_builtin = schema.startswith("builtin_")

    if y_obj is not None:
        findings.extend(
            _check_frontmatter_rules(
                rel_file, y_obj, yaml_lines, index["ids_to_files"], pre_tags, schema, is_builtin, manifest
            )
        )

    if schema == "builtin_deep" and isinstance(y_obj, dict):
        from scriptorium.engines._decision import audit_note_against_contract, check_slug_and_forward_links, resolve_decisions

        body_text = "\n".join(lines[body_idx:]) if body_idx < len(lines) else ""
        topic_val = str(y_obj.get("topic") or "")
        aliases_val = y_obj.get("aliases") if isinstance(y_obj.get("aliases"), list) else []
        tags_val = y_obj.get("tags") if isinstance(y_obj.get("tags"), list) else []
        contract = resolve_decisions(
            topic_val,
            {"title": str(aliases_val[0]) if aliases_val else md_file.stem, "math_level": 0},
            topic_val,
            tags=[str(t) for t in tags_val],
        )
        contract["math_level"] = None
        for c_line, c_msg in audit_note_against_contract(body_text, contract):
            findings.append({
                "file": rel_file,
                "line": body_idx + c_line,
                "level": "ERROR",
                "code": "DECISION_MATRIX_VIOLATION",
                "message": c_msg,
            })
        for s_line, s_msg in check_slug_and_forward_links(
            body_text,
            metadata=y_obj,
            target_filename=md_file.name,
            existing_stems=set(index["stems"].keys()),
        ):
            findings.append({
                "file": rel_file,
                "line": body_idx + s_line,
                "level": "ERROR",
                "code": "LINK_HYGIENE",
                "message": s_msg,
            })

    in_fence = in_mermaid = in_display = False
    display_start_line = fence_len = s5_line = s5_impl_count = cur_q_line = 0
    fence_char = cur_q_title = ""
    in_section_5 = in_section_6 = has_key_equations = cur_q_callout = False
    q_blocks: list[tuple[int, str, bool]] = []

    for idx, raw_line in enumerate(lines):
        line_no = idx + 1
        stripped = raw_line.strip()

        m_fence = re.match(r"^\s*(`{3,}|~{3,})(.*)$", raw_line)
        if m_fence and not in_display:
            marker = m_fence.group(1)
            lang = m_fence.group(2).strip().lower()
            if not in_fence:
                in_fence, in_mermaid, fence_char, fence_len = True, lang == "mermaid", marker[0], len(marker)
                continue
            if marker[0] == fence_char and len(marker) >= fence_len and stripped[len(marker) :].strip() == "":
                in_fence = in_mermaid = False
                continue
        if in_fence:
            if in_mermaid and is_builtin and "$" in raw_line:
                findings.append({
                    "file": rel_file,
                    "line": line_no,
                    "level": "ERROR",
                    "code": "MERMAID_RAW_MATH_DELIMITER",
                    "message": "Raw '$' inside Mermaid node label; use Unicode.",
                })
            continue

        if UNRESOLVED_TPL_RE.search(raw_line):
            findings.append({
                "file": rel_file,
                "line": line_no,
                "level": "ERROR",
                "code": "UNRESOLVED_TEMPLATE_SYNTAX",
                "message": "Unresolved dynamic template placeholder (<% ... %> or {{...}}) in note.",
            })
        if m_ph := PLACEHOLDER_RE.search(raw_line):
            findings.append({
                "file": rel_file,
                "line": line_no,
                "level": "ERROR",
                "code": "PLACEHOLDER_TOKEN",
                "message": f"Unresolved placeholder token '{m_ph.group(0)}'.",
            })

        findings.extend(_check_wikilink_line(raw_line, rel_file, line_no, md_file, vault_root, index))
        if idx < body_idx:
            continue

        if raw_line.lstrip().startswith("> [!abstract] Key Equations"):
            has_key_equations = True

        if schema == "builtin_deep":
            if re.match(r"^##\s+5\.\s+", stripped):
                in_section_5, s5_line = True, line_no
            elif in_section_5 and re.match(r"^##\s+\d+\.\s+", stripped):
                in_section_5 = False
            if in_section_5 and re.match(r"^###\s+Implementation\b", stripped, flags=re.IGNORECASE):
                s5_impl_count += 1

            if re.match(r"^##\s+6\.\s+", stripped):
                in_section_6 = True
            elif in_section_6 and re.match(r"^##\s+\d+\.\s+", stripped):
                if cur_q_line:
                    q_blocks.append((cur_q_line, cur_q_title, cur_q_callout))
                    cur_q_line = 0
                in_section_6 = False
            if in_section_6:
                if re.match(r"^####\s+", stripped):
                    if cur_q_line:
                        q_blocks.append((cur_q_line, cur_q_title, cur_q_callout))
                    cur_q_line, cur_q_title, cur_q_callout = line_no, stripped, False
                elif cur_q_line and stripped.startswith("> [!example]-"):
                    cur_q_callout = True
                if BANNED_S6_LABELS_RE.search(raw_line):
                    findings.append({
                        "file": rel_file,
                        "line": line_no,
                        "level": "ERROR",
                        "code": "FORBIDDEN_SECTION_6_STRUCTURE",
                        "message": f"Forbidden Section 6 scaffolding label on line {line_no}.",
                    })
            if re.search(r"</?(?:details|summary)\b", raw_line, flags=re.IGNORECASE):
                findings.append({
                    "file": rel_file,
                    "line": line_no,
                    "level": "ERROR",
                    "code": "FORBIDDEN_SECTION_6_STRUCTURE",
                    "message": "Forbidden raw <details>/<summary> HTML tag.",
                })

        if re.match(r"^\s*[\"'`]+#{1,6}[\"'`]+", raw_line):
            findings.append({
                "file": rel_file,
                "line": line_no,
                "level": "ERROR",
                "code": "QUOTED_HEADING_MARKER",
                "message": "Heading hashes wrapped in quotation marks.",
            })

        body_check = re.sub(r"^\s*>\s?", "", raw_line).strip()
        if body_check == "$$":
            if in_display:
                in_display = False
            else:
                in_display, display_start_line = True, line_no
            continue
        if in_display:
            continue

        findings.extend(_check_inline_math_delimiters(raw_line, stripped, rel_file, line_no))

    if in_section_6 and cur_q_line:
        q_blocks.append((cur_q_line, cur_q_title, cur_q_callout))
    if in_display:
        findings.append({
            "file": rel_file,
            "line": display_start_line,
            "level": "ERROR",
            "code": "DELIMITER_IMBALANCE",
            "message": "Unclosed display math '$$' block.",
        })

    body_text = "\n".join(lines[body_idx:])
    findings.extend(
        _check_builtin_schema_rules(
            rel_file, schema, body_text, body_idx, has_key_equations, s5_line, s5_impl_count, q_blocks
        )
    )
    # Enforce local raster image resolution & valid non-corrupt bytes for non-legacy embeds
    from scriptorium.engines.composition.media import validate_visual_embeds

    vis_report = validate_visual_embeds(text, note_path=md_file, vault_root=vault_root)
    for err in vis_report.get("errors", []):
        if is_builtin or schema == "routed":
            findings.append({
                "file": rel_file,
                "line": int(err["line"]),
                "level": "ERROR",
                "code": "INVALID_VISUAL_EMBED",
                "message": f"Image embed '{err['target']}' failed visual verification: {err['reason']}",
            })
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Template-aware, scoped Obsidian vault validator with safe mechanical --fix."
    )
    parser.add_argument("vault_path", help="Path to the Obsidian vault root directory.")
    parser.add_argument("target_folder", nargs="?", default=None, help="Optional subfolder within vault to audit.")
    parser.add_argument("--files", nargs="+", default=None, help="Explicit vault-relative file(s) to validate/fix.")
    parser.add_argument("--manifest", default=None, help="Operational provenance manifest JSON path.")
    parser.add_argument("--fix", action="store_true", help="Apply mechanical repairs to scoped files, then re-validate.")
    args = parser.parse_args(argv)

    vault_path = Path(args.vault_path)
    if not vault_path.is_dir():
        print(f"ERROR: Vault path is not an existing directory: {vault_path}", file=sys.stderr)
        return 2
    vault_root = Path(os.path.realpath(vault_path))

    manifest: dict[str, Any] | None = None
    if args.manifest:
        m_path = Path(args.manifest)
        if not m_path.is_file():
            print(f"ERROR: Manifest not found: {m_path}", file=sys.stderr)
            return 2
        manifest = json.loads(m_path.read_text(encoding="utf-8"))
        tpl_path = manifest.get("template_path")
        tpl_hash = manifest.get("template_hash")
        if tpl_path and tpl_hash:
            cand_tpl = vault_root / tpl_path
            if not cand_tpl.is_file() or not _is_within_vault(vault_root, cand_tpl):
                print(f"ERROR  {tpl_path}:1  STALE_TEMPLATE_PLAN", file=sys.stdout)
                return 1
            cur_hash = hashlib.sha256(cand_tpl.read_text(encoding="utf-8").encode("utf-8")).hexdigest()[:16]
            if cur_hash != tpl_hash:
                print(f"ERROR  {tpl_path}:1  STALE_TEMPLATE_PLAN", file=sys.stdout)
                return 1

    # Determine scoped files
    scoped_files: list[Path] = []
    target_list = args.files or (manifest.get("outputs") if manifest else None)
    if target_list:
        for rel in target_list:
            cand = vault_root / rel
            if not _is_within_vault(vault_root, cand):
                print(f"ERROR: Path escapes vault root: {rel}", file=sys.stderr)
                return 2
            if not cand.is_file():
                print(f"ERROR: Scoped file not found: {rel}", file=sys.stderr)
                return 2
            scoped_files.append(cand)
    else:
        scan_root = (vault_root / args.target_folder) if args.target_folder else vault_root
        if not _is_within_vault(vault_root, scan_root) or not scan_root.is_dir():
            print(f"ERROR: Invalid target folder: {scan_root}", file=sys.stderr)
            return 2
        scoped_files = _iter_markdown_files(vault_root, scan_root)

    repairs: list[tuple[str, int, str]] = []
    if args.fix:
        for md_file in scoped_files:
            # Determine if built-in style applies before running style-only repairs
            rel = md_file.relative_to(vault_root).as_posix()
            lines = md_file.read_text(encoding="utf-8").splitlines()
            yl, _ = _split_frontmatter_lines(lines)
            y_obj = yaml.safe_load("\n".join(yl)) if yl else None
            schema = _resolve_note_schema(rel, y_obj if isinstance(y_obj, dict) else None, manifest)
            if schema == "routed":
                continue  # Routed notes are linted in draft and published without automatic repair.
            repairs.extend(
                apply_mechanical_fixes(
                    md_file,
                    vault_root,
                    enforce_builtin_style=schema.startswith("builtin_"),
                )
            )

    index = build_vault_index(vault_root)
    findings: list[dict[str, Any]] = []
    for md_file in scoped_files:
        findings.extend(validate_file(md_file, vault_root, index, manifest=manifest))

    for f in findings:
        print(f"{f['level']}  {f['file']}:{f['line']}  {f['code']}")
    for r_file, r_line, r_code in repairs:
        print(f"FIXED  {r_file}:{r_line}  {r_code}")

    err_count = sum(1 for f in findings if f["level"] == "ERROR")
    print(f"\nScanned: {len(scoped_files)} notes\nErrors: {err_count}\nRepairs: {len(repairs)}")
    return 0 if err_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
