---
name: scribe-notes
description: Universal adaptive note-creation command. Interactively calibrates note style (M1-M7), depth, scope (single note vs. hierarchical multi-note collection), and Obsidian Properties before generating verified study notes.
---

# `/scribe-notes` — Universal Adaptive Notes Command

`/scribe-notes` is the **sole public note-creation command** in Scriptorium. All note styles (`M1` Deep Learning Notes, `M2` Structured Study Notes, `M3` Quick Reference / Cheat Sheet / Formula Sheet / Atomic Card, `M4` Worked Problems & Solutions, `M5` Implementation & Technical Guide, `M6` Practice & Assessment / Flashcards, `M7` Synthesis / Comparison / Concept Map / Paper Breakdown) are routed internally through `/scribe-notes` across the 12 logical architectures (**A0 Director, A1 Map, A2 Tutor, A3 Planner, A4 Researcher, A5 Writer, A6 Visuals, A7 Assets, A8 Quiz, A9 Checker, A10 Vault, A11 Speed**) and explicit triggers (`T01`–`T16`; see [SKILL.md](../../SKILL.md) and [router.md](../../router.md)).

> **Non-note commands preserved separately:** `/scribe-doubt` (read-only vault Q&A), `/scribe-quiz` (interactive active-recall quizzing), `/scribe-setfolder` (vault target folder configuration).

## Comprehensive topic collections

For full-topic M1 notes, follow [the composition contract](../../references/workflows/notes-creation/composition-contract.md), [the KCP integrity contract](../../references/contracts/composition-integrity.md), and [the representation contract](../../references/workflows/notes-creation/representations.md):
- **Layout (`T04`, `T14`):** Publish to the vault-native `<Topic>/` folder via `resolve_collection_layout` (honoring `/scribe-setfolder`, `create_category_folders=false` default) with one numbered MOC and 5–10 substantive chapters (omit `chapters` for adaptive planning). Supply a shared concept plan to `scripts/scribe.py notes compose`.
- **Metadata:** Exact five-key YAML (`id`, `aliases`, `topic`, `tags`, `nexttopics`) with hierarchical `domain/`, `subject/`, `topic/` tags; internal state stays in `.scriptorium/collections/` manifests.
- **Web-Image-First Visuals (`T06`–`T09`):** Follow LAVIA web-image discovery and BVIA accessibility evaluation + image inspection + `Explain -> Show -> Decode -> Connect` walkthroughs, persisting verified local assets under `assets/scriptorium/<collection-slug>/`. Programmatic SVG diagram creation is retired; if no permitted image exists, record an unmet visual obligation honestly.
- **Preparation & Integrity (`T10`–`T16`):** Run `notes compose --prepare` before reviewing; hash prepared chapter bodies for artifact-bound reviews. Use `--context` (`T16`) for selective compilation, `--repair` (`T15`) for dependency-aware fixes, and `--validate` (`T13`) to recheck published artifacts without writing. Record unavailable host checks explicitly. `notes generate --legacy-layout` remains available for existing nested collections; other masters and explicitly narrow single notes follow the workflow below.

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
