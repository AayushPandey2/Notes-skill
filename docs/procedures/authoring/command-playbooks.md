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
- **Execution:** Inspect existing vault notes directly, match dominant style (or clarify when mixed), update the index/syllabus allowlist first, reconcile existing notes non-destructively, and verify metadata without overwriting custom YAML.

### Command C — Comprehensive Learning (`M1` Deep Notes)
- **Trigger:** Broad or first-principles deep-learning requests routed to `M1`.
- **Inputs & Dependencies:** [adaptive-engine.md](adaptive-engine.md), [research-engine.md](../sourcing/research-engine.md), [teaching_core.md](../../../core/teaching_core.md), [math_gates.md](../../../core/math_gates.md).
- **Execution & Review:** Plan concepts and depth, inspect evidence using [research guidance](../sourcing/research-engine.md), explain each displayed equation, work examples step by step, complete needed visuals through [representations.md](representations.md), create each new content note's [companion lab](experimental-lab.md), and review saved Markdown and assets with [the manual checklist](../review/verification-checklist.md). Keep internal planning labels out of the note.

### Command D — Rapid Reference (`M3` Quick Reference / Variants)
- **Trigger:** Cheat sheet, formula sheet, syntax table, or CLI command reference requests.
- **Execution:** Distill verified definitions, formulas with units/conditions, choice cues, and high-signal pitfalls from sibling notes or bounded authorities while enforcing `M3` density caps.

### Command E — Source-Faithful Ingestion (`M2` / `lecture_order`)
- **Trigger:** PDF, slide deck, URL, or raw source notes with sequence/terminology preservation.
- **Execution & Failure:** Extract source segments directly, verify uncertain formulas against source passages, preserve sequence via local `[Educational Addition — Prerequisite Bridge]` inserts instead of silent reordering, and label inaccessible spans explicitly without inventing missing pages.

### Command F — Trade-Off Comparison (`M7` / `comparison_guide`)
- **Trigger:** Explicit multi-option comparison or "X vs Y" request.
- **Execution:** Resolve targets, explain causal divergences before tables under equivalent workloads/assumptions, prove trade-offs on a shared example, and state crossover regimes.

### Command G — Interactive Vault Quiz (`/scribe-quiz`)
- **Trigger:** `/scribe-quiz <topic/note>` or interactive recall/viva over existing vault notes (for static Markdown practice files, use `/scribe-notes` with `M6` [assessment.md](../../blueprints/formats/assessment.md) instead).
- **Inputs & Discovery:** Vault path ([pre-gen-gate.md](pre-gen-gate.md)), target note(s), and read-only note inspection (zero web browsing).
- **Execution & Constraints:** Ask **one question per turn**, wait for the learner's reply, grade strictly against existing note content with exact `[[Note Title#Heading]]` citations, escalate difficulty (`recall → application/trace → boundary/viva`), and keep vault notes unchanged by default. Save weak spots in an existing body review section only when explicitly requested; never add YAML keys for quiz state or create an experimental lab.
- **Failure Handling:** State missing vault/note coverage honestly rather than inventing answers.

### Command H — Atomic Card (`M3` / `atomic_card`)
- **Trigger:** Single-concept transcludable note (`<150` words).
- **Execution:** Fetch a source only when the active source policy permits it. Write one focused definition, micro-example, and boundary sentence; resolve existing wikilinks and keep pending concepts as plain text.

### Command I — Multi-Note Curriculum (`M2` Collection Series)
- **Trigger:** Structured multi-note curriculum without single-unit lock.
- **Execution:** Decompose into `4–10+` numbered child notes (minimum `3` + MOC index), preserve source terminology/order, label additions, create [one lab per new content note](experimental-lab.md) but none for the MOC, and apply `core/math_gates.md` whenever quantitative material appears.

### Command V — Video-Grounded Notes (`/scribe-ytnotes` / `/scribe-notes`)
- **Trigger:** Video URL, lecture recording, transcript, or explicitly requested playlist (`/scribe-ytnotes`).
- **Execution & Validation:** Follow [video-notes.md](../../blueprints/formats/video-notes.md) (overrides collection splitting, companion-lab generation, and multi-language lab tracks). Check metadata/transcript access once and acquire the timestamped transcript into one compact evidence map—never play the video or capture video frames. Instead, download and inspect multiple relevant raster web images (`assets/scriptorium/<video-id>/<name>.png`) via [representations.md](representations.md), compose once around those visuals and timestamps, and repair omissions locally.
