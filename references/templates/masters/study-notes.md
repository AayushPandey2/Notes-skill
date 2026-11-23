---
id: "<topic-slug>-<subtopic-number>"
aliases: []
topic: "<Topic or source title>"
tags: []
nexttopics: []
---

<!-- scaffold:preflight
Purpose: Generate source-aligned or syllabus-aligned sequential study notes faithfully preserving source order, terminology, and local prerequisite bridges.
Master ID: M2 (study_notes / compatibility route: studynotes).
Activation Trigger: /scribe-notes with supplied lecture, PDF, transcript, or structured study request ("notes from this lecture/PDF", "preserve chapter order", "study notes").
Non-activation: Deep first-principles reorganization without source order -> M1; compact cheat sheet -> M3; problem set -> M4; build guide -> M5; quiz -> M6; revision pack -> M7.
Variants: lecture-order.md.
Inputs: Verified source sections/transcript/syllabus, access scope status, target depth, math_level 0–2.
Dependencies: shared/teaching_core.md, shared/authoring_rules.md, shared/math_gates.md, workflows/notes-creation/adaptive-engine.md, workflows/research/source-fidelity.md.
Decision Rules: Preserve verified source sequence; place Foundation Bridges & M01–M14 formula+folds directly before dependent notation; merge redundant sections cleanly without fabricating missing pages.
Failure Handling: Label partial access explicitly and mark unsupported claims [UNVERIFIED]; omit unused optional templates before publishing.
Validation: [verification-checklist.md](../../workflows/validation/verification-checklist.md) (`M2` study-notes rules).
-->

# <Topic / Source Title>

## 1. What am I studying, and what should I be able to do? (Source Context & Learning Goals)

> [!info] Source & Scope Context
> - **Domain / Subject**: <Field>
> - **Module / Section**: <Relevant chapter or segment, when available>
> - **Primary Source(s)**: <Title and verified page, section, timestamp, or link>
> - **Access & Scope**: <What was accessible, what is covered, and any material gaps>

**Sequential Topic Outline**

1. <First idea in verified source or study order>
2. <Next idea>

**By the end of this note, I should be able to**

- <Observable explanation, calculation, distinction, or application outcome.>

## 2. How does the material develop each idea? (Sequential Concepts & Explanations)

Repeat `### 2.<k> <Subtopic Title>` in verified source order, inserting concise `[Educational Addition — Prerequisite Bridge]` explanations inline right before dependent notation rather than silently reordering the source:

- **Core Statement / Source Point** — <What the source establishes, with locator.>
- **In Simple Words** — <Beginner-clear intuitive explanation preserving meaning.>
- **Why This Matters** — <Purpose, consequence, or link to prior idea.>
- **Key Terms & Symbols** — <Define terms, units, shapes, and domain restrictions.>
- **Formal Relation & Step-by-Step Breakdown** — <Follow [math_gates.md](../../../shared/math_gates.md): intuition first, then `$$...$$` + `> [!example]- Understand this formula step by step`.>
- **Illustrative Example** — <Setup/Given -> Step-by-Step Working -> Result/Interpretation (keep interleaved right beside the concept it teaches).>
- **Quick Check** — <One focused prediction or mechanism check.>

## 3. How do I carry out the method or solve a problem? (Procedures, Reasoning & Worked Problems)

Merge into Section 2 when procedures appear inline in the source; otherwise document reusable procedures (`Starting Point -> Steps with Reasons -> Result & Applicability`) and `Step 1`–`12` worked problems with explicit dimensional/unit sanity checks and recognition cues.

## 4. Which rule or approach applies here? (Rules, Definitions & Reference Matrix)

Omit when inline explanation suffices; otherwise map:
`Rule / Definition / Formula | Symbol Meanings | Conditions for Use | Notes / Units / Caveats`
Followed by **How to Choose the Right Rule or Approach** (naming distinguishing criteria before selecting).

## 5. What needs clarification, and where are the limits? (Questions, Confusions & Caveats)

Keep only genuine edge cases, source attributions preceding corrections, `[UNVERIFIED]` / `[NEEDS CLARIFICATION]` notices, and real open confusions (`**Confusion** :: ...`).

## 6. What can I recall, explain, and apply? (Key Takeaways & Active Recall)

- **Key Takeaways** & **Common Mistake to Avoid** (`Mistake -> why it fails -> how to prevent it`).
- **Self-Check Questions** (Recall, Causal Explanation, Application) + **Answers / Hints** matched to objectives.
- **Next Topic Connection** pointing into `nexttopics`.

<!-- Contract Summary: Apply [authoring_rules.md](../../../shared/authoring_rules.md), [math_gates.md](../../../shared/math_gates.md), and [footer_widgets.md](../../../shared/footer_widgets.md). Remove unused scaffolding before saving. -->
