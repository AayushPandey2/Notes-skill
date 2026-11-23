# M1 — Deep Learning Notes

- **Master ID:** `M1` (`deep_notes` / compatibility route `deepstudy-master`)
- **Primary intent:** `comprehensive_learning` — build complete first-principles understanding from the learner's baseline to requested mastery.
- **Activation signals:** "teach me from scratch", "explain deeply", "comprehensive notes", "from fundamentals to advanced", or bare `/scribe-notes <topic>` without an explicit alternate product format.
- **Non-activation:** Do not select M1 when the user primarily requests a compact cheat sheet (`M3`), solved problem set (`M4`), implementation/build guide (`M5`), quiz/flashcards (`M6`), or standalone comparison/revision pack (`M7`).
- **Load as needed:** [teaching rules](../../../shared/teaching_core.md), [adaptive planning](../../workflows/notes-creation/adaptive-engine.md), [research](../../workflows/research/research-engine.md), [source fidelity](../../workflows/research/source-fidelity.md), [authoring rules](../../../shared/authoring_rules.md), and [math guidance](../../../shared/math_gates.md).
- **Output profile:** Comprehensive collections use the five-key YAML profile in [properties policy](../../metadata/properties-policy.md); single or existing notes use their appropriate Obsidian properties without rewriting user-managed fields.

## Orientation

Give the bounded topic, central question, observable objectives, and learning roadmap. Prepare only prerequisites the learner needs (`assume`, `remind`, `bridge`, `teach`, or `defer`). Apply the appropriate line-1 YAML profile from [properties policy](../../metadata/properties-policy.md); keep planning records outside the finished note.

## Core learning sequence

Order concepts by essential prerequisites, preserving source sequence with local bridges for source-grounded notes. Establish definitions and notation before use. Choose the relevant knowledge-type subtemplate and teaching moves at the depth the learner needs. Mathematics, code, proofs, diagrams, chronology, and experiments remain conditional.

Compose one coherent explanation following [teaching_core.md](../../../shared/teaching_core.md) (Layers A–H and internal stages A–N) with domain-natural headings—never dump equations before orientation/intuition, never pack multiple major concepts into sparse summary bullets (anti-overcompression), and always prepare every governing equation via `M01–M14` math deconstruction ([math_gates.md](../../../shared/math_gates.md)). Give every definition and governing equation one canonical home; align prose, math, visuals, matrix/tensor dimensions, worked `Step 1–12` examples, and code (`P03`). Store visual assets under `assets/scriptorium/<collection-slug>/` following the web-image-first BVIA/LAVIA routing and structured `Explain -> Show -> Decode -> Connect` reading walkthrough ([representations.md](../../workflows/notes-creation/representations.md)). Explain differences between alternatives causally before summary tables, place misconception corrections beside the confusing step (`P06`), put consequential assumptions beside claims, and review against [verification-checklist.md](../../workflows/validation/verification-checklist.md).

## Integration and assessment

Connect concepts through synthesis or cross-topic vault bridges (`P08`) without repeating prior chapters. Verify stated objectives through recall, calculation, derivation, diagnosis, or source interpretation without arbitrary question quotas.

## Revision and further learning

Provide Layer B structured concept review and concise retrieval cues (`P11`) preserving all applicability conditions, plus separately curated further-learning resources ([resource-recommendations.md](../../workflows/research/resource-recommendations.md)) when helpful. Use [footer_widgets.md](../../../shared/footer_widgets.md) only for active vault workflows.

## Quality & validation gate

Review ARRIE source coverage/citations, pedagogical quality, formula folds, and local visual embeds against [verification-checklist.md](../../workflows/validation/verification-checklist.md) before finishing. Repair the smallest affected region rather than regenerating the entire note.

**Activation examples:** Domain-independent comprehensive learning requests (e.g., first-principles derivations with code, visual analysis, or systematic conceptual foundations).  
**Non-M1 examples:** Compact cheat sheets -> `M3`; solved problem sets -> `M4`; pure implementation guides -> `M5`; comparisons/revision packs -> `M7`.

## Comprehensive composition profile

For comprehensive M1 layout, metadata and publication, follow the [canonical composition contract](../../workflows/notes-creation/composition-contract.md).
