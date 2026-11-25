# Physics Implementation Lab Blueprint

Use this lean, realization-focused blueprint for Physics companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed step-by-step walkthroughs, and honest evidence.

**Do not** include standalone chapters for opening metadata inventories, repeated theory, historical background, separate parameter-variation chapters, 10-step system chapters, quizzes/challenges, or repetitive summaries. **Do not** invent wet-lab measurements, and **never** force four programming tracks, ML splits, or gradient descent onto noncomputational physics topics.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Physical Realization Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Physical System & Quantity Contract
Briefly define the physical system, boundary, coordinate axes, sign conventions, idealizations, validity scales, and measurable quantities with SI units and resolution (or published-data / thought-experiment basis).

## Domain-Appropriate Physical Realization(s)

Choose the smallest meaningful physical realization—such as an analytical derivation + numerical prediction with uncertainty propagation, a supplied/published-data analysis, or a minimal numerical simulation *only* when closed form is unavailable.

Directly beneath the realization, include `> [!example]- Understand this implementation: mathematics, code, and numerical dry run` (or `> [!example]- Understand this realization: physics, calculation, and numerical dry run` for non-code realizations) covering **A–G**: system inputs & SI units, governing physical mechanism, step-by-step derivation/calculation/code order, one complete numerical dry run with unit cancellation and uncertainty propagation, physical interpretation & limits, failure cases (wrong sign, unit mismatch, violated idealization), and core-logic reconstruction.

## Verification Status

If code is present, end with **`Source and static review only; not compiled or executed here.`**; otherwise state **`Analytical, dimensional, and manual arithmetic review only (no physical apparatus or code executed).`**
