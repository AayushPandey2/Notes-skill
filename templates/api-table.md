# Workflow-Organized API Reference, Execution Model & Cookbook

- **Header Block**: YAML frontmatter + `# <nn>. <Subtopic Title>`. At positive math levels, use the Key Equations callout for governing shapes and costs (for example, Conv2d output dimensions).

## 1. What am I trying to understand & how does this API behave under the hood? (Execution, Memory & State Model)

- **Core Execution & Memory Mental Model**: `3–4` sentences explaining the foundational mechanics governing the API (e.g., NumPy `ndarray` strides, axes, and zero-copy views vs. allocations; PyTorch tensor layout `(B, C, H, W)`, device placement, and autograd tracking; or container iterator invalidation rules).
- **Governing Preconditions & Invariants**: Explicitly state version assumptions, default `dtype`/precision rules, indexing conventions, and thread/mutation safety guarantees.
- **Named Running Example Setup**: Define the single shared input object (with concrete dimensions and values) used across all quick examples and cookbook recipes below.

## 2. How do I look up the exact signatures and parameters by workflow? (Categorized API Reference Tables)

- Organize entries into logical workflow subsections (e.g., `### 2.1 Creation & Initialization`, `### 2.2 Shape, Axes & View Manipulation`, `### 2.3 Aggregation, Reduction & Filtering`, `### 2.4 Linear Algebra / Core Parameter Reference`).
- In each workflow group, render a dense Markdown table (escaping all internal pipes `\|`):`Function / Parameter Signature | What It Does & Mechanism | Key Parameters, Types & Defaults | Return Value & Mutation / Copy vs. View | Time & Allocation Complexity | Quick Runnable One-Liner`
- _If `math_level >= 1`_: Include a **Symbol & Parameter Anatomy Table** (`Parameter / Symbol | Mathematical Role | Shape / Constraint | Directional Effect on Output`) and a 4-row **Input-to-Output Shape/Value Table** using the Named Running Example.

## 3. How do I combine these calls to solve real problems? (Runnable Cookbook Recipes & Edge-Case Verification)

- Provide a **Shared Setup Block** outside the recipes so code is clean and DRY.
- Author `3–5` complete, runnable **Cookbook Recipes** that chain multiple API calls to solve realistic engineering patterns.
- For every recipe, show the idiomatic code, exact expected output on the Named Running Example, and an explicit edge-case guard (e.g., handling zero-row L2 normalization without `NaN`, empty tensor slices, zero-size batches, or broadcasting misalignment).

## 4. Where do performance traps and silent bugs hide? (Limitations, Gotchas & Vault Connections)

- `> [!caution] Performance Traps, Hidden Allocations & Silent Mutation Bugs`: 3+3+3+ `_Avoid_ -> True Invariant` entries exposing real production pitfalls (e.g., accidental copy inside a tight loop, mutating a sliced view and corrupting upstream data, implicit `float64` promotion) with a refuting snippet and diagnostic check (`np.shares_memory`, `.is_contiguous()`, etc.).
- **Primary Sources & Official Versioned Docs Table** (`Library & Version | Direct Official Doc URL | Vault Link | Exact Signature / Behavior Verified`).
- Append `shared/footer_widgets.md` (**What I learned**, **Open Confusion** `**Confusion** :: ...`, **Atomize**, **Connection**, and the `dataviewjs` **Mark Revisited** button).

Follow [shared authoring rules](../shared/authoring_rules.md) and the [footer contract](../shared/footer_widgets.md). Apply the math gate only at the planned level. Scaffold comments are editing slots and must be removed before publication.

> [!important] AGENT AUTHORING DIRECTIVE — `api-table` Retain the exact workflow-grouped table schema, escaped pipes (`\|`), shared setup contract, and reflection footer. Never dump an unorganized alphabetical list of functions or omit copy-vs-view / allocation semantics. Every signature, default parameter value, and return behavior must reflect verified official documentation for the stated library version, and every cookbook recipe must handle boundary edge cases cleanly. Execute the mandatory **Humanization & Cohesion Pass** so execution mental models and recipes read with a direct, practical engineer-to-future-self voice, natural narrative flow, and zero robotic AI clichés.
