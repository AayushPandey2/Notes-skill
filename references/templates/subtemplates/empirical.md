# Subtemplate: Empirical

- **Purpose:** Teach research papers, benchmarks, experimental studies, and statistical/clinical evaluations rigorously while separating illustrative fixtures from verified empirical evidence.
- **Activation conditions:** Paper breakdowns, benchmark evaluations, ablations, experimental methodology, or uncertainty analysis (`research`).
- **Expected inputs:** Research question, population/sample, source claims/tables with locators, metrics, experimental protocols, baselines, uncertainty values (`SD`/`SE`/`CI`), and threats to validity.

> **Authoring-agent image instruction:** Before drafting, identify the visual learning needs of each substantive concept. Acquire suitable images where they materially improve understanding. Inspect the saved images, then compose the explanation around their actual visible content. Do not treat image placement as an optional finishing step.

- **Teaching progression:** Frame the research question and what each metric actually measures → define population/sample, protocol, and baseline parity → decode actual source figures via the six-phase visual narrative → interpret results alongside variance/uncertainty and missing ablations → state alternative explanations, replication status, and what cannot be concluded.
- **Necessary prerequisite bridges:** Explain metric intuition, baseline conditions, and statistical uncertainty terms before reporting numbers.
- **Visual opportunities:** Follow [representations.md](../../workflows/notes-creation/representations.md) using the six-phase visual narrative. Image opportunities: actual source figures, experimental setups, and reported benchmark/ablation plots; use Markdown tables for exact reported numbers.
- **Formalism appropriate to the knowledge type:** Explain metric definitions, loss functions, or statistical tests through [math_gates.md](../../../shared/math_gates.md) when quantitative formulas appear.
- **Worked-example requirements:** Walk through one concrete reading of a reported table row or figure point to show what the metric establishes and what it leaves open.
- **Evidence requirements:** Cite exact source locators (page, section, table, figure); mark missing data `[UNVERIFIED]`, never invent data, and never treat correlation or illustrative fixtures as empirical findings.
- **Practice and mastery checks:** Include metric-interpretation, figure-reading, and validity-critique questions with collapsed answers.
- **Failure handling:** Locally repair unmatched benchmark comparisons, missing uncertainty qualifiers, or uninspected source figures via [verification-checklist.md](../../workflows/validation/verification-checklist.md).
