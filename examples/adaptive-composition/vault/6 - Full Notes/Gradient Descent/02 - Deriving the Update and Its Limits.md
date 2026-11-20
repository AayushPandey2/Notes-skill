---
id: gd.ch2
aliases:
- Deriving the Update and Its Limits
topic: Gradient Descent
tags:
- type/full-notes
nexttopics:
- '[[03 - Tracing the Algorithm]]'
---
# Deriving the Update and Its Limits

## Deriving the Update and Its Limits

Let x_k denote the parameter after k completed updates; x_0 is the initialization.
Let alpha be a fixed positive real number. Differentiating the quadratic gives
f'(x)=x. Substituting it into the negative-gradient step yields

$$
x_{k+1}=x_k-\alpha f'(x_k)=x_k-\alpha x_k=(1-\alpha)x_k.
$$

The final equality is not an approximation for this objective. Applying the same
relation repeatedly gives x_1=(1-alpha)x_0, x_2=(1-alpha)²x_0, and, by induction,

$$
x_k=(1-\alpha)^k x_0.
$$

The induction starts at k=0. If the expression holds at k, multiplying by
(1-alpha) proves it at k+1. This closed form lets us prove convergence rather than
infer it from a finite plot. For any nonzero x_0, the iterates approach zero exactly
when |1-alpha|<1. Solving the double inequality gives -1<1-alpha<1; subtracting
one and reversing signs gives 0<alpha<2. At alpha=1, zero is reached in one update.
For 0<alpha<1, the sign stays fixed; for 1<alpha<2, signs alternate while magnitudes
shrink. The direction may cross the optimum without preventing convergence.

The objective sequence is f(x_k)=(1-alpha)^(2k)x_0²/2. Its multiplier is the
square of the state multiplier, so an oscillating state can still have a
monotonically decreasing cost. At alpha=2, the state alternates with constant
magnitude and the cost is constant. For alpha>2, magnitudes grow. At alpha=0 the
state does not move. If x_0=0, every step remains zero regardless of finite alpha;
that special initialization does not establish convergence from arbitrary points.

Now replace the objective by f(x)=lambda x²/2, where lambda is positive curvature.
Its derivative is lambda x and the multiplier becomes 1-alpha lambda. The same
argument gives 0<alpha<2/lambda. Units must be consistent: alpha lambda must be
dimensionless. Greater curvature therefore permits a smaller stable step.

For a general function with an L-Lipschitz gradient, the descent lemma supplies
an upper quadratic bound, not this exact recurrence. We must state that assumption
before using an analogous sufficient step condition. Quadratic equality cannot
be silently transferred to arbitrary objectives.

## Check your understanding

**Question (gd.q2.1):** Derive the scalar contraction interval.

> [!hint]- Show hint
> Require |1-alpha|<1.

> [!answer]- Show detailed answer
> For nonzero initialization, the exact state multiplier contracts when -1<1-alpha<1. Subtract one and reverse signs to obtain 0<alpha<2. The special initialization x0=0 stays fixed outside that interval too.

**Question (gd.q2.2):** At alpha=1.5 and x0=4, find x1, x2 and the two costs.

> [!hint]- Show hint
> The multiplier is -0.5.

> [!answer]- Show detailed answer
> x1=-2 and x2=1; their costs are 2 and 0.5. Signs alternate while magnitudes and cost decrease.

**Question (gd.q2.3):** Why does alpha=2 fail to contract a nonzero initial state?

> [!hint]- Show hint
> Compute the state multiplier and its square.

> [!answer]- Show detailed answer
> The state multiplier is -1, giving alternating states with constant magnitude. Its squared multiplier is 1, so the objective also remains constant.

**Question (gd.q2.4):** Can this exact recurrence be used for every smooth objective?

> [!hint]- Show hint
> Identify what made the derivative equal x.

> [!answer]- Show detailed answer
> No. The recurrence uses the exact quadratic derivative. A general smooth objective needs its own gradient and additional assumptions such as a Lipschitz gradient for a descent bound.
