---
topic: "<Topic or source title>"
tags: []
master_topic: "<Broader conceptual parent>"
domain: "<Field or Discipline>"
note_type: study-notes
---

# <Topic / Source Title>

*Master ID: `M2` (`study_notes`, variant: `lecture-order.md`). Default artifact policy: `theory_bundle` per [master-registry.yaml](../../dispatch/master-registry.yaml).*

## 1. What am I studying, and what should I be able to do? (Source Context & Learning Goals)

> [!info] Source & Scope Context
> - **Domain / Subject**: <Field>
> - **Module / Section**: <Relevant chapter or segment, when available>
> - **Primary Source(s)**: <Title and verified page, section, timestamp, or link>
> - **Access & Scope**: <What was accessible, what is covered, and any material gaps>

**Sequential Topic Outline & Learning Outcomes**

1. <First idea in verified source or study order>
2. <Next idea>

## 2. How does the material develop each idea? (Source-Preserving Educational Reconstruction)

Reconstruct every significant accessible source section in verified source order (`### 2.<k> <Subtopic Title>`) adapted to the actual discipline:
- **Distinguish three levels of reconstruction** per [source-fidelity.md](../../procedures/sourcing/source-fidelity.md):
  1. *Source-faithful paraphrase:* Explain what the supplied material establishes in its terminology and order.
  2. *Source-supported reasoning:* Unpack skipped transitions using information already present in the supplied source.
  3. *External educational addition:* Add outside prerequisite bridges or context **only when `source_policy` permits** (labeled `[Educational Addition]`). Under `strict` source mode, an essential missing prerequisite becomes an **explicitly identified gap** rather than an outside insertion.
- **Examples, figures & equations:** Keep important source examples beside the concepts they support; decode source figures (or permitted supplementary visuals) via [representations.md](../../procedures/authoring/representations.md); pair coherent top-level `$$...$$` equations with `> [!example]- Understand this formula step by step` ([math_gates.md](../../../core/math_gates.md)).
- **Separate source claims from corrections & local misconceptions:** Preserve original claims with locators (`page`/`section`/`timestamp`) and present permitted evidence-based corrections separately alongside inline misconception notes.

## 3. How do I carry out the method or solve a problem? (Integrated Procedures & Worked Examples)

Merge into Section 2 when procedures appear inline; otherwise document reusable procedures (`Starting Point -> Steps with Reasons -> Result & Applicability`) and domain-appropriate worked examples with independent checks.

## 4. Which rule or approach applies here? (Reference Matrix)

Omit when inline explanation suffices; otherwise map:
`Rule / Definition / Formula | Meanings | Conditions for Use | Notes / Units / Caveats`

## 5. Source Coverage Audit & Unresolved Gaps *(Proportional to Source Length)*

Keep proportional to the source (concise note for short lectures; section-level audit for long PDFs/textbooks): track accessible vs. inaccessible/unreadable sections, missing prerequisites under `strict` mode, `[UNVERIFIED]` / `[NEEDS CLARIFICATION]` notices, and real open confusions (`**Confusion** :: ...`).

## 6. What can I recall, explain, and apply? (Synthesis & Active Recall)

- **Conceptual Synthesis & Common Mistake to Avoid** (`Mistake -> why it fails -> how to prevent it`).
- **Source-Aligned Self-Check Questions** (Recall, Causal Explanation, Application) + **Answers / Hints** matched to objectives.
- **Next Topic Connection** explaining *why* the next topic in `nexttopics` matters.

*Contract: [authoring_rules.md](../../../core/authoring_rules.md), [math_gates.md](../../../core/math_gates.md), [footer_widgets.md](../../../core/footer_widgets.md), [verification-checklist.md](../../procedures/review/verification-checklist.md).*
