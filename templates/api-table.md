<!-- scaffold:preflight
Decision-Matrix Pre-Flight: [routing index](../shared/note_decision_matrix.md) and [shared decision guide](../shared/notes_decision_matrix.md).
Switches: D01 route (`api-table`); D02 scope; D03 reader; D04 track/outcome; D05 official versioned docs;
D06–D09 `math_level`/shapes; D10 shared running fixture & execution topology; D11 visual modality;
D12–D13 verification stack & recipe guards; D14 optional modules (`memory`, `operations`); D15 final audit.
Strip this block before emission. Load detailed DM branches only when active.
-->

# Workflow-Organized API Reference, Execution Model & Cookbook

- **Header Block**: YAML frontmatter + `# <nn>. <Subtopic Title>`. At positive math levels, use the Key Equations callout for governing shapes and costs (for example, Conv2d output dimensions).

## 1. What am I trying to understand & how does this API behave under the hood? (Execution, Memory & State Model)

<!-- Gate: DM-03, DM-04, DM-15.
KEEP the state or execution model when it changes how a call is used. Show the governing behavior and its conditions. Remove this gate before publication. -->

- **Core Execution & Memory Mental Model**: `3–4` sentences explaining the foundational mechanics governing the API (e.g., NumPy `ndarray` strides, axes, and zero-copy views vs. allocations; PyTorch tensor layout `(B, C, H, W)`, device placement, and autograd tracking; or container iterator invalidation rules).
- **Governing Preconditions & Invariants**: Explicitly state version assumptions, default `dtype`/precision rules, indexing conventions, and thread/mutation safety guarantees.
- **Named Running Example Setup**: Define the single shared input object (with concrete dimensions and values) used across all quick examples and cookbook recipes below.

## 2. How do I look up the exact signatures and parameters by workflow? (Categorized API Reference Tables)

<!-- Gate: DM-05, DM-15, DM-19.
KEEP versioned signatures that support the named workflows. MERGE repeated parameters and check each row against official documentation. Remove this gate before publication. -->

- Organize entries into logical workflow subsections (e.g., `### 2.1 Creation & Initialization`, `### 2.2 Shape, Axes & View Manipulation`, `### 2.3 Aggregation, Reduction & Filtering`, `### 2.4 Linear Algebra / Core Parameter Reference`).
- In each workflow group, render a dense Markdown table (escaping all internal pipes `\|`):`Function / Parameter Signature | What It Does & Mechanism | Key Parameters, Types & Defaults | Return Value & Mutation / Copy vs. View | Time & Allocation Complexity | Quick Runnable One-Liner`
- _If `math_level >= 1`_: Include a **Symbol & Parameter Anatomy Table** (`Parameter / Symbol | Mathematical Role | Shape / Constraint | Directional Effect on Output`) and a 4-row **Input-to-Output Shape/Value Table** using the Named Running Example.

## 3. How do I combine these calls to solve real problems? (Runnable Cookbook Recipes & Edge-Case Verification)

<!-- Gate: DM-11, DM-14, DM-17, DM-18.
ADAPT to one recipe per distinct workflow. Show inputs, expected behavior, and actual verification status. Remove this gate before publication. -->

- Provide a **Shared Setup Block** outside the recipes so code is clean and DRY.
- Author `3–5` complete, runnable **Cookbook Recipes** that chain multiple API calls to solve realistic engineering patterns.
- For every recipe, show the idiomatic code, exact expected output on the Named Running Example, and an explicit edge-case guard (e.g., handling zero-row L2 normalization without `NaN`, empty tensor slices, zero-size batches, or broadcasting misalignment).

## 4. Where do performance traps and silent bugs hide? (Limitations, Gotchas & Vault Connections)

<!-- Gate: DM-05, DM-19, DM-20.
KEEP concrete failure triggers and relevant links. State how a reader can recognize the failure. Remove this gate before publication. -->

- `> [!caution] Performance Traps, Hidden Allocations & Silent Mutation Bugs`: consequential `_Avoid_ -> True Invariant` entries exposing real production pitfalls (e.g., accidental copy inside a tight loop, mutating a sliced view and corrupting upstream data, implicit `float64` promotion) with a refuting snippet and diagnostic check (`np.shares_memory`, `.is_contiguous()`, etc.).
- **Primary Sources & Official Versioned Docs Table** (`Library & Version | Direct Official Doc URL | Vault Link | Exact Signature / Behavior Verified`).

<!-- optional: memory -->
## [OPTIONAL] How do layout and allocation change performance? (Hardware, Memory Layout & Systems Performance Profile)

<!-- Gate: DM-06, DM-13, DM-19.
Include when layout or allocation changes the choice. OMIT if the execution model already explains the consequence. Remove this gate before publication. -->

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: The API involves material view/copy semantics, memory strides, alignment, ownership transfer, or host/device transfers; D04, D10–D14.
- When to Omit Cleanly: Omit if memory layout does not affect usage or is already covered in Section 1. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: Trace one concrete allocation or zero-copy view on the running example, state lifetime/aliasing constraints, compare layout choices, and specify a diagnostic check (`np.shares_memory`, `.is_contiguous()`, profiler) without inventing timings.
-->

- **Context:** State the specific trigger, library version, and memory/hardware assumptions activating this section.
- **Analysis:** Trace one concrete allocation or zero-copy view, name lifetime/aliasing constraints, and compare relevant layout choices.
- **Check:** State the diagnostic check and evidence limit (observed vs. unmeasured performance).

<!-- optional: operations -->
## [OPTIONAL] How do I debug, profile, and operate this API in production? (Production Deployment, Debugging & Observability Playbook)

<!-- Gate: DM-14, DM-18, DM-19.
Include only a real operational failure with a reproducible symptom, diagnostic, and check. Remove this gate before publication. -->

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: Applied systems or ML engineering workflows where runtime diagnostics, concurrency limits, version drift, or failure recovery matter; D04, D12–D14.
- When to Omit Cleanly: Omit for pure syntax lookup or single-script exercises. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: Define the operational contract, primary failure signals, minimal isolating check, and safe remediation/rollback without guessing metrics.
-->

- **Context:** State the production workload, runtime/version constraints, and failure surface activating this section.
- **Analysis:** Map observable failure signals to root causes, isolating diagnostics, and concrete remediation steps.
- **Check:** State what the diagnostic verifies and which production conditions remain untested.

See [authoring rules](../shared/authoring_rules.md) for 5-key YAML, rendering, evidence, and cohesion.
See [math gates](../shared/math_gates.md) for selected mathematical depth.
See [footer contract](../shared/footer_widgets.md) for reflection behavior.
- **Template Contract (`api-table`):** Group calls by workflow (never alphabetical dumps), escape table pipes (`\|`), specify copy-vs-view and allocation semantics against verified official versioned docs, and guard boundary cases in every recipe.
