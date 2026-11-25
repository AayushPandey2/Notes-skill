<!-- scaffold:preflight
Purpose: Organize API, framework, or library syntax strictly by engineering workflow rather than alphabetical dumps, capturing state/memory semantics and verified cookbook recipes.
Parent Master: M3 (../formats/quick-reference.md) | Route: api-table (variant: syntax_reference).
Activation Trigger: "syntax reference", "api table", or library workflow reference via /scribe-notes.
Inputs: Official versioned documentation, shared concrete running fixture, edge-case guards, and runtime verification status.
Dependencies: router.md, core/authoring_rules.md, core/math_gates.md.
Decision Rules: Group signatures by task workflow; state copy-vs-view, mutation, and layout semantics before lookup tables; reuse one shared running fixture across all recipes.
Failure Handling: Never fabricate unverified signatures or performance timings; handle empty/zero/boundary inputs explicitly in recipes.
Validation: [verification-checklist.md](../../procedures/review/verification-checklist.md).
-->

# Workflow-Organized API Reference, Execution Model & Cookbook

- **Header Block:** Line-1 YAML Properties + `# <nn>. <Subtopic Title>`. At positive math depth, emit `> [!abstract] Key Equations` for governing dimensions/complexity.

## 1. What am I trying to understand & how does this API behave under the hood? (Execution, Memory & State Model)

- **Core Execution & Memory Model (`3–4` sentences):** Explain foundational mechanics governing calls (memory layout, view-vs-copy aliasing, ownership/mutation rules, default precision/type behavior).
- **Preconditions & Shared Fixture:** State checked library versions, invariants, and one concrete non-square/asymmetric **Named Running Example** reused throughout Sections 2–4.

## 2. How do I look up the exact signatures and parameters by workflow? (Categorized API Reference Tables)

Organize subsections by workflow (`### 2.1 Initialization`, `### 2.2 Transformation & Layout`, `### 2.3 Reduction & Query`, `### 2.4 Core Operators`), escaping internal `|`:
`Function / Signature | Mechanism | Key Parameters & Defaults | Return Value & Mutation / Copy vs. View | Time & Allocation Complexity | Minimal One-Liner`
When the concept's math profile in `core/math_gates.md` includes equations, include Symbol Anatomy and a concise Input-to-Output table on the Named Running Example.

## 3. How do I combine these calls to solve real problems? (Runnable Cookbook Recipes & Edge-Case Verification)

- Provide one **Shared Setup Block** followed by `3–5` complete recipes showing idiomatic calls, verified outputs on the Named Running Example, and explicit edge-case guards (empty inputs, zero divisors, unaligned shapes, aliasing hazards).

## 4. Where do performance traps and silent bugs hide? (Limitations, Gotchas & Vault Connections)

- `> [!caution] Performance Traps, Hidden Allocations & Silent Mutation Bugs`: concrete `_Avoid_ -> True Invariant` failure patterns, isolating diagnostic helper, and refuting example.
- **Primary Sources & Official Docs Table:** `Library & Version | Official URL | Vault Link | Verified Behavior`.

<!-- optional: memory -->
## [OPTIONAL] How do layout and allocation change performance? (Hardware, Memory Layout & Systems Performance Profile)

<!-- Activate only when stride, memory layout, or device ownership materially changes usage; delete cleanly otherwise. -->

- **Context / Analysis / Check:** Concrete view/allocation trace, aliasing constraints, diagnostic check, and unmeasured vs observed bounds.

<!-- optional: operations -->
## [OPTIONAL] How do I debug, profile, and operate this API in production? (Production Deployment, Debugging & Observability Playbook)

<!-- Activate only for live runtime/concurrency/version-drift workflows; delete cleanly otherwise. -->

- **Context / Analysis / Check:** Production failure surface, isolating check, remediation/rollback rule, and coverage limits.

- **Contract Summary:** Verify workflow grouping, escaped table pipes, verified official signatures, shared fixture parity, and [authoring_rules.md](../../../core/authoring_rules.md) / [math_gates.md](../../../core/math_gates.md) / [footer_widgets.md](../../../core/footer_widgets.md).
