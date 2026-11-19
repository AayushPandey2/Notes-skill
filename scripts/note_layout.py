"""Shared structural contract for built-in routed notes."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
DEEP_ROUTES = {"deepstudy-master"}
ROUTES = (
    "deepstudy-master", "api-table", "cheat-sheet", "atomic",
    "comparison", "summary", "practice", "dsa", "paper-breakdown", "studynotes",
)
ADAPTIVE_ROUTES = DEEP_ROUTES | {"studynotes"}
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
    "cheat-sheet": 1, "atomic": 1, "comparison": 3, "summary": 2,
    "practice": 1, "dsa": 3, "paper-breakdown": 2, "studynotes": 2,
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
    "comparison": {
        1: ('> [!tip] Executive Decision Rules ("Choose X When...")',),
        5: ("> [!caution] Migration & Selection Traps",),
    },
    "summary": {1: ("> [!info] Source Metadata & Accessibility Audit",)},
    "paper-breakdown": {1: ("> [!info] Primary Paper Metadata",)},
    "studynotes": {1: ("> [!info] Source & Scope Context",)},
}


def section_layout(route: str, level: int, *, narrow: bool = False) -> list[tuple[int, str]]:
    """Read just one spec. Return stable section IDs and rendered headings."""
    if route not in ROUTES or level not in ((0, 1, 2, 3) if route in DEEP_ROUTES else (0, 1, 2)):
        raise ValueError(f"Unknown route or math level: {route}, {level}")
    if route in DEEP_ROUTES:
        # The decision record, not a heading list, selects adaptive modules.
        return []
    spec = (ROOT / "templates" / f"{route}.md").read_text(encoding="utf-8")
    headings = re.findall(r"^## (?!\[OPTIONAL\]).+$", spec.split("> [!important] AGENT AUTHORING DIRECTIVE", 1)[0], re.M)
    layout = []
    for number, heading in enumerate(headings, 1):
        if route == "practice" and narrow and 1 <= number <= 3:
            first, last = NARROW_RANGES[number - 1]
            heading = re.sub(r"Q\d+–Q\d+", f"Q{first}–Q{last}", heading)
        heading = re.sub(r"^## \d+\.", f"## {len(layout) + 1}.", heading)
        layout.append((number, heading))
    return layout


def title_heading(route: str, number: str, title: str) -> str:
    if route == "cheat-sheet":
        return f"# {number}. {title} — Cheat Sheet"
    if route == "practice":
        subject = re.sub(r" - Practice(?: Test)?$", "", title)
        return f"# {subject} — Active Recall & Synthesis Practice Set"
    prefix = {"summary": "Summary: ", "dsa": "DSA: ", "paper-breakdown": "Paper Breakdown: ", "studynotes": ""}
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
            "\n<!-- scaffold: Read templates/deepstudy-master.md and references/adaptive-engine.md; "
            "compose only the selected instructional modules. Remove this instruction before publishing. -->\n"
        )
    if route == "studynotes":
        for section, heading in layout:
            lines += [heading, "", "<!-- scaffold: Follow this section's gate in templates/studynotes.md. -->", ""]
            if section == 1:
                lines += [CALLOUTS[route][1][0], "> <!-- scaffold: Record actual source, access and scope. -->", ""]
        return "\n".join(lines)
    if level and route != "practice":
        lines += ["> [!abstract] Key Equations", "> <!-- scaffold: Introduce symbols and 1–3 display equations. -->", ""]
    route_header = {
        "comparison": "Core Trade-Off Verdict",
        "dsa": "Complexity Target & Core Invariant",
        "paper-breakdown": "Core Equations & Contribution Summary" if level else "Contribution Summary",
    }
    if route in route_header:
        lines += [f"> [!abstract] {route_header[route]}", "> <!-- scaffold: Fill the abstract. -->", ""]

    for section, heading in layout:
        lines += [heading, ""]
        if route != "practice":
            lines += ["<!-- scaffold: Author this section using the selected specification. -->", ""]
        for wrapper in CALLOUTS.get(route, {}).get(section, ()):
            lines += [wrapper, "> <!-- scaffold: Fill the callout. -->", ""]
        if route == "cheat-sheet" and section == 1 and level:
            lines += ["> [!abstract] Core Equations & Bounds", "> <!-- scaffold: Add compact bounds. -->", ""]
        if route == "practice" and 1 <= section <= 3:
            first, last = (NARROW_RANGES if narrow else PRACTICE_RANGES)[section - 1]
            for question in range(first, last + 1):
                lines += [
                    f"### Q{question}. <!-- scaffold: Question prompt. -->", "",
                    HINT, "> <!-- scaffold: Non-spoiling hint. -->", "",
                    SOLUTION, "> <!-- scaffold: Approach, final answer, and common trap. -->", "",
                ]
        if level and route != "practice" and section == MATH_SECTION[route]:
            lines += _math_slots(level, inline_proof=True, compact=route == "atomic")
    if route == "practice":
        return "\n".join(lines).rstrip() + "\n"
    footer = (ROOT / "shared" / "footer_widgets.md").read_text(encoding="utf-8")
    return "\n".join(lines) + "\n" + footer.split("<!-- scaffold:footer -->", 1)[1].lstrip("\n")


def optional_headings(route):
    """Read optional declarations from templates, never duplicate module IDs here."""
    spec = (ROOT / "templates" / f"{route}.md").read_text(encoding="utf-8")
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
    if route == "studynotes":
        required = {expected[0], expected[1], expected[-1]}
        return (
            required <= set(core)
            and core == [heading for heading in expected if heading in core]
            and all(heading.startswith(f"## {number}. ") for number, heading in enumerate(headings, 1))
        )
    if route == "practice":
        def _tier_norm(text: str) -> str:
            return re.sub(r"\s*\(Q\d+–Q\d+\)\s*$", "", text).strip()
        return [_tier_norm(h) for h in core] == [_tier_norm(h) for h in expected]
    return core == expected
