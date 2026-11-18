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

**Exhaustive Non-Stopping Execution (`/scribe-notes` & `/scribe-expand`):** In Wave 1, write `00-MOC-<topic-slug>.md` **first** (`references/syllabus_template.md`, `scope_locked: true`) with `allowed_subtopics` and `excluded_adjacent_topics`. Execute `k = 1..NN` sequentially—writing each `.md` immediately to disk and keeping only `{id, filename, title, aliases}` in memory. **Never** create files outside `allowed_subtopics` (use a 2-sentence inline recap + link for tangents), stop after 3–4 notes, abbreviate later notes, or pause mid-batch.

## Command Dispatch

Read **only** the matching `## Command ...` section in `references/command_playbooks.md`:
- **`/scribe-doubt <topic> <doubt>`** $\to$ `Command A` (read-only; targeted `--fields` + `--extract`)
- **`/scribe-expand <topic>`** $\to$ `Command B` (exhaustive 5-layer gap audit; `patch_links.py` / `vault_graph.py`)
- **`/scribe-notes <topic>`** $\to$ `Command C` (Wave 1 full 5-layer DAG $\to$ non-stopping `1..NN` write-and-flush $\to$ batch verify)
- **`/scribe-distill <topic>`** $\to$ `Command D` (extract `abstract,1,3,7` $\to$ `<topic-slug>-CHEAT-SHEET.md`)
- **`/scribe-ingest <topic> <pdf|url|notes>`** $\to$ `Command E` (non-destructive source ingestion)
- **`/scribe-compare <A> vs <B>`** $\to$ `Command F` (`comparison/<slug-a>-vs-<slug-b>.md` + echo in chat)
- **`/scribe-quiz <topic>`** $\to$ `Command G` (1 question per turn + `patch_links.py --append-review-log`)

## Section 5 Domain-to-Language Routing (1–3 Implementations)

| Topic Domain | Selected Implementations (Foundational $\to$ Production) |
|---|---|
| **ML / Deep Learning** | 1. `Python + NumPy` (from-scratch) · 2. `Python + scikit-learn` · 3. `Python + PyTorch` *(when applicable)* |
| **DSA** | 1. `C++20` · 2. `Python 3` · 3. *(Optional)* `Rust` or `Java` |
| **Systems / OS / Concurrency** | 1. `C17` or `Rust` · 2. `Python 3` (harness/simulation) |
| **Databases / Data Eng** | 1. `SQL` (PostgreSQL / DuckDB) · 2. `Python (pandas / polars)` |
| **Web / Distributed / APIs** | 1. `TypeScript / Node.js` or `Go` · 2. `Python 3` |
| **Pure Math / Non-Code** | 1. `Python + SymPy / NumPy` *(or proof/counterexample check if inapplicable)* |
