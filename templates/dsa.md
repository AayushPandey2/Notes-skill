# Algorithmic Problem Solving, Bottleneck Analysis & Production Implementation

Supports `/scribe-dsa cpp <problem>` and `/scribe-dsa python <problem>` (and any additional supported language), locking code generation to the requested language.
- **Header Block**: YAML frontmatter (`type: dsa`, `language: <cpp|python>`) + `# DSA: <Problem Title>` + `> [!abstract] Complexity Target & Core Invariant`.

## 1. What is the exact problem, what are the constraints & what complexity target do they force? (Problem Specification & Envelope)

- **Problem Statement & I/O Contract**: Formal statement, input/output types, and concrete small example.
- **Verified Constraints & Missing-Constraint Audit**: List all stated input bounds ($N$, value ranges, graph density, memory/time limits). Explicitly tag any missing constraint or assumption as `[ASSUMED / UNVERIFIED]`.
- **Inferred Asymptotic Target Envelope**: Deduce the plausible required time and auxiliary space complexity class from the verified size and time limits (e.g., $N \le 2 \cdot 10^5$ suggests $O(N \log N)$ or $O(N)$ target) without promising exact wall-clock runtime from $N$ alone.
- **Algorithmic Pattern & Unbreakable Invariant**: Name the core pattern (e.g., Monotonic Queue, Offline Fenwick Tree, Binary Search on Answer) and state the governing loop/recursion invariant in `2–3` sentences.

## 2. What is the brute-force baseline and why does it bottleneck? (Naive Approach & The Optimization Bridge)

- **Brute-Force Intuition & Runnable Code**: Explain the direct exhaustive approach and provide clean, runnable baseline code in the selected language.
- **Exact Bottleneck Quantification**: Derive the brute-force Time and Space Complexity and quantify operation counts at maximum $N$ to explain why it exceeds time/memory limits.
- **The Optimization Bridge**: Pinpoint the exact redundant computation (e.g., re-scanning elements, recomputing prefix states) and explain the structural insight that eliminates it. _(Guardrail: If the brute-force solution is already asymptotically optimal, prove why it matches the lower bound and do not invent a fake optimization)._

## 3. How does the optimal algorithm work step by step? (Mechanism, Correctness Justification & Dry-Run Table)

- **Step-by-Step Optimal Mechanism & Correctness Proof**: Walk through the state transitions, prove why the invariant holds at initialization, maintenance, and termination (`math_level` `1` or `2`), and derive exact Time and Space Complexity (explicitly stating whether auxiliary space excludes the required output container).
- **Complete Step-by-Step Dry-Run Table**: Choose a **tricky, non-trivial input** (one that triggers pointer adjustments, stack pops, or tie-breaking) and trace every loop iteration, index, auxiliary data structure state, and return update in a Markdown table (escaping all pipes `\|`).

## 4. How do I implement and stress-test the optimal solution? (Production Code & Edge-Case Suite)

- **Complete Optimal Implementation (`C++20` or `Python 3`)**:
    - Fully runnable, self-contained code with imports/includes and a test driver.
    - For `C++`, explicitly audit integer widths (`int64_t` / `long long` vs. `int32_t`) against worst-case accumulation overflow, fast I/O concerns, and iterator validity.
    - Record compiler/runtime version and execution status (`executed` vs. `not executed`).
- **Verified Edge-Case Test Matrix (`4–5` Tricky Cases)**:
    - Markdown table and runnable assertions covering: (1) Minimum/empty boundary input, (2) All-equal / duplicate elements, (3) Strictly monotonic / adversarial order, (4) Maximum value / integer-overflow boundary, and (5) The tricky dry-run input, showing Expected vs. Observed outputs.

## 5. How does this pattern transfer to harder variations? (Related Problems, Twists & Reflections)

- **Related Problems (`2–3` Curated Follow-Ups)**: For each related problem, present its full problem prompt visibly, then place its structural twist and optimal solution adaptation inside an independently collapsed callout:`> [!example]- Reveal Structural Twist & Optimal Solution for <Related Problem Title>`
- Append `shared/footer_widgets.md` (**What I learned**, **Open Confusion** `**Confusion** :: ...`, **Atomize**, **Connection**, and the `dataviewjs` **Mark Revisited** button).

Follow [shared authoring rules](../shared/authoring_rules.md) and the [footer contract](../shared/footer_widgets.md). Apply the math gate only at the planned level. Scaffold comments are editing slots and must be removed before publication.

> [!important] AGENT AUTHORING DIRECTIVE — `dsa` Retain every section from constraints audit through the brute-force optimization bridge, dry-run table, edge-case harness, and collapsed related-problem twists. Never skip the brute-force code or the step-by-step dry-run table on a tricky input. In C++, always verify 64-bit integer overflow boundaries (`int64_t`), explicitly state whether auxiliary space excludes the output container, and compile or execute the test harness whenever a runtime is available.
