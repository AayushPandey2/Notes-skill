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

# Bias-Variance Decomposition and Randomness

Why does a very simple straight line miss curved signals while a high-degree polynomial swings wildly across training subsets? To diagnose underfitting versus overfitting precisely, we need to measure error across repeated random samples rather than one lucky split.

Think of throwing darts at a bullseye: bias measures whether your average aim sits off-center, variance measures how widely your throws scatter from sample to sample, and noise is wind shaking the board. This decomposition applies cleanly under squared loss with zero-mean additive noise.

### Identifying the Exact Sources of Randomness

Notice first what is random inside the expectation operator $\mathbb{E}_{\mathcal{D}, \varepsilon}[\cdot]$: **$\mathcal{D}$** is a random training set draw (causing the learned hypothesis $\hat{f}_{\mathcal{D}}(\mathbf{x})$ to fluctuate), and **$\varepsilon$** is unseen target noise at test input $\mathbf{x}$ (independent of $\mathcal{D}$, with $\mathbb{E}[\varepsilon] = 0$ and $\operatorname{Var}(\varepsilon) = \sigma^2$).

Before expanding expectations over training datasets D and noise epsilon, see how total error combines falling bias and rising variance.

![[assets/scriptorium/supervised-learning-preview/bias-variance-decomposition-78e1dbbf12de.png|540]]

*Figure: Plot of descending squared bias, rising variance, and U-shaped total expected error across complexity.*

*Source: [original publication](https://commons.wikimedia.org/wiki/File:Bias-variance_decomposition.png); rights: CC BY-SA 4.0*

*Figure: Plot of descending squared bias, rising variance, and U-shaped total expected error across complexity..*

**How to read this figure:**
- *Where to begin:* Read from left (simple underfit models with high bias) rightward across the U-curve trough toward complex high-variance models.
- Bias^2 falls as hypothesis flexibility captures systematic curvature.
- Variance rises as models track sample noise across different training draws D.

The decomposition next proves algebraically why total expected error never drops below noise variance sigma^2.

Decompose expected squared prediction error at test input x across random training draws D and irreducible target noise epsilon.

$$
\mathbb{E}_{\mathcal{D}, \varepsilon}\big[(y - \hat{f}_{\mathcal{D}}(\mathbf{x}))^2\big] = \big(f(\mathbf{x}) - \mathbb{E}_{\mathcal{D}}[\hat{f}_{\mathcal{D}}(\mathbf{x})]\big)^2 + \mathbb{E}_{\mathcal{D}}\big[\big(\hat{f}_{\mathcal{D}}(\mathbf{x}) - \mathbb{E}_{\mathcal{D}}[\hat{f}_{\mathcal{D}}(\mathbf{x})]\big)^2\big] + \sigma^2
$$

> [!example]- Understand this formula step by step
> **What question does it answer?**
> Decompose expected squared prediction error at test input x across random training draws D and irreducible target noise epsilon.
>
> **How to read it aloud:** Expectation over training sets D and test noise epsilon of squared error equals Squared Bias across D, plus Variance across D, plus irreducible noise variance sigma squared.
>
> | Symbol | Name / Meaning | Type | Shape / Units | Role |
> |---|---|---|---|---|
> | $\mathcal{D}$ | random training dataset sampled i.i.d. of size n | random_variable | dataset | random training dataset sampled i.i.d. of size n |
> | $\varepsilon$ | zero-mean irreducible target observation noise at test input x (Var = sigma^2, independent of D) | random_variable | scalar | zero-mean irreducible target observation noise at test input x (Var = sigma^2, independent of D) |
> | $f(\mathbf{x})$ | deterministic true conditional mean E[Y | X=x] | scalar | 1x1 | deterministic true conditional mean E[Y | X=x] |
> | $\hat{f}_{\mathcal{D}}(\mathbf{x})$ | model prediction fitted specifically on random training draw D | random_variable | scalar | model prediction fitted specifically on random training draw D |
> | $\sigma^2$ | irreducible observation noise variance E[epsilon^2] | parameter | 1x1 | irreducible observation noise variance E[epsilon^2] |
>
> **Derivation reasoning:** First identify the two independent sources of randomness in E_{D, epsilon}[.]: dataset draw D governs the trained hypothesis f_hat_D, whereas test noise epsilon perturbs y = f(x) + epsilon independently of D. Independence splits E[(f - f_hat) * epsilon] = E[f - f_hat] * E[epsilon] = 0; then adding/subtracting mean model f_bar = E_D[f_hat_D] makes the second cross-term vanish because E_D[f_bar - f_hat_D] = f_bar - f_bar = 0.
>
> **Worked numerical example:**
> - **Declared inputs:** `f_true = 5.0`, `f_bar = 4.2`, `var_model = 0.36`, `noise_var = 0.25`
> - **bias_sq:** `(f_bar - f_true) ** 2` = `0.64` — systematic error (4.2 - 5.0)^2 = 0.64
> - **total_err:** `b2 + var_model + noise_var` = `1.25` — 0.64 + 0.36 + 0.25 = 1.25
> - **Interpretation:** Out of 1.25 total expected error, 0.64 comes from systematic underfitting bias, 0.36 from sample variance across training draws, and 0.25 from unavoidable target noise.
> - **Sanity check:** All three variance/squared components are non-negative, bounding total error >= sigma^2.
>
> **Common misunderstandings to avoid:**
> - Treating E[.] as an average over test inputs x rather than expectation over repeated random training sets D and noise epsilon at fixed x.


### Worked Numerical Expected Error Breakdown

Suppose true target expectation $f(\mathbf{x}) = 5.0$, average fitted predictor across training draws is $\bar{f}(\mathbf{x}) = 4.2$ with variance $0.36$, and irreducible noise variance is $\sigma^2 = 0.25$:
1. Bias equals $4.2 - 5.0 = -0.8$, so squared bias gives $(-0.8)^2 = 0.64$.
2. Adding sample variance ($0.36$) and irreducible noise ($0.25$) yields $0.64 + 0.36 + 0.25 = 1.25$.
3. Sanity verification: every additive term is non-negative, avoiding the misconception that larger training samples reduce $\sigma^2$.

### Interpreting the Three Additive Terms

Because noise $\varepsilon$ is independent of the training sample $\mathcal{D}$, the cross-term involving $\varepsilon$ factors and vanishes since $\mathbb{E}[\varepsilon] = 0$. Similarly, inserting and subtracting the average trained predictor $\bar{f}(\mathbf{x}) = \mathbb{E}_{\mathcal{D}}[\hat{f}_{\mathcal{D}}(\mathbf{x})]$ zeroes the second cross-term cleanly, proving why irreducible noise $\sigma^2$ acts as an unbreakable lower bound.

- **Use higher capacity when:** validation error stays high on both train and test due to systematic underfitting bias.
- **Avoid unchecked complexity when:** small dataset perturbations cause unstable variance swings.

## Check Your Understanding

**Question:** If average prediction at $\mathbf{x}$ is $4.2$ when true $f(\mathbf{x}) = 5.0$, with $\operatorname{Var}(\hat{f}_{\mathcal{D}}) = 0.36$ and $\sigma^2 = 0.25$, explain which quantities random expectation $\mathbb{E}$ averages over.

> [!hint]- Show hint
> Separate randomness over training set draws $\mathcal{D}$ from unseen test target noise $\varepsilon$.

> [!answer]- Show detailed answer
> $\mathbb{E}_{\mathcal{D}, \varepsilon}$ averages over independent draws of the training set $\mathcal{D}$ (which determines $\text{Bias}^2 = (-0.8)^2 = 0.64$ and $\text{Variance} = 0.36$) and test noise $\varepsilon$ ($\sigma^2 = 0.25$), summing to total error $1.25$.

Next, see how Ridge regularization controls variance cleanly while avoiding intercept/scaling bugs in [[05 - Ridge Regularization Conventions and Scaling]].
