"""Shared structural layout contract for M1-M7 masters and compatibility routes."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
DEEP_ROUTES = {"deepstudy-master", "deep-notes"}
CANONICAL_MASTER_ROUTES = (
    "deep-notes",
    "study-notes",
    "quick-reference",
    "worked-solutions",
    "implementation-guide",
    "assessment",
    "synthesis-revision",
)
COMPAT_ROUTES = (
    "deepstudy-master", "api-table", "cheat-sheet", "atomic",
    "comparison", "summary", "practice", "dsa", "paper-breakdown", "studynotes",
)
ROUTES = COMPAT_ROUTES + CANONICAL_MASTER_ROUTES
ADAPTIVE_ROUTES = DEEP_ROUTES | {"studynotes", "study-notes"}

ROUTE_TO_CANONICAL_NOTE_TYPE = {
    "deep-notes": "deep-notes",
    "deepstudy-master": "deep-notes",
    "study-notes": "study-notes",
    "studynotes": "study-notes",
    "quick-reference": "quick-reference",
    "cheat-sheet": "quick-reference",
    "api-table": "quick-reference",
    "atomic": "quick-reference",
    "worked-solutions": "worked-solutions",
    "implementation-guide": "implementation-guide",
    "dsa": "implementation-guide",
    "assessment": "assessment",
    "practice": "assessment",
    "synthesis-revision": "synthesis-revision",
    "comparison": "synthesis-revision",
    "summary": "synthesis-revision",
    "paper-breakdown": "synthesis-revision",
    "index": "index",
}

TEMPLATE_PATHS = {
    "deep-notes": "references/templates/masters/deep-notes.md",
    "study-notes": "references/templates/masters/study-notes.md",
    "quick-reference": "references/templates/masters/quick-reference.md",
    "worked-solutions": "references/templates/masters/worked-solutions.md",
    "implementation-guide": "references/templates/masters/implementation-guide.md",
    "assessment": "references/templates/masters/assessment.md",
    "synthesis-revision": "references/templates/masters/synthesis-revision.md",
    "deepstudy-master": "references/templates/masters/deep-notes.md",
    "studynotes": "references/templates/masters/study-notes.md",
    "cheat-sheet": "references/templates/masters/quick-reference.md",
    "dsa": "references/templates/masters/implementation-guide.md",
    "practice": "references/templates/masters/assessment.md",
    "api-table": "references/templates/variants/syntax-reference.md",
    "atomic": "references/templates/variants/atomic-card.md",
    "comparison": "references/templates/variants/comparison-guide.md",
    "summary": "references/templates/variants/quick-summary.md",
    "paper-breakdown": "references/templates/variants/paper-breakdown.md",
}

LEGACY_STUDY_LAYOUT = (
    "What is this note about, where does the material come from, and what should I learn? (Overview, Source Context & Learning Goals)",
    "How does the source develop each idea, and how can I understand it step by step? (Core Concepts & Sequential Breakdown)",
    "What should I remember, test myself on, and study next? (Key Takeaways & Active Recall)",
)
PRACTICE_RANGES = ((1, 5), (6, 12), (13, 18))
NARROW_RANGES = ((1, 3), (4, 7), (8, 11))
HINT = "> [!hint]- Need a nudge?"
SOLUTION = "> [!tip]- Reveal approach and solution"
MATH_SECTION = {
    "api-table": 1,
    "cheat-sheet": 1, "quick-reference": 1,
    "atomic": 1,
    "comparison": 3,
    "summary": 2,
    "practice": 1, "assessment": 1,
    "dsa": 3, "implementation-guide": 3,
    "paper-breakdown": 2,
    "studynotes": 2, "study-notes": 2,
    "worked-solutions": 2,
    "synthesis-revision": 2,
}
SYMBOL_TABLE = (
    "| Symbol / Operator | Meaning | Shape / Dimensions | Domain / Units | Directional Sensitivity |",
    "|---|---|---|---|---|",
)
BEHAVIOR_TABLE = (
    "| Case | Concrete Inputs | Intermediate Computation | Final Output | Interpretation |",
    "|---|---|---|---|---|",
)
CALLOUTS = {
    "api-table": {4: ("> [!caution] Performance Traps, Hidden Allocations & Silent Mutation Bugs",)},
    "cheat-sheet": {4: ("> [!caution] One-Line Exam & Interview Traps",)},
    "quick-reference": {4: ("> [!caution] One-Line Exam & Interview Traps",)},
    "comparison": {
        1: ('> [!tip] Executive Decision Rules ("Choose X When...")',),
        5: ("> [!caution] Migration & Selection Traps",),
    },
    "summary": {1: ("> [!info] Source Metadata & Accessibility Audit",)},
    "paper-breakdown": {1: ("> [!info] Primary Paper Metadata",)},
    "studynotes": {1: ("> [!info] Source & Scope Context",)},
    "study-notes": {1: ("> [!info] Source & Scope Context",)},
}


def canonical_note_type(route: str | None) -> str:
    if not route:
        return "deep-notes"
    return ROUTE_TO_CANONICAL_NOTE_TYPE.get(route.strip().lower(), "deep-notes")


def _template_path(route: str) -> Path:
    rel = TEMPLATE_PATHS.get(route)
    if rel:
        candidate = ROOT / rel
        if candidate.is_file():
            return candidate
    fallback = ROOT / "templates" / f"{route}.md"
    if fallback.is_file():
        return fallback
    if rel:
        return ROOT / rel
    raise ValueError(f"Unknown route: {route}")


def section_layout(route: str, level: int, *, narrow: bool = False) -> list[tuple[int, str]]:
    """Read just one spec. Return stable section IDs and rendered headings."""
    if route not in ROUTES or level not in ((0, 1, 2, 3) if route in DEEP_ROUTES else (0, 1, 2)):
        raise ValueError(f"Unknown route or math level: {route}, {level}")
    if route in DEEP_ROUTES:
        return []
    spec = _template_path(route).read_text(encoding="utf-8")
    headings = re.findall(r"^## (?!\[OPTIONAL\]).+$", spec.split("> [!important] AGENT AUTHORING DIRECTIVE", 1)[0], re.M)
    layout = []
    for number, heading in enumerate(headings, 1):
        if route in {"practice", "assessment"} and narrow and 1 <= number <= 3:
            first, last = NARROW_RANGES[number - 1]
            heading = re.sub(r"Q\d+–Q\d+", f"Q{first}–Q{last}", heading)
        heading = re.sub(r"^## \d+\.", f"## {len(layout) + 1}.", heading)
        layout.append((number, heading))
    return layout


def title_heading(route: str, number: str, title: str) -> str:
    if route in {"cheat-sheet", "quick-reference"}:
        return f"# {number}. {title} — Cheat Sheet"
    if route in {"practice", "assessment"}:
        subject = re.sub(r" - Practice(?: Test)?$", "", title)
        return f"# {subject} — Active Recall & Synthesis Practice Set"
    prefix = {
        "summary": "Summary: ",
        "dsa": "DSA: ",
        "implementation-guide": "Implementation: ",
        "paper-breakdown": "Paper Breakdown: ",
        "studynotes": "",
        "study-notes": "",
        "worked-solutions": "Worked Solutions: ",
        "synthesis-revision": "Synthesis & Revision: ",
    }
    if route == "comparison":
        return f"# {number}. {title} — Decision & Trade-Off Analysis"
    if route == "atomic":
        return f"# {title}"
    return f"# {prefix.get(route, f'{number}. ')}{title}"


def _math_slots(level: int, *, inline_proof: bool, compact: bool) -> list[str]:
    lines = []
    if level == 2:
        lines += ["### Mathematical Intuition", "<!-- scaffold: Explain scale and sensitivity. -->", ""]
    lines += [
        *([] if compact else ["### Governing Equation & Complete Symbol Anatomy"]),
        "<!-- scaffold: Define all symbols, domain and assumptions; then show the display equation. -->",
        "",
        *SYMBOL_TABLE,
        "",
        *([] if compact else ["### Input-to-Output Behavior"]),
        *BEHAVIOR_TABLE,
    ]
    for label in ("Smallest non-trivial", "Named running example", "Perturbed input", "Boundary / degenerate"):
        lines.append(f"| {label} | | | | |")
    lines.append("")
    if level == 2:
        lines += [
            "### Boundary & Limit Analysis",
            "<!-- scaffold: Evaluate zero, ±1, ties and ±∞ under the stated domain. -->",
            "",
            "### Overgeneralization Counterexample",
            "<!-- scaffold: Give a concrete invalid application. -->",
            "",
        ]
        if inline_proof:
            lines += ["### Derivation" if compact else "### Why does the math hold? (Zero-Skip Derivation)", *_proof_slots()]
    return lines


def _proof_slots() -> list[str]:
    return [
        "<!-- scaffold: State target, domain and strategy; number every display-math step. -->",
        "",
        "*Why this step holds:* <!-- scaffold: Justify the assumption, guards and implication. -->",
        "",
    ]


def body_skeleton(route: str, level: int, number: str, title: str, *, narrow: bool) -> str:
    layout = section_layout(route, level, narrow=narrow)
    lines = [title_heading(route, number, title), ""]
    if route in DEEP_ROUTES:
        return "\n".join(lines) + (
            "\n<!-- scaffold: Read references/templates/masters/deep-notes.md and "
            "references/workflows/notes-creation/adaptive-engine.md; "
            "compose only the selected instructional modules. Remove this instruction before publishing. -->\n"
        )
    if route in {"studynotes", "study-notes"}:
        for section, heading in layout:
            lines += [heading, "", "<!-- scaffold: Follow this section's gate in references/templates/masters/study-notes.md. -->", ""]
            if section == 1:
                lines += [CALLOUTS[route][1][0], "> <!-- scaffold: Record actual source, access and scope. -->", ""]
        return "\n".join(lines)
    if level and route not in {"practice", "assessment"}:
        lines += ["> [!abstract] Key Equations", "> <!-- scaffold: Introduce symbols and 1–3 display equations. -->", ""]
    route_header = {
        "comparison": "Core Trade-Off Verdict",
        "dsa": "Complexity Target & Core Invariant",
        "implementation-guide": "Complexity Target & Core Invariant",
        "paper-breakdown": "Core Equations & Contribution Summary" if level else "Contribution Summary",
    }
    if route in route_header:
        lines += [f"> [!abstract] {route_header[route]}", "> <!-- scaffold: Fill the abstract. -->", ""]

    for section, heading in layout:
        lines += [heading, ""]
        if route not in {"practice", "assessment"}:
            lines += ["<!-- scaffold: Author this section using the selected specification. -->", ""]
        for wrapper in CALLOUTS.get(route, {}).get(section, ()):
            lines += [wrapper, "> <!-- scaffold: Fill the callout. -->", ""]
        if route in {"cheat-sheet", "quick-reference"} and section == 1 and level:
            lines += ["> [!abstract] Core Equations & Bounds", "> <!-- scaffold: Add compact bounds. -->", ""]
        if route in {"practice", "assessment"} and 1 <= section <= 3:
            first, last = (NARROW_RANGES if narrow else PRACTICE_RANGES)[section - 1]
            for question in range(first, last + 1):
                lines += [
                    f"### Q{question}. <!-- scaffold: Question prompt. -->", "",
                    HINT, "> <!-- scaffold: Non-spoiling hint. -->", "",
                    SOLUTION, "> <!-- scaffold: Approach, final answer, and common trap. -->", "",
                ]
        if level and route not in {"practice", "assessment"} and section == MATH_SECTION[route]:
            lines += _math_slots(level, inline_proof=True, compact=route == "atomic")
    if route in {"practice", "assessment"}:
        return "\n".join(lines).rstrip() + "\n"
    footer = (ROOT / "shared" / "footer_widgets.md").read_text(encoding="utf-8")
    return "\n".join(lines) + "\n" + footer.split("<!-- scaffold:footer -->", 1)[1].lstrip("\n")


def optional_headings(route):
    """Read optional declarations from templates, never duplicate module IDs here."""
    spec = _template_path(route).read_text(encoding="utf-8")
    return re.findall(r"^## \[OPTIONAL\] (.+)$", spec, re.M)


def heading_key(heading):
    return re.sub(r"^## (?:\d+\. )?", "", heading).strip()


def matches_legacy_study(headings):
    actual = [heading_key(heading) for heading in headings]
    return [heading for heading in actual if heading in LEGACY_STUDY_LAYOUT] == list(LEGACY_STUDY_LAYOUT)


def matches_layout(route, level, headings, *, narrow=False):
    optional = set(optional_headings(route))
    actual = [heading_key(h) for h in headings]
    if len(actual) != len(set(actual)):
        return False
    core = [h for h in actual if h not in optional]
    expected = [heading_key(h) for _, h in section_layout(route, level, narrow=narrow)]
    if route in {"studynotes", "study-notes"}:
        required = {expected[0], expected[1], expected[-1]}
        return (
            required <= set(core)
            and core == [heading for heading in expected if heading in core]
            and all(heading.startswith(f"## {number}. ") for number, heading in enumerate(headings, 1))
        )
    if route in {"practice", "assessment"}:
        def _tier_norm(text: str) -> str:
            return re.sub(r"\s*\(Q\d+–Q\d+\)\s*$", "", text).strip()
        return [_tier_norm(h) for h in core] == [_tier_norm(h) for h in expected]
    return core == expected
