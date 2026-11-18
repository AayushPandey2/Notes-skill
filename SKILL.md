---
name: scriptorium
description: >-
  Token-efficient Obsidian knowledge-engineering router. Supports /scribe-notes,
  /scribe-expand, /scribe-doubt, /scribe-distill, /scribe-ingest,
  /scribe-compare, /scribe-quiz, /scribe-dsa, and /scribe-practice.
---

# Scriptorium — Progressive-Loading Router

Identify the active command first, read **only** its section in `references/command_playbooks.md` plus the permitted references below, and delegate indexing, scaffolding, graph checks, link patching, and validation to `scripts/`.

## Progressive Loading Policy

| Command | Load | Helpers |
|---|---|---|
| `/scribe-doubt` | Only Command A and targeted notes; no research/templates | index fields/extract |
| `/scribe-quiz` | Only Command G and 1-2 notes | index, review-log patch |
| `/scribe-distill` | Command D, shared rules, selected Cheat-Sheet | targeted extraction, scoped validation |
| `/scribe-compare` | Command F, selected Comparison | index, scoped validation |
| Generation (notes/expand/ingest/dsa/practice) | Matching playbook, gate, routing; selected template/modules; research only as needed | index, scaffold, graph, patch, scoped validation |

**Vault Security:** Resolve `[PATH_TO_OBSIDIAN_VAULT]` from explicit argument, `SCRIPTORIUM_VAULT_PATH`, or `~/.scriptorium-config.json`; reject `..` traversal and escaping symlinks.

**Exhaustive Non-Stopping Execution (`/scribe-notes` & `/scribe-expand`):** In Wave 1, write `00-MOC-<topic-slug>.md` **first** (`references/syllabus_template.md`, `scope_locked: true`) with `allowed_subtopics` and `excluded_adjacent_topics`. Execute `k = 1..NN` sequentially—writing each `.md` immediately to disk and keeping only `{id, filename, title, aliases}` in memory. **Never** create files outside `allowed_subtopics` (use a 2-sentence inline recap + link for tangents), stop after 3–4 notes, abbreviate later notes, or pause mid-batch.

## Command Dispatch

Read **only** the matching `## Command ...` section in `references/command_playbooks.md`:
- **`/scribe-doubt <topic> <doubt>`** $\to$ `Command A` (read-only; targeted `--fields` + `--extract`)
- **`/scribe-expand <topic>`** $\to$ `Command B` (exhaustive 5-layer gap audit; `patch_links.py` / `vault_graph.py`)
- **`/scribe-notes <topic>`** $\to$ `Command C` (Wave 1 full 5-layer DAG $\to$ non-stopping `1..NN` write-and-flush $\to$ batch verify)
- **`/scribe-distill <topic>`** $\to$ `Command D` (targeted extraction from legacy or readable headings $\to$ `<topic-slug>-CHEAT-SHEET.md`)
- **`/scribe-ingest <topic> <pdf|url|notes>`** $\to$ `Command E` (non-destructive source ingestion)
- **`/scribe-compare <A> vs <B>`** $\to$ `Command F` (`comparison/<slug-a>-vs-<slug-b>.md` + echo in chat)
- **`/scribe-quiz <topic>`** $\to$ `Command G` (1 question per turn + `patch_links.py --append-review-log`)

## Per-note routing before research

For generation commands, run the two-pass [routing contract](references/routing.md)
after cheap vault discovery and before expensive research. Read only the chosen
entry in [routes.json](references/routes.json), its template, and needed shared
modules via [note_templates.md](references/note_templates.md). Explicit commands
lock their documented modes; explicit/custom vault template selection is preserved.
The optional `scripts/route_request.py` helper handles cheap command/source/purpose
resolution; the agent supplies independent purpose, math and language signals for
each bounded outline item. It is a planning tool, not a research or note generator.

- `/scribe-dsa <cpp|python> <problem>` -> `Command H`, DSA.
- `/scribe-practice <topic-or-note>` -> `Command I`, saved Practice set.
- Bare article/video URLs -> Summary; identifiable paper URLs -> Paper-Breakdown.
- Revision, lookup, choice, one idea and deep understanding use their distinct routes.

Keep the existing five-layer coverage audit and complete the locked syllabus queue.
Size that queue to the requested scope: a single mechanism can stay one note;
broad topics receive full coverage without padding or unrelated tangents. Each
entry can use a different route and math level. Mathematics is conditional; technical
depth, evidence, invariants and purposeful domain stacks are retained. `routing.md`
is the canonical language matrix; explicit user language takes precedence.
