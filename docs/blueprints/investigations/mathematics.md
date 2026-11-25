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

## Four Mathematical Tracks (Apply Track-Applicability Gate)

Select all 4 tracks for comprehensive mathematical topics (or the meaningful subset for narrower concepts), never forcing irrelevant programming tracks onto non-computational mathematics:
1. **Track 1 — Analytical:** Exact symbolic derivation, proof, or formal construction.
2. **Track 2 — Concrete Numerical:** Fully worked exact-arithmetic example using small inspectable values (e.g., eigenvalues/eigenvectors of a $2\times 2$ matrix).
3. **Track 3 — Alternative Representation:** Geometric, graphical, or second independent mathematical method illuminating why the result holds.
4. **Track 4 — Verification & Boundary Cases:** Independent check (e.g., substituting $A\mathbf{v} = \lambda\mathbf{v}$), counterexamples, degenerate/defective cases, and hypothesis-relaxation checks (plus a minimal computational verification snippet *only* if computation is part of the objective).

Directly beneath each realization, include `> [!example]- Understand this realization: mathematics, steps, and numerical dry run` (or `...implementation: mathematics, code, and numerical dry run` when code is included) covering **A–G**: **A** definitions, hypotheses, quantifiers, domain restrictions; **B** governing mathematical mechanism; **C** step-by-step justified logical transitions; **D** complete exact-arithmetic dry run + boundary case; **E** interpretation & scope; **F** failure cases (dividing by zero, assuming the converse, defective/degenerate failures); **G** core-argument reconstruction.

## Verification Status

State what was verified by hand (**Analytical** / **Hand-calculated**). If code is present, end with **`Source and static review only; not compiled or executed here.`**; otherwise state **`Analytical and manual arithmetic review only (no code executed).`**
