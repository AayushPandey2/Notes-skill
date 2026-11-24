# Mathematical Reasoning & Formula-Fold Gates

## Purpose

Ensure every mathematical expression teaches meaning, dimensions, derivations, and numerical interpretation—bridging visuals and intuition into formalism via **Question → intuition → visual meaning → symbols → formula → calculation → interpretation → check**.

## Activation Trigger & Inputs

- **Activate when:** `math_depth >= 1`, knowledge type is `mathematical` or `scientific`, master is `M4`, or any displayed `$$...$$` block appears anywhere.
- **Inputs:** Concept objective, depth (`M0`–`M5` for deep notes; `math_level` `0`–`2` for source/compact routes), governing equations, symbol/unit/dimension specs, and the stable running example fixture.
- **Dependencies:** [core/teaching_core.md](teaching_core.md), [adaptive-engine.md](../docs/procedures/authoring/adaptive-engine.md#selection-and-depth).

## Execution Rules — Atomic Formula + Fold Contract

1. **Question & Intuition First:** Before introducing an equation, explain what question it answers. Never drop an advanced expression before motivating it or stack back-to-back equations without intervening explanation.
2. **Native Obsidian Delimiters:** Use `$...$` and separate-line `$$...$$` consistently with [authoring_rules.md](authoring_rules.md) (never copy `\(...\)` or `\[...\]` from external samples, and never leave raw LaTeX commands like `\frac` outside math delimiters).
3. **Visible Meaning + Collapsed Walkthrough:** Keep the central argument visible with folds closed, and place one immediately following `> [!note]- 📐 Understand this formula` callout beneath **every** displayed `$$...$$` equation (quoting every line, including blank separator lines with `>`). Cover applicable details inside that single fold without creating separate visible headings for pronunciation, symbols, or dimensions:
   - Question and purpose
   - Read-aloud interpretation
   - Symbols and indices
   - Types, shapes, units, and domains
   - Operations and their order
   - Assumptions (distinguishing **approximation**, **identity**, **assumption**, **empirical observation**, and **theorem**)
   - Non-obvious transformations / derivation
   - Worked calculation with explicit intermediate steps
   - Result interpretation (what it measures vs. what it does **not** establish)
   - Sanity checks and limitations
4. **One Canonical Calculation & No Nesting:** Keep one canonical worked calculation rather than duplicating it across sections. Keep arithmetic inside folds inline (`$...$`), emit sibling formula+fold blocks for distinct derivation steps rather than nesting callouts recursively, and introduce advanced notation only when necessary.

## Failure Handling & Review

Locally repair unprepared equations, stacked equations, missing/nested/generic folds, raw LaTeX outside delimiters, dimension mismatches, or uninterpreted numbers before verifying against [verification-checklist.md](../docs/procedures/review/verification-checklist.md).
