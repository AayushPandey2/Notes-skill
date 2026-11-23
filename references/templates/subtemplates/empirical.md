# Subtemplate: Empirical

- **Purpose:** Teach research papers, benchmarks, experimental studies, and statistical/clinical evaluations while separating illustrative fixtures from verified empirical evidence.
- **Activation conditions:** Paper breakdowns, benchmark evaluations, ablations, experimental methodology, or uncertainty analysis (`research`).
- **Required inputs:** Source claims/tables, datasets, metrics, experimental protocols, baselines, uncertainty values (`SD`/`SE`/`CI`), and threats to validity.

> **Authoring-agent image instruction:** Before drafting, identify the visual learning needs of each substantive concept. Acquire suitable images where they materially improve understanding. Inspect the saved images, then compose the explanation around their actual visible content. Do not treat image placement as an optional finishing step.

## Teaching Sequence

1. **Research question & metric intuition:** Explain what question the study asks and what each metric measures before reporting numbers.
2. **Protocol & baseline parity:** State dataset, splits, controls, and baseline conditions before comparing outcomes.
3. **Source-figure walkthrough:** Acquire and inspect key source figures, then explain axes, error bars, and comparisons via **Orient → Show → Explain → Work through → Connect**.
4. **Uncertainty & ablations:** Pair metric claims with variance/uncertainty and identify missing ablations or confounded variables.
5. **Validity & limits:** Bound conclusions by sample, protocol, and threats to internal/external validity.

## Obligations

- **Evidence expectations:** Cite exact source locators (page, section, table, figure); mark missing data `[UNVERIFIED]` and never present illustrative data as empirical findings.
- **Visual requirements:** Follow [representations.md](../../workflows/notes-creation/representations.md) using **Orient → Show → Explain → Work through → Connect**. Image opportunities: actual source figures, experimental setups, and reported benchmark/ablation plots; use Markdown tables for exact reported numbers.
- **Mathematical explanation requirements:** Explain metric definitions, loss objectives, or statistical tests through [math_gates.md](../../../shared/math_gates.md) when quantitative formulas appear.
- **Practical-example requirements:** Walk through one concrete reading of a reported result row or figure data point to show how the metric behaves.
- **Failure handling:** Reject unmatched benchmark comparisons, missing uncertainty qualifiers, or uninspected source figures; disclose inaccessible paywalled/missing artifacts honestly.
- **Completion checks:** Verify against [verification-checklist.md](../../workflows/validation/verification-checklist.md) — every claim locator-backed, illustrative vs observed separated, and source figures decoded.
