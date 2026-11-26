# Hidden Grading Key: `logistic-regression-flawed.md`

*Evaluation-only answer key—never provide to the blind reviewer.*

1. **Critical — Wrong gradient scaling:** Objective uses $\frac{1}{m}$, but gradient uses $\frac{1}{2m}$ (silent factor-of-2 mismatch).
2. **Critical — False numerical claim:** Claims $\sigma(z) \in (0, 1)$ on any computer so $\ln(\hat{p})$ never produces `-inf`/`NaN` (ignores finite-precision saturation and log-sum-exp / logits stability).
3. **Major — Conceptual error on thresholds:** Claims raising the decision threshold *"retrains the model to output higher probabilities"* (thresholding changes decision counts only, not fitted parameters or probabilities).
