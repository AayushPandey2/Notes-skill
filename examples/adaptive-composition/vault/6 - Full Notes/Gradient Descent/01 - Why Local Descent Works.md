---
id: gd.ch1
aliases:
- Why Local Descent Works
topic: Gradient Descent
tags:
- topic/first-order-descent-model
- subject/machine-learning
- domain/artificial-intelligence
- master-topic/machine-learning
- subdomain/optimization
- concept/first-order-descent-model
- concept/descent-direction-and-finite-step-length
- type/full-notes
nexttopics:
- '[[02 - Deriving the Update and Its Limits]]'
---
# Why Local Descent Works

## Why Local Descent Works

Suppose a model has one adjustable parameter x, and a differentiable objective f
measures the cost of choosing it. Our task is to find a parameter value with lower
cost using information available at the current point. Finding an exact global
minimum symbolically is often difficult. A derivative offers a local answer to a
smaller question: which nearby change should reduce the objective?

The derivative f'(x) is the slope of the tangent approximation. For a small change
d, differentiability gives f(x+d)=f(x)+f'(x)d+o(|d|). If f'(x) is positive, a negative
d makes the linear term negative; if f'(x) is negative, a positive d does so.
Choosing d=-alpha f'(x), with alpha positive, makes that linear term
-alpha[f'(x)]². This is why the negative derivative is a descent direction when
the derivative is nonzero. The neglected remainder is the reason a finite step
can still fail. Direction and step length solve different parts of the problem.

For a vector x, replace the derivative by the gradient, the vector of partial
derivatives. The directional first-order change becomes the inner product of the
gradient with the displacement. The direction of steepest decrease here uses the
Euclidean norm; changing the geometry changes the meaning of steepest. This
qualification matters when parameter scales differ substantially.

We will study f(x)=x²/2 first. It has a unique minimum at zero, a derivative x,
and constant curvature one. Starting at x=4 gives cost 8. A step of size
alpha=0.25 produces x=3 and cost 4.5. We have reduced cost without having to solve
the general optimization problem. This simple model will also reveal overshooting,
oscillation and divergence, rather than concealing them behind an attractive sketch.

A zero derivative means the first-order test is inconclusive. For this quadratic,
it identifies the minimum. For a nonconvex objective it can also identify a maximum
or saddle point. Do not turn a local derivative calculation into a global guarantee.
The next chapter derives exactly when the quadratic iteration succeeds.

For general gradient methods and their assumptions, consult
[Boyd and Vandenberghe, chapter 9](https://web.stanford.edu/~boyd/cvxbook/).
The particular scalar calculations below are derived directly from f(x)=x²/2.

## Check your understanding

**Question (gd.q1.1):** Why is the negative derivative locally useful?

> [!hint]- Show hint
> Write the linear term f'(x)d.

> [!answer]- Show detailed answer
> With d=-alpha f'(x), the linear term is -alpha[f'(x)]². It is negative for a nonzero derivative and positive alpha, but the neglected remainder still matters.

**Question (gd.q1.2):** For x=4 and alpha=0.25, what are the new state and cost?

> [!hint]- Show hint
> Use the derivative x for this quadratic.

> [!answer]- Show detailed answer
> The new state is 4-0.25(4)=3. The objective changes from 4²/2=8 to 3²/2=4.5.

**Question (gd.q1.3):** Does a zero derivative certify a minimum?

> [!hint]- Show hint
> Compare a positive and a negative quadratic.

> [!answer]- Show detailed answer
> No. At zero, both x²/2 and -x²/2 have zero derivative, but the second has a maximum. Curvature and the domain determine the conclusion.

**Question (gd.q1.4):** Does steepest decrease depend on the chosen norm?

> [!hint]- Show hint
> The norm constrains the allowed displacements.

> [!answer]- Show detailed answer
> Yes. The negative gradient gives steepest Euclidean first-order decrease per unit Euclidean displacement. A different geometry changes the constrained direction problem.
