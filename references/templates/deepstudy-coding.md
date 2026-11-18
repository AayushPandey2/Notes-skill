# DeepStudy-Coding

**Use for:** mechanisms, algorithms, ML operations, systems behavior, data transformations, or engineering concepts that need implementation to understand them.

**Research:** relevant primary papers, official API/standard documentation, and substantive implementation sources. Fetch evidence for the selected language and version, not merely a general explainer.

## What am I trying to understand?

- Open with 3–4 clear, symbol-free sentences: the concrete problem, its inputs and outputs, why the mechanism is needed, and what a simpler approach can and cannot handle.
- State **Learning outcome**, **Scope**, and **How to recognize this problem in practice**.
- Set a meaningful success criterion, such as matching a reference operation under stated assumptions. Avoid a vague goal such as “understand deeply.”

## Overview

- Explain what the mechanism does in plain language and where it fits in the larger system.
- Add a **Start here** prerequisites callout: introduce terms in dependency order with meaning, relevant type/units, and a tiny example. Link prerequisite notes that actually exist.
- Include a short readiness check whose answer exposes a missing prerequisite rather than just asking “Are you ready?”
- State the central mechanism, invariant, and validity boundary in words. Reserve formal justification for Details.

## How it works

- Identify preconditions as `A1`, `A2`, and so on when later reasoning needs to reference them.
- Introduce one named running example with explicit inputs and a clear expected outcome.
- Explain each causal step: what enters, what changes internally, what condition or operation determines the next step, and what comes out.
- For a suitable computational mechanism, use input → internal transformation → decision/aggregation → output. Adapt this sequence to the real process; do not invent a threshold for an operation without one.
- Trace state, shapes, ownership, or data movement where it explains the mechanism.
- Add a focused Mermaid diagram for three or more interacting components or a genuinely useful process trace, followed by 2–3 sentences explaining it.

## Intuition / Mental Model

- Give an everyday analogy or a direct technical mental model, with an explicit object-to-concept mapping.
- Add a **Where the analogy breaks** warning describing the precise mismatch. Do not force an analogy that is less clear than the mechanism.
- Include a compact **What it is / What it is not** table when a neighboring concept is easily confused with it. Compare mechanism, learned versus fixed behavior, invariant, failure mode, and appropriate use as applicable.
- Explain what should happen when the running example's inputs or parameters change before presenting equations.

## Details

- Add **Why this was needed** when historical or engineering context improves understanding: the previous bottleneck, the key insight, and the resulting impact. Give roughly one substantive paragraph per part when the history warrants it; verify dates and attribution. Omit unsupported lore.
- State interfaces, representations, assumptions, invariants, and operational details even at math level 0.
- At level 1, include the full formula-and-symbol treatment from the shared math rules, with worked substitution and input/output behavior.
- At level 2, additionally include **Derivation, step by step**, with every nontrivial step justified and a conclusion separating the proved result from remaining assumptions.
- Connect mathematical operations to the running example and a useful interpretation. Include domain-relevant limits and a counterexample to an overgeneralization.
- Optionally include a **Key equations** callout containing 1–3 genuinely central equations only after their notation is defined.
- Cover complexity, numerical behavior, and implementation choices where they are part of understanding the mechanism. Refer to the verification section for measured or executed results.

## Experiment / Worked Example

- State the **Selected verification stack** and **Shared test contract**.
- Normally provide **Implementation 1 — First principles** and **Implementation 2 — Idiomatic usage**. A third stack is optional when it adds a genuinely different perspective, such as autodiff or a database execution model.
- Make the first tier show the mechanics instead of hiding the operation behind the very API being explained. Make the second show realistic usage of the standard facility/library.
- Include setup, complete code, invocation, expected output, execution status, and observed output only when run.
- Trace tensor dimensions at relevant operations; trace low-level allocation, ownership, and lifetime when applicable.
- Test the running example, a changed input, an appropriate valid boundary case, and meaningful invalid input. Cross-check implementations under aligned semantics.
- Explain precision, stability, time/space complexity, and verification limits.
- Add a **Silent bugs & gotchas** callout with specific examples such as unintended broadcasting, integer truncation, wrong axis, aliasing, in-place mutation, overflow, or device/dtype mismatch.

## What I learned

- Give a short synthesis of the mechanism, invariant, applicability, and practical recognition. Do not impersonate the user's completed learning experience.
- Add 5–6 transfer questions, up to 7 when justified, progressing through intuition, quantitative/state trace, parameter synthesis, boundary stress, and a trade-off with another approach.
- Keep the question visible and put each full answer inside `> [!example]- Reveal detailed answer & step-by-step breakdown`. Answers explain the reasoning, not just the result.
- Avoid duplicating the entire separate Practice set. These questions check transfer within this note; the Practice route creates a broader assessment.

## Open Confusion

- Preserve `**Confusion** ::`.
- Record a specific unresolved assumption, evidence gap, ambiguous implementation behavior, or question outside the note's scope. State what would resolve it.
- If no concrete uncertainty is identified, say so neutrally. Do not invent confusion or leave an unexplained placeholder.

## Limitations / Edge Cases

- Cover at least three plausible misconceptions or anti-patterns for a substantive deep note. For each, state the mistaken belief, the actual invariant/condition, a refuting example, and a diagnostic check.
- Include valid edge cases, invalid inputs, numerical problems, operational constraints, and situations where a simpler or different approach is better.
- Make any guarantee's domain explicit. Refer to earlier boundary analysis without repeating the whole derivation.

## Atomize

- Identify only independently useful concepts that deserve their own Atomic notes. Give a one-line reason for each.
- Link existing atomic notes. Keep new candidates plain text unless creation was requested or already included in a bounded plan.
- Do not recursively expand every candidate or create empty files just to satisfy a link quota.

## Connection

- Show where the idea belongs: parent topic, prerequisites, downstream users, and the actual interface between related concepts.
- Include the primary-source/deep-link table with exact claims and inspection status.
- End with a 2–3 sentence bridge explaining what the next topic adds. Link it only when the note exists.
