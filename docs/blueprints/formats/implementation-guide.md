<!-- scaffold:preflight
Purpose: Build, implement from scratch, trace on non-trivial inputs, test, and verify algorithms or systems engineering solutions cleanly.
Master ID: M5 (implementation_guide / compatibility route: dsa).
Activation Trigger: /scribe-notes requests to implement from scratch, build/debug code, write verified algorithm solutions, or trace program state.
Non-activation: Deep conceptual theory with minor snippets -> M1; syntax/API table -> M3/syntax_reference.
Inputs: Problem/system spec, stated bounds, chosen language/stack, test fixtures, and runtime verification status.
Dependencies: router.md, core/teaching_core.md, core/authoring_rules.md, core/math_gates.md, properties/properties-policy.md.
Decision Rules: Lock educational code to the user-specified stack; explain a simpler baseline when it clarifies the bottleneck. Never execute code or inspect local runtimes.
Failure Handling: Tag missing constraints [ASSUMED / UNVERIFIED]; label code 'Source and static review only; not compiled or executed here.'; never fabricate runtime metrics.
Validation: [verification-checklist.md](../../procedures/review/verification-checklist.md) (`M5` implementation rules).
-->

# M5 — Implementation, Algorithmic Design & Technical Verification Guide

- **Header Block:** Line-1 Obsidian Properties (`note_type: implementation-guide`) + `# Implementation: <Title>` (or `# DSA: <Title>` when solving DSA tasks) + `> [!abstract] Complexity Target & Core Invariant`.
- **Six Implementation Types:** Select the mode matching the implementation request rather than forcing algorithmic baseline-vs-optimal framing onto every build:
  - *Algorithm* (correctness, loop/recursion invariants, complexity)
  - *Library / API* (contract, lifecycle, state transitions, error conditions)
  - *System* (components, interfaces, resource management, concurrency/isolation)
  - *Application / Full-Stack* (requirements, file responsibilities, frontend-to-backend request flow, persistent data model, input validation, authn/authz, config & secret handling, error propagation, reproducible setup, tests)
  - *Infrastructure* (configuration, dependencies, environment isolation, reliability/recovery)
  - *Debugging* (observed symptoms, competing hypotheses, discriminating inspections, verified fixes)
  For Application/Full-Stack and System guides, multi-file architecture explanations are permitted inside Markdown code blocks (while still never creating repo/project files on disk or executing code).

## 1. What is the exact problem, what are the constraints & what complexity target do they force? (Problem Specification & Envelope)

- **Problem Statement & I/O Contract:** Input/output types, preconditions, and small concrete instance.
- **Constraints Audit:** Verified bounds and library/compiler versions (`[ASSUMED / UNVERIFIED]` for unstated limits).
- **Target Complexity & Governing Invariant:** Asymptotic envelope justified from bounds and core invariant (`2–3` sentences).

## 2. What is the brute-force baseline and why does it bottleneck? (Naive Approach & The Optimization Bridge)

- **Baseline Intuition & Runnable Code:** Simplest baseline exposing redundant work (omit fake naive variants when optimal is already direct).
- **Bottleneck Quantification & Optimization Bridge:** Identify exact cost wall and the structural invariant eliminating it.

## 3. How does the optimal algorithm work step by step? (Mechanism, Correctness Justification & Dry-Run Table)

- **Mechanism & Correctness:** State transitions, loop/recursion invariant (`initialization`, `maintenance`, `termination`), and exact complexity.
- **Dry-Run Trace Table:** Trace a **discriminating, non-trivial input** triggering key branches/edge cases (escaping internal `|` pipes cleanly).

## 4. How do I implement and stress-test the optimal solution? (Implementation & Edge-Case Suite)

- **Runnable Optimal Implementation:** Complete self-contained code with explicit equation-to-variable mapping and test driver. In statically typed/systems languages, audit numeric bit-widths, overflow bounds, and iterator/memory safety. Label code `Source and static review only; not compiled or executed here.` without running code on the user's device.
- **Edge-Case Test Matrix (`4–5` Cases):** Assertions covering minimal/empty, duplicate/degenerate, adversarial/monotonic, extreme boundary, and dry-run fixture.

## 5. How does this pattern transfer to harder variations? (Related Problems, Twists & Reflections)

- **Related Variations (`2–3`):** Show visible prompt followed by an unquoted blank line and collapsed `> [!example]- Reveal Structural Twist & Optimal Solution for <Title>`.

<!-- optional: complexity -->
## [OPTIONAL] Why does the resource bound hold? (Formal Complexity & Lower-Bound Derivation)

<!-- Include only when non-obvious recurrence/amortized/lower-bound proof adds insight; delete cleanly otherwise. -->

- **Context / Analysis / Check:** Cost model, recurrence/potential derivation, worst-case vs amortized distinction, discriminating bound case.

<!-- optional: visual -->
## [OPTIONAL] How do pointers, windows, or structures evolve step by step? (Visual Diagram / State-Transition Walkthrough)

<!-- Include when spatial structure beats table trace; follow representations.md for completed local web raster embeds (never Mermaid or ASCII). -->

- **Context / Analysis / Check:** Structure traced, inflection transitions ([representations.md](../../procedures/authoring/representations.md)), and invariant parity check.

- **Contract Summary:** Verify constraints audit, runnable baseline + optimal code, tricky dry-run trace, honest runtime status, edge-case suite, and [authoring_rules.md](../../../core/authoring_rules.md) / [math_gates.md](../../../core/math_gates.md) / [footer_widgets.md](../../../core/footer_widgets.md).
