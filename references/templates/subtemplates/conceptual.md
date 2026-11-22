# Subtemplate: Conceptual

- **ID:** `conceptual` | **Registry alignment:** `conceptual`, `comparative` via [teaching_core.md](../../../shared/teaching_core.md).
- **Purpose:** Teach definitions, mental models, causal distinctions, and policy/design trade-offs clearly without forcing artificial equations or CS jargon.
- **Trigger:** Conceptual mastery, taxonomy, comparison, or decision-selection objectives (`TEACH-01`, `TEACH-02`, `TEACH-04`, `TEACH-08`).
- **Preconditions:** Unfamiliar foundational terms are bridged before relying on them (`TEACH-01`); analogies disclose breakdown boundaries (`CF-08`).
- **Inputs:** Target concept, prerequisite concepts, contrasting near-misses, concrete scenario examples, and domain context.
- **Output Contract:** Motivating problem, concrete scenario intuition, precise definitions, causal explanation of differences **before** summary tables, near-miss counterexamples, and explicit When-to-Use / When-Not-to-Use criteria.
- **Execution Procedure:**
  1. Open with why the concept matters and an accessible real-world scenario.
  2. Distinguish near-miss concepts causally in prose before compact comparison tables.
  3. Place misconception corrections at the exact point of ambiguity without assuming unverified formulas or code.
- **Dependencies:** `scriptorium/engines/pedagogy.py`, `scriptorium/engines/quality.py`, [teaching_core.md](../../../shared/teaching_core.md).
- **Validation:** `QualityEngine.evaluate_teaching()`, `QualityEngine.review_explanatory_clarity()` (`CF-01`..`CF-12`), `KnowledgeEngine.verify_claim_links()`.
- **Failure Behavior:** Reject table-only comparisons lacking causal explanation, unexplained jargon on beginner profiles, or fabricated formalism.
