"""Shared registry, safe vault paths, and Markdown measurements (no generation)."""
from __future__ import annotations

import json
import os
import re
from functools import lru_cache
from pathlib import Path, PureWindowsPath

ROOT = Path(__file__).resolve().parent.parent


@lru_cache(maxsize=1)
def routes() -> dict:
    return json.loads((ROOT / "references/routes.json").read_text(encoding="utf-8"))


def route_name(value: str) -> str:
    key = re.sub(r"[^a-z0-9]", "", value.lower())
    for name, spec in routes().items():
        if key in {re.sub(r"[^a-z0-9]", "", s.lower()) for s in [name, *spec.get("aliases", [])]}:
            return name
    raise ValueError(f"Unsupported template {value!r}. Choose: {', '.join(routes())}")


def resolve_vault(explicit: str | None = None) -> Path:
    # One resolver for discovery, scaffolding and routing.
    from vault_index import resolve_vault_root
    return resolve_vault_root(explicit)


def route_headings(template: str, math_level: int = 0) -> list[str]:
    headings = list(routes()[route_name(template)]["headings"])
    if template == "paper-breakdown" and math_level == 0:
        headings[4] = "Technical Details"
    return headings


def safe_path(root: Path, relative: str) -> Path:
    """Validate vault-relative paths, including Windows names when run on POSIX."""
    relative = str(relative).replace("\\", "/")
    parts = relative.split("/")
    if not relative or PureWindowsPath(relative).drive or relative.startswith("/"):
        raise ValueError(f"Expected a relative vault path: {relative!r}")
    for part in parts:
        if part in {"", ".", ".."} or part.startswith(".") or part.endswith((".", " ")):
            raise ValueError(f"Unsafe path component: {part!r}")
        if re.search(r'[<>:"|?*\x00-\x1f]', part) or re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", part, re.I):
            raise ValueError(f"Invalid filename component: {part!r}")
    root = root.resolve()
    target = root.joinpath(*parts).resolve()
    if not target.is_relative_to(root):
        raise ValueError("Path or symlink escapes the vault")
    return target


def body_text(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[i + 1:])
    return text


def prose_lines(text: str):
    """Yield line numbers and text outside fenced code, including quoted callouts."""
    fence = None
    for n, raw in enumerate(text.splitlines(), 1):
        line = re.sub(r"^(?:\s*> ?)+", "", raw)
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, suffix = match.groups()
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not suffix.strip():
                fence = None
            continue
        if fence is None:
            yield n, line


def rendered_word_count(text: str) -> int:
    """Deterministic approximation documented in note_templates.md; includes code/tables."""
    text = body_text(text)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"!?(?:\[\[)([^\]]+)\]\]", lambda m: re.split(r"\\?\|", m[1])[-1], text)
    text = re.sub(r"!?\[([^\]]*)\]\([^\n)]*\)", r"\1", text)
    text = re.sub(r"^\s*\[[^\]]+\]:.*$", "", text, flags=re.M)
    text = re.sub(r"https?://[^\s<>]+", "", text)
    rendered = []
    for line in text.splitlines():
        line = re.sub(r"^(?:\s*> ?)+", "", line)
        if re.match(r"^\s*(`{3,}|~{3,})", line) or re.fullmatch(r"[\s|:\-]+", line):
            continue
        line = re.sub(r"^\[![^\]]+\][+-]?\s*", "", line)
        line = re.sub(r"^\s*(?:#{1,6}\s+|[-+*]\s+|\d+\.\s+)", "", line)
        line = line.replace("\\|", " ").replace("|", " ")
        line = re.sub(r"[\$`*_~]", "", line)
        rendered.extend(t for t in line.split() if re.search(r"\w", t))
    return len(rendered)


def resources_for(entry: dict) -> list[str]:
    """Return only the chosen contract and its conditional shared modules."""
    spec = routes()[entry["template"]]
    resources = ["references/note_templates.md", "references/modules/authoring.md"]
    resources.append(entry.get("custom_template") or spec["file"])
    if entry.get("math_level", 0):
        resources.append("references/modules/math.md")
    if spec.get("verification") or entry.get("implementation_weight"):
        resources.append("references/modules/verification.md")
    return resources


def validate_route(text: str, template: str, math_level: int = 0, *, expanded_sheet: bool = False) -> list[tuple[str, str]]:
    """Structural gates; source accuracy, proofs and pedagogical depth still need review."""
    body = body_text(text)
    lines = list(prose_lines(body))
    prose = "\n".join(line for _, line in lines)
    errors = []
    def fail(code, message):
        errors.append((code, message))
    headings = re.findall(r"^## (.+)$", prose, re.M)
    if headings != route_headings(template, math_level):
        fail("ROUTE_HEADINGS", f"Expected the ordered {template} heading contract")
    sections = re.split(r"^## .+\n?", prose, flags=re.M)[1:]
    if any(not section.strip() for section in sections):
        fail("EMPTY_ROUTE_SECTION", "Populate every required section")
    if "SCRIPTORIUM_DRAFT" in body or re.search(r"<%(?:.|\n)*?%>|\{\{[^}]+\}\}|<(?:Equation|Term|Starting|Governing|exact|Title)[^>]*>", body):
        fail("UNFINISHED_NOTE", "Materialize the draft before marking it complete")
    if math_level not in (0, 1, 2):
        fail("MATH_LEVEL", "Math level must be 0, 1, or 2")
    elif math_level == 0:
        if re.search(r"(?<!\\)\$(?:[^$\n]+\$|\$)", re.sub(r"`[^`]*`", "", prose)) or re.search(r"^#{2,6} .*\b(?:equations?|derivation|symbol anatomy)\b", prose, re.M | re.I):
            fail("MATH_GATE", "Level 0 must omit equations and math-only headings")
    elif template not in {"atomic", "cheat-sheet", "practice"}:
        if "$$" not in prose or not re.search(r"\|\s*Symbol\b", prose, re.I):
            fail("MATH_CONTRACT", "Define symbols in a table before the display formula")
        if math_level == 2 and "Why this step holds" not in prose:
            fail("DERIVATION_JUSTIFICATION", "Justify nontrivial derivation steps explicitly")
    count = rendered_word_count(text)
    if template == "atomic" and count >= 150:
        fail("ATOMIC_WORD_LIMIT", f"Rendered body is {count} words; must be under 150")
    if template == "cheat-sheet" and not expanded_sheet:
        if count > 350:
            fail("CHEATSHEET_WORD_LIMIT", f"Rendered body is {count} words; maximum is 350")
        for _, line in lines:
            if re.match(r"^\s*[-+*] ", line) and rendered_word_count(line) > 20:
                fail("CHEATSHEET_BULLET_LIMIT", "Ordinary bullets must have at most 20 words")
                break
    if template.startswith("deepstudy-"):
        if "**Confusion** ::" not in prose:
            fail("MISSING_CONFUSION", "Keep the existing review field")
        learned = body.split("## What I learned", 1)[-1].split("## Open Confusion", 1)[0]
        questions = re.split(r"^#{3,4} (?:Question\s*|Q)\d+[^\n]*", learned, flags=re.M)[1:]
        if not 5 <= len(questions) <= 7:
            fail("TRANSFER_QUESTION_COUNT", "Deep notes require 5–7 transfer questions")
        if any(not re.search(r"^> \[!example\]-", q, re.M) for q in questions):
            fail("MISSING_ANSWER_CALLOUT", "Each transfer answer must be independently collapsed")
    if template == "practice":
        # Work on raw text: prose_lines deliberately strips callout prefixes.
        questions = re.split(r"^### Q\d+[^\n]*", body, flags=re.M)[1:]
        if not 10 <= len(questions) <= 15:
            fail("PRACTICE_QUESTION_COUNT", "Use 10–15 distinct questions")
        for question in questions:
            if not all(re.search(pattern, question, re.M) for pattern in [r"^> \[!hint\]-", r"^> \[!tip\]-"]):
                fail("PRACTICE_CALLOUTS", "Each question needs separate collapsed hint and solution")
                break
            if not all(label in question for label in ["**Core intuition:**", "**Final answer:**", "**Common trap:**"]):
                fail("PRACTICE_SOLUTION", "Give intuition, steps, final answer and common trap")
                break
    if template == "summary":
        main = prose.split("## Main idea", 1)[-1].split("## Breakdown", 1)[0]
        if len(re.findall(r"^[-*] ", main, re.M)) != 3:
            fail("SUMMARY_THESIS_COUNT", "Main idea needs exactly three thesis bullets")
    if re.search(r"</?(?:details|summary)\b", prose, re.I):
        fail("FORBIDDEN_HTML_CALLOUT", "Use native Obsidian callouts for built-in routes")
    return errors
