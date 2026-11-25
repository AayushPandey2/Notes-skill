# Physics Implementation Lab Blueprint

Use this lean, realization-focused blueprint for Physics companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) and [physical lab safety policy](../../procedures/safety/physical-lab-safety.md) govern structure, collapsed step-by-step walkthroughs, safe scope, and honest evidence.

**Do not** include standalone chapters for opening metadata inventories, repeated theory, historical background, separate parameter-variation chapters, 10-step system chapters, quizzes/challenges, or repetitive summaries. **Do not** invent wet-lab/apparatus measurements, prescribe hazardous high-energy setups, or force four programming tracks, ML splits, or gradient descent onto noncomputational physics topics.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Physical Realization Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Physical System & Quantity Contract
Briefly define the physical system, boundary, coordinate axes, sign conventions, idealizations, validity scales, and measurable quantities with SI units and resolution (explicitly labeling **Analytical** / **Expected** / **Published** basis when no physical experiment is conducted).

## Four Physics Tracks (Apply Track-Applicability Gate)

1. **Track 1 — Analytical Model:** Derive governing physical relationships from conservation laws or equations of motion under stated idealizations.
2. **Track 2 — Safe Physical Investigation:** Explain safe educational apparatus, measurement procedure, effective quantities, and resolution techniques (or published/simulated setup for hazardous/large-scale regimes per [physical-lab-safety.md](../../procedures/safety/physical-lab-safety.md)).
3. **Track 3 — Numerical Model:** Calculate or simulate predicted behavior across varied parameters (explicitly marking outputs **Analytical** / **Expected**, never observed readings).
4. **Track 4 — Data & Uncertainty Analysis:** Propagate measurement uncertainties, check dimensional consistency, and diagnose idealization breakdown (air drag, finite amplitude, friction).

Directly beneath each realization, include `> [!example]- Understand this realization: physics, calculation, and numerical dry run` (or `...implementation...` if simulation code appears) covering **A–G**: **A** system inputs, axes, SI units; **B** governing physical mechanism; **C** step-by-step derivation/calculation/procedure order; **D** complete numerical dry run with unit cancellation and uncertainty propagation; **E** physical interpretation & validity limits; **F** failure cases (wrong sign, unit mismatch, violated idealization); **G** core-logic reconstruction.

## Verification Status

If code is present, end with **`Source and static review only; not compiled or executed here.`**; otherwise state **`Analytical, dimensional, and manual arithmetic review only (no physical apparatus or code executed).`**
