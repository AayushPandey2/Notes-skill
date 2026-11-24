# Concept authoring checklist (formerly teaching-input contract)

When planning and authoring any note or collection directly in Markdown, ensure every concept covers these elements using [teaching_core.md](../../core/teaching_core.md) (without creating intermediate JSON builders or helper scripts):

- **Core teaching (`what`, `why`, `how`, `when_use`, `when_not_use`, `apply`):** Realize the 12 teaching layers in [teaching_core.md](../../core/teaching_core.md): enforce the 3-tier prerequisite rule (explain essential terms locally, bridge secondary ones, bound outside topics), unpack definitions in natural prose with positive/non-example/boundary cases, use connective-tissue patterns rather than disconnected lists, carry one **stable running example** across mechanism and formalism, and test transfer on a second case.
- **Mathematics (`core/math_gates.md`):** Bridge via **Question → intuition → visual meaning → symbols → formula → calculation → interpretation → check** using native Obsidian `$...$` / `$$...$$` delimiters. Keep main prose understandable with folds closed, and follow every `$$...$$` immediately with `> [!note]- 📐 Understand this formula`.
- **Worked examples:** Problem, given values, target quantity, assumptions, governing formula, explicit intermediate steps, final result, **careful interpretation** (what it measures vs. what it does not establish), sanity check, common mistakes, and generalization.
- **Comparisons:** Causal explanation of *why* methods differ **before** any summary table.
- **Visuals ([representations.md](../procedures/authoring/representations.md)):** Plan complementary visuals before drafting, download and inspect local raster assets, and teach every visual via the **six-phase visual narrative** (Set question → Show → Decode → Trace → Connect & limits → Check).
- **Assessments:** Objective-aligned practice progressing from guided to independent, with separate collapsed `> [!hint]- Hint` and `> [!tip]- Answer` callouts.

Manual review checks Markdown structure and reader-facing teaching quality; it does not replace independent human review or live Obsidian UI inspection.
