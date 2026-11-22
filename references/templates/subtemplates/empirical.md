# Subtemplate: Empirical

- **ID:** `empirical` | **Registry alignment:** `research` (empirical studies, ML benchmarks, papers, economics, clinical/statistical evaluation).
- **Entry & Scope:** Selected internally through `/scribe-notes` for standalone notes or hierarchical collection children; respects resolved interactive preferences, source policy, and F02 depth allocation.
- **Compatible Masters:** `M1`, `M2`, `M3`, `M6`, `M7` (`paper_breakdown`, `comparison_guide`, `quick_summary`).
- **Modules:**
  - **Required (depth-gated):** `experiment`, `definitions`, `limitations` (threats to validity & uncertainty), `source_attribution` (ARRIE `empirical_result`).
  - **Optional:** `mathematics`, `comparison` (matched-protocol baselines), `visual_reasoning`, `F10` cross-note synthesis, `F12` evaluation outcomes.
  - **Excluded:** Invented benchmark figures, unmatched protocol rankings, or unverified ablation claims.
- **Core Adaptations:**
  - Always preserve dataset/sample, baseline, evaluation metric, experimental setup, uncertainty/variance, and threats to validity alongside any numerical claim.
  - Flag missing ablations or unmeasured claims honestly (`[UNVERIFIED]`, `[ABLATION / RESULT ABSENT IN PAPER]`) and distinguish illustrative synthetic data from observed measurements.
- **Validation:** `KnowledgeEngine.verify_claim_links()`, `KnowledgeEngine.uncertainty`, `QualityEngine.check_representations()`.
