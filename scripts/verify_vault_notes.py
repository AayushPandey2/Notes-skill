#!/usr/bin/env python3
r"""Deterministic, read-by-default Obsidian vault validator with safe --fix repairs.

Default mode inspects notes without modifying any file.
--fix applies only supported mechanical repairs (inline math boundary whitespace,
quoted Markdown heading markers, missing clean title in YAML aliases, and
unprefixed blank lines inside `> [!example]-` callouts), then re-runs validation.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import os
import re
from pathlib import Path
from typing import Any

import yaml

MANDATORY_TOPIC_KEYS = ("id", "title", "aliases", "base_domain", "master_topic", "topic", "tags")

RAW_LATEX_IN_YAML_RE = re.compile(
    r"\\(?:mathbb|mathbf|mathcal|mathrm|text|operatorname|sum|prod|int|frac|dfrac|"
    r"hat|widehat|bar|tilde|vec|left|right|ge|le|geq|leq|neq|approx|equiv|to|"
    r"implies|iff|land|lor|forall|exists|in|notin|theta|alpha|beta|gamma|delta|"
    r"lambda|sigma|omega|eta|rho|lVert|rVert|lvert|rvert|mid|sqrt|cdot|times)\b"
)

PLACEHOLDER_RE = re.compile(r"(?:<exact-url>|<source-anchor>|PLACEHOLDER_URL|\[\[none\]\])")
BANNED_S6_LABELS_RE = re.compile(
    r"\b(?:I\s+Do|We\s+Do|You\s+Do|Worked\s+Trace|Faded\s+Variation|Drill\s+[AB])\b",
    flags=re.IGNORECASE,
)


def _split_frontmatter_lines(lines: list[str]) -> tuple[list[str], int] | tuple[None, int]:
    """Return (yaml_lines, body_start_idx_0based) or (None, 0)."""
    if not lines or lines[0].strip() != "---":
        return None, 0
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[1:idx], idx + 1
    return None, 0


def _clean_title_for_alias(title: str) -> str:
    """Strip numeric sequence prefix like '07-' or '01. ' without removing meaningful numbers."""
    cleaned = title.strip()
    cleaned = re.sub(r"^\d{1,3}\s*(?:[-–—.]\s*|\s+-\s+)", "", cleaned).strip()
    return cleaned


def _heading_slug(heading: str) -> str:
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading.strip())
    s = s.replace("`", "").replace("*", "").replace("~", "").lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def _extract_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
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
    return anchors


def _iter_markdown_files(vault_root: Path, scan_root: Path) -> list[Path]:
    md_files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(scan_root, followlinks=False):
        dirnames[:] = sorted(
            d for d in dirnames if not d.startswith(".") and d.lower() != "scratchpad"
        )
        for fname in sorted(filenames):
            if fname.lower().endswith(".md"):
                full = Path(dirpath) / fname
                if not full.is_symlink():
                    md_files.append(full)
    return sorted(md_files, key=lambda p: p.relative_to(vault_root).as_posix().lower())


def build_vault_index(vault_root: Path) -> dict[str, Any]:
    """Index stems, titles, aliases, IDs, and heading anchors across the entire vault."""
    stems: dict[str, Path] = {}
    titles: dict[str, Path] = {}
    aliases: dict[str, Path] = {}
    ids_map: dict[str, Path] = {}
    ids_to_files: dict[str, list[Path]] = {}
    anchors_by_file: dict[Path, set[str]] = {}

    for md_file in _iter_markdown_files(vault_root, vault_root):
        stems[md_file.stem.lower()] = md_file
        rel_no_ext = md_file.relative_to(vault_root).with_suffix("").as_posix().lower()
        stems[rel_no_ext] = md_file

        try:
            text = md_file.read_text(encoding="utf-8")
        except OSError:
            continue

        anchors_by_file[md_file] = _extract_anchors(text)
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
            except yaml.YAMLError:
                pass

    return {
        "stems": stems,
        "titles": titles,
        "aliases": aliases,
        "ids_map": ids_map,
        "ids_to_files": ids_to_files,
        "anchors_by_file": anchors_by_file,
    }


# ---------------------------------------------------------------------------
# Mechanical Auto-Repairs (--fix only)
# ---------------------------------------------------------------------------

def _repair_inline_math_whitespace_in_line(line: str) -> tuple[str, bool]:
    """Trim spaces immediately inside inline $ ... $ delimiters without altering code or $$."""
    # Preserve escaped \$ and inline `code` spans
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
            # Display math $$...$$ on single line -> leave untouched
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
    """Insert clean title alias into YAML frontmatter lines without rewriting body."""
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

    # Case 1: aliases: [...] flow list
    for idx, yl in enumerate(new_lines):
        m_flow = re.match(r"^aliases\s*:\s*\[(.*)\]\s*$", yl.strip())
        if m_flow:
            inner = m_flow.group(1).strip()
            new_lines[idx] = f"aliases: [{quoted_alias}]" if not inner else f"aliases: [{inner}, {quoted_alias}]"
            return new_lines, True

    # Case 2: aliases: block list
    for idx, yl in enumerate(new_lines):
        if re.match(r"^aliases\s*:\s*$", yl.strip()):
            insert_at = idx + 1
            while insert_at < len(new_lines) and re.match(r"^\s+-\s+", new_lines[insert_at]):
                insert_at += 1
            new_lines.insert(insert_at, f"  - {quoted_alias}")
            return new_lines, True

    # Case 3: aliases key missing entirely -> insert after title: (or at end)
    insert_at = len(new_lines)
    for idx, yl in enumerate(new_lines):
        if re.match(r"^title\s*:", yl):
            insert_at = idx + 1
            break
    new_lines.insert(insert_at, f"  - {quoted_alias}")
    new_lines.insert(insert_at, "aliases:")
    return new_lines, True


def apply_mechanical_fixes(md_file: Path, vault_root: Path) -> list[tuple[str, int, str]]:
    """Apply Rules A-D in-place only when needed; return list of (rel_file, line, code)."""
    raw_bytes = md_file.read_bytes()
    newline = "\r\n" if b"\r\n" in raw_bytes else "\n"
    text = raw_bytes.decode("utf-8")
    had_trailing_nl = text.endswith("\n")
    lines = text.splitlines()
    rel_file = md_file.relative_to(vault_root).as_posix()
    repairs: list[tuple[str, int, str]] = []

    yaml_lines, body_idx = _split_frontmatter_lines(lines)
    if yaml_lines is not None:
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

    # Pass 1 on body lines: Rule A (inline math whitespace) & Rule B (quoted headings)
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

        # Rule B: Quoted heading markers
        m_qh = re.match(r"^(\s*)[\"'`]+(#{1,6})[\"'`]+(\s+.*)$", raw_line)
        if m_qh:
            lines[idx] = f"{m_qh.group(1)}{m_qh.group(2)}{m_qh.group(3)}"
            repairs.append((rel_file, line_no, "QUOTED_HEADING_FIXED"))

        # Rule A: Inline math boundary whitespace
        fixed_line, math_changed = _repair_inline_math_whitespace_in_line(lines[idx])
        if math_changed:
            lines[idx] = fixed_line
            repairs.append((rel_file, line_no, "INLINE_MATH_NORMALIZED"))

    # Pass 2 on body lines: Rule D (normalize blank lines inside > [!example]- callouts)
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
                    # Look ahead past consecutive blank lines: if next non-blank line still starts with '>'
                    # (not a new callout), then this blank line is inside the callout block.
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
# Blocking Validation Rules (Read-Only)
# ---------------------------------------------------------------------------

def _scan_yaml_for_latex(obj: Any, yaml_lines: list[str]) -> list[tuple[int, str, str]]:
    """Return list of (line_no, key_path, value_preview) for raw LaTeX or '$' in YAML."""
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


def validate_file(
    md_file: Path,
    vault_root: Path,
    index: dict[str, Any],
) -> list[dict[str, Any]]:
    """Validate one Markdown file; returns list of {file, line, level, code, message}."""
    findings: list[dict[str, Any]] = []
    rel_file = md_file.relative_to(vault_root).as_posix()
    text = md_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    is_topic_lesson = "topics" in md_file.relative_to(vault_root).parts

    stems = index["stems"]
    titles = index["titles"]
    aliases = index["aliases"]
    ids_map = index["ids_map"]
    ids_to_files = index["ids_to_files"]
    anchors_by_file = index["anchors_by_file"]

    yaml_lines, body_idx = _split_frontmatter_lines(lines)
    if yaml_lines is not None:
        try:
            y_obj = yaml.safe_load("\n".join(yaml_lines))
            if isinstance(y_obj, dict):
                for lno, key_path, val in _scan_yaml_for_latex(y_obj, yaml_lines):
                    findings.append(
                        {
                            "file": rel_file,
                            "line": lno,
                            "level": "ERROR",
                            "code": "LATEX_IN_FRONTMATTER",
                            "message": f"Raw LaTeX or '$' in YAML '{key_path}': {val[:60]!r}",
                        }
                    )
                fid = y_obj.get("id")
                if isinstance(fid, str) and len(ids_to_files.get(fid.strip(), [])) > 1:
                    findings.append(
                        {
                            "file": rel_file,
                            "line": 2,
                            "level": "ERROR",
                            "code": "DUPLICATE_YAML_ID",
                            "message": f"Duplicate YAML id '{fid}' across vault.",
                        }
                    )
                if is_topic_lesson:
                    for req in MANDATORY_TOPIC_KEYS:
                        if req not in y_obj:
                            findings.append(
                                {
                                    "file": rel_file,
                                    "line": 2,
                                    "level": "ERROR",
                                    "code": "MISSING_YAML_KEY",
                                    "message": f"Missing mandatory key '{req}' in YAML frontmatter.",
                                }
                            )
                    raw_title = y_obj.get("title")
                    if isinstance(raw_title, str) and raw_title.strip():
                        clean_alias = _clean_title_for_alias(raw_title)
                        existing_a = [str(a).strip().lower() for a in (y_obj.get("aliases") or [])]
                        if clean_alias and clean_alias.lower() not in existing_a:
                            findings.append(
                                {
                                    "file": rel_file,
                                    "line": 2,
                                    "level": "ERROR",
                                    "code": "MISSING_TITLE_ALIAS",
                                    "message": f"Clean title '{clean_alias}' missing from YAML aliases.",
                                }
                            )
        except yaml.YAMLError as exc:
            findings.append(
                {
                    "file": rel_file,
                    "line": 2,
                    "level": "ERROR",
                    "code": "YAML_SYNTAX_ERROR",
                    "message": f"Invalid YAML frontmatter: {exc}",
                }
            )

    in_fence = False
    in_mermaid = False
    in_display = False
    display_start_line = 0
    fence_char = ""
    fence_len = 0
    in_section_6 = False
    has_key_equations = False
    q_blocks: list[tuple[int, str, bool]] = []
    cur_q_line = 0
    cur_q_title = ""
    cur_q_callout = False

    for idx, raw_line in enumerate(lines):
        line_no = idx + 1
        stripped = raw_line.strip()

        m_fence = re.match(r"^\s*(`{3,}|~{3,})(.*)$", raw_line)
        if m_fence and not in_display:
            marker = m_fence.group(1)
            lang = m_fence.group(2).strip().lower()
            if not in_fence:
                in_fence = True
                in_mermaid = lang == "mermaid"
                fence_char = marker[0]
                fence_len = len(marker)
                continue
            if marker[0] == fence_char and len(marker) >= fence_len and stripped[len(marker) :].strip() == "":
                in_fence = False
                in_mermaid = False
                continue
        if in_fence:
            if in_mermaid and "$" in raw_line:
                findings.append(
                    {
                        "file": rel_file,
                        "line": line_no,
                        "level": "ERROR",
                        "code": "MERMAID_RAW_MATH_DELIMITER",
                        "message": "Raw '$' inside Mermaid node label; use Unicode.",
                    }
                )
            continue

        # Placeholder check
        m_ph = PLACEHOLDER_RE.search(raw_line)
        if m_ph:
            findings.append(
                {
                    "file": rel_file,
                    "line": line_no,
                    "level": "ERROR",
                    "code": "PLACEHOLDER_TOKEN",
                    "message": f"Unresolved placeholder token '{m_ph.group(0)}'.",
                }
            )

        # Wikilinks across YAML + Body (excluding external [text](url) links)
        for m_wl in re.finditer(r"\[\[([^\]]+)\]\]", raw_line):
            inner = m_wl.group(1)
            target_full = re.split(r"\\?\|", inner, maxsplit=1)[0].strip()
            if "#" in target_full:
                target_part, anchor_part = target_full.split("#", 1)
                target_part = target_part.strip()
                anchor_part = anchor_part.strip()
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
                    findings.append(
                        {
                            "file": rel_file,
                            "line": line_no,
                            "level": "ERROR",
                            "code": "UNRESOLVED_WIKILINK",
                            "message": f"Unresolved wikilink '[[{inner}]]'.",
                        }
                    )
                    continue

            if anchor_part:
                valid_anchors = anchors_by_file.get(resolved_target, set())
                a_norm = anchor_part.lower()
                a_slug = _heading_slug(anchor_part)
                if (
                    a_norm not in valid_anchors
                    and a_slug not in valid_anchors
                    and re.sub(r"-{2,}", "-", a_slug) not in valid_anchors
                ):
                    findings.append(
                        {
                            "file": rel_file,
                            "line": line_no,
                            "level": "ERROR",
                            "code": "UNRESOLVED_HEADING_ANCHOR",
                            "message": f"Heading anchor '#{anchor_part}' not found in '{resolved_target.name}'.",
                        }
                    )

        if idx < body_idx:
            continue

        if raw_line.lstrip().startswith("> [!abstract] Key Equations"):
            has_key_equations = True

        # Track Section 6 boundaries
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
                cur_q_line = line_no
                cur_q_title = stripped
                cur_q_callout = False
            elif cur_q_line and stripped.startswith("> [!example]-"):
                cur_q_callout = True

            if BANNED_S6_LABELS_RE.search(raw_line):
                findings.append(
                    {
                        "file": rel_file,
                        "line": line_no,
                        "level": "ERROR",
                        "code": "FORBIDDEN_SECTION_6_STRUCTURE",
                        "message": f"Forbidden Section 6 scaffolding label on line {line_no}.",
                    }
                )

        # Raw <details> / <summary> HTML tags anywhere in body
        if re.search(r"</?(?:details|summary)\b", raw_line, flags=re.IGNORECASE):
            findings.append(
                {
                    "file": rel_file,
                    "line": line_no,
                    "level": "ERROR",
                    "code": "FORBIDDEN_SECTION_6_STRUCTURE",
                    "message": "Forbidden raw <details>/<summary> HTML tag.",
                }
            )

        # Quoted heading markers
        if re.match(r"^\s*[\"'`]+#{1,6}[\"'`]+", raw_line):
            findings.append(
                {
                    "file": rel_file,
                    "line": line_no,
                    "level": "ERROR",
                    "code": "QUOTED_HEADING_MARKER",
                    "message": "Heading hashes wrapped in quotation marks.",
                }
            )

        # Display math $$
        body_check = re.sub(r"^\s*>\s?", "", raw_line).strip()
        if body_check == "$$":
            if in_display:
                in_display = False
            else:
                in_display = True
                display_start_line = line_no
            continue
        if in_display:
            continue

        # Mask single-line $$...$$ and inline `...` before checking inline $...$
        masked = re.sub(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$", " ", raw_line)
        masked = re.sub(r"`[^`]*`", " ", masked)
        is_table = stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 1

        i = 0
        n = len(masked)
        while i < n:
            if masked[i] == "\\" and i + 1 < n:
                i += 2
                continue
            if masked[i] == "$":
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
                    findings.append(
                        {
                            "file": rel_file,
                            "line": line_no,
                            "level": "ERROR",
                            "code": "DELIMITER_IMBALANCE",
                            "message": f"Unbalanced inline '$' delimiter on line {line_no}.",
                        }
                    )
                    break
                expr = masked[i + 1 : close_pos]
                if expr and (expr[0].isspace() or expr[-1].isspace()):
                    findings.append(
                        {
                            "file": rel_file,
                            "line": line_no,
                            "level": "ERROR",
                            "code": "INLINE_MATH_WHITESPACE",
                            "message": f"Whitespace immediately inside inline math delimiters: '${expr}$'.",
                        }
                    )
                if is_table and re.search(r"(?<!\\)\|", expr):
                    findings.append(
                        {
                            "file": rel_file,
                            "line": line_no,
                            "level": "ERROR",
                            "code": "TABLE_RAW_PIPE_IN_MATH",
                            "message": f"Unescaped '|' inside inline math in Markdown table: '${expr}$'.",
                        }
                    )
                i = close_pos + 1
                continue
            i += 1

    if in_section_6 and cur_q_line:
        q_blocks.append((cur_q_line, cur_q_title, cur_q_callout))

    if in_display:
        findings.append(
            {
                "file": rel_file,
                "line": display_start_line,
                "level": "ERROR",
                "code": "DELIMITER_IMBALANCE",
                "message": "Unclosed display math '$$' block.",
            }
        )

    if is_topic_lesson:
        if not has_key_equations:
            findings.append(
                {
                    "file": rel_file,
                    "line": body_idx + 1,
                    "level": "ERROR",
                    "code": "MISSING_KEY_EQUATIONS_CALLOUT",
                    "message": "Missing required '> [!abstract] Key Equations' callout.",
                }
            )
        if len(q_blocks) < 5:
            findings.append(
                {
                    "file": rel_file,
                    "line": body_idx + 1,
                    "level": "ERROR",
                    "code": "INSUFFICIENT_SECTION_6_QA",
                    "message": f"Section 6 requires at least 5 #### Question blocks; found {len(q_blocks)}.",
                }
            )
        for q_line, q_title, has_c in q_blocks:
            if not has_c:
                findings.append(
                    {
                        "file": rel_file,
                        "line": q_line,
                        "level": "ERROR",
                        "code": "MISSING_ANSWER_CALLOUT",
                        "message": f"Question '{q_title}' missing '> [!example]-' answer callout.",
                    }
                )

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic Obsidian vault validator with optional mechanical --fix repairs."
    )
    parser.add_argument("vault_path", help="Path to the Obsidian vault root directory.")
    parser.add_argument("target_folder", nargs="?", default=None, help="Optional subfolder within vault to audit.")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply supported mechanical formatting repairs, then re-run validation.",
    )
    args = parser.parse_args(argv)

    vault_path = Path(args.vault_path)
    if not vault_path.is_dir():
        print(f"ERROR: Vault path is not an existing directory: {vault_path}", file=sys.stderr)
        return 2

    vault_root = vault_path.resolve()
    scan_root = (vault_root / args.target_folder).resolve() if args.target_folder else vault_root
    if not scan_root.is_dir():
        print(f"ERROR: Target folder is not an existing directory: {scan_root}", file=sys.stderr)
        return 2

    files = _iter_markdown_files(vault_root, scan_root)
    repairs: list[tuple[str, int, str]] = []
    if args.fix:
        for md_file in files:
            repairs.extend(apply_mechanical_fixes(md_file, vault_root))

    index = build_vault_index(vault_root)
    findings: list[dict[str, Any]] = []
    for md_file in files:
        findings.extend(validate_file(md_file, vault_root, index))

    for f in findings:
        print(f"{f['level']}  {f['file']}:{f['line']}  {f['code']}")
    for r_file, r_line, r_code in repairs:
        print(f"FIXED  {r_file}:{r_line}  {r_code}")

    err_count = sum(1 for f in findings if f["level"] == "ERROR")
    print(f"\nScanned: {len(files)} notes\nErrors: {err_count}\nRepairs: {len(repairs)}")
    return 0 if err_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
