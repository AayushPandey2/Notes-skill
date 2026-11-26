---
id: eval-golden-logistic-regression-lab
aliases:
  - Logistic Regression - Experimental Lab
topic: Logistic Regression
tags:
  - domain/ml
  - subject/machine-learning
  - topic/logistic-regression
nexttopics: []
---

# Logistic Regression — Machine Learning Lab

This companion lab pairs with [[logistic-regression|Logistic Regression]] under the explicit Python-only scope in `evaluation-spec.md`, progressing from a single exact gradient step to a complete $L_2$-regularized NumPy classifier with an objective matched to `scikit-learn 1.4.2`.

> [!info] Bundle Navigation
> - **Theory:** [[logistic-regression|Logistic Regression]] · **Mastery & Practice:** [[logistic-regression-mastery|Logistic Regression - Cheatsheet & Interview Q&A]]

## Shared Problem & Reproducibility Contract

- **Learning objective:** Implement overflow-safe `sigmoid` and cancellation-free signed-logit `bce_from_logits`, verify the 1-step gradient update by hand, build a complete $L_2$-regularized NumPy training and prediction pipeline (`fit`, `predict_proba`, `predict`), verify objective equivalence ($C = \frac{1}{m\lambda}$) against `scikit-learn 1.4.2`, and reproduce the non-monotonic threshold precision drop on the 6-point fixture.
- **Shared fixture:** $m = 4$ 1D observations `x = [-2.0, -1.0, 1.0, 2.0]`, labels `y = [0, 0, 1, 1]`, regularization $\lambda = 0.05$ (equivalent to scikit-learn $C = \frac{1}{4 \times 0.05} = 5.0$).
- **Environment & verification scope:** Targets `Python 3.11`, `NumPy 1.26.4`, and `scikit-learn 1.4.2` (pinned version matters because newer `scikit-learn` releases revise penalty APIs). All numerical trace values below are **author-derived / manual_arithmetic / statically_reviewed**; no interpreter executed these blocks.

---

## Track 1 — Complete First-Principles NumPy Implementation (Statically Reviewed)

Evaluating `np.exp(-z)` and `np.exp(z)` directly inside `np.where` fails under NumPy because NumPy evaluates **both** branch arrays eagerly before masking, triggering overflow warnings on large $|z|$. Computing only `t = np.exp(-np.abs(z))` keeps the exponent non-positive everywhere. Similarly, computing `signed_logits = (1.0 - 2.0 * y) * z` evaluates $\ln(1 + e^{-z})$ when $y=1$ and $\ln(1 + e^{z})$ when $y=0$ with zero subtraction cancellation.

```python
from typing import NamedTuple
import numpy as np

class FitReport(NamedTuple):
    converged: bool
    iterations: int
    final_loss: float
    gradient_norm: float
    stop_reason: str
    history: list[float]

X = np.array([[-2.0], [-1.0], [1.0], [2.0]], dtype=np.float64)
y = np.array([0.0, 0.0, 1.0, 1.0], dtype=np.float64)

def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.asarray(z, dtype=np.float64)
    t = np.exp(-np.abs(z))
    return np.where(z >= 0.0, 1.0 / (1.0 + t), t / (1.0 + t))

def bce_from_logits(z: np.ndarray, y_binary: np.ndarray) -> float:
    # Exact signed-logit softplus for y in {0, 1}: log(1 + exp((1 - 2*y)*z))
    z = np.asarray(z, dtype=np.float64)
    y_binary = np.asarray(y_binary, dtype=np.float64)
    signed_logits = (1.0 - 2.0 * y_binary) * z
    return float(np.mean(np.logaddexp(0.0, signed_logits)))

def logit_gradient(z: np.ndarray, y: np.ndarray) -> np.ndarray:
    sign = 1.0 - 2.0 * y
    return sign * sigmoid(sign * z)

def fit_logistic_l2(
    X_in: np.ndarray,
    y_in: np.ndarray,
    lam: float = 0.05,
    lr: float = 1.0,
    max_iter: int = 500,
    grad_tol: float = 1e-8,
) -> tuple[np.ndarray, float, FitReport]:
    X_arr = np.asarray(X_in, dtype=np.float64)
    y_arr = np.asarray(y_in, dtype=np.float64)
    if X_arr.ndim != 2 or min(X_arr.shape) == 0:
        raise ValueError("X must have nonempty shape (m, n)")
    m, n = X_arr.shape
    if y_arr.shape != (m,):
        raise ValueError("y must have shape (m,) with one label per row")
    if not np.all(np.isin(y_arr, [0, 1])):
        raise ValueError("Labels must be binary")
    if not np.isfinite(X_arr).all():
        raise ValueError("Features must be finite")
    if not np.isfinite(lam) or lam < 0:
        raise ValueError("lam must be finite and nonnegative")
    if not np.isfinite(lr) or lr <= 0 or not np.isfinite(grad_tol) or grad_tol <= 0:
        raise ValueError("lr and grad_tol must be finite and positive")
    if isinstance(max_iter, (bool, np.bool_)) or not isinstance(max_iter, (int, np.integer)) or max_iter < 1:
        raise ValueError("max_iter must be a positive integer")

    w = np.zeros(n, dtype=np.float64)
    b = 0.0
    history: list[float] = []
    for updates in range(max_iter + 1):
        with np.errstate(over="raise", invalid="raise"):
            try:
                z = X_arr @ w + b
                obj = bce_from_logits(z, y_arr) + 0.5 * lam * float(w @ w)
                err = logit_gradient(z, y_arr) / m
                grad_w = X_arr.T @ err + lam * w
                grad_b = float(np.sum(err))
                grad_norm = float(np.hypot(np.linalg.norm(grad_w), grad_b))
            except FloatingPointError as exc:
                raise FloatingPointError("Nonfinite training state") from exc
        if not np.isfinite(obj) or not np.isfinite(grad_norm):
            raise FloatingPointError("Nonfinite objective or gradient norm")
        history.append(obj)
        if grad_norm <= grad_tol:
            return w, b, FitReport(True, updates, obj, grad_norm, "gradient_tolerance", history)
        if updates < max_iter:
            with np.errstate(over="raise", invalid="raise"):
                w = w - lr * grad_w
                b = b - lr * grad_b

    return w, b, FitReport(False, max_iter, obj, grad_norm, "iteration_limit", history)

def predict_proba(X_in: np.ndarray, w: np.ndarray, b: float) -> np.ndarray:
    return sigmoid(np.asarray(X_in, dtype=np.float64) @ w + b)

def predict(X_in: np.ndarray, w: np.ndarray, b: float, threshold: float = 0.5) -> np.ndarray:
    return (predict_proba(X_in, w, b) >= threshold).astype(np.int64)
```

### Visible Mechanism, Trace & Numerical Failure Analysis

The trainer enforces one label per feature row because a column of labels would broadcast against the score vector into a square array. Finite features and valid hyperparameters keep failures local. The signed-logit gradient preserves small residuals when a positive probability rounds to one. Each recorded state includes its actual objective and gradient norm, including the state after the last allowed update. A nonfinite state raises a numerical error instead of returning unusable parameters. Neither one-class data nor a separable unpenalized dataset guarantees a finite optimum.

- **Step-1 manual check (author-derived / manual_arithmetic / statically_reviewed):** At iteration 0 (`w = [0.0], b = 0.0, lam = 0.05, lr = 1.0`), `z = [0, 0, 0, 0]`, `p = [0.5, 0.5, 0.5, 0.5]`, `obj_0 = 0.693147`, `grad_w = [-0.75]`, and `grad_b = 0.0`, producing `w_1 = [0.75], b_1 = 0.0`. At iteration 1 (`w = [0.75], b = 0.0`), `p ≈ [0.1824, 0.3208, 0.6792, 0.8176]`, `bce ≈ 0.294142`, and `0.5 * 0.05 * 0.75**2 = 0.014063`, giving regularized `obj_1 ≈ 0.308205`.
- **Stopping & edge behavior:** Checking Euclidean gradient norm against `grad_tol` is a stopping criterion. The shared fixture has both classes and $\lambda > 0$, so it has a unique finite minimum. Setting `lr` too high can cause oscillation or objective increases.

> [!example]- Understand this implementation: step-by-step A–G walkthrough and subtraction cancellation trap
> - **A. Setup & shapes:** `X_arr` has shape `(m, n) = (4, 1)`, `w` has shape `(1,)`, and matrix multiply `X_arr @ w + b` broadcasts scalar `b` cleanly across rows.
> - **B. Mechanism:** Adding `lam * w` strictly inside `grad_w` (leaving `grad_b` unregularized) matches $J_\lambda(\mathbf{w}, b) = J(\mathbf{w}, b) + \frac{\lambda}{2}\|\mathbf{w}\|_2^2$.
> - **C–D. Stability comparison on $z = 50, y = 1$:** Naive `np.logaddexp(0.0, 50.0) - 50.0` cancels `~50.0 - 50.0` and rounds to zero, whereas `(1 - 2*1)*50 = -50` evaluates `np.logaddexp(0.0, -50.0) = np.log1p(exp(-50.0)) ≈ 1.93e-22` directly without subtracting two nearly equal numbers.
> - **E–G. Limits & failure repair:** `sigmoid(z)` with `np.exp(-z)` inside `np.where` overflows at `z = -1000` before selecting the safe branch; `np.exp(-np.abs(z))` eliminates overflow across all finite inputs.

---

## Track 2 — Identical $L_2$ Objective in `scikit-learn 1.4.2` (L-BFGS Solver)

To align Track 2 directly with Track 1's `fit_logistic_l2`, match `scikit-learn 1.4.2`'s unnormalized sum objective $J_{\text{sk}}(\mathbf{w}, b) = C \sum_{i=1}^m \ell(z_i, y_i) + \frac{1}{2}\|\mathbf{w}\|_2^2$ via $C = \frac{1}{m\lambda}$. The pinned implementation uses this equivalent penalty scaling. [scikit-learn 1.4.2 L-BFGS setup](https://github.com/scikit-learn/scikit-learn/blob/1.4.2/sklearn/linear_model/_logistic.py#L411-L422)

For $m = 4$ and $\lambda = 0.05$, `C = 1.0 / (4 * 0.05) = 5.0`.

Unlike fixed-step gradient descent, `lbfgs` (Limited-memory BFGS) uses recent parameter and gradient differences to approximate inverse Hessian curvature along search directions with a line search, reducing step oscillation along steep-vs.-flat weight directions without needing manual step-size tuning `lr` on convex smooth problems (though finite-iteration agreement still depends on both solvers' gradient tolerances).

```python
from sklearn.linear_model import LogisticRegression
import numpy as np

X = np.array([[-2.0], [-1.0], [1.0], [2.0]], dtype=np.float64)
y_cls = np.array([0, 0, 1, 1], dtype=np.int64)

lam = 0.05
C_equiv = 1.0 / (len(X) * lam)  # = 5.0 for m = 4
clf = LogisticRegression(C=C_equiv, penalty="l2", solver="lbfgs", tol=1e-10, max_iter=500)
clf.fit(X, y_cls)

# Threshold evaluation check from Section 8 of Theory
probs = np.array([0.95, 0.85, 0.65, 0.55, 0.40, 0.20])
y_eval = np.array([1, 0, 1, 1, 0, 0])

def precision_and_recall(p_hat: np.ndarray, y_true: np.ndarray, tau: float) -> tuple[float, float]:
    preds = p_hat >= tau
    tp = int(np.sum((preds == 1) & (y_true == 1)))
    fp = int(np.sum((preds == 1) & (y_true == 0)))
    fn = int(np.sum((preds == 0) & (y_true == 1)))
    # This example reports 0.0 when a denominator is zero.
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return precision, recall

# Run this block after Track 1 to compare the fitted parameters.
w_fit, b_fit, report = fit_logistic_l2(X, y_cls, lam=lam)
assert report.converged
np.testing.assert_allclose(w_fit, clf.coef_[0], atol=1e-6, rtol=0)
np.testing.assert_allclose(b_fit, clf.intercept_[0], atol=1e-6, rtol=0)
np.testing.assert_allclose(precision_and_recall(probs, y_eval, 0.50), (0.75, 1.0))
np.testing.assert_allclose(precision_and_recall(probs, y_eval, 0.70), (0.50, 1 / 3))
```

| Property | Track 1 (`fit_logistic_l2` NumPy) | Track 2 (`scikit-learn 1.4.2` `lbfgs`) |
|---|---|---|
| **Loss scaling** | Mean BCE over $m$ ($\frac{1}{m}\sum \ell_i$) | Summed BCE weighted by $C$ ($C\sum \ell_i$) |
| **Regularization parameter** | $\lambda = 0.05$ | $C = \frac{1}{m\lambda} = 5.0$ (never `1 / lam = 20.0`) |
| **Intercept treatment** | `grad_b` unpenalized | Unpenalized for this L-BFGS setup |
| **Expected converged params** | Unique finite $(\mathbf{w}^*, b^*)$ ($\|\nabla J_\lambda\| < 10^{-8}$) | Same minimizer within solver convergence tolerances |

- **Threshold evaluation check (author-derived / manual_arithmetic / statically_reviewed):** Running `precision_and_recall(probs, y_eval, 0.50)` yields `(0.75, 1.00)`, whereas `precision_and_recall(probs, y_eval, 0.70)` yields `(0.50, 1/3)`, illustrating that raising $\tau$ lowers precision here because true positives ($0.65, 0.55$) were filtered out before false positive ($0.85$).

> [!example]- Understand this realization: diagnosing regularization drift and L-BFGS limits
> Passing `C = 1 / lam = 20.0` makes `scikit-learn`'s penalty $m = 4$ times weaker than `fit_logistic_l2(..., lam=0.05)`, producing systematically larger $\|\mathbf{w}\|$ even when both solvers reach gradient zero. On high-dimensional problems with tiny sample counts, omitting `C = 1/(m*lam)` prevents meaningful cross-track comparison.

## Track 3 — Compare local optimizer steps and evaluate held-out data

At an identical starting point, form the design with an intercept column. The diagonal curvature entries are $\sigma(z_i)\sigma(-z_i)$, which avoids forming $1-\sigma(z_i)$ by subtraction. For ridge Newton, add $\lambda$ only to the weight block. Solve the linear system for the increment. This also gives the regularized IRLS increment without dividing a working response by tiny diagonal entries.

```python
def newton_step(X, y, theta, lam):
    design = np.column_stack([X, np.ones(len(y))])
    z = design @ theta
    penalty = np.r_[np.full(X.shape[1], lam), 0.0]
    gradient = design.T @ logit_gradient(z, y) / len(y) + penalty * theta
    curvature = sigmoid(z) * sigmoid(-z)
    hessian = (design.T * curvature) @ design / len(y) + np.diag(penalty)
    return theta + np.linalg.solve(hessian, -gradient)

theta0 = np.zeros(X.shape[1] + 1)
theta_unpenalized = newton_step(X, y_cls, theta0, lam=0.0)
theta_ridge = newton_step(X, y_cls, theta0, lam=lam)
np.testing.assert_allclose(theta_unpenalized, [1.2, 0.0], atol=1e-12)
np.testing.assert_allclose(theta_ridge, [10 / 9, 0.0], atol=1e-12)
w_one, b_one, one_update = fit_logistic_l2(X, y_cls, lam=lam, max_iter=1)
np.testing.assert_allclose([w_one[0], b_one], [.75, 0.0], atol=1e-12)
assert one_update.stop_reason == "iteration_limit"
assert len(one_update.history) == one_update.iterations + 1

# A separate illustrative train/test split with overlapping classes.
train_x = np.array([[-2.], [-1.5], [-1.], [-.5], [.5], [1.], [1.5], [2.]])
train_y = np.array([0, 0, 1, 0, 1, 0, 1, 1])
test_x = np.array([[-1.75], [-.75], [-.25], [.25], [.75], [1.75]])
test_y = np.array([0, 1, 0, 1, 0, 1])
for strength in (0.0, 0.5):
    weights, intercept, fit = fit_logistic_l2(train_x, train_y, lam=strength)
    assert fit.converged
    test_logits = test_x @ weights + intercept
    test_probabilities = sigmoid(test_logits)
    test_loss = bce_from_logits(test_logits, test_y)
    precision, recall = precision_and_recall(test_probabilities, test_y, 0.5)
    print(strength, weights[0], test_loss, precision, recall)
```

The first comparison isolates the effect of the update rule and penalty on one step. The second compares probability scores on held-out observations. Its two fits can have the same classifications at threshold $0.5$ and different BCE because the predicted probabilities differ. These six constructed test points illustrate the distinction. They cannot estimate deployment performance or establish calibration.

**Simulated author verification:** source and static review only. Repository execution evidence is listed in [the evaluation specification](evaluation-spec.md).
