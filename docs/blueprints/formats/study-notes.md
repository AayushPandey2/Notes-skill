---
topic: "<Topic or source title>"
tags: []
master_topic: "<Broader conceptual parent>"
domain: "<Field or Discipline>"
note_type: study-notes
---

<!-- scaffold:preflight
Purpose: Generate source-aligned or syllabus-aligned sequential study notes faithfully preserving source order, terminology, and local prerequisite bridges.
Master ID: M2 (study_notes / compatibility route: studynotes).
Activation Trigger: /scribe-notes with supplied lecture, PDF, transcript, or structured study request ("notes from this lecture/PDF", "preserve chapter order", "study notes").
Non-activation: Deep first-principles reorganization without source order -> M1; compact cheat sheet -> M3; problem set -> M4; build guide -> M5; quiz -> M6; revision pack -> M7.
Variants: lecture-order.md.
Inputs: Verified source sections/transcript/syllabus, access scope status, target depth, concept-level math profile (Conceptual through Formal reasoning).
Dependencies: core/teaching_core.md, core/authoring_rules.md, core/math_gates.md, procedures/authoring/adaptive-engine.md, procedures/sourcing/source-fidelity.md.
Decision Rules: Preserve verified source sequence; apply the 3-tier prerequisite rule and progressive teaching flow in core/teaching_core.md inline before dependent notation, and use > [!example]- Understand this formula step by step per core/math_gates.md; merge redundant sections cleanly without fabricating missing pages.
Failure Handling: Label partial access explicitly and mark unsupported claims [UNVERIFIED]; omit unused optional templates before publishing.
Validation: [verification-checklist.md](../../procedures/review/verification-checklist.md) (`M2` study-notes rules).
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

Repeat `### 2.<k> <Subtopic Title>` in verified source order using **short, crisp single-idea paragraphs (1–3 sentences)** separated by tiny concrete tables, explicit symbol disambiguation, and strategic visuals ([teaching_core.md](../../../core/teaching_core.md)):
- Open each unfamiliar subtopic with a concrete tiny table or numerical scenario before defining abstract terms, and insert concise `[Educational Addition — Prerequisite Bridge]` foundations (value tables, rules, or symbol-clash notes) inline right before dependent notation.
- Progress from **simple scalar case → multi-component sum/table → general compact form** whenever equations appear; break core formulas into parts (`Part | Purpose`), test negative/zero/positive/limit cases, pair every top-level displayed `$$...$$` with `> [!example]- Understand this formula step by step`, and decode needed visuals via [representations.md](../../procedures/authoring/representations.md) (respecting source-only limits).
- Include explicit **"Why simpler approach X fails here"** and **"What this does NOT assume"** clarifications where misconceptions arise, plus a worked example with intermediate arithmetic and a focused check.

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

<!-- Contract Summary: Apply [authoring_rules.md](../../../core/authoring_rules.md), [math_gates.md](../../../core/math_gates.md), and [footer_widgets.md](../../../core/footer_widgets.md). Remove unused scaffolding before saving. -->
