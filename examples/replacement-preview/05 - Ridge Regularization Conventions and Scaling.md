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

# Ridge Regularization Conventions and Scaling

Adding an $L_2$ penalty prevents collinear weights from exploding, but two subtle notation switches often confuse readers: intercept absorption and loss normalization. Making both conventions explicit prevents factor-of-$n$ mismatches and accidental bias shrinkage.

Think of tightening a leash on slope weights $\mathbf{w}$ while leaving the starting height anchor $b$ completely free. If you penalized intercept $b$, merely changing units from Celsius to Kelvin would alter predictions arbitrarily. This distinction applies whenever feature shifts or uncentered targets matter.

### Explicit Penalty Matrix Mask & Loss Scaling Convention

When absorbing bias $b$ into parameter vector $\tilde{\mathbf{w}} = [b, w_1, \dots, w_d]^\top$, use the diagonal mask $I_0 = \operatorname{diag}(0, 1, \dots, 1)$ so bias index $0$ receives zero penalty. Notice also how averaged loss relates to unnormalized sum loss:

Regularize feature slopes fairly even when the bias column is absorbed inside X_tilde by masking index 0 (intercept b) out of the L2 penalty.

$$
J_{\text{Ridge}}(\tilde{\mathbf{w}}) = \frac{1}{n} \|\tilde{X}\tilde{\mathbf{w}} - \mathbf{y}\|_2^2 + \lambda_{\text{avg}} \|I_0 \tilde{\mathbf{w}}\|_2^2, \qquad I_0 = \operatorname{diag}(0, 1, \dots, 1)
$$

> [!example]- Understand this formula step by step
> **What question does it answer?**
> Regularize feature slopes fairly even when the bias column is absorbed inside X_tilde by masking index 0 (intercept b) out of the L2 penalty.
>
> **How to read it aloud:** Averaged Ridge objective equals one over n times residual norm squared plus lambda_avg times squared L2 norm of I_0 times w_tilde, where I_0 zeroes the intercept index.
>
> | Symbol | Name / Meaning | Type | Shape / Units | Role |
> |---|---|---|---|---|
> | $\tilde{X}$ | design matrix with leading all-ones column for intercept b | matrix | n x (d+1) | design matrix with leading all-ones column for intercept b |
> | $\tilde{\mathbf{w}}$ | stacked parameter vector [b, w_1, ..., w_d]^T | vector | (d+1) x 1 | stacked parameter vector [b, w_1, ..., w_d]^T |
> | $I_0$ | diagonal mask with 0 at intercept entry and 1s on feature weights | matrix | (d+1) x (d+1) | diagonal mask with 0 at intercept entry and 1s on feature weights |
> | $\lambda_{\text{avg}}$ | regularization strength on averaged loss (rescaling rule: lambda_sum = n * lambda_avg) | parameter | 1x1 | regularization strength on averaged loss (rescaling rule: lambda_sum = n * lambda_avg) |
>
> **Derivation reasoning:** When switching from averaged empirical risk (with 1/n) to unnormalized least-squares sum ||Xw - y||_2^2 + lambda_sum ||w||_2^2, multiplying the entire objective by n yields the exact same minimizer iff lambda_sum = n * lambda_avg.
>
> **Worked numerical example:**
> - **Declared inputs:** `xtx = 2.0`, `xty = 6.0`, `lam_sum = 1.0`, `n = 2.0`
> - **ols_no_intercept:** `xty / xtx` = `3.0` — explicitly intercept-free uncentered setup X=[1,1], y=[2,4] -> mean 3.0
> - **ridge_no_intercept:** `xty / (xtx + lam_sum)` = `2.0` — unnormalized sum lambda_sum=1 corresponds to averaged lambda_avg = 1/2 = 0.5
> - **Interpretation:** With unnormalized sum penalty lambda_sum = 1 on n = 2 observations, Ridge shrinks w from 3.0 to 2.0 (equivalent to averaged loss penalty lambda_avg = 0.5).
> - **Sanity check:** Notice X=[1,1]^T here is explicitly uncentered intercept-free (mean != 0) to isolate slope shrinkage cleanly, distinct from centered-data derivations where b=0 after subtracting sample means.
>
> **Common misunderstandings to avoid:**
> - Mixing averaged loss 1/n and unaveraged sum ||Xw - y||^2 without scaling lambda by n, or forgetting that intercept absorption requires mask I_0.


### Causal Choice: Ridge vs. Lasso & Uncentered Trace Distinction

Here a **subgradient** (a set-valued slope extension used where a function has a sharp kink, such as $|w|$ at $0$) takes the place of an ordinary smooth derivative in Lasso coordinate descent. Suppose an uncentered 1D intercept-free setup has $X=[1,1]^\top$ and $\mathbf{y}=[2,4]^\top$ ($n=2$):
1. Computing Gram sum gives $X^\top X = 2$ and alignment $X^\top \mathbf{y} = 6$, so unregularized OLS yields $w^* = 6/2 = 3.0$.
2. Under unnormalized Ridge sum penalty $\lambda_{\text{sum}} = 1$, $w^*_{\text{Ridge}} = 6/(2+1) = 2.0$ (equivalent to averaged-loss $\lambda_{\text{avg}} = 1/2 = 0.5$).
3. Sanity check: verify $n\lambda_{\text{avg}} = \lambda_{\text{sum}}$ cleanly and distinguish intercept-free runs from centered-data derivations to avoid bias shrinkage errors.

| Criterion | Ridge ($L_2$) | Lasso ($L_1$) |
|---|---|---|
| Penalty Masking | $I_0 \tilde{\mathbf{w}}$ never shrinks intercept $b$ | $I_0 \tilde{\mathbf{w}}$ never shrinks intercept $b$ |
| Collinear Features | Shares shrinkage smoothly across correlated slopes | Picks one correlated feature and zeroes peers |
| Closed Form | Yes: $(\tilde{X}^\top \tilde{X} + n \lambda_{\text{avg}} I_0)^{-1} \tilde{X}^\top \mathbf{y}$ | No (coordinate descent / subgradient) |

## Check Your Understanding

**Question:** If an optimizer drops $1/n$ and minimizes $\|X\mathbf{w}-\mathbf{y}\|_2^2 + \lambda_{\text{sum}}\|\mathbf{w}\|_2^2$ on $n=100$ samples, what $\lambda_{\text{sum}}$ matches averaged-loss penalty $\lambda_{\text{avg}} = 0.05$?

> [!hint]- Show hint
> Multiply the entire averaged objective by sample count $n$.

> [!answer]- Show detailed answer
> Multiplying $\frac{1}{n}\|X\mathbf{w}-\mathbf{y}\|_2^2 + \lambda_{\text{avg}}\|\mathbf{w}\|_2^2$ by $n = 100$ leaves minimizer $\mathbf{w}^*$ unchanged when $\lambda_{\text{sum}} = n \lambda_{\text{avg}} = 100 \times 0.05 = 5.0$.

This completes the five supervised learning replacement previews cleanly without altering the protected original vault.
