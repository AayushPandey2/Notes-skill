#!/usr/bin/env python3
"""Deterministic 7-section deep-note skeleton generator for Scriptorium.

Generates a compliant YAML frontmatter + > [!abstract] Key Equations +
7-section deep-note Markdown skeleton so the LLM does not spend output
tokens emitting boilerplate structure.

Usage:
  python3 scripts/scaffold_note.py "<vault_path>" \\
      --output "ml/02-gradient-descent.md" \\
      --id "ml-02" --number "02" --title "Gradient Descent" \\
      --base-domain "Computer Science" --master-topic "Machine Learning" --topic "Optimization" \\
      --tags ml optimization --depends-on "[[01-calculus|Calculus]]"
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import os
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from vault_index import is_within_vault, resolve_vault_root


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
    """Render a deterministic 7-section Scriptorium deep-note Markdown skeleton."""
    alias_list = [title]
    for a in aliases or []:
        cleaned = a.strip()
        if cleaned and cleaned not in alias_list:
            alias_list.append(cleaned)

    tag_list = list(
        dict.fromkeys(
            [t.strip().lstrip("#") for t in (tags or []) if t.strip()]
            or [_slugify(base_domain), _slugify(master_topic), _slugify(topic), _slugify(title)]
        )
    )

    lines: list[str] = [
        "---",
        f"id: {_yaml_quote(note_id)}",
        f"title: {_yaml_quote(title)}",
        "aliases:",
    ]
    for a in alias_list:
        lines.append(f"  - {_yaml_quote(a)}")
    lines.extend(
        [
            f"base_domain: {_yaml_quote(base_domain)}",
            f"master_topic: {_yaml_quote(master_topic)}",
            f"topic: {_yaml_quote(topic)}",
        ]
    )
    if depends_on:
        lines.append("depends_on:")
        for dep in depends_on:
            lines.append(f"  - {_yaml_quote(_format_wikilink(dep))}")
    if next_topic:
        lines.append(f"next_topic: {_yaml_quote(_format_wikilink(next_topic))}")
    lines.append("tags:")
    for t in tag_list:
        lines.append(f"  - {_yaml_quote(t)}")
    lines.extend(
        [
            "---",
            "",
            f"# {number}. {title}",
            "",
            "> [!abstract] Key Equations",
            "> - **<Equation Name>:**",
            ">   $$<Display LaTeX Equation>$$",
            "",
            "<!-- SECTION: S1-SYNTHESIS -->",
            "## 1. Executive Synthesis & Architectural Significance",
            "",
            "### Core Problem & Computational Purpose",
            "<!-- 3-4 symbol-free sentences: problem, inputs/outputs, simpler-approach limit -->",
            "",
            "- **Learning outcome:** <!-- explain, solve, implement, or evaluate -->",
            "- **Scope:** <!-- formulation, level, validity conditions, nearby topics -->",
            "- **Practical recognition:** <!-- cue favoring this vs. alternative -->",
            "",
            "### Governing Mechanism & Unbreakable Invariant",
            "<!-- 2-3 sentences: central mechanism + governing invariant & domain -->",
            "",
            "- **Validity boundary:** <!-- condition outside which mechanism changes -->",
            "- **Success criterion:** <!-- how a correct result is recognized -->",
            "",
            "### Position in the Broader Architecture",
            f"- **Taxonomic Lineage:** `{base_domain}` $\\to$ `{master_topic}` $\\to$ `{topic}` $\\to$ **`{title}`**",
            "- **Systemic Role:** <!-- direct prerequisites, downstream consumers, real interface -->",
            "- **Conceptual Mental Model:** <!-- 1-sentence mental model -->",
            "",
            "<!-- SECTION: S2-CONTEXT -->",
            "## 2. Building Blocks & Deep Historical Context",
            "",
            "> [!note] Zero-Baseline Prerequisites",
            "> Introduce terms in dependency order before using them in equations.",
            "> - **<Term 1> ($x_i$):** <!-- meaning, type/domain/units, tiny example -->",
            "> - **Readiness check:** <!-- small prerequisite task + short answer -->",
            "> - **Prerequisite connections:** <!-- [[Exact Filename|Title]] + skill needed -->",
            "",
            "### Historical & Engineering Motivation (Why This Had to Be Invented)",
            "",
            "#### The Pre-Invention Bottleneck",
            "<!-- 4-5 sentences cited to verified sources -->",
            "",
            "#### The Breakthrough & Core Insight",
            "<!-- 4-5 sentences: conceptual shift, verified attribution/dates -->",
            "",
            "#### Theoretical Impact & Modern Legacy",
            "<!-- 3-4 sentences: enabled capability, refinement, modern scope -->",
            "",
            "<!-- SECTION: S3-THEORY -->",
            "## 3. Deep Theory Stack: Intuition to Formal Mathematics",
            "",
            "### Daily-Life Analogy",
            "<!-- Concrete everyday analogy + explicit object mapping -->",
            "",
            "> [!warning] Where the Analogy Breaks Down",
            "> <!-- 2-3 sentences: preserved, omitted, incorrect prediction -->",
            "",
            "### Step-by-Step Mechanism & Visuals",
            "- **Assumptions before the trace:** <!-- A1, A2, ... -->",
            "- **Running example:** <!-- Named example reused across Sections 3-5 -->",
            "- **Causal Pipeline (`Input` $\\to$ `Internal State` $\\to$ `Decision / Output`):**",
            "  1. **Signal Ingestion:**",
            "  2. **Internal Aggregation / Transformation:**",
            "  3. **Gate / Threshold / Activation Evaluation:**",
            "  4. **Final Output Emission:**",
            "",
            "```mermaid",
            "flowchart TD",
            '    I["Inputs"] --> V{"Preconditions satisfied?"}',
            '    V -- "Yes" --> T["Core transformation"]',
            '    T --> O["Result"]',
            '    V -- "No" --> E["Invalid case / revise"]',
            "```",
            "",
            "#### Contrastive \"Is vs. Is Not\" Table",
            f"| Dimension | {title} (What It IS) | <Closest Lookalike> (What It Is NOT) |",
            "|---|---|---|",
            "| **Core Mechanism** | | |",
            "| **Parameter / Learning Nature** | | |",
            "| **Governing Invariant** | | |",
            "| **Primary Failure Mode** | | |",
            "| **Appropriate Use** | | |",
            "",
            "### Mathematical Intuition",
            "<!-- 1-2 paragraphs connecting operations to geometry/scale/dependence -->",
            "",
            "### Formal Equation & Complete Symbol Anatomy",
            "",
            "$$",
            "<Governing Display LaTeX Equation>",
            "$$",
            "",
            "| Symbol / Operator | Name & Physical Role | Tensor Shape / Domain / Units | Directional Sensitivity |",
            "|---|---|---|---|",
            "| $x_i$ | | | |",
            "",
            "#### Input-to-Output Behavior Table",
            "| Concrete Inputs | Intermediate Computation | Final Output | Physical / Logical Interpretation |",
            "|---|---|---|---|",
            "| | | | |",
            "",
            "- **Boundary Limits & Extreme Regimes:**",
            "  - **Zero Regime ($\\to 0$):**",
            "  - **Unit / Normalized Regime ($\\to 1$ / $-1$):**",
            "  - **Degenerate / Tie Regime:**",
            "  - **Asymptotic Regime ($\\to \\pm\\infty$):**",
            "",
            "<!-- SECTION: S4-PROOF -->",
            "## 4. Step-by-Step Mathematical Proof & Derivation (Zero Skips)",
            "",
            "1. **Step 1 (Base Axiom / Starting Definition):**",
            "   $$",
            "   <Starting definition>",
            "   $$",
            "   *Why this step holds:*",
            "",
            "<!-- SECTION: S5-CODE -->",
            "## 5. Executable Verification (Python & NumPy Implementation)",
            "",
            "```python",
            "# Self-contained verification matching the running example and boundary cases",
            "```",
            "",
            "<!-- SECTION: S6-QA-MASTERY -->",
            "## 6. Deep Conceptual & Analytical Q&A Mastery Set",
            "",
            "#### Question 1 — First-Principles Mechanism & Intuition",
            "",
            "> [!example]- Reveal Detailed Answer & Step-by-Step Breakdown",
            "> - **Direct Conclusion:**",
            "> - **First-Principles Explanation:**",
            "> - **Concrete Micro-Illustration:**",
            "",
            "<!-- SECTION: S7-SOURCES -->",
            "## 7. Common Traps, Primary Sources & Bridge",
            "",
            "> [!caution] Common Misconceptions & Anti-Patterns",
            "> - **_Avoid_:** <Misconception> $\\to$ **True Invariant:** <Correct invariant>",
            "",
            "### Primary Sources & Deep Links",
            "| Source | Direct External Deep Link | Vault Deep Link | Exact Claim / Equation Verified |",
            "|---|---|---|---|",
            "| | | | |",
            "",
            "**Bridge to Next Topic:**",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scaffold a 7-section Scriptorium deep note.")
    parser.add_argument("vault_path", nargs="?", help="Path to Obsidian vault.")
    parser.add_argument("--output", help="Vault-relative output path (prints to stdout if omitted).")
    parser.add_argument("--id", dest="note_id", help="Note YAML id (defaults to <topic-slug>-<number>).")
    parser.add_argument("--number", default="01", help="Subtopic number prefix (default: 01).")
    parser.add_argument("--title", required=True, help="Subtopic title.")
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

    note_id = args.note_id or f"{_slugify(args.topic)}-{args.number}"
    content = render_deep_note_skeleton(
        note_id=note_id,
        number=args.number,
        title=args.title,
        base_domain=args.base_domain,
        master_topic=args.master_topic,
        topic=args.topic,
        aliases=args.aliases,
        tags=args.tags,
        depends_on=args.depends_on,
        next_topic=args.next_topic,
    )

    if args.dry_run or not args.output:
        print(content, end="")
        return 0

    try:
        vault_root = resolve_vault_root(args.vault_path)
        if ".." in Path(args.output).parts:
            raise ValueError(f"Path traversal ('..') is not allowed: {args.output}")
        out_path = Path(args.output)
        if not out_path.is_absolute():
            out_path = vault_root / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if not is_within_vault(vault_root, out_path):
            raise ValueError(f"Output path escapes vault root: {args.output}")
        if out_path.exists() and not args.overwrite:
            raise FileExistsError(f"Refusing to overwrite existing note without --overwrite: {args.output}")
        out_path.write_text(content, encoding="utf-8")
        print(f"Scaffolded {out_path.relative_to(vault_root).as_posix()}")
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
