# Command Playbooks

## Purpose & Progressive Loading Rule

Dispatch each active public command or `/scribe-notes` internal branch cleanly—load only the single active branch alongside [router](../../../router.md) and [authoring_rules.md](../../../core/authoring_rules.md).

## Playbook Matrix (Trigger -> Inputs -> Execution -> Output & Validation)

### Command A

- **Role:** `/scribe-doubt` — Read-only vault Q&A.
- **Trigger:** `/scribe-doubt <question>` or read-only lookup on existing vault notes.
- **Inputs & Dependencies:** Vault path, question, native file search/read tools.
- **Execution & Output:** Discover and read only matching vault notes; answer with exact `[[Note Title]]` / `[[Note Title#Heading]]` citations.
- **Failure / Constraints:** Perform zero edits and zero external web research; state missing vault coverage honestly.

### Command B — Expand Existing Vault Topic (`/scribe-notes`)
- **Trigger:** Adding subtopics or filling gaps inside an existing vault topic directory.
- **Execution:** Inspect existing vault notes and match the dominant style. Plan any index or syllabus updates as part of the incremental revision. Publish accepted changes together where possible, preserving existing layouts and custom YAML.

### Command C — Comprehensive Learning (`M1` Deep Notes)
- **Trigger:** Broad or first-principles deep-learning requests routed to `M1`.
- **Inputs & Dependencies:** [adaptive-engine.md](adaptive-engine.md), [research-engine.md](../sourcing/research-engine.md), [teaching_core.md](../../../core/teaching_core.md), [math_gates.md](../../../core/math_gates.md).
- **Execution & Review:** Plan concepts and depth, inspect evidence using [research guidance](../sourcing/research-engine.md), connect mathematical milestones and verify derivations, work examples step by step, complete needed visuals through [representations.md](representations.md), generate the artifacts dictated by `artifact_policy` in [master-registry.yaml](../../dispatch/master-registry.yaml), and review saved Markdown and assets with [the manual checklist](../review/verification-checklist.md). Keep internal planning labels out of the note.

### Command D — Rapid Reference (`M3` Quick Reference / Variants)
- **Trigger:** Cheat sheet, formula sheet, syntax table, or CLI command reference requests.
- **Execution:** Distill verified definitions, formulas with units and conditions, choice cues, and pitfalls from permitted sources. Follow the selected M3 density target.

### Command E — Source-Faithful Ingestion (`M2` / `lecture_order`)
- **Trigger:** PDF, slide deck, URL, or raw source notes with sequence/terminology preservation.
- **Execution & Failure:** Extract source segments directly, verify uncertain formulas against source passages, preserve sequence via local `[Educational Addition — Prerequisite Bridge]` inserts instead of silent reordering, and label inaccessible spans explicitly without inventing missing pages.

### Command F — Trade-Off Comparison (`M7` / `comparison_guide`)
- **Trigger:** Explicit multi-option comparison or "X vs Y" request.
- **Execution:** Resolve targets, explain causal divergences before tables under equivalent workloads/assumptions, prove trade-offs on a shared example, and state crossover regimes.

### Command G — Interactive Vault Quiz (`/scribe-quiz`)
- **Trigger:** `/scribe-quiz <topic/note>` or interactive recall/viva over existing vault notes (for static Markdown practice files, use `/scribe-notes` with `M6` [assessment.md](../../blueprints/formats/assessment.md) instead).
- **Execution & Delegation:** [skills/scribe-quiz/SKILL.md](../../../skills/scribe-quiz/SKILL.md) is the canonical owner of the read-only 7-step interactive progression (including `note_conflict` classification, misconception uncertainty, one-question-per-turn pacing, zero web browsing, and no YAML quiz-state keys). Load [pre-gen-gate.md](pre-gen-gate.md), [mastery-design.md](mastery-design.md), and [revision-strategy.md](../learning/revision-strategy.md) alongside it.
- **Failure Handling:** State missing vault/note coverage honestly rather than inventing answers.

### Command J — Read-Only Vault Quality Audit (`/scribe-audit`)
- **Trigger:** `/scribe-audit <note/folder>` or explicit quality review of existing vault notes without immediate rewrites.
- **Execution & Delegation:** Delegate to [skills/scribe-audit/SKILL.md](../../../skills/scribe-audit/SKILL.md) as the canonical read-only audit workflow, inspecting across the 9 audit dimensions (theory, mathematics, prerequisites, practical work, evidence, presentation, consistency, currency, and mastery) using [adversarial-theory-review.md](../review/adversarial-theory-review.md), [educational-editor.md](../review/educational-editor.md), [verification-checklist.md](../review/verification-checklist.md), and [claim-verification.md](../sourcing/claim-verification.md).
- **Failure / Constraints:** Remain strictly read-only by default, cite exact `[[Note Title#Heading]]` locators, and never claim unperformed code execution or live Obsidian rendering.

### Command H — Atomic Card (`M3` / `atomic_card`)
- **Trigger:** A transcludable reference for one concept, typically under 150 words.
- **Execution:** Fetch a source only when the active source policy permits it. Write one focused definition, micro-example, and boundary sentence; resolve existing wikilinks and keep pending concepts as plain text.

### Command I — Multi-Note Curriculum (`M2` Collection Series)
- **Trigger:** Structured multi-note curriculum without single-unit lock.
- **Execution:** Let the source's real sub-branches determine child-note count (no artificial chapter quotas) plus MOC index, preserve source terminology/order, label additions per `source_policy`, follow `artifact_policy` in [master-registry.yaml](../../dispatch/master-registry.yaml) for companions (none for the MOC), and apply `core/math_gates.md` whenever quantitative material appears.

### Command V — Video-Grounded Notes (`/scribe-ytnotes` / `/scribe-notes`)
- **Trigger:** Video URL, lecture recording, transcript, or explicitly requested playlist (`/scribe-ytnotes`).
- **Execution & Validation:** Delegate to [video-notes.md](../../blueprints/formats/video-notes.md) as the single authority (transcript-first, conditional web visuals, staged drafting for long transcripts, and honest disclosure of un-narrated visual content; never play video or capture frames).
