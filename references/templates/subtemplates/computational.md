# Subtemplate: Computational

- **Purpose:** Teach algorithms, data structures, ML/DL mechanics, and code pipelines by connecting intuition, state transitions, mathematics, and honest code explanations.
- **Activation conditions:** Code, algorithms, invariants, state machines, complexity bounds, ML/DL architectures, or debugging (`programming`, `algorithmic`, `architectural`, `procedural`).
- **Required inputs:** Input/output contract, bounds/assumptions, target language/stack, equation-to-code mapping, edge-case fixtures, and execution status.

> **Authoring-agent image instruction:** Before drafting, identify the visual learning needs of each substantive concept. Acquire suitable images where they materially improve understanding. Inspect the saved images, then compose the explanation around their actual visible content. Do not treat image placement as an optional finishing step.

## Teaching Sequence

1. **Contract & bottleneck:** Clarify exact input/output types, shapes, and why a naive approach bottlenecks.
2. **Visual & state intuition:** Show intermediate states or data flow before code so the learner sees what the code is automating.
3. **Complete code + collapsed walkthrough:** Present the complete relevant code block, give a brief visible summary, then explain operations in a collapsed `> [!example]- Step-by-step: ...` callout (covering purpose, syntax, variables, types, inputs, internal execution, math link, output, shapes, mistakes, and next step).
4. **Equation-to-code mapping:** Map mathematical terms directly to code expressions, types, and shapes.
5. **Trace, test & debug:** Walk a small concrete input through the code, state edge cases, and report honest execution status.

## Obligations

- **Evidence expectations:** Label unexecuted code `Status: static review (not executed)`; never fabricate runtime output, benchmarks, or crate/library APIs.
- **Visual requirements:** Follow [representations.md](../../workflows/notes-creation/representations.md) using **Orient → Show → Explain → Work through → Connect**. Image opportunities: ML/DL decision boundaries, network architectures, tensor organization, diagnostic curves (loss/ROC/confusion matrices), and meaningful intermediate/before-after states; use native Mermaid for control flow, pipelines, and state machines.
- **Mathematical explanation requirements:** Bind any governing equations via [math_gates.md](../../../shared/math_gates.md) and expand code-to-math mappings step by step rather than one-line claims.
- **Practical-example requirements:** Trace one small concrete input end to end (showing exact slice/tensor/variable values) and include edge-case checks.
- **Failure handling:** Replace one-line syntax summaries, cross-reference-only explanations, or unverified API claims with complete step-by-step walkthroughs and honest gaps.
- **Completion checks:** Verify against [verification-checklist.md](../../workflows/validation/verification-checklist.md) — complete code before breakdown, collapsed walkthroughs quoted properly, and honest execution status.
