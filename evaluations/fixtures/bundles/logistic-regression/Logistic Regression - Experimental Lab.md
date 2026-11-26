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

This companion lab pairs with [[Logistic Regression]] under the explicit Python-only scope in `evaluation-spec.md`, progressing from a single exact gradient step to a complete $L_2$-regularized NumPy classifier matched identically against `scikit-learn 1.4.2`.

> [!info] Bundle Navigation
> - **Theory:** [[Logistic Regression]] · **Mastery & Practice:** [[Logistic Regression - Cheatsheet & Interview Q&A]]

## Shared Problem & Reproducibility Contract

- **Learning objective:** Implement overflow-safe `sigmoid` and cancellation-free signed-logit `bce_from_logits`, verify the 1-step gradient update by hand, build a complete $L_2$-regularized NumPy training and prediction pipeline (`fit`, `predict_proba`, `predict`), verify objective equivalence ($C = \frac{1}{m\lambda}$) against `scikit-learn 1.4.2`, and reproduce the non-monotonic threshold precision drop on the 6-point fixture.
- **Shared fixture:** $m = 4$ 1D observations `x = [-2.0, -1.0, 1.0, 2.0]`, labels `y = [0, 0, 1, 1]`, regularization $\lambda = 0.05$ (equivalent to scikit-learn $C = \frac{1}{4 \times 0.05} = 5.0$).
- **Environment & verification scope:** Targets `Python 3.11`, `NumPy 1.26.4`, and `scikit-learn 1.4.2` (pinned version matters because newer `scikit-learn` releases revise penalty APIs). All numerical trace values below are **author-derived / manual_arithmetic / statically_reviewed**; no interpreter executed these blocks.

---

## Track 1 — Complete First-Principles NumPy Implementation (Statically Reviewed)

Evaluating `np.exp(-z)` and `np.exp(z)` directly inside `np.where` fails under NumPy because NumPy evaluates **both** branch arrays eagerly before masking, triggering overflow warnings on large $|z|$. Computing only `t = np.exp(-np.abs(z))` keeps the exponent non-positive everywhere. Similarly, computing `signed_logits = (1.0 - 2.0 * y) * z` evaluates $\ln(1 + e^{-z})$ when $y=1$ and $\ln(1 + e^{z})$ when $y=0$ with zero subtraction cancellation.

```python
import numpy as np

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

def fit_logistic_l2(
    X_in: np.ndarray,
    y_in: np.ndarray,
    lam: float = 0.05,
    lr: float = 1.0,
    max_iter: int = 500,
    grad_tol: float = 1e-8,
) -> tuple[np.ndarray, float, list[float]]:
    X_arr = np.asarray(X_in, dtype=np.float64)
    y_arr = np.asarray(y_in, dtype=np.float64)
    m, n = X_arr.shape
    w = np.zeros(n, dtype=np.float64)
    b = 0.0
    history: list[float] = []

    for _ in range(max_iter):
        z = X_arr @ w + b
        p = sigmoid(z)
        obj = bce_from_logits(z, y_arr) + 0.5 * lam * float(w @ w)
        history.append(obj)

        err = (p - y_arr) / m
        grad_w = X_arr.T @ err + lam * w
        grad_b = float(np.sum(err))  # Intercept b is unpenalized

        if np.hypot(np.linalg.norm(grad_w), abs(grad_b)) < grad_tol:
            break

        w = w - lr * grad_w
        b = b - lr * grad_b

    return w, b, history

def predict_proba(X_in: np.ndarray, w: np.ndarray, b: float) -> np.ndarray:
    return sigmoid(np.asarray(X_in, dtype=np.float64) @ w + b)

def predict(X_in: np.ndarray, w: np.ndarray, b: float, threshold: float = 0.5) -> np.ndarray:
    return (predict_proba(X_in, w, b) >= threshold).astype(np.int64)
```

### Visible Mechanism, Trace & Numerical Failure Analysis

- **Step-1 manual check (author-derived / manual_arithmetic / statically_reviewed):** At iteration 0 (`w = [0.0], b = 0.0, lam = 0.05, lr = 1.0`), `z = [0, 0, 0, 0]`, `p = [0.5, 0.5, 0.5, 0.5]`, `obj_0 = 0.693147`, `grad_w = [-0.75]`, and `grad_b = 0.0`, producing `w_1 = [0.75], b_1 = 0.0`. At iteration 1 (`w = [0.75], b = 0.0`), `p ≈ [0.1824, 0.3208, 0.6792, 0.8176]`, `bce ≈ 0.294142`, and `0.5 * 0.05 * 0.75**2 = 0.014063`, giving regularized `obj_1 ≈ 0.308205`.
- **Stopping & edge behavior:** Checking Euclidean gradient norm against `grad_tol` halts near the strictly convex unique minimum when $\lambda > 0$, whereas setting `lr` too high causes oscillatory objective spikes.

> [!example]- Understand this implementation: step-by-step A–G walkthrough and subtraction cancellation trap
> - **A. Setup & shapes:** `X_arr` has shape `(m, n) = (4, 1)`, `w` has shape `(1,)`, and matrix multiply `X_arr @ w + b` broadcasts scalar `b` cleanly across rows.
> - **B. Mechanism:** Adding `lam * w` strictly inside `grad_w` (leaving `grad_b` unregularized) matches $J_\lambda(\mathbf{w}, b) = J(\mathbf{w}, b) + \frac{\lambda}{2}\|\mathbf{w}\|_2^2$.
> - **C–D. Stability comparison on $z = 50, y = 1$:** Naive `np.logaddexp(0.0, 50.0) - 50.0` cancels `~50.0 - 50.0` and loses precision near `2e-16`, whereas `(1 - 2*1)*50 = -50` evaluates `np.logaddexp(0.0, -50.0) = np.log1p(exp(-50.0)) ≈ 1.93e-22` directly with full `float64` relative accuracy.
> - **E–G. Limits & failure repair:** `sigmoid(z)` with `np.exp(-z)` inside `np.where` overflows at `z = -1000` before selecting the safe branch; `np.exp(-np.abs(z))` eliminates overflow across all finite inputs.

---

## Track 2 — Identical $L_2$ Objective in `scikit-learn 1.4.2` (L-BFGS Solver)

To align Track 2 directly with Track 1's `fit_logistic_l2`, match `scikit-learn 1.4.2`'s unnormalized sum objective $J_{\text{sk}}(\mathbf{w}, b) = C \sum_{i=1}^m \ell(z_i, y_i) + \frac{1}{2}\|\mathbf{w}\|_2^2$ via $C = \frac{1}{m\lambda}$. For $m = 4$ and $\lambda = 0.05$, `C = 1.0 / (4 * 0.05) = 5.0`.

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
    return tp / (tp + fp), tp / (tp + fn)
```

| Property | Track 1 (`fit_logistic_l2` NumPy) | Track 2 (`scikit-learn 1.4.2` `lbfgs`) |
|---|---|---|
| **Loss scaling** | Mean BCE over $m$ ($\frac{1}{m}\sum \ell_i$) | Summed BCE weighted by $C$ ($C\sum \ell_i$) |
| **Regularization parameter** | $\lambda = 0.05$ | $C = \frac{1}{m\lambda} = 5.0$ (never `1 / lam = 20.0`) |
| **Intercept treatment** | `grad_b` unpenalized | Unpenalized unless regularized intercept scaling applies |
| **Expected converged params** | Unique finite $(\mathbf{w}^*, b^*)$ ($\|\nabla J_\lambda\| < 10^{-8}$) | Same minimizer within solver convergence tolerances |

- **Threshold evaluation check (author-derived / manual_arithmetic / statically_reviewed):** Running `precision_and_recall(probs, y_eval, 0.50)` yields `(0.75, 1.00)`, whereas `precision_and_recall(probs, y_eval, 0.70)` yields `(0.50, 1/3)`, confirming in code that raising $\tau$ lowers precision here because true positives ($0.65, 0.55$) were filtered out before false positive ($0.85$).

> [!example]- Understand this realization: diagnosing regularization drift and L-BFGS limits
> Passing `C = 1 / lam = 20.0` makes `scikit-learn`'s penalty $m = 4$ times weaker than `fit_logistic_l2(..., lam=0.05)`, producing systematically larger $\|\mathbf{w}\|$ even when both solvers reach gradient zero. On high-dimensional problems with tiny sample counts, omitting `C = 1/(m*lam)` prevents meaningful cross-track comparison.

**Source and static review only; not compiled or executed here.**
