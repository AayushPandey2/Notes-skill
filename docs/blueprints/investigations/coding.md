# Coding Implementation Lab Blueprint

Use this lean, implementation-focused blueprint for programming, algorithms, data structures, APIs, and software engineering companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed **A–G** walkthroughs beneath every implementation, zero local execution, and static correctness review.

**Do not** include standalone chapters for opening metadata inventories, repeated theory, historical background, scaling-experiment chapters, 12-step modular builds, quizzes/challenges, or repetitive summaries. **Do not** force ML splits, gradient descent, or 4-language ML/Rust stacks onto general coding topics.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Implementation Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Problem Contract & Discriminating Fixture
Briefly define input/output types, bounds (`n`, value ranges, mutability, empty/duplicate behavior), and one discriminating miniature fixture traced across the implementation(s).

## Implementation Tracks

Choose only relevant tracks (often one optimal implementation, or baseline + optimal when the baseline exposes the core bottleneck, plus an optional idiomatic/secondary-language comparison when genuinely instructive). For each track:
- `### [Implementation name]` + short rationale.
- Setup/dependencies block + proportionate collapsed explanation.
- Complete code block.
- Immediately beneath it, `> [!example]- Understand this implementation: mathematics, code, and numerical dry run` covering **A–G** (inputs & bounds, invariants & complexity cost model, line-by-line execution order, concrete dry run on the discriminating fixture, output interpretation, off-by-one/aliasing/overflow failure cases, and core-logic reconstruction).

## Verification Status

End with **`Source and static review only; not compiled or executed here.`**
