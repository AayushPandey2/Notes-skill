# Subtemplate: Historical

- **ID:** `historical` | **Registry alignment:** `historical`.
- **Entry & Scope:** Selected internally through `/scribe-notes` for standalone notes or hierarchical collection children; respects resolved interactive preferences, source policy, and F02 depth allocation.
- **Compatible Masters:** `M1`, `M2`, `M3`, `M6`, `M7` (`revision_pack`, `concept_map`, `quick_summary`).
- **Modules:**
  - **Required (depth-gated):** `history`, `definitions`, `limitations` (evidence limits & competing interpretations), `source_attribution` (ARRIE `historical_claim`).
  - **Optional:** `visual_reasoning` (chronological timelines), `comparison`, `cross_topic_connections` (`P08`), `F12` explanation/evaluation outcomes.
  - **Excluded:** Mathematical derivations, complexity bounds, loop invariants, and runnable code.
- **Core Adaptations:**
  - Establish dated context, verifiable chronology, primary records/publications, causes, and consequences.
  - Strictly distinguish documented events and dates from later causal attribution or competing scholarly interpretations; never collapse rival interpretations into false consensus.
- **Validation:** `KnowledgeEngine.verify_claim_links()`, `KnowledgeEngine.uncertainty`, `QualityEngine.review_explanatory_clarity()`.
