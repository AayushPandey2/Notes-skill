---
name: scribe-notes
description: Universal adaptive note-creation command. Interactively calibrates note style (M1-M7), depth, scope (single note vs. hierarchical multi-note collection), and Obsidian Properties before generating verified study notes.
---

# `/scribe-notes` — Universal Adaptive Notes Command

`/scribe-notes` is the **sole public note-creation command** in Scriptorium. All note styles (`M1` Deep Learning Notes, `M2` Structured Study Notes, `M3` Quick Reference / Cheat Sheet / Formula Sheet / Atomic Card, `M4` Worked Problems & Solutions, `M5` Implementation & Technical Guide, `M6` Practice & Assessment / Flashcards, `M7` Synthesis / Comparison / Concept Map / Paper Breakdown) are routed internally through `/scribe-notes`.

> **Non-note commands preserved separately:** `/scribe-doubt` (read-only vault Q&A), `/scribe-quiz` (interactive active-recall quizzing), `/scribe-setfolder` (vault target configuration).

## Comprehensive topic collections

For full-topic M1 notes, follow [the composition contract](../../references/workflows/notes-creation/composition-contract.md). After scope calibration, supply a shared concept plan and subject-specific allocation of 5–10 chapters (or omit chapters for adaptive planning) to `notes compose`. Author and verify complete chapters before publication. This profile uses exactly `id`, `aliases`, `topic`, `tags`, `nexttopics`; internal metadata stays in manifests. The legacy grouped-file preview below is a provisional concept inventory. `notes generate --legacy-layout` is available for existing nested collections. Other masters and explicitly narrow single notes retain the workflow below.

For comprehensive composition, the [KCP integrity contract](../../references/contracts/composition-integrity.md) owns obligation states, technical records, exact source evidence, renderer execution and assessment coverage. Run `notes compose --prepare` before reviewing; use its prepared chapter bodies for structured review hashes. `--context` compiles active-concept instructions, `--repair` lists affected dependents, and `--validate` rechecks published artifacts without writing. Record unavailable host checks explicitly.

## Legacy and single-note execution contract

1. **Always start with the Interactive Configuration Gate (before generating final notes):**
   - Inspect the request via `python scripts/scribe.py notes start "<request>" --vault "<vault>"` (or `OrchestrationEngine.start_notes_session()`).
   - If the user invoked bare `/scribe-notes` with no topic, ask first what topic, source, or learning goal they want notes on.
   - Infer provisional recommendations for **master template (`M1`–`M7`)**, **variant**, **depth**, **scope tier (`S0`–`S5`)**, and **organization (`single_note` vs. `hierarchical_collection`)**.
   - Ask only the **adaptive, unanswered** plain-text configuration questions (typically 1–4 concise questions; skip any preference already explicitly stated in the user's request, or honor `"skip questions"` / `"use your recommendations"`).
   - Present the inferred recommendation clearly alongside a zero-friction default (`Reply "use your recommendations" to proceed`).
2. **Accept Natural Follow-Up Replies Without Repeating `/scribe-notes`:**
   - Process free-text answers, numbered/lettered replies (`1b, 2a`), partial answers, mid-flow corrections (`"actually make it a cheat sheet"`), outline edits (`"remove CNNs and add Bayesian Inference"`), or cancellation (`"cancel"`) via `python scripts/scribe.py notes respond --vault "<vault>" --session-id "<id>" --reply "<reply>"`.
3. **Preview Substantial Hierarchical Collections Before Generation:**
   - For broad topics (`S3`–`S5`, or `hierarchical_collection` with > 3 notes), show the proposed **Parent Map of Content (`index`) + grouped child notes + learning path** before writing notes.
   - Keep **Topic Hierarchy** (`parent_id` / `child_ids`), **Prerequisites** (`prerequisite_ids`), and **Related Links** (`related_ids`) strictly separated.
4. **Generate Through the Full Adaptive Pipeline & Validate Collection-Wide:**
   - Run `python scripts/scribe.py notes generate --vault "<vault>" --session-id "<id>" --validate`.
   - Every child note uses the full adaptive `M1`–`M7` + `EIS-01..EIS-07` Explanation Intelligence pipeline, mandatory Obsidian Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type`, `parent_topic`, `collection_id`), safe atomic writes, and non-destructive incremental reconciliation if a canonical file already exists.
   - Parent MOC notes (`note_type: index`) synthesize structure and link to every child without duplicating child derivations.
   - Validate structural integrity, wikilinks, Obsidian Properties, coverage completeness, and manifest honesty before reporting completion.

## Reference Architecture

- Master skill instructions: `../../SKILL.md`
- Request router & seven-master policy: `../../router.md`, `../../references/routing/master-registry.yaml`, `../../references/routing/routing-policy.md`
- Pre-generation gate & interactive playbooks: `../../references/workflows/notes-creation/pre-gen-gate.md`, `../../references/workflows/notes-creation/command-playbooks.md`
- Obsidian Properties & tag taxonomy: `../../references/metadata/properties-policy.md`, `../../references/metadata/tag-taxonomy.md`
