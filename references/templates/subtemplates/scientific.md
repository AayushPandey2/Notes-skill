# Subtemplate: Scientific

- **ID:** `scientific` | **Registry alignment:** `scientific` (physics, chemistry, biology, engineering) integrated with [teaching_core.md](../../../shared/teaching_core.md).
- **Purpose:** Ground natural-science laws and empirical mechanisms in physical intuition, units, dimensional balance, approximation regimes, and inspected figures.
- **Trigger:** Objectives explaining physical phenomena, causal natural mechanisms, experimental measurements, or equations carrying physical units (`MATH-01`, `MATH-10`, `TEACH-02`, `TEACH-05`).
- **Preconditions:** Physical intuition and observable scenario precede symbolic laws; units and coordinate conventions are explicit.
- **Inputs:** Physical phenomenon, governing relations, dimensional units, approximation conditions, experimental bounds, and web-image search queries.
- **Output Contract:** Intuitive mechanism, unit-consistent equations (`M05`, `M11`), concrete worked calculation with units, web-acquired figures under `assets/scriptorium/<slug>/` with reading guides, and explicit validity regimes.
- **Execution Procedure:**
  1. Motivate the observable phenomenon before introducing physical laws or differential equations.
  2. Define every physical constant/variable with SI or domain units and verify dimensional balance (`check_dimension_compatibility`).
  3. Acquire real schematic/plot assets via web image research (`T06`–`T09`, zero programmatic SVG generation) and walk the reader through labels and physical meaning.
  4. Separate observed measurements and uncertainties from idealized assumptions.
- **Dependencies:** `scriptorium/engines/mathematics.py`, `scriptorium/engines/composition/lavia.py`, [representations.md](../../workflows/notes-creation/representations.md).
- **Validation:** `QualityEngine.check_representations()`, `F09` unit consistency, `QualityEngine.evaluate_teaching()`, `KnowledgeEngine.verify_claim_links()`.
- **Failure Behavior:** Reject inconsistent units, fabricated experimental curves/SVGs, or unlabeled approximations; surface unmet visual obligations honestly.
