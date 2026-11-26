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
1. The example actually demonstrates the intended property (e.g., for KNN feature scaling, choose values where scaling **flips the nearest neighbor**—such as query `(30, ₹50,000)` with Candidate A `(20, ₹50,100)` vs. Candidate B `(29, ₹55,000)`, where unscaled distance picks A `≈ 100.5` vs. `5000.0` while range-normalized distance picks B—rather than merely showing different feature ranges).
2. Arithmetic and intermediate values are verified exact.
3. Simplicity does not conceal the central mechanism or assumptions.
4. Values remain strictly consistent across prose, equations, code, and visuals.

## 2. Guidance Fading Progression

For multi-example learning sequences and problem sets, fade scaffolding progressively without false numeric percentages:
**Complete solution $\to$ partial solution (learner fills intermediate steps) $\to$ optional hint $\to$ independent problem** (with collapsed `> [!tip]- Solution`).
