# Variant: Formula Sheet

- **Purpose:** Produce a high-density mathematical/scientific equation reference preserving every symbol unit, dimension, and domain hypothesis.
- **Parent Master:** [M3 — Quick Reference & Cheat Sheet](../formats/quick-reference.md) (`formula_sheet`)
- **Activation Trigger:** `"formula sheet"`, `"cheat sheet for ... formulas"` via `/scribe-notes`.
- **Inputs & Dependencies:** Governing equations, verified units/shapes, applicability assumptions; [math_gates.md](../../../core/math_gates.md), [source-fidelity.md](../../procedures/sourcing/source-fidelity.md).
- **Execution Overrides:**
  1. Follow [math_gates.md](../../../core/math_gates.md) for native `$...$`/`$$...$$` delimiters, notation stability, and reasoning distinctions, while keeping per-formula explanations concise for `M3` density: emit canonical `$$...$$`, compact inline symbol meanings (with units/dimensions/shapes), explicit **applicability conditions & hypotheses**, and one-line physical/mathematical meaning.
  2. Never strip smoothness, convexity, independence, or domain assumptions just to save space; review them in the final sheet.
  3. Under `R-S0` (`strict`), extract only formulas present in the supplied source with exact source locators.
- **Failure Handling & Validation:** Reject bare equations lacking units/conditions ([verification-checklist.md](../../procedures/review/verification-checklist.md)).
