# Variant: Formula Sheet

- **Purpose:** Produce a high-density mathematical/scientific equation reference preserving every symbol unit, dimension, and domain hypothesis.
- **Parent Master:** [M3 — Quick Reference & Cheat Sheet](../masters/quick-reference.md) (`formula_sheet`)
- **Activation Trigger:** `"formula sheet"`, `"cheat sheet for ... formulas"` via `/scribe-notes`.
- **Inputs & Dependencies:** Governing equations, verified units/shapes, applicability assumptions; [math_gates.md](../../../shared/math_gates.md), [source-fidelity.md](../../workflows/research/source-fidelity.md).
- **Execution Overrides:**
  1. Emit per formula: canonical `$$...$$`, compact inline symbol meanings (with units/dimensions/shapes), explicit **applicability conditions & hypotheses**, and one-line physical/mathematical meaning.
  2. Never strip smoothness, convexity, independence, or domain assumptions just to save space; review them in the final sheet.
  3. Under `R-S0` (`strict`), extract only formulas present in the supplied source with exact source locators.
- **Failure Handling & Validation:** Reject bare equations lacking units/conditions ([verification-checklist.md](../../workflows/validation/verification-checklist.md)).
