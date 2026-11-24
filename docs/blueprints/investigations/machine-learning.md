# Machine Learning experimental lab reference

Use this compact 7-section hierarchy for classical ML investigations. This overrides earlier multi-track 14/15-section layouts and is an authoring reference, not text to copy verbatim. The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs opening prose, dataset/unit consistency, collapsed walkthroughs, technical accuracy, and execution honesty.

Keep the title, YAML frontmatter, and parent-note navigation link. **Do not** include a visible opening inventory (`Level`, `Estimated prerequisites`, `Implementation languages`, `Libraries and tools`, `Practical objective`, `Experiment objective`).

# EXPERIMENTAL LAB [NUMBER]: [TOPIC NAME]

> [!abstract] Parent Note
> Core theory lives in [[<Parent Note>]].

Open with a short, connected introduction explaining what the learner will investigate, why it matters, and a native Mermaid architecture flow showing how data splitting, modeling, experiments, and end-to-end verification connect.

## LAB SECTION 01 — INTRODUCTION
Explain the concrete problem, why training error alone is misleading, what the learner will build and investigate, and any essential prerequisite reminders needed before Section 02.

## LAB SECTION 02 — PROBLEM AND INPUT DESIGN
Organize into three coherent subsections:
### 2.1 What problem will we investigate?
Start in ordinary language: explain the concrete situation, what is known, what must be predicted or compared, why training performance alone is insufficient, and what the learner will investigate before introducing formal names.
### 2.2 What does one example look like?
Choose one consistent primary dataset (keep synthetic vs. real-unit rules strictly aligned throughout the entire lab). Explain what each row and column represents, the target, units, shapes (`p` features vs `k` polynomial degree), and one concrete input/output pair. Introduce a small table in prose, distinguish observed labels from model predictions, and explain *why* a single new sample needs a 2D feature matrix.
### 2.3 How will we judge the result fairly?
Explain train, validation, and test responsibilities, assumptions, baseline, metric, what evidence supports improvement, and what the experiment cannot guarantee (never promise a specific degree always wins). Embed and decode a local raster visual here via [representations.md](../../procedures/authoring/representations.md) rather than only pointing to the parent chapter.

## LAB SECTION 03 — THEORETICAL AND MATHEMATICAL BRIDGE
Organize into three connected subsections without repeating the same worked calculation or scattering pronunciation/symbol/dimension headings:
### 3.1 From a prediction mistake to an average training error
Walk step by step from one prediction → difference from truth → squaring → averaging → empirical risk minimization. Introduce one canonical `$$...$$` formula with an immediately following `> [!note]- 📐 Understand this formula` fold containing pronunciation, symbols, dimensions, assumptions, and interpretation.
### 3.2 Follow one example from predictions to MSE
Establish one canonical worked calculation showing true values, predictions, residuals, squares, sum, average, and accurate unit interpretation. Connect later sections back to this example.
### 3.3 Translate the reasoning into computation
Explain how predictions, subtraction, squaring, and averaging map to vectorized code, array shapes, and accidental broadcasting risks (use a compact mapping table only if helpful). Do not inject unbridged advanced formalism (such as empirical distributions or Dirac deltas) into a beginner bridge.

## LAB SECTION 04 — FOUR IMPLEMENTATIONS OF THE SAME LEARNING TASK
Implement the **same underlying learning task** across all four tracks using comparable inputs, outputs, objective, intercept convention, and evaluation rules (never compare a hand-written mean with a polynomial regression model as if they solve the same task). Choose the smallest common task teachable cleanly across all four tracks and explain differences from Section 06's experiment.

Beneath each track heading (`4.1`–`4.4`), include: what this version reveals, dependencies/setup, complete educational code in a Markdown fence, an immediately following collapsed `> [!example]- Understand this implementation line by line` walkthrough (covering meaningful lines/groups in execution order: purpose, syntax, types/structures, inputs, internal operation, shapes, math link, output/state, mistakes, next step), and brief interpretation/comparison.

### 4.1 Python and NumPy (from scratch)
Explain array shapes, axis choices, vectorization, and broadcasting inside the collapsed walkthrough.
### 4.2 Scikit-learn (standard library)
Explain estimator state, `.fit()`, transformation, `.predict()`, and pipeline behavior inside the collapsed walkthrough.
### 4.3 Rust (standard library only)
Explain ownership, borrowing, references, slices, iterators, explicit `as f64` conversions, and `Result` error handling inside the collapsed walkthrough.
### 4.4 Rust (using suitable verified libraries)
For educational code inside Markdown, **do not** inspect the local environment, install dependencies, create project files, compile, or execute—missing local Cargo, dependencies, or compiler access is never a reason to omit this track. Use official, version-specific crate documentation (`docs.rs` / `crates.io`) and examples to establish compatible dependency declarations, imports, dataset construction, types, fitting, prediction, and error handling without inventing APIs or mixing incompatible versions. Provide complete `Cargo.toml` and Rust source blocks followed by a detailed collapsed line-by-line explanation, label it once **"Documentation-checked example; not compiled or executed here."**, and describe expected behavior without fabricating execution results. Report a limitation only if the crate documentation itself is inaccessible.

## LAB SECTION 05 — CONTROLLED EXPERIMENTS
Design a small number of substantive investigations (e.g., polynomial complexity, baseline vs learned model, sample size with fair evaluation design, and out-of-domain extrapolation on separate diagnostic inputs without mutating the held-out test set). For each experiment, cover in connected prose: question, why it matters, hypothesis/reasoning, changed variable, controls, exact procedure, relevant code in Markdown, collapsed code/procedure walkthrough, what to record, how to interpret different possible outcomes, and limitations.

Never promise that Degree 4 always wins, Degree 15 always hits zero train error, more samples always shrink the gap, or one run must be U-shaped; distinguish theoretical nested-class properties from finite-precision solver behavior. Label unexecuted designs honestly; never title anticipated patterns "experimental findings."

## LAB SECTION 06 — REALISTIC END-TO-END WORKFLOW
Teach each applicable stage sequentially (environment/imports, data acquisition/generation, evaluation partitions, training-data exploration, input validation, transformations, reusable transformers, pipeline construction, model configuration, validation-based selection, final held-out evaluation, internal-result interpretation, new-input inference, failure handling, and integrated complete program).

For **every** step:
1. Explain the purpose in connected prose.
2. Show the relevant code directly below (merge purely conceptual steps into the next executable step rather than writing comment-only blocks).
3. Add a collapsed `> [!example]- Step-by-step: ...` explanation directly below the code.
4. Explain the output or decision.
5. Connect to the next step.

Keep variables consistent with the final integrated program, which must also carry a collapsed walkthrough tracing overall execution and integration boundaries. Ensure candidate and baseline are compared on the **same** partition, pipeline leakage boundaries are stated accurately, feature-count validation is explicit (not `np.atleast_2d`), and standardized polynomial coefficients are not misrepresented as importance rankings.

## LAB SECTION 07 — VERIFICATION, DEBUGGING, COMPARISON, AND INDEPENDENT PRACTICE
Keep distinct final subheadings where helpful for navigation:
### 7.1 Verification and Honest Status
State property checked, concrete inputs, independently expected results, tolerance, what each check establishes/does not establish, and `Status: static review (not executed)` if unexecuted. Qualify small-test-set uncertainty honestly.
### 7.2 Common Mistakes and Debugging
Cover programming, mathematical, and experimental errors (e.g., fitting scalers before splitting, MSE vs RMSE unit confusion, tuning on test data, treating a train–val gap as proof of noise memorization) with concrete fixes.
### 7.3 Implementation Comparison
Compare the four tracks from Section 04 and the integrated pipeline on mathematical visibility, abstraction, error surface, and best use.
### 7.4 Challenges, Checkpoint, and Summary
Provide progressive challenges (beginner, intermediate, advanced, debugging), a reasoning checkpoint with collapsed `> [!tip]- Answer` guidance, and a concise summary linking back to the parent note and next topic.
