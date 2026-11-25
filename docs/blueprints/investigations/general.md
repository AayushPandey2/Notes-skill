# General Implementation Lab Blueprint

Use this lean, realization-focused blueprint when a named STEM or coding domain would impose irrelevant machinery (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed step-by-step walkthroughs, and honest verification.

**Do not** include standalone chapters for opening metadata inventories, repeated theory, historical background, separate variation chapters, 10-step practical-workflow chapters, quizzes/challenges, or repetitive summaries. **Do not** insert Python, Rust, ML metrics, gradient descent, chemical apparatus, or physical measurements without genuine need.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Practical Realization Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Task, Inputs & Success Criteria
Briefly define the practical deliverable, given inputs/constraints, one small shared case, and concrete observable success criteria.

## Domain-Appropriate Practical Realization(s)

Choose the smallest meaningful realization—such as a first-principles worked construction or decision procedure on the shared case (optionally paired with one established method when comparison adds clarity), or a structured evidence-analysis walkthrough (with code *only* if software execution is genuinely part of the topic).

Directly beneath the realization, include `> [!example]- Understand this implementation: mathematics, code, and numerical dry run` (or `> [!example]- Understand this realization: method, steps, and worked dry run` for non-code realizations) covering **A–G**: inputs & criteria, governing principle, step-by-step execution order, one complete worked dry run on the shared case, output interpretation, failure cases & violated assumptions, and core-logic reconstruction.

## Verification Status

If code is present, end with **`Source and static review only; not compiled or executed here.`**; otherwise state **`Manual logical and criteria-based review only (no code executed).`**
