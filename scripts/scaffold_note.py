#!/usr/bin/env python3
"""Scaffold adaptive deep-study notes, other built-in routes, and syllabus maps."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
import re
from datetime import date
from pathlib import Path
import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from vault_index import is_within_vault, resolve_vault_root
from note_layout import ADAPTIVE_ROUTES, DEEP_ROUTES, ROUTES, body_skeleton
from decision_matrix import resolve_decisions


def _slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return s or "note"


def _yaml_quote(value: str) -> str:
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


def _format_wikilink(value: str) -> str:
    s = value.strip()
    if s.startswith("[[") and s.endswith("]]"):
        return s
    return f"[[{s}]]"


def render_deep_note_skeleton(
    *,
    note_id: str,
    number: str,
    title: str,
    base_domain: str,
    master_topic: str,
    topic: str,
    aliases: list[str] | None = None,
    tags: list[str] | None = None,
    depends_on: list[str] | None = None,
    next_topic: str | None = None,
) -> str:
    """Compatibility entry point for the canonical adaptive deep-study scaffold."""
    args = argparse.Namespace(
        template="deepstudy-master", topic=topic, title=title, number=number,
        base_domain=base_domain, master_topic=master_topic, aliases=aliases or [],
        tags=tags or [], next_topic=next_topic, depends_on=depends_on or [],
        math_level=0, narrow_practice=False, compared_notes=[],
    )
    return render_routed_note(args, note_id)


def render_syllabus_skeleton(
    *,
    note_id: str,
    topic: str,
    base_domain: str,
    master_topic: str,
    allowed_subtopics: list[str] | None = None,
    excluded_topics: list[str] | None = None,
    tags: list[str] | None = None,
) -> str:
    """Render a deterministic 00-MOC-<topic-slug>.md Syllabus & Learning Graph contract."""
    allowed = [s.strip() for s in (allowed_subtopics or []) if s.strip()] or ["01-intro.md"]
    excluded = [s.strip() for s in (excluded_topics or []) if s.strip()] or [
        "<Adjacent Topic> (separate topic — link only)"
    ]
    tag_list = list(
        dict.fromkeys(
            [t.strip().lstrip("#") for t in (tags or []) if t.strip()]
            or [_slugify(base_domain), _slugify(master_topic), _slugify(topic), "moc"]
        )
    )
    if "moc" not in tag_list:
        tag_list.append("moc")

    lines: list[str] = [
        "---",
        f"id: {_yaml_quote(note_id)}",
        "aliases:",
        f"  - {_yaml_quote(f'{topic} — Syllabus & Learning Graph')}",
        f"  - {_yaml_quote(f'{topic} Syllabus')}",
        f"  - {_yaml_quote(f'{topic} MOC')}",
        f"topic: {_yaml_quote(topic)}",
        "tags:",
    ]
    for t in tag_list:
        lines.append(f"  - {_yaml_quote(t)}")
    lines.append("nexttopics: []")
    lines.extend(
        [
            "---",
            "",
            f"# {topic} — Syllabus & Learning Graph",
            "",
            "## 1. Scope Boundary Contract",
            f"- **Core Learning Objective:** <!-- Define the exact start-to-end boundary of {topic}. -->",
            "- **In-Scope Subtopics (Strict Allowlist):**",
        ]
    )
    for idx, sub in enumerate(allowed, start=1):
        lines.append(f"  {idx}. `{sub}` — <!-- 1-line scope -->")
    lines.append("- **Explicitly Out-of-Scope (Do-Not-Create Fence):**")
    for exc in excluded:
        lines.append(f"  - **{exc}**")

    lines.extend(
        [
            "",
            "## 2. Detailed Learning-Flow Graph",
            "",
            "```mermaid",
            "flowchart TD",
        ]
    )
    for idx, sub in enumerate(allowed, start=1):
        stem = Path(sub).stem
        lines.append(f'    N{idx}["{stem}"]')
    for idx in range(1, len(allowed)):
        lines.append(f"    N{idx} -->|depends| N{idx + 1}")
    lines.extend(
        [
            "```",
            "",
            "- **Topological Mastery Order:** " + " $\\to$ ".join(f"`{Path(s).stem}`" for s in allowed),
            "",
            "## 3. Subtopic Manifest & Status Matrix",
            "",
            "| Order | Note | Layer | Prerequisites (`depends_on`) | Next | Status |",
            "|---|---|---|---|---|---|",
        ]
    )
    for idx, sub in enumerate(allowed, start=1):
        stem = Path(sub).stem
        prev_cell = f"[[{Path(allowed[idx - 2]).stem}]]" if idx > 1 else "—"
        next_cell = f"[[{Path(allowed[idx]).stem}]]" if idx < len(allowed) else "—"
        lines.append(f"| {idx:02d} | [[{stem}]] | L1 | {prev_cell} | {next_cell} | planned |")
    lines.append("")
    return "\n".join(lines)


def render_routed_note(args: argparse.Namespace, note_id: str) -> str:
    topic = args.topic
    route = "deepstudy-master" if args.template in DEEP_ROUTES else args.template
    tags = [t.strip().lstrip("#") for t in args.tags if t.strip()]
    if not tags:
        route_tag = "cheatsheet" if route == "cheat-sheet" else route
        tags = [_slugify(args.base_domain), _slugify(args.master_topic), _slugify(topic), route_tag]
    nexttopics = [_format_wikilink(args.next_topic)] if args.next_topic else []
    metadata = {
        "id": note_id,
        "aliases": list(dict.fromkeys([args.title, *filter(None, map(str.strip, args.aliases))])),
        "topic": topic,
        "tags": list(dict.fromkeys(tags)),
        "nexttopics": nexttopics,
    }
    frontmatter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False)
    body = body_skeleton(route, args.math_level, args.number, args.title, narrow=args.narrow_practice)
    if route in ADAPTIVE_ROUTES:
        contract = getattr(args, "contract_data", None) or resolve_decisions(
            args.title,
            {"title": args.title, "template": route, "math_level": args.math_level,
             "language": getattr(args, "language", None) or "none"},
            topic,
        )
        body += (
            f"\n<!-- decision-contract: subject={contract['subject_family']}; domain={contract.get('domain', 'general')}; "
            f"math_level={contract['math_level']}; "
            f"code_depth={contract['code_depth']}; visual={contract['visual_modality']}; "
            f"max_qa={contract['max_qa_items']}; omit={','.join(contract['omitted_sections']) or 'none'} -->\n"
        )
    extra_lines: list[str] = []
    if args.depends_on:
        extra_lines.append("- **Prerequisites:** " + ", ".join(_format_wikilink(n) for n in args.depends_on))
    if args.compared_notes:
        extra_lines.append("- **Compared Notes:** " + ", ".join(_format_wikilink(n) for n in args.compared_notes))
    if extra_lines:
        h1, rest = body.split("\n", 1)
        body = f"{h1}\n\n" + "\n".join(extra_lines) + "\n" + rest
    return f"---\n{frontmatter}---\n\n{body}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scaffold an adaptive deep note, another routed note, or syllabus MOC.")
    parser.add_argument("vault_path", nargs="?", help="Path to Obsidian vault.")
    parser.add_argument("--output", help="Vault-relative output path (prints to stdout if omitted).")
    parser.add_argument("--syllabus", action="store_true", help="Scaffold a 00-MOC-<topic>.md syllabus boundary note.")
    parser.add_argument("--template", choices=ROUTES, help="Built-in route; defaults to adaptive deep study.")
    parser.add_argument("--math-level", type=int, choices=(0, 1, 2, 3), default=0)
    parser.add_argument("--language", help="Verification language, required for routed DSA notes.")
    parser.add_argument("--area", help="Area (defaults to base domain).")
    parser.add_argument("--created", type=date.fromisoformat, default=date.today())
    parser.add_argument("--compared-notes", nargs="*", default=[])
    parser.add_argument("--narrow-practice", action="store_true", help="Use the shorter practice tier ranges.")
    parser.add_argument("--allowed-subtopics", nargs="*", default=[], help="Allowlisted subtopic filenames for --syllabus.")
    parser.add_argument("--excluded-topics", nargs="*", default=[], help="Out-of-scope adjacent topics for --syllabus.")
    parser.add_argument("--id", dest="note_id", help="Note YAML id (defaults to <topic-slug>-<number>).")
    parser.add_argument("--number", default="01", help="Subtopic number prefix (default: 01).")
    parser.add_argument("--title", help="Subtopic title (optional when --syllabus is set).")
    parser.add_argument("--base-domain", default="General", help="Base domain.")
    parser.add_argument("--master-topic", default="General", help="Master topic.")
    parser.add_argument("--topic", required=True, help="Parent topic.")
    parser.add_argument("--aliases", nargs="*", default=[], help="Additional aliases.")
    parser.add_argument("--tags", nargs="*", default=[], help="Tags to include.")
    parser.add_argument("--depends-on", nargs="*", default=[], help="Prerequisite wikilinks.")
    parser.add_argument("--next-topic", help="Next topic wikilink.")
    parser.add_argument("--overwrite", action="store_true", help="Allow overwriting an existing file.")
    parser.add_argument("--dry-run", action="store_true", help="Print rendered skeleton without writing.")
    parser.add_argument("--contract", type=Path, help="Optional JSON Decision Contract from decision_matrix.py.")
    args = parser.parse_args(argv)
    args.contract_data = json.loads(args.contract.read_text(encoding="utf-8")) if args.contract else None

    if args.template and (args.syllabus or args.overwrite):
        parser.error("--template cannot be used with --syllabus or --overwrite")
    if args.math_level == 3 and args.template and args.template not in DEEP_ROUTES:
        parser.error("--math-level 3 is supported only for adaptive deep-study routes")
    if args.template == "dsa" and args.language in (None, "none"):
        parser.error("--language is required for --template dsa")

    if args.syllabus:
        note_id = args.note_id or f"moc-{_slugify(args.topic)}"
        content = render_syllabus_skeleton(
            note_id=note_id,
            topic=args.topic,
            base_domain=args.base_domain,
            master_topic=args.master_topic,
            allowed_subtopics=args.allowed_subtopics,
            excluded_topics=args.excluded_topics,
            tags=args.tags,
        )
    elif args.template:
        if not args.title or "\n" in args.title or "\r" in args.title:
            parser.error("--title must be nonempty and single-line for routed notes")
        note_id = args.note_id or f"{_slugify(args.topic)}-{args.number}"
        content = render_routed_note(args, note_id)
    else:
        if not args.title:
            print("ERROR: --title is required unless --syllabus is set.", file=sys.stderr)
            return 2
        note_id = args.note_id or f"{_slugify(args.topic)}-{args.number}"
        args.template = "deepstudy-master"
        content = render_routed_note(args, note_id)

    if args.dry_run or not args.output:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(content, end="")
        return 0

    try:
        vault_root = resolve_vault_root(args.vault_path)
        if ".." in Path(args.output).parts:
            raise ValueError(f"Path traversal ('..') is not allowed: {args.output}")
        out_path = Path(args.output)
        if not out_path.is_absolute():
            out_path = vault_root / out_path
        if not is_within_vault(vault_root, out_path):
            raise ValueError(f"Output path escapes vault root: {args.output}")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w" if args.overwrite else "x", encoding="utf-8") as output:
            output.write(content)
        print(f"Scaffolded {out_path.relative_to(vault_root).as_posix()}")
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
