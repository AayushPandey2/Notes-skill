---
name: scriptorium
description: >-
  Token-efficient Obsidian knowledge-engineering router. Supports /scribe-notes,
  /scribe-expand, /scribe-doubt, /scribe-distill, /scribe-ingest,
  /scribe-compare, and /scribe-quiz.
---

# Scriptorium — Progressive-Loading Router

Identify the active command first, read **only** its section in `references/command_playbooks.md` plus the permitted references below, and delegate indexing, scaffolding, graph checks, link patching, and validation to `scripts/`.

## Progressive Loading Policy

| Command | `pre_gen_gate.md` | `research_protocol.md` | `note_templates.md` | `cheatsheet_template.md` | `comparison_template.md` | `verification_checklist.md` | Python Helpers |
|---|---|---|---|---|---|---|---|
| `/scribe-doubt` | **No** | **No** | **No** | **No** | **No** | **No** | `vault_index.py --fields ... --extract` |
| `/scribe-quiz` | **No** | **No** | **No** | **No** | **No** | **No** | `vault_index.py --fields`, `patch_links.py` |
| `/scribe-distill` | **No** | **Wave 0 only** | **No** | **Yes** | **No** | **No** | `vault_index.py --extract`, `verify_vault_notes.py` |
| `/scribe-compare` | **No** | **No** | **No** | **No** | **Yes** | **No** | `vault_index.py --fields`, `verify_vault_notes.py` |
| `/scribe-ingest` | **Yes** | **No** *(dedup only)* | **Yes** | **No** | **No** | Semantic only | `vault_index.py --discover`, `scaffold_note.py`, `verify_vault_notes.py` |
| `/scribe-expand` | If new notes | If new content | If new notes | **No** | **No** | Semantic only | `vault_index.py`, `patch_links.py`, `vault_graph.py`, `verify_vault_notes.py` |
| `/scribe-notes` | **Yes** | Phase 1 | Phase 2 | **No** | **No** | Phase 3 semantic | `vault_index.py --discover`, `scaffold_note.py`, `vault_graph.py`, `verify_vault_notes.py` |

**Vault Security:** Resolve `[PATH_TO_OBSIDIAN_VAULT]` from explicit argument, `SCRIPTORIUM_VAULT_PATH`, or `~/.scriptorium-config.json`; reject `..` traversal and escaping symlinks.

## Command Dispatch

Read **only** the matching `## Command ...` section in `references/command_playbooks.md`:
- **`/scribe-doubt <topic> <doubt>`** $\to$ `Command A` (read-only; targeted `--fields` + `--extract`)
- **`/scribe-expand <topic>`** $\to$ `Command B` (index-first incremental; `patch_links.py` / `vault_graph.py`)
- **`/scribe-notes <topic>`** $\to$ `Command C` (Waves 0–4 research $\to$ `scaffold_note.py` $\to$ `verify_vault_notes.py`)
- **`/scribe-distill <topic>`** $\to$ `Command D` (extract `abstract,1,3,7` $\to$ `<topic-slug>-CHEAT-SHEET.md`)
- **`/scribe-ingest <topic> <pdf|url|notes>`** $\to$ `Command E` (non-destructive source ingestion)
- **`/scribe-compare <A> vs <B>`** $\to$ `Command F` (`comparison/<slug-a>-vs-<slug-b>.md` + echo in chat)
- **`/scribe-quiz <topic>`** $\to$ `Command G` (1 question per turn + `patch_links.py --append-review-log`)
