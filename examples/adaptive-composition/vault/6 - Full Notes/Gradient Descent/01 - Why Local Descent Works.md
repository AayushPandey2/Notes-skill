---
id: gd.ch1
aliases:
- Why Local Descent Works
topic: Gradient Descent
tags:
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
