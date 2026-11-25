# Shared Canonical Teaching Core

## Purpose

Establish one domain-independent theory-authoring architecture across substantive Scriptorium outputs (`M1`, `M2`, `M4`, `M5`, `M7`, and video notes) so explanations develop understanding **gradually** rather than compressing dense technical material into a polished outline. Compact `M3` cheat sheets and question-only `M6` assessments follow their own density contracts while preserving symbol accuracy and assumptions.

## Diagnosing Teaching Gaps & One Burden at a Time

Before drafting each major concept, diagnose the gap: identify (1) what the reader currently understands, (2) what the next paragraph assumes, and (3) the missing explanation connecting them. Add the missing reasoning—never another generic introduction or more jargon.

- **One conceptual burden at a time:** Never introduce several unfamiliar abstractions simultaneously in a beginner-facing opening (e.g., introduce outcome → known examples → combined score → probability → separate threshold rule before naming log-odds, likelihood, convexity, or calibration). Never stuff advanced claims into an opening callout merely to make a paragraph look shorter.
- **Definition teaching structure:** Selectively fulfill five responsibilities in natural prose (not five compulsory headings): establish the need → state a short, accurate definition → translate it into ordinary language → demonstrate with one concrete example beside it → establish the nearest boundary. Bold only the term being defined; use short non-collapsed definition callouts sparingly so the note reads as connected explanation, not a stack of boxes. Separate definition, consequence, assumption, and optional advanced property rather than combining them into one sentence.
- **Comparison tables follow explanation:** Teach the compared ideas first; never make a dense comparison table the reader's first encounter with unfamiliar concepts.

## Visual Identity, Headings & Reading Path

- **Separated opening metadata & clickable TOC:** Place blank lines between `Difficulty`, `Prerequisites`, and `Learning objectives` blocks so renderers never merge them into one paragraph, followed by a compact **clickable Obsidian Table of Contents** (`- [[#1. Heading|Short Label]]`).
- **Fewer, question-driven headings:** Prefer headings that reflect real learning questions (*"Why do we need a probability instead of a raw score?"*, *"What does the sigmoid change?"*, *"Why does the gradient contain prediction minus label?"*) developed through explanation, example, and interpretation—never 1-sentence micro-sections, bold pseudo-headings, or identical headings forced across unrelated domains.
- **Spacing, no highlighting & purposeful callouts:** Keep paragraphs to 1–3 concise sentences, put blank lines between complex list items, and reserve `---` for major thematic transitions. Do **not** use `==highlight==`, semantic highlight spans, or `\color{...}` anywhere. Keep the central argument visible in prose, and reserve collapsed blocks for detailed formula breakdowns (`> [!example]- Understand this formula step by step`), extended derivations, prerequisite refreshers, additional calculations, and checkpoint answers (`> [!question]` visible with nested `> > [!success]- Reveal Answer`). Never treat bare displayed formulas as compliant merely because their symbols appear in a trailing notation table.

## Tone, Precision & Accuracy Discipline

Write calm, direct reference prose free of scripted filler (`"We now..."`, `"Let us..."`, `"Notice how..."`, `"Inspect Figure..."`) and unedited self-correction transcripts (`"Wait—check the sign carefully!"`). Flag and qualify strong claims—especially guaranteed calibration, existence/uniqueness of an optimum, outlier robustness, solver defaults, regularization scaling, and universal preprocessing—clearly separating helpful simplifications from unconditional truths.

## Progressive Explanation & Consolidated Scope

1. **Motivate every representation:** For any transformation (e.g., probability → odds → log-odds), explain what it expresses, why transform, what changes numerically, what stays invariant, and how it connects to the model before summarizing in a table.
2. **Build multi-step objectives via questions:** Before giving a full likelihood or loss formula, walk through the case-by-case questions (`y = 1` vs `y = 0` → single combined expression → independence product → log preservation → sign flip → averaging) with a tiny numerical probability example.
3. **Interpret mechanisms, not just arithmetic:** In numerical traces, explain *why* initial predictions take their starting values (e.g., `0.5`), what residual signs mean, *why* features multiply residuals, *why* contributions are averaged, *why* subtracting a negative gradient raises a weight, *why* total loss can drop while individual points worsen, and what the next step recomputes—without speculating unestablished future trajectories.
4. **Consolidate before expanding & teach metrics from examples:** Establish core mechanics (e.g., binary classification, loss, updates) before multiclass or advanced extensions; label brief orientations honestly and never drop a complex equation (like softmax) in one paragraph and call it self-contained. Teach evaluation metrics from concrete actual vs. predicted counts (TP/FP/TN/FN first), stating each metric's question, counts, calculation, interpretation, and limitation before any summary table, and never conflating probability quality, calibration, discrimination, and accuracy.
5. **Closing & Companion Handoff:** End with a concise **Mental Model**, trailing **Notation Reference** (revision aid only—essential notation must be defined locally first), and reciprocal links to `<note stem> - Experimental Lab.md` and `<note stem> - Cheatsheet & Interview Q&A.md`.
