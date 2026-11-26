---
id: eval-golden-logistic-regression
aliases:
  - Logistic Regression
topic: Logistic Regression
tags:
  - domain/ml
  - subject/machine-learning
  - topic/logistic-regression
nexttopics: []
---

# Logistic Regression

Logistic regression models binary event probabilities by linearly parameterizing conditional log-odds and fitting weights via convex regularized maximum likelihood.

**Difficulty:** Intermediate (requires linear combinations, logarithm/exponential inverses, and single-variable calculus; multivariable chain-rule and Hessian steps are derived inline)
**Prerequisites:** Linear equations ($\mathbf{w}^\top\mathbf{x} + b$), inverse identities ($e^{\ln u} = u$), product/quotient/chain derivative rules, and positive semidefinite quadratic forms ($\mathbf{v}^\top A \mathbf{v} \ge 0$)

## Learning objectives
1. Show numerically why ordinary least squares violates probability bounds and Bernoulli variance assumptions for $0/1$ targets.
2. Derive the logistic sigmoid and odds-ratio weight interpretation from a linear log-odds assumption, connect scores to hyperplane decision geometry, and derive $\sigma'(z) = \sigma(z)(1 - \sigma(z))$ before likelihood differentiation.
3. Construct Binary Cross-Entropy (BCE) step by step from conditional Bernoulli likelihood and prove why BCE is globally convex while sigmoid squared error loses convexity in saturation tails.
4. Derive BCE scalar, indexed, and vectorized matrix gradients ($\nabla_{\mathbf{w}} J = \frac{1}{m}X^\top(\hat{\mathbf{p}}-\mathbf{y})$) from first principles, trace one gradient update by hand, and explain both Gradient Descent anatomy and Newton–Raphson / IRLS curvature scaling.
5. Formulate $L_2$ regularization for linear separation, derive signed-logit numerical stability, and separate fitted probabilities from non-monotonic classification thresholding ($\tau$).

**Table of Contents**
- [[#1. Problem Formulation & Why Ordinary Least Squares Fails|1. Problem Formulation & OLS Failure]]
- [[#2. Probability, Odds, Log-Odds & Sigmoid Derivation|2. Log-Odds to Sigmoid Derivation]]
- [[#3. Odds-Ratio Interpretation, Decision Geometry & Sigmoid Derivative|3. Odds Ratios, Geometry & Sigmoid Derivative]]
- [[#4. Bernoulli Likelihood to Binary Cross-Entropy Derivation|4. Bernoulli MLE to BCE Derivation]]
- [[#5. Chain-Rule & Scalar-to-Matrix Gradient Derivation|5. Chain-Rule & Matrix Gradients]]
- [[#6. Convexity, Hessian Geometry & Parameter Optimization|6. Convexity, GD & Newton Optimization]]
- [[#7. L2 Regularization, Separation & Numerical Stability|7. L2 Regularization & Numerical Stability]]
- [[#8. Decision Thresholds, Evaluation & Model Limitations|8. Thresholds, Evaluation & Limitations]]
- [[#9. Mental Model, Notation Reference & Bundle Links|9. Mental Model & Bundle Links]]

---

## 1. Problem Formulation & Why Ordinary Least Squares Fails

Binary classification separates two connected problems: estimating **conditional class probabilities** $p_i = P(Y_i = 1 \mid \mathbf{x}_i) \in [0, 1]$ from input features $\mathbf{x}_i \in \mathbb{R}^n$, and mapping those probabilities into discrete decisions $\hat{y}_i \in \{0, 1\}$ under problem-specific error costs.

Trying to predict $Y \in \{0, 1\}$ directly with ordinary linear regression $\hat{y}_{\text{OLS}}(x) = wx + b$ on our shared 4-point dataset $(-2, 0), (-1, 0), (1, 1), (2, 1)$ demonstrates two structural mismatches:
- Sample means give $\bar{x} = 0$ and $\bar{y} = 0.50$. Computing centered ordinary least squares gives $w_{\text{OLS}} = \frac{(-2)(-0.5) + (-1)(-0.5) + (1)(0.5) + (2)(0.5)}{(-2)^2 + (-1)^2 + 1^2 + 2^2} = \frac{3.0}{10} = 0.30$ and $b_{\text{OLS}} = 0.50$.
- Evaluating $\hat{y}_{\text{OLS}}(x) = 0.30x + 0.50$ at observed training inputs yields $\hat{y}_{\text{OLS}}(-2) = -0.10 < 0$ and $\hat{y}_{\text{OLS}}(+2) = +1.10 > 1$.

More generally, any nonzero linear coefficient on an unbounded domain outputs values outside $[0, 1]$, violating Kolmogorov probability axioms, while Gaussian least squares treats residual variance as constant instead of matching Bernoulli variance $\operatorname{Var}(Y \mid \mathbf{x}) = p(1 - p)$.

**Unresolved question:** How can we preserve an unconstrained linear score $z = \mathbf{w}^\top \mathbf{x} + b \in \mathbb{R}$ while inverting it cleanly into $(0, 1)$?

---

## 2. Probability, Odds, Log-Odds & Sigmoid Derivation

Converting real scores $z \in (-\infty, +\infty)$ into probabilities $p \in (0, 1)$ requires choosing a smooth monotone link function—a **modeling assumption** rather than a unique mathematical necessity (alternative links include probit $\Phi(z)$ and asymmetric complementary log-log $1 - e^{-e^z}$).

Logistic regression constructs its link in two symmetric steps:
1. **Odds:** For $p \in (0, 1)$, the ratio of event probability to complementary probability is $\operatorname{odds}(p) = \frac{p}{1 - p} \in (0, +\infty)$. When $p = 0.80$, odds equal $\frac{0.80}{0.20} = 4$ (four times more likely positive than negative).
2. **Log-odds (logit):** Taking the natural logarithm expands $(0, +\infty)$ symmetrically onto $(-\infty, +\infty)$, where $p = 0.50 \iff \ln(1) = 0$.

Logistic regression models these conditional log-odds as a linear function of predictors:

$$
z = \mathbf{w}^\top \mathbf{x} + b = \ln\left(\frac{p}{1 - p}\right)
$$

Inverting this log-odds definition expresses probability $p$ directly as the **logistic sigmoid**:

$$
\boxed{p = \sigma(z) = \frac{1}{1 + e^{-z}}}
$$

> [!example]- Understand this formula step by step
> 1. **Mathematical origin:** Start from the modeling assumption $z = \ln\left(\frac{p}{1 - p}\right)$ with $0 < p < 1$ so both $p$ and $1 - p$ are strictly positive.
> 2. **Symbol interpretation:** $z \in \mathbb{R}$ is the unconstrained linear score ($\mathbf{w}^\top\mathbf{x} + b$), $p \in (0, 1)$ is $P(Y=1 \mid \mathbf{x})$, and $1-p$ is $P(Y=0 \mid \mathbf{x})$.
> 3. **Remove the logarithm:** Exponentiate both sides (valid because $\exp$ and $\ln$ are inverse functions on $(0, +\infty)$):
> $$
> e^z = e^{\ln\left(\frac{p}{1 - p}\right)} = \frac{p}{1 - p}
> $$
> 4. **Clear the denominator:** Multiply both sides by $1 - p > 0$ and distribute $e^z$:
> $$
> e^z(1 - p) = p \implies e^z - p e^z = p
> $$
> 5. **Collect and isolate $p$:** Add $p e^z$ to both sides, factor out $p$, and divide by $1 + e^z > 0$:
> $$
> e^z = p(1 + e^z) \implies p = \frac{e^z}{1 + e^z}
> $$
> 6. **Normalize to standard reciprocal form:** Divide numerator and denominator by $e^z > 0$ so $z$ appears once with negative sign:
> $$
> p = \frac{e^z / e^z}{(1 + e^z)/e^z} = \frac{1}{e^{-z} + 1} = \frac{1}{1 + e^{-z}}
> $$
> 7. **Worked check & boundaries:** At $z = 3.0$, $\operatorname{odds} = e^{3.0} \approx 20.0855$ and $p = \frac{20.0855}{21.0855} = \frac{1}{1 + e^{-3}} \approx 0.9526$. Since $e^{-z} > 0$ for all finite $z \in \mathbb{R}$, denominator $1 + e^{-z} > 1$, guaranteeing $\sigma(z) \in (0, 1)$ strictly ($\lim_{z\to+\infty}\sigma(z)=1$, $\lim_{z\to-\infty}\sigma(z)=0$, $\sigma(0)=0.5$).

---

## 3. Odds-Ratio Interpretation, Decision Geometry & Sigmoid Derivative

### Odds Ratios & Hyperplane Decision Boundary
Exponentiating $z = \ln\left(\frac{p}{1-p}\right)$ yields $\operatorname{odds}(\mathbf{x}) = \exp(\mathbf{w}^\top\mathbf{x} + b)$. Consequently, a unit step in predictor $x_j$ scales modeled odds multiplicatively by $e^{w_j}$:

$$
\boxed{\frac{\operatorname{odds}(\dots, x_j + 1, \dots)}{\operatorname{odds}(\dots, x_j, \dots)} = e^{w_j}}
$$

> [!example]- Understand this formula step by step
> 1. **Starting identity:** Let $\mathbf{x}'$ agree with $\mathbf{x}$ on every coordinate except $x_j' = x_j + 1$. Then $z' = \mathbf{w}^\top \mathbf{x}' + b = (\mathbf{w}^\top \mathbf{x} + b) + w_j = z + w_j$.
> 2. **Exponentiate and factor:** Using $e^{a+b} = e^a e^b$:
> $$
> \frac{\operatorname{odds}(\mathbf{x}')}{\operatorname{odds}(\mathbf{x})} = \frac{e^{z + w_j}}{e^z} = \frac{e^z e^{w_j}}{e^z} = e^{w_j}
> $$
> 3. **Interpretation & limitation:** A $+1$ change in $x_j$ multiplies odds by $e^{w_j}$ holding other covariates fixed (for example, $w_j = \ln 2 \approx 0.6931$ doubles odds). Note this holds only under the linear log-odds specification and depends directly on $x_j$'s measurement units.

Geometrically, setting probability threshold $\sigma(z) \ge \tau$ is equivalent (by applying monotone $\ln\frac{\tau}{1-\tau}$) to $\mathbf{w}^\top \mathbf{x} + b \ge \ln\left(\frac{\tau}{1-\tau}\right)$, defining an $(n-1)$-dimensional separating **hyperplane** orthogonal to $\mathbf{w}$ (reducing to $\mathbf{w}^\top\mathbf{x} + b = 0$ at $\tau = 0.50$).

### Sigmoid Derivative (Derived Before Likelihood Optimization)
To optimize parameters via gradients of loss wrt $\mathbf{w}$, we first establish how $\sigma(z)$ responds to small changes in logit $z$:

$$
\boxed{\sigma'(z) = \sigma(z)\bigl(1 - \sigma(z)\bigr)}
$$

> [!example]- Understand this formula step by step
> 1. **Mathematical origin:** Rewrite $\sigma(z) = (1 + e^{-z})^{-1}$ as a composition $u^{-1}$ with inner function $u(z) = 1 + e^{-z}$.
> 2. **Chain rule differentiation:** Differentiating wrt $z$ applies the power rule $\frac{d}{du}(u^{-1}) = -u^{-2}$ multiplied by $\frac{du}{dz} = -e^{-z}$:
> $$
> \sigma'(z) = -(1 + e^{-z})^{-2}(-e^{-z}) = \frac{e^{-z}}{(1 + e^{-z})^2}
> $$
> 3. **Factor to express cleanly in $\sigma(z)$:** Split one factor $\frac{1}{1+e^{-z}} = \sigma(z)$ and algebraically rewrite the remaining factor $\frac{e^{-z}}{1 + e^{-z}} = \frac{(1 + e^{-z}) - 1}{1 + e^{-z}} = 1 - \frac{1}{1 + e^{-z}} = 1 - \sigma(z)$:
> $$
> \sigma'(z) = \frac{1}{1 + e^{-z}} \cdot \frac{e^{-z}}{1 + e^{-z}} = \sigma(z)\bigl(1 - \sigma(z)\bigr)
> $$
> 4. **Symmetry identity:** Checking $\sigma(-z) = \frac{1}{1+e^z} = \frac{e^{-z}}{e^{-z}+1} = 1 - \sigma(z)$ confirms $\sigma'(-z) = \sigma'(z)$ (even sensitivity around $z=0$).
> 5. **Worked check & bounds:** Sensitivity peaks at $z = 0$ ($\sigma(0)=0.5 \implies \sigma'(0) = 0.5(0.5) = 0.25$) and shrinks sharply in tails (at $z = 3.0$, $\sigma(3) \approx 0.9526 \implies \sigma'(3) \approx 0.9526(0.0474) \approx 0.0452$).

**Unresolved question:** With $\sigma(z)$ and its identity $\sigma'(z) = \sigma(z)(1-\sigma(z))$ established, how do we construct an objective function from observed binary outcomes $(y_1, \dots, y_m)$?

---

## 4. Bernoulli Likelihood to Binary Cross-Entropy Derivation

Model each label conditioned on features as $Y_i \mid \mathbf{x}_i \sim \text{Bernoulli}(p_i)$ with $p_i = \sigma(\mathbf{w}^\top \mathbf{x}_i + b)$. Because $y_i \in \{0, 1\}$, both outcome probabilities unify into one probability mass expression $P(Y_i = y_i \mid \mathbf{x}_i) = p_i^{y_i}(1 - p_i)^{1 - y_i}$. Assuming conditionally independent samples and maximizing likelihood leads cleanly to **mean Binary Cross-Entropy (BCE)**:

$$
\boxed{J(\mathbf{w}, b) = -\frac{1}{m}\sum_{i=1}^{m}\Bigl[y_i\ln(p_i) + (1 - y_i)\ln(1 - p_i)\Bigr]}
$$

> [!example]- Understand this formula step by step
> 1. **Mathematical origin (Bernoulli PMF):** For binary $y_i \in \{0, 1\}$, $p_i^{1}(1-p_i)^0 = p_i$ when $y_i = 1$, and $p_i^0(1-p_i)^1 = 1 - p_i$ when $y_i = 0$.
> 2. **Joint dataset likelihood:** Under conditional independence across $i = 1, \dots, m$, probabilities multiply:
> $$
> L(\mathbf{w}, b) = \prod_{i=1}^{m} p_i^{y_i}(1 - p_i)^{1 - y_i}
> $$
> Products of $m$ terms inside $(0, 1)$ underflow rapidly in finite precision and turn differentiation into massive product rules.
> 3. **Log-likelihood transformation:** Because $\ln(\cdot)$ is strictly increasing on $(0, +\infty)$, maximizing $\ln L$ achieves the exact same argmax $(\mathbf{w}^*, b^*)$ while converting products into sums ($\ln(ab) = \ln a + \ln b$) and exponents into multipliers ($\ln(a^c) = c\ln a$):
> $$
> \ln L(\mathbf{w}, b) = \sum_{i=1}^{m}\Bigl[y_i\ln(p_i) + (1 - y_i)\ln(1 - p_i)\Bigr]
> $$
> 4. **Negation & sample normalization:** Multiplying by $-1$ turns likelihood maximization into loss minimization, and dividing by sample count $m$ yields mean per-example loss comparable across dataset sizes: $J(\mathbf{w}, b) = -\frac{1}{m}\ln L(\mathbf{w}, b)$.
> 5. **Equivalent logit form:** Substituting $p_i = \frac{e^{z_i}}{1+e^{z_i}}$ and $1-p_i = \frac{1}{1+e^{z_i}}$ inside $\ell(p_i, y_i) = -\bigl[y_i\ln p_i + (1-y_i)\ln(1-p_i)\bigr]$ simplifies single-sample loss directly to $\ell(z_i, y_i) = \ln(1 + e^{z_i}) - y_i z_i$ (used below for convexity).
> 6. **Interpretation & check:** When $y_i = 1$ and $p_i = 0.90$, loss is $-\ln(0.90) \approx 0.1054$; if a confident mistake predicts $p_i = 0.01$, loss jumps to $-\ln(0.01) \approx 4.6052$, penalizing overconfident wrong predictions without bound.

**Unresolved question:** How does $J(\mathbf{w}, b)$ change when we perturb parameters $\mathbf{w}$ and $b$—and can our newly derived $\sigma'(z)$ simplify that derivative?

---

## 5. Chain-Rule & Scalar-to-Matrix Gradient Derivation

### Partial Derivatives via Exact Factor Cancellation
Using the multivariable chain rule alongside $\sigma'(z) = p(1 - p)$ derived in Section 3 yields clean residual-scaled gradients:

$$
\boxed{\frac{\partial J}{\partial w_j} = \frac{1}{m}\sum_{i=1}^{m}(p_i - y_i)x_{ij}, \qquad \frac{\partial J}{\partial b} = \frac{1}{m}\sum_{i=1}^{m}(p_i - y_i)}
$$

> [!example]- Understand this formula step by step
> 1. **Decompose single-sample loss $\ell_i(p_i, y_i)$:** Compute $\frac{\partial \ell_i}{\partial w_j}$ via the chain rule $\frac{\partial \ell_i}{\partial p_i} \cdot \frac{\partial p_i}{\partial z_i} \cdot \frac{\partial z_i}{\partial w_j}$:
>    - Differentiating $\ell_i = -[y_i\ln p_i + (1-y_i)\ln(1-p_i)]$ wrt $p_i$ (noting $\frac{d}{dp}\ln(1-p) = -\frac{1}{1-p}$ by chain rule):
> $$
> \frac{\partial \ell_i}{\partial p_i} = -\frac{y_i}{p_i} + \frac{1 - y_i}{1 - p_i} = \frac{-y_i(1 - p_i) + p_i(1 - y_i)}{p_i(1 - p_i)} = \frac{p_i - y_i}{p_i(1 - p_i)}
> $$
>    - Substituting the previously derived sigmoid derivative $\frac{\partial p_i}{\partial z_i} = p_i(1 - p_i)$ and score derivative $\frac{\partial z_i}{\partial w_j} = x_{ij}$ ($\frac{\partial z_i}{\partial b} = 1$):
> $$
> \frac{\partial \ell_i}{\partial w_j} = \frac{p_i - y_i}{p_i(1 - p_i)} \cdot p_i(1 - p_i) \cdot x_{ij} = (p_i - y_i)x_{ij}
> $$
> 2. **Cancellation rationale:** The inverse probability variance denominator $p_i(1-p_i)$ from Bernoulli log-likelihood cancels identically with $\sigma'(z_i) = p_i(1-p_i)$, preventing sigmoid derivative shrinkage on confidently wrong binary predictions. (*Qualification:* this eliminates saturation in the output logistic head, not across deeper hidden neural layers.)
> 3. **Average over $m$ samples:** Linearity of differentiation sums single-sample derivatives across $i = 1, \dots, m$ and multiplies by $\frac{1}{m}$. Notice $(p_i - y_i)$ gives the signed probability error while $x_{ij}$ scales how strongly weight $w_j$ shifts sample $i$'s logit.

### Scalar-to-Vector-to-Matrix Gradient Construction
Stacking all $m$ feature vectors row-wise into design matrix $X \in \mathbb{R}^{m \times n}$ expresses all $n$ weight derivatives in one vectorized operation:

$$
\boxed{\nabla_{\mathbf{w}} J = \frac{1}{m}X^\top(\hat{\mathbf{p}} - \mathbf{y})}
$$

> [!example]- Understand this formula step by step
> 1. **Stage 1 (1 parameter, scalar):** $\frac{\partial J}{\partial w} = \frac{1}{m}\sum_{i=1}^m (\hat{p}_i - y_i)x_i$.
> 2. **Stage 2 ($n$ parameters, indexed sums):** For feature column $j \in \{1, \dots, n\}$, weight $w_j$ accumulates residual-weighted entries down column $j$: $\left[\nabla_{\mathbf{w}} J\right]_j = \frac{1}{m}\sum_{i=1}^m x_{ij}(\hat{p}_i - y_i)$.
> 3. **Stage 3 (Matrix dimension & transpose justification):** Let residual vector $\mathbf{r} = \hat{\mathbf{p}} - \mathbf{y} \in \mathbb{R}^{m \times 1}$. With concrete batch dimensions $m = 5$ examples and $n = 3$ features, $X$ has shape `(5, 3)` and $\mathbf{r}$ has shape `(5, 1)`. You cannot multiply `(5, 3) @ (5, 1)` because inner dimensions disagree; transposing $X$ gives $X^\top$ of shape `(3, 5)`. Then matrix multiplication $X^\top \mathbf{r}$ produces shape `(3, 5) @ (5, 1) = (3, 1)`: row $j$ of $X^\top$ is column $j$ of $X$, so its dot product with $\mathbf{r}$ computes $\sum_{i=1}^m x_{ij}(\hat{p}_i - y_i)$ for every weight $w_j$ simultaneously. Dividing by $m$ yields the mean gradient vector $\in \mathbb{R}^n$.

### Hand Trace on Shared 4-Point Fixture ($w_0 = 0, b_0 = 0, \eta = 1.0$)
Using $x = [-2, -1, 1, 2]$ and $y = [0, 0, 1, 1]$, initial logits are $z_i = 0$ and $\hat{p}_i = 0.50$:

**Prediction pass:**

| Sample $i$ | Feature $x_i$ | True Label $y_i$ | Logit $z_i$ | Predicted $\hat{p}_i$ |
|---:|---:|---|---:|---:|
| 1 | $-2$ | `0 — Negative` | $0.00$ | $0.50$ |
| 2 | $-1$ | `0 — Negative` | $0.00$ | $0.50$ |
| 3 | $+1$ | `1 — Positive` | $0.00$ | $0.50$ |
| 4 | $+2$ | `1 — Positive` | $0.00$ | $0.50$ |

**Learning update pass ($J(0,0) = -\ln(0.5) \approx 0.6931$):**

| Sample $i$ | Feature $x_i$ | Residual $\hat{p}_i - y_i$ | Gradient Term $(\hat{p}_i - y_i)x_i$ |
|---:|---:|---:|---:|
| 1 | $-2$ | $+0.50$ | $-1.00$ |
| 2 | $-1$ | $+0.50$ | $-0.50$ |
| 3 | $+1$ | $-0.50$ | $-0.50$ |
| 4 | $+2$ | $-0.50$ | $-1.00$ |

- Mean gradients: $\frac{\partial J}{\partial w} = \frac{-3.00}{4} = -0.75$ and $\frac{\partial J}{\partial b} = 0.00$.
- Step 1 update ($\eta = 1.0$): $w_1 = 0 - 1.0(-0.75) = 0.75$, $b_1 = 0.00$, shifting probabilities to $\hat{p} \approx [0.1824, 0.3208, 0.6792, 0.8176]$ and lowering BCE to $J(0.75, 0) \approx 0.2941$.

---

## 6. Convexity, Hessian Geometry & Parameter Optimization

Because BCE has no general closed-form analytic zero for $(\mathbf{w}^*, b^*)$ when probabilities are nonlinear in $z$, optimization relies on iterative algorithms whose global reliability rests on objective **convexity**.

### Global Convexity of Binary Cross-Entropy
Using the logit form $\ell(z, y) = \ln(1 + e^z) - yz$ derived in Section 4, BCE yields a positive semidefinite Hessian matrix across all augmented parameters $\boldsymbol{\theta} = [\mathbf{w}; b] \in \mathbb{R}^{n+1}$ (with augmented design matrix $\tilde{X} = [X,\; \mathbf{1}] \in \mathbb{R}^{m \times (n+1)}$):

$$
\boxed{\nabla_{\boldsymbol{\theta}}^2 J(\boldsymbol{\theta}) = \frac{1}{m}\tilde{X}^\top D \tilde{X} \succeq 0, \qquad D = \operatorname{diag}\Bigl(\hat{p}_1(1-\hat{p}_1),\dots,\hat{p}_m(1-\hat{p}_m)\Bigr)}
$$

> [!example]- Understand this formula step by step
> 1. **Scalar first and second logit derivatives:** Differentiating $\ell(z, y) = \ln(1 + e^z) - yz$ wrt $z$ gives $\frac{\partial \ell}{\partial z} = \frac{e^z}{1+e^z} - y = \sigma(z) - y$. Differentiating a second time uses Section 3's identity:
> $$
> \frac{\partial^2 \ell}{\partial z^2} = \sigma'(z) = \sigma(z)\bigl(1 - \sigma(z)\bigr) \ge 0
> $$
> 2. **Chain rule to augmented parameters:** Since $z_i = \tilde{\mathbf{x}}_i^\top \boldsymbol{\theta}$, $\nabla_{\boldsymbol{\theta}} \ell_i = (\hat{p}_i - y_i)\tilde{\mathbf{x}}_i$, and differentiating once more gives rank-1 Hessian $\nabla_{\boldsymbol{\theta}}^2 \ell_i = \hat{p}_i(1 - \hat{p}_i)\tilde{\mathbf{x}}_i\tilde{\mathbf{x}}_i^\top$.
> 3. **Matrix assembly & positive semidefiniteness:** Summing $\frac{1}{m}\sum_{i=1}^m d_i \tilde{\mathbf{x}}_i\tilde{\mathbf{x}}_i^\top = \frac{1}{m}\tilde{X}^\top D \tilde{X}$ with $d_i = \hat{p}_i(1 - \hat{p}_i) \ge 0$. For every vector $\mathbf{v} \in \mathbb{R}^{n+1}$, quadratic form $\mathbf{v}^\top \nabla^2 J\,\mathbf{v} = \frac{1}{m}\sum_{i=1}^m d_i (\tilde{\mathbf{x}}_i^\top \mathbf{v})^2 \ge 0$. Therefore $J$ is **globally convex** (strictly convex whenever $\tilde{X}$ has full column rank and $\hat{p}_i \in (0, 1)$).
> 4. **Why sigmoid squared error fails global convexity:** For $y = 1$, $\ell_{\text{sq}}(z, 1) = \frac{1}{2}(p - 1)^2$ gives $\frac{\partial \ell_{\text{sq}}}{\partial z} = (p-1)\sigma'(z) = -p(1-p)^2$. Differentiating wrt $p$ gives $-(1-p)^2 + 2p(1-p) = (1-p)(3p-1)$, and multiplying by $\frac{dp}{dz} = p(1-p)$ gives:
> $$
> \frac{\partial^2 \ell_{\text{sq}}}{\partial z^2} = p(1 - p)^2(3p - 1)
> $$
> Whenever $p < \frac{1}{3}$ ($z < -\ln 2 \approx -0.6931$), $(3p - 1) < 0$, making curvature **negative** (at $p = 0.1$, curvature is $-0.0567 < 0$ vs. BCE $+0.09 > 0$). Although whether an aggregated sum over a specific dataset has multiple local minima depends on $X$ and $\mathbf{y}$, sigmoid squared error is not convex in general and creates flat saturation plateaus.

### Parameter Optimization: Gradient Descent & Newton's Method
First-order optimization minimizes $J$ iteratively by updating weights against the gradient:

$$
\boxed{\mathbf{w}_{t+1} = \mathbf{w}_t - \eta \nabla_{\mathbf{w}} J(\mathbf{w}_t, b_t)}
$$

> [!example]- Understand this formula step by step
> 1. **Component-by-component formula construction:**
>    - $\mathbf{w}_t$: Starting iterate anchoring the local quadratic/linear Taylor model around the current parameter estimate.
>    - $\nabla_{\mathbf{w}} J$: Local sensitivity vector pointing in the direction of steepest local *increase* of $J$.
>    - **Negative sign (`-`):** By first-order Taylor expansion $J(\mathbf{w}_t + \Delta\mathbf{w}) \approx J(\mathbf{w}_t) + \nabla J^\top \Delta\mathbf{w}$, setting $\Delta\mathbf{w} = -\eta \nabla J$ gives $J(\mathbf{w}_t + \Delta\mathbf{w}) \approx J(\mathbf{w}_t) - \eta\|\nabla J\|_2^2 \le J(\mathbf{w}_t)$.
>    - **Learning rate $\eta > 0$:** Controls step size so updates remain inside the region where the first-order linear approximation holds.
>    - **Iteration index $t$:** Repeating moves down curved valleys until $\|\nabla J\|$ reaches a stopping tolerance.
> 2. **Assumptions & failure mode:** Guarantees decrease only for sufficiently small $\eta$ at nonstationary points ($\nabla J \neq 0$); overly large $\eta$ overshoots and diverges even on convex BCE.

*(Advanced extension — second-order Newton / IRLS step):* Because we explicitly derived both gradient $\nabla_{\boldsymbol{\theta}} J$ and positive-definite Hessian $H_t = \frac{1}{m}\tilde{X}^\top D_t \tilde{X}$, second-order **Newton–Raphson** (equivalently **Iteratively Reweighted Least Squares**) rescales the step by local inverse curvature: $\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - H_t^{-1}\nabla_{\boldsymbol{\theta}} J_t$, converging quadratically near finite regularized optima on moderate feature dimensions.

---

## 7. L2 Regularization, Separation & Numerical Stability

### L2 Regularization & Conditions for a Unique Finite Optimum
When training data is **linearly separable**, any separating $\mathbf{w}$ achieves $y_i = 1 \implies z_i > 0$ and $y_i = 0 \implies z_i < 0$. Scaling $\|\mathbf{w}\| \to \infty$ sends $\sigma(z_i) \to y_i$ and $J(\mathbf{w}, b) \to 0$, so **no finite minimizer exists**. Adding an $L_2$ quadratic penalty restores coercivity:

$$
\boxed{J_{\lambda}(\mathbf{w}, b) = J(\mathbf{w}, b) + \frac{\lambda}{2}\|\mathbf{w}\|_2^2 \quad\implies\quad \nabla_{\mathbf{w}} J_\lambda = \frac{1}{m}X^\top(\hat{\mathbf{p}} - \mathbf{y}) + \lambda \mathbf{w}}
$$

> [!example]- Understand this formula step by step
> 1. **Derivative derivation:** Expanding $\frac{\lambda}{2}\|\mathbf{w}\|_2^2 = \frac{\lambda}{2}\sum_{k=1}^n w_k^2$ and differentiating wrt $w_j$ cancels $\frac{1}{2}$ with factor $2$, contributing $+\lambda w_j$, while $\frac{\partial}{\partial b}\left(\frac{\lambda}{2}\|\mathbf{w}\|_2^2\right) = 0$ leaves intercept $b$ unpenalized (preserving class prior base rates).
> 2. **Strong convexity & existence conditions:** Adding $\lambda I$ raises every eigenvalue of the $\mathbf{w}$-block Hessian by at least $\lambda > 0$, making $J_\lambda$ strictly convex in $\mathbf{w}$ and coercive ($\|\mathbf{w}\|\to\infty \implies J_\lambda\to\infty$). Combined with finite bounded data where both classes $0$ and $1$ occur (keeping intercept $b$ finite), a **unique finite global minimizer** exists even under linear separation.
> 3. **Library convention check:** `scikit-learn 1.4.2` scales summed loss by $C$ alongside $\frac{1}{2}\|\mathbf{w}\|_2^2$, giving identical solutions at $C = \frac{1}{m\lambda}$ (implemented and verified in [[Logistic Regression - Experimental Lab]]).

### Overflow-Safe Sigmoid & Subtraction-Free Logit BCE
Mathematically $\sigma(z) \in (0, 1)$ strictly for all finite $z \in \mathbb{R}$, yet finite-precision `float64` breaks naive code:
- Evaluating `1 / (1 + exp(-z))` overflows `exp(-z)` when $z = -1000$; factoring out $t = e^{-|z|} \le 1$ computes `1/(1+t)` for $z \ge 0$ and `t/(1+t)` for $z < 0$ without overflow.
- Naive `np.logaddexp(0, z) - y*z` still cancels tiny remainders at $z = 50, y = 1$ ($\ln(1 + e^{50}) - 50 \approx 0.0$ drops true loss $1.93 \times 10^{-22}$). Exploiting $\sigma(-z) = 1 - \sigma(z)$ eliminates subtraction completely:

$$
\boxed{\ell(z, y) = \ln\Bigl(1 + e^{(1 - 2y)z}\Bigr), \qquad y \in \{0, 1\}}
$$

> [!example]- Understand this formula step by step
> 1. **Case $y = 1$:** Multiplier $(1 - 2y) = -1$, giving $-\ln \sigma(z) = \ln(1 + e^{-z})$. At $z = 50$, `logaddexp(0, -50)` preserves $e^{-50} \approx 1.93 \times 10^{-22}$ with full `float64` relative precision.
> 2. **Case $y = 0$:** Multiplier $(1 - 2y) = +1$, giving $-\ln(1 - \sigma(z)) = -\ln\sigma(-z) = \ln(1 + e^{+z})$.
> 3. **Applicability limit:** Exact for hard binary labels $y \in \{0, 1\}$; soft fractional targets $y \in (0, 1)$ require convex weighting $(1-y)\ln(1+e^z) + y\ln(1+e^{-z})$.

---

## 8. Decision Thresholds, Evaluation & Model Limitations

Choosing threshold $\tau$ in $\hat{y} = \mathbf{1}[\hat{p} \ge \tau]$ **never changes fitted weights $(\mathbf{w}, b)$ or predicted probabilities $\hat{p}_i$**. Raising $\tau$ cannot increase the set of predicted positives ($\text{TP}$ and $\text{FP}$ cannot rise), **yet precision is not guaranteed to improve**:

| Case $i$ | Predicted Probability $\hat{p}_i$ | Actual Class $y_i$ | Decision ($\tau = 0.50$) | Decision ($\tau = 0.70$) |
|---:|---:|---|---|---|
| 1 | $0.95$ | `1 — Positive` | `TP` | `TP` |
| 2 | $0.85$ | `0 — Negative` | `FP` | `FP` |
| 3 | $0.65$ | `1 — Positive` | `TP` | `FN` |
| 4 | $0.55$ | `1 — Positive` | `TP` | `FN` |
| 5 | $0.40$ | `0 — Negative` | `TN` | `TN` |
| 6 | $0.20$ | `0 — Negative` | `TN` | `TN` |

- At $\tau = 0.50$: `TP = 3, FP = 1` $\implies$ **Precision = $75.0\%$ (`3/4`)**, **Recall = $100.0\%$ (`3/3`)**.
- At $\tau = 0.70$: dropping true positives at $0.65$ and $0.55$ while keeping false positive $0.85$ gives `TP = 1, FP = 1` $\implies$ **Precision drops to $50.0\%$ (`1/2`)** alongside **Recall = $33.3\%$ (`1/3`)**.

**Evaluation, limitations & multiclass handoff:** Evaluate discrimination with ROC-AUC/$F_1$ and calibration with BCE log-loss/reliability curves. Note logistic regression assumes linear log-odds in engineered features (failing on XOR interactions without nonlinear feature maps), suffers intercept distortion under arbitrary resampling, and generalizes to $K > 2$ classes via One-vs-Rest binary heads or **multinomial softmax** ($P(Y=k\mid\mathbf{x}) = \frac{e^{z_k}}{\sum_{j=1}^K e^{z_j}}$).

---

## 9. Mental Model, Notation Reference & Bundle Links

**Mental Model:** Construct conditional log-odds linearity $\to$ invert to $\sigma(z)$ $\to$ derive $\sigma'(z) = p(1-p)$ $\to$ build Bernoulli MLE negative log-likelihood (BCE) $\to$ combine chain-rule cancellation with $X^\top(\hat{\mathbf{p}}-\mathbf{y})$ $\to$ establish Hessian convexity + Newton/GD + $L_2$ separation control $\to$ stabilize numerically with signed logits before choosing threshold $\tau$ for asymmetric decision costs.

**Trailing Notation Reference:** $m$ samples · $n$ features · $X \in \mathbb{R}^{m\times n}, \tilde{X} = [X,\mathbf{1}]$ · $\mathbf{w}, b, \boldsymbol{\theta}$ parameters · $z$ logit · $\sigma(z)$ sigmoid · $p_i, \hat{p}_i$ probabilities · $y_i \in \{0,1\}$ targets · $\eta$ step size · $\lambda, C$ $L_2$ regularization parameters · $\tau$ threshold.

- **Companions in this bundle:** [[Logistic Regression - Experimental Lab]] · [[Logistic Regression - Cheatsheet & Interview Q&A]]
