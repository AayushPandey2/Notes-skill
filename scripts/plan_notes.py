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

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
for _p in (str(REPO_ROOT), str(SCRIPT_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from scriptorium.layout import DEEP_ROUTES, ROUTES
from scriptorium.models import slugify as _slugify, normalize_stack
from vault_index import is_within_vault, resolve_notes_folder, resolve_vault_root, set_notes_folder
from scriptorium.engines._decision import requested_stack, resolve_decisions
from scriptorium.engines._verification import EXTENSIONS, check_evidence, check_python, required_examples, split_blocks, verify_runtimes

COMMANDS = {f"scribe-{name}" for name in (
    "dsa", "practice", "deepnotes", "expand", "doubt", "distill", "ingest", "compare", "quiz", "atomic-notes", "notes", "setfolder"
)}
LOCKS = {
    "scribe-dsa": "dsa", "scribe-practice": "practice",
    "scribe-distill": "cheat-sheet", "scribe-compare": "comparison",
    "scribe-atomic-notes": "atomic",
}
FORBIDDEN_STUDYNOTES_TEMPLATES = DEEP_ROUTES
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
    "deepstudy-master": "adaptive-research-engine",
    "deep-notes": "adaptive-research-engine",
    "api-table": "official-docs",
    "summary": "source-only",
    "dsa": "problem-and-docs",
    "implementation-guide": "problem-and-docs",
    "paper-breakdown": "primary-paper",
    "practice": "vault-notes",
    "assessment": "vault-notes",
    "atomic": "papers-and-textbooks",
    "cheat-sheet": "vault-notes",
    "quick-reference": "vault-notes",
    "comparison": "docs-and-papers",
    "studynotes": "fast-web-fetch",
    "study-notes": "fast-web-fetch",
    "worked-solutions": "adaptive-research-engine",
    "synthesis-revision": "vault-notes",
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


def inspect_request(request: str, *, stack: list[str] | None = None) -> dict:
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
    route_names = "|".join(sorted(ROUTES, key=len, reverse=True))
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
        (r"\b(?:make|create|write|give me|generate)\b.*\bstudy\s?notes\b", "studynotes"),
        (r"^\s*(?:please\s+)?solve\b.*\bin\s+(?:c\+\+(?:20)?|cpp|python(?:3)?|rust|java|go)(?=\W|$)", "dsa"),
    ) if re.search(pattern, payload, re.I)), None)
    override = (explicit[1] or explicit[2]).lower() if explicit else intent
    if not language and override == "dsa":
        requested = re.search(r"\bin\s+(c\+\+(?:20)?|cpp|python(?:3)?|rust|java|go)(?=\W|$)", payload, re.I)
        if requested:
            language = LANGUAGES[requested[1].lower()]
    standalone = URL.fullmatch(payload.strip("<>"))
    source_lock = None
    if standalone and command in {None, "scribe-deepnotes"}:
        source = urlsplit(sources[0])
        host = (source.hostname or "").removeprefix("www.")
        prefixes = PAPER_PATHS.get(host, ())
        is_paper = source.path != "/" and source.path.startswith(prefixes)
        source_lock = "paper-breakdown" if is_paper else "summary"
    locked = LOCKS.get(command)
    from scriptorium.engines.orchestration import route_request, route_to_master

    routed = route_request(raw, has_source=bool(sources), existing_command=command)
    if command == "scribe-notes":
        selected = override or source_lock or routed.get("compat_route") or "deepstudy-master"
    else:
        selected = locked or override or source_lock or {
            "scribe-deepnotes": "deepstudy-master",
        }.get(command)
    if selected in DEEP_ROUTES:
        selected = "deepstudy-master"
    implementation_stack = requested_stack(payload) if stack is None else normalize_stack(stack)
    if selected and routed.get("master") is None:
        m_id, v_id = route_to_master(selected)
        routed["master"] = m_id
        routed["variant"] = v_id
    return {
        "command": command, "payload": payload, "template": selected,
        "lock": "command" if locked else "explicit" if override else "source" if source_lock else None,
        "language": language, "sources": sources,
        "implementation_stack": implementation_stack,
        "mode": "setfolder" if command == "scribe-setfolder" else "existing-notes" if command in {"scribe-doubt", "scribe-quiz"} else "author",
        "master": routed.get("master"),
        "variant": routed.get("variant"),
        "multi_artifact": routed.get("multi_artifact", False),
        "shared_context": routed.get("shared_context", False),
        "source_policy": routed.get("source_policy", "adaptive"),
        "research_mode": routed.get("research_mode", "R-I"),
        "knowledge_types": routed.get("knowledge_types", []),
        "artifacts": routed.get("artifacts", []),
        "routing_trace": routed.get("routing_trace", {}),
        "retired_command": routed.get("retired_command"),
        "migration_hint": routed.get("migration_hint"),
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
    return "deepstudy-master"


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
    if values is not None and (not isinstance(values, list) or (route not in DEEP_ROUTES and len(values) > 3)
                               or any(not isinstance(v, str) or not v.strip() for v in values)):
        raise ValueError("verification_stack must contain nonempty strings (up to three for non-deep routes).")
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
    if route in {"api-table", "dsa"} and values is None:
        return DOMAIN_STACKS.get(domain, ("python", ["Python 3"]))
    return "none", []


def build_plan(
    vault: Path, request: str, topic_folder: str, outline: list, *,
    template: str | None = None, language: str | None = None, topic_name: str | None = None,
    legacy_names: bool = False, stack: list[str] | None = None, allow_math_override: bool = False,
) -> dict:
    intent = inspect_request(request, stack=stack)
    if intent["mode"] != "author":
        raise ValueError(f"{intent['command']} uses existing notes and does not create a plan.")
    lock = intent["template"] if intent["lock"] == "command" else template or (intent["template"] if intent["lock"] else None)
    language = intent["language"] or language
    topic_folder = _relative(topic_folder, folder=True)
    notes_root = resolve_notes_folder(vault)
    if notes_root and topic_folder != "." and not topic_folder.lower().startswith(f"{notes_root.lower()}/") and topic_folder.lower() != notes_root.lower():
        topic_folder = f"{notes_root}/{topic_folder}"
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
        if intent["command"] == "scribe-notes":
            # Universal /scribe-notes supports ALL seven masters (M1-M7) dynamically without prohibiting M1
            explicit_item_tpl = item.get("template")
            route = lock or explicit_item_tpl or intent["template"] or "deepstudy-master"
            level = item.get("math_level")
        elif intent["command"] == "scribe-deepnotes" or "instructional_plan" in item:
            # Modern adaptive deep-notes route: never call select_route() to switch subtopics
            # into api-table, atomic, cheat-sheet, or comparison based on purpose/density/impl_weight.
            route = lock or item.get("template") or "deepstudy-master"
            level = item.get("math_level")
        else:
            route = lock or item.get("template")
            if not route:
                if any(k in item for k in ("purpose", "impl_weight", "density")):
                    route = select_route(
                        item.get("purpose", "explain"),
                        item.get("impl_weight", "low"),
                        item.get("density", "cohesive"),
                    )
                else:
                    route = "deepstudy-master"
            level = item.get("math_level")
        if route in DEEP_ROUTES:
            route = "deepstudy-master"
        levels = (0, 1, 2, 3) if route in DEEP_ROUTES else (0, 1, 2)
        if route not in ROUTES or (level is not None and (type(level) is not int or level not in levels)):
            raise ValueError(f"Invalid template or math_level for {title}")
        lang, verification_stack = _stack(item, route, language)
        selected_stack = item.get("implementation_stack")
        if intent["implementation_stack"] is not None and (
            len(outline) == 1 or "instructional_plan" in item or item.get("purpose") == "implement"
            or item.get("impl_weight") == "high" or re.search(r"\bimplementations?\b", title, re.I)
        ):
            selected_stack = intent["implementation_stack"]
        tags = item.get("tags")
        if tags is not None and (not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags)):
            raise ValueError(f"{title}: tags must be a list of strings.")
        if route in DEEP_ROUTES and "instructional_plan" in item:
            from scriptorium.engines._instructional import resolve_instructional_contract

            decision_contract = resolve_instructional_contract(
                request,
                topic,
                item["instructional_plan"],
                item={**item, "template": route, "language": lang, "implementation_stack": selected_stack},
                vault=vault,
            )
        else:
            decision_contract = resolve_decisions(
                request,
                {**item, "template": route, "math_level": level, "language": lang, "implementation_stack": selected_stack},
                topic,
                tags=tags,
                allow_math_override=allow_math_override,
            )
        if decision_contract["subject_family"] == "non-computing" and route in DEEP_ROUTES and "instructional_plan" not in item:
            if lang != "none" or selected_stack or item.get("impl_weight") == "high":
                raise ValueError(f"Non-computing topic '{title}' prohibits code/implementation. Request a simulation explicitly.")
        level = decision_contract["math_level"]
        if decision_contract["verify_stack"]:
            planned_lang = decision_contract["language"]
            verify_names = decision_contract["implementation_stack"]
            if route == "dsa" and (len(verify_names) != 1 or planned_lang != intent["language"] and intent["language"]):
                raise ValueError("The DSA stack must match the command language.")
            lang = planned_lang
            if selected_stack is not None or not item.get("verification_stack"):
                verification_stack = verify_names
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
            "template": route, "domain": decision_contract["domain"], "math_level": level,
            **({"clamped_from": decision_contract["clamped_from"]} if "clamped_from" in decision_contract else {}),
            "language": lang, "verification_stack": verification_stack,
            "source_profile": _text(item, "source_profile", default_profile),
            "routing_reason": _text(item, "routing_reason"),
            "decision_contract": decision_contract,
            "output_path": _relative(filename if route in {"practice", "atomic", "cheat-sheet"} else _text(item, "output_path", filename)),
        }
        if "decision_record" in item:
            if not isinstance(item["decision_record"], dict):
                raise ValueError("decision_record must be an object of conclusions and concise reasons.")
            entry["decision_record"] = item["decision_record"]
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
            "domain": plan[0]["domain"],
            "math_level": min(2, max(item["math_level"] for item in plan)),
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


def _planned_examples(content: str, item: dict):
    from validate_note import read_frontmatter

    _, _, body_start = read_frontmatter(content)
    blocks, prose = split_blocks("\n".join(content.splitlines()[body_start:]))
    contract = item.get("decision_contract") or {}
    stack = contract.get("implementation_stack", []) if contract.get("verify_stack") else []
    examples, missing = required_examples(blocks, stack, minimum_lines=1 if contract.get("contract_version") in {2, 3} else 6)
    if findings := check_python(blocks) + missing:
        raise ValueError("\n".join(f"{body_start + line}: {message}" for line, message in findings))
    return examples, blocks, prose


def _check_export(path: Path, data: bytes) -> None:
    if path.is_symlink() or (path.exists() and (not path.is_file() or path.read_bytes() != data)):
        raise ValueError(f"Conflicting example output, preserved: {path}")


def publish(
    vault: Path,
    plan_id: str,
    item_id: str,
    draft: Path,
    *,
    export_code: bool = False,
    coverage: dict | None = None,
    evidence: dict | None = None,
) -> str:
    from validate_note import read_frontmatter, validate_text

    saved = _read_plan(vault, plan_id)
    targets = _targets(vault, saved)
    if item_id not in targets:
        raise ValueError(f"Unknown plan item: {item_id}")
    states = _status(vault, plan_id, saved)
    _require_no_conflicts(states)
    complete = states[item_id] == "complete"
    if complete and not export_code:
        return "already complete"
    item = next(item for item in saved["plan"] if item["id"] == item_id)
    if any(states[dep] != "complete" for dep in item.get("depends_on", ())):
        raise ValueError("Publish the planned prerequisites before this note.")
    target = targets[item_id]
    data = (target if complete else draft).read_bytes()
    content = data.decode("utf-8-sig")
    from scriptorium.engines._instructional import coverage_errors
    contract = dict(item.get("decision_contract") or {})
    instructional = contract.get("instructional_plan", {})
    coverage_path = _under_vault(vault, (_plan_dir(vault, plan_id) / f"{item_id}.coverage.json").relative_to(vault).as_posix())
    evidence_path = _under_vault(vault, (_plan_dir(vault, plan_id) / f"{item_id}.evidence.json").relative_to(vault).as_posix())
    if complete and coverage is None and coverage_path.is_file():
        coverage = json.loads(coverage_path.read_text(encoding="utf-8"))["report"]
    if complete and evidence is None and evidence_path.is_file():
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))["registry"]
    errors = coverage_errors(instructional, coverage, content)
    if errors:
        raise ValueError("\n".join(errors))
    normalized_evidence = None
    if evidence is not None:
        from scriptorium.engines.research import normalize_evidence_registry

        normalized_evidence = normalize_evidence_registry(
            evidence,
            research_plan=contract.get("research_plan"),
            mode=contract.get("research_mode") or evidence.get("mode") or "R-I",
        )
        contract["evidence_registry"] = normalized_evidence
        contract["research_mode"] = normalized_evidence["mode"]
    findings = validate_text(
        content, vault=vault, target=target, planned=targets.values(),
        route=item["template"], math_level=item["math_level"],
        decision_contract=contract if contract else None,
    )
    if findings:
        raise ValueError("\n".join(f"{line}: {message}" for line, message in findings))
    metadata, _, _ = read_frontmatter(content)
    if metadata.get("id") != item["note_id"] or item["title"] not in (metadata.get("aliases") or []):
        raise ValueError(f"Draft metadata does not match planned identity: id={item['note_id']}, title={item['title']}")

    examples, blocks, prose = _planned_examples(content, item)
    if examples:
        check_evidence(verify_runtimes(examples, prose), blocks, prose)
    exports = {}
    if export_code:
        for name, block in examples.items():
            export = _under_vault(vault, f"assets/{_slugify(metadata['topic'])}/examples/{_slugify(item['note_id'])}-{name}{EXTENSIONS.get(name, '.py')}")
            exports[export] = block.code.encode("utf-8")
            _check_export(export, exports[export])

    journal = _plan_dir(vault, plan_id)
    intent = _under_vault(vault, (journal / f"{item_id}.intent").relative_to(vault).as_posix())
    receipt = _under_vault(vault, (journal / f"{item_id}.done").relative_to(vault).as_posix())
    digest = _hash(data).encode()
    if coverage is not None:
        coverage_bytes = json.dumps({"draft_hash": digest.decode(), "report": coverage}, sort_keys=True, ensure_ascii=False).encode("utf-8")
        if coverage_path.exists() and coverage_path.read_bytes() != coverage_bytes:
            raise ValueError("Source coverage receipt differs from an earlier publication attempt")
    if normalized_evidence is not None:
        evidence_bytes = json.dumps({"draft_hash": digest.decode(), "registry": normalized_evidence}, sort_keys=True, ensure_ascii=False).encode("utf-8")
        if evidence_path.exists() and evidence_path.read_bytes() != evidence_bytes:
            raise ValueError("Evidence registry receipt differs from an earlier publication attempt")
    try:
        _write_once(intent, digest)
    except FileExistsError:
        if intent.read_bytes() != digest:
            raise ValueError("Publish already started with different draft bytes. Retry the original draft.")
    if coverage is not None:
        try:
            _write_once(coverage_path, coverage_bytes)
        except FileExistsError:
            if coverage_path.read_bytes() != coverage_bytes:
                raise ValueError("Conflicting source coverage receipt; existing report preserved")
    if normalized_evidence is not None:
        try:
            _write_once(evidence_path, evidence_bytes)
        except FileExistsError:
            if evidence_path.read_bytes() != evidence_bytes:
                raise ValueError("Conflicting evidence registry receipt; existing registry preserved")
    for export, example_data in exports.items():
        try:
            _write_once(export, example_data)
        except FileExistsError:
            _check_export(export, example_data)
    if not complete:
        try:
            _write_once(target, data)
        except FileExistsError:
            if target.is_symlink() or not target.is_file() or _hash(target.read_bytes()).encode() != digest:
                raise ValueError(f"Conflicting output, preserved: {target.relative_to(vault)}")
        try:
            _write_once(receipt, digest)
        except FileExistsError:
            pass
    if complete:
        return f"already complete; exported {len(exports)} example(s)"
    return f"published {target.relative_to(vault).as_posix()}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    inspect = commands.add_parser("inspect")
    inspect.add_argument("request")
    inspect.add_argument("--stack", help="Comma-separated stack names.")
    commands.add_parser("setfolder").add_argument("folder_path")
    start = commands.add_parser("start")
    start.add_argument("vault")
    start.add_argument("--request", required=True)
    start.add_argument("--topic-folder", required=True)
    start.add_argument("--outline", type=Path, help="Outline JSON, required when starting a new plan.")
    start.add_argument("--topic", help="Display name when the topic folder uses a slug.")
    start.add_argument("--template", choices=ROUTES)
    start.add_argument("--language")
    start.add_argument("--stack", help="Comma-separated stack names.")
    start.add_argument("--allow-math-override", action="store_true")
    start.add_argument("--legacy-names", action="store_true")
    for action in ("status", "publish", "verify-runtimes"):
        sub = commands.add_parser(action)
        sub.add_argument("vault")
        sub.add_argument("plan_id")
        if action in {"publish", "verify-runtimes"}:
            sub.add_argument("item_id")
            sub.add_argument("draft", type=Path)
        if action == "publish":
            sub.add_argument("--export-code", action="store_true")
            sub.add_argument("--coverage", type=Path, help="Validated source-element coverage report JSON.")
            sub.add_argument("--evidence", type=Path, help="Validated ARRIE source/evidence registry JSON.")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        if args.action == "inspect":
            result = inspect_request(args.request, stack=args.stack.split(",") if args.stack else None)
        elif args.action == "setfolder":
            result = set_notes_folder(args.folder_path)
        else:
            vault = resolve_vault_root(args.vault)
            if args.action == "publish":
                coverage = json.loads(args.coverage.read_text(encoding="utf-8-sig")) if args.coverage else None
                evidence = json.loads(args.evidence.read_text(encoding="utf-8-sig")) if args.evidence else None
                print(publish(vault, args.plan_id, args.item_id, args.draft, export_code=args.export_code, coverage=coverage, evidence=evidence))
                return 0
            if args.action == "verify-runtimes":
                saved = _read_plan(vault, args.plan_id)
                item = next((entry for entry in saved["plan"] if entry["id"] == args.item_id), None)
                if item is None:
                    raise ValueError(f"Unknown plan item: {args.item_id}")
                examples, _, prose = _planned_examples(args.draft.read_text(encoding="utf-8-sig"), item)
                print(json.dumps(verify_runtimes(examples, prose), indent=2, ensure_ascii=False))
                return 0
            if args.action == "start":
                outline = json.loads(args.outline.read_text(encoding="utf-8-sig")) if args.outline else []
                plan_id, saved = start_plan(
                    vault, args.request, args.topic_folder, outline, template=args.template,
                    language=args.language, topic_name=args.topic, legacy_names=args.legacy_names,
                    stack=args.stack.split(",") if args.stack else None, allow_math_override=args.allow_math_override,
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
