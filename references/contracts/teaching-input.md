# Concept authoring checklist (formerly teaching-input contract)

When planning and authoring any note or collection directly in Markdown, ensure every concept covers these elements as applicable (without creating intermediate JSON builders or helper scripts):

- **Core teaching (`what`, `why`, `how`, `when_use`, `when_not_use`, `apply`):** Motivating starting problem, intuitive mental model (with analogy limits), prerequisite bridges immediately before use, step-by-step causal mechanism, worked application, selection criteria, limitations/misconceptions, and reinforcement.
- **Mathematics (`shared/math_gates.md`):** Orienting prose before every `$$...$$`, followed immediately by `> [!note]- 📐 Understand this formula` covering applicable 12-stage elements (purpose, components, symbol-by-symbol breakdown with shapes/units, plain reading, prerequisites, numerical walkthrough, visual/parameter intuition, derivation, implementation, limitations, recall).
- **Worked examples (`Step 1`–`12`):** Problem, given values, target quantity, assumptions, governing formula, explicit intermediate steps, result, interpretation, sanity check, common mistakes, and generalization.
- **Comparisons:** Causal explanation of *why* methods differ (suitability, assumptions, mechanism, strengths, limitations) **before** any summary table.
- **Visuals ([representations.md](../workflows/notes-creation/representations.md)):** Use a visual when it clarifies the lesson; check its rights and content with available tools before embedding it locally. Teach through Explain → Show → Decode → Connect, and report unavailable visuals honestly.
- **Assessments:** Objective-aligned questions with separate collapsed `> [!hint]- Hint` and `> [!tip]- Answer` callouts.

Manual review checks Markdown structure and content completeness; it does not replace independent human review or live Obsidian UI inspection.
