# Scriptorium Command Playbooks

Read **only** the section matching the active command.

---

## Command A: `/scribe-doubt <topic name> <your doubt>` (Read-Only)

**Restrictions:** Never load `research_protocol.md`, `note_templates.md`, `verification_checklist.md`, initiate external research, create notes, or modify any vault file.

1. **Index Discovery:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic name>" --fields file,title,aliases,headings` to locate the 1–3 most relevant notes.
2. **Targeted Retrieval:** Use `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --extract "<rel_file>" --sections "<matching_sections>"` (or `read_file` on specific line ranges) to read only the relevant sections—never scan unrelated notes.
3. **Grounded Answer:** Answer strictly from retrieved notes using `[[Note Title]]` citations, preserving note terminology. Distinguish note facts from interpretation, and state explicitly what is missing if unanswerable.

---

## Command B: `/scribe-expand <topic name>` (Index-First Incremental)

1. **Index Coverage:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic name>" --fields file,title,aliases,depends_on,next_topic,headings` without reading full note bodies.
2. **Gap Analysis:** Compare indexed subtopics, titles, aliases, dependencies, and `##` headings against required coverage. Prioritize missing foundational concepts before advanced additions; never duplicate existing concepts.
3. **Conditional Generation:**
   - If only metadata/links need updating, apply targeted edits via `python3 <skill_dir>/scripts/patch_links.py` (`--dry-run` to preview) without loading research/template docs or rewriting whole files.
   - If new notes are needed, load `references/pre_gen_gate.md`, `references/research_protocol.md`, and `references/note_templates.md`; scaffold skeletons via `scripts/scaffold_note.py`, research & draft only missing subtopics, and update a compact in-memory link registry `{id, filename, title, aliases}`.
4. **Minimal Relationship Updates & Validation:** Patch `depends_on`, `next_topic`, and MOC links in place via `scripts/patch_links.py` without rewriting entire existing notes or imposing a new template retroactively. Skip generation if coverage already exists. Run `python3 <skill_dir>/scripts/vault_graph.py "<vault_path>" --topic "<topic name>" --check-cycles` and `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files <modified_files> --fix`; if semantic errors remain, load `references/verification_checklist.md` and inspect only flagged sections.

---

## Command C: `/scribe-notes <topic>` (Sequential Research & Generation)

### Phase 1 — Research, Planning & Indexing
1. Load `references/pre_gen_gate.md` and `references/research_protocol.md`.
2. Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --discover --topic "<topic>"` to inventory existing notes and avoid duplication.
3. Execute **Waves 0–4** of `references/research_protocol.md`: build an acyclic subtopic DAG (`topic-01`, `topic-02`, ...), lock global notation, verify Tier 1–3 primary & practitioner sources, and complete the Wave 4 pre-writing dossier per subtopic.

### Phase 2 — Sequential Note Generation
1. Load `references/note_templates.md`.
2. Scaffold each note sequentially in dependency order via `python3 <skill_dir>/scripts/scaffold_note.py` (when using the Scriptorium default template) and fill in the 7 sections, updating a compact in-memory link registry `{id, filename, title, aliases}` after each file. Keep uncreated future topics as plain text until written.

### Phase 3 — Automated & Semantic Verification
1. Run `python3 <skill_dir>/scripts/vault_graph.py "<vault_path>" --topic "<topic>" --check-cycles` and `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --manifest <manifest.json> --fix` (or `--files <generated_files> --fix`) to apply scoped mechanical repairs and detect blocking errors without modifying unrelated notes.
2. Load `references/verification_checklist.md` and perform semantic checks on flagged or newly created sections only. Apply targeted fixes without rewriting valid notes, and report final status (`0 errors` required; report `BLOCKED` if vault unavailable).

---

## Command D: `/scribe-distill <topic>` (1-Page Cheat Sheet)

1. **Index Discovery (Wave 0):** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic>" --fields file,title,aliases,status,headings` per `references/research_protocol.md` §0/Wave 0 (skip Waves 2–3 unless `[UNVERIFIED]` gaps exist in the vault).
2. **Targeted Extraction & Synthesis:** Load `references/cheatsheet_template.md`. Extract only `abstract,1,3,7` from each subtopic note via `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --extract "<rel_file>" --sections abstract,1,3,7` and write `<vault>/<topic-slug>/<topic-slug>-CHEAT-SHEET.md` with `note_type: cheatsheet`, strict word budgets (`CS1-DEFINITION`: 25–30 words; `CS2-THEORY`: 50–60 words), zero raw LaTeX in YAML, and `[[Exact Filename|Title]]` links to all distilled notes.
3. **Validation Gate:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files "<cheat_sheet_rel_path>" --fix` and resolve any reported errors until exit code is `0`.

---

## Command E: `/scribe-ingest <topic> <pdf|url|notes>` (Source Ingestion)

1. **Vault Discovery (Wave 0):** Load `references/pre_gen_gate.md`. Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --discover --topic "<topic>"` to locate `<vault>/<topic-slug>/`, existing subtopic numbering (`01`, `02`, ...), and existing tags (create `<vault>/<topic-slug>/` if absent).
2. **Source Extraction:**
   - **PDF:** Extract text/equations cleanly using Python (`pypdf` / `pdfplumber` / `pymupdf` if available) without dumping unformatted noise into context.
   - **URL:** Fetch primary content directly.
   - **Raw notes:** Parse directly from user input.
3. **Deduplication & Non-Destructive Creation:** Cross-check existing titles/headings from `vault_index.py`; reference already-covered concepts via `[[Exact Filename|Title]]` instead of duplicating. Scaffold `<nn>-<ingested-topic-slug>.md` via `scripts/scaffold_note.py` (or follow a pre-existing vault template) and populate it using `references/note_templates.md`, reusing existing tags. **NEVER** overwrite or delete existing completed notes.
4. **Validation:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files "<new_file>" --fix` until `0 errors`.

---

## Command F: `/scribe-compare <A> vs <B>` (Trade-Off Matrix)

1. **Locate Notes (Zero Web Re-Research):** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --fields file,title,aliases,topic,tags_unique` to find the exact `.md` files for `<A>` and `<B>` (same or different topics). Read only those two target files and `references/comparison_template.md` (unless a comparison template already exists in the vault). Synthesize strictly from notes A and B without web searches unless a critical complexity/assumption is missing from both.
2. **Save at Vault Root:** Ensure `<vault_path>/comparison/` exists alongside all `<topic-name>` folders, and save the note as `<vault_path>/comparison/<slug-a>-vs-<slug-b>.md` with `note_type: comparison`.
3. **Verify & Echo in Chat:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files "comparison/<slug-a>-vs-<slug-b>.md" --fix`, then **output the complete, exact Markdown content of the generated comparison note directly in the agent chat** alongside its saved vault path.

---

## Command G: `/scribe-quiz <topic>` (Interactive Chat Active Recall)

1. **Targeted Load:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic>" --fields file,title,review_log,headings`. Select 1–2 target notes (prioritizing notes with empty `review_log` or previously logged weak concepts) and read only those 1–2 `.md` files. Do **not** load `note_templates.md` or `research_protocol.md`.
2. **One-Question-at-a-Time Loop:** Internally design 3–5 transfer questions probing governing invariants, validity boundaries, edge cases, and traces.
   - **Turn 1:** Present **only Question 1** and **stop immediately** to wait for the user's answer. Never output multiple questions at once.
   - **Subsequent Turns:** Grade explicitly (`Correct`, `Partially Correct`, or `Incorrect`) against the note's exact invariants/equations, explain any missed edge case/assumption with section/equation citations, then present the next single question and wait.
3. **Metadata-Only `review_log` Patch:** After the final question, show a concise **Quiz Summary & Weak-Spot Breakdown** in chat and patch **only** the YAML frontmatter of the tested note(s) via `python3 <skill_dir>/scripts/patch_links.py "<vault_path>" --file "<note.md>" --append-review-log "YYYY-MM-DD | Score: <X>/<N> | Weak: <comma-separated weak invariants/concepts or 'None'>"`.
