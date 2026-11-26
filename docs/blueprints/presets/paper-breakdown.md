# Preset: Research-Method-Adaptive Paper Breakdown (`M7` / `paper_breakdown`)

- **Parent Master:** [M7 — Synthesis & Revision](../formats/synthesis-revision.md) (`single_artifact`).
- **Activation Trigger:** `"paper breakdown"` or standalone primary arXiv/DOI/OpenReview/journal URL via `/scribe-notes`.

## Execution Overrides
1. **Select Analysis by Research Methodology** (never force ML architectures or ablations onto non-ML papers):
   - *Mathematical:* Definitions, theorem hypotheses, proof structure, consequences & counterexamples.
   - *Empirical / Scientific:* Study design, measurements, estimation, uncertainty, confounders & bias.
   - *ML / Computational:* Formulation, benchmarks, baselines, ablations, generalization & compute/reproducibility.
   - *Review / Meta-Analysis:* Inclusion criteria, evidence synthesis, publication bias & scope limits.
   - *Historical:* Archives, primary vs. secondary sources, context & historiography.
   - *Qualitative:* Sampling, coding, interpretation, reflexivity & credibility.
   - *Engineering:* Requirements, architecture/design, validation, tolerances & operational constraints.
2. **Method-Neutral Evidence Evaluation:** Use **"How strongly does the evidence support the claim?"** (empirical experiments support claims under stated conditions rather than "proving" them mathematically). Mark absent ablations/controls/variance bounds `[ABSENT IN PAPER]`.
3. **Attribution & Non-Author Clarifications:** Cite exact paper section/equation/figure numbers; mark independent explanatory derivations visibly as `> [!info] Explanatory Derivation (Distinct from Authors' Presentation in Section X)`.
