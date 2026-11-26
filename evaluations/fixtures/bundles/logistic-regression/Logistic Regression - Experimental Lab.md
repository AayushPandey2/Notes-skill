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

> [!info] Bundle Navigation
> - **Theory:** [[Logistic Regression]] · **Mastery & Practice:** [[Logistic Regression - Cheatsheet & Interview Q&A]]

## Shared Problem & Reproducibility Contract

- **Learning objective:** Verify gradient descent on unregularized BCE matches the hand-calculated step in [[Logistic Regression]], demonstrate numerically stable logits loss against naive saturation, and establish exact $L_2$ objective-level equivalence between manual penalty $\lambda$ and scikit-learn's `C`.
- **Shared fixture:** $m = 4$ 1D points $x = [-2, -1, 1, 2]$, labels $y = [0, 0, 1, 1]$, initial weights $w_0 = 0.0, b_0 = 0.0$, learning rate $\eta = 1.0$.
- **Governing mechanism & verification:** Minimize mean BCE $J(w, b) = -\frac{1}{m}\sum_{i=1}^m [y_i\ln\sigma(z_i) + (1-y_i)\ln(1-\sigma(z_i))]$ via logits (`softplus`), verifying step-1 predictions and gradients against hand arithmetic.
- **Reproducibility & integrity notice:** Code blocks target Python 3.11 + NumPy 1.26+ / scikit-learn 1.4+. All numerical outputs below are **author-derived / manual_arithmetic / statically_reviewed**; no interpreter was invoked.

---

## Track 1 — From-Scratch NumPy Logistic Regression (Statically Verified)

```python
import numpy as np

x = np.array([-2.0, -1.0, 1.0, 2.0], dtype=np.float64)
y = np.array([0.0, 0.0, 1.0, 1.0], dtype=np.float64)

def sigmoid(z: np.ndarray) -> np.ndarray:
    return np.where(z >= 0, 1.0 / (1.0 + np.exp(-z)), np.exp(z) / (1.0 + np.exp(z)))

def bce_from_logits(z: np.ndarray, y_true: np.ndarray) -> float:
    # Numerically stable softplus form: log(1 + exp(z)) - y*z
    return float(np.mean(np.logaddexp(0.0, z) - y_true * z))

w, b, eta = 0.0, 0.0, 1.0
z0 = w * x + b
p0 = sigmoid(z0)
err0 = p0 - y
grad_w = float(np.mean(err0 * x))
grad_b = float(np.mean(err0))
loss0 = bce_from_logits(z0, y)

w1 = w - eta * grad_w
b1 = b - eta * grad_b
loss1 = bce_from_logits(w1 * x + b1, y)
```

> [!example]- Understand this implementation: mathematics, code, and numerical dry run
> - **A. Setup & inputs:** `x` (`shape (4,)`) and binary `y` match the Theory fixture identically; `(w, b) = (0.0, 0.0)`, `eta = 1.0`.
> - **B. Governing mechanism:** `bce_from_logits` computes $\ln(1 + e^z) - y z = \max(z, 0) + \ln(1 + e^{-|z|}) - y z$ via `np.logaddexp(0.0, z)` so extreme logits never produce `0 * inf -> NaN`.
> - **C. Execution order:** Evaluate `z0 -> p0 -> err0 -> (grad_w, grad_b)` before applying the descent step `(w1, b1)` and recomputing `loss1`.
> - **D. Complete concrete trace (author-derived / manual_arithmetic / statically_reviewed):**
>   - `z0 = [0, 0, 0, 0]`, `p0 = [0.5, 0.5, 0.5, 0.5]`, `loss0 = 0.693147`
>   - `grad_w = -0.75`, `grad_b = 0.0` $\implies$ `w1 = 0.75`, `b1 = 0.0`
>   - `z1 = [-1.5, -0.75, 0.75, 1.5]` $\implies$ `p1 ≈ [0.1824, 0.3208, 0.6792, 0.8176]`, `loss1 ≈ 0.294142`.
> - **E. Interpretation & limits:** One gradient step halves the loss on this symmetric separable set; continuing indefinitely without $L_2$ regularization pushes $w \to +\infty$.
> - **F. Failure analysis (Problematic approach -> failure mechanism -> correction -> explanation):** Writing `-(y*np.log(p) + (1-y)*np.log(1-p))` fails with `RuntimeWarning` / `NaN` when large $|z|$ rounds `p` to `0.0` or `1.0`; `np.logaddexp(0.0, z) - y*z` avoids intermediate `log(0)`.
> - **G. Reconstruction:** Stable logits loss separates exponential overflow guards from clean probability residuals.

---

## Track 2 — Objective-Level Equivalence with scikit-learn `L2` Regularization

Matching scikit-learn's unnormalized sum-of-losses objective (with unpenalized intercept $b$):

$$
J_{\text{mean}}(w, b) = \frac{1}{m}\sum_{i=1}^m \ell(z_i, y_i) + \frac{\lambda}{2} w^2
\quad\Longleftrightarrow\quad
J_{\text{sklearn}}(w, b) = C\sum_{i=1}^m \ell(z_i, y_i) + \frac{1}{2} w^2
\quad\text{at}\quad C = \frac{1}{m\lambda}
$$

- Because $m = 4$, setting custom weight decay $\lambda = 0.05$ corresponds to scikit-learn `C = 1 / (4 * 0.05) = 5.0`—**never** `C = 1 / lambda = 20.0`.
- Dropping $b$ from the penalty avoids shrinking baseline class bias toward $0.5$.

```python
from sklearn.linear_model import LogisticRegression
import numpy as np

X = np.array([[-2.0], [-1.0], [1.0], [2.0]], dtype=np.float64)
y_cls = np.array([0, 0, 1, 1], dtype=np.int64)

lam = 0.05
C_equiv = 1.0 / (len(X) * lam)  # = 5.0 for m = 4
clf = LogisticRegression(C=C_equiv, penalty="l2", solver="lbfgs")
clf.fit(X, y_cls)
```

> [!example]- Understand this realization: scikit-learn solver & hyperparameter scaling trace
> - **A–B. Setup & change from Track 1:** Only the $L_2$ solver (`lbfgs`) and exact scaled parameter `C_equiv = 5.0` change; input data $(X, y)$ stays identical.
> - **C–D. Expected boundary & check (author-derived / analytical / statically_reviewed):** `lbfgs` converges much faster than fixed-step GD and finds a unique finite $w^* > 0$ bounded by $\frac{1}{2}w^2$, whereas `clf.coef_` would change systematically if one erroneously passed `C = 1 / lam = 20.0` (4x weaker regularization).
> - **E–G. Failure & limit:** Assuming `C = 1 / alpha` silently mismatches batch-size scaling whenever $m$ changes across datasets.

**Source and static review only; not compiled or executed here.**
