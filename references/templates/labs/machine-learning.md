# Machine Learning experimental lab reference

Use this 14-section heading hierarchy, order, named code-block roles, and visual roles for a classical ML investigation. This is an authoring reference, not text to copy into a finished lesson. The [shared lab contract](../../workflows/notes-creation/experimental-lab.md) controls evidence, collapsed walkthroughs, metadata, links, and execution honesty. Every visual must teach at its point of need via the six-phase narrative in [representations.md](../../workflows/notes-creation/representations.md); plan inspected local raster assets separately from Mermaid and tables. Never fill a result slot with fabricated output or hollow grouped placeholder ranges.

If an optional Rust track (`05` or `06`) is omitted because it is inapplicable or no verified crate is warranted, briefly explain that choice in the implementation-selection discussion and renumber subsequent sections consecutively.

# EXPERIMENTAL LAB [NUMBER]: [TOPIC NAME]

Open with **Subject**, **Level**, **Estimated prerequisites**, **Implementation languages**, **Libraries and tools**, **Practical objective**, **Experiment objective**, and **Learning outcomes**. Also state investigation question, expected deliverable, and constraints in the opening prose. Match the note's metadata profile.

## LAB SECTION 01 — INTRODUCTION AND OBJECTIVES
### 1.1 What Are We Building?
Describe the exact model or procedure, its output, and its use; show a small concrete prediction rather than a vague promise.
### 1.2 Why Are We Building It?
State the motivating problem and a simpler baseline's specific limit; avoid claiming the model is universally better.
### 1.3 What Will We Learn?
List conceptual, mathematical, programming, and experimental outcomes as abilities the learner can demonstrate.
### 1.4 Final System Preview
**Visual 1: Complete Experimental Lab Architecture.** Show data, framework fit, applicable Rust track(s), controlled experiments, and professional workflow in a native Mermaid flow; decode the arrows in prose.
### 1.5 Prerequisite Review
Bridge unfamiliar statistics, arrays, evaluation splits, and notation before they are used.

## LAB SECTION 02 — PROBLEM AND INPUT DESIGN
### 2.1 Problem Statement
Define the prediction task, target, and relevant decision in precise terms.
### 2.2 Input and Output Specification
Give feature and target types, dimensions, units, valid values, and new-input shape; do not confuse one row with a dataset.
### 2.3 Example Dataset or Test Case
Present a small labeled fixture traced across implementations, distinguishing illustrative data from measured data.
### 2.4 Assumptions and Constraints
State sample, model, resource, privacy, and evaluation assumptions relevant to the task.
### 2.5 Input Visualization
**Visual 2: Input Representation.** Use an inspected local raster figure for geometry or data appearance, a table for exact rows, or Mermaid for flow; decode axes and labels.
### 2.6 Success Criteria
Define correctness, baseline, metric, split, and acceptable failure conditions before fitting.

## LAB SECTION 03 — THEORETICAL AND MATHEMATICAL BRIDGE
### 3.1 Main Concept
Explain how inputs become predictions and how fitting changes parameters, first intuitively.
### 3.2 Principal Equations or Rules
State prediction and objective with assumptions; pair every displayed `$$...$$` formula with `> [!note]- 📐 Understand this formula`. Retain small illustrative snippets here only where they genuinely clarify a theoretical step.
### 3.3 Equation Pronunciation
Read summations, indices, hats, derivatives, and other unfamiliar symbols aloud.
### 3.4 Exhaustive Symbol Breakdown
Define every variable, constant, operator, index, and annotation; match symbols to the fixture.
### 3.5 Dimensions and Units
Track scalar, vector, matrix, and output shapes, plus physical units if present.
### 3.6 Step-by-Step Derivation
Show why the fitting rule follows and justify non-obvious transformations; do not disguise an assumption as algebra.
### 3.7 Worked Numerical Example
Calculate one prediction or update completely with the common fixture.
### 3.8 Equation-to-Code Mapping
Map mathematical components to variables, code statements, types, and shapes in a table, expanding non-trivial expressions step by step.
### 3.9 Mathematical Visualization
**Visual 3: Equation or Mechanism Visualization.** Use an inspected graph or suitable diagram to explain behavior, not as invented experiment output.

# IMPLEMENTATION TRACK A — STANDARD LIBRARY
Use the shared fixture and clear execution status (`Status: static review (not executed)` if unexecuted).
## LAB SECTION 04 — FRAMEWORK IMPLEMENTATION
### 4.1 Why Use This Library?
Explain suitability, what complexity it abstracts, and why this track is chosen (plus brief rationale if any optional Rust track is omitted).
### 4.2 Environment Setup
Show installation and imports with version caveats for unverified APIs.
### 4.3 Complete Source Code
**Code Block A1: Entire runnable library implementation.** Include all inputs, fitting, prediction, and output in one Markdown fence.
### 4.4 Output
Label expected or verified results and numerical tolerances.
### 4.5 Exhaustive Code Explanation
After the complete code, explain constructor parameters, methods, attributes, transformations, returned structures, and errors in logical groups using brief visible summaries + collapsed `> [!example]- Step-by-step: ...` walkthroughs.
### 4.6 What Happens Internally?
Explain actual data flow, transformations, and intermediate states of the fitting/optimization behavior without inventing internals or relying on an overview diagram alone.
### 4.7 Inspect Internal Parameters
Show how learned parameters or diagnostics relate to the mathematical bridge (`Section 03`).
### 4.8 Limitations and Debugging
Cover shape, configuration, convergence, and unsupported-input failures with concrete checks.

# IMPLEMENTATION TRACK B — RUST (OPTIONAL WHEN APPLICABLE)
Include `Section 05` when a Rust implementation teaches typed systems representation; include `Section 06` only when a verified crate genuinely supports the task. Omit `Section 06` (and explain briefly in `4.1` or `5.1`) rather than writing hollow placeholder ranges like `6.2–6.6`.
## LAB SECTION 05 — RUST FROM SCRATCH
### 5.1 Why Rust?
State what typed, systems-level implementation teaches for this algorithm.
### 5.2 Project Setup
Show Cargo commands (`cargo new ...`), folder structure, and `Cargo.toml` inside Markdown; explain what each command creates, where source lives, and how compilation differs from execution.
### 5.3 Complete Source Code
**Code Block B1: Rust from-scratch implementation.** Include complete educational code in Markdown if relevant and verifiable.
### 5.4 Compile and Run
Give `cargo build` / `cargo run` commands, distinguish debug and release builds, and state execution status once clearly.
### 5.5 Detailed Rust Syntax Explanation
Give brief visible summaries and collapsed `> [!example]- Step-by-step: ...` walkthroughs explaining bindings, mutability, types, slices (`&[f64]`), ownership, borrowing, bounds, loops, functions, collections, and error handling with small concrete inputs.
### 5.6 Mathematical-to-Rust Mapping
Map equations to Rust expressions step by step (collection contents, iterator, aggregation, type conversion, division/formula, small numerical trace, nonempty/precision limits).
### 5.7 Step-by-Step Execution Trace
Walk the shared fixture through the Rust representation.
### 5.8 Comparison With Python
Compare actual representations, types, and abstractions, not assumed speed.
### 5.9 Rust-Specific Mistakes
Explain relevant compiler, ownership, indexing, type, and precision errors.
## LAB SECTION 06 — RUST LIBRARY IMPLEMENTATION (OMIT IF NO CRATE IS WARRANTED)
### 6.1 Select the Library
Choose a documented, verified crate only when it supports the algorithm and adds educational value; otherwise omit Section 06 cleanly and renumber subsequent sections.
### 6.2 Dependencies
**Code Block B2: Cargo.toml.** Include verified dependencies and versions.
### 6.3 Complete Source Code
**Code Block B3: Full Rust library implementation.** Use verified APIs only.
### 6.4 Explanation
Explain imports, traits, structures, initialization, operations, output, and errors using brief visible summaries and collapsed walkthroughs.
### 6.5 Output Comparison
Compare with Python and Rust from-scratch tracks under matching inputs and tolerances.
### 6.6 Performance and Architectural Discussion
Explain complexity and resource behavior; report benchmarks only when actually run fairly.

# EXPERIMENTAL INVESTIGATION
Plan controlled comparisons; never invent observations.
## LAB SECTION 07 — CONTROLLED EXPERIMENTS
### 7.1 Experimental Questions
State relationships, hypotheses, variables, controls, and evidence needed.
### 7.2 Experiment 1: Parameter Sensitivity
Specify hypothesis, changed parameter, constants, runnable modification, observation table, explanation, and **Visual 4: Parameter Sensitivity Graph** (inspected plot or clearly labeled expected behavior).
### 7.3 Experiment 2: Alternative Methods
Compare valid implementations with equivalent tasks and settings.
### 7.4 Experiment 3: Input or Transformation Effects
Change one justified preprocessing or feature condition while preserving evaluation boundaries.
### 7.5 Experiment 4: Robustness and Failure Cases
Test invalid, extreme, missing, or noisy inputs relevant to the model.
### 7.6 Experiment 5: Performance
Benchmark only when meaningful and actually run; define hardware, builds, inputs, repetitions, and accuracy parity.
### 7.7 Consolidated Experimental Findings
Use a comparison table, explain observed or expected patterns, and state limits.

# PROFESSIONAL IMPLEMENTATION TRACK
Teach all 18 stages individually (with Purpose, Inputs/assumptions, Code or setup, Brief visible explanation, Collapsed walkthrough, Output structure/interpretation, Math correspondence, Common mistakes, Visual support, and Connection to next stage as applicable) before assembling the integrated program in Step 17.
## LAB SECTION 08 — REALISTIC END-TO-END WORKFLOW
### Step 01: Define the Task
State task type, target, stakeholders, loss or metric, baseline, output, and next step.
### Step 02: Import Libraries and Prepare Environment
List required packages, versions if verified, imports, reproducibility settings, and common setup failures.
### Step 03: Load or Create Data
Define source, schema, shape, target, provenance, and whether data are illustrative.
### Step 04: Create Evaluation Partitions
Explain train/validation/test or cross-validation boundaries, grouping/time constraints, and leakage precautions before exploration.
### Step 05: Explore the Data or System
Inspect training data distributions, relationships, missingness, and outliers; use verified figures with conclusions justifying preprocessing.
### Step 06: Identify Data Quality Problems
Record concrete defects, affected columns, and justified remedies rather than generic cleaning.
### Step 07: Define Transformations
Explain inputs, outputs, mathematics, fitting boundary, alternatives, and limitations for each needed transform.
### Step 08: Construct Reusable Transformers
Show only transformations the task needs, `fit()`/`transform()`/`fit_transform()` boundaries, types/shapes, validation, and train-only fitted state.
### Step 09: Build the Pipeline
Explain execution order and leakage prevention. **Visual 5: Complete Professional Pipeline.** Decode data flow and fitted state.
### Step 10: Configure the Model or Main Algorithm
Define parameters, defaults used, assumptions, and why this model fits the task.
### Step 11: Configure Optimization and Regularization
Explain only relevant settings and expected effects; keep an explicit reason if the estimator has none.
### Step 12: Train and Tune
Show fitting and validation procedure, search space where warranted, selection criterion, and output status; never tune on final test data.
### Step 13: Evaluate
Define metric equations and baseline, report held-out results only if observed. **Visual 6: Evaluation and Diagnostics.** Interpret actual diagnostics or name the unmet need.
### Step 14: Interpret Internal Results
Relate learned parameters or feature effects to assumptions and limits; avoid causal claims from prediction alone.
### Step 15: Process New Inputs
Trace a new row through fitted transformations to prediction, showing shape, preprocessing consistency, and output meaning.
### Step 16: Handle Failures
Give symptom, cause, diagnosis, correction, and prevention for relevant schema, leakage, training, and inference failures.
### Step 17: Assemble the Complete Program
**Code Block C1: Full end-to-end executable implementation.** Include imports, data preparation, split, pipeline, fitting, evaluation, and new-input inference in Markdown; do not create a source file for this task.
### Step 18: Explain the Complete Integration
Trace one example through the entire workflow and explain component boundaries.

# FINAL VALIDATION AND LEARNING
## LAB SECTION 09 — TESTING AND VERIFICATION
### 9.1 Correctness Tests
For every check, state property checked, concrete inputs, independently expected results, comparison/tolerance, what it establishes, what it does not establish, and execution status.
### 9.2 Output Validation
Judge against the stated metric and baseline, with evidence status.
### 9.3 Reproducibility
Record seeds, dependencies, configuration, and commands without implying execution.
### 9.4 Limitations
Bound conclusions by data, sample size, model assumptions, and unverified steps.
## LAB SECTION 10 — COMMON MISTAKES AND DEBUGGING
### 10.1 Programming Errors
Diagnose realistic syntax, type, indexing, shape, and API errors.
### 10.2 Mathematical Errors
Diagnose sign, objective, denominator, or numerical mistakes against a small fixture.
### 10.3 Experimental Errors
Identify leakage, uncontrolled changes, unfair metrics, and inadequate partitions.
### 10.4 Diagnostic Walkthrough
Walk one symptom through checks, cause, correction, and recheck.
## LAB SECTION 11 — IMPLEMENTATION COMPARISON
Compare Python framework, Rust tracks (if included), and integrated pipeline on the same problem: mathematical visibility, validated output, abstraction, errors, resource cost, and use case (**Visual 7: Implementation Comparison** if helpful). Use a table and explain actual differences; do not rely on language stereotypes.
## LAB SECTION 12 — PRACTICAL CHALLENGES
### Beginner Challenge
Change one input or parameter and predict the effect.
### Intermediate Challenge
Add a justified feature, transformation, metric, or check.
### Advanced Challenge
Transfer to a dataset with different constraints and defend the evaluation plan.
### Debugging Challenge
Diagnose a planted, meaningful implementation or leakage error.
### Reflection Questions
Ask why the observed or expected behavior follows from the mechanism.
## LAB SECTION 13 — FINAL LEARNING CHECKPOINT
Test conceptual mechanism, formulas, syntax, design choices, debugging, evidence interpretation, and practical transfer. Give answer guidance and remediation; do not mistake memorized API names for understanding.
## LAB SECTION 14 — FINAL SUMMARY
### What Was Built?
Summarize the model and deliverable.
### What Was Learned Mathematically?
State the governing relationship and assumptions.
### What Was Learned Programmatically?
State the central operations and representations.
### What Was Learned Experimentally?
Summarize only actual or clearly expected findings.
### What Was Learned Professionally?
Recap data boundaries, pipeline, evaluation, and inference.
### Which Method Should Be Used When?
Give a task-specific decision rule.
### What Comes Next?
Link to a logical follow-up question.
