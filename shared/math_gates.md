# Mathematical Reasoning & Formula-Fold Gates

## Purpose

Ensure every mathematical expression teaches meaning, dimensions, derivations, and numerical interpretation—bridging visuals and intuition into formalism via **Question → intuition → visual meaning → symbols → formula → calculation → interpretation → check**.

## Activation Trigger & Inputs

- **Activate when:** `math_depth >= 1`, knowledge type is `mathematical` or `scientific`, master is `M4`, or any displayed `$$...$$` block appears anywhere.
- **Inputs:** Concept objective, depth (`M0`–`M5` for deep notes; `math_level` `0`–`2` for source/compact routes), governing equations, symbol/unit/dimension specs, and the running example fixture.
- **Dependencies:** [shared/teaching_core.md](teaching_core.md), [adaptive-engine.md](../references/workflows/notes-creation/adaptive-engine.md#selection-and-depth).

## Execution Rules — Atomic Formula + Fold Contract

1. **Question & Intuition First:** Never drop an advanced expression before explaining what problem it solves. Orient the learner in plain language (and visual meaning where helpful) before any `$$...$$` block; never stack back-to-back equations without intervening explanation.
2. **Native Obsidian Delimiters:** Use `$...$` and separate-line `$$...$$` consistently with [authoring_rules.md](authoring_rules.md) (never copy `\(...\)` or `\[...\]` from external samples, and never leave raw LaTeX commands like `\frac` outside math delimiters).
3. **Visible Meaning + Collapsed Walkthrough:** Keep visible prose understandable with folds closed, and place an immediately following `> [!note]- 📐 Understand this formula` callout beneath **every** displayed `$$...$$` equation covering relevant items without generic filler (and quoting every line, including blank separator lines with `>`):
   - Purpose (`1. Why this formula exists`)
   - Components (`2. Formula components`)
   - Symbols, types, dimensions, or units (`3. Symbol-by-symbol breakdown`)
   - Read-aloud interpretation (`4. How to read it`)
   - Prerequisites & assumptions (`5. Prerequisites & assumptions`)
   - Worked calculation with explicit intermediate steps (`6. Numerical example`)
   - Visual/parameter intuition (`7. Visual & parameter interpretation`)
   - Non-obvious transformations / derivation (`8. Derivation`)
   - Code correspondence when relevant (`9. Implementation`)
   - Meaning of result, sanity check, and limitations (`10. Interpretation, sanity check & limits`)
   - Mental model & recall (`11. Mental model & recall`)
4. **Anti-Recursive Nesting & Honesty:** Keep supporting arithmetic inside formula folds inline (`$...$`); emit separate sibling formula+fold blocks for distinct derivation steps rather than nesting callouts recursively. Distinguish source derivations from added explanatory bridges.

## Worked Application & Interpretation Protocol

Solve quantitative problems systematically: **Question & Objective → Method & Assumptions → Symbols & Units → Governing Formula + Fold → Declared Inputs → Explicit Intermediate Arithmetic → Final Result → Careful Interpretation (what the result measures and what it does NOT establish) → Sanity Check (magnitude/sign/units/limits) → Common Mistakes → Pattern Generalization**.

## Failure Handling & Review

Locally repair unprepared equations, stacked equations, missing/nested/generic folds, raw LaTeX outside delimiters, dimension mismatches, or uninterpreted numbers before verifying against [verification-checklist.md](../references/workflows/validation/verification-checklist.md).
