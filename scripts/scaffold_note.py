#!/usr/bin/env python3
"""Scaffold adaptive deep-study notes, M1-M7 routed notes, and syllabus maps with Obsidian Properties."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
for _p in (str(REPO_ROOT), str(SCRIPT_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from scriptorium.engines.vault import build_obsidian_properties, render_note_with_properties
from scriptorium.layout import DEEP_ROUTES, ROUTES, body_skeleton, canonical_note_type
from scriptorium.models import format_wikilink as _format_wikilink, slugify as _slugify
from vault_index import is_within_vault, resolve_vault_root


def render_syllabus_skeleton(
    *,
    note_id: str,
    topic: str,
    base_domain: str,
    master_topic: str,
    allowed_subtopics: list[str] | None = None,
    excluded_topics: list[str] | None = None,
    tags: list[str] | None = None,
    created: date | str | None = None,
) -> str:
    """Render a deterministic 00-MOC-<topic-slug>.md Syllabus & Learning Graph with Obsidian Properties."""
    allowed = [s.strip() for s in (allowed_subtopics or []) if s.strip()] or ["01-intro.md"]
    excluded = [s.strip() for s in (excluded_topics or []) if s.strip()] or [
        "<Adjacent Topic> (separate topic — link only)"
    ]
    user_tags = [t.strip().lstrip("#") for t in (tags or []) if t.strip()]
    if "moc" not in user_tags:
        user_tags.append("moc")

    props = build_obsidian_properties(
        topic=topic,
        note_type="synthesis-revision",
        domain=base_domain,
        master_topic=master_topic,
        user_tags=user_tags,
        note_id=note_id,
        aliases=[
            f"{topic} — Syllabus & Learning Graph",
            f"{topic} Syllabus",
            f"{topic} MOC",
        ],
        nexttopics=[],
        created=created,
    )

    body_lines: list[str] = [
        f"# {topic} — Syllabus & Learning Graph",
        "",
        "## 1. Scope Boundary Contract",
        f"- **Core Learning Objective:** <!-- Define the exact start-to-end boundary of {topic}. -->",
        "- **In-Scope Subtopics (Strict Allowlist):**",
    ]
    for idx, sub in enumerate(allowed, start=1):
        body_lines.append(f"  {idx}. `{sub}` — <!-- 1-line scope -->")
    body_lines.append("- **Explicitly Out-of-Scope (Do-Not-Create Fence):**")
    for exc in excluded:
        body_lines.append(f"  - **{exc}**")

    body_lines.extend(
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
        body_lines.append(f'    N{idx}["{stem}"]')
    for idx in range(1, len(allowed)):
        body_lines.append(f"    N{idx} -->|depends| N{idx + 1}")
    body_lines.extend(
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
        body_lines.append(f"| {idx:02d} | [[{stem}]] | L1 | {prev_cell} | {next_cell} | planned |")
    body_lines.append("")
    return render_note_with_properties(props, "\n".join(body_lines))


def render_routed_note(args: argparse.Namespace, note_id: str) -> str:
    topic = args.topic
    route = "deepstudy-master" if args.template in DEEP_ROUTES else args.template
    user_tags = [t.strip().lstrip("#") for t in args.tags if t.strip()]
    nexttopics = [_format_wikilink(args.next_topic)] if args.next_topic else []
    aliases = list(dict.fromkeys([args.title, *filter(None, map(str.strip, args.aliases))]))
    base_domain = getattr(args, "base_domain", None)
    master_topic = getattr(args, "master_topic", None)

    props = build_obsidian_properties(
        topic=topic,
        note_type=canonical_note_type(route),
        domain=base_domain,
        master_topic=master_topic,
        content=f"{topic} {args.title}",
        user_tags=user_tags,
        note_id=note_id,
        aliases=aliases,
        nexttopics=nexttopics,
        created=getattr(args, "created", None),
    )
    body = body_skeleton(route, args.math_level, args.number, args.title, narrow=args.narrow_practice)
    extra_lines: list[str] = []
    if args.depends_on:
        extra_lines.append("- **Prerequisites:** " + ", ".join(_format_wikilink(n) for n in args.depends_on))
    if args.compared_notes:
        extra_lines.append("- **Compared Notes:** " + ", ".join(_format_wikilink(n) for n in args.compared_notes))
    if extra_lines:
        h1, rest = body.split("\n", 1)
        body = f"{h1}\n\n" + "\n".join(extra_lines) + "\n" + rest
    return render_note_with_properties(props, body)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scaffold an adaptive deep note, another routed note, or syllabus MOC.")
    parser.add_argument("vault_path", nargs="?", help="Path to Obsidian vault.")
    parser.add_argument("--output", help="Vault-relative output path (prints to stdout if omitted).")
    parser.add_argument("--syllabus", action="store_true", help="Scaffold a 00-MOC-<topic>.md syllabus boundary note.")
    parser.add_argument("--template", choices=ROUTES, help="Built-in route; defaults to adaptive deep study.")
    parser.add_argument("--math-level", type=int, choices=(0, 1, 2, 3), default=0)
    parser.add_argument("--language", help="Verification language, required for routed DSA notes.")
    parser.add_argument("--created", type=date.fromisoformat, default=None, help="Optional ISO creation date property.")
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
    args = parser.parse_args(argv)

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
            created=args.created,
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
