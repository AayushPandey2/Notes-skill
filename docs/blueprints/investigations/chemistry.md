# Chemistry Implementation Lab Blueprint

Use this lean, realization-focused blueprint for Chemistry companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) and [physical lab safety policy](../../procedures/safety/physical-lab-safety.md) govern structure, collapsed step-by-step walkthroughs, safe chemical boundaries, and honest evidence.

**Do not** include standalone chapters for opening metadata inventories, repeated theory, historical background, separate condition-variation chapters, 10-step analytical chapters, quizzes/challenges, or repetitive summaries. **Do not** invent wet-lab observations, supply hazardous synthesis/handling instructions, or force four programming tracks, ML splits, or gradient descent onto noncomputational chemistry topics.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Chemical Realization Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Chemical System & Condition Contract
Briefly define species, phases, concentrations, temperature/pressure, safe handling scope (explicitly noting analytical/published-data mode when no wet lab is performed), and conserved quantities (atoms, charge).

## Four Chemistry Tracks (Apply Track-Applicability Gate)

1. **Track 1 — Symbolic & Molecular:** Balance equations and connect particle-level mechanisms (electron flow, collisions, equilibrium exchange) to macroscopic symbols.
2. **Track 2 — Quantitative Calculation:** Compute stoichiometry, pH/equilibrium, reaction rates, or $\Delta G / \Delta H$ under explicitly justified assumptions.
3. **Track 3 — Experimental or Published Analysis:** Interpret supplied or published analytical data (e.g., titration curve, spectroscopy, calorimetry) without fabricating wet-lab readings.
4. **Track 4 — Condition & Validity Analysis:** Examine how temperature, pressure, concentration, buffering, or ionic strength alter outcomes and break ideal approximations.

Directly beneath each realization, include `> [!example]- Understand this realization: chemistry, procedure, and numerical dry run` (or `...implementation...` when simulation code appears) covering **A–G**: **A** species, mole/charge balances, conditions, units; **B** particle-to-symbolic mechanism; **C** step-by-step calculation/procedure order; **D** complete numerical dry run with significant figures; **E** chemical interpretation & competing pathways; **F** failure cases (unbalanced charge, wrong stoichiometry, activity vs. concentration); **G** core-logic reconstruction.

## Verification Status

If code is present, end with **`Source and static review only; not compiled or executed here.`**; otherwise state **`Stoichiometric, balance, and manual arithmetic review only (no wet lab or code executed).`**
