"""Shared structural contract for built-in routed notes."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
ROUTES = (
    "deepstudy-coding", "deepstudy-general", "api-table", "cheat-sheet", "atomic",
    "comparison", "summary", "practice", "dsa", "paper-breakdown",
)
PRACTICE_RANGES = ((1, 4), (5, 10), (11, 15))
NARROW_RANGES = ((1, 3), (4, 7), (8, 11))
HINT = "> [!hint]- Need a nudge?"
SOLUTION = "> [!tip]- Reveal approach and solution"
MATH_SECTION = {
    "deepstudy-coding": 3, "deepstudy-general": 3, "api-table": 1,
    "cheat-sheet": 1, "atomic": 1, "comparison": 3, "summary": 2,
    "practice": 1, "dsa": 3, "paper-breakdown": 2,
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
    "deepstudy-coding": {
        2: ("> [!note] Zero-Baseline Prerequisites",),
        3: ("> [!warning] Where the Analogy Breaks Down",),
        6: ("> [!example]- Reveal Detailed Answer & Step-by-Step Breakdown",),
        7: ("> [!caution] Silent Bugs, Gotchas & Anti-Patterns",),
    },
    "deepstudy-general": {
        2: ("> [!note] Zero-Baseline Prerequisites",),
        3: ("> [!warning] Where the Analogy Breaks Down",),
        6: ("> [!example]- Reveal Detailed Answer & Step-by-Step Breakdown",),
        7: ("> [!caution] Common Misconceptions & Anti-Patterns",),
    },
    "api-table": {4: ("> [!caution] Performance Traps, Hidden Allocations & Silent Mutation Bugs",)},
    "cheat-sheet": {4: ("> [!caution] One-Line Exam & Interview Traps",)},
    "comparison": {
        1: ('> [!tip] Executive Decision Rules ("Choose X When...")',),
        5: ("> [!caution] Migration & Selection Traps",),
    },
    "summary": {1: ("> [!info] Source Metadata & Accessibility Audit",)},
    "paper-breakdown": {1: ("> [!info] Primary Paper Metadata",)},
}


def section_layout(route: str, level: int, *, narrow: bool = False) -> list[tuple[int, str]]:
    """Read just one spec. Return stable section IDs and rendered headings."""
    if route not in ROUTES or level not in (0, 1, 2):
        raise ValueError(f"Unknown route or math level: {route}, {level}")
    spec = (ROOT / "templates" / f"{route}.md").read_text(encoding="utf-8")
    headings = re.findall(r"^## .+$", spec.split("> [!important] AGENT AUTHORING DIRECTIVE", 1)[0], re.M)
    layout = []
    for number, heading in enumerate(headings, 1):
        if route == "deepstudy-coding":
            if number == 4 and level == 0:
                continue
            if number == 4 and level == 1:
                heading = "## 4. How do dimensions, shapes, and state invariants transform step by step?"
            if number > 4 and level == 0:
                heading = heading.replace(f"## {number}.", f"## {number - 1}.", 1)
        if route == "deepstudy-general" and number == 4 and level < 2:
            heading = heading.replace("Manual Trace & Derivation", "Manual Trace")
        if route == "practice" and narrow and 2 <= number <= 4:
            first, last = NARROW_RANGES[number - 2]
            heading = re.sub(r"Q\d+–Q\d+", f"Q{first}–Q{last}", heading)
        layout.append((number, heading))
    return layout


def title_heading(route: str, number: str, title: str) -> str:
    if route == "cheat-sheet":
        return f"# {number}. {title} — Cheat Sheet"
    if route == "practice":
        subject = re.sub(r" - Practice(?: Test)?$", "", title)
        return f"# {subject} — Active Recall & Synthesis Practice Set"
    prefix = {"summary": "Summary: ", "dsa": "DSA: ", "paper-breakdown": "Paper Breakdown: "}
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
    lines = [title_heading(route, number, title), ""]
    if level:
        lines += ["> [!abstract] Key Equations", "> <!-- scaffold: Introduce symbols and 1–3 display equations. -->", ""]
    route_header = {
        "comparison": "Core Trade-Off Verdict",
        "dsa": "Complexity Target & Core Invariant",
        "paper-breakdown": "Core Equations & Contribution Summary" if level else "Contribution Summary",
    }
    if route in route_header:
        lines += [f"> [!abstract] {route_header[route]}", "> <!-- scaffold: Fill the abstract. -->", ""]

    for section, heading in section_layout(route, level, narrow=narrow):
        lines += [heading, "", "<!-- scaffold: Author this section using the selected specification. -->", ""]
        for wrapper in CALLOUTS.get(route, {}).get(section, ()):
            lines += [wrapper, "> <!-- scaffold: Fill the callout. -->", ""]
        if route == "cheat-sheet" and section == 1 and level:
            lines += ["> [!abstract] Core Equations & Bounds", "> <!-- scaffold: Add compact bounds. -->", ""]
        if route == "practice" and 2 <= section <= 4:
            first, last = (NARROW_RANGES if narrow else PRACTICE_RANGES)[section - 2]
            for question in range(first, last + 1):
                lines += [
                    f"### Q{question}. <!-- scaffold: Question prompt. -->", "",
                    HINT, "> <!-- scaffold: Non-spoiling hint. -->", "",
                    SOLUTION, "> <!-- scaffold: Approach, final answer, and common trap. -->", "",
                ]
        if level and section == MATH_SECTION[route]:
            lines += _math_slots(level, inline_proof=route != "deepstudy-coding", compact=route == "atomic")
        if level == 2 and route == "deepstudy-coding" and section == 4:
            lines += _proof_slots()
    footer = (ROOT / "shared" / "footer_widgets.md").read_text(encoding="utf-8")
    return "\n".join(lines) + "\n" + footer.split("<!-- scaffold:footer -->", 1)[1].lstrip("\n")
