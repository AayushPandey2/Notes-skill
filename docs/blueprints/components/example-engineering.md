# Worked Example & Exercise Engineering

## Purpose

Select example values and progression **deliberately** so examples expose the governing mechanism instead of accidentally hiding it.

## 1. Seven Deliberate Example Purposes, Completeness & Validity Gate

Select examples by educational function—introducing an **early representative concrete example near the beginning** of abstract topics before heavy theory or formal mathematics (never starting with an example requiring untaught concepts or repeating identical numeric substitutions without new insight):

| Example Purpose | Required Pedagogical Effect |
|---|---|
| **Initial intuitive** | Establish the basic idea early through an accessible real-world situation |
| **Simple mathematical** | Introduce relevant quantities and calculations without cognitive clutter |
| **Complete representative** | Demonstrate the full central mechanism under standard conditions |
| **Contrasting (parameter behavior)** | Hold data fixed and change one condition (parameter magnitude, scaling, uniform vs. weighted rule, assumption, input encoding, or operating validity) to expose *why* behavior or decisions flip |
| **Boundary** | Test limiting, degenerate, empty, tie, or threshold-edge behavior |
| **Failure** | Demonstrate an incorrect method, violated assumption, numerical instability, or unsuitable regime |
| **Transfer** | Require applying the governing principle to a different problem or context |

**Complete worked-example architecture:** For consequential worked examples, state clearly: **(1)** what is given, **(2)** what must be determined, **(3)** why the chosen method applies, **(4)** which relationships/assumptions are required, **(5)** how each consequential step works, **(6)** what intermediate results mean, **(7)** what the final answer represents, and **(8)** a sanity/reasonableness check of the outcome—never merely plugging numbers into a formula and printing a bare answer. Place misconception counterexamples contextually right where a concept is prone to confusion rather than postponing all warnings to a final section.

**Example Validity Gate (verify before drafting around any worked example):**
1. The example actually demonstrates the intended property with **complete preprocessing and initial-condition contracts**. For instance, in KNN feature scaling: compare Query `(30, ₹50,000)` against Candidate A `(20, ₹50,100)` and Candidate B `(29, ₹55,000)`. Unscaled Euclidean distances pick **A** (`≈ 100.50` vs. `≈ 5000.00`). With **training-fitted feature ranges** (`Age range = 20 years`, `Income range = ₹60,000`) applied to the query and candidates, range-normalized distances become A `= √((10/20)² + (100/60000)²) ≈ 0.5000` vs. B `= √((1/20)² + (5000/60000)²) ≈ 0.0972`, flipping the nearest neighbor to **B**. Different fitted ranges can yield different neighbors, so fitted parameters are part of the example.
2. Verify exact arithmetic where possible. For approximate computations, state the rounding convention, tolerance, and expected numerical accuracy.
3. Simplicity does not conceal the central mechanism or assumptions.
4. Values remain strictly consistent across prose, equations, code, and visuals.
5. **Iterative & multi-stage trace completeness:** For sequential or iterative algorithms (such as boosting rounds, gradient descent steps, iterative root-finding, or state transitions), trace **at least two rounds/iterations** whenever one round cannot show how updated predictions/states feed into recomputed errors, gradients, or states; trace how an unseen input passes through the trained/final artifact to produce a prediction; and check all relevant decision branches (e.g., evaluating both child nodes before concluding tree stopping) instead of checking one branch silently. Keep tables compact and show step-by-step arithmetic in prose or display equations rather than packing wide formula-heavy tables.
6. **Continuous running examples & independent transfer:** For substantial interconnected topics, consider carrying one consistent **running example** across units (preserving values, notation, assumptions, and intermediate results) alongside additional independent examples for transfer beyond the original setup—never forcing a running example onto topics where it adds no benefit.

A worked trace, a controlled contrast and a transfer check often answer different questions. Reuse the same dataset when this isolates a changed condition. Add a second example when it teaches a new consequence, tests a failure boundary or gives the learner independent practice. Specify scoring, preprocessing and relevant tie handling. Compute and inspect both outcomes before choosing a contrast. If the result does not distinguish the mechanisms, revise the values or state what stayed the same and why.

## 2. Progressive Example Support (Guidance Fading)

For substantial problem-solving topics (without forcing this progression onto every minor concept), fade scaffolding gradually using collapsible `[!hint]-` and `[!success]-` blocks appropriately:
**(1) Fully worked example $\to$ (2) Guided example $\to$ (3) Partially solved problem $\to$ (4) Independent application** (without false numeric percentages).
