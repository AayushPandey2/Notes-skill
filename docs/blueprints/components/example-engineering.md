# Worked Example & Exercise Engineering

## Purpose

Select example values and progression **deliberately** so examples expose the governing mechanism instead of accidentally hiding it (e.g., unscaled features `[20, 30, 40]` vs. `[2, 12, 22]` hide feature-scale domination in KNN, whereas `[20, 30, 40]` vs. `[20000, 50000, 80000]` exposes it immediately).

## 1. Seven Deliberate Example Purposes

Review every significant example before building prose around it; select only the types needed by the objective:

| Example Type | Required Pedagogical Effect |
|---|---|
| **Minimal** | Isolate one central operation with minimal cognitive clutter |
| **Representative** | Reflect ordinary real-world or standard-case application conditions |
| **Discriminating** | Expose *why* two methods, models, or representations behave differently |
| **Boundary** | Test limiting, degenerate, empty, or threshold-edge behavior |
| **Counterexample** | Disprove an overgeneralization or show what breaks when a hypothesis is dropped |
| **Stress** | Reveal numerical instability, collinearity, or structural bottlenecks |
| **Transfer** | Require applying the mechanism in an unfamiliar context |

## 2. Guidance Fading Progression

For multi-example learning sequences and problem sets, alternate worked examples with progressively faded practice:
1. **Fully worked example (100% guidance):** Complete steps, reasoning, and verification shown.
2. **Partially completed example (~70% guidance):** Setup and governing method supplied; learner predicts key intermediate transitions (with collapsed reveal).
3. **Hint-supported problem (~35% guidance):** Problem and governing cue/hint only; full solution collapsed.
4. **Independent problem (0% guidance):** Unscaffolded problem with concealed solution (`> [!tip]- Solution`).
