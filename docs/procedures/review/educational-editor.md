# Cognitive Load, Editorial Quality & Reader Accessibility

## Purpose

Review substantive notes from the **reader's perspective** so prose is clear, learnable, and accessible across laptops, tablets, and plain Obsidian without plugins—strictly honoring the **Educational & Mathematical Depth Preservation Contract** in [theory_quality_contract.md](../../../core/theory_quality_contract.md) (never trimming unique educational information, consequential mathematical derivation steps, intermediate transformations, or formula-construction explanations merely for length). Apply **Three-Level Progressive Disclosure** ([authoring_rules.md](../../../core/authoring_rules.md)): keep essential intuition, definitions, governing mechanisms, assumptions, and failure conditions in the *Main reading path* (visible prose); keep consequential intermediate equations in the main path, move full derivations as appropriate, extended algebra, optional formal proofs, line-by-line code walkthroughs, and extra calculations to *Expandable detail*; and link deep prerequisites or related topics as *Linked reference*.

## 1. Editorial Dimensions & Productive vs. Redundant Repetition

Distinguish **redundant repetition** (restating a definition verbatim immediately after explaining it $\to$ merge or link to canonical home) from **productive retrieval repetition** (deliberate brief recaps or cross-context comparisons that aid memory $\to$ preserve).

| Editorial Defect | Targeted Repair |
|---|---|
| **Repeated definition** | Merge or refer to canonical home |
| **Dense / overloaded passage** | Split at logical boundary; introduce notation/terms progressively |
| **Structural fragmentation** | Combine closely related micro-sections into one coherent flow |
| **Essential reasoning hidden in folds** | Restore core explanation to visible prose (notes must stay readable with all callouts collapsed) |
| **Repeated callouts** | Consolidate into purposeful callouts |
| **False depth / artificial tone** | Replace AI filler (`"We now..."`) with causal mechanism; never shorten proofs for length |

**Paragraph Contribution Test:** Every substantive paragraph must perform at least one primary teaching function—**Motivation**, **Definition**, **Intuition**, **Mechanism**, **Justification**, **Example**, **Interpretation**, **Qualification**, **Transition**, or **Synthesis**. Any paragraph performing none of these functions (e.g., pure restatement, decorative throat-clearing, or empty recap) must be tightened, merged, or cut.

## 2. Reader Experience & Accessibility

- Read the mathematical prose with formula folds closed. Split dense inline algebra into displays and use prose to connect the operations. Merge adjacent folds when they serve the same result.
- Split overly wide tables into focused single-question tables; keep code and displayed math lines readable without horizontal overflow.
- Provide meaningful figure captions and textual equivalents; never rely solely on color to distinguish curves or states.
- Ensure navigation (`[[#Heading]]` TOC, callouts, wikilinks) works in standard Obsidian without requiring third-party plugins.

Read one whole learning unit as the intended learner. Separate crowded paragraphs at changes in intellectual task. Expand any heading that merely names a mechanism the reader must reconstruct. Check that each figure earns its space and each worked contrast changes the intended outcome or exposes an invariant. Repair supporting examples, captions, and formulas when the underlying explanation changes.
