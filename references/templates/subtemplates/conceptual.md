# Subtemplate: Conceptual

- **Purpose:** Build deep mental models for concepts, definitions, mechanisms, comparisons, and method-selection decisions without forcing unnecessary equations or code.
- **Activation conditions:** Concepts, classifications, trade-offs, architectural principles, or method selection (`conceptual`, `comparative`).
- **Required inputs:** Concept identity, learning objectives, prerequisite map, audience baseline, source policy, concrete examples/counterexamples, and boundary conditions.

> **Authoring-agent image instruction:** Before drafting, identify the visual learning needs of each substantive concept. Acquire suitable images where they materially improve understanding. Inspect the saved images, then compose the explanation around their actual visible content. Do not treat image placement as an optional finishing step.

## Teaching Sequence

1. **Orient:** Name the concrete problem or confusion the concept resolves and why simpler mental models fail.
2. **Bridge prerequisites:** Define unfamiliar terms and analogies before first use; state where each analogy breaks down.
3. **Explain mechanism & distinctions:** Present the core idea in natural paragraphs, one conceptual move per paragraph, using concrete examples and counterexamples.
4. **Causal comparison:** Explain *why* alternatives differ in prose before summarizing in a comparison table.
5. **Boundaries & check:** State explicit **Use when / When not to use** limits and include a reasoning-focused quick check.

## Obligations

- **Evidence expectations:** Ground definitions and comparisons in verified sources with locators when source-bound; separate established facts from author analogies.
- **Visual requirements:** Follow [representations.md](../../workflows/notes-creation/representations.md) using **Orient → Show → Explain → Work through → Connect**. Image opportunities: conceptual schemas, real-world referent photos, side-by-side before/after or contrast figures; use native Mermaid for taxonomies, decision trees, and state/process flows.
- **Mathematical explanation requirements:** Omit forced math for non-quantitative concepts; if a governing relation appears, bind it to [math_gates.md](../../../shared/math_gates.md).
- **Practical-example requirements:** Include at least one concrete example and one boundary counterexample showing where the concept fails or no longer applies.
- **Failure handling:** Repair topic-name substitutions, ungrounded analogies, or tables without causal prose locally; retrieve additional sources only when permitted.
- **Completion checks:** Verify against [verification-checklist.md](../../workflows/validation/verification-checklist.md) — zero undefined terms, zero unsupported comparisons, and every embedded visual decoded in prose.
