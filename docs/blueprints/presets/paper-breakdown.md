<!-- scaffold:preflight
Purpose: Deconstruct a primary research paper from bottleneck to formal mechanism, ablation audit, sanity verification, and threats to validity.
Parent Master: M7 (../formats/synthesis-revision.md) | Route: paper-breakdown (variant: paper_breakdown).
Activation Trigger: "paper breakdown" or standalone primary arXiv/DOI/OpenReview URL via /scribe-notes.
Inputs: Primary paper PDF/text + supplementary material, exact equation numbers, reported evaluation tables/ablations.
Dependencies: router.md, core/authoring_rules.md, core/math_gates.md, procedures/sourcing/source-fidelity.md.
Decision Rules: Attribute exact paper section/equation numbers; separate independent explanatory derivations visibly; flag unstated ablations honestly.
Failure Handling: Mark unavailable metrics or ablations '[ABLATION / RESULT ABSENT IN PAPER]'; never fabricate baselines or supplementary claims.
Validation: [verification-checklist.md](../../procedures/review/verification-checklist.md) and [source-fidelity.md](../../procedures/sourcing/source-fidelity.md).
-->

# Primary Research Paper Deconstruction, Derivation & Ablation Audit

- **Header Block:** Line-1 YAML Properties + `# Paper Breakdown: <Paper Title>` + `> [!abstract] Core Equations & Contribution Summary`.

## 1. What bottleneck was the field stuck on & what did this paper contribute? (Citation, Prior Wall & Breakthrough)

- `> [!info] Primary Paper Metadata`: Title, Authors, Venue/Year, Direct Paper URL/DOI, Code URL, Supplement availability.
- **Pre-Paper Bottleneck (`4–5` sentences):** Exact theoretical, methodological, or resource wall motivating this work.
- **Core Contribution & Scope (`3–4` sentences + 3 bullets):** Governing mechanism, primary invariant, and explicit out-of-scope boundaries.
- **Research Lineage:** Foundational prior work and verified downstream developments.

## 2. How does the proposed mechanism work & why do the equations hold? (Architecture, Equations & Derivations)

- **Mechanism Walkthrough & Visual Architecture:** Define one concrete **Named Running Example** with explicit input bounds/dimensions; trace data/control flow using an inspected local web architecture figure ([representations.md](../../procedures/authoring/representations.md)) + `2–3` sentence summary (never Mermaid or ASCII).
- **Equations & Zero-Skip Derivation (`math_level` `1–2`):** Pair numbered paper equations (`$$...$$`) with collapsible formula folds (`math_gates.md`), Symbol Anatomy, Input-to-Output Behavior table, and `*Why this step holds:*` derivations. Mark added non-author clarifications visibly:
  `> [!note] Explanatory Derivation (Distinct from Authors' Presentation in Section X)`

## 3. Do the experiments and ablations actually prove the claim? (Empirical Evaluation & Ablation Audit)

- **Primary Benchmarks:** Exact tables/figures, datasets, metrics, controls, and variance/compute budgets.
- **Ablation Audit Table:** `Ablated Factor | Setup & Control | Reported Metric & Delta | Causal Conclusion`
- Mark missing ablations or variance bounds `[ABLATION / RESULT ABSENT IN PAPER]`.

## 4. Can we verify the paper's core mechanism in minimal code? (Executable Sanity Check)

- Minimal runnable check on the Named Running Example confirming core dimensions/invariants (or structured manual thought-experiment verification for non-computational papers, labeled honestly).

## 5. Where does this method break & what came next? (Limitations, Legacy & Vault Connections)

- **Stated vs. Unstated Limitations:** Contrast author caveats against hidden assumptions and deployment bottlenecks.
- **Primary Sources & Section/Equation Verification Table.**

<!-- optional: history -->
## [OPTIONAL] Which earlier constraint explains this design? (Historical Evolution & Competing Paradigms)

<!-- Include only documented design lineage backed by inspected primary passages; delete cleanly otherwise. -->

- **Context / Analysis / Check:** Documented prior constraint, resulting paper choice, and primary-source verification status.

- **Contract Summary:** Verify claim attribution, zero-skip core derivations, ablation honesty, and [authoring_rules.md](../../../core/authoring_rules.md) / [math_gates.md](../../../core/math_gates.md) / [footer_widgets.md](../../../core/footer_widgets.md).
