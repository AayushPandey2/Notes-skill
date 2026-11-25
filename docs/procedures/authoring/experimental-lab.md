# Companion Implementation Lab Contract

For each newly generated non-video content note, create or update a **3-file topic bundle**: the content note (`<note stem>.md`), its sibling `<note stem> - Experimental Lab.md`, and its sibling `<note stem> - Cheatsheet & Interview Q&A.md` ([cheatsheet-interview.md](cheatsheet-interview.md)). Exclude `/scribe-ytnotes` video notes, playlist indexes, MOCs, labs, cheatsheet packs, and internal workflow documents; do not create companions retroactively across a vault. Link all three files reciprocally, share the active YAML profile, and keep definitions, symbols, datasets, assumptions, and conventions strictly consistent with the parent note.

## Lean Implementation-Focused Structure

Replace long multi-chapter experimental labs with a focused, implementation-first document. **Do not** include standalone sections for:

- Opening metadata inventories (`Level`, `Prerequisites`, `Languages`, `Libraries`, `Objectives`).
- Repeated theory chapters (theory lives in `<note stem>.md`).
- Historical background or general experimental investigations.
- Professional-workflow chapters (e.g., 12-step project walkthroughs or hyperparameter sweeps).
- Quiz and challenge chapters, learning roadmaps, repository-structure recommendations, or repetitive final summaries.

Do not recreate removed chapters under different names. Retain **only**:

1. **Title and parent-note navigation:** Line-1 YAML frontmatter, `# <Topic> — Implementation Lab`, and a concise navigation callout linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.
2. **Brief shared problem and I/O contract:** State the central task, dataset/inputs, target, objective scaling, intercept/regularization conventions, prediction meaning, and comparison criteria shared across the tracks.
3. **Relevant implementation tracks:**
   - **Machine Learning:** Always provide **4 comparable tracks** (Python + NumPy, Python libraries, Rust from scratch, Rust using Linfa or SmartCore) per [machine-learning.md](../../blueprints/investigations/machine-learning.md).
   - **Other domains:** Choose only domain-appropriate realizations per `deep-learning.md`, `coding.md`, `mathematics.md`, `physics.md`, `chemistry.md`, or `general.md`. Never force four programming tracks, gradient descent, or ML libraries onto unrelated subjects.
4. **Setup beside each track:** Show necessary dependencies, versions, or `Cargo.toml` manifests as Markdown learning material directly beside each track, with a proportionate collapsed explanation beneath supporting blocks.
5. **Complete code:** Place complete implementations inside properly formatted Markdown code fences (never create Python files, Rust projects, scripts, downloaders, builders, or validators).
6. **Immediately following collapsed explanations:** Directly beneath every implementation's code block, include:

```markdown
> [!example]- Understand this implementation: mathematics, code, and numerical dry run
> ...
```

7. **Brief, accurate verification status:** End every lab containing code with:

**`Source and static review only; not compiled or executed here.`**

Integrate essential examples, comparisons, limitations, and checks directly into the collapsed explanations rather than separate chapters.

## Collapsed Implementation Walkthrough Standard (A–G)

Keep the full implementation visible before its walkthrough. Inside `> [!example]- Understand this implementation: mathematics, code, and numerical dry run`, quote **every** line—including blank lines—with `>` so Obsidian keeps the entire walkthrough inside one collapsed callout. Supporting blocks (imports, `pip install`, `Cargo.toml`) receive a proportionate collapsed explanation directly beneath them rather than repeating an entire long walkthrough.

Every full implementation walkthrough must include sections **A through G**:

- **A. Understand the inputs and state:** Define inputs, targets, shapes, types, units, assumptions, parameters, and settings using one consistent miniature dataset. Explain why inputs are prepared (centered, standardized, initialized, validated) and how original interpretations (such as intercept recovery) are recovered.
- **B. Understand the mathematical mechanism:** Establish the algorithmic distinction (what this method changes compared with an alternative and why it matters), explicitly define objective scaling (SSE vs MSE vs half-MSE, normalized vs unnormalized penalties), derive or justify operations and library parameter conversions from that objective, and unpack intermediate quantities (`rho`, partial residual, gradient, threshold) before use.
- **C. Follow the implementation in order:** For every meaningful line or tightly related group in execution order: (1) quote the expression, (2) explain its purpose, (3) explain unfamiliar syntax, (4) identify entering values and shapes, (5) explain the internal operation, (6) show the output or state change (explicitly tracking sequential vs simultaneous updates), and (7) connect it to the next operation.
- **D. Complete a numerical dry run:** Trace one full meaningful operation with actual numbers (showing products, sums, norms, thresholds, updated values, and intercept recovery, while qualifying special dataset properties such as orthogonal features):
  - *Gradient-based:* **Initialization → predictions → errors → gradient → update → new state → interpretation.**
  - *Coordinate descent:* **Current state → partial residual → coordinate statistic → threshold → updated coordinate → next coordinate → completed sweep.**
  - *Noniterative method:* Trace its actual construction or inference process.
- **E. Interpret the output:** Explain returned values, parameter meanings (e.g., why a coefficient becomes zero or a probability changes), predictions, losses, and metrics, distinguishing training behavior from evidence of generalization and stating what the result does not prove.
- **F. Explain failure cases:** Cover invalid inputs, shape mistakes, unstable arithmetic, incorrect operators, and violated assumptions using: **Problematic approach → failure mechanism → correction → explanation.**
- **G. Reconstruct the core logic:** Finish with a short plain-language sequence enabling the learner to explain the implementation independently.

## Instruction-Only & Static Correctness Review Gate

Never execute code, compile Rust, run Cargo, install dependencies, probe local runtimes, or create executable scripts/projects. Review every displayed implementation statically before finalizing:

1. **Operators:** Check every `*` vs `@`, `**` vs `^`, matrix vs element-wise operations, integer vs floating-point division, and logical vs bitwise operators based on types, shapes, and mathematics.
2. **Gradients, Updates & Objective Scaling:** Check signs, averaging factors, transposes, bias updates, penalty gradients, threshold scaling, update ordering, stopping criteria, zero-denominator cases, and library hyperparameter conversions (`C`, `alpha`, `penalty`). Choose optimizers honestly (never force gradient descent onto coordinate-descent, proximal, tree, nearest-neighbor, or quasi-Newton methods).
3. **Implementation Completeness:** Check syntax, indentation, imports, defined variables, consistent naming, input/output shapes, official versioned API consistency, dependencies, bounds, empty inputs, and numerical guards using hand calculations where feasible. Never copy `"Expected output"` from unexecuted references as verified output.
