# Concept authoring checklist (formerly teaching-input contract)

When planning and authoring any note or collection directly in Markdown, ensure every concept covers these elements using [teaching_core.md](../../shared/teaching_core.md) (without creating intermediate JSON builders or helper scripts):

- **Core teaching (`what`, `why`, `how`, `when_use`, `when_not_use`, `apply`):** Establish the learner's problem before naming the method, introduce prerequisites and vocabulary at first need, build a bounded analogy (stating what corresponds to what and where it breaks down), trace a **stable running example** through mechanism and formalism, qualify claims, and test transfer on a second case.
- **Mathematics (`shared/math_gates.md`):** Bridge via **Question → intuition → visual meaning → symbols → formula → calculation → interpretation → check** using native Obsidian `$...$` / `$$...$$` delimiters. Keep main prose understandable with folds closed, and follow every `$$...$$` immediately with `> [!note]- 📐 Understand this formula`.
- **Worked examples:** Problem, given values, target quantity, assumptions, governing formula, explicit intermediate steps, final result, **careful interpretation** (what it measures vs. what it does not establish), sanity check, common mistakes, and generalization.
- **Comparisons:** Causal explanation of *why* methods differ **before** any summary table.
- **Visuals ([representations.md](../workflows/notes-creation/representations.md)):** Plan complementary visuals before drafting, download and inspect local raster assets, and teach every visual via the **six-phase visual narrative** (Set question → Show → Decode → Trace → Connect & limits → Check).
- **Assessments:** Objective-aligned practice progressing from guided to independent, with separate collapsed `> [!hint]- Hint` and `> [!tip]- Answer` callouts.

Manual review checks Markdown structure and reader-facing teaching quality; it does not replace independent human review or live Obsidian UI inspection.
