# Mathematics Implementation Lab Blueprint

Use this lean, realization-focused blueprint for Mathematics companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed step-by-step walkthroughs, and honest verification.

**Do not** include standalone chapters for opening metadata inventories, repeated theory, historical background, conjecture-experiment chapters, 10-step applied-modeling chapters, quizzes/challenges, or repetitive summaries. **Do not** force four programming tracks, Python/Rust libraries, datasets, train/test splits, or gradient descent onto mathematical topics unless computation is genuinely part of the mathematical objective.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Mathematical Realization Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Mathematical Task & Domain Contract
Briefly state the claim, construction, or problem, along with exact definitions, symbols, quantifiers, admissibility/domain restrictions, and one concrete instance.

## Domain-Appropriate Mathematical Realization(s)

Choose the smallest meaningful mathematical realization—such as a symbolic derivation/proof paired with normal and degenerate/boundary cases, an explicit construction with hypothesis-relaxation checks, or a minimal computational verification snippet *only* when computation is genuinely part of the mathematical task.

Directly beneath the realization, include `> [!example]- Understand this implementation: mathematics, code, and numerical dry run` (or `> [!example]- Understand this realization: mathematics, steps, and numerical dry run` for non-code derivations) covering **A–G**: inputs/hypotheses, mathematical mechanism, step-by-step logical transitions, a complete exact-arithmetic dry run (plus boundary case), interpretation, failure cases (e.g., dividing by zero, assuming the converse), and core-argument reconstruction.

## Verification Status

State what was verified by hand. If code is present, end with **`Source and static review only; not compiled or executed here.`**; otherwise state **`Analytical and manual arithmetic review only (no code executed).`**
