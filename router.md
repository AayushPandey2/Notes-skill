# Scriptorium routing

All creation routes follow [the direct-authoring workflow](shared/runtime_pipeline.md): read only the needed references, research with native tools, and write Obsidian Markdown and downloaded raster assets directly. During note creation, author content directly—never create, execute, or modify scripts or project source code to assemble, render, validate, download, or publish notes.

## Intent

Explicit `/scribe-*` command locks outrank explicit template/artifact selectors; selectors outrank dominant-intent classification and standalone-source defaults. Strip negated artifact requests (`"don't make a cheat sheet"`) before classification. Source-policy constraints (`strict` / `source_first`) are never overridden by template routing. See [routing-policy.md](references/routing/routing-policy.md) and [master-registry.yaml](references/routing/master-registry.yaml).

### Seven Canonical Master Output Templates (`M1–M7`)

| Master | Route | Purpose | Template |
|---|---|---|---|
| **M1** | `deep-notes` | Comprehensive first-principles deep learning notes | [deep-notes.md](references/templates/masters/deep-notes.md) |
| **M2** | `study-notes` | Source-aligned or syllabus-aligned structured study notes (`lecture_order` variant) | [study-notes.md](references/templates/masters/study-notes.md) |
| **M3** | `quick-reference` | High-density cheat sheets, formula sheets, syntax/command references, atomic cards | [quick-reference.md](references/templates/masters/quick-reference.md) |
| **M4** | `worked-solutions` | Problem-centered step-by-step worked solutions with method selection & verification | [worked-solutions.md](references/templates/masters/worked-solutions.md) |
| **M5** | `implementation-guide` | Build, implement, trace, test, and debug technical solutions with clear code blocks | [implementation-guide.md](references/templates/masters/implementation-guide.md) |
| **M6** | `assessment` | Active recall practice sets, flashcards, mock exams, and diagnostic self-testing | [assessment.md](references/templates/masters/assessment.md) |
| **M7** | `synthesis-revision` | Comparisons, paper breakdowns, source summaries, concept maps, exam revision packs | [synthesis-revision.md](references/templates/masters/synthesis-revision.md) |

### Active Public `/scribe-*` Commands

| Command | Role / Routing | Load next |
|---|---|---|
| `/scribe-notes` | **Universal Adaptive Note Creation (`M1`–`M7`)** — Interactive configuration gate, scope calibration, atomic formula+fold rendering, raster web-image & video-frame composition (`/scribe-ytnote`), and manual review | [Pre-generation gate](references/workflows/notes-creation/pre-gen-gate.md) + [Adaptive engine](references/workflows/notes-creation/adaptive-engine.md) + [ARRIE research engine](references/workflows/research/research-engine.md) + selected master (`M1`–`M7`) |
| `/scribe-ytnote` | **Unified Video & Lecture Command** (merges `/scribe-ytnotes` and `/scribe-ytlecture`) — Timestamped transcript segmentation, authorized frame inspection, access-state honesty, and formula folds inside `/scribe-notes` | [representation & media rules](references/workflows/notes-creation/representations.md) + selected master (`M2`/`M1`/`M7`) |
| `/scribe-doubt` | Read existing notes only; zero edits or external research | [Command A](references/workflows/notes-creation/command-playbooks.md#command-a) only |
| `/scribe-quiz` | **M6 (`mock_exam`)** — One question at a time from existing notes; log weak spots in note body | [Command G](references/workflows/notes-creation/command-playbooks.md#command-g) only |
| `/scribe-setfolder` | Configure default target Obsidian notes folder in `~/.scriptorium-config.json` | Vault config only |

> **Retired public wrappers:** `/scribe-deepnotes`, `/scribe-distill`, `/scribe-atomic-notes`, `/scribe-compare`, `/scribe-dsa`, `/scribe-practice`, `/scribe-ingest`, and `/scribe-expand` are unified into `/scribe-notes`. Their playbooks and master templates (`M1`–`M7`) remain active inside `/scribe-notes`.

## Plan and Publish

1. **Resolve vault & layout:** Check explicit vault path → `SCRIPTORIUM_VAULT_PATH` → `~/.scriptorium-config.json`. Inspect existing vault notes for overlap; place new `M1` collections directly under `<Vault>/<Topic>/` (`create_category_folders=false` default) and preserve existing IDs, tags, and filenames. See [pre-generation gate](references/workflows/notes-creation/pre-gen-gate.md) and [composition contract](references/workflows/notes-creation/composition-contract.md).
2. **Plan concepts & chapters:** Order concepts topologically by prerequisites without fixed chapter quotas—chapter count follows instructional coherence and complexity. For comprehensive collections, plan `00 - Map of Contents.md` + numbered chapters (`01 - <Title>.md`, ...). See [adaptive engine](references/workflows/notes-creation/adaptive-engine.md).
3. **Selective context & ARRIE research:** Load only the active master/variant, [authoring rules](shared/authoring_rules.md), [math gates](shared/math_gates.md), and required knowledge-type subtemplates. Verify claims via [ARRIE](references/workflows/research/research-engine.md) and separate factual citations from [further-learning recommendations](references/workflows/research/resource-recommendations.md).
4. **Acquire & inspect visuals before writing:** Search open educational images, verify file-specific permissive licenses, download real raster bytes (`png`/`jpg`/`webp`) into `<Vault>/assets/scriptorium/<collection-slug>/`, inspect the downloaded image visually via `read_file`, and compose `Explain -> Show -> Decode -> Connect` around the inspected image.
5. **Author, review & publish:** Write natural beginner-first prose ([teaching_core.md](shared/teaching_core.md)), pair every `$$...$$` with `> [!note]- 📐 Understand this formula`, include complete `Step 1`–`12` worked examples and folded hint/answer assessments, review everything against [verification-checklist.md](references/workflows/validation/verification-checklist.md), and repair only failing spans without overwriting unrelated user notes.
