# Subtemplate: Computational

- **Purpose:** Teach algorithms, data structures, ML/DL models, software systems, and code pipelines by connecting intuition, state transitions, architecture traces, mathematics, and beginner-accessible code walkthroughs.
- **Activation conditions:** Code, algorithms, invariants, system architectures, state machines, complexity bounds, ML/DL pipelines, or debugging (`programming`, `algorithmic`, `architectural`, `procedural`).
- **Expected inputs:** Problem/system contract, bounds/assumptions, target stack, equation-to-code mapping, deterministic running fixture, edge-case inputs, and honest execution status.

> **Authoring-agent image instruction:** Before drafting, identify the visual learning needs of each substantive concept. Acquire suitable images where they materially improve understanding. Inspect the saved images, then compose the explanation around their actual visible content. Do not treat image placement as an optional finishing step.

- **Teaching progression:** Establish the bottleneck or system question → trace one concrete input through intermediate states or system components (inputs/outputs, state, trust boundaries, failure/recovery) → present complete relevant code → summarize briefly in visible prose → unpack operations in collapsed `> [!example]- Step-by-step: ...` walkthroughs → map math to code → diagnose mistakes and test edge cases.
- **Necessary prerequisite bridges:** Define types, shapes, memory/ownership concepts, and API roles before first use; never reduce syntax explanations to one-line summaries or cross-references.
- **Visual opportunities:** Follow [representations.md](../../procedures/authoring/representations.md) using the six-phase visual narrative. Image opportunities: ML/DL decision boundaries, architectures, tensor layouts, diagnostic curves, and meaningful before/after states; use native Mermaid for control flow, pipelines, sequence traces, and state machines.
- **Formalism appropriate to the knowledge type:** Expand equation-to-code mappings step by step via [math_gates.md](../../../core/math_gates.md) (collection contents, iteration, conversions, calculations, small trace, nonempty/precision limits).
- **Worked-example requirements:** Trace one deterministic miniature fixture end to end through variables, shapes, and outputs (never stop at a whole-system picture without tracing a concrete input).
- **Evidence requirements:** Keep educational code inside Markdown fences, verify APIs before citing, and label unexecuted code `Status: static review (not executed)` once per implementation; never fabricate outputs or benchmarks.
- **Practice and mastery checks:** Include code-prediction, trace-the-state, bug-diagnosis, and edge-case exercises with collapsed answers.
- **Failure handling:** Locally replace one-line syntax summaries, hollow placeholder tracks, unmapped formulas, or fabricated outputs via [verification-checklist.md](../../procedures/review/verification-checklist.md).
