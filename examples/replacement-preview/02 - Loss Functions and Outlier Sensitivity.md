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

# Loss Functions and Outlier Sensitivity

How should a model measure mistake size when predicting continuous numbers? If we treat a tiny error and a corrupted extreme outlier identically, noisy points can pull the entire regression line away from typical observations.

Think of a loss function as a penalty meter for each residual $r = y - \hat{y}$: squaring small mistakes stabilizes optimization near zero error, while switching to linear tails beyond a threshold prevents outliers from dominating the fit. Unlike physical measurements, empirical loss measures average error purely on the observed sample $\mathcal{D}$.

Approximate the unknown population expected risk R(h) by averaging pointwise errors across the n observed training examples.

$$
R_{\text{emp}}(h) = \frac{1}{n} \sum_{i=1}^{n} L\big(y^{(i)}, h(\mathbf{x}^{(i)})\big)
$$

> [!example]- Understand this formula step by step
> **What question does it answer?**
> Approximate the unknown population expected risk R(h) by averaging pointwise errors across the n observed training examples.
>
> **How to read it aloud:** Empirical risk of hypothesis h equals one over n times the sum from i equals 1 to n of pointwise loss L between true target y^(i) and predicted h(x^(i)).
>
> | Symbol | Name / Meaning | Type | Shape / Units | Role |
> |---|---|---|---|---|
> | $R_{\text{emp}}(h)$ | average training error of model h | scalar | 1x1 | average training error of model h |
> | $n$ | number of training examples | scalar | 1x1 | number of training examples |
> | $i$ | training example index running 1..n | index | 1x1 | training example index running 1..n |
> | $L(\cdot,\cdot)$ | non-negative pointwise error penalty | function | scalar output | non-negative pointwise error penalty |
>
> **Expanded elementary form:** $\frac{1}{3}\big[L(y^{(1)}, h(\mathbf{x}^{(1)})) + L(y^{(2)}, h(\mathbf{x}^{(2)})) + L(y^{(3)}, h(\mathbf{x}^{(3)}))\big]$
>
> **Step-by-step operations:**
> 1. Evaluate pointwise error L on every sample i from 1 to n.
> 2. Sum all n errors and divide by n so loss stays invariant to sample count n.
>
> **Worked numerical example:**
> - **Declared inputs:** `l1 = 1.0`, `l2 = 4.0`, `l3 = 1.0`, `n = 3.0`
> - **sum_losses:** `l1 + l2 + l3` = `6.0` — total sample loss across 3 points
> - **mean_loss:** `tot / n` = `2.0` — divide by n = 3
> - **Interpretation:** Average training penalty is 2.0 error units per example.
> - **Sanity check:** All losses >= 0 implies R_emp >= 0; low training risk does not guarantee low unseen test risk if overfitting.
>
> **Common misunderstandings to avoid:**
> - Equating low R_emp on training data with low expected population risk R(h) ignores overfitting.


Before inspecting the piecewise equations, see visually how each loss grows as prediction residual error moves away from zero.

![[assets/scriptorium/supervised-learning-preview/comparison-of-loss-functions-8e57447d079c.png|560]]

*Figure: Comparison curves of squared error, Huber, Log-Cosh, and absolute error losses as residual magnitude grows.*

*Source: [original publication](https://commons.wikimedia.org/wiki/File:Comparison_of_loss_functions.png); rights: CC BY-SA 4.0*

*Figure: Comparison curves of squared error, Huber, Log-Cosh, and absolute error losses as residual magnitude grows..*

**How to read this figure:**
- *Where to begin:* Start at error = 0 in the center where every curve hits zero, then follow the horizontal tails outward.
- MSE rises steeply as a parabola, amplifying large outlier residuals quadratically.
- MAE and Huber flatten into constant-slope straight lines in the outer tails, bounding outlier influence.

The numerical comparison at r = 3 versus r = 20 directly below confirms this exact curve separation.

Combine smooth quadratic behavior near zero error with outlier-resistant linear tails beyond cutoff delta.

$$
L_\delta(r) = \begin{cases} \frac{1}{2} r^2 & \text{if } |r| \le \delta \\ \delta \left(|r| - \frac{1}{2}\delta\right) & \text{if } |r| > \delta \end{cases}
$$

> [!example]- Understand this formula step by step
> **What question does it answer?**
> Combine smooth quadratic behavior near zero error with outlier-resistant linear tails beyond cutoff delta.
>
> **How to read it aloud:** Huber loss L_delta of residual r equals half r squared when absolute r is at most delta, otherwise delta times (absolute r minus half delta).
>
> | Symbol | Name / Meaning | Type | Shape / Units | Role |
> |---|---|---|---|---|
> | $r$ | prediction residual y - y_hat | scalar | 1x1 | prediction residual y - y_hat |
> | $\delta$ | positive threshold separating quadratic center from linear tails | parameter | 1x1 | positive threshold separating quadratic center from linear tails |
> | $L_delta$ | piecewise Huber penalty | scalar | 1x1 | piecewise Huber penalty |
>
> **Step-by-step operations:**
> 1. Compare |r| against threshold delta (e.g. delta = 1).
> 2. Use smooth 0.5 * r^2 for small residuals so gradients vanish smoothly at zero; switch to linear delta * (|r| - 0.5 * delta) in large-error tails so outliers cannot create giant gradients.
>
> **Worked numerical example:**
> - **Declared inputs:** `r_small = 3.0`, `r_outlier = 20.0`, `delta = 1.0`
> - **huber_r3:** `delta * (r_small - 0.5 * delta)` = `2.5` — for |r|=3 > 1, Huber=2.5 vs MSE r^2=9.0
> - **huber_r20:** `delta * (r_outlier - 0.5 * delta)` = `19.5` — for outlier |r|=20 > 1, Huber=19.5 vs MSE r^2=400.0
> - **Interpretation:** When residual jumps from 3 to 20, squared loss explodes 44.4x (9 -> 400), while Huber grows linearly (2.5 -> 19.5).
> - **Sanity check:** At exact boundary |r| = delta = 1, both branches match: 0.5*(1)^2 = 0.5 and 1*(1 - 0.5) = 0.5.
>
> **Assumptions & conditions:** Threshold delta > 0 must reflect normal target scale.
>
> **Common misunderstandings to avoid:**
> - Thinking Huber is non-differentiable at |r| = delta; both values and first derivatives match continuously at the boundary.


### Worked Numerical Comparison: Outlier Pull on MSE vs. Huber

Suppose we fix Huber threshold $\delta = 1.0$ and test two predictions:
1. Given residual $r = 3.0$: MSE computes $3^2 = 9.0$, while Huber uses its linear branch $1.0(3.0 - 0.5) = 2.5$.
2. Given extreme outlier $r = 20.0$: MSE jumps to $20^2 = 400.0$ ($44.4\times$), while Huber yields $1.0(20.0 - 0.5) = 19.5$.
3. Sanity check: both branches agree cleanly at $|r| = \delta = 1$ ($0.5$), and never confuse training fit ($R_{\text{emp}}$) with generalization ($R$).

### Why Causal Difference Drives Choice Before Tables

Because squared error multiplies residual slopes linearly ($\frac{d}{dr}(\frac{1}{2}r^2) = r$), an outlier with $r=20$ pulls parameters $6.7\times$ harder than $r=3$, and inflates squared penalty $44.4\times$ ($9 \to 400$). Huber loss caps the tail derivative at $\pm\delta = \pm 1$, keeping penalty growth linear ($2.5 \to 19.5$).

| Residual $r$ | MSE ($r^2$) | MAE ($|r|$) | Huber ($\delta = 1$) | Outlier Pull |
|---|---|---|---|---|
| $3.0$ | $9.0$ | $3.0$ | $2.5$ | Mild baseline |
| $20.0$ | $400.0$ ($44.4\times$) | $20.0$ ($6.7\times$) | $19.5$ | Huber resists explosion |

- **Use MSE when:** residuals have symmetric light tails and outliers are genuine high-cost events.
- **Avoid MSE when:** noisy sensors or label corruption inject heavy outliers; choose Huber or MAE instead.

## Check Your Understanding

**Question:** For residual $r = 20$ with $\delta = 1$, verify step-by-step why Huber returns $19.5$ rather than $200$.

> [!hint]- Show hint
> Check which branch of the piecewise definition applies when $|r| > \delta$.

> [!answer]- Show detailed answer
> Since $|20| > 1$, the linear tail branch applies: $\delta(|r| - 0.5\delta) = 1.0 \times (20.0 - 0.5) = 19.5$. Because growth is linear rather than quadratic, extreme points lose disproportionate pull.

Next, examine how binary probability classification transforms linear scores smoothly in [[03 - Logistic Regression Chain-Rule Derivation]].
