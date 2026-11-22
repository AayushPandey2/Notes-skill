# Subtemplate: Historical

- **ID:** `historical` | **Registry alignment:** `historical` via [teaching_core.md](../../../shared/teaching_core.md).
- **Purpose:** Explain historical sequences, primary evidence, structural causes, consequences, and historiographical debate without false determinism or forced math/code.
- **Trigger:** Historical analysis, institutional evolution, or chronology-centered learning objectives (`TEACH-02`, `TEACH-03`, `TEACH-04`, `TEACH-07`).
- **Preconditions:** Dated context and primary-source scope precede causal interpretation; competing scholarly accounts remain clearly separated.
- **Inputs:** Chronological events, actors/institutions, verified primary/secondary sources, causal hypotheses, and contested evidence gaps.
- **Output Contract:** Contextual background, verified timeline, primary-evidence-grounded narrative, explicitly qualified causal analysis, and competing scholarly interpretations.
- **Execution Procedure:**
  1. Establish historical problem/context before events unfold.
  2. Sequence documented chronology cleanly using prose (plus Mermaid timelines only when sequence density warrants).
  3. Distinguish primary historical facts from retrospective causal arguments and avoid imposing mathematical/algorithmic templates.
- **Dependencies:** `scriptorium/engines/research.py`, `scriptorium/engines/knowledge.py`, [teaching_core.md](../../../shared/teaching_core.md).
- **Validation:** `KnowledgeEngine.verify_claim_links()`, `QualityEngine.evaluate_teaching()`, `QualityEngine.review_explanatory_clarity()`.
- **Failure Behavior:** Flag unsupported causal assertions (`EIS-SPINE-002`), collapsed scholarly disputes, or forced technical jargon.
