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

# Logistic Regression Chain-Rule Derivation

Predicting a probability between $0$ and $1$ creates a roadblock for raw linear regression: lines shoot off toward $\pm\infty$. We need a smooth function compressing real logits $z$ into $(0, 1)$ while still keeping gradient updates clean and stable.

Think of a dimmer curve that responds gently near $0\%$ and $100\%$ while sliding smoothly across the middle $50\%$ threshold. This analogy holds for monotonic probability calibration, though sigmoid outputs are probabilities under the log-odds assumption rather than calibrated uncertainty intervals everywhere.

Before writing the log-likelihood gradient, notice how the S-curve maps unbounded logits smoothly between horizontal asymptotes.

![[assets/scriptorium/supervised-learning-preview/sigmoidal-curves-2ad05db99108.jpg|520]]

*Figure: Smooth S-shaped sigmoidal curves saturating asymptotically without reaching endpoints at finite inputs.*

*Source: [original publication](https://commons.wikimedia.org/wiki/File:Quatre_fonctions_sigmo%C3%AFdes_%E2%80%94_four_sigmoidal_functions.jpg); rights: CC BY 4.0*

*Figure: Smooth S-shaped sigmoidal curves saturating asymptotically without reaching endpoints at finite inputs..*

**How to read this figure:**
- *Where to begin:* Start at x = 0 where the slope is steepest, then trace both tails asymptotically toward the upper and lower limits.
- Around zero, changing logits moves predicted probabilities cleanly.
- Far in the tails, outputs approach asymptotes without attaining exact endpoints for finite logits, forcing weight norms ||w|| to grow when data is linearly separable.

That exact derivative property sigma'(z) = sigma(z)(1 - sigma(z)) simplifies the chain rule cleanly next.

Map any unbounded real linear score (logit z) cleanly into a probability between 0 and 1.

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

> [!example]- Understand this formula step by step
> **What question does it answer?**
> Map any unbounded real linear score (logit z) cleanly into a probability between 0 and 1.
>
> **How to read it aloud:** sigma of z equals one divided by one plus e to the negative z.
>
> | Symbol | Name / Meaning | Type | Shape / Units | Role |
> |---|---|---|---|---|
> | $\sigma(z)$ | predicted positive-class probability in (0, 1) | scalar | 1x1 | predicted positive-class probability in (0, 1) |
> | $z$ | unbounded linear logit w^T x + b | scalar | 1x1 | unbounded linear logit w^T x + b |
> | $e$ | Euler base approx 2.71828 | scalar | 1x1 | Euler base approx 2.71828 |
>
> **Step-by-step operations:**
> 1. Negate logit z and exponentiate e^(-z) (strictly positive).
> 2. Add 1 so denominator exceeds 1, guaranteeing quotient lies strictly in (0, 1).
>
> **Worked numerical example:**
> - **Declared inputs:** `z = 2.0`, `e_val = 2.71828`
> - **exp_pos_z:** `e_val ** 2` = `7.389046` — for z = 2, e^2 approx 7.389
> - **exp_neg_z:** `1 / ez_pos` = `0.135335` — reciprocal e^(-2) = 0.1353
> - **probability:** `1 / (1 + ez)` = `0.880797` — logit 2.0 maps to 88.1% probability
> - **Interpretation:** Logit z = 2 produces probability 88.1%, while z = 0 gives exact decision boundary 0.5.
> - **Sanity check:** Strictly bounded in (0, 1) for finite z, never attaining exact 0 or 1.
>
> **Common misunderstandings to avoid:**
> - Thinking probability equals 0 or 1 at finite logits—exact 0/1 is only an asymptotic limit as |z| -> infinity.


### Splitting the Cross-Entropy Chain Rule Into Manageable Steps

Rather than cramming logs, fractions, and sigmoid derivatives into one long line, let us define what **asymptote / asymptotic** means first (a horizontal boundary line that a curve approaches infinitely closely without ever touching at finite inputs), and then write the **intermediate substitution** $u = 1 - \hat{p}^{(i)}$ separating the **outer derivative** ($-1/u$) and **inner derivative** ($du/d\hat{p}^{(i)} = -1$) before combining via the chain rule:

Step 1 of the chain rule: compute how sensitive binary cross-entropy loss is to small changes in predicted probability p_hat^(i).

$$
\frac{\partial L^{(i)}}{\partial \hat{p}^{(i)}} = -\left(\frac{y^{(i)}}{\hat{p}^{(i)}} - \frac{1 - y^{(i)}}{1 - \hat{p}^{(i)}}\right) = \frac{\hat{p}^{(i)} - y^{(i)}}{\hat{p}^{(i)}(1 - \hat{p}^{(i)})}
$$

> [!example]- Understand this formula step by step
> **What question does it answer?**
> Step 1 of the chain rule: compute how sensitive binary cross-entropy loss is to small changes in predicted probability p_hat^(i).
>
> **How to read it aloud:** Partial derivative of loss L^(i) with respect to probability p-hat^(i) equals p-hat^(i) minus y^(i) divided by p-hat^(i) times one minus p-hat^(i).
>
> | Symbol | Name / Meaning | Type | Shape / Units | Role |
> |---|---|---|---|---|
> | $L^{(i)}$ | single-example binary cross-entropy loss | scalar | 1x1 | single-example binary cross-entropy loss |
> | $\hat{p}^{(i)}$ | predicted positive probability in (0, 1) | scalar | 1x1 | predicted positive probability in (0, 1) |
> | $y^{(i)}$ | binary ground-truth label in {0, 1} | scalar | 1x1 | binary ground-truth label in {0, 1} |
>
> **Derivation reasoning:** Differentiating -y log(p_hat) gives -y / p_hat, and differentiating -(1-y) log(1-p_hat) inserts a negative sign from (1-p_hat)' = -1, leaving + (1-y)/(1-p_hat). Putting over the common denominator p_hat(1-p_hat) simplifies the numerator directly to p_hat - y.
>
> **Worked numerical example:**
> - **Declared inputs:** `y = 1.0`, `p_hat = 0.8`
> - **numerator:** `p_hat - y` = `-0.2` — error p_hat - y
> - **denom:** `p_hat * (1 - p_hat)` = `0.16` — sigmoid variance denominator
> - **dL_dp:** `num / den` = `-1.25` — increasing p_hat lowers loss when y=1
> - **Interpretation:** When label y = 1 and prediction p_hat = 0.8, slope is -1.25 (increasing p_hat reduces loss).
> - **Sanity check:** Denominator p_hat(1-p_hat) > 0 since p_hat is strictly inside (0, 1).
>
> **Common misunderstandings to avoid:**
> - Dropping the minus sign from the derivative of log(1 - p_hat) causes cancellation to fail.


Next, multiplying by the inner sigmoid derivative $rac{d\hat{p}^{(i)}}{dz^{(i)}} = \hat{p}^{(i)}(1 - \hat{p}^{(i)})$ in the chain rule cancels the matching denominators cleanly:

Step 2 of the chain rule: combine log-loss sensitivity with sigmoid derivative sigma'(z) = p_hat(1 - p_hat) so denominators cancel completely.

$$
\frac{\partial L^{(i)}}{\partial z^{(i)}} = \frac{\partial L^{(i)}}{\partial \hat{p}^{(i)}} \cdot \frac{d\hat{p}^{(i)}}{dz^{(i)}} = \hat{p}^{(i)} - y^{(i)}
$$

> [!example]- Understand this formula step by step
> **What question does it answer?**
> Step 2 of the chain rule: combine log-loss sensitivity with sigmoid derivative sigma'(z) = p_hat(1 - p_hat) so denominators cancel completely.
>
> **How to read it aloud:** Partial L^(i) over partial z^(i) equals partial L^(i) over partial p-hat^(i) times d p-hat^(i) over d z^(i), cancelling down to p-hat^(i) minus y^(i).
>
> | Symbol | Name / Meaning | Type | Shape / Units | Role |
> |---|---|---|---|---|
> | $z^{(i)}$ | pre-activation logit w^T x^(i) + b | scalar | 1x1 | pre-activation logit w^T x^(i) + b |
> | $\hat{p}^{(i)}$ | sigmoid(z^(i)) probability | scalar | 1x1 | sigmoid(z^(i)) probability |
> | $y^{(i)}$ | binary label {0, 1} | scalar | 1x1 | binary label {0, 1} |
>
> **Derivation reasoning:** Multiply (p_hat - y)/[p_hat(1-p_hat)] from Step 1 by sigma'(z) = p_hat(1-p_hat); the matching p_hat(1-p_hat) factors cancel identically, leaving simple signed residual error p_hat - y with no vanishing denominator.
>
> **Worked numerical example:**
> - **Declared inputs:** `y = 1.0`, `p_hat = 0.8`
> - **grad_p:** `(p_hat - y) / (p_hat * (1 - p_hat))` = `-1.25`
> - **sig_deriv:** `p_hat * (1 - p_hat)` = `0.16`
> - **cancelled:** `gp * dpdz` = `-0.2` — matches p_hat - y = 0.8 - 1.0 = -0.2
> - **Interpretation:** Gradient with respect to logit z is simply prediction minus truth (-0.2), identical in structure to linear regression error.
> - **Sanity check:** Exact cancellation eliminates saturation blowup in denominator.
>
> **Common misunderstandings to avoid:**
> - Confusing Cross-Entropy with Squared Error on sigmoid outputs; only Cross-Entropy cancels sigma'(z).


### Worked Gradient Evaluation Trace

Suppose true label $y = 1$ and linear score produces $\hat{p} = 0.8$ (under $z pprox 1.386$):
1. Step 1 log-loss slope gives $\frac{-0.2}{0.16} = -1.25$.
2. Step 2 sigmoid derivative $\sigma'(z) = 0.8(0.2) = 0.16$ cancels identically, yielding final logit gradient $\frac{\partial L}{\partial z} = 0.8 - 1 = -0.2$.
3. Sanity check: negative sign pulls logit $z$ upward to raise $\hat{p}$ toward $1.0$; common mistake to avoid is forgetting that sigmoid output never reaches exact $1.0$ at finite weights.

### Convergence vs. Parameter Divergence on Separable Data

When two classes can be separated perfectly without error, scaling weights $(c\mathbf{w}, cb)$ with $c > 1$ pushes positive logits toward $+\infty$ and negative logits toward $-\infty$. Notice the distinction carefully: the cross-entropy loss $J$ strictly approaches its **lower bound of zero**, while the unregularized weight norm $\|\mathbf{w}\|_2$ diverges without bound. Adding $L_2$ regularization anchors a finite optimum.

## Check Your Understanding

**Question:** On a linearly separable dataset, does unregularized cross-entropy loss $J$ diverge to $-\infty$, or why do weights grow toward infinity?

> Explain precisely why unregularized logistic regression parameters diverge on linearly separable data while loss remains bounded below by zero.
>
> $$
> J(c\mathbf{w}, cb) \xrightarrow{c \to \infty} 0 \quad \text{while } \|c\mathbf{w}\|_2 \to \infty
> $$
>
> > [!example]- Understand this formula step by step
> > **What question does it answer?**
> > Explain precisely why unregularized logistic regression parameters diverge on linearly separable data while loss remains bounded below by zero.
> >
> > **How to read it aloud:** Objective J evaluated at scaled parameters c w, c b approaches zero as c grows toward infinity, while parameter norm magnitude c w diverges to infinity.
> >
> > | Symbol | Name / Meaning | Type | Shape / Units | Role |
> > |---|---|---|---|---|
> > | $c$ | positive scaling multiplier c > 1 along separating direction | scalar | 1x1 | positive scaling multiplier c > 1 along separating direction |
> > | $J$ | non-negative binary cross-entropy loss (>= 0) | scalar | 1x1 | non-negative binary cross-entropy loss (>= 0) |
> > | $\|\mathbf{w}\|_2$ | Euclidean norm of weights | scalar | 1x1 | Euclidean norm of weights |
> >
> > **Worked numerical example:**
> > - **Declared inputs:** `c1 = 1.0`, `c2 = 5.0`, `margin_w_norm = 2.0`
> > - **norm_1:** `c1 * margin_w_norm` = `2.0`
> > - **norm_2:** `c2 * margin_w_norm` = `10.0` — weight norm scales linearly while loss shrinks toward lower bound 0
> > - **Interpretation:** Cross-entropy never falls below 0 (not 'without bound'); it decreases strictly toward its lower bound 0 while weights grow unboundedly.
> > - **Sanity check:** Because log(p_hat) <= 0, negative log-loss J is always >= 0.
> >
> > **Common misunderstandings to avoid:**
> > - Incorrectly writing that cross-entropy decreases 'without bound': loss is bounded below by 0, whereas weight magnitude ||w|| diverges without bound.


> [!hint]- Show hint
> Remember log-loss is always $\ge 0$ for $\hat{p} \in (0, 1)$, and check whether sigmoid reaches exact $0$ or $1$ for finite $z$.

> [!answer]- Show detailed answer
> Cross-entropy loss $J$ does **not** decrease without bound—it is bounded below by $0$. Because $\sigma(z)$ approaches $0$ and $1$ only asymptotically as $|z| \to \infty$, gradient descent keeps enlarging $\|\mathbf{w}\|_2$ indefinitely to push $J$ ever closer toward $0$.

Next, study why balancing simplicity and flexibility reduces expected error in [[04 - Bias-Variance Decomposition and Randomness]].
