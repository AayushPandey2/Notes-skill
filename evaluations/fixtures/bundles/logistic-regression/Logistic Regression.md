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

Logistic regression models binary outcome probabilities by mapping a linear predictor score to conditional log-odds and fitting weights via regularized maximum likelihood.

**Difficulty:** Intermediate (requires linear weighted sums and single-variable derivatives; local probability bridges provided before first use)
**Prerequisites:** Linear combinations ($\mathbf{w}^\top \mathbf{x} + b$), exponential/logarithm inverse rules ($e^{\ln u} = u$), and first/second derivatives of scalar functions

## Learning objectives
1. Demonstrate numerically why ordinary least squares fails as a probability classifier and explain why binary outcomes call for a Bernoulli likelihood model.
2. Construct the logit link ($z \to \text{odds} \to \text{log-odds} \to \sigma(z)$), interpret weights as multiplicative odds ratios, and connect $z = \ln\frac{\tau}{1-\tau}$ to linear decision-boundary geometry.
3. Derive Binary Cross-Entropy (BCE) from Bernoulli maximum likelihood and prove why regularized BCE is convex while sigmoid squared error admits non-convex plateaus.
4. Derive the simplified BCE gradient via the chain rule, hand-trace a complete update on a 4-point fixture, and implement numerically stable sigmoid and signed-logit loss formulas.
5. Formulate $L_2$-regularized logistic regression to handle linear separation and separate fitted probabilities from classification thresholding ($\tau$).

**Table of Contents**
- [[#1. Binary Classification & Why Ordinary Least Squares Fails|1. Problem Formulation & OLS Failure]]
- [[#2. Link Functions, Log-Odds, Sigmoid & Coefficient Interpretation|2. Log-Odds, Sigmoid & Geometry]]
- [[#3. Deriving Binary Cross-Entropy from Bernoulli Likelihood|3. Bernoulli MLE to BCE]]
- [[#4. Why BCE Is Convex While Sigmoid Squared Error Is Not|4. Convexity vs. Non-Convexity]]
- [[#5. Gradient Descent Derivation & Step-by-Step Numerical Trace|5. Gradient Derivation & Trace]]
- [[#6. L2 Regularization & Complete Linear Separation|6. Regularization & Separation]]
- [[#7. Numerical Stability in Finite-Precision Arithmetic|7. Finite-Precision Stability]]
- [[#8. Threshold Decisions, Limitations & Multiclass Handoff|8. Thresholds, Evaluation & Limits]]
- [[#9. Mental Model, Notation Reference & Bundle Links|9. Mental Model & Bundle Links]]

---

## 1. Binary Classification & Why Ordinary Least Squares Fails

Binary classification distinguishes two coupled tasks: **probability estimation** ($p = P(Y = 1 \mid \mathbf{x}) \in [0, 1]$) and **decision-making** (picking a discrete class $\hat{y} \in \{0, 1\}$ under action costs).

Consider fitting ordinary linear regression $\hat{y}_{\text{OLS}} = w x + b$ directly to $m = 4$ binary-labeled observations $(-2, 0), (-1, 0), (1, 1), (2, 1)$:
- Mean predictor $\bar{x} = 0$ and mean label $\bar{y} = 0.50$.
- Centered least-squares slope gives $w_{\text{OLS}} = \frac{(-2)(-0.5) + (-1)(-0.5) + (1)(0.5) + (2)(0.5)}{(-2)^2 + (-1)^2 + 1^2 + 2^2} = \frac{3.0}{10} = 0.30$, with intercept $b_{\text{OLS}} = 0.50$.

Evaluating $\hat{y}_{\text{OLS}}(x) = 0.30 x + 0.50$ at $x = -2$ predicts $-0.10 < 0$, and at $x = +2$ predicts $+1.10 > 1$. Across unbounded feature domains (when $w \neq 0$), a linear function exits $[0, 1]$, violating valid probability axioms, while Gaussian squared-error fitting mismatches discrete $0/1$ Bernoulli variance (where variance $p(1-p)$ depends strongly on the mean).

**Unresolved question:** How do we keep a tractable linear score $z = \mathbf{w}^\top \mathbf{x} + b \in \mathbb{R}$ while mapping it smoothly into $(0, 1)$?

---

## 2. Link Functions, Log-Odds, Sigmoid & Coefficient Interpretation

Many smooth functions map $(-\infty, +\infty)$ onto $(0, 1)$, so choosing the mapping is a **modeling decision** rather than a unique algebraic theorem:

| Model / Link | Inverse Mapping ($z \mapsto p$) | Key Property |
|---|---|---|
| **Logistic (Logit)** | $\sigma(z) = \frac{1}{1 + e^{-z}}$ | Symmetric around $z=0$; linear log-odds give exact odds ratios |
| **Probit** | $\Phi(z)$ (standard normal CDF) | Symmetric; assumes latent Gaussian noise, heavier tail decay than logit |
| **Complementary log-log** | $1 - e^{-e^z}$ | Asymmetric; approaches $1$ much faster than $0$ |

Logistic regression assumes the **log-odds** (logit) is linear in the predictors $\mathbf{x} \in \mathbb{R}^n$:
- If an outcome has probability $p \in (0, 1)$, its **odds** measure the ratio of event to non-event probability: $\operatorname{odds}(p) = \frac{p}{1 - p} \in (0, +\infty)$ (for instance, $p = 0.80 \implies \operatorname{odds} = 4.0$).
- Taking the natural logarithm maps $(0, +\infty)$ onto all of $\mathbb{R}$, matching the unconstrained linear score:

$$
z = \mathbf{w}^\top \mathbf{x} + b = \ln\left(\frac{p}{1 - p}\right)
$$

Exponentiating ($e^z = \frac{p}{1-p}$) and isolating $p$ yields the **logistic sigmoid**:

$$
p = \sigma(z) = \frac{e^z}{1 + e^z} = \frac{1}{1 + e^{-z}}
$$

**Why exponentiated weights interpret cleanly:** Because $\operatorname{odds}(\mathbf{x}) = \exp(\mathbf{w}^\top \mathbf{x} + b)$, increasing one coordinate $x_j$ by $+1$ while holding all other coordinates fixed multiplies the odds by:

$$
\frac{\operatorname{odds}(x_j + 1)}{\operatorname{odds}(x_j)} = e^{w_j}
$$

A positive weight $w_j > 0$ multiplies the odds by $e^{w_j} > 1$; note that raw weight magnitudes depend on feature units and scaling, so features on smaller scales look like larger weights unless standardized.

**Decision-boundary geometry & matrix notation:** Thresholding $\sigma(\mathbf{w}^\top \mathbf{x} + b) \ge \tau$ is equivalent to $z \ge \ln\left(\frac{\tau}{1-\tau}\right)$, defining an $(n-1)$-dimensional separating **hyperplane** in $\mathbb{R}^n$ orthogonal to $\mathbf{w}$ (at $\tau = 0.50$, simply $\mathbf{w}^\top \mathbf{x} + b = 0$). Across $m$ training samples stacked into design matrix $X \in \mathbb{R}^{m \times n}$ and label vector $\mathbf{y} \in \{0, 1\}^m$, logits compute simultaneously as $\mathbf{z} = X\mathbf{w} + b\mathbf{1} \in \mathbb{R}^m$.

> [!example]- Understand this derivation: from linear logit to sigmoid derivative $\sigma'(z) = \sigma(z)(1-\sigma(z))$
> 1. Starting from $z = \ln\frac{p}{1-p}$, exponentiate to get $e^z(1 - p) = p \implies e^z = p(1 + e^z) \implies p = \frac{e^z}{1 + e^z}$. Dividing top and bottom by $e^z$ gives $\frac{1}{1 + e^{-z}}$.
> 2. Differentiating $\sigma(z) = (1 + e^{-z})^{-1}$ via the chain rule yields:
> $$
> \sigma'(z) = -(1 + e^{-z})^{-2}(-e^{-z}) = \frac{1}{1 + e^{-z}} \cdot \frac{e^{-z}}{1 + e^{-z}} = \sigma(z)\bigl(1 - \sigma(z)\bigr)
> $$
> 3. Notice $\sigma'(z) \in (0, 0.25]$ for all finite $z \in \mathbb{R}$, peaking at $z = 0$ ($p = 0.5$) and decaying exponentially toward $0$ when $|z| \gg 0$.

**Unresolved question:** Given candidate parameters $(\mathbf{w}, b)$, what principled loss function measures how well predicted probabilities $\hat{p}_i$ fit observed binary labels $y_i \in \{0, 1\}$?

---

## 3. Deriving Binary Cross-Entropy from Bernoulli Likelihood

Under the conditional Bernoulli assumption $Y_i \mid \mathbf{x}_i \sim \text{Bernoulli}(p_i)$ with $p_i = \sigma(\mathbf{w}^\top \mathbf{x}_i + b)$, we can write both $y_i = 1$ ($P = p_i$) and $y_i = 0$ ($P = 1 - p_i$) in one compact likelihood factor:

$$
P(Y_i = y_i \mid \mathbf{x}_i; \mathbf{w}, b) = p_i^{y_i}(1 - p_i)^{1 - y_i}
$$

Assuming conditional independence across the $m$ training observations, the joint likelihood multiplies individual probabilities:

$$
L(\mathbf{w}, b) = \prod_{i=1}^{m} p_i^{y_i}(1 - p_i)^{1 - y_i}
$$

Taking the strictly increasing natural logarithm converts this fragile product of tiny numbers into a sum, and dividing the negative log-likelihood by $m$ converts likelihood maximization into minimization of **mean Binary Cross-Entropy (BCE)**:

$$
J(\mathbf{w}, b) = -\frac{1}{m}\ln L(\mathbf{w}, b) = -\frac{1}{m}\sum_{i=1}^{m}\Bigl[y_i\ln(\hat{p}_i) + (1 - y_i)\ln(1 - \hat{p}_i)\Bigr]
$$

When $y_i = 1$, loss reduces to $-\ln(\hat{p}_i)$, diverging smoothly toward $+\infty$ as $\hat{p}_i \to 0$; when $y_i = 0$, loss reduces to $-\ln(1 - \hat{p}_i)$, punishing confident false positives without bound.

---

## 4. Why BCE Is Convex While Sigmoid Squared Error Is Not

Optimization reliability depends on curvature: convex objectives have no strict suboptimal local minima, whereas non-convex losses can trap first-order methods on flat plateaus.

Express single-sample BCE directly in terms of logit $z = \mathbf{w}^\top\mathbf{x} + b$ by substituting $p = \frac{e^z}{1+e^z}$ and $1 - p = \frac{1}{1+e^z}$:

$$
\ell(z, y) = -y\ln\frac{e^z}{1+e^z} - (1-y)\ln\frac{1}{1+e^z} = \ln(1 + e^z) - yz
$$

Differentiating twice with respect to $z$ gives exact first and second derivatives:

$$
\frac{\partial \ell}{\partial z} = \frac{e^z}{1+e^z} - y = \sigma(z) - y, \qquad \frac{\partial^2 \ell}{\partial z^2} = \sigma'(z) = \sigma(z)\bigl(1 - \sigma(z)\bigr) > 0
$$

Because $z_i = \tilde{\mathbf{x}}_i^\top \boldsymbol{\theta}$ is linear in augmented parameter vector $\boldsymbol{\theta} = [\mathbf{w}; b]$ (where $\tilde{X} = [X,\; \mathbf{1}] \in \mathbb{R}^{m \times (n+1)}$ appends the constant $1$ intercept column), summing over all $m$ samples produces the full **Hessian matrix**:

$$
\nabla_{\boldsymbol{\theta}}^2 J(\boldsymbol{\theta}) = \frac{1}{m}\tilde{X}^\top D \tilde{X}, \qquad D = \operatorname{diag}\Bigl(\hat{p}_1(1-\hat{p}_1),\dots,\hat{p}_m(1-\hat{p}_m)\Bigr)
$$

Since every diagonal entry $d_i = \hat{p}_i(1-\hat{p}_i) \ge 0$, for any vector $\mathbf{v} \in \mathbb{R}^{n+1}$ we have $\mathbf{v}^\top \nabla^2 J\,\mathbf{v} = \frac{1}{m}\sum_{i=1}^m d_i (\tilde{\mathbf{x}}_i^\top \mathbf{v})^2 \ge 0$. Thus $J(\mathbf{w}, b)$ is **globally convex** (and strictly convex wherever $\tilde{X}$ has full column rank and probabilities remain strictly inside $(0, 1)$).

**Contrast with sigmoid squared error:** For $y = 1$, consider $\ell_{\text{sq}}(z, 1) = \frac{1}{2}(\sigma(z) - 1)^2$. Differentiating yields $\frac{\partial \ell_{\text{sq}}}{\partial z} = -p(1-p)^2$ and second derivative:

$$
\frac{\partial^2 \ell_{\text{sq}}}{\partial z^2} = p(1-p)^2(3p - 1)
$$

Notice that whenever $p < \frac{1}{3}$ ($z < -\ln 2 \approx -0.6931$—confident mistakes for $y=1$), $3p - 1 < 0$, making the curvature strictly **negative** (for instance, at $p = 0.1$, curvature is $0.1(0.9)^2(-0.7) = -0.0567 < 0$ whereas BCE curvature is $+0.09 > 0$). Although whether an aggregated sum over a specific dataset exhibits multiple local minima depends on $X$ and $\mathbf{y}$, squared error on $\sigma(z)$ is not globally convex and creates vanishing-gradient plateaus for confident mistakes.

---

## 5. Gradient Descent Derivation & Step-by-Step Numerical Trace

Applying the multivariable chain rule to single-sample BCE $\ell(p, y)$ exposes the exact algebraic cancellation that keeps gradient signals clean:

$$
\frac{\partial \ell}{\partial w_j} = \frac{\partial \ell}{\partial p} \cdot \frac{\partial p}{\partial z} \cdot \frac{\partial z}{\partial w_j}
$$

1. **Loss wrt probability:** $\frac{\partial \ell}{\partial p} = -\frac{y}{p} + \frac{1 - y}{1 - p} = \frac{p - y}{p(1 - p)}$.
2. **Probability wrt logit:** $\frac{\partial p}{\partial z} = p(1 - p)$.
3. **Logit wrt weight:** $\frac{\partial z}{\partial w_j} = x_j$.

Multiplying the three factors cancels $p(1-p)$ exactly, averaging across $m$ observations to yield:

$$
\frac{\partial J}{\partial w_j} = \frac{1}{m}\sum_{i=1}^{m}(\hat{p}_i - y_i)x_{ij}, \qquad \frac{\partial J}{\partial b} = \frac{1}{m}\sum_{i=1}^{m}(\hat{p}_i - y_i)
$$

Notice the two roles: $(\hat{p}_i - y_i)$ sets error direction and magnitude, while $x_{ij}$ scales how strongly parameter $w_j$ actually changes sample $i$'s logit $z_i$. (*Qualification:* BCE prevents the extra $\sigma'(z)$ saturation penalty in binary output heads, though vanishing gradients can still arise inside hidden layers of deep networks.)

Subtracting $\eta \nabla J$ steps in the direction of steepest local Euclidean decrease justified by $J(\boldsymbol{\theta} + \Delta\boldsymbol{\theta}) \approx J(\boldsymbol{\theta}) + \nabla J(\boldsymbol{\theta})^\top \Delta\boldsymbol{\theta}$; this guarantees local objective reduction at nonstationary points for sufficiently small learning rates $\eta$, whereas overly large $\eta$ overshoots the valley.

### Hand Trace on the Shared 4-Point Fixture
Using $x = [-2, -1, 1, 2]$, $y = [0, 0, 1, 1]$, starting from $w_0 = 0, b_0 = 0$ with $\eta = 1.0$:

**Prediction pass ($z_i = 0 \cdot x_i + 0 = 0$):**

| Sample $i$ | Feature $x_i$ | True Label $y_i$ | Logit $z_i$ | Predicted $\hat{p}_i$ |
|---:|---:|---|---:|---:|
| 1 | $-2$ | `0 — Negative` | $0.00$ | $0.50$ |
| 2 | $-1$ | `0 — Negative` | $0.00$ | $0.50$ |
| 3 | $+1$ | `1 — Positive` | $0.00$ | $0.50$ |
| 4 | $+2$ | `1 — Positive` | $0.00$ | $0.50$ |

**Learning update pass ($J(0,0) = -\ln(0.5) \approx 0.6931$):**

| Sample $i$ | Feature $x_i$ | Residual $\hat{p}_i - y_i$ | Weight Grad Contribution $(\hat{p}_i - y_i)x_i$ |
|---:|---:|---:|---:|
| 1 | $-2$ | $+0.50$ | $-1.00$ |
| 2 | $-1$ | $+0.50$ | $-0.50$ |
| 3 | $+1$ | $-0.50$ | $-0.50$ |
| 4 | $+2$ | $-0.50$ | $-1.00$ |

- **Mean gradients:** $\frac{\partial J}{\partial w} = \frac{-3.00}{4} = -0.75$, and $\frac{\partial J}{\partial b} = 0.00$.
- **Step 1 update:** $w_1 = 0 - 1.0(-0.75) = 0.75$, $b_1 = 0.00$.
- **Post-step evaluation:** Logits become $z = [-1.50, -0.75, +0.75, +1.50]$, yielding $\hat{p} \approx [0.1824, 0.3208, 0.6792, 0.8176]$ and dropping BCE from $0.6931$ to $J(0.75, 0) \approx 0.2941$.

> [!question] Concept Checkpoint — Single-Sample Update Direction
> On sample 4 ($x_4 = +2, y_4 = 1, \hat{p}_4 = 0.50$), why does gradient descent *increase* $w$ even though the update rule *subtracts* $\eta \frac{\partial J}{\partial w}$?
>
> > [!success]- Reveal Answer
> > The signed residual $\hat{p}_4 - y_4 = -0.50$ is negative and $x_4 = +2$ is positive, making the contribution $(\hat{p}_4 - y_4)x_4 = -1.00 < 0$. Subtracting a negative gradient produces $w_1 = w_0 - \eta(-0.75) > w_0$, increasing $z_4 = w x_4$ toward $y_4 = 1$.

---

## 6. L2 Regularization & Complete Linear Separation

On linearly separable data (like our 4-point fixture where every negative point has $x < 0$ and every positive point has $x > 0$), unregularized logistic regression has **no finite optimum**: any separating weights satisfy $y_i = 1 \implies z_i > 0$ and $y_i = 0 \implies z_i < 0$, so scaling $\|\mathbf{w}\| \to \infty$ sends $\sigma(z_i) \to y_i$ and BCE asymptotically toward $0$ while overfitting extreme confidence.

Adding an $L_2$ quadratic weight penalty restores coercivity and **strong convexity**:

$$
J_{\lambda}(\mathbf{w}, b) = -\frac{1}{m}\sum_{i=1}^{m}\Bigl[y_i\ln(\hat{p}_i) + (1-y_i)\ln(1-\hat{p}_i)\Bigr] + \frac{\lambda}{2}\|\mathbf{w}\|_2^2
$$

- **Modified weight gradient:** $\nabla_{\mathbf{w}} J_\lambda = \frac{1}{m}X^\top (\hat{\mathbf{p}} - \mathbf{y}) + \lambda \mathbf{w}$, pulling large weights proportionally back toward $0$ on every step (**weight decay / shrinkage**).
- **Unpenalized intercept $b$:** Leaving $b$ outside $\|\mathbf{w}\|_2^2$ ensures overall base-rate class priors are preserved rather than shrunk arbitrarily toward $p = 0.5$.
- **Uniqueness conditions:** Provided $\lambda > 0$ (with intercept $b$ remaining unregularized and both classes $0$ and $1$ present in bounded training data—actually strict convexity of the quadratic term holds on $\mathbf{w}$, while class presence keeps the intercept $b$ finite too), $J_\lambda(\mathbf{w}, b)$ is strictly convex and admits a **unique finite global minimizer**.
- **Hyperparameter bridge to libraries:** Libraries optimize different objective normalizations (e.g., `scikit-learn 1.4.2` weights summed loss by $C$ alongside $\frac{1}{2}\|\mathbf{w}\|_2^2$, giving exact equivalence at $C = \frac{1}{m\lambda}$, verified in [[Logistic Regression - Experimental Lab]]).

---

## 7. Numerical Stability in Finite-Precision Arithmetic

Mathematically, $\sigma(z) \in (0, 1)$ strictly for all finite $z \in \mathbb{R}$. In IEEE `float64` arithmetic, both forward probabilities and naive cross-entropy break at extreme logits:
1. **Sigmoid overflow guard:** Evaluating `1 / (1 + np.exp(-z))` directly at $z = -1000$ overflows `np.exp(1000)` to `+inf`. Writing piecewise exponential evaluation using only non-positive arguments $t = e^{-|z|} \in (0, 1]$ (`1 / (1 + t)` for $z \ge 0$, `t / (1 + t)` for $z < 0$) avoids overflow without relying on lazy branching.
2. **Eliminating `log(0)` and subtraction cancellation:** Naive `-(y*ln(p) + (1-y)*ln(1-p))` yields `0.0 * (-inf) = NaN` once large $z$ rounds $\sigma(z)$ to `1.0`. Even rewriting BCE as $\ln(1 + e^z) - yz$ (`np.logaddexp(0, z) - y*z`) suffers **catastrophic subtraction cancellation** when $z = 50, y = 1$: $\ln(1 + e^{50}) \approx 50.0$ rounds the tiny true loss $\ln(1 + e^{-50}) \approx 1.93 \times 10^{-22}$ completely to `0.0`! Instead, exploit the symmetry $1 - \sigma(z) = \sigma(-z)$ to fold binary labels cleanly into a single **signed-logit** expression with zero subtraction:

$$
\ell(z, y) = \begin{cases} \ln(1 + e^{-z}), & y = 1 \\ \ln(1 + e^{+z}), & y = 0 \end{cases} \quad\Longleftrightarrow\quad \ell(z, y) = \ln\Bigl(1 + e^{(1 - 2y)z}\Bigr)
$$

*(This requires $y \in \{0, 1\}$; for soft probability targets $y \in (0, 1)$, blend or clamp safely.)*

---

## 8. Threshold Decisions, Limitations & Multiclass Handoff

Changing threshold $\tau$ in $\hat{y} = \mathbf{1}[\hat{p} \ge \tau]$ **never changes fitted weights $(\mathbf{w}, b)$ or predicted probabilities $\hat{p}_i$**—it only changes which probabilities cross the decision boundary. Raising $\tau$ cannot increase the count of predicted positives ($\text{TP}$ and $\text{FP}$ cannot rise), **yet precision $\frac{\text{TP}}{\text{TP}+\text{FP}}$ is NOT guaranteed to increase monotonically**!

### Discriminating Threshold Counterexample ($\tau = 0.50 \to 0.70$)

| Case $i$ | Predicted Probability $\hat{p}_i$ | Actual Class $y_i$ | Prediction at $\tau = 0.50$ | Prediction at $\tau = 0.70$ |
|---:|---:|---|---|---|
| 1 | $0.95$ | `1 — Positive` | Positive (`TP`) | Positive (`TP`) |
| 2 | $0.85$ | `0 — Negative` | Positive (`FP`) | Positive (`FP`) |
| 3 | $0.65$ | `1 — Positive` | Positive (`TP`) | Negative (`FN`) |
| 4 | $0.55$ | `1 — Positive` | Positive (`TP`) | Negative (`FN`) |
| 5 | $0.40$ | `0 — Negative` | Negative (`TN`) | Negative (`TN`) |
| 6 | $0.20$ | `0 — Negative` | Negative (`TN`) | Negative (`TN`) |

- **At $\tau = 0.50$:** `TP = 3`, `FP = 1` $\implies$ **Precision = $75.0\%$ (`3/4`)**, **Recall = $100.0\%$ (`3/3`)**.
- **At $\tau = 0.70$:** Correct positives at $0.65$ and $0.55$ drop below $\tau$ while false positive $0.85$ remains above $\tau$: `TP = 1`, `FP = 1` $\implies$ **Precision drops to $50.0\%$ (`1/2`)** alongside **Recall = $33.3\%$ (`1/3`)**!

### Evaluation, Scope Limitations & Extensions
- **Discrimination vs. calibration:** Threshold metrics (accuracy, $F_1$, ROC-AUC) test ranking discrimination, whereas log-loss (BCE) and reliability diagrams test whether predicted probabilities match empirical event frequencies.
- **Model limitations & failure diagnosis:** Standard logistic regression assumes linear log-odds in engineered features $\mathbf{x}$; XOR-like nonlinear boundaries require explicit feature maps/splines or neural models, while severe class imbalance shifts base-rate intercepts (requiring careful cost weighting rather than blind resampling if calibrated probabilities matter) and target leakage inflates validation AUC artificially.
- **Multiclass extension:** $K$-class classification generalizes sigmoid + binary log-odds either via **One-vs-Rest** independent binary models or **multinomial softmax** ($P(Y=k \mid \mathbf{x}) = \frac{e^{z_k}}{\sum_{j=1}^K e^{z_j}}$) minimizing categorical cross-entropy.

---

## 9. Mental Model, Notation Reference & Bundle Links

**Mental Model:** Logistic regression separates **probabilistic modeling** (find linear log-odds weights $(\mathbf{w}, b)$ minimizing convex regularized Bernoulli negative log-likelihood via signed-logit stability) from **downstream action rules** (choose $\tau$ based on asymmetric false-positive vs. false-negative costs without expecting monotonic precision).

**Trailing Notation Reference:** $m$ samples · $n$ features · $X \in \mathbb{R}^{m \times n}$ design matrix · $\mathbf{x}_i$ input vector · $y_i \in \{0, 1\}$ binary label · $z = \mathbf{w}^\top \mathbf{x} + b$ logit · $\sigma(z)$ sigmoid · $\hat{p}_i$ predicted probability · $\eta$ step size · $\lambda, C$ $L_2$ regularization parameters · $\tau$ classification threshold.

- **Companions in this bundle:** [[Logistic Regression - Experimental Lab]] · [[Logistic Regression - Cheatsheet & Interview Q&A]]
