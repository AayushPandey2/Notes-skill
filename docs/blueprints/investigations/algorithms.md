# Algorithms & Data Structures Implementation Lab Blueprint

Use this lean, implementation-focused blueprint for Data Structures & Algorithms companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed **A–G** walkthroughs beneath every implementation, experiment integrity, and static correctness review.

**Do not** include standalone chapters for opening metadata inventories, repeated theory, historical background, or repetitive summaries. **Honor the user's requested language**—never force Python and Rust onto every DSA lab unless explicitly requested.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Algorithms & Data Structures Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Problem Contract & Discriminating Fixture
Define input/output types, bounds (`n`, ordering/uniqueness invariants, empty/single/duplicate cases), target time/space complexity, and one discriminating fixture traced across tracks.

## Four DSA Tracks (Apply Track-Applicability Gate)

1. **Track 1 — Baseline:** Simplest correct approach exposing redundant work (omit when the optimal approach is already direct; for data structures, implement the minimal internal representation).
2. **Track 2 — Improved Algorithm / Core Operations:** Efficient solution using the governing invariant (loop/recursion invariant, amortized or structural invariant).
3. **Track 3 — Alternative Representation:** Recursive vs. iterative variant, or standard-library alternative showing API/complexity trade-offs.
4. **Track 4 — Verification & Boundary Suite:** Edge cases (empty, single element, duplicates, missing target, overflow/bounds), complexity verification, and invariant-violation failure analysis.

Directly beneath each implementation, include `> [!example]- Understand this implementation: mathematics, code, and numerical dry run` covering **A–G**: **A** input bounds & invariants; **B** governing invariant & time/space cost model; **C** line-by-line execution order; **D** complete dry run on the discriminating fixture; **E** returned state/complexity outcome; **F** off-by-one, mid-overflow, empty-input, or broken-invariant failures; **G** core-algorithm reconstruction.

## Verification Status

State result status honestly (**Expected** / **Analytical**, never **Executed**) and end with **`Source and static review only; not compiled or executed here.`**
