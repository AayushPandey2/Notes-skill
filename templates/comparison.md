<!-- scaffold:preflight
Decision-Matrix Pre-Flight: [note_decision_matrix.md](../shared/note_decision_matrix.md).
Switches: D01 route (`comparison`); D02 family comparison scope; D03 reader; D04 choose/design outcome; D05 vault notes / primary benchmarks;
D06–D09 `math_level`; D10 shared workload fixture & diverging causal pipeline; D11 visual (`flowchart TD` + matrix);
D12–D13 verification / benchmark reproducibility; D14 optional modules (`measurement`, `operations`); D15 final audit.
Strip this block before emission. Load detailed DM branches only when active.
-->

# Decision-First Architectural, Algorithm & Tool Comparison

- **Header Block**: YAML frontmatter + `# <nn>. <Option A> vs. <Option B> — Decision & Trade-Off Analysis`.

## 1. Which option should I choose right now? (Choose X When... Verdict Block)

- `> [!tip] Executive Decision Rules ("Choose X When...")`:
    - **Choose `<Option A>` when**: Concrete workload, scale, constraint, and latency/accuracy profile.
    - **Choose `<Option B>` when**: Contrasting workload, scale, constraint, and operational profile.
    - **Choose neither / look elsewhere when**: Boundary regime where both candidates fail.
- `2–3` sentences defining the shared problem space and the core architectural tension separating the candidates.

## 2. How do they compare side by side on equivalent workloads? (Multi-Axis Comparison Matrix)

- Render a comprehensive Markdown table comparing all candidates on equivalent workloads (escape all internal pipes `\|`):`Decision Criterion | <Option A> | <Option B> | <Option C (if applicable)> | Governing Trade-Off / Winner`
- Mandatory rows:
    1. **Core Mechanism & Invariant**
    2. **Time Complexity (with explicit assumptions)** _(or `N/A — Qualitative Operational Cost` for conceptual comparisons)_
    3. **Space / Memory / State Overhead**
    4. **Best Use Case (Sweet Spot)**
    5. **Primary Failure Mode & Worst-Case Input**
    6. **Implementation & Maintenance Ergonomics**

## 3. How do their mechanisms diverge under the hood? (Causal Pipeline & Mathematical Contrast)

- Contrast the internal dataflow or equations (`math_level` `0–2` via `shared/math_gates.md`). Include a side-by-side or unified **Mermaid diagram** (`flowchart TD`) illustrating where the two causal pipelines diverge, followed by a `2–3` sentence summary.

## 4. What happens on the exact same workload and where does the winner flip? (Worked Benchmark & Crossover Edge Case)

- **Shared Workload Trace**: Run the **exact same Named Running Example** through `<Option A>` and `<Option B>` step by step (or in a runnable comparison code snippet).
- **Verified Benchmarks**: Report quantitative benchmark numbers **only** when supported by a cited primary source or a reproducible local test run; otherwise mark `[UNVERIFIED]`.
- **The Crossover Edge Case**: Demonstrate one concrete edge-case input or scaling threshold where the normally inferior option decisively outperforms the default winner.

## 5. What did I learn & how does this connect to my stack? (Gotchas, Sources & Reflections)

- `> [!caution] Migration & Selection Traps`: consequential `_Avoid_ -> True Invariant` entries.
- **Primary Sources & Benchmark Verification Table**.

<!-- optional: measurement -->
## [OPTIONAL] How can I reproduce this comparison? (Matched Evaluation)

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: The architectural choice hinges on measured latency, throughput, memory, or accuracy rather than purely qualitative/asymptotic properties; D12–D14.
- When to Omit Cleanly: Omit for purely theoretical/conceptual comparisons or when no benchmark protocol exists. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: Hold task, dataset/workload, split, metric, and resource budget constant; record material environment, observed vs. cited results, and uncertainty; flag any unavoidable mismatch.
-->

- **Context:** State the workload, controlled variables, and hardware/runtime environment.
- **Analysis:** Compare observed or primary-cited metrics under matched budgets and explain any unavoidable protocol mismatch.
- **Check:** State variance, execution status, and what the benchmark does not establish.

<!-- optional: operations -->
## [OPTIONAL] How do I migrate safely and detect regressions? (Production Deployment & Observability Playbook)

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: Switching between `<Option A>` and `<Option B>` in a live system carries data, latency, or compatibility migration risk; D04, D12–D14.
- When to Omit Cleanly: Omit for greenfield algorithm comparisons or academic concept contrasts. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: Specify shadow/canary rollout criteria, key observability signals that catch regressions early, and the rollback trigger.
-->

- **Context:** State the migration boundary and live operational constraints.
- **Analysis:** Outline compatibility checks, dual-run/canary signals, and rollback criteria.
- **Check:** State the verification metric that confirms migration parity and its blind spots.

See [authoring rules](../shared/authoring_rules.md) for 5-key YAML, rendering, evidence, and cohesion.
See [math gates](../shared/math_gates.md) for selected mathematical depth.
See [footer contract](../shared/footer_widgets.md) for reflection behavior.
- **Template Contract (`comparison`):** Lead Section 1 with the actionable `Choose X when...` verdict, compare candidates under strictly equivalent workloads and assumptions, never fabricate benchmarks (`[UNVERIFIED]` when unmeasured), and prove the trade-off with a concrete crossover edge case.
