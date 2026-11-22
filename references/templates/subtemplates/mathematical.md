# Subtemplate: Mathematical

- **ID:** `mathematical` | **Registry alignment:** `mathematical` (`M0–M5` depth via [teaching_core.md](../../../shared/teaching_core.md), [adaptive-engine.md](../../workflows/notes-creation/adaptive-engine.md), and [math_gates.md](../../../shared/math_gates.md)).
- **Purpose:** Transform compact equations, derivations, and numerical methods into beginner-accessible, step-by-step understanding without sacrificing rigor.
- **Trigger:** Learning objectives involving formulas, symbols, vector/matrix operations, optimization objectives, derivatives, probability, or proofs (`MATH-01`–`MATH-10` via `scriptorium/triggers.py`).
- **Preconditions:** Concept orientation and starting intuition precede formal equations (`TEACH-02`); prerequisites bridged locally (`TEACH-01`).
- **Inputs:** Concept objective, learner level, governing equation(s), symbol metadata, operand dimensions/units, and declared synthetic inputs when applicable.
- **Output Contract:** Prose applying `M01`–`M14` proportionally (`scriptorium/engines/mathematics.py`): purpose, natural pronunciation, symbol inventory (subscripts, superscripts, transposes, operators), object types, explicit shape compatibility, expanded elementary form, declared numerical substitution with intermediate arithmetic, contextual interpretation, sanity check, and misconception guard.
- **Execution Procedure:**
  1. Prepare the motivating problem and intuitive mental model before any `$$` display equation.
  2. Call `Mathematics.detect_equation_features` / `check_dimension_compatibility` to select active `M01`–`M14` obligations and verify shapes.
  3. Synthesize symbol breakdown, expanded form, and `Step 1–12` worked numerical steps cleanly into continuous prose (avoiding equation dumping or duplicated definitions).
- **Dependencies:** `scriptorium/engines/mathematics.py`, `scriptorium/engines/pedagogy.py`, [teaching_core.md](../../../shared/teaching_core.md), [math_gates.md](../../../shared/math_gates.md).
- **Validation:** `PedagogyEngine.verify_math_teaching()`, `PedagogyEngine.verify_trace()`, `PedagogyEngine.validate_worked_problem()`, `F09` `CollectionTerminologyRegistry.validate_consistency()`.
- **Failure Behavior:** Reject unprepared formula drops (`MATH-DECON-01`), back-to-back equation dumps (`MATH-DECON-02`), dimension mismatches, or unverified arithmetic steps and emit targeted local repairs.
