---
id: gd.ch3
aliases:
- Tracing the Algorithm
topic: Gradient Descent
tags:
- type/full-notes
nexttopics:
- '[[04 - Implementing and Testing Descent]]'
---
# Tracing the Algorithm

## Tracing the Algorithm

The input is an initial real state x_0, a positive step alpha, and an iteration
count K. The output is the sequence of K+1 states, including the initial state.
The algorithm stores a current state, evaluates its gradient, subtracts the
scaled gradient, and then records the new state. Defining whether a trace records
the state before or after an update prevents a common off-by-one error.

With x_0=4 and alpha=0.25, the first states are shown below. Each gradient is
computed at the state in that row; the last column is the next row's state.

| k | current x_k | gradient | displacement | next x |
|---|---|---|---|---|
| 0 | 4 | 4 | -1 | 3 |
| 1 | 3 | 3 | -0.75 | 2.25 |
| 2 | 2.25 | 2.25 | -0.5625 | 1.6875 |

The update is simultaneous with respect to the old state. In a vector program,
overwriting coordinates one at a time while recomputing gradients would implement
a different procedure. Keep the old iterate available until all coordinates of
the gradient have been evaluated.

The loop invariant is that, after k completed updates, the recorded list has k+1
entries and its last entry equals (1-alpha)^k x_0 in exact arithmetic. The invariant
holds before the loop, and the recurrence preserves both its numerical and list
length statements. At termination k=K, it proves what the returned trace means.
It does not assert that K updates meet a particular accuracy target.

![[assets/quadratic-iterations.svg]]

The curves use the exact recurrence on a synthetic quadratic, not experimental
training measurements. The stable alpha=0.25 curve keeps its sign; alpha=1.5
alternates with decreasing amplitude; alpha=2.1 grows in magnitude. The axes show
state rather than objective, which makes oscillation visible. A loss plot alone
would hide sign changes. The plotted finite horizon illustrates the derived
conditions; the proof in the preceding chapter establishes their long-run meaning.

Each scalar update takes constant arithmetic work, so K steps require O(K) work.
Storing the full trace requires O(K) space. If only the final state is needed,
the working state requires O(1) space. For a vector objective, gradient-evaluation
cost and parameter dimension replace these scalar assumptions.
