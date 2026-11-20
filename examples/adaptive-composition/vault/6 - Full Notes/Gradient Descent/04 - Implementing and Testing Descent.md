---
id: gd.ch4
aliases:
- Implementing and Testing Descent
topic: Gradient Descent
tags:
- type/full-notes
nexttopics:
- '[[05 - Curvature and Failure Analysis]]'
---
# Implementing and Testing Descent

## Implementing and Testing Descent

This complete implementation uses only Python 3's standard library. The objective
is fixed to x²/2 so that the mathematical reference remains independent of the
loop. A general optimizer would accept a gradient callback and document its shape
and domain contract; this small example keeps those concerns explicit and limited.

```python
import math

def descend(x, alpha, iterations):
    if not math.isfinite(x) or not math.isfinite(alpha) or alpha <= 0:
        raise ValueError("finite initial state and positive step required")
    if type(iterations) is not int or iterations < 0:
        raise ValueError("nonnegative integer count required")
    states = [x]
    for _ in range(iterations):
        x -= alpha * x
        if not math.isfinite(x):
            raise ArithmeticError("nonfinite iterate")
        states.append(x)
    return states

states = descend(4.0, 0.25, 12)
assert len(states) == 13
for k, value in enumerate(states):
    assert math.isclose(value, 4.0 * 0.75**k, rel_tol=1e-12)
assert descend(4.0, 1.0, 1) == [4.0, 0.0]
assert descend(4.0, 2.0, 2) == [4.0, -4.0, 4.0]
assert descend(4.0, 0.25, 0) == [4.0]
```

The closed-form assertion tests the computation against a separately derived
expression. The length assertion tests trace semantics. The alpha=1 case checks
one-step minimization, alpha=2 checks the stability boundary, and the zero-step
case checks that initialization is returned without an update. These tests cover
different observable obligations rather than simply repeating the loop statements.

The finite-state guard detects numerical overflow; it does not reject every
mathematically divergent choice in advance. For example, alpha=2.1 initially
produces finite values that grow. A diagnostic should distinguish a step-size
instability from overflow encountered much later. Conversely, a finite answer
after twelve iterations is not evidence of convergence.

Production stopping conditions often combine a gradient norm, an update-size
threshold and an iteration cap. Each has limitations. A small gradient can be
caused by poor scaling; a small update can be caused by a tiny step; reaching the
cap means the budget ended. Report the stopping reason rather than converting
every termination into success. Floating-point tolerance checks need an absolute
tolerance near zero and a relative tolerance for larger values.
