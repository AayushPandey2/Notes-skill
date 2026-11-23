# Command Playbooks

## Purpose & Progressive Loading Rule

Dispatch each active public command or `/scribe-notes` internal branch cleanly—load only the single active branch alongside [router](../../../router.md) and [authoring_rules.md](../../../shared/authoring_rules.md).

## Playbook Matrix (Trigger -> Inputs -> Execution -> Output & Validation)

### Command A

- **Role:** `/scribe-doubt` — Read-only vault Q&A.
- **Trigger:** `/scribe-doubt <question>` or read-only lookup on existing vault notes.
- **Inputs & Dependencies:** Vault path, question, native file search/read tools.
- **Execution & Output:** Discover and read only matching vault notes; answer with exact `[[Note Title]]` / `[[Note Title#Heading]]` citations.
- **Failure / Constraints:** Perform zero edits and zero external web research; state missing vault coverage honestly.

### Command B — Expand Existing Vault Topic (`/scribe-notes`)
- **Trigger:** Adding subtopics or filling gaps inside an existing vault topic directory.
- **Execution:** Inspect existing vault notes directly, match dominant style (or clarify when mixed), update the index/syllabus allowlist first, reconcile existing notes non-destructively, and verify metadata without overwriting custom YAML.

### Command C — Comprehensive Learning (`M1` Deep Notes)
- **Trigger:** Broad or first-principles deep-learning requests routed to `M1`.
- **Inputs & Dependencies:** [adaptive-engine.md](adaptive-engine.md), [research-engine.md](../research/research-engine.md), [teaching_core.md](../../../shared/teaching_core.md), [math_gates.md](../../../shared/math_gates.md).
- **Execution & Review:** Plan concepts and depth, inspect evidence using [research guidance](../research/research-engine.md), explain each displayed equation, work examples step by step, acquire only needed inspected visuals, and review the actual Markdown with [the manual checklist](../validation/verification-checklist.md). Keep internal planning labels out of the note.

### Command D — Rapid Reference (`M3` Quick Reference / Variants)
- **Trigger:** Cheat sheet, formula sheet, syntax table, or CLI command reference requests.
- **Execution:** Distill verified definitions, formulas with units/conditions, choice cues, and high-signal pitfalls from sibling notes or bounded authorities while enforcing `M3` density caps.

### Command E — Source-Faithful Ingestion (`M2` / `lecture_order`)
- **Trigger:** PDF, slide deck, URL, or raw source notes with sequence/terminology preservation.
- **Execution & Failure:** Extract source segments directly, verify uncertain formulas against source passages, preserve sequence via local `[Educational Addition — Prerequisite Bridge]` inserts instead of silent reordering, and label inaccessible spans explicitly without inventing missing pages.

### Command F — Trade-Off Comparison (`M7` / `comparison_guide`)
- **Trigger:** Explicit multi-option comparison or "X vs Y" request.
- **Execution:** Resolve targets, explain causal divergences before tables under equivalent workloads/assumptions, prove trade-offs on a shared example, and state crossover regimes.

### Command G

- **Role:** `/scribe-quiz` — Interactive active recall.
- **Trigger:** `/scribe-quiz <topic/note>` over existing vault notes (`M6`).
- **Execution & Constraints:** Ask **one question per turn**, wait for the user reply, and grade strictly against existing note content. Save weak spots in an existing body review section only when the learner asks for a saved record; never add YAML keys for quiz state.

### Command H — Atomic Card (`M3` / `atomic_card`)
- **Trigger:** Single-concept transcludable note (`<150` words).
- **Execution:** Fetch a source only when the active source policy permits it. Write one focused definition, micro-example, and boundary sentence; resolve existing wikilinks and keep pending concepts as plain text.

### Command I — Multi-Note Curriculum (`M2` Collection Series)
- **Trigger:** Structured multi-note curriculum without single-unit lock.
- **Execution:** Decompose into `4–10+` numbered child notes (minimum `3` + MOC index), preserve source terminology/order, label additions, and apply `shared/math_gates.md` (`M01`–`M14`) whenever quantitative material appears.

### Command V — Unified Video & Lecture Ingestion (`/scribe-ytnote` -> `/scribe-notes`)
- **Trigger:** Video URL, lecture recording, transcript, or candidate video frames (`/scribe-ytnote`, `/scribe-ytnotes`, `/scribe-ytlecture`).
- **Execution & Validation:** State tool/media availability honestly, declare explicit `access_state` (`full_multimodal`, `transcript_plus_frames`, `transcript_only`, `media_only`, `metadata_only`), segment transcript chronologically, keep only clear inspected stills under `assets/scriptorium/<slug>/`, explain prose + formulas via `shared/teaching_core.md` + `shared/math_gates.md`, and degrade honestly on unavailable transcripts/frames.
