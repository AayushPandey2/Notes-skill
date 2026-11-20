---
id: gd.ch5
aliases:
- Curvature and Failure Analysis
topic: Gradient Descent
tags:
- type/full-notes
nexttopics: []
---
# Curvature and Failure Analysis

## Curvature and Failure Analysis

The scalar model suggests why one fixed step can perform poorly in several
dimensions. Consider f(x)=x^T H x/2 with a real symmetric positive definite matrix
H. The gradient is Hx. Symmetry permits an orthonormal eigenbasis: H=Q Lambda Q^T.
Writing z=Q^T x transforms the update into

$$
z_{k+1}=(I-\alpha\Lambda)z_k,\qquad
z_{k+1,i}=(1-\alpha\lambda_i)z_{k,i}.
$$

Each eigen-direction behaves like our scalar problem with curvature lambda_i.
All initial states converge when every multiplier has magnitude below one.
Because the eigenvalues are positive, their intersection is
0<alpha<2/lambda_max. The largest curvature constrains stability; the smallest
curvature can still leave a multiplier close to one, causing slow progress.
This explains a long narrow quadratic valley without relying on a metaphor alone.

For eigenvalues 1 and 100, alpha=0.01 gives multipliers 0.99 and 0. The high-curvature
coordinate disappears in one ideal update while the low-curvature coordinate
shrinks by only one percent each step. Raising alpha to 0.03 makes the second
multiplier -2 and destabilizes that coordinate. A larger step is not a universal
remedy for slow convergence.

The spectral contraction factor is the largest absolute multiplier. Minimizing it
over positive fixed steps balances the two extreme eigenvalues:
1-alpha lambda_min=-(1-alpha lambda_max). Solving gives
alpha=2/(lambda_min+lambda_max), with factor
(lambda_max-lambda_min)/(lambda_max+lambda_min). This statement assumes a fixed
positive definite quadratic and exact arithmetic. It is not a recommendation for
choosing an unknown neural network's learning rate.

| Symptom | Latent property under the stated model | Candidate cause | Diagnostic measurement | Evidence status | Possible response |
|---|---|---|---|---|---|
| Growing alternating states | Noncontracting eigen-direction | Step exceeds the quadratic stability range | Compare alpha with 2/lambda_max | Derived for the stated quadratic; not inferred from arbitrary logs | Reduce step or estimate curvature |
| Very slow stable progress | Weak contraction | A multiplier is close to 1 | Inspect scale and spectral spread | Conditional analytical explanation | Rescale or precondition |
| Flat gradient away from desired solution | Stationarity may be uninformative | Quadratic assumptions may not apply | Inspect objective and stationary point | Candidate diagnosis, not established cause | Reassess model and stopping test |

The table is a diagnostic aid, not a proof of the cause for arbitrary training
logs. Preconditioning changes the geometry so that a descent step can account
for differing scales, but its stability must be analyzed for the transformed
system. Stochastic gradients introduce noise; nonconvex objectives introduce
stationary points beyond minima; adaptive methods introduce extra state. Each
requires additional assumptions and analysis. Reconstruct the argument by asking
what the update multiplier is, which assumptions justify it, and whether its
magnitude contracts every relevant direction.

## Check your understanding

**Question (gd.q5.1):** Why does lambda_max limit the SPD quadratic step?

> [!hint]- Show hint
> Require every eigen-direction multiplier to contract.

> [!answer]- Show detailed answer
> Each positive eigenvalue requires 0<alpha<2/lambda_i. Intersecting these intervals yields 0<alpha<2/lambda_max; the eigenbasis reduction assumes a real symmetric positive definite Hessian.

**Question (gd.q5.2):** For eigenvalues 1 and 100 and alpha=0.01, find both multipliers.

> [!hint]- Show hint
> Evaluate 1-alpha lambda_i.

> [!answer]- Show detailed answer
> They are 0.99 and 0. The stiff coordinate disappears in one ideal update, while the first contracts by only one percent per step.

**Question (gd.q5.3):** Do oscillating training logs prove an excessively large fixed step?

> [!hint]- Show hint
> The table analyzed an explicitly stated quadratic.

> [!answer]- Show detailed answer
> No. That is one candidate cause under the quadratic model. Other objectives, stochastic noise and extra optimizer state require their own diagnostics and controlled evidence.

**Question (gd.q5.4):** Does the balanced quadratic step prescribe a neural network learning rate?

> [!hint]- Show hint
> Check whether its Hessian is fixed, known and SPD.

> [!answer]- Show detailed answer
> No. The derived 2/(lambda_min+lambda_max) result assumes a fixed positive definite quadratic and exact arithmetic. Those assumptions do not generally describe neural network training.
