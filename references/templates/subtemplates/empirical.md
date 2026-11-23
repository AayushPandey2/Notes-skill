# Subtemplate: Empirical

- **ID:** `empirical` | **Registry alignment:** `research` (empirical studies, ML benchmarks, papers, economics, statistical/clinical evaluation) via [teaching_core.md](../../../shared/teaching_core.md).
- **Purpose:** Teach experimental findings, ablations, metrics, and research papers rigorously while separating illustrative fixtures from verified empirical measurements.
- **Trigger:** Research breakdown, benchmark evaluation, experimental methodology, or uncertainty analysis objectives (`TEACH-04`, `TEACH-05`, `TEACH-09`, `MATH-08`).
- **Preconditions:** Evaluation metrics, experimental setups, and baseline conditions are defined before comparing numerical performance.
- **Inputs:** Source claims/tables, datasets, metrics, protocols, uncertainty values (`SD`/`SE`/`CI`), and threats to validity.
- **Output Contract:** Method motivation, matched-protocol comparison, explicit uncertainty and limitation qualifiers, clearly labeled illustrative vs observed examples, and honest gaps (`[UNVERIFIED]`).
- **Execution Procedure:**
  1. Explain the research question and evaluation metric intuition before reporting metric numbers.
  2. Pair every metric claim with dataset, protocol, baseline, and variance/uncertainty metadata.
  3. Complete needed research figures through [representations.md](../../workflows/notes-creation/representations.md) and explain them; flag absent ablations explicitly.
- **Dependencies:** [research-engine.md](../../workflows/research/research-engine.md), [source-fidelity.md](../../workflows/research/source-fidelity.md), [teaching_core.md](../../../shared/teaching_core.md).
- **Review:** Check each numerical claim against its source location, dataset, metric, protocol, and uncertainty; label illustrative values.
- **Failure Behavior:** Reject unmatched benchmark comparisons, missing uncertainty classifications, or unlabeled synthetic data presented as empirical findings.
