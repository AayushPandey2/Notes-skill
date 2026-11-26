# Teaching upgrade matched comparison

Both revisions were evaluated on 12 focused teaching prompts, evals 50–61, with one Codex-generated output per prompt and revision. The baseline was `34c7ee4`. The revised runs used the updated canonical teaching and runtime policies. Both configurations received identical prompts, tool constraints, and learner descriptions. A separate reviewer graded notes without revision labels.

Both versions passed **24 of 24 criteria**. The criteria primarily discriminate mathematical correctness and basic explanatory coverage. They did not distinguish the versions at that level. The review below describes observed differences in particular passages. The anonymous A/B order alternated by case.

| Topic | A | B | Blind reviewer observation |
|---|---:|---:|---|
| knn-weighted-vote | 2/2 | 2/2 | A is compact. B makes the reversal easier to scan with a table and carries the tie through normalization in its checkpoint. |
| svm-margin | 2/2 | 2/2 | A starts with an accessible 2D example and tests a deliberate rescaling of the same planes. B derives the width first and checks how holding the canonical levels fixed changes the width. |
| logistic-tail | 2/2 | 2/2 | Both trace the lost residual clearly. A makes the underflow limit concrete at score 1000. B names its rounding assumption, describes the limit qualitatively, and also flags overflow for large negative scores. |
| pca-projection | 2/2 | 2/2 | A explicitly returns from the general result to the horizontal eigendirection in the main text. B explains the divisor convention and puts the diagonal covariance calculation in the checkpoint. |
| backprop-chain | 2/2 | 2/2 | A presents both gradient products together and checks how zero loss sensitivity propagates. B traces each path separately and tests how a zero local derivative blocks only one gradient. |
| rust-ownership | 2/2 | 2/2 | A offers a runnable move snippet with the failure commented out and tests last-use behavior. B clearly marks its intentionally failing line and tests an outliving reference, though its final process note interrupts the lesson. |
| virtual-memory | 2/2 | 2/2 | A keeps the trace focused by explicitly assuming a hardware walker. B spells out equal page and frame sizes and explains how a software-filled TLB can also resolve a miss with the mapping already present. |
| binary-search | 2/2 | 2/2 | Both tables are clear. A is more explicit about why the qualifying branch works and when the answer sits past the array. B quickly separates a lower-bound result from checking for an exact match. |
| rc-circuit | 2/2 | 2/2 | A is more compact and checks voltage at the original time after doubling capacitance. B shows the integration limits and current mechanism more explicitly and checks the voltage at the rescaled time constant. |
| newton-raphson | 2/2 | 2/2 | A demonstrates a nonzero but shallow slope with an overshoot to 100.005. B flows directly from the general derivation to the requested step and tests the zero-slope endpoint. |
| database-transactions | 2/2 | 2/2 | A supplies a concrete SQL pattern and notes its concurrency assumptions. B’s table makes the overwrite easy to see, and its checkpoint illustrates why locking only the final write can fail. |
| opportunity-cost | 2/2 | 2/2 | A spells out the rankings and compares two nonmonetary costs with the wage fixed. B uses a concrete dollar amount and recovery benefits to make the monetary and nonmonetary examples easy to distinguish. |

The new suite exercised 12 subject contexts within one runtime. These runs did not measure learner outcomes, long-document consistency, generation variability, token or timing cost, live Obsidian rendering or native image acquisition. The illustrated KNN fixture tests the separate visual pathway with inspected local assets. The Rust examples were statically reviewed.

## Behavioral regressions

| Eval | Observed result |
|---|---|
| 62 — Original KNN note | Identified compressed mechanisms, premature notation and missing geometry. Preserved exact voting and regression calculations and qualified the unavailable linked companions. The audit's section references had a Markdown backtick formatting defect. |
| 63 — Circle area | Distinguished the correct derivative from its incomplete justification, inspected and rejected an irrelevant raster, and replaced the radius-1 versus diameter-2 comparison with radii 1 and 2. |
| 64 — Missing instruction dependencies | Searched only the eligible incomplete installation, reported both missing required files, and blocked publication independently of the optional image tool. |

These runs exercised the revised skill only. They are regression checks rather than additional matched pairs.
