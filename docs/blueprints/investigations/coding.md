# Coding experimental lab

Use for programming, algorithms, data structures, APIs, and software engineering investigations. Keep this hierarchy and the opening rules in [the lab contract](../../procedures/authoring/experimental-lab.md) (no visible opening inventory dumps; begin with a connected introduction and parent-note link). Each subsection needs an explained concrete example, checkable deliverable, collapsed line-by-line code walkthrough (`> [!example]- Understand this implementation line by line`), and visual where it clarifies state or flow. Never inspect the local environment, install packages, create project files, or fabricate execution results (`Status: static review (not executed)` or `"Documentation-checked example; not compiled or executed here."`).

The section prompts below define purpose and content. Use this companion check for an example, evidence, visual opportunity, and common error to avoid:

| Section | Example and evidence/deliverable | Visual opportunity | Avoid; genuine limit |
|---|---|---|---|
| 01 | Two-sum or LRU cache problem & target complexity | End-to-end lab flow Mermaid | Avoid vague "learn coding" goals; always |
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
State the concrete software or algorithmic problem, why naive approaches bottleneck, what capability the implementation delivers, and essential prerequisites right before use. Include a native Mermaid flow showing how baseline, optimal implementation, experiments, and verification connect.
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
### Input validation, separation, and integration
Walk step by step (with code and collapsed explanation per step) through input validation, core module separation, error handling, and final program assembly, keeping names and fixtures consistent with earlier sections.
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
