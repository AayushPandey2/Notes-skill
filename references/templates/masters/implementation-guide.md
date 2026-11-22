<!-- scaffold:preflight
Master ID: M5 (implementation_guide / compatibility route: dsa).
Primary intent: practical_implementation — build, implement from scratch, trace, test, and debug technical solutions with verified executable evidence.
Activation signals: /scribe-notes implementation requests, "implement from scratch", "build this project", "write and test the code", "debug this program", "code walkthrough", "solve <problem> in <language>".
Non-activation: Deep conceptual theory with a small code example -> M1; API lookup table -> M3/syntax_reference.
Pre-Flight: [router](../../../router.md) and [authoring rules](../../../shared/authoring_rules.md).
Strip this block before emission.
-->

# M5 — Implementation, Algorithmic Design & Technical Verification Guide

Invoked internally through `/scribe-notes` (locking code generation to the requested language when specified) for algorithm solutions, from-scratch implementations, framework walkthroughs, debugging guides, and build tutorials. Integrates `EIS-05` state narration, F11 implementation-staged progressive disclosure, F12 implementation/debugging outcomes, and mandatory Obsidian Properties.
- **Header Block**: 5-key YAML frontmatter + `# DSA: <Problem Title>` (or `# <nn>. <Implementation Title>`) + `> [!abstract] Complexity Target & Core Invariant`.

## 1. What is the exact problem, what are the constraints & what complexity target do they force? (Problem Specification & Envelope)

<!--
KEEP the problem/implementation contract, requirements, runtime/library versions, and actual constraints. Tag missing constraints as [ASSUMED / UNVERIFIED]. Remove before publication.
-->

- **Problem Statement & I/O Contract**: Formal specification, input/output types, dependencies, and concrete small example.
- **Verified Constraints & Missing-Constraint Audit**: List stated input bounds, runtime versions, and memory/time limits (`[ASSUMED / UNVERIFIED]` if missing).
- **Inferred Asymptotic Target Envelope**: Deduce plausible time and auxiliary space complexity targets from stated limits without guessing wall-clock timings.
- **Algorithmic Pattern & Unbreakable Invariant**: Name the core architecture/pattern and state its governing invariant in `2–3` sentences.

## 2. What is the brute-force baseline and why does it bottleneck? (Naive Approach & The Optimization Bridge)

<!--
Show the smallest baseline or naive design that exposes the bottleneck (omit fake optimizations if baseline is already optimal). Remove before publication.
-->

- **Brute-Force Intuition & Runnable Code**: Direct baseline implementation in the selected language.
- **Exact Bottleneck Quantification**: Time/space cost explaining why the naive approach bottlenecks.
- **The Optimization Bridge**: Pinpoint the redundant work and structural insight that eliminates it.

## 3. How does the optimal algorithm work step by step? (Mechanism, Correctness Justification & Dry-Run Table)

<!--
Trace a discriminating input, map equations/invariants to code variables, and justify initialization, maintenance, and termination. Remove before publication.
-->

- **Step-by-Step Optimal Mechanism & Correctness Proof**: Walk through state transitions, invariant justification (`math_level` `1` or `2`), and exact Time/Space Complexity.
- **Complete Step-by-Step Dry-Run Table**: Choose a **tricky, non-trivial input** triggering key branches/evictions and trace every step in a Markdown table (escaping pipes `\|`).

## 4. How do I implement and stress-test the optimal solution? (Implementation & Edge-Case Suite)

<!--
KEEP a complete runnable implementation in the selected language with honest verification tier (generated / syntax_checked / executed / tests_passed). Never fabricate execution output or run untrusted source code. Remove before publication.
-->

- **Complete Optimal Implementation**:
    - Fully runnable, self-contained code with imports/includes, explicit equation-to-code mapping, and a test driver.
    - For `C`/`C++`, explicitly audit integer widths (`int64_t` vs. `int32_t`), bounds, and memory/iterator validity.
    - Record runtime/compiler version and exact execution status (`executed` + verbatim `stdout` via `plan_notes.py verify-runtimes`, or `static verification (not executed)`).
- **Verified Edge-Case Test Matrix (`4–5` Tricky Cases)**:
    - Markdown table and runnable assertions covering: (1) Minimum/empty boundary input, (2) Duplicate/all-equal elements, (3) Adversarial/monotonic order, (4) Overflow/extreme boundary, and (5) The tricky dry-run input.

## 5. How does this pattern transfer to harder variations? (Related Problems, Twists & Reflections)

<!--
KEEP variations, debugging follow-ups, or operational extensions that alter the invariant or constraints. Remove before publication.
-->

- **Related Problems (`2–3` Curated Follow-Ups)**: Present each prompt visibly, then place its structural twist and optimal adaptation inside an independently collapsed callout: `> [!example]- Reveal Structural Twist & Optimal Solution for <Related Problem Title>`

<!-- optional: complexity -->
## [OPTIONAL] Why does the resource bound hold? (Formal Complexity & Lower-Bound Derivation)

<!--
Include only formal resource reasoning allowed by the math contract. Remove before publication.
-->

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: A non-obvious recurrence, amortized charging/potential argument, or information-theoretic lower bound is essential to proving optimality.
- When to Omit Cleanly: Omit when complexity follows trivially from a single loop or is already derived in Section 3. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: State the cost model and input variables; derive the recurrence, potential function, or lower bound step by step; separate worst-case from amortized bounds and show a discriminating worst-case input.
-->

- **Context:** State the cost model, input-size variables, and why naive counting is insufficient.
- **Analysis:** Justify the recurrence, amortized charging/potential argument, or lower bound and separate worst-case from amortized cost.
- **Check:** Supply a concrete adversarial/discriminating input confirming the tight bound.

<!-- optional: visual -->
## [OPTIONAL] How do pointers, windows, or structures evolve step by step? (Visual Diagram / ASCII State-Transition Walkthrough)

<!--
Include a diagram only when a state transition is hard to follow in the trace. Remove before publication.
-->

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: Multi-pointer motion, monotonic stack/deque eviction, tree/DP-table transitions, or bit/memory layouts are clearer spatially than in prose alone.
- When to Omit Cleanly: Omit when Section 3's dry-run table already makes state transitions obvious. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: Render a compact ASCII state-transition walkthrough or Mermaid diagram aligned to the exact tricky dry-run input, highlighting the pivotal invariant-preserving transition.
-->

- **Context:** Name the spatial structure (pointers, window, stack, tree, DP grid) and tricky input being traced.
- **Analysis:** Show the aligned ASCII or Mermaid state transitions across the key inflection steps.
- **Check:** State the invariant visible at every transition and the edge state that would violate it.

See [authoring rules](../../../shared/authoring_rules.md), [math gates](../../../shared/math_gates.md), and [footer contract](../../../shared/footer_widgets.md).
- **Template Contract (`M5` / `dsa`):** Retain constraints audit (`[ASSUMED / UNVERIFIED]`), runnable baseline + optimal code, tricky dry-run table, honest execution status (`verify-runtimes`), edge-case suite, and collapsed follow-up twists.
