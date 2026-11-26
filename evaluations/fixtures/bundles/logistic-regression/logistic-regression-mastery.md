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

*Scope note:* Covers binary logistic regression through $L_2$ regularization and threshold behavior (`12` targeted questions spanning all 10 mastery dimensions + `4` progressively faded problems, scaled proportionally to the single-chapter binary model scope).

> [!info] Bundle Navigation
> - **Theory:** [[logistic-regression|Logistic Regression]] · **Lab:** [[logistic-regression-lab|Logistic Regression - Experimental Lab]]

## 1. Quick Reference & Formula Sheet

| Concept | Formula / Rule | Key Condition / Pitfall |
|---|---|---|
| **Log-odds & odds ratio** | $z = \mathbf{w}^\top \mathbf{x} + b = \ln\frac{p}{1-p}$, $\frac{\operatorname{odds}(x_j+1)}{\operatorname{odds}(x_j)} = e^{w_j}$ | Assumes linear log-odds; weight sizes depend on feature scales |
| **Sigmoid & derivative** | $\sigma(z) = \frac{1}{1+e^{-z}}$, $\sigma'(z) = p(1-p) \le 0.25$ | Use $t = e^{-\|z\|}$ to avoid eager `np.where` overflow in code |
| **Signed-logit BCE** | $\ell(z, y) = \ln(1 + e^{(1-2y)z})$ ($y \in \{0,1\}$) | Avoids both `log(0)` and `logaddexp(0, z) - y*z` cancellation |
| **Convexity / Hessian** | $\nabla_{\boldsymbol{\theta}}^2 J = \frac{1}{m}\tilde{X}^\top D \tilde{X} \succeq 0$ | Regularized objective ($\lambda>0$) keeps $\mathbf{w}^*$ unique on separable data |
| **Regularization match** | $C = \frac{1}{m\lambda}$ (mean BCE + $\frac{\lambda}{2}\|\mathbf{w}\|^2$ vs. `sklearn 1.4.2`) | Always verify batch-size $m$ scaling and optimizer penalty rules |
| **Decision rule** | $\hat{y} = \mathbf{1}[\hat{p} \ge \tau]$ | Changing $\tau$ **can** alter precision/recall if scores cross $\tau$, without changing $\mathbf{w}, b$ |

---

## 2. Tiered Interview / Viva Questions & Answers

### Beginner-Level Questions (Q1–Q4: *Recognition, Recall, Explanation, Execution*)

**Q1. (*Recognition*) Which expression gives the modeled probability ratio ("odds") from a linear score $z = \mathbf{w}^\top\mathbf{x} + b$, and when does a logit of $0$ occur?**

> [!tip]- Answer
> $\operatorname{odds}(p) = \frac{p}{1 - p} = e^z$. A logit $z = 0$ occurs when $p = 0.50$, giving even $1:1$ odds ($e^0 = 1$).

**Q2. (*Explanation*) Why does clipping ordinary linear regression outputs $\hat{y} = \mathbf{w}^\top \mathbf{x} + b$ to $[0, 1]$ fail to produce a clean classifier?**

> [!tip]- Answer
> Distinguish **post-fit clipping** (clipping predictions after OLS finishes, which leaves an underlying least-squares fit pulled by squared distance on extreme points and violates Bernoulli mean–variance structure) from **in-training clipping** (which yields zero gradient everywhere outside $[0, 1]$, stalling learning on confident misclassified points). Logistic regression models linear log-odds directly with smooth $\sigma(z)$ and convex BCE.

**Q3. (*Recall*) What is the mathematical relationship between feature weight $w_j$ and predicted odds, holding other features constant?**

> [!tip]- Answer
> A $+1$ unit increase in $x_j$ multiplies the predicted odds by $e^{w_j}$ ($\frac{\operatorname{odds}(x_j + 1)}{\operatorname{odds}(x_j)} = e^{w_j}$). Because odds depend on feature units, doubling $x_j$'s numerical scale halves $w_j$.

**Q4. (*Execution*) For a single-sample update (batch size $m=1$) on $(x = 3, y = 0)$ where the current model predicts $\hat{p} = 0.80$, calculate $\frac{\partial \ell}{\partial w}$ and state which direction gradient descent moves $w$.**

> [!tip]- Answer
> The residual is $\hat{p} - y = +0.80$, so $\frac{\partial \ell}{\partial w} = (+0.80)(3) = +2.40$. Subtracting $\eta \nabla_w \ell$ moves $w$ downward (in a multi-sample batch, this sample contributes $+2.40/m$ to the average gradient; the net step depends on all samples).

### Intermediate-Level Questions (Q5–Q8: *Derivation/Explanation, Prediction, Discrimination, Critique*)

**Q5. (*Explanation*) Trace how mean BCE arises from Bernoulli maximum likelihood and why its Hessian is positive semidefinite.**

> [!tip]- Answer
> Modeling $P(Y_i=y_i \mid \mathbf{x}_i) = p_i^{y_i}(1-p_i)^{1-y_i}$ across conditionally independent points multiplies likelihoods $\prod_i p_i^{y_i}(1-p_i)^{1-y_i}$. Taking $-\frac{1}{m}\ln L$ converts products to sums, giving mean BCE. Differentiating $\ell(z, y) = \ln(1+e^z) - yz$ twice yields $\ell''(z) = p(1-p) \ge 0$, so the Hessian $\frac{1}{m}\tilde{X}^\top D \tilde{X}$ is positive semidefinite because every entry $d_i = p_i(1-p_i) \ge 0$.

**Q6. (*Prediction*) If a practitioner raises $\tau$ from $0.50$ to $0.70$, which prediction counts are guaranteed not to increase, and does precision always improve?**

> [!tip]- Answer
> Only observations whose predicted probabilities $\hat{p}_i$ cross $\tau$ change classification: predicted positives ($\text{TP} + \text{FP}$), $\text{TP}$, and $\text{FP}$ are guaranteed **not to increase** (staying identical if no $\hat{p}_i \in [0.50, 0.70)$). Precision does **not** always increase—if true positives fall in $[0.50, 0.70)$ while false positives sit above $0.70$, precision drops (e.g., $75.0\% \to 50.0\%$).

**Q7. (*Discrimination*) How do log-loss (BCE) and ROC-AUC evaluate two logistic classifiers differently?**

> [!tip]- Answer
> ROC-AUC measures **ranking discrimination** (probability a random positive outranks a random negative, invariant to monotonic probability rescaling), whereas log-loss penalizes **probability miscalibration** as well as ordering mistakes (confident wrong probabilities suffer unbounded logarithmic penalties).

**Q8. (*Critique*) Why is converting NumPy/PyTorch `weight_decay` or $\lambda$ via `C = 1 / lambda` unreliable?**

> [!tip]- Answer
> It fails in two ways: first, batch normalization differs (for unweighted mean BCE $+\frac{\lambda}{2}\|\mathbf{w}\|^2$ matching `scikit-learn 1.4.2`'s $C\sum \ell_i + \frac{1}{2}\|\mathbf{w}\|^2$, equivalence requires $C = \frac{1}{m\lambda}$, not $1/\lambda$); second, in PyTorch, `SGD(weight_decay=...)` couples $L_2$ into the gradient under standard rules whereas decoupled optimizers such as `AdamW` apply weight shrinkage directly to weights independently of gradient scaling—never interchangeable with adding $\frac{\lambda}{2}\|\mathbf{w}\|^2$ to the loss.

### Advanced-Level Questions (Q9–Q12: *Diagnosis, Construction, Critique, Transfer*)

**Q9. (*Diagnosis*) During unregularized logistic regression on a clean dataset, weights grow steadily past $\|\mathbf{w}\| > 50$ while training loss keeps shrinking toward zero. What caused this, and when does $L_2$ regularization guarantee a unique finite optimum?**

> [!tip]- Answer
> The classes are **linearly separable**: scaling separating weights $\mathbf{w}$ toward $\infty$ pushes logits to $\pm\infty$ and $\sigma(z_i) \to y_i$ with no finite minimum. Adding $\frac{\lambda}{2}\|\mathbf{w}\|_2^2$ guarantees a **unique finite global minimizer** when $\lambda > 0$, the intercept $b$ remains unregularized while both classes $0$ and $1$ appear in bounded data (keeping $b$ finite alongside coercive $\mathbf{w}$).

**Q10. (*Construction*) Explain why `np.where(z >= 0, 1/(1+np.exp(-z)), np.exp(z)/(1+np.exp(z)))` still warns on extreme negative `z`, and how `np.exp(-np.abs(z))` fixes it.**

> [!tip]- Answer
> NumPy evaluates both argument expressions **before** selecting elements in `np.where`, so `np.exp(-z)` overflows on large negative $z$ even though the second branch is kept. Setting `t = np.exp(-np.abs(z))` keeps the exponent $\le 0$ for every finite $z$ before choosing `1/(1+t)` vs. `t/(1+t)`.

**Q11. (*Critique*) A colleague claims *"MSE on sigmoid outputs always fails because every empirical sum of squares is concave everywhere."* Evaluate both what is true and what is overclaimed.**

> [!tip]- Answer
> Single-sample squared error on $y=1$ has second derivative $p(1-p)^2(3p-1)$, which is strictly **negative** (concave/plateauing) whenever $p < \frac{1}{3}$ ($z < -\ln 2$), making gradient steps slow for confident errors. However, the aggregate loss over an entire dataset is not concave everywhere (e.g., where $p > \frac{1}{3}$)—the accurate statement is that sigmoid squared error lacks global convexity and admits non-convex flat plateaus.

**Q12. (*Transfer*) A fraud-detection logistic regression model produces well-calibrated fraud probabilities $\hat{p}$, but each missed fraud costs 9x more than flagging a legitimate charge for SMS confirmation. Should you reweight classes during BCE training or shift the threshold $\tau$?**

> [!tip]- Answer
> Keep $\hat{p}$ calibrated by training on unweighted empirical BCE (unless data sampling itself was biased) and lower the **decision threshold** via Bayes-optimal cost balancing: predict fraud when expected false-negative cost $9\hat{p}$ exceeds false-positive cost $1(1-\hat{p})$, giving $\tau = \frac{1}{1+9} = 0.10$. Reweighting training data distorts predicted log-odds and breaks calibration unless mathematically corrected afterward.

---

## 3. Applied Practice Problems (Progressive Guidance Fading)

### Problem 1 (*Complete Walkthrough*): Single-Step BCE Gradient & Update
**Given:** Single training point $x = -2$, label $y = 1$, weight $w = 0$, bias $b = 0$, learning rate $\eta = 0.5$. Compute $z, \hat{p}, \frac{\partial J}{\partial w}, \frac{\partial J}{\partial b}$, and $(w_1, b_1)$.

> [!tip]- Solution
> 1. **Forward pass:** $z = 0(-2) + 0 = 0 \implies \hat{p} = \sigma(0) = 0.5$.
> 2. **Gradients ($m=1$):** $\frac{\partial J}{\partial w} = (0.5 - 1)(-2) = +1.0$; $\frac{\partial J}{\partial b} = 0.5 - 1 = -0.5$.
> 3. **Update ($\eta = 0.5$):** $w_1 = 0 - 0.5(1.0) = -0.50$; $b_1 = 0 - 0.5(-0.5) = +0.25$.
> 4. **Verify direction:** Updated logit $z_1 = (-0.50)(-2) + 0.25 = +1.25 > 0$, shifting $\hat{p}_1 > 0.5$ toward $y = 1$. **Final:** $\boxed{(w_1, b_1) = (-0.50,\; +0.25)}$.

### Problem 2 (*Partial Scaffolding*): Regularization Hyperparameter Equivalence ($m = 100$)
**Given:** Pipeline A minimizes $J_A(\mathbf{w}, b) = \frac{1}{100}\sum_{i=1}^{100} \ell(z_i, y_i) + \frac{0.02}{2}\|\mathbf{w}\|_2^2$ (unpenalized $b$). Derive the matching `scikit-learn 1.4.2` parameter `C` so `LogisticRegression(penalty="l2")` minimizes the identical objective surface.

> [!tip]- Solution
> Multiply $J_A$ by $m = 100$ to match summed cross-entropy, divide by $m\lambda = 100 \times 0.02 = 2.0$, and match to $C\sum \ell_i + \frac{1}{2}\|\mathbf{w}\|_2^2$: $C = \frac{1}{m\lambda} = \frac{1}{2.0} = 0.50$. Using `1 / 0.02 = 50` would be $100\times$ too weak. **Final:** $\boxed{C = 0.50}$.

### Problem 3 (*Hinted Diagnosis*): Threshold Raising Causing a Precision Drop
**Given:** Fixed model probabilities $\hat{p} = [0.95, 0.85, 0.65, 0.55, 0.40, 0.20]$ and labels $y = [1, 0, 1, 1, 0, 0]$. Compute `(Precision, Recall)` at $\tau = 0.50$ and $\tau = 0.70$, and explain why precision drops.

> [!tip]- Solution
> - **At $\tau = 0.50$:** Positives predicted for $\{0.95(1), 0.85(0), 0.65(1), 0.55(1)\} \implies \text{TP}=3, \text{FP}=1, \text{FN}=0$. **Precision = $\boxed{75.0\%}$**, **Recall = $\boxed{100.0\%}$**.
> - **At $\tau = 0.70$:** Positives predicted for $\{0.95(1), 0.85(0)\} \implies \text{TP}=1, \text{FP}=1, \text{FN}=2$. **Precision = $\boxed{50.0\%}$**, **Recall = $\boxed{33.3\%}$**.
> - **Why:** Raising $\tau$ pruned two borderline **true** positives ($0.65, 0.55$) while retaining a confident **false** positive ($0.85$), shrinking precision.

### Problem 4 (*Independent Transfer*): `0 * (-inf)` `NaN` vs. Subtraction Cancellation in `bce_from_logits`
**Given:** At $z = 50, y = 1$ in `float64`: (a) explain the exact IEEE failure in `-(y * np.log(p) + (1 - y) * np.log(1 - p))` when `p = sigmoid(50)` rounds to `1.0`, (b) explain why `np.logaddexp(0.0, z) - y * z` still suffers precision loss here, and (c) write the cancellation-free expression for $y \in \{0, 1\}$.

> [!tip]- Solution
> - **(a) `0.0 * (-inf) = NaN`:** At $z = 50$, $e^{-50} \approx 1.93 \times 10^{-22} < 2.22 \times 10^{-16}$, so `p` rounds to exact `1.0`. Next, `(1 - y)` equals `0.0` while `np.log(1 - 1.0) = np.log(0.0) = -inf`; evaluating `0.0 * (-inf)` yields IEEE `NaN` (multiplying zero by the `-inf` returned from `log(0)`—not a benign `0.0`).
> - **(b) Subtraction cancellation:** `np.logaddexp(0.0, 50.0) - 50.0` adds `1.93e-22` to `50.0`, losing the small fractional term during `float64` rounding so subtraction returns `0.0`.
> - **(c) Signed-logit form:** `np.logaddexp(0.0, (1.0 - 2.0 * y) * z)` evaluates `np.logaddexp(0.0, -50.0) ≈ 1.93e-22` directly with zero cancellation.
