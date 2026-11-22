# Command Playbooks

## Purpose & Progressive Loading Rule

Dispatch each active public command or `/scribe-notes` internal branch cleanly—load only the single active branch alongside [router](../../../router.md) and [authoring_rules.md](../../../shared/authoring_rules.md).

## Playbook Matrix (Trigger -> Inputs -> Execution -> Output & Validation)

### Command A

- **Role:** `/scribe-doubt` — Read-only vault Q&A.
- **Trigger:** `/scribe-doubt <question>` or read-only lookup on existing vault notes.
- **Inputs & Dependencies:** Vault path, question, `scripts/vault_index.py`.
- **Execution & Output:** Discover and read only matching vault notes; answer with exact `[[Note Title]]` / `[[Note Title#Heading]]` citations.
- **Failure / Constraints:** Perform zero edits and zero external web research; state missing vault coverage honestly.

### Command B — Expand Existing Vault Topic (`/scribe-notes`)
- **Trigger:** Adding subtopics or filling gaps inside an existing vault topic directory.
- **Execution:** Run `vault_index.py --discover`, inspect `detected_workflow` (`"deep-notes"`, `"study-notes"`, `"mixed"`, or `null`), match dominant style (or clarify when mixed), update the index/syllabus allowlist first, reconcile existing notes non-destructively, and run `scripts/patch_links.py --dry-run` for metadata updates.

### Command C — Comprehensive Learning (`M1` Deep Notes)
- **Trigger:** Broad or first-principles deep-learning requests routed to `M1`.
- **Inputs & Dependencies:** [adaptive-engine.md](adaptive-engine.md), [research-engine.md](../research/research-engine.md), [teaching_core.md](../../../shared/teaching_core.md), [math_gates.md](../../../shared/math_gates.md).
- **Execution & Validation:** Plan concepts and depths (`0–5`), verify evidence via ARRIE (`research_package`), embed atomic formula+folds beneath every displayed `$$...$$`, execute `Step 1`–`12` worked examples, acquire raster web visuals via BVIA/LAVIA, verify 12-dimension teaching quality (`QualityEngine.evaluate_teaching()`), and strip internal module labels.

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
- **Execution & Constraints:** Ask **one question per turn**, wait for the user reply, grade strictly against existing note content, and log weak spots only in body review fields via `scripts/patch_links.py` (never inject extra YAML keys).

### Command H — Atomic Card (`M3` / `atomic_card`)
- **Trigger:** Single-concept transcludable note (`<150` words).
- **Execution:** Perform one bounded direct fetch if needed, write one focused definition + micro-example + boundary sentence, resolve existing wikilinks cleanly, and keep pending concepts as plain text.

### Command I — Multi-Note Curriculum (`M2` Collection Series)
- **Trigger:** Structured multi-note curriculum without single-unit lock.
- **Execution:** Decompose into `4–10+` numbered child notes (minimum `3` + MOC index), preserve source terminology/order, label additions, and apply `shared/math_gates.md` (`M01`–`M14`) whenever quantitative material appears.

### Command V — Unified Video & Lecture Ingestion (`/scribe-ytnote` -> `/scribe-notes`)
- **Trigger:** Video URL, lecture recording, timestamped transcript JSON, or candidate video frames (`VIDEO-01`–`VIDEO-04`, `scripts/scribe.py ytnote`; compatible aliases `ytnotes` and `ytlecture` remain supported).
- **Execution & Validation:** Check tool availability honestly (`yt-dlp`, `ffmpeg`, captions), declare explicit `access_state` (`full_multimodal`, `transcript_plus_frames`, `transcript_only`, `media_only`, `metadata_only`), segment transcript chronologically, screen frames via `composition/video.py` to keep readable derivation/diagram stills under `assets/scriptorium/<slug>/`, explain prose + formulas via `shared/teaching_core.md` + `shared/math_gates.md`, and degrade honestly on unavailable transcripts/frames.
