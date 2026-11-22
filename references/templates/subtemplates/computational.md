# Subtemplate: Computational

- **ID:** `computational` | **Registry alignment:** `programming`, `algorithmic`, `architectural`, `procedural` (`C0–C5` depth via [teaching_core.md](../../../shared/teaching_core.md) and [adaptive-engine.md](../../workflows/notes-creation/adaptive-engine.md)).
- **Purpose:** Teach algorithms, data structures, code pipelines, and architectures by connecting intuition, state transitions, equations, and executable verification.
- **Trigger:** Objectives involving code, algorithms, invariants, state machines, complexity bounds, preprocessing, or debugging (`TEACH-03`, `MATH-03`, `MATH-05`).
- **Preconditions:** Intuition and algorithm invariants are established before showing implementation code (`P10`, `EIS-05`).
- **Inputs:** Problem contract, bounds/assumptions, target language/stack, equation-to-code variable map, and edge-case fixtures.
- **Output Contract:** Clean baseline-to-optimal intuition, unambiguous symbol-to-variable mapping, step-by-step trace table on concrete non-trivial inputs, runnable self-contained code (`C2+`) with honest execution tier, and explicit failure/complexity limits.
- **Execution Procedure:**
  1. Clarify the exact input/output contract, shape expectations, and motivating bottleneck.
  2. Trace state transitions on small asymmetric concrete inputs before full implementation.
  3. Map every mathematical term (e.g., dot product, scaling, loss) to exact code lines and explain why steps like feature scaling or array orientation matter.
  4. Verify syntax/execution via `plan_notes.py verify-runtimes` and report verbatim status (`executed`, `tests_passed`, or `static verification (not executed)`).
- **Dependencies:** `scriptorium/engines/pedagogy.py`, `scripts/plan_notes.py`, [teaching_core.md](../../../shared/teaching_core.md).
- **Validation:** `scripts/plan_notes.py verify-runtimes`, `QualityEngine.check_representations()`, `QualityEngine.validate_master(..., "M5")`.
- **Failure Behavior:** Block fabricated execution logs, untrusted source execution, or unmapped equations, and repair missing edge/invariant steps locally.
