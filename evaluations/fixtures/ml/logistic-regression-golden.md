# Evaluation Fixture (Golden): Logistic Regression (`evaluations/fixtures/ml/`)

*Evaluation-only reference excerpt—never copy as a mandatory template.*

## From Log-Odds to Sigmoid
To map a linear score $z = \mathbf{w}^\top \mathbf{x} + b \in (-\infty, +\infty)$ to a valid probability $p \in (0, 1)$, model the **log-odds** as linear: $z = \ln\left(\frac{p}{1-p}\right)$. Exponentiating and solving for $p$ yields:
$$
p = \sigma(z) = \frac{1}{1 + e^{-z}}
$$
Mathematically, $\sigma(z) \in (0, 1)$ strictly for all finite $z \in \mathbb{R}$; in `float32`/`float64` arithmetic, large $|z|$ saturates to `0.0` or `1.0`, so cross-entropy loss should be computed from logits using log-sum-exp rather than $\ln(\sigma(z))$.

## Thresholds vs. Fitted Model
Changing a classification threshold (e.g., $0.50 \to 0.70$) **can** alter TP/FP/TN/FN counts, precision, and recall **without changing the fitted weights $(\mathbf{w}, b)$ or predicted probabilities**—it only changes the downstream decision rule. (If no predicted probabilities lie between the old and new thresholds, the confusion-matrix counts and threshold-dependent metrics remain unchanged.)
