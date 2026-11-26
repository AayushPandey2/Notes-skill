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

> [!info] Learning Metadata
> - **Difficulty:** Intermediate (requires linear equations and basic derivatives; explained locally before first use)
> - **Prerequisites:** Linear weighted sum ($w x + b$), basic exponential function ($e^z$), and single-variable derivative intuition
> - **Learning objectives:**
>   1. Explain why linear regression fails as a probability classifier and trace the transition $z \to \text{odds} \to \text{log-odds} \to \sigma(z)$.
>   2. Derive and compute Binary Cross-Entropy (BCE) loss and its gradient with respect to $(w, b)$, and explain why BCE is convex while MSE on $\sigma(z)$ is non-convex.
>   3. Separate model training from downstream classification thresholding ($\tau$), diagnosing threshold vs. regularization trade-offs.

**Table of Contents**
- [[#1. Why Linear Scores Cannot Directly Output Probabilities|1. Why Linear Scores Fail]]
- [[#2. From Linear Score to Odds, Log-Odds, and Sigmoid|2. Score to Odds to Sigmoid]]
- [[#3. Measuring Error with Binary Cross-Entropy|3. Binary Cross-Entropy Loss]]
- [[#4. Learning Parameters via Gradient Descent|4. Gradient Descent & Running Trace]]
- [[#5. Decision Thresholds vs. Fitted Probabilities|5. Thresholds vs. Model]]
- [[#6. Mental Model & Companion Navigation|6. Mental Model & Bundle Links]]

---

## 1. Why Linear Scores Cannot Directly Output Probabilities

Suppose a spam filter predicts whether an email is spam ($y = 1$) or ordinary mail ($y = 0$) from a continuous feature $x$ (such as standardized suspicious-link score). Fitting ordinary linear regression $\hat{y} = w x + b$ creates two structural failures:

1. **Unbounded outputs:** As $x$ grows large in either direction, $w x + b$ sweeps across $(-\infty, +\infty)$ instead of remaining inside valid probability bounds $[0, 1]$.
2. **Boundary distortion by confident examples:** A single email at $x = 10$ with label $y = 1$ pulls a least-squares line steeply upward so that borderline emails around $x = 0.5$ get pulled across the $0.5$ boundary, even though $x = 10$ was already clearly spam.

**Unresolved question:** How can we keep the simplicity of a linear weighted score $z = \mathbf{w}^\top \mathbf{x} + b \in \mathbb{R}$ while mapping it smoothly into $(0, 1)$?

---

## 2. From Linear Score to Odds, Log-Odds, and Sigmoid

Instead of mapping $z$ directly to probability $p \in (0, 1)$, move in two small steps through **odds**:

- **Probability to odds:** If an event occurs with probability $p$, its **odds** measure how likely success is relative to failure: $\text{odds}(p) = \frac{p}{1 - p} \in (0, +\infty)$. For example, $p = 0.75$ corresponds to odds $\frac{0.75}{0.25} = 3$ (three times as likely to be class $1$ as class $0$).
- **Odds to log-odds (logit):** Odds are asymmetric and bounded below by $0$. Taking the natural logarithm maps $(0, +\infty)$ onto the entire real line $(-\infty, +\infty)$, matching the unbounded range of a linear score:

$$
z = \mathbf{w}^\top \mathbf{x} + b = \ln\left(\frac{p}{1 - p}\right)
$$

> [!example]- Understand this formula step by step
> 1. $\mathbf{w}^\top \mathbf{x} + b$ produces an unconstrained real score $z \in (-\infty, +\infty)$ combining input evidence $\mathbf{x}$ with learned weights $\mathbf{w}$ and bias $b$.
> 2. $\frac{p}{1-p}$ converts probability $p \in (0, 1)$ into positive odds $\in (0, +\infty)$.
> 3. $\ln(\cdot)$ makes the scale symmetric around $z = 0$ (where $p = 0.5$ gives $\ln 1 = 0$): reversing class labels simply negates $z$.

Solving $z = \ln\left(\frac{p}{1 - p}\right)$ for $p$ by exponentiating both sides ($e^z = \frac{p}{1 - p}$, then $p = e^z(1 - p)$) yields the **logistic sigmoid**:

$$
p = \sigma(z) = \frac{1}{1 + e^{-z}}
$$

> [!example]- Understand this formula step by step
> 1. Dividing numerator and denominator of $\frac{e^z}{1 + e^z}$ by $e^z$ gives $\frac{1}{1 + e^{-z}}$, which stays strictly inside $(0, 1)$ mathematically for every finite $z \in \mathbb{R}$.
> 2. As $z \to +\infty$, $e^{-z} \to 0$ and $\sigma(z) \to 1$; as $z \to -\infty$, $e^{-z} \to +\infty$ and $\sigma(z) \to 0$.
> 3. **Key derivative identity:** Differentiating yields $\sigma'(z) = \sigma(z)\bigl(1 - \sigma(z)\bigr)$, peaking at $0.25$ when $z = 0$ and vanishing in the saturation tails ($|z| \gg 0$).
> 4. **Numerical boundary:** In finite `float64` arithmetic, large $|z|$ rounds to exact `0.0` or `1.0`, so production loss code computes cross-entropy directly from logits $z$ rather than taking $\ln(\sigma(z))$.

**Unresolved question:** Now that parameters $(\mathbf{w}, b)$ produce probabilities $\hat{p}_i = \sigma(\mathbf{w}^\top \mathbf{x}_i + b)$, which objective function should we minimize to fit $(\mathbf{w}, b)$ cleanly?

---

## 3. Measuring Error with Binary Cross-Entropy

Squared error $(\sigma(z) - y)^2$ paired with sigmoid saturation produces a **non-convex** loss landscape with flat plateaus where wrong confident predictions have tiny gradients $\sigma'(z) \approx 0$. Instead, modeling $y_i \mid \mathbf{x}_i \sim \text{Bernoulli}(\hat{p}_i)$ and maximizing log-likelihood (equivalently minimizing negative log-likelihood averaged over $m$ training samples) gives **Binary Cross-Entropy (BCE)**:

$$
J(\mathbf{w}, b) = -\frac{1}{m}\sum_{i=1}^{m}\Bigl[y_i \ln(\hat{p}_i) + (1 - y_i)\ln(1 - \hat{p}_i)\Bigr]
$$

> [!example]- Understand this formula step by step
> 1. When $y_i = 1$, only $-\ln(\hat{p}_i)$ remains: predicting $\hat{p}_i \approx 1$ gives near-zero penalty, while confident error $\hat{p}_i \to 0$ sends penalty toward $+\infty$.
> 2. When $y_i = 0$, only $-\ln(1 - \hat{p}_i)$ remains: confident false positives $\hat{p}_i \to 1$ likewise diverge smoothly.
> 3. **Convexity & gradient benefit:** $J(\mathbf{w}, b)$ is convex with respect to $(\mathbf{w}, b)$, and the $\frac{1}{\hat{p}_i(1-\hat{p}_i)}$ term from $\ln$ cancels the $\hat{p}_i(1-\hat{p}_i)$ factor from $\sigma'(z)$, eliminating sigmoid gradient saturation during training.

---

## 4. Learning Parameters via Gradient Descent

Using the chain rule and the cancellation $\sigma'(z) = \hat{p}(1-\hat{p})$, the partial derivatives of $J(\mathbf{w}, b)$ simplify cleanly to:

$$
\frac{\partial J}{\partial w_j} = \frac{1}{m}\sum_{i=1}^{m}(\hat{p}_i - y_i)x_{ij}, \qquad \frac{\partial J}{\partial b} = \frac{1}{m}\sum_{i=1}^{m}(\hat{p}_i - y_i)
$$

> [!example]- Understand this formula step by step
> 1. $(\hat{p}_i - y_i)$ is the signed probability residual: positive when $\hat{p}_i$ is too high above $y_i$, negative when too low.
> 2. Subtracting $\eta \nabla J$ steps in the steepest local decrease direction justified by first-order expansion $J(\theta + \Delta\theta) \approx J(\theta) + \nabla J(\theta)^\top \Delta\theta$; this guarantees local reduction only for sufficiently small learning rates $\eta$ (overshooting if $\eta$ is too large).

### Complete Hand-Worked Step on Shared 4-Point Fixture
Consider $m = 4$ 1D training points $(-2, 0), (-1, 0), (1, 1), (2, 1)$ starting at $w_0 = 0, b_0 = 0$ with $\eta = 1.0$:

| Sample $i$ | Input $x_i$ | Label $y_i$ | Score $z_i$ | Predicted $\hat{p}_i$ | Residual $\hat{p}_i - y_i$ | Contribution $(\hat{p}_i - y_i)x_i$ |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | $-2$ | `0 — Negative` | $0.0$ | $0.50$ | $+0.50$ | $-1.00$ |
| 2 | $-1$ | `0 — Negative` | $0.0$ | $0.50$ | $+0.50$ | $-0.50$ |
| 3 | $+1$ | `1 — Positive` | $0.0$ | $0.50$ | $-0.50$ | $-0.50$ |
| 4 | $+2$ | `1 — Positive` | $0.0$ | $0.50$ | $-0.50$ | $-1.00$ |

- **Initial loss:** $J(0, 0) = -\ln(0.5) = \ln 2 \approx 0.6931$.
- **Gradients:** $\frac{\partial J}{\partial w} = \frac{-1.00 - 0.50 - 0.50 - 1.00}{4} = -0.75$, and $\frac{\partial J}{\partial b} = 0$.
- **One update ($\eta = 1.0$):** $w_1 = 0 - 1.0(-0.75) = 0.75$, $b_1 = 0$.
- **Updated probabilities & loss:** $z = [-1.5, -0.75, +0.75, +1.5]$ gives $\hat{p} \approx [0.1824, 0.3208, 0.6792, 0.8176]$, dropping BCE to $J(0.75, 0) \approx 0.2941$.

> [!question] Concept Checkpoint — Predicting Update Direction
> On sample 4 ($x_4 = +2, y_4 = 1, \hat{p}_4 = 0.50$), why does gradient descent *increase* $w$ even though we *subtract* $\eta \frac{\partial J}{\partial w}$?
>
> > [!success]- Reveal Answer
> > Because $\hat{p}_4 - y_4 = -0.50 < 0$ while $x_4 = +2 > 0$, the product contribution $(\hat{p}_4 - y_4)x_4 = -1.00$ is negative. Subtracting a negative gradient produces $w_1 = w_0 - \eta(-0.75) = w_0 + 0.75$, pushing $z_4 = w x_4$ upward toward $y_4 = 1$.

---

## 5. Decision Thresholds vs. Fitted Probabilities

Logistic regression outputs a calibrated score *only under well-specified model and data conditions*; turning probability $\hat{p}$ into a binary class prediction $\hat{y} = \mathbf{1}[\hat{p} \ge \tau]$ requires choosing a **decision threshold $\tau$**:

- Changing $\tau$ (e.g., from $0.50$ to $0.70$) **does not alter fitted parameters $(\mathbf{w}, b)$ or probabilities $\hat{p}_i$**; it only shifts which predictions count as positive.
- Higher $\tau$ lowers false positives (usually improving precision when positives still exist above $\tau$) at the cost of missing borderline positives (lowering recall). Lower $\tau$ catches more true positives while admitting more false alarms.
- **Misconception trap:** Lowering $\tau$ predicts *more* positives, never fewer.

---

## 6. Mental Model & Companion Navigation

**Mental Model:** Logistic regression separates **ranking evidence** (fit $(\mathbf{w}, b)$ by convex log-odds cross-entropy) from **acting under asymmetric costs** (choose decision threshold $\tau$ afterward). Notice that linearly separable data pushes unregularized weights toward $\pm\infty$ to drive $\sigma(z) \to \{0,1\}$, which is why $L_2$ regularization (`alpha` / `C`) is tested next in the lab.

**Trailing Notation Reference:** $m$ samples · $x_i$ feature · $y_i \in \{0,1\}$ label · $z = \mathbf{w}^\top\mathbf{x}+b$ logit · $\sigma(z)$ sigmoid · $\tau$ decision threshold · $\eta$ learning rate · $\lambda, C$ $L_2$ regularization terms.

- **Companions in this bundle:** [[Logistic Regression - Experimental Lab]] · [[Logistic Regression - Cheatsheet & Interview Q&A]]
