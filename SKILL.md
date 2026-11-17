---
name: scriptorium
description: >-
  Token-efficient Obsidian knowledge-engineering router. Supports /scribe-notes,
  /scribe-expand, /scribe-doubt, /scribe-distill, /scribe-ingest,
  /scribe-compare, and /scribe-quiz.
---

# Scriptorium — Progressive-Loading Router

Identify the active command first, load **only** the resources permitted for that route, and delegate indexing/mechanical checks to Python (`scripts/vault_index.py`, `scripts/verify_vault_notes.py`).

## Progressive Loading Policy

| Command | `research_protocol.md` | `note_templates.md` | `cheatsheet_template.md` | `comparison_template.md` | `verification_checklist.md` | `vault_index.py` |
|---|---|---|---|---|---|---|
| `/scribe-doubt` | **No** | **No** | **No** | **No** | **No** | **Yes (`--topic`)** |
| `/scribe-quiz` | **No** | **No** | **No** | **No** | **No** | **Yes (`--topic`)** |
| `/scribe-distill` | **Wave 0 only** | **No** | **Yes** | **No** | **No** | **Yes (`--topic`)** |
| `/scribe-compare` | **No** | **No** | **No** | **Yes** | **No** | **Yes** |
| `/scribe-ingest` | **No** *(dedup only)* | **Yes** | **No** | **No** | Semantic only | **Yes (`--topic`)** |
| `/scribe-expand` | Only for new content | Only for new notes | **No** | **No** | Semantic only | **Yes (`--topic`)** |
| `/scribe-notes` | Phase 1 | Phase 2 | **No** | **No** | Phase 3 semantic | **Yes** |

Resolve `[PATH_TO_OBSIDIAN_VAULT]` from explicit argument, `SCRIPTORIUM_VAULT_PATH`, or `~/.scriptorium-config.json` before running any command; reject traversal (`..`) and symlinks escaping the vault.

## Pre-Generation Resolution Gate (Mandatory Before Writing)

Before creating or expanding notes (`/scribe-notes`, `/scribe-expand`, `/scribe-ingest`), execute this 7-step gate:
1. **Resolve Vault:** Validate `[PATH_TO_OBSIDIAN_VAULT]` canonically.
2. **Refresh Index:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --discover --topic "<topic>"`.
3. **Retrieve Existing Concepts:** Link existing coverage via `[[Exact Filename|Title]]` instead of duplicating; distinguish a brief recap from duplicate content.
4. **Resolve Placement & Naming:** Prefer local folder conventions and existing numbering (`01-`, `02-`, ...) over vault-wide averages; disambiguate duplicate basenames with vault-relative paths.
5. **Resolve Template Precedence:** (1) Explicit user choice $\to$ (2) Configured `.obsidian/templates.json` / Templater folder mapping $\to$ (3) Strong semantic match $\to$ (4) Sibling convention $\to$ (5) Scriptorium built-in default. Ask one focused question if materially different templates tie. Never execute Templater JS or save unresolved `<% ... %>` / `{{...}}` placeholders. Follow custom template structure/frontmatter/style (including `<details>` or literal YAML LaTeX if required) instead of forcing Scriptorium's 7-section layout.
6. **Resolve Tags & Metadata:** Reuse exact existing tags and metadata values/types from `tag_candidates` / sibling notes; check the full registry (`--full-registry`) before proposing a new tag.
7. **Lock Operational Manifest:** Record `{operation_id, template_path, template_hash, template_type, outputs, pre_generation_tags}` for scoped validation (`--manifest`), without injecting validation metadata into user notes. *(Optional cross-skill teaching context may personalize notes as factual input without modifying external skill state.)*

**Scoped Validation:** Always run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files <created_or_edited_files> --fix` (or `--manifest <manifest.json> --fix`) so unrelated vault notes remain byte-for-byte unchanged.

---

## Command A: `/scribe-doubt <topic name> <your doubt>` (Read-Only)

**Restrictions:** Never load `references/*.md`, initiate external research, create notes, or modify any vault file.

1. **Index Discovery:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic name>"` to locate the 1–3 most relevant notes via title, aliases, topic, and `##` headings.
2. **Targeted Retrieval:** Read only those 1–3 notes (and direct dependencies if required)—never scan unrelated notes.
3. **Grounded Answer:** Answer strictly from retrieved notes using `[[Note Title]]` citations, preserving note terminology. Distinguish note facts from interpretation, and state explicitly what is missing if unanswerable.

---

## Command B: `/scribe-expand <topic name>` (Index-First Incremental)

1. **Index Coverage:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic name>"` without reading full note bodies.
2. **Gap Analysis:** Compare indexed subtopics, titles, aliases, dependencies, and `##` headings against required coverage. Prioritize missing foundational concepts before advanced additions; never duplicate existing concepts.
3. **Conditional Generation:**
   - If only metadata/links need updating, apply targeted line-level/frontmatter edits without loading research/template docs or rewriting whole files.
   - If new notes are needed, load `references/research_protocol.md` and `references/note_templates.md`, research & draft only missing subtopics, and update a compact in-memory link registry `{id, filename, title, aliases}`.
4. **Minimal Relationship Updates & Validation:** Patch `depends_on`, `next_topic`, and MOC links in place without rewriting entire existing notes or imposing a new template retroactively. Skip generation if coverage already exists. Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files <modified_files> --fix`; if semantic errors remain, load `references/verification_checklist.md` and inspect only flagged sections.

---

## Command C: `/scribe-notes <topic>` (Sequential Research & Generation)

### Phase 1 — Research, Planning & Indexing
1. Load `references/research_protocol.md`.
2. Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>"` to inventory existing notes and avoid duplication.
3. Execute **Waves 0–4** of `references/research_protocol.md`: build an acyclic subtopic DAG (`topic-01`, `topic-02`, ...), lock global notation, verify Tier 1–3 primary & practitioner sources, and complete the Wave 4 pre-writing dossier per subtopic.

### Phase 2 — Sequential Note Generation
1. Load `references/note_templates.md`.
2. Generate each note sequentially in dependency order using the full 7-section template, updating a compact in-memory link registry `{id, filename, title, aliases}` after each file. Keep uncreated future topics as plain text until written.

### Phase 3 — Automated & Semantic Verification
1. Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --manifest <manifest.json> --fix` (or `--files <generated_files> --fix`) to apply scoped mechanical repairs and detect blocking errors without modifying unrelated notes.
2. Load `references/verification_checklist.md` and perform semantic checks on flagged or newly created sections only. Apply targeted fixes without rewriting valid notes, and report final status (`0 errors` required; report `BLOCKED` if vault unavailable).


---

## Command D: `/scribe-distill <topic>` (1-Page Cheat Sheet)

1. **Index Discovery (Wave 0):** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic>"` per `references/research_protocol.md` §0/Wave 0 (skip Waves 2–3 unless `[UNVERIFIED]` gaps exist in the vault).
2. **Targeted Extraction & Synthesis:** Load `references/cheatsheet_template.md`. Read the topic's subtopic notes (prioritizing `> [!abstract] Key Equations`, Section 1, Section 3, and Section 7 traps) and write `<vault>/<topic-slug>/<topic-slug>-CHEAT-SHEET.md` with `note_type: cheatsheet`, strict word budgets (`CS1-DEFINITION`: 25–30 words; `CS2-THEORY`: 50–60 words), zero raw LaTeX in YAML, and `[[Exact Filename|Title]]` links to all distilled notes.
3. **Validation Gate:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --fix` and resolve any reported errors until exit code is `0`.


---

## Command E: `/scribe-ingest <topic> <pdf|url|notes>` (Source Ingestion)

1. **Vault Discovery (Wave 0):** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic>"` to locate `<vault>/<topic-slug>/`, existing subtopic numbering (`01`, `02`, ...), and existing tags (create `<vault>/<topic-slug>/` if absent).
2. **Source Extraction:**
   - **PDF:** Extract text/equations cleanly using Python (`pypdf` / `pdfplumber` / `pymupdf` if available) without dumping unformatted noise into context.
   - **URL:** Fetch primary content directly.
   - **Raw notes:** Parse directly from user input.
3. **Deduplication & Non-Destructive Creation:** Cross-check existing titles/headings from `vault_index.py`; reference already-covered concepts via `[[Exact Filename|Title]]` instead of duplicating. Create a new `<nn>-<ingested-topic-slug>.md` inside `<vault>/<topic-slug>/topics/` using any pre-existing vault template or `references/note_templates.md`, reusing existing tags. **NEVER** overwrite or delete existing completed notes.
4. **Validation:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --fix` until `0 errors`.

---

## Command F: `/scribe-compare <A> vs <B>` (Trade-Off Matrix)

1. **Locate Notes (Zero Web Re-Research):** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>"` to find the exact `.md` files for `<A>` and `<B>` (same or different topics). Read only those two target files and `references/comparison_template.md` (unless a comparison template already exists in the vault). Synthesize strictly from notes A and B without web searches unless a critical complexity/assumption is missing from both.
2. **Save at Vault Root:** Ensure `<vault_path>/comparison/` exists alongside all `<topic-name>` folders, and save the note as `<vault_path>/comparison/<slug-a>-vs-<slug-b>.md` with `note_type: comparison`.
3. **Verify & Echo in Chat:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --fix`, then **output the complete, exact Markdown content of the generated comparison note directly in the agent chat** alongside its saved vault path.

---

## Command G: `/scribe-quiz <topic>` (Interactive Chat Active Recall)

1. **Targeted Load:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic>"`. Select 1–2 target notes (prioritizing notes with empty `review_log` or previously logged weak concepts) and read only those 1–2 `.md` files. Do **not** load `note_templates.md` or `research_protocol.md`.
2. **One-Question-at-a-Time Loop:** Internally design 3–5 transfer questions probing governing invariants, validity boundaries, edge cases, and traces.
   - **Turn 1:** Present **only Question 1** and **stop immediately** to wait for the user's answer. Never output multiple questions at once.
   - **Subsequent Turns:** Grade explicitly (`Correct`, `Partially Correct`, or `Incorrect`) against the note's exact invariants/equations, explain any missed edge case/assumption with section/equation citations, then present the next single question and wait.
3. **Metadata-Only `review_log` Patch:** After the final question, show a concise **Quiz Summary & Weak-Spot Breakdown** in chat and patch **only** the YAML frontmatter of the tested note(s) to append:
   ```yaml
   review_log:
     - "YYYY-MM-DD | Score: <X>/<N> | Weak: <comma-separated weak invariants/concepts or 'None'>"
   ```
