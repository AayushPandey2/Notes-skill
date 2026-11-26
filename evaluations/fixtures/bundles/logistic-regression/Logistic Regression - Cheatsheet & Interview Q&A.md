---
id: eval-golden-logistic-regression-mastery
aliases:
  - Logistic Regression - Cheatsheet & Interview Q&A
topic: Logistic Regression
tags:
  - domain/ml
  - subject/machine-learning
  - topic/logistic-regression
nexttopics: []
---

# Logistic Regression — Cheat Sheet, Interview Q&A & Practice

> [!info] Bundle Navigation
> - **Theory:** [[Logistic Regression]] · **Lab:** [[Logistic Regression - Experimental Lab]]

## 1. Quick Reference & Formula Sheet

| Concept | Formula / Rule | Key Condition / Pitfall |
|---|---|---|
| **Log-odds link** | $z = \mathbf{w}^\top \mathbf{x} + b = \ln\frac{p}{1-p}$ | Linear in parameters, not directly linear in probability $p$ |
| **Sigmoid probability** | $\sigma(z) = \frac{1}{1+e^{-z}} \in (0, 1)$ | Finite precision saturates to `0.0`/`1.0` for large $\|z\|$ |
| **Mean BCE gradient** | $\nabla_{\mathbf{w}} J = \frac{1}{m}\sum_{i=1}^m (\hat{p}_i - y_i)\mathbf{x}_i$ | Convex objective; requires logits stabilization in code |
| **Regularization conversion** | $C = \frac{1}{m\lambda}$ (for mean BCE $+\frac{\lambda}{2}\|\mathbf{w}\|^2$) | Never assume $C = 1/\lambda$ without checking batch $m$ scaling |
| **Decision rule** | $\hat{y} = \mathbf{1}[\hat{p} \ge \tau]$ | Changing $\tau$ alters precision/recall without changing $\mathbf{w}, b$ |

---

## 2. Tiered Interview / Viva Questions & Answers

### Beginner-Level Questions (Q1–Q2)

**Q1. Why does ordinary linear regression fail as a probability classifier even if we clip outputs to $[0, 1]$?**

> [!tip]- Answer
> Clipping forces outputs inside $[0, 1]$ after fitting, but least-squares loss still measures squared distance to $0$ and $1$: distant well-classified examples pull the regression line awkwardly across the midpoint boundary, and clipped flat regions have zero gradient. Modeling log-odds as linear maps scores smoothly through $\sigma(z)$ while convex BCE keeps gradients informative.

**Q2. What does a linear logit $z = 0$ correspond to in odds and probability?**

> [!tip]- Answer
> At $z = 0$, $\text{odds} = e^0 = 1$ (even $1:1$ odds) and $\sigma(0) = \frac{1}{1+1} = 0.50$.

### Intermediate-Level Questions (Q3–Q4)

**Q3. Suppose sample $x = 3$ has true label $y = 0$ and the model predicts $\hat{p} = 0.80$. In which direction does one gradient descent step move $w$, and why?**

> [!tip]- Answer
> The residual is $\hat{p} - y = +0.80$, so the sample gradient contribution is $(+0.80)(3) = +2.40 > 0$. Because gradient descent subtracts $\eta \nabla_w J$, subtracting a positive quantity decreases $w$, lowering $z = wx + b$ and reducing $\hat{p}$ toward $0$.

**Q4. Why does changing the classification threshold from $\tau = 0.50$ to $\tau = 0.70$ leave predicted probabilities unchanged yet potentially alter precision and recall?**

> [!tip]- Answer
> Fitted parameters $(\mathbf{w}, b)$ come solely from minimizing training BCE before thresholding. Raising $\tau$ to $0.70$ leaves every $\hat{p}_i = \sigma(\mathbf{w}^\top \mathbf{x}_i + b)$ intact while converting predictions in $[0.50, 0.70)$ from positive to negative, changing downstream TP/FP/TN/FN counts.

### Advanced-Level Questions (Q5–Q6)

**Q5. Why must a scikit-learn `LogisticRegression` user scale `C = 1 / (m * lambda)` instead of `C = 1 / lambda` when matching PyTorch/NumPy mean BCE with weight decay $\lambda$?**

> [!tip]- Answer
> Standard NumPy/PyTorch training divides cross-entropy by batch/dataset size $m$ before adding $\frac{\lambda}{2}\|\mathbf{w}\|^2$. Scikit-learn sums unnormalized cross-entropy across all $m$ samples and multiplies that sum by $C$ before adding $\frac{1}{2}\|\mathbf{w}\|^2$. Equating the ratios requires $C = \frac{1}{m\lambda}$; omitting $m$ makes regularization $m$ times too weak.

**Q6. What breaks in unregularized logistic regression when training classes are strictly linearly separable?**

> [!tip]- Answer
> Any separating vector $\mathbf{w}$ satisfies $y_i \to 1$ logits $>0$ and $y_i \to 0$ logits $<0$, so scaling $\|\mathbf{w}\| \to \infty$ drives $\sigma(z_i) \to y_i$ and pushes BCE arbitrarily close to $0$ with no finite minimizer. Adding $L_2$ weight decay creates a strictly convex problem with a unique finite solution.

---

## 3. Applied Practice Problems (Progressive Guidance Fading)

### Problem 1 (Complete Walkthrough): Compute Step-1 BCE Residual & Direction
**Given:** Single training point $x = -2$, label $y = 1$, current weight $w = 0$, bias $b = 0$, learning rate $\eta = 0.5$. Compute $z, \hat{p}, \frac{\partial J}{\partial w}, \frac{\partial J}{\partial b}$, and updated $(w_1, b_1)$.

> [!tip]- Solution
> 1. **Score & probability:** $z = 0(-2) + 0 = 0 \implies \hat{p} = \sigma(0) = 0.5$.
> 2. **Gradients ($m=1$):** $\frac{\partial J}{\partial w} = (0.5 - 1)(-2) = +1.0$; $\frac{\partial J}{\partial b} = 0.5 - 1 = -0.5$.
> 3. **Update ($\eta = 0.5$):** $w_1 = 0 - 0.5(1.0) = -0.5$; $b_1 = 0 - 0.5(-0.5) = +0.25$.
> 4. **Check:** New score $z_1 = (-0.5)(-2) + 0.25 = +1.25 > 0$, pushing $\hat{p}_1 > 0.5$ toward $y = 1$. **Final:** $\boxed{(w_1, b_1) = (-0.50,\; +0.25)}$.

### Problem 2 (Partial Scaffolding — Complete the Calculation): Hyperparameter Matching Across $m = 100$
**Given:** Team A minimizes $J_A(\mathbf{w}) = \frac{1}{100}\sum_{i=1}^{100} \ell(z_i, y_i) + \frac{0.02}{2}\|\mathbf{w}\|^2$. Fill in the equivalent scikit-learn `C` so `LogisticRegression` minimizes the same scaled objective.

> [!tip]- Solution
> Multiply $J_A$ by $m = 100$ to match scikit-learn's summed cross-entropy, divide by $m\lambda = 100 \times 0.02 = 2.0$, and apply $C = \frac{1}{m\lambda} = \frac{1}{2.0} = 0.50$. Using `C = 1 / 0.02 = 50` would be wrong by $100\times$. **Final:** $\boxed{C = 0.50}$.

### Problem 3 (Independent Transfer): Numerical Saturation Diagnosis
**Given:** A student writes `loss = -np.mean(y * np.log(sigmoid(z)) + (1 - y) * np.log(1 - sigmoid(z)))` and observes `NaN` on sample $z = 50, y = 1$. Explain why it happens in `float64` and write the invariant logits expression that prevents it.

> [!tip]- Solution
> At $z = 50$, $e^{-50} \approx 1.93 \times 10^{-22} < \epsilon_{\text{mach}}$ (`2.22e-16`), so `sigmoid(50)` rounds to exact `1.0` in `float64`. Even though `y = 1` multiplies `(1 - 1.0)` by zero, IEEE arithmetic evaluates `np.log(0.0) = -inf` and `(1 - y) * (-inf) = 0.0 * (-inf) = NaN`. Using $\ln(1 + e^z) - y z$ via `np.logaddexp(0.0, z) - y * z` stays finite ($\approx 0.0$ for $z=50, y=1$) without ever computing `log(0)`.
