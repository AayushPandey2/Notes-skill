# Chemistry Implementation Lab Blueprint

Use this lean, realization-focused blueprint for Chemistry companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed step-by-step walkthroughs, and honest evidence.

**Do not** include standalone chapters for opening metadata inventories, repeated theory, historical background, separate condition-variation chapters, 10-step analytical chapters, quizzes/challenges, or repetitive summaries. **Do not** invent wet-lab observations, unsafe procedures, or force four programming tracks, ML splits, or gradient descent onto noncomputational chemistry topics.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Chemical Realization Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Chemical System & Condition Contract
Briefly define species, phases, concentrations, temperature/pressure, safe handling scope (explicitly noting paper/published-data mode when no wet lab is performed), and conserved quantities (atoms, charge).

## Domain-Appropriate Chemical Realization(s)

Choose the smallest meaningful chemical realization—such as balanced symbolic equations + macroscopic–particle–symbolic stoichiometric/equilibrium/rate calculation, supplied/published analytical data processing, or a minimal kinetics/equilibrium script *only* when numerical root-finding or ODE integration is genuinely required.

Directly beneath the realization, include `> [!example]- Understand this implementation: mathematics, code, and numerical dry run` (or `> [!example]- Understand this realization: chemistry, procedure, and numerical dry run` for non-code realizations) covering **A–G**: species/inputs & units, particle-to-symbolic mechanism, step-by-step calculation/code order, one complete numerical dry run (moles, limiting reagent, equilibrium/pH, significant figures), chemical interpretation & competing mechanisms, failure cases (unbalanced charge, wrong stoichiometry, activity vs concentration), and core-logic reconstruction.

## Verification Status

If code is present, end with **`Source and static review only; not compiled or executed here.`**; otherwise state **`Stoichiometric, balance, and manual arithmetic review only (no wet lab or code executed).`**
