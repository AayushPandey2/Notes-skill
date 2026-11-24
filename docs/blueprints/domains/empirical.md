# Subtemplate: Empirical

- **Purpose:** Realize the [12 teaching layers](../../../core/teaching_core.md) for research papers, benchmarks, empirical studies, and statistical evaluations while distinguishing observed evidence from inference.
- **Activation conditions:** Paper breakdowns, benchmark evaluations, ablations, experimental methodology, or uncertainty analysis (`research`).
- **Expected inputs:** Research question, population/sample, source claims/tables with locators, metrics, protocols, baselines, uncertainty (`SD`/`SE`/`CI`), and validity threats.

> **Authoring-agent image instruction:** Before drafting, identify the visual learning needs of each substantive concept. Acquire suitable images where they materially improve understanding. Inspect the saved images, then compose the explanation around their actual visible content. Do not treat image placement as an optional finishing step.

- **Realizing the 12 Teaching Layers:** Frame the empirical question and why it matters (Layer 1) → build intuition for what the metric and protocol actually measure (Layers 2–3) → unpack sample, baseline, and uncertainty terms (Layers 4–5) → decode actual source figures and reported plots (Layer 6) → trace experimental mechanism and formal metric definitions (Layers 7–8) → walk through one concrete reported row/point and interpret what it establishes (Layer 9) → analyze confounders, missing ablations, replication limits, and alternative explanations (Layers 10–11) → test critical reading independently (Layer 12).
- **Visual opportunities:** Follow [representations.md](../../procedures/authoring/representations.md) using actual inspected source figures, experimental setups, and reported benchmark/ablation plots, plus Markdown tables for exact reported values.
- **Formalism, evidence & failure handling:** Explain metrics/statistical tests via [math_gates.md](../../../core/math_gates.md) when quantitative; cite exact locators (`[UNVERIFIED]` for missing data); never present illustrative fixtures or correlation as causal empirical proof; repair unmatched comparisons via [verification-checklist.md](../../procedures/review/verification-checklist.md).
