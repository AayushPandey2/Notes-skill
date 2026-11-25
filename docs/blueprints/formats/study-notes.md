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

## 2. How does the material develop each idea? (Source-Preserving Educational Reconstruction)

Reconstruct every significant accessible source section in verified source order (`### 2.<k> <Subtopic Title>`) as a **source-preserving educational reconstruction**, adapting explanations to the actual discipline (never forcing ML numerical tables or scalar-to-vector math onto non-quantitative history, programming, or biology):
- **Preserve source sequence & terminology:** Keep the presenter's/author's sequence and terms intact while clarifying ambiguity; insert concise `[Educational Addition — Prerequisite Bridge]` foundations inline right before dependent concepts without silently reordering sections.
- **Reconstruct skipped transitions & preserve examples:** Fill in reasoning steps the presenter skipped, keep important source examples beside the concepts they support, and clearly label any substantial added explanation (`[Educational Addition]`, only when permitted by the active `source_policy`).
- **Handle source figures & equations:** Decode source figures (or clearly labeled supplementary visuals when permitted by `source_policy`) via [representations.md](../../procedures/authoring/representations.md). When equations appear, pair every top-level `$$...$$` with `> [!example]- Understand this formula step by step` ([math_gates.md](../../../core/math_gates.md)).
- **Separate source claims from corrections:** If the source contains an error or outdated convention, preserve the original claim accurately with its locator (`page`/`section`/`timestamp`) and present the evidence-based correction separately.
- **Local misconceptions & depth:** Expand explanations proportionately to conceptual importance and place concise misconception clarifications inline right where confusion arises.

## 3. How do I carry out the method or solve a problem? (Integrated Problem-Solving & Procedures)

Merge into Section 2 when procedures appear inline in the source; otherwise document reusable procedures (`Starting Point -> Steps with Reasons -> Result & Applicability`) and domain-appropriate worked examples with independent verification checks and recognition cues.

## 4. Which rule or approach applies here? (Rules, Definitions & Reference Matrix)

Omit when inline explanation suffices; otherwise map:
`Rule / Definition / Formula | Meanings | Conditions for Use | Notes / Units / Caveats`
Followed by **How to Choose the Right Rule or Approach** (naming distinguishing criteria before selecting).

## 5. Source Coverage Audit, Clarifications & Unresolved Gaps

Maintain an explicit accounting of accessible vs. inaccessible or unreadable source sections, genuine edge cases, source-to-correction separations, `[UNVERIFIED]` / `[NEEDS CLARIFICATION]` notices, and real open confusions (`**Confusion** :: ...`).

## 6. What can I recall, explain, and apply? (Conceptual Synthesis & Active Recall)

- **Final Conceptual Synthesis & Common Mistake to Avoid** (`Mistake -> why it fails -> how to prevent it`).
- **Source-Aligned Retrieval Cues / Self-Check Questions** (Recall, Causal Explanation, Application) + **Answers / Hints** matched to objectives.
- **Next Topic Connection** pointing into `nexttopics`.

<!-- Contract Summary: Apply [authoring_rules.md](../../../core/authoring_rules.md), [math_gates.md](../../../core/math_gates.md), and [footer_widgets.md](../../../core/footer_widgets.md). Remove unused scaffolding before saving. -->
