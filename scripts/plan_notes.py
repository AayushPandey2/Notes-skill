#!/usr/bin/env python3
"""Resolve request locks, save an outlined plan, and publish validated notes."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

import yaml

from note_layout import ROUTES
from scaffold_note import _slugify
from vault_index import is_within_vault, resolve_vault_root

COMMANDS = {f"scribe-{name}" for name in (
    "dsa", "practice", "notes", "expand", "doubt", "distill", "ingest", "compare", "quiz", "atomic-notes", "classnotes"
)}
LOCKS = {
    "scribe-dsa": "dsa", "scribe-practice": "practice",
    "scribe-distill": "cheat-sheet", "scribe-compare": "comparison",
    "scribe-atomic-notes": "atomic",
}
FORBIDDEN_CLASSNOTES_TEMPLATES = {"deepstudy-coding", "deepstudy-general"}
LANGUAGES = {
    "cpp": "cpp", "c++": "cpp", "c++20": "cpp", "python": "python", "py": "python",
    "python3": "python", "rust": "rust", "java": "java", "c": "c", "go": "go",
    "javascript": "javascript", "js": "javascript", "typescript": "typescript", "ts": "typescript",
    "sql": "sql", "c#": "csharp", "csharp": "csharp", "kotlin": "kotlin",
}
RUNTIMES = {"cpp": "C++20", "python": "Python 3", "c": "C17", "typescript": "TypeScript / Node.js"}
DOMAIN_STACKS = {
    "ml": ("python", ["Python + NumPy", "Python + PyTorch"]),
    "classical-ml": ("python", ["Python + NumPy", "Python + scikit-learn"]),
    "dsa": ("cpp", ["C++20", "Python 3"]),
    "systems": ("c", ["C17", "Python 3"]),
    "database": ("sql", ["SQL (PostgreSQL / DuckDB)", "Python (pandas / polars)"]),
    "web": ("typescript", ["TypeScript / Node.js", "Python 3"]),
    "math": ("python", ["Python + SymPy"]),
}
PROFILES = {
    "deepstudy-coding": "docs-and-papers", "deepstudy-general": "papers-and-textbooks",
    "api-table": "official-docs", "summary": "source-only", "dsa": "problem-and-docs",
    "paper-breakdown": "primary-paper", "practice": "vault-notes", "atomic": "papers-and-textbooks",
    "cheat-sheet": "vault-notes", "comparison": "docs-and-papers", "classnotes": "fast-web-fetch",
}
URL = re.compile(r"https?://[^\s<>\"]+", re.I)
PAPER_PATHS = {
    "arxiv.org": ("/abs/", "/pdf/", "/html/"),
    "doi.org": ("/10.",),
    "openreview.net": ("/forum", "/pdf"),
    "aclanthology.org": ("/",),
    "papers.nips.cc": ("/paper",),
    "proceedings.neurips.cc": ("/paper",),
    "openaccess.thecvf.com": ("/content",),
    "ieeexplore.ieee.org": ("/document/", "/abstract/document/", "/stamp/"),
    "dl.acm.org": ("/doi/",),
}


def inspect_request(request: str) -> dict:
    raw = request.strip()
    if not raw:
        raise ValueError("Provide a request.")
    first, *rest = raw.split(maxsplit=1)
    command = first.lower().lstrip("/")
    command = command if command in COMMANDS else None
    payload = rest[0] if command and rest else "" if command else raw
    language = None
    if command == "scribe-dsa":
        parts = payload.split(maxsplit=1)
        language = LANGUAGES.get(parts[0].lower()) if parts else None
        if len(parts) < 2 or not language:
            raise ValueError("Usage: /scribe-dsa cpp Two Sum or /scribe-dsa python <problem or URL>")
        payload = parts[1]
    elif command and not payload:
        arg_hint = "topic-or-note" if command == "scribe-practice" else "topic name" if command == "scribe-atomic-notes" else "topic"
        raise ValueError(f"Usage: /{command} <{arg_hint}>")

    sources = [match.group().rstrip(".,;") for match in URL.finditer(payload)]
    route_names = "|".join(ROUTES)
    quote = "[" + chr(96) + "\"']?"
    explicit = re.search(
        rf"\btemplate\s*[:=]\s*{quote}({route_names}){quote}(?![\w-])"
        rf"|\buse (?:the )?{quote}({route_names}){quote}\s+template\b", payload, re.I,
    )
    intent = next((route for pattern, route in (
        (r"^\s*(?:please\s+)?summari[sz]e\b", "summary"),
        (r"^\s*(?:please\s+)?compare\b.+\b(?:vs\.?|versus|and|with)\s", "comparison"),
        (r"\b(?:make|create|write|give me|generate)\b.*\bcheat[\s-]?sheet\b", "cheat-sheet"),
        (r"\b(?:make|create|write|give me|generate)\b.*\batomic note\b", "atomic"),
        (r"\b(?:make|create|write|give me|generate)\b.*\bpractice (?:set|test)\b", "practice"),
        (r"\b(?:make|create|write|give me|generate)\b.*\bpaper breakdown\b", "paper-breakdown"),
        (r"\b(?:make|create|write|give me|generate)\b.*\bclass\s?notes\b", "classnotes"),
        (r"^\s*(?:please\s+)?solve\b.*\bin\s+(?:c\+\+(?:20)?|cpp|python(?:3)?|rust|java|go)(?=\W|$)", "dsa"),
    ) if re.search(pattern, payload, re.I)), None)
    override = (explicit[1] or explicit[2]).lower() if explicit else intent
    if not language and override == "dsa":
        requested = re.search(r"\bin\s+(c\+\+(?:20)?|cpp|python(?:3)?|rust|java|go)(?=\W|$)", payload, re.I)
        if requested:
            language = LANGUAGES[requested[1].lower()]
    standalone = URL.fullmatch(payload.strip("<>"))
    source_lock = None
    if standalone and command in {None, "scribe-notes"}:
        source = urlsplit(sources[0])
        host = (source.hostname or "").removeprefix("www.")
        prefixes = PAPER_PATHS.get(host, ())
        is_paper = source.path != "/" and source.path.startswith(prefixes)
        source_lock = "paper-breakdown" if is_paper else "summary"
    locked = LOCKS.get(command)
    return {
        "command": command, "payload": payload, "template": locked or override or source_lock,
        "lock": "command" if locked else "explicit" if override else "source" if source_lock else None,
        "language": language, "sources": sources,
        "mode": "existing-notes" if command in {"scribe-doubt", "scribe-quiz"} else "author",
    }


def select_route(purpose: str, impl_weight: str, density: str) -> str:
    if purpose not in {"compare", "reference", "revise", "definition", "implement", "explain"}:
        raise ValueError(f"Invalid purpose: {purpose}")
    if impl_weight not in {"high", "low"} or density not in {"callables", "micro", "cohesive"}:
        raise ValueError("Use impl_weight high/low and density callables/micro/cohesive.")
    if purpose == "compare":
        return "comparison"
    if purpose == "reference" or density == "callables":
        return "api-table"
    if purpose == "revise":
        return "cheat-sheet"
    if purpose == "definition" or density == "micro":
        return "atomic"
    if purpose == "implement" or impl_weight == "high":
        return "deepstudy-coding"
    return "deepstudy-general"


def _name(title: str) -> str:
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", title).strip(" .") or "Note"


def _relative(value: str, *, folder: bool = False) -> str:
    if folder and value == ".":
        return value
    value = value.replace("\\", "/")
    parts = value.split("/")
    for part in parts:
        if (not part or part in {".", ".."} or part.endswith((" ", "."))
                or re.search(r'[<>:"|?*\x00-\x1f]', part)
                or re.fullmatch(r"(?:CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])(?:\..*)?", part, re.I)):
            raise ValueError(f"Invalid vault-relative path: {value!r}")
    if parts[0].casefold() in {".scriptorium", ".obsidian", ".git", ".trash"}:
        raise ValueError(f"Reserved vault-relative path: {value!r}")
    if not folder and PurePosixPath(value).suffix.lower() != ".md":
        raise ValueError(f"Note output must be Markdown: {value!r}")
    return value


def _under_vault(vault: Path, relative: str) -> Path:
    target = vault / relative
    if not is_within_vault(vault, target):
        raise ValueError(f"Path escapes the vault: {relative}")
    for parent in target.parents:
        if parent == vault:
            break
        if parent.exists() and not parent.is_dir():
            raise ValueError(f"Output parent is not a folder: {parent}")
    return target


def _text(item: dict, key: str, default: str = "") -> str:
    value = item.get(key, default)
    if not isinstance(value, str) or not value.strip() or len(value.splitlines()) != 1:
        raise ValueError(f"{key} must be nonempty single-line text.")
    return value.strip()


def _stack(item: dict, route: str, override: str | None) -> tuple[str, list[str]]:
    values = item.get("verification_stack")
    if values is not None and (not isinstance(values, list) or len(values) > 3
                               or any(not isinstance(v, str) or not v.strip() for v in values)):
        raise ValueError("verification_stack must contain up to three nonempty strings.")
    language = override or item.get("language")
    if language is not None:
        if not isinstance(language, str):
            raise ValueError("language must be text.")
        language = LANGUAGES.get(language.lower(), language.lower())
        if override and language != LANGUAGES.get(str(item.get("language", "")).lower(), item.get("language")):
            values = None
        return language, list(dict.fromkeys(values if values is not None else (
            [] if language == "none" else [RUNTIMES.get(language, language.title())]
        )))
    if values:
        raise ValueError("Specify language alongside a nonempty verification_stack.")
    domain = item.get("domain", "dsa" if route == "dsa" else "")
    if route in {"deepstudy-coding", "api-table", "dsa"} and values is None:
        return DOMAIN_STACKS.get(domain, ("python", ["Python 3"]))
    return "none", []


def build_plan(
    vault: Path, request: str, topic_folder: str, outline: list, *,
    template: str | None = None, language: str | None = None, topic_name: str | None = None,
    legacy_names: bool = False,
) -> dict:
    intent = inspect_request(request)
    if intent["mode"] != "author":
        raise ValueError(f"{intent['command']} uses existing notes and does not create a plan.")
    lock = intent["template"] if intent["lock"] == "command" else template or intent["template"]
    if intent["command"] == "scribe-classnotes" and (
        template in FORBIDDEN_CLASSNOTES_TEMPLATES or lock in FORBIDDEN_CLASSNOTES_TEMPLATES
    ):
        raise ValueError("/scribe-classnotes prohibits deepstudy-coding and deepstudy-general templates.")
    language = intent["language"] or language
    topic_folder = _relative(topic_folder, folder=True)
    directory = _under_vault(vault, topic_folder)
    if directory.exists() and not directory.is_dir():
        raise ValueError(f"Topic folder is occupied by a file: {topic_folder}")
    if not isinstance(outline, list) or not outline:
        raise ValueError("Outline must be a nonempty array of subtopics.")
    if lock in {"dsa", "practice", "summary", "paper-breakdown"} and len(outline) != 1:
        raise ValueError(f"This {lock} request expects exactly one output.")
    if lock == "practice" and (topic_folder == "." or not directory.is_dir()):
        raise ValueError("Manual practice requires an existing topic folder.")

    topic = _text({"topic": topic_name}, "topic") if topic_name else directory.name
    plan = []
    for number, item in enumerate(outline, 1):
        if not isinstance(item, dict):
            raise ValueError("Each outline entry must be an object.")
        title = _text(item, "title")
        item_id = _text(item, "id", f"{number:02d}")
        if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", item_id) or item_id == "practice":
            raise ValueError(f"Invalid or reserved item ID: {item_id}")
        if intent["command"] == "scribe-classnotes":
            explicit_item_tpl = item.get("template")
            if explicit_item_tpl in FORBIDDEN_CLASSNOTES_TEMPLATES:
                raise ValueError("/scribe-classnotes prohibits deepstudy-coding and deepstudy-general templates.")
            route = lock or explicit_item_tpl or select_route(item.get("purpose"), item.get("impl_weight"), item.get("density"))
            if route in FORBIDDEN_CLASSNOTES_TEMPLATES:
                route = "classnotes"
            level = item.get("math_level", 0)
        else:
            route = lock or item.get("template") or select_route(item.get("purpose"), item.get("impl_weight"), item.get("density"))
            level = item.get("math_level")
        if route not in ROUTES or type(level) is not int or level not in (0, 1, 2):
            raise ValueError(f"Invalid template or math_level for {title}")
        lang, stack = _stack(item, route, language)
        if route == "dsa" and lang not in LANGUAGES.values():
            raise ValueError("DSA requires a supported verification language.")
        filename = f"{item_id}-{_slugify(title)}.md" if legacy_names else f"{item_id} - {_name(title)}.md"
        if route == "atomic":
            raw_atomic = _text(item, "output_path", f"Atomic Notes/{_name(title)}.md")
            filename = raw_atomic if raw_atomic.startswith("Atomic Notes/") else f"Atomic Notes/{raw_atomic}"
        if route == "practice":
            subject = re.sub(r" - Practice(?: Test)?$", "", title)
            label = subject if topic_folder == "." or topic.casefold() in subject.casefold() else f"{topic} - {subject}"
            filename = f"Practice Sets/{_name(label)} - Practice.md"
        id_topic = title if topic_folder == "." and not topic_name else topic
        default_id = f"{_slugify(id_topic)}-{item_id}"
        if route == "practice":
            default_id = f"practice-{_slugify(topic)}-{_slugify(subject)}"
        if route == "cheat-sheet":
            subject = re.sub(r"[\s_-]*cheat[\s-]?sheet$", "", title, flags=re.I).strip() or title
            t_slug = _slugify(id_topic)
            s_slug = _slugify(subject)
            if t_slug == s_slug or t_slug in s_slug:
                cs_name = f"{s_slug}-CHEAT-SHEET.md"
                default_id = f"cheatsheet-{s_slug}"
            else:
                cs_name = f"{t_slug}-{s_slug}-CHEAT-SHEET.md"
                default_id = f"cheatsheet-{t_slug}-{s_slug}"
            if intent["command"] == "scribe-distill" or "output_path" not in item:
                filename = f"Cheatsheets/{cs_name}"
            else:
                raw_cs = _text(item, "output_path")
                filename = raw_cs if raw_cs.startswith("Cheatsheets/") else f"Cheatsheets/{raw_cs}"
        if intent["command"] == "scribe-compare":
            pair_parts = re.split(r"\s+(?:vs\.?|versus)\s+", intent["payload"], maxsplit=1, flags=re.I)
            if len(pair_parts) != 2 or topic_folder != ".":
                raise ValueError("Use /scribe-compare <A> vs <B> and topic folder '.'")
            pair = "-vs-".join(map(_slugify, pair_parts))
            filename = f"comparison/{pair}.md"
            default_id = f"compare-{pair}"
        default_profile = "vault-notes" if intent["command"] in {"scribe-compare", "scribe-distill"} else PROFILES[route]
        entry = {
            "id": item_id, "note_id": _text(item, "note_id", default_id), "title": title,
            "template": route, "math_level": level, "language": lang, "verification_stack": stack,
            "source_profile": _text(item, "source_profile", default_profile),
            "routing_reason": _text(item, "routing_reason"),
            "output_path": _relative(filename if route in {"practice", "atomic", "cheat-sheet"} else _text(item, "output_path", filename)),
        }
        if "depends_on" in item:
            deps = item["depends_on"]
            if not isinstance(deps, list) or any(dep not in [other["id"] for other in plan] for dep in deps):
                raise ValueError(f"{item_id}: dependencies must reference earlier plan items.")
            entry["depends_on"] = deps
        if "next_topic" in item:
            entry["next_topic"] = _text(item, "next_topic")
        plan.append(entry)
    for index, item in enumerate(plan):
        if "next_topic" in item and item["next_topic"] not in [other["id"] for other in plan[index + 1:]]:
            raise ValueError(f"{item['id']}: next_topic must reference a later plan item.")

    automatic = (
        not directory.exists()
        and topic_folder not in {".", "Atomic Notes", "Practice Sets", "Cheatsheets"}
        and intent["command"] not in {"scribe-atomic-notes", "scribe-distill"}
        and not all(item["template"] in {"practice", "atomic", "cheat-sheet"} for item in plan)
        and all(item["template"] != "practice" for item in plan)
    )
    if automatic:
        with_stack = [item for item in plan if item["verification_stack"]]
        stacks = list(dict.fromkeys(stack for item in with_stack for stack in item["verification_stack"]))
        plan.append({
            "id": "practice", "note_id": f"{_slugify(topic)}-practice",
            "title": f"{topic} - Practice Test", "template": "practice",
            "math_level": max(item["math_level"] for item in plan),
            "language": with_stack[0]["language"] if with_stack else "none", "verification_stack": stacks[:3],
            "source_profile": "planned-notes", "routing_reason": "Topic-wide recall and synthesis across the planned notes.",
            "output_path": _relative(f"Practice Sets/{_name(topic)} - Practice Test.md"),
            "depends_on": [item["id"] for item in plan],
        })
    for key in ("id", "note_id", "output_path"):
        if len({item[key].casefold() for item in plan}) != len(plan):
            raise ValueError(f"Duplicate planned {key} values.")
    paths = [PurePosixPath(_item_vault_rel(topic_folder, item).casefold()) for item in plan]
    if any(parent in paths for path in paths for parent in path.parents):
        raise ValueError("A planned note path is also a parent folder of another note.")
    return {"topic_folder": topic_folder, "plan": plan}


def _item_vault_rel(folder: str, item: dict) -> str:
    folder = _relative(folder, folder=True)
    out = _relative(item["output_path"])
    if item.get("template") in {"practice", "atomic", "cheat-sheet"} or out.startswith(("Practice Sets/", "Atomic Notes/", "Cheatsheets/")):
        parent = PurePosixPath(folder).parent.as_posix() if folder != "." else "."
        return out if parent == "." else f"{parent}/{out}"
    return out if folder == "." else f"{folder}/{out}"


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_once(path: Path, data: bytes) -> None:
    """Publish all bytes at once, using a same-directory exclusive hard link."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".scriptorium-", delete=False) as temp:
        staged = Path(temp.name)
        try:
            temp.write(data)
            temp.flush()
            os.fsync(temp.fileno())
            temp.close()
            os.link(staged, path)
        finally:
            temp.close()
            staged.unlink(missing_ok=True)


def _plan_dir(vault: Path, plan_id: str) -> Path:
    if not re.fullmatch(r"[0-9a-f]{32}", plan_id):
        raise ValueError("Invalid plan ID.")
    return _under_vault(vault, f".scriptorium/plans/{plan_id}")


def _read_plan(vault: Path, plan_id: str) -> dict:
    journal = _plan_dir(vault, plan_id)
    file = _under_vault(vault, (journal / "plan.json").relative_to(vault).as_posix())
    return json.loads(file.read_text(encoding="utf-8"))


def _targets(vault: Path, saved: dict) -> dict[str, Path]:
    folder = _relative(saved["topic_folder"], folder=True)
    paths = {
        item["id"]: _under_vault(vault, _item_vault_rel(folder, item))
        for item in saved["plan"]
    }
    resolved = [target.resolve().as_posix().casefold() for target in paths.values()]
    if len(set(resolved)) != len(resolved):
        raise ValueError("Multiple plan items resolve to the same destination.")
    return paths


def _status(vault: Path, plan_id: str, saved: dict) -> dict[str, str]:
    journal = _plan_dir(vault, plan_id)
    states = {}
    for item_id, target in _targets(vault, saved).items():
        intent = _under_vault(vault, (journal / f"{item_id}.intent").relative_to(vault).as_posix())
        receipt = _under_vault(vault, (journal / f"{item_id}.done").relative_to(vault).as_posix())
        if target.is_symlink() or (target.exists() and not target.is_file()):
            states[item_id] = "conflict"
        elif not target.exists():
            states[item_id] = "conflict" if receipt.exists() else "pending"
        elif receipt.is_file() or (intent.is_file() and intent.read_text() == _hash(target.read_bytes())):
            states[item_id] = "complete"
        else:
            states[item_id] = "conflict"
    return states


def _require_no_conflicts(states: dict[str, str]) -> None:
    conflicts = [item_id for item_id, state in states.items() if state == "conflict"]
    if conflicts:
        raise ValueError(f"Conflicting output(s), preserved: {', '.join(conflicts)}")


def start_plan(vault: Path, request: str, folder: str, outline: list, **options) -> tuple[str, dict]:
    folder = _relative(folder, folder=True)
    plan_id = _hash(json.dumps([request.strip(), folder.casefold()], ensure_ascii=False).encode())[:32]
    journal = _plan_dir(vault, plan_id)
    plan_file = _under_vault(vault, (journal / "plan.json").relative_to(vault).as_posix())
    if not plan_file.exists():
        saved = build_plan(vault, request, folder, outline, **options)
        _require_no_conflicts(_status(vault, plan_id, saved))
        try:
            _write_once(plan_file, json.dumps(saved, indent=2, ensure_ascii=False).encode("utf-8"))
        except FileExistsError:
            pass  # A concurrent retry saved the canonical plan.
    saved = _read_plan(vault, plan_id)
    _require_no_conflicts(_status(vault, plan_id, saved))
    return plan_id, saved


def publish(vault: Path, plan_id: str, item_id: str, draft: Path) -> str:
    from validate_note import read_frontmatter, validate_text

    saved = _read_plan(vault, plan_id)
    targets = _targets(vault, saved)
    if item_id not in targets:
        raise ValueError(f"Unknown plan item: {item_id}")
    states = _status(vault, plan_id, saved)
    _require_no_conflicts(states)
    if states[item_id] == "complete":
        return "already complete"
    item = next(item for item in saved["plan"] if item["id"] == item_id)
    if any(states[dep] != "complete" for dep in item.get("depends_on", ())):
        raise ValueError("Publish the planned prerequisites before this note.")
    data = draft.read_bytes()
    content = data.decode("utf-8-sig")
    target = targets[item_id]
    findings = validate_text(content, vault=vault, target=target, planned=targets.values())
    if findings:
        raise ValueError("\n".join(f"{line}: {message}" for line, message in findings))
    metadata, _, _ = read_frontmatter(content)
    expected = {"id": item["note_id"], "title": item["title"], "template": item["template"],
                "math_level": item["math_level"]}
    if item["language"] != "none" or "language" in metadata:
        expected["language"] = item["language"]
    if any(metadata.get(key) != val for key, val in expected.items()):
        raise ValueError(f"Draft metadata does not match planned identity: {expected}")

    journal = _plan_dir(vault, plan_id)
    intent = _under_vault(vault, (journal / f"{item_id}.intent").relative_to(vault).as_posix())
    receipt = _under_vault(vault, (journal / f"{item_id}.done").relative_to(vault).as_posix())
    digest = _hash(data).encode()
    try:
        _write_once(intent, digest)
    except FileExistsError:
        if intent.read_bytes() != digest:
            raise ValueError("Publish already started with different draft bytes. Retry the original draft.")
    try:
        _write_once(target, data)
    except FileExistsError:
        if target.is_symlink() or not target.is_file() or _hash(target.read_bytes()).encode() != digest:
            raise ValueError(f"Conflicting output, preserved: {target.relative_to(vault)}")
    try:
        _write_once(receipt, digest)
    except FileExistsError:
        pass
    return f"published {target.relative_to(vault).as_posix()}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("inspect").add_argument("request")
    start = commands.add_parser("start")
    start.add_argument("vault")
    start.add_argument("--request", required=True)
    start.add_argument("--topic-folder", required=True)
    start.add_argument("--outline", type=Path, help="Outline JSON, required when starting a new plan.")
    start.add_argument("--topic", help="Display name when the topic folder uses a slug.")
    start.add_argument("--template", choices=ROUTES)
    start.add_argument("--language")
    start.add_argument("--legacy-names", action="store_true")
    for action in ("status", "publish"):
        sub = commands.add_parser(action)
        sub.add_argument("vault")
        sub.add_argument("plan_id")
        if action == "publish":
            sub.add_argument("item_id")
            sub.add_argument("draft", type=Path)
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        if args.action == "inspect":
            result = inspect_request(args.request)
        else:
            vault = resolve_vault_root(args.vault)
            if args.action == "publish":
                print(publish(vault, args.plan_id, args.item_id, args.draft))
                return 0
            if args.action == "start":
                outline = json.loads(args.outline.read_text(encoding="utf-8-sig")) if args.outline else []
                plan_id, saved = start_plan(
                    vault, args.request, args.topic_folder, outline, template=args.template,
                    language=args.language, topic_name=args.topic, legacy_names=args.legacy_names,
                )
            else:
                plan_id = args.plan_id
                saved = _read_plan(vault, plan_id)
            result = {"plan_id": plan_id, **saved, "status": _status(vault, plan_id, saved)}
        print(yaml.safe_dump(result, sort_keys=False, allow_unicode=True), end="")
        return 0
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
