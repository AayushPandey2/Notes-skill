# Format Blueprint: M2 — Study Notes (Source-Anchored)

*Master ID: `M2` (`study_notes`, variant: `lecture-order.md`). Default artifact policy: `theory_bundle` per [master-registry.yaml](../../dispatch/master-registry.yaml). Use line-1 Standard Obsidian Properties YAML (`topic`, `tags`, `master_topic`, `domain`, `note_type: study-notes`) per [properties-policy.md](../../properties/properties-policy.md).*

# <Topic / Source Title>

## 1. Source Context & Learning Goals

Open with concise separated metadata lines (not a crowded opening box):
- **Primary Source(s):** <Title and verified page, section, timestamp, or link>
- **Access & Scope:** <What was accessible, covered boundaries, and any material gaps>
- **Learning Outcomes & Sequential Outline:** <Ordered sequence of ideas in verified source order>

## 2. Core Material in Source Order

Reconstruct every significant accessible source section in verified source order (`### 2.<k> <Subtopic Title>`) adapted to the actual discipline:
- Use the [source policy](../../procedures/sourcing/source-fidelity.md) to distinguish attributed paraphrase, reasoning supported by the source, and permitted additions.
- **Examples, figures & equations:** Keep important source examples beside the concepts they support; decode source figures (or permitted supplementary visuals) via [representations.md](../../procedures/authoring/representations.md); organize substantive equations into reasoning units with visible milestones and descriptive derivation folds where warranted ([math_gates.md](../../../core/math_gates.md)).
- **Separate source claims from corrections & local misconceptions:** Preserve original claims with locators (`page`/`section`/`timestamp`) and present permitted evidence-based corrections separately alongside inline misconception notes.

## 3. Integrated Procedures & Worked Examples

Merge into Section 2 when procedures appear inline; otherwise document reusable procedures (`Starting Point -> Steps with Reasons -> Result & Applicability`) and domain-appropriate worked examples with independent checks.

## 4. Quick Reference Matrix

Omit when inline explanation suffices; otherwise map:
`Rule / Definition / Formula | Meanings | Conditions for Use | Notes / Units / Caveats`

## 5. Source Coverage Audit & Unresolved Gaps *(Proportional to Source Length)*

Keep proportional to the source (concise note for short lectures; section-level audit for long PDFs/textbooks): track accessible vs. inaccessible/unreadable sections, missing prerequisites under `strict` mode, `[UNVERIFIED]` / `[NEEDS CLARIFICATION]` notices, and any open questions or confusions in ordinary Markdown prose (avoiding default Dataview inline syntax).

## 6. Synthesis & Active Recall

- **Conceptual Synthesis & Common Mistake to Avoid** (`Mistake -> why it fails -> how to prevent it`).
- Use source-aligned self-check questions and answers or hints when permitted by the source policy and suitable for the objectives.
- **Next Topic Connection** explaining *why* the next topic in `nexttopics` matters.

*Contract: [authoring_rules.md](../../../core/authoring_rules.md), [math_gates.md](../../../core/math_gates.md), [footer_widgets.md](../../../core/footer_widgets.md), [verification-checklist.md](../../procedures/review/verification-checklist.md).*
