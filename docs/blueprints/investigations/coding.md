# Coding experimental lab

Use for programming, algorithms, data structures, APIs, and software engineering investigations. Keep this hierarchy and the opening rules in [the lab contract](../../procedures/authoring/experimental-lab.md) (no visible opening inventory dumps; begin with a connected introduction and parent-note link). Each subsection needs an explained concrete example, checkable deliverable, collapsed line-by-line code walkthrough (`> [!example]- Understand this implementation line by line`), and visual where it clarifies state or flow. Never inspect the local environment, install packages, create project files, or fabricate execution results (`Status: static review (not executed)` or `"Documentation-checked example; not compiled or executed here."`).

The section prompts below define purpose and content. Use this companion check for an example, evidence, visual opportunity, and common error to avoid:

| Section | Example and evidence/deliverable | Visual opportunity | Avoid; genuine limit |
|---|---|---|---|
| 01 | Two-sum or LRU cache problem & target complexity | End-to-end lab architecture web figure | Avoid vague "learn coding" goals; always |
| 02 | Input/output types, bounds (`n <= 10^5`), edge fixture | I/O & constraint map | Avoid unstated integer overflow or empty-input rules; always |
| 03 | Loop/data-structure invariant & Big-O cost model | State/pointer diagram or raster figure | Avoid memorizing Big-O without counting operations; always |
| 04 | Clear brute-force baseline exposing redundant work | Nested-loop / repeated-work trace | Avoid fake naive code when optimal is already direct |
| 05 | Optimal algorithm + discriminating dry-run trace table | Pointer, window, or heap evolution | Avoid skipping tricky branches; trace one non-trivial input |
| 06 | Idiomatic standard-library / typed implementation | Structure or API call flow | Avoid inventing unverified library APIs; check official docs |
| 07 | Input-size, worst-case, & data-layout experiments | Scaling / collision comparison table | Avoid claiming measured runtime benchmarks without running |
| 08 | Modular end-to-end program with CLI/API boundary | Module & error-handling flow | Avoid scattering incompatible snippets across steps |
| 09 | Edge-case matrix (empty, duplicate, extreme, adversarial) | Pass/fail property matrix | Avoid presenting static review as executed test runs |
| 10 | Off-by-one, mutation-during-iteration, & overflow bugs | Buggy vs fixed state trace | Avoid generic "be careful" warnings; always |
| 11 | Time vs auxiliary space & cache/allocation trade-offs | Memory layout or complexity table | Avoid language-speed stereotypes without workload context |
| 12 | Baseline vs optimal vs standard-library comparison | Decision table on matched inputs | Avoid comparing unlike input contracts; always |
| 13 | Guided-to-independent coding & debugging challenges | Trace table to complete | Avoid answerless prompts; always |
| 14 | Predict output, spot invariant break, justify complexity | Short state trace | Avoid trivia recall of syntax names; always |
| 15 | Core invariant, complexity bounds, and transfer link | Usually no new image | Avoid treating planned runs as verified benchmarks; always |

## LAB SECTION 01 — INTRODUCTION AND CODING OBJECTIVES
### Problem and capability
State the concrete software or algorithmic problem, why naive approaches bottleneck, what capability the implementation delivers, and essential prerequisites right before use. Show how baseline, optimal implementation, experiments, and verification connect using a downloaded local web diagram or structured stage table (never Mermaid or ASCII).
## LAB SECTION 02 — PROBLEM CONTRACT, INPUTS, AND CONSTRAINTS
### Types, bounds, and discriminating fixture
Define exact input/output types, preconditions, constraints (`n` bounds, value ranges, mutability), and one discriminating miniature fixture traced across all implementations. State what happens on empty, duplicate, or out-of-range inputs.
## LAB SECTION 03 — INVARIANTS, REPRESENTATION, AND COMPLEXITY BRIDGE
### Why the mechanism works
Explain the governing invariant (initialization, maintenance, termination), data-structure representation, and time/space cost model before writing full code. Bind any recurrence or cost formulas with [math_gates.md](../../../core/math_gates.md) and decode a state diagram or inspected local visual via [representations.md](../../procedures/authoring/representations.md).
## IMPLEMENTATION TRACK A — BASELINE AND OPTIMAL MECHANISM
Reveal what high-level abstractions hide before reaching for built-in helpers.
## LAB SECTION 04 — BASELINE IMPLEMENTATION
### Expose the bottleneck
Present the simplest correct baseline (omitting fake baselines when optimal is direct) inside a Markdown fence, followed by a collapsed line-by-line walkthrough quantifying the exact bottleneck on the shared fixture.
## LAB SECTION 05 — OPTIMAL ALGORITHM AND STATE TRACE
### Complete code and dry-run trace
Provide the complete self-contained optimal implementation in Markdown, a collapsed line-by-line walkthrough (covering purpose, syntax, types, invariants, mutations, mistakes, and next step), and a dry-run table tracing the discriminating fixture through key branches.
## IMPLEMENTATION TRACK B — IDIOMATIC STANDARD LIBRARY / TYPED TRACK
Use the same fixture and input contract.
## LAB SECTION 06 — STANDARD LIBRARY AND LANGUAGE COMPARISON
### Idiomatic abstractions and doc-checked APIs
Show how idiomatic standard-library constructs (or a secondary typed/systems language such as Rust when educationally valuable) express the same task. Verify any third-party library APIs via official version-specific docs without inspecting the local environment or installing dependencies; label doc-checked unexecuted code **"Documentation-checked example; not compiled or executed here."**
## EXPERIMENTAL INVESTIGATION
Design fair, reproducible comparisons; never invent timings or outputs.
## LAB SECTION 07 — CONTROLLED CODING EXPERIMENTS
### Scaling, adversarial inputs, and memory layout
Design controlled investigations varying one factor at a time: input size scaling, adversarial/worst-case inputs (e.g., hash collisions, sorted inputs), and data-structure choices. State hypothesis, controls, procedure, what to record, and honest execution status.
## PROFESSIONAL IMPLEMENTATION TRACK
Assemble a clean, testable program boundary.
## LAB SECTION 08 — END-TO-END MODULAR PROGRAM
### Part A — Complete Real-World Modular Build (12 Steps)
Replace disconnected helper snippets with a realistic end-to-end program on a realistic input corpus or workload. For **every** applicable step, provide: (1) prose explaining purpose and design choice, (2) executable Markdown code block (`Status: static review (not executed)` if unexecuted), (3) collapsed `> [!example]- Step-by-step: ...` walkthrough, (4) expected output/table interpretation without fabricating unrun timings, and (5) transition to the next step:
1. **Imports & Module Setup:** Group standard-library / documentation-checked crate or package imports cleanly.
2. **Load or Parse Realistic Input Workload:** Define input schema, size scale, and domain polarity/convention (e.g., 1-based vs. 0-based indexing, tie-breaking rules, `Input | Meaning` table).
3. **Inspect & Validate Input Integrity:** Check length/size, type bounds, duplicates, empty inputs, and malformed records (`Check | Purpose` table).
4. **Partition Test Fixtures (Nominal / Edge / Adversarial):** Separate standard cases, boundary/degenerate fixtures, and worst-case inputs with explicit sample counts and reproducibility seed if randomized.
5. **Design Clean Modular Pipeline:** Chain `parse -> validate -> core_engine -> format_result` with clear ownership/immutability boundaries and zero hidden global state.
6. **Execute & Trace Core Engine Internals:** Walk step by step through the internal execution sequence (initialize state/buffers → maintain invariant per step → handle collisions/rebalancing/cache eviction → terminate cleanly).
7. **Compare Output Contracts (`bool` vs. `Option/Result` vs. Structured Report):** Contrast raw return values, diagnostic state objects, and error types in a `Method/Return | Example output` table.
8. **Evaluate Functional & Complexity Metrics by Category:** Separate **correctness checks** (exact equality, invariant preservation, property checks) from **resource bounds** (operation counts, comparisons, allocations, asymptotic time/space) against the baseline on the **same** fixtures.
9. **Plot or Tabulate Scaling Behavior:** Present complexity/operation-count comparison code or structured trace tables across input sizes (without fabricating unmeasured wall-clock timings).
10. **Extract Internal Telemetry & State Metrics:** Inspect counters such as comparisons, swaps, hash collisions, cache hit ratio, or peak stack depth (`Metric | Meaning` table).
11. **Visualize Operation Breakdown & Hardware Caveat:** Summarize dominant cost centers and warn that asymptotic Big-O ignores constant factors, cache locality, and allocator noise.
12. **Guarded CLI / API Entrypoint:** Wrap final integration with explicit precondition validation and actionable error returns.

### Part B — Configuration, Algorithm Variants & Parameter Tuning
- **Invariants vs. Configuration Parameters Table:** Contrast algorithmic invariants (fixed correctness rules) against tunable engineering parameters (`initial_capacity`, `load_factor`, `branching_factor`, `cache_size`, `threshold`, `max_depth`).
- **Threshold & Capacity Sensitivity:** Concrete parameter table showing trade-offs (e.g., low vs. high hash load factor, recursion cutoff to insertion sort, buffer chunk size).
- **Strategy & Data-Structure Compatibility Matrix:** Compare alternative implementations/variants across time complexity, space overhead, mutability/thread safety, and worst-case guarantees.
- **Safety Caps & Degeneracy Controls:** Explain `max_depth` / stack guards, timeout/iteration caps, overflow-checked arithmetic, and tie-breaking rules.
- **Systematic Benchmark / Stress-Test Design:** Define a controlled multi-size, multi-distribution harness (sorted, reverse-sorted, random, adversarial), showing exact trial counts (`configs × distributions × sizes`) and honest `Status: static review (not executed)` reporting.
## FINAL VALIDATION AND LEARNING
## LAB SECTION 09 — CORRECTNESS TESTING AND EDGE CASES
### Property checks and honest status
Test empty/minimal, duplicate/degenerate, adversarial, and boundary cases against independently calculated expectations. State property, inputs, expected result, what it establishes/does not establish, and `Status: static review (not executed)` when unexecuted.
## LAB SECTION 10 — COMMON BUGS AND DEBUGGING
### Concrete failure walkthroughs
Diagnose off-by-one bounds, aliasing/mutation bugs, integer overflow, and wrong complexity assumptions with symptom, cause, inspection step, fix, and prevention.
## LAB SECTION 11 — TIME, SPACE, AND RESOURCE TRADE-OFFS
### Complexity and allocation
Analyze asymptotic time, auxiliary stack/heap space, and data-locality trade-offs without fabricating unmeasured microbenchmarks.
## LAB SECTION 12 — IMPLEMENTATION COMPARISON
### Matched-contract comparison
Compare baseline, optimal manual, and standard-library/typed implementations on clarity, invariant visibility, error surface, and asymptotic cost.
## LAB SECTION 13 — PRACTICAL CHALLENGES
### Extend and debug
Provide beginner, intermediate, advanced transfer, and debugging challenges with separately collapsed hints/answers.
## LAB SECTION 14 — FINAL LEARNING CHECKPOINT
### Reasoning over syntax
Ask the learner to trace a state transition, spot a broken invariant, and defend a complexity bound, with collapsed `> [!tip]- Answer` guidance.
## LAB SECTION 15 — FINAL SUMMARY
### What was built and where to go next
Summarize the core invariant, time/space bounds, key bug patterns, and link back to the parent note.
