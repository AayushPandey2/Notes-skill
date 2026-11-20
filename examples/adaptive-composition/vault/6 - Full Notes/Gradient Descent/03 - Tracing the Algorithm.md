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

## Check your understanding

**Question (gd.q3.1):** What does trace entry k represent?

> [!hint]- Show hint
> Distinguish initialization from updates.

> [!answer]- Show detailed answer
> Entry zero is the initialization. Entry k is the state after k completed simultaneous updates, so K updates return K+1 entries.

**Question (gd.q3.2):** Complete the alpha=0.25 trace after x=2.25.

> [!hint]- Show hint
> Evaluate the gradient at the old state.

> [!answer]- Show detailed answer
> The gradient is 2.25 and displacement is -0.5625, giving next state 1.6875. Recomputing during coordinate writes would change a vector algorithm.

**Question (gd.q3.3):** Can twelve finite iterates establish long-run convergence?

> [!hint]- Show hint
> Separate a finite observation from the multiplier proof.

> [!answer]- Show detailed answer
> No. A divergent multiplier can produce finite outputs for many steps. The exact closed form and its contraction condition establish the long-run behavior for this quadratic.

**Question (gd.q3.4):** How can final-state storage reduce memory?

> [!hint]- Show hint
> Which entries does a final-state client consume?

> [!answer]- Show detailed answer
> Keep only the current scalar state and overwrite it after computing the gradient from the old value. This uses O(1) working storage while retaining O(K) arithmetic work.

![[assets/scriptorium/dc77bb9061f9b8f9e757d16a9019cfe646b558687d59fa724f3e60a2e6d3c49c.svg]]

These deterministic synthetic trajectories illustrate the proved recurrence; they are not training experiments.
