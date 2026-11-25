# Machine Learning Implementation Lab Blueprint

Use this lean, implementation-focused blueprint for Machine Learning companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, the collapsed **A–G** walkthrough directly beneath every implementation, zero local execution, and static correctness review.

**Do not** include standalone chapters for opening metadata inventories, repeated theory, historical background, general experimental investigations, 12-step project workflows or `GridSearchCV` chapters, quiz/challenge chapters, learning roadmaps, repo-structure recommendations, or repetitive final summaries. Integrate examples, comparisons, limitations, and checks directly into the collapsed walkthroughs.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Implementation Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Problem and Input/Output Contract
Define **one central learning task** teachable across all four tracks, aligning:
- Dataset, feature representation, and target convention.
- Objective scaling (explicitly distinguishing SSE, MSE, half-MSE, normalized vs unnormalized penalties) and intercept treatment.
- Regularization convention, prediction meaning, and comparison criteria.
- Genuine solver or hyperparameter-scaling conversions (never claim equivalence where formulations differ).

## Optimizer Selection & Honesty

Choose and explain the **actual** appropriate optimizer or solver for each track—never force ordinary gradient descent onto every algorithm:
- Coordinate descent (sequential coordinate updates with partial residuals), proximal gradient descent (smooth gradient step + nonsmooth soft-thresholding), batch/mini-batch/stochastic GD, quasi-Newton (L-BFGS), closed-form solvers, or tree/nearest-neighbor construction.
- Inside the collapsed walkthrough (**B**, **C**, **D**), cover: objective, parameters, gradient or coordinate-update rule, batch usage, learning rate, threshold/proximal operation (where applicable), stopping criterion, numerical limitations, and alternatives/trade-offs. If a desired optimizer is unsupported by the library, state that honestly and use a documented alternative without inventing solver options.

## Four Mandatory Implementation Tracks

Every applicable ML lab must provide all four tracks below, structured consistently as:
- `### [Implementation name]` + short explanation of what it demonstrates and why its tools fit.
- Setup/dependencies block + proportionate collapsed explanation (`> [!example]- Understand this setup`).
- Complete implementation in a fenced code block.
- Immediately beneath it, `> [!example]- Understand this implementation: mathematics, code, and numerical dry run` covering **A–G** (inputs & state, mathematical mechanism & objective scaling, line-by-line execution order, full numerical dry run with intermediate values, output interpretation, failure cases, and core-logic reconstruction).

1. **Python and NumPy:** Expose central calculations (centering, dot products, norms, gradients/partial residuals, thresholding/updates) directly; explain vectorization, axes, shapes, and broadcasting through small numbers.
2. **Python Libraries (e.g., `scikit-learn`):** Explain what fitting does internally, the actual solver, configuration, objective-parameter conversion (e.g., `C` or `alpha`), learned state, and prediction behavior—never reduce this track to `.fit()`.
3. **Rust from Scratch:** Use clear, readable Rust; explain types, mutability, borrowing/references, slices, indexing, iteration, numeric conversions (`as f64`), error handling, and sequential vs simultaneous state updates.
4. **Rust Using Linfa or SmartCore:** Verify dependencies, feature flags, imports, dataset/matrix construction, types, fit/predict methods, and error handling against official versioned `docs.rs`/`crates.io` docs. Provide complete `Cargo.toml` and Rust source blocks in Markdown. Never omit this track due to missing local Cargo; only if genuinely unsupported or docs are inaccessible, identify the exact unresolved requirement without inventing APIs.

## Verification Status

End with a brief static-review summary (operators, gradients/updates, objective scaling, shapes, APIs) and the exact status:

**`Source and static review only; not compiled or executed here.`**
