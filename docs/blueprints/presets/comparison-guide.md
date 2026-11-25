<!-- scaffold:preflight
Purpose: Contrast competing methods, algorithms, or architectures fairly under strictly equivalent workloads, criteria, and crossover edge cases.
Parent Master: M7 (../formats/synthesis-revision.md) | Route: comparison (variant: comparison_guide).
Activation Trigger: "compare X vs Y", "trade-offs between A and B", "when to use X vs Y".
Inputs: Resolved comparison candidates (existing notes or verified sources), shared evaluation workload, equivalent criteria.
Dependencies: router.md, core/authoring_rules.md, core/math_gates.md, procedures/authoring/representations.md.
Decision Rules: Lead with 'Choose X When...' verdict; explain causal differences before comparison tables; compare under matched workloads; prove a crossover edge case.
Failure Handling: Never fabricate quantitative benchmarks (mark unmeasured metrics '[UNVERIFIED]'); clarify ambiguous target notes before writing.
Validation: [verification-checklist.md](../../procedures/review/verification-checklist.md) (`M7` comparison guide).
-->

# Decision-First Architectural, Algorithm & Tool Comparison

- **Header Block:** Line-1 YAML Properties + `# <nn>. <Option A> vs. <Option B> — Decision & Trade-Off Analysis`.

## 1. Which option should I choose right now? (Choose X When... Verdict Block)

- `> [!tip] Executive Decision Rules ("Choose X When...")`:
  - **Choose `<Option A>` when:** Concrete workload, constraint, and performance profile.
  - **Choose `<Option B>` when:** Contrasting workload, scale, and operational profile.
  - **Choose neither / reconsider when:** Boundary regime where both options fail.
- `2–3` sentences defining the shared problem and core structural tension.

## 2. How do they compare side by side on equivalent workloads? (Multi-Axis Comparison Matrix)

Render table (escaping internal `|` pipes): `Decision Criterion | <Option A> | <Option B> | <Option C> | Governing Trade-Off / Winner`
Include rows for: **Core Mechanism & Invariant**, **Time Complexity / Cost**, **Memory / State Overhead**, **Best Use Case**, **Primary Failure Mode**, and **Implementation Ergonomics**.

## 3. How do their mechanisms diverge under the hood? (Causal Pipeline & Mathematical Contrast)

Contrast causal internals before tables (selecting concept-level math depth via `core/math_gates.md`) using a verified local web raster diagram ([representations.md](../../procedures/authoring/representations.md)) plus a `2–3` sentence summary (never Mermaid or ASCII).

## 4. What happens on the exact same workload and where does the winner flip? (Worked Benchmark & Crossover Edge Case)

- **Shared Workload Trace:** Trace one identical **Named Running Example** step by step through each candidate.
- **Verified Benchmarks:** Report numbers only from verified sources or reproducible runs (otherwise `[UNVERIFIED]`).
- **Crossover Edge Case:** Show one concrete threshold or input where the default winner reverses.

## 5. What did I learn & how does this connect to my stack? (Gotchas, Sources & Reflections)

- `> [!caution] Migration & Selection Traps`: `_Avoid_ -> True Invariant`.
- **Primary Sources & Benchmark Verification Table.**

<!-- optional: measurement -->
## [OPTIONAL] How can I reproduce this comparison? (Matched Evaluation)

<!-- Include only when controlled benchmark methodology goes beyond Section 4; delete cleanly otherwise. -->

- **Context / Analysis / Check:** Controlled variables, parity metrics, variance, and coverage limits.

<!-- optional: operations -->
## [OPTIONAL] How do I migrate safely and detect regressions? (Production Deployment & Observability Playbook)

<!-- Include only for live production migration risks; delete cleanly otherwise. -->

- **Context / Analysis / Check:** Migration constraints, canary/observability signals, and rollback trigger.

- **Contract Summary:** Apply [authoring_rules.md](../../../core/authoring_rules.md), [math_gates.md](../../../core/math_gates.md), and [footer_widgets.md](../../../core/footer_widgets.md).
