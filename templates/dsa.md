<!-- scaffold:preflight
Pre-Flight: [router](../router.md) and [authoring rules](../shared/authoring_rules.md).
Route: `dsa` (locked language, brute-force + optimal + tricky dry-run table + edge-case suite, optional `complexity` and `visual` modules).
Strip this block before emission.
-->

# Algorithmic Problem Solving, Bottleneck Analysis & Production Implementation

Supports `/scribe-dsa cpp <problem>` and `/scribe-dsa python <problem>` (and any additional supported language), locking code generation to the requested language.
- **Header Block**: Metadata per shared contract + `# DSA: <Problem Title>` + `> [!abstract] Complexity Target & Core Invariant`.

## 1. What is the exact problem, what are the constraints & what complexity target do they force? (Problem Specification & Envelope)

<!-- Authoring note: KEEP the problem contract and actual constraints. State the resulting performance target. Remove this gate before publication. -->

- **Problem Statement & I/O Contract**: Formal statement, input/output types, and concrete small example.
- **Verified Constraints & Missing-Constraint Audit**: List all stated input bounds ($N$, value ranges, graph density, memory/time limits). Explicitly tag any missing constraint or assumption as `[ASSUMED / UNVERIFIED]`.
- **Inferred Asymptotic Target Envelope**: Deduce the plausible required time and auxiliary space complexity class from the verified size and time limits (e.g., $N \le 2 \cdot 10^5$ suggests $O(N \log N)$ or $O(N)$ target) without promising exact wall-clock runtime from $N$ alone.
- **Algorithmic Pattern & Unbreakable Invariant**: Name the core pattern (e.g., Monotonic Queue, Offline Fenwick Tree, Binary Search on Answer) and state the governing loop/recursion invariant in `2–3` sentences.

## 2. What is the brute-force baseline and why does it bottleneck? (Naive Approach & The Optimization Bridge)

<!-- Authoring note: Show the smallest baseline that exposes the bottleneck. Remove this gate before publication. -->

- **Brute-Force Intuition & Runnable Code**: Explain the direct exhaustive approach and provide clean, runnable baseline code in the selected language.
- **Exact Bottleneck Quantification**: Derive the brute-force Time and Space Complexity and quantify operation counts at maximum $N$ to explain why it exceeds time/memory limits.
- **The Optimization Bridge**: Pinpoint the exact redundant computation (e.g., re-scanning elements, recomputing prefix states) and explain the structural insight that eliminates it. _(Guardrail: If the brute-force solution is already asymptotically optimal, prove why it matches the lower bound and do not invent a fake optimization)._

## 3. How does the optimal algorithm work step by step? (Mechanism, Correctness Justification & Dry-Run Table)

<!-- Authoring note: Trace a discriminating input and justify the algorithm's invariant or pivot choice. Remove this gate before publication. -->

- **Step-by-Step Optimal Mechanism & Correctness Proof**: Walk through the state transitions, prove why the invariant holds at initialization, maintenance, and termination (`math_level` `1` or `2`), and derive exact Time and Space Complexity (explicitly stating whether auxiliary space excludes the required output container).
- **Complete Step-by-Step Dry-Run Table**: Choose a **tricky, non-trivial input** (one that triggers pointer adjustments, stack pops, or tie-breaking) and trace every loop iteration, index, auxiliary data structure state, and return update in a Markdown table (escaping all pipes `\|`).

## 4. How do I implement and stress-test the optimal solution? (Implementation & Edge-Case Suite)

<!-- Authoring note: KEEP a complete example in the selected language with credible edge-case results. Remove this gate before publication. -->

- **Complete Optimal Implementation (`C++20` or `Python 3`)**:
    - Fully runnable, self-contained code with imports/includes and a test driver.
    - For `C++`, explicitly audit integer widths (`int64_t` / `long long` vs. `int32_t`) against worst-case accumulation overflow, fast I/O concerns, and iterator validity.
    - Record compiler/runtime version and execution status (`executed` vs. `not executed`).
- **Verified Edge-Case Test Matrix (`4–5` Tricky Cases)**:
    - Markdown table and runnable assertions covering: (1) Minimum/empty boundary input, (2) All-equal / duplicate elements, (3) Strictly monotonic / adversarial order, (4) Maximum value / integer-overflow boundary, and (5) The tricky dry-run input, showing Expected vs. Observed outputs.

## 5. How does this pattern transfer to harder variations? (Related Problems, Twists & Reflections)

<!-- Authoring note: KEEP variations that change the selection rule or invariant. Remove this gate before publication. -->

- **Related Problems (`2–3` Curated Follow-Ups)**: For each related problem, present its full problem prompt visibly, then place its structural twist and optimal solution adaptation inside an independently collapsed callout:`> [!example]- Reveal Structural Twist & Optimal Solution for <Related Problem Title>`

<!-- optional: complexity -->
## [OPTIONAL] Why does the resource bound hold? (Formal Complexity & Lower-Bound Derivation)

<!-- Authoring note: Include only formal resource reasoning allowed by the math contract. Explain a qualitative bound in prose when sufficient. Remove this gate before publication. -->

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: A non-obvious recurrence, amortized charging/potential argument, or information-theoretic lower bound is essential to proving optimality.
- When to Omit Cleanly: Omit when complexity follows trivially from a single loop or is already derived in Section 3. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: State the cost model and input variables; derive the recurrence, potential function, or lower bound step by step; distinguish worst-case from amortized bounds and show a discriminating worst-case input.
-->

- **Context:** State the cost model, input-size variables, and why naive counting is insufficient.
- **Analysis:** Justify the recurrence, amortized charging/potential argument, or lower bound and separate worst-case from amortized cost.
- **Check:** Supply a concrete adversarial/discriminating input confirming the tight bound.

<!-- optional: visual -->
## [OPTIONAL] How do pointers, windows, or structures evolve step by step? (Visual Diagram / ASCII State-Transition Walkthrough)

<!-- Authoring note: Include a diagram only when a state transition is hard to follow in the trace. Remove this gate before publication. -->

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: Multi-pointer motion, monotonic stack/deque eviction, tree/DP-table transitions, or bit/memory layouts are clearer spatially than in prose alone.
- When to Omit Cleanly: Omit when Section 3's dry-run table already makes state transitions obvious. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: Render a compact ASCII state-transition walkthrough or Mermaid diagram aligned to the exact tricky dry-run input, highlighting the pivotal invariant-preserving transition.
-->

- **Context:** Name the spatial structure (pointers, window, stack, tree, DP grid) and tricky input being traced.
- **Analysis:** Show the aligned ASCII or Mermaid state transitions across the key inflection steps.
- **Check:** State the invariant visible at every transition and the edge state that would violate it.

See [authoring rules](../shared/authoring_rules.md) for 5-key YAML, rendering, evidence, and cohesion.
See [math gates](../shared/math_gates.md) for selected mathematical depth.
See [footer contract](../shared/footer_widgets.md) for reflection behavior.
- **Template Contract (`dsa`):** Retain constraints audit (`[ASSUMED / UNVERIFIED]` for missing bounds), runnable brute-force baseline + optimization bridge, tricky-input dry-run table, C++ `int64_t` overflow & auxiliary-space audit, edge-case suite, and collapsed related-problem twists.
