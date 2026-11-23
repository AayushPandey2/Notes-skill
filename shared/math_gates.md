# Mathematical Reasoning & Formula-Fold Gates

## Purpose

Ensure every mathematical expression across Scriptorium notes teaches meaning, dimensions, derivations, and numerical computation cleanly—never dropping opaque symbolic formulas onto beginners.

## Activation Trigger & Inputs

- **Activate when:** `math_depth >= 1`, knowledge type is `mathematical` or `scientific`, master is `M4`, or any displayed `$$...$$` block appears anywhere (main body, worked solutions, assessments, tables, or video/source notes).
- **Inputs:** Concept objective, depth (`M0`–`M5` for deep notes; `math_level` `0`–`2` for source/compact routes), governing equations, symbol/unit/dimension specs, and concrete numerical fixtures.
- **Dependencies:** [shared/teaching_core.md](teaching_core.md), [adaptive-engine.md](../references/workflows/notes-creation/adaptive-engine.md#selection-and-depth).

## Execution Rules — Atomic Formula + Fold Contract (`M01`–`M14`)

1. **Prepare Before Display:** Orient the learner in plain language before any `$$...$$` block; never open a conceptual section with a naked equation or dump back-to-back equations without intervening explanation.
2. **Mandatory 12-Stage Collapsible Walkthrough:** Place one Obsidian-native collapsed callout directly beneath **every** displayed `$$...$$` equation:
   - Heading: `> [!note]- 📐 Understand this formula` (preceding narrative remains smooth when all folds are closed).
   - Canonical 12-stage headings (apply relevant stages in depth; omit genuinely inapplicable stages without generic filler, and quote blank separator lines with `>`):
     1. `### 1. Why this formula exists`
     2. `### 2. Formula components`
     3. `### 3. Symbol-by-symbol breakdown`
     4. `### 4. How to read it`
     5. `### 5. Prerequisites`
     6. `### 6. Numerical example`
     7. `### 7. Visual interpretation`
     8. `### 8. Parameter behavior`
     9. `### 9. Derivation`
     10. `### 10. Python implementation`
     11. `### 11. Limitations and mistakes`
     12. `### 12. Mental model and recall`
3. **Anti-Recursive Nesting & Parity:** Keep supporting arithmetic inside formula folds inline (`$...$`); emit separate sibling formula+fold blocks for distinct derivation steps rather than nesting callouts recursively, bundling unrelated equations together, converting complex math into unreadable inline text, or forcing irrelevant filler tables.
4. **Source Attribution:** Distinguish derivation steps present in a supplied source/video from independently added explanatory bridges.

## Worked Application Protocol (`Step 1`–`12`)

Solve every quantitative problem systematically: State Question & Objective → Method & Assumptions → Symbols & Units → Governing Formula + Fold → Declared Numerical Inputs → Explicit Intermediate Arithmetic → Final Result → Contextual Interpretation → Sanity Check (magnitude/sign/units/limits) → Common Mistakes → Pattern Generalization.

## Failure Handling & Review

- Flag and locally repair unprepared formulas, stacked equations, missing/nested/generic folds, dimension mismatches, or arithmetic errors before finishing.
- Verify every displayed `$$...$$` block directly against [verification-checklist.md](../references/workflows/validation/verification-checklist.md).
