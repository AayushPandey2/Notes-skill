# Statistics & Probability Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Sample Dataset
Applies to probability models, estimation, confidence intervals, hypothesis tests, and causal inference. Define population parameter vs. sample estimator, distributional/independence assumptions, and one shared small dataset once.

## Practical Realizations
1. **Manual Calculation:** Hand-compute probabilities, estimators, test statistics, or intervals on the shared sample dataset.
2. **Formal Reasoning:** Derive or justify the governing estimator/test statistic and its null/sampling-distribution assumptions.
3. **Simulation or Data Analysis:** Use a non-executed Python or R example to explain repeated sampling. Label predicted output as a prediction and apply the shared lab evidence rules to any supplied simulation results.
4. **Assumption & Significance Verification:** Check sensitivity to outliers, dependence, or small $n$, and separate **statistical vs. practical significance**—explicitly noting that **simulation evidence illustrates sampling behavior rather than proving an analytical theorem**.

## Specialized Walkthrough & Verification
Verify $p$-value wording (test-statistic extremeness under $H_0$), and end with **`Source and static review only; not compiled or executed here.`** (or **`Hand-calculated and analytical review only (no code executed).`** when no code appears).
