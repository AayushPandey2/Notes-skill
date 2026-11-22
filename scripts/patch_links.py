#!/usr/bin/env python3
"""Deterministic, non-destructive frontmatter and wikilink patcher for Scriptorium vaults.

Supports:
  - Frontmatter relationship & metadata patching without touching note bodies:
      python3 scripts/patch_links.py "<vault_path>" --file "<note.md>" \\
          --add-depends-on "[[01-intro|Intro]]" --set-next-topic "[[03-advanced|Advanced]]"
      python3 scripts/patch_links.py "<vault_path>" --file "<note.md>" \\
          --append-review-log "2026-11-18 | Score: 4/5 | Weak: boundary condition"
  - Safe wikilink target renaming across scoped files or the entire vault:
      python3 scripts/patch_links.py "<vault_path>" --rename-link "Old Note" "New Note" [--files ...]
  - Unified diff preview without writing to disk:
      ... --dry-run

Security & containment guarantees:
  - Resolves vault canonically; rejects '..' traversal and symlinks escaping the vault.
  - Preserves note bodies byte-for-byte during frontmatter-only edits.
  - Skips fenced code blocks, inline code, and HTML comments during body wikilink renames.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import difflib
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

from scriptorium.models import STRICT_KEYS, format_wikilink as _format_wikilink, split_frontmatter_lines
from vault_index import _iter_vault_markdown, is_within_vault, resolve_vault_root


WIKILINK_RE = re.compile(r"(!?\[\[)([^\]\r\n]+)(\]\])")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


# ---------------------------------------------------------------------------
# Path & Target Resolution
# ---------------------------------------------------------------------------

def _resolve_note_path(vault_root: Path, raw_path: str) -> Path:
    """Resolve a note path (relative to vault_root or absolute) and enforce containment."""
    if ".." in Path(raw_path).parts:
        raise ValueError(f"Path traversal ('..') is not allowed: {raw_path}")
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = vault_root / candidate
    if not candidate.exists():
        raise FileNotFoundError(f"Note file not found: {raw_path}")
    if not is_within_vault(vault_root, candidate):
        raise ValueError(f"Path escapes vault root: {raw_path}")
    resolved = Path(os.path.realpath(candidate))
    if not resolved.is_file():
        raise ValueError(f"Target is not a file: {raw_path}")
    return resolved


def _strip_wikilink_brackets(value: str) -> str:
    s = value.strip()
    if s.startswith("[[") and s.endswith("]]"):
        return s[2:-2].strip()
    return s


def _link_target_key(value: str) -> str:
    """Extract normalized target stem (without [[ ]], |alias, or #heading) for comparison."""
    inner = _strip_wikilink_brackets(value)
    if "|" in inner:
        inner = inner.split("|", 1)[0]
    if "#" in inner:
        inner = inner.split("#", 1)[0]
    return inner.strip().lower()


# ---------------------------------------------------------------------------
# Non-Destructive YAML Frontmatter Line Patching
# ---------------------------------------------------------------------------

def _split_frontmatter_and_body(text: str) -> tuple[list[str], str, str]:
    """Return (yaml_lines, body_with_leading_newline, line_ending).

    Raises ValueError if the file does not start with valid '---' frontmatter.
    """
    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines(keepends=False)
    if not lines or lines[0].strip() != "---":
        raise ValueError("Note does not have YAML frontmatter starting with '---'.")
    yaml_lines, body_start = split_frontmatter_lines(lines)
    if yaml_lines is None:
        raise ValueError("Unterminated YAML frontmatter (missing closing '---').")
    body_lines = lines[body_start:]
    body = newline.join(body_lines)
    if text.endswith(("\n", "\r\n")) and (body_lines or body_start < len(lines)):
        body += newline
    elif text.endswith(("\n", "\r\n")) and not body_lines:
        body = newline
    return yaml_lines, body, newline


def _yaml_quote(value: str) -> str:
    """Quote a YAML scalar safely (double-quoting wikilinks or special chars)."""
    s = str(value)
    needs_quotes = (
        s == ""
        or s.startswith(("[", "{", "*", "&", "!", "|", ">", "'", '"', "%", "@", "`", "- ", "? "))
        or ": " in s
        or "#" in s
    )
    if not needs_quotes:
        return s
    escaped = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _find_yaml_key_span(yaml_lines: list[str], key: str) -> tuple[int, int] | None:
    """Find (start_idx, end_idx_exclusive) for a top-level YAML key."""
    key_re = re.compile(rf"^{re.escape(key)}\s*:(.*)$")
    for i, line in enumerate(yaml_lines):
        if line.startswith((" ", "\t", "#", "-")):
            continue
        m = key_re.match(line)
        if not m:
            continue
        j = i + 1
        while j < len(yaml_lines):
            nxt = yaml_lines[j]
            if nxt.strip() == "" or nxt.startswith((" ", "\t", "-")):
                j += 1
                continue
            break
        # Trim trailing blank lines from the span
        while j > i + 1 and yaml_lines[j - 1].strip() == "":
            j -= 1
        return i, j
    return None


def _parse_existing_list(meta: dict[str, Any], key: str) -> list[str]:
    val = meta.get(key)
    if val is None:
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if x is not None and str(x).strip()]
    if isinstance(val, str) and val.strip():
        return [val.strip()]
    return []


def _render_yaml_list_block(key: str, items: list[str]) -> list[str]:
    if not items:
        return [f"{key}: []"]
    out = [f"{key}:"]
    for item in items:
        out.append(f"  - {_yaml_quote(item)}")
    return out


def _set_yaml_list_key(yaml_lines: list[str], key: str, items: list[str]) -> list[str]:
    new_block = _render_yaml_list_block(key, items)
    span = _find_yaml_key_span(yaml_lines, key)
    if span is not None:
        start, end = span
        return yaml_lines[:start] + new_block + yaml_lines[end:]
    # Insert before tags if present, else append at end
    tags_span = _find_yaml_key_span(yaml_lines, "tags")
    if tags_span is not None and key != "tags":
        pos = tags_span[0]
        return yaml_lines[:pos] + new_block + yaml_lines[pos:]
    return yaml_lines + new_block


def _set_yaml_scalar_key(yaml_lines: list[str], key: str, value: str | None) -> list[str]:
    span = _find_yaml_key_span(yaml_lines, key)
    if value is None:
        if span is None:
            return yaml_lines
        return yaml_lines[: span[0]] + yaml_lines[span[1] :]
    new_line = f"{key}: {_yaml_quote(value)}"
    if span is not None:
        return yaml_lines[: span[0]] + [new_line] + yaml_lines[span[1] :]
    tags_span = _find_yaml_key_span(yaml_lines, "tags")
    if tags_span is not None:
        pos = tags_span[0]
        return yaml_lines[:pos] + [new_line] + yaml_lines[pos:]
    return yaml_lines + [new_line]


def patch_frontmatter_text(
    text: str,
    *,
    add_depends_on: list[str] | None = None,
    remove_depends_on: list[str] | None = None,
    set_next_topic: str | None = None,
    clear_next_topic: bool = False,
    append_review_log: list[str] | None = None,
    add_aliases: list[str] | None = None,
    add_tags: list[str] | None = None,
    set_status: str | None = None,
) -> tuple[str, bool]:
    """Patch YAML frontmatter fields in memory, returning (new_text, changed).

    Preserves the note body verbatim.
    """
    yaml_lines, body, newline = _split_frontmatter_and_body(text)
    yaml_raw = "\n".join(yaml_lines)
    meta = yaml.safe_load(yaml_raw)
    if meta is None:
        meta = {}
    if not isinstance(meta, dict):
        raise ValueError("YAML frontmatter must be a mapping.")

    if set(meta) == set(STRICT_KEYS):
        additions = []
        if add_depends_on:
            additions.append("**Prerequisites** :: " + ", ".join(map(_format_wikilink, add_depends_on)))
        if remove_depends_on:
            raise ValueError("Remove body prerequisites explicitly; strict notes have no depends_on YAML key.")
        if append_review_log:
            additions.extend("**Review** :: " + entry.strip() for entry in append_review_log if entry.strip())
        if set_status is not None:
            additions.append("**Status** :: " + set_status.strip())
        body += "".join(newline + entry + newline for entry in additions)
        add_depends_on = append_review_log = None
        set_status = None
    updated_lines = list(yaml_lines)

    # 1. depends_on
    if add_depends_on or remove_depends_on:
        deps = _parse_existing_list(meta, "depends_on")
        if remove_depends_on:
            rem_keys = {_link_target_key(x) for x in remove_depends_on}
            rem_raw = {x.strip().lower() for x in remove_depends_on}
            deps = [
                d
                for d in deps
                if _link_target_key(d) not in rem_keys and d.strip().lower() not in rem_raw
            ]
        if add_depends_on:
            existing_keys = {_link_target_key(d) for d in deps}
            for item in add_depends_on:
                formatted = _format_wikilink(item)
                key = _link_target_key(formatted)
                if key not in existing_keys:
                    deps.append(formatted)
                    existing_keys.add(key)
        updated_lines = _set_yaml_list_key(updated_lines, "depends_on", deps)

    # 2. nexttopics / next_topic
    if "nexttopics" in meta or "next_topic" not in meta:
        if clear_next_topic:
            updated_lines = _set_yaml_list_key(updated_lines, "nexttopics", [])
        elif set_next_topic is not None:
            existing_next = _parse_existing_list(meta, "nexttopics")
            formatted = _format_wikilink(set_next_topic)
            if _link_target_key(formatted) not in {_link_target_key(x) for x in existing_next}:
                existing_next.append(formatted)
            updated_lines = _set_yaml_list_key(updated_lines, "nexttopics", existing_next)
    elif clear_next_topic:
        updated_lines = _set_yaml_scalar_key(updated_lines, "next_topic", None)
    elif set_next_topic is not None:
        updated_lines = _set_yaml_scalar_key(updated_lines, "next_topic", _format_wikilink(set_next_topic))

    # 3. review_log
    if append_review_log:
        logs = _parse_existing_list(meta, "review_log")
        for entry in append_review_log:
            cleaned = entry.strip()
            if cleaned:
                logs.append(cleaned)
        updated_lines = _set_yaml_list_key(updated_lines, "review_log", logs)

    # 4. aliases
    if add_aliases:
        aliases = _parse_existing_list(meta, "aliases")
        seen = {a.lower() for a in aliases}
        for alias in add_aliases:
            cleaned = alias.strip()
            if cleaned and cleaned.lower() not in seen:
                aliases.append(cleaned)
                seen.add(cleaned.lower())
        updated_lines = _set_yaml_list_key(updated_lines, "aliases", aliases)

    # 5. tags
    if add_tags:
        tags = _parse_existing_list(meta, "tags")
        seen_tags = {t.lstrip("#").lower() for t in tags}
        for tag in add_tags:
            cleaned = tag.strip().lstrip("#")
            if cleaned and cleaned.lower() not in seen_tags:
                tags.append(cleaned)
                seen_tags.add(cleaned.lower())
        updated_lines = _set_yaml_list_key(updated_lines, "tags", tags)

    # 6. status
    if set_status is not None:
        updated_lines = _set_yaml_scalar_key(updated_lines, "status", set_status.strip())

    # Validate resulting YAML before returning
    rebuilt_yaml = "\n".join(updated_lines)
    parsed_after = yaml.safe_load(rebuilt_yaml)
    if not isinstance(parsed_after, dict):
        raise ValueError("Patched YAML frontmatter failed validation.")

    new_text = f"---{newline}" + newline.join(updated_lines) + f"{newline}---"
    if body:
        if not body.startswith(("\n", "\r\n")):
            new_text += newline
        new_text += body
    elif text.endswith(("\n", "\r\n")):
        new_text += newline

    return new_text, new_text != text


# ---------------------------------------------------------------------------
# Safe Wikilink Renaming (Frontmatter + Body, Skipping Code/Comments)
# ---------------------------------------------------------------------------

def _replace_wikilinks_in_segment(segment: str, old_key: str, new_target: str) -> str:
    def _repl(match: re.Match[str]) -> str:
        prefix, inner, suffix = match.group(1), match.group(2), match.group(3)
        alias_part = ""
        target_and_anchor = inner
        if "|" in inner:
            target_and_anchor, alias = inner.split("|", 1)
            alias_part = "|" + alias
        anchor_part = ""
        target = target_and_anchor
        if "#" in target_and_anchor:
            target, anchor = target_and_anchor.split("#", 1)
            anchor_part = "#" + anchor
        if target.strip().lower() == old_key:
            return f"{prefix}{new_target}{anchor_part}{alias_part}{suffix}"
        return match.group(0)

    return WIKILINK_RE.sub(_repl, segment)


def rename_wikilink_in_text(text: str, old_target: str, new_target: str) -> tuple[str, bool]:
    """Rename [[old_target]] -> [[new_target]] preserving anchors, aliases, and code blocks."""
    old_key = _link_target_key(old_target)
    clean_new = _strip_wikilink_brackets(new_target)
    if not old_key or not clean_new:
        return text, False

    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines(keepends=False)
    out_lines: list[str] = []
    in_fence = False
    fence_char = ""
    in_html_comment = False

    for line in lines:
        fence_m = FENCE_RE.match(line)
        if fence_m:
            marker = fence_m.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_char = marker
            elif marker == fence_char:
                in_fence = False
                fence_char = ""
            out_lines.append(line)
            continue

        if in_fence:
            out_lines.append(line)
            continue

        if in_html_comment:
            if "-->" in line:
                in_html_comment = False
            out_lines.append(line)
            continue

        if "<!--" in line:
            if "-->" not in line.split("<!--", 1)[1]:
                in_html_comment = True
            # Still skip rewriting inside inline HTML comment segments
            parts = re.split(r"(<!--[\s\S]*?-->)", line)
            rebuilt = []
            for part in parts:
                if part.startswith("<!--"):
                    rebuilt.append(part)
                else:
                    rebuilt.append(_replace_inline_safe(part, old_key, clean_new))
            out_lines.append("".join(rebuilt))
            continue

        out_lines.append(_replace_inline_safe(line, old_key, clean_new))

    new_text = newline.join(out_lines)
    if text.endswith(("\n", "\r\n")):
        new_text += newline
    return new_text, new_text != text


def _replace_inline_safe(line: str, old_key: str, clean_new: str) -> str:
    """Replace wikilinks in a line while skipping `inline code` spans."""
    parts = re.split(r"(`[^`]*`)", line)
    for idx, part in enumerate(parts):
        if idx % 2 == 0:
            parts[idx] = _replace_wikilinks_in_segment(part, old_key, clean_new)
    return "".join(parts)


# ---------------------------------------------------------------------------
# Unified Diff & CLI
# ---------------------------------------------------------------------------

def make_unified_diff(rel_path: str, old_text: str, new_text: str) -> str:
    return "".join(
        difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=f"a/{rel_path}",
            tofile=f"b/{rel_path}",
        )
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Non-destructively patch YAML frontmatter links/metadata or rename wikilinks."
    )
    parser.add_argument("vault_path", nargs="?", help="Path to Obsidian vault.")
    parser.add_argument("--file", dest="target_file", help="Single note path to patch (for frontmatter edits).")
    parser.add_argument("--files", nargs="+", help="Scoped note paths for --rename-link.")
    parser.add_argument("--add-depends-on", action="append", default=[], help="Add entry to depends_on.")
    parser.add_argument("--remove-depends-on", action="append", default=[], help="Remove entry from depends_on.")
    parser.add_argument("--set-next-topic", help="Set next_topic wikilink.")
    parser.add_argument("--clear-next-topic", action="store_true", help="Remove next_topic from frontmatter.")
    parser.add_argument("--append-review-log", action="append", default=[], help="Append entry to review_log.")
    parser.add_argument("--add-alias", action="append", default=[], help="Add alias to aliases.")
    parser.add_argument("--add-tag", action="append", default=[], help="Add tag to tags.")
    parser.add_argument("--set-status", help="Set status scalar in frontmatter.")
    parser.add_argument(
        "--rename-link",
        nargs=2,
        metavar=("OLD_TARGET", "NEW_TARGET"),
        help="Rename [[OLD_TARGET]] -> [[NEW_TARGET]] across --files or entire vault.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview unified diff without writing to disk.")
    parser.add_argument("--json", action="store_true", help="Output structured JSON summary.")
    args = parser.parse_args(argv)

    try:
        vault_root = resolve_vault_root(args.vault_path)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    has_fm_ops = any(
        [
            args.add_depends_on,
            args.remove_depends_on,
            args.set_next_topic is not None,
            args.clear_next_topic,
            args.append_review_log,
            args.add_alias,
            args.add_tag,
            args.set_status is not None,
        ]
    )

    if not has_fm_ops and not args.rename_link:
        print("ERROR: No patch operation specified.", file=sys.stderr)
        return 2

    if has_fm_ops and not args.target_file:
        print("ERROR: Frontmatter operations require --file <note.md>.", file=sys.stderr)
        return 2

    modified: list[str] = []
    unchanged: list[str] = []
    diffs: list[str] = []

    try:
        if has_fm_ops:
            note_path = _resolve_note_path(vault_root, args.target_file)
            rel = note_path.relative_to(vault_root).as_posix()
            old_text = note_path.read_text(encoding="utf-8")
            new_text, changed = patch_frontmatter_text(
                old_text,
                add_depends_on=args.add_depends_on,
                remove_depends_on=args.remove_depends_on,
                set_next_topic=args.set_next_topic,
                clear_next_topic=args.clear_next_topic,
                append_review_log=args.append_review_log,
                add_aliases=args.add_alias,
                add_tags=args.add_tag,
                set_status=args.set_status,
            )
            if changed:
                modified.append(rel)
                if args.dry_run:
                    diffs.append(make_unified_diff(rel, old_text, new_text))
                else:
                    note_path.write_text(new_text, encoding="utf-8")
            else:
                unchanged.append(rel)

        if args.rename_link:
            old_target, new_target = args.rename_link
            if args.files:
                targets = [_resolve_note_path(vault_root, f) for f in args.files]
            else:
                targets, _ = _iter_vault_markdown(vault_root)

            for note_path in targets:
                rel = note_path.relative_to(vault_root).as_posix()
                old_text = note_path.read_text(encoding="utf-8")
                new_text, changed = rename_wikilink_in_text(old_text, old_target, new_target)
                if changed:
                    if rel not in modified:
                        modified.append(rel)
                    if args.dry_run:
                        diffs.append(make_unified_diff(rel, old_text, new_text))
                    else:
                        note_path.write_text(new_text, encoding="utf-8")
                elif rel not in modified and rel not in unchanged:
                    unchanged.append(rel)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        payload = {
            "dry_run": args.dry_run,
            "modified": modified,
            "unchanged_count": len(unchanged),
            "diffs": diffs if args.dry_run else [],
        }
        print(json.dumps(payload, indent=2))
    else:
        if args.dry_run:
            if diffs:
                print("\n".join(diffs), end="")
            else:
                print("Dry run: no changes.")
        else:
            print(f"Patched {len(modified)} file(s); {len(unchanged)} unchanged.")
            for m in modified:
                print(f"  - {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
