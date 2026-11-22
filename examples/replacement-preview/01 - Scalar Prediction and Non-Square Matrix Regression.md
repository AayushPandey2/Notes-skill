---
topic: Supervised Learning
tags:
- topic/supervised-learning
- subject/supervised-learning-replacement-preview
- domain/machine-learning
- master-topic/supervised-learning-replacement-preview
- subdomain/foundations
- concept/supervised-learning
- type/deep-notes
- ml
- supervised-learning
- replacement-preview
master_topic: Supervised Learning (Replacement Preview)
domain: machine-learning
note_type: deep-notes
subdomain: Foundations
---

# Scalar Prediction and Non-Square Matrix Regression

Suppose we want to predict a house price or trip cost from measurable features. A simple constant average ignores how features change, so we build a linear predictor starting from one feature before scaling cleanly to multiple features in matrix form.

Think of linear regression as adjusting one slope dial $w$ and one starting height $b$: each unit step in $x$ shifts the line up or down by $w$. This linear mental model applies only when outcomes scale proportionally across the feature range and fails on strongly curved boundaries.

### Scalar Prediction Before Matrix Notation

Predict a continuous target y-hat from one numerical input x using slope w and baseline bias b.

$$
\hat{y} = w x + b
$$

> [!example]- Understand this formula step by step
> **What question does it answer?**
> Predict a continuous target y-hat from one numerical input x using slope w and baseline bias b.
>
> **How to read it aloud:** y-hat equals w times x plus b.
>
> | Symbol | Name / Meaning | Type | Shape / Units | Role |
> |---|---|---|---|---|
> | $\hat{y}$ | predicted target value | scalar | 1x1 | predicted target value |
> | $w$ | weight (rate of change per unit x) | parameter | 1x1 | weight (rate of change per unit x) |
> | $x$ | input feature value | scalar | 1x1 | input feature value |
> | $b$ | bias intercept baseline when x = 0 | parameter | 1x1 | bias intercept baseline when x = 0 |
>
> **Step-by-step operations:**
> 1. Multiply input feature x by weight w to compute feature contribution.
> 2. Add scalar baseline bias b so zero-input predictions match the baseline.
>
> **Worked numerical example:**
> - **Declared inputs:** `w = 2.5`, `x = 4.0`, `b = 10.0`
> - **scaled_feature:** `w * x` = `10.0` — slope 2.5 over 4 units adds 10.0
> - **prediction:** `wx + b` = `20.0` — shift by baseline bias 10.0
> - **Interpretation:** At x = 4.0 with baseline 10.0 and slope 2.5, the predicted output is 20.0.
> - **Sanity check:** Setting x = 0 returns b = 10.0; doubling slope doubles the sensitivity to x.
>
> **Assumptions & conditions:** Assumes an approximately linear relationship across the observed x range.
>
> **Common misunderstandings to avoid:**
> - Confusing weight w (slope) with correlation coefficient or confusing y-hat (prediction) with ground truth y.


### Scaling Up to Non-Square Feature Matrices

With $n = 3$ examples and $d = 2$ features, writing one scalar equation per row gets tedious, so we stack features into a non-square matrix $X \in \mathbb{R}^{3 \times 2}$. First let us check geometry before algebraic inversion.

To see geometrically why the Normal Equations solve least squares, inspect how the fitted prediction lies inside the column subspace while the residual points orthogonally away.

![[assets/scriptorium/supervised-learning-preview/least-squares-projection-bd92be15b65c.png|560]]

*Figure: Ordinary least squares orthogonal projection of target vector b onto the plane spanned by feature columns a1 and a2.*

*Source: [original publication](https://commons.wikimedia.org/wiki/File:Least_squares_projection_geometry.png); rights: CC BY-SA 4.0*

*Figure: Ordinary least squares orthogonal projection of target vector b onto the plane spanned by feature columns a1 and a2..*

**How to read this figure:**
- *Where to begin:* Begin on the shaded plane spanned by a1 and a2, then trace the vertical perpendicular residual up to b.
- The shaded plane is every linear combination Xw achievable by the model.
- The perpendicular segment is the residual y - Xw*, minimized precisely when orthogonal to the feature plane.

That perpendicularity X^T(y - Xw*) = 0 directly produces the Normal Equations below.

Compute predictions simultaneously across n = 3 examples and d = 2 features with explicit non-square matrix alignment.

$$
\hat{\mathbf{y}} = X \mathbf{w} + b \mathbf{1}
$$

> [!example]- Understand this formula step by step
> **What question does it answer?**
> Compute predictions simultaneously across n = 3 examples and d = 2 features with explicit non-square matrix alignment.
>
> **How to read it aloud:** y-hat vector equals design matrix X times weight vector w plus bias vector b times all-ones column 1.
>
> | Symbol | Name / Meaning | Type | Shape / Units | Role |
> |---|---|---|---|---|
> | $\hat{\mathbf{y}}$ | vector of 3 example predictions | vector | 3x1 | vector of 3 example predictions |
> | $X$ | non-square feature matrix (3 rows = samples, 2 cols = features) | matrix | 3x2 | non-square feature matrix (3 rows = samples, 2 cols = features) |
> | $\mathbf{w}$ | feature weight vector | vector | 2x1 | feature weight vector |
> | $b$ | unpenalized scalar bias intercept | scalar | 1x1 | unpenalized scalar bias intercept |
> | $\mathbf{1}$ | column vector of n ones | vector | 3x1 | column vector of n ones |
>
> **Shape compatibility:** `(3×2) × (2×1) = (3×1)`.
>
> **Step-by-step operations:**
> 1. Verify inner dimensions match: X is (3x2) and w is (2x1), yielding (3x1).
> 2. Swap check (anti-error): computing w^T X would attempt (1x2) @ (3x2) which fails inner dimension matching (2 != 3).
> 3. Compute each row dot product x^(i) . w and add bias b to every row.
>
> **Worked numerical example:**
> - **Declared inputs:** `x11 = 1.0`, `x12 = 2.0`, `w1 = 3.0`, `w2 = -1.0`, `b = 4.0`
> - **row1_dot:** `x11 * w1 + x12 * w2` = `1.0` — first row (1*3 + 2*(-1)) = 1.0
> - **row1_pred:** `dot1 + b` = `5.0` — add bias 4.0
> - **Interpretation:** Row 1 of the (3x2) matrix yields prediction 5.0 cleanly inside the (3x1) output vector.
> - **Sanity check:** Output shape (3x1) matches the 3 training targets; switching X and w shapes fails compatibility check.
>
> **Common misunderstandings to avoid:**
> - Forgetting that X^T is (2x3), so X^T X is (2x2) rather than (3x3), or attempting (2x1) @ (2x1) without transposing.


Identify the linear weight vector w* whose residual vector y - Xw* is orthogonal to every feature column of X.

$$
X^\top X \mathbf{w}^* = X^\top \mathbf{y}
$$

> [!example]- Understand this formula step by step
> **What question does it answer?**
> Identify the linear weight vector w* whose residual vector y - Xw* is orthogonal to every feature column of X.
>
> **How to read it aloud:** X transpose X times w-star equals X transpose y.
>
> | Symbol | Name / Meaning | Type | Shape / Units | Role |
> |---|---|---|---|---|
> | $X^\top$ | transpose of feature matrix (features by samples) | matrix | 2x3 | transpose of feature matrix (features by samples) |
> | $X$ | feature matrix (samples by features) | matrix | 3x2 | feature matrix (samples by features) |
> | $\mathbf{w}^*$ | optimal least-squares weights | vector | 2x1 | optimal least-squares weights |
> | $\mathbf{y}$ | observed target vector | vector | 3x1 | observed target vector |
>
> **Shape compatibility:** `(2×3) × (3×2) = (2×2)`.
>
> **Step-by-step operations:**
> 1. Multiply X^T (2x3) by X (3x2) to form symmetric Gram matrix (2x2).
> 2. Require X^T(y - Xw*) = 0 so every feature column is orthogonal to residuals.
>
> **Worked numerical example:**
> - **Declared inputs:** `gram_11 = 14.0`, `rhs_1 = 28.0`
> - **solve_1d_diag:** `rhs_1 / gram_11` = `2.0` — solve symmetric normal system
> - **Interpretation:** When curvature X^T X = 14 and alignment X^T y = 28, w* = 2.0 zeros the gradient.
> - **Sanity check:** Residual inner product vanishes at the solution.
>
> **Assumptions & conditions:** Exact inverse (X^T X)^(-1) requires linearly independent columns (full column rank d).
>
> **Common misunderstandings to avoid:**
> - Feature standardization rescales feature magnitudes to help gradient descent converge faster, NOT fix exact linear collinearity rank deficiency.


> [!IMPORTANT] Feature Scaling Qualification
> Standardizing features (mean $0$, variance $1$) balances elongated numerical scales so iterative gradient descent converges far faster, **but scaling alone does not cure exact linear collinearity** among redundant columns.

### Worked Sanity Check (Code After Conceptual Mastery)

```python
import numpy as np

X = np.array([[1.0, 2.0], [2.0, 1.0], [3.0, 4.0]])  # shape (3, 2) non-square
w = np.array([[3.0], [-1.0]])                       # shape (2, 1)
b = 4.0
preds = X @ w + b                                   # shape (3, 1)
assert preds.shape == (3, 1) and float(preds[0, 0]) == 5.0
```

## Check Your Understanding

**Question:** If $X \in \mathbb{R}^{5 \times 3}$ has 5 observations and 3 features, why does attempting $\mathbf{w} \in \mathbb{R}^{3 \times 1}$ multiplied as $\mathbf{w}^	op X$ fail dimension matching?

> [!hint]- Show hint
> Compare the inner dimensions of $(1 \times 3) \times (5 \times 3)$.

> [!answer]- Show detailed answer
> A $1 \times 3$ row vector has inner column count $3$, while $X$ has $5$ rows ($3 \ne 5$). Putting the feature matrix on the left as $X\mathbf{w}$ pairs $(5 \times 3)(3 \times 1) = (5 \times 1)$, matching one scalar prediction to each of the $5$ samples.

For measuring how inaccurate any prediction is before updating weights, continue to [[02 - Loss Functions and Outlier Sensitivity]].
