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

- `> [!caution] Migration & Selection Traps`: 3+3+3+ `_Avoid_ -> True Invariant` entries.
- **Primary Sources & Benchmark Verification Table**.
- Append `shared/footer_widgets.md` (**What I learned**, **Open Confusion** `**Confusion** :: ...`, **Atomize**, **Connection**, and the `dataviewjs` **Mark Revisited** button).

Follow [shared authoring rules](../shared/authoring_rules.md) and the [footer contract](../shared/footer_widgets.md). Apply the math gate only at the planned level. Scaffold comments are editing slots and must be removed before publication.

> [!important] AGENT AUTHORING DIRECTIVE — `comparison` Always place the actionable `Choose X when...` verdict block at the very top of Section 1 and compare all options under strictly equivalent assumptions and workloads. Never invent unverified benchmark numbers, never hand-wave complexity assumptions, and always prove the trade-off by demonstrating a concrete crossover edge case that flips the decision.
