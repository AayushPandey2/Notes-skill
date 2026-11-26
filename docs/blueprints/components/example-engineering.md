# Worked Example & Exercise Engineering

## Purpose

Select example values and progression **deliberately** so examples expose the governing mechanism instead of accidentally hiding it.

## 1. Seven Deliberate Example Purposes & Validity Gate

| Example Type | Required Pedagogical Effect |
|---|---|
| **Minimal** | Isolate one central operation with minimal cognitive clutter |
| **Representative** | Reflect ordinary real-world or standard-case application conditions |
| **Discriminating** | Expose *why* two methods, models, or representations produce different decisions/results |
| **Boundary** | Test limiting, degenerate, empty, or threshold-edge behavior |
| **Counterexample** | Disprove an overgeneralization or show what breaks when a hypothesis is dropped |
| **Stress** | Reveal numerical instability, collinearity, or structural bottlenecks |
| **Transfer** | Require applying the mechanism in an unfamiliar context |

**Example Validity Gate (verify before drafting around any fixture):**
1. The example actually demonstrates the intended property with **complete preprocessing/fixture contracts**. For instance, in KNN feature scaling: compare Query `(30, ₹50,000)` against Candidate A `(20, ₹50,100)` and Candidate B `(29, ₹55,000)`. Unscaled Euclidean distances pick **A** (`≈ 100.50` vs. `≈ 5000.00`). With **training-fitted feature ranges** (`Age range = 20 years`, `Income range = ₹60,000`) applied to the query and candidates, range-normalized distances become A `= √((10/20)² + (100/60000)²) ≈ 0.5000` vs. B `= √((1/20)² + (5000/60000)²) ≈ 0.0972`, flipping the nearest neighbor to **B**. Different fitted ranges can yield different neighbors, so fitted parameters are part of the example.
2. Verify exact arithmetic where possible. For approximate computations, state the rounding convention, tolerance, and expected numerical accuracy.
3. Simplicity does not conceal the central mechanism or assumptions.
4. Values remain strictly consistent across prose, equations, code, and visuals.

A worked trace, a controlled contrast and a transfer check often answer different questions. Reuse the same dataset when this isolates a changed condition. Add a second example when it teaches a new consequence, tests a failure boundary or gives the learner independent practice. Specify scoring, preprocessing and relevant tie handling.

## 2. Guidance Fading Progression

For multi-example learning sequences and problem sets, fade scaffolding progressively without false numeric percentages:
**Complete solution $\to$ partial solution (learner fills intermediate steps) $\to$ optional hint $\to$ independent problem** (with collapsed `> [!tip]- Solution`).
