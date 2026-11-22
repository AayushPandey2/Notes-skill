# Mathematical Reasoning & Formula-Fold Gates

## Purpose

Ensure every mathematical expression across Scriptorium notes teaches meaning, dimensions, derivations, and numerical computation cleanly—never dropping opaque symbolic formulas onto beginners.

## Activation Trigger & Inputs

- **Activate when:** `math_depth >= 1`, knowledge type is `mathematical` or `scientific`, master is `M4`, or any displayed `$$...$$` block appears anywhere (main body, worked solutions, assessments, tables, or video/source notes; `T10`–`T11`, `MATH-01`–`MATH-10`).
- **Inputs:** Concept objective, depth (`M0`–`M5` for deep notes; `math_level` `0`–`2` for source/compact routes), governing equations, symbol/unit/dimension specs, and concrete numerical fixtures.
- **Dependencies:** `scriptorium/engines/mathematics.py` (`render_formula_component`, `validate_formula_folds`, `check_dimension_compatibility`, `build_worked_solution`, `verify_numerical_trace`), [shared/teaching_core.md](teaching_core.md), [adaptive-engine.md](../references/workflows/notes-creation/adaptive-engine.md#selection-and-depth).

## Execution Rules — Atomic Formula + Fold Contract (`M01`–`M14`)

1. **Prepare Before Display:** Orient the learner in plain language before any `$$...$$` block; never open a conceptual section with a naked equation or dump back-to-back equations without intervening explanation.
2. **Mandatory Collapsible Walkthrough:** Place one native folded callout directly beneath **every** displayed `$$...$$` equation using the single canonical builder (`render_formula_component`):
   - Heading: `> [!example]- Understand this formula step by step` (preceding narrative stays smooth when all folds are closed).
   - Adaptive elements (`M01`–`M14`): Purpose → Spoken reading → Every symbol/subscript/operator → Object types, SI units, and explicit shape compatibility (`(m×k)(k×n)`) → Expanded operations → Evaluation order → Non-obvious derivation/chain-rule/mask/scaling reasoning & assumptions → Meaningful declared numerical calculation (zero `"substitute the values"` filler; use distinct non-square numbers exposing axis/order bugs) → Interpretation & conditions → Misconception check.
3. **Anti-Recursive Nesting & Parity:** Keep supporting arithmetic inside formula folds inline (`$...$`); emit separate sibling formula+fold blocks for distinct derivation steps rather than nesting callouts recursively, bundling unrelated equations together, converting complex math into unreadable inline text, or forcing irrelevant constant/infinity filler tables.
4. **Source Attribution:** Distinguish derivation steps present in a supplied source/video from independently added explanatory bridges.

## Worked Application Protocol (`Step 1`–`12`)

Solve every quantitative problem systematically: State Question & Objective → Method & Assumptions → Symbols & Units → Governing Formula + Fold → Declared Numerical Inputs → Explicit Intermediate Arithmetic → Final Result → Contextual Interpretation → Sanity Check (magnitude/sign/units/limits) → Common Mistakes → Pattern Generalization.

## Failure Handling & Validation

- **Failure Handling:** Flag and locally repair unprepared formulas (`MATH-DECON-01`), stacked equations (`MATH-DECON-02`), missing/nested folds, dimension mismatches, or unverified arithmetic before publication.
- **Validation:** Run `validate_formula_folds`, `verify_math_deconstruction`, and `verify_numerical_trace` (`scriptorium/engines/mathematics.py`) alongside `scripts/validate_note.py` (`MATH-01`–`MATH-10`).
