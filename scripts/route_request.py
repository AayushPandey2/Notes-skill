"""Cheap routing aid for the prompt dispatcher; research and authoring stay in the skill.

Broad topics use one call per planned note, with purpose/depth from the outline.
The helper never fetches sources, loads template bodies or writes vault notes.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex

from note_contracts import resources_for, route_name, routes

PURPOSES = {"revision": "cheat-sheet", "choice": "comparison", "lookup": "api-table",
            "idea": "atomic", "implementation": "deepstudy-coding", "understanding": "deepstudy-general"}


def plan_request(request: str, *, template: str | None = None, purpose: str | None = None,
                 math_level: int = 0, language: str | None = None, domain: str = "general") -> dict:
    if math_level not in (0, 1, 2):
        raise ValueError("Math level must be 0, 1, or 2")
    tokens = shlex.split(request)
    if not tokens:
        raise ValueError("Supply a topic, source URL, or /scribe command")
    command = tokens.pop(0) if tokens[0].startswith("/") else None
    known = {"/scribe-" + s for s in ["notes", "expand", "ingest", "distill", "compare", "doubt", "quiz", "dsa", "practice"]}
    if command and command not in known:
        raise ValueError(f"Unknown command {command}")
    locked = {"/scribe-dsa": "dsa", "/scribe-practice": "practice", "/scribe-distill": "cheat-sheet", "/scribe-compare": "comparison"}.get(command)
    if command == "/scribe-dsa":
        if len(tokens) < 2 or tokens[0] not in {"cpp", "c++", "c++20", "python", "python3"}:
            raise ValueError("Usage: /scribe-dsa <cpp|python> <problem text or URL>")
        language = "cpp" if tokens.pop(0) in {"cpp", "c++", "c++20"} else "python"
    if command and not tokens:
        raise ValueError(f"Usage: {command} <topic or source>")
    if command in {"/scribe-doubt", "/scribe-quiz"}:
        if template:
            raise ValueError(f"{command} does not generate a template note")
        return {"command": command, "mode": "read-only" if command.endswith("doubt") else "interactive", "resources": []}
    selected = route_name(template) if template else None
    if locked and selected and locked != selected:
        raise ValueError(f"{command} locks {locked}; explicit {selected} conflicts")
    payload = " ".join(tokens)
    if not selected:
        for name in routes():
            if re.search(r"\b" + re.escape(name) + r"\b", payload, re.I):
                selected = name
                break
    text = payload.lower()
    urls = re.findall(r"https?://[^\s<>]+", payload)
    standalone = bool(urls) and payload.strip() == urls[0] and len(urls) == 1
    summary_intent = bool(re.search(r"\b(?:summari[sz]e|summary)\b", text))
    if not locked and not selected:
        if standalone or summary_intent:
            selected = "paper-breakdown" if urls and re.search(r"(?:arxiv\.org/(?:abs|pdf)/|openreview\.net/|doi\.org/)", urls[0]) and not summary_intent else "summary"
        elif purpose:
            selected = PURPOSES[purpose]
        elif re.search(r"\b(?:revise|revision|cheat sheet)\b", text): selected = "cheat-sheet"
        elif re.search(r"\b(?:compare|versus|vs)\b", text): selected = "comparison"
        elif re.search(r"\b(?:parameters|signatures|api catalog|lookup)\b", text): selected = "api-table"
        elif re.search(r"\b(?:implement|implementation|debug|trace code)\b", text): selected = "deepstudy-coding"
        else: selected = "deepstudy-general"
    selected = locked or selected
    defaults = {"ml": "python", "dsa": "cpp", "systems": "c", "databases": "sql", "web": "typescript"}
    language = language or defaults.get(domain)
    entry = {"command": command, "title": payload, "template": selected, "math_level": math_level,
             "language": language, "source_profile": routes()[selected]["source_profile"],
             "practice_policy": "none" if selected == "practice" else "topic-set-if-new-folder",
             "routing_reason": "command" if locked else "explicit-template" if template else "source-or-purpose"}
    entry["resources"] = resources_for(entry)
    return entry


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request")
    parser.add_argument("--template")
    parser.add_argument("--purpose", choices=PURPOSES)
    parser.add_argument("--math-level", type=int, choices=[0, 1, 2], default=0)
    parser.add_argument("--language")
    parser.add_argument("--domain", default="general", choices=["general", "ml", "dsa", "systems", "databases", "web"])
    args = parser.parse_args(argv)
    try:
        print(json.dumps(plan_request(**vars(args)), indent=2))
    except ValueError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
