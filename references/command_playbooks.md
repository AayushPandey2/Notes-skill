# Scriptorium Command Playbooks

Read **only** the section matching the active command.

---

## Command A: `/scribe-doubt <topic name> <your doubt>` (Read-Only)

**Restrictions:** Never load `research_protocol.md`, `note_templates.md`, `verification_checklist.md`, initiate external research, create notes, or modify any vault file.

1. **Index Discovery:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic name>" --fields file,title,aliases,headings` to locate the 1–3 most relevant notes.
2. **Targeted Retrieval:** Use `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --extract "<rel_file>" --sections "<matching_sections>"` (or `read_file` on specific line ranges) to read only the relevant sections—never scan unrelated notes.
3. **Grounded Answer:** Answer strictly from retrieved notes using `[[Note Title]]` citations, preserving note terminology. Distinguish note facts from interpretation, and state explicitly what is missing if unanswerable.

---

## Command B: `/scribe-expand <topic name>` (Exhaustive Five-Layer Incremental)

1. **Index Coverage:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic name>" --fields file,title,aliases,depends_on,next_topic,headings` without reading full note bodies.
2. **Five-Layer Gap Audit:** Run the Wave 1 Five-Layer Coverage Audit (Foundations, Core Mechanisms, Formal Theory/Proofs, Variants/Extensions, Pathology/Edge Cases) against existing notes. Identify **all** remaining gaps across Layers 1–5 at once (never just 2–3 items) without duplicating existing concepts.
3. **Conditional Generation (Non-Stopping Queue):**
   - If only metadata/links need updating, apply targeted edits via `python3 <skill_dir>/scripts/patch_links.py` (`--dry-run` to preview) without loading research/template docs or rewriting whole files.
   - Route new notes via `router.md` before research. Persist the plan, then update the syllabus allowlist before authoring every pending note in order. Keep local filenames and numbering.
4. **Minimal Relationship Updates & Batch Validation:** Patch `depends_on`, `next_topic`, and MOC links in place via `scripts/patch_links.py` without rewriting entire existing notes or imposing a new template retroactively. Run `python3 <skill_dir>/scripts/vault_graph.py "<vault_path>" --topic "<topic name>" --check-cycles` and `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files <modified_files> --fix` until `0 errors`; if semantic errors remain, load `references/verification_checklist.md` and inspect only flagged sections.

---

## Command C: `/scribe-notes <topic>` (Exhaustive Sequential Research & Generation)

### Phase 1 — Exhaustive Research Planning & Indexing
1. Load `references/pre_gen_gate.md` and `references/research_protocol.md`.
2. Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --discover --topic "<topic>"` to inventory existing notes and avoid duplication.
3. Use Waves 0–1 and `router.md` to scope the Five-Layer DAG. Persist the routed plan before creating the folder or fetching sources. Retain numbered slug filenames unless local conventions or a user override specify otherwise. Then write the locked syllabus MOC and show the complete manifest.

### Phase 2 — Non-Stopping Sequential Write-and-Flush Loop (`k = 1..NN`)
1. Follow the one-note workflow in `router.md` for every pending item.
2. Research, scaffold, author, and publish in dependency order. Reuse existing tags, the run's source dossier, and compact link metadata.
3. Complete every pending item at its selected depth, including automatic practice for a newly created topic.

### Phase 3 — Batch Automated & Semantic Verification
1. Once the queue is complete, run `vault_graph.py "<vault_path>" --topic "<topic>" --check-cycles` and `verify_vault_notes.py "<vault_path>" --files <generated_files>`. Use `--manifest` for the existing custom-layout validation contract.
2. Use each built-in route's own directive for semantic checks. Use `references/verification_checklist.md` for legacy deep notes. Return the completion manifest and each note's verification status.

---

## Command D: `/scribe-distill <topic>` (1-Page Cheat Sheet)

1. **Index Discovery (Wave 0):** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic>" --fields file,title,aliases,status,headings` per `references/research_protocol.md` §0/Wave 0 (skip Waves 2–3 unless `[UNVERIFIED]` gaps exist in the vault).
2. Extract the abstract, synthesis, mechanism, and final traps via `vault_index.py --extract` using the indexed headings. Follow `router.md` to author a `cheat-sheet`. Keep `<topic-folder>/<topic-slug>-CHEAT-SHEET.md` and `note_type: cheatsheet`.
3. **Validation Gate:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files "<cheat_sheet_rel_path>" --fix` and resolve any reported errors until exit code is `0`.

---

## Command E: `/scribe-ingest <topic> <pdf|url|notes>` (Source Ingestion)

1. Resolve placement, numbering, existing coverage, and tags with the pre-generation gate. Plan the route from the request and cheap metadata before source extraction. Persist the plan before creating a folder.
2. **Source Extraction:**
   - **PDF:** Extract text/equations cleanly using Python (`pypdf` / `pdfplumber` / `pymupdf` if available) without dumping unformatted noise into context.
   - **URL:** Fetch primary content directly.
   - **Raw notes:** Parse directly from user input.
3. Link existing coverage. Use the routed workflow at `<nn>-<ingested-topic-slug>.md` or the selected custom vault template under its manifest contract.
4. **Validation:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files "<new_file>" --fix` until `0 errors`.

---

## Command F: `/scribe-compare <A> vs <B>` (Trade-Off Matrix)

1. Resolve A and B via `vault_index.py --fields file,title,aliases,topic,tags_unique`. Plan a `comparison` with topic-folder `.`. Read those two notes and the selected template. Search only when a critical assumption is missing from both.
2. Publish `comparison/<slug-a>-vs-<slug-b>.md` with `note_type: comparison` and `compared_notes` linking the source notes.
3. **Verify & Echo in Chat:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files "comparison/<slug-a>-vs-<slug-b>.md" --fix`, then **output the complete, exact Markdown content of the generated comparison note directly in the agent chat** alongside its saved vault path.

---

## Command G: `/scribe-quiz <topic>` (Interactive Chat Active Recall)

1. **Targeted Load:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic>" --fields file,title,review_log,headings`. Select 1–2 target notes (prioritizing notes with empty `review_log` or previously logged weak concepts) and read only those 1–2 `.md` files. Do **not** load `note_templates.md` or `research_protocol.md`.
2. **One-Question-at-a-Time Loop:** Internally design 3–5 transfer questions probing governing invariants, validity boundaries, edge cases, and traces.
   - **Turn 1:** Present **only Question 1** and **stop immediately** to wait for the user's answer. Never output multiple questions at once.
   - **Subsequent Turns:** Grade explicitly (`Correct`, `Partially Correct`, or `Incorrect`) against the note's exact invariants/equations, explain any missed edge case/assumption with section/equation citations, then present the next single question and wait.
3. **Metadata-Only `review_log` Patch:** After the final question, show a concise **Quiz Summary & Weak-Spot Breakdown** in chat and patch **only** the YAML frontmatter of the tested note(s) via `python3 <skill_dir>/scripts/patch_links.py "<vault_path>" --file "<note.md>" --append-review-log "YYYY-MM-DD | Score: <X>/<N> | Weak: <comma-separated weak invariants/concepts or 'None'>"`.
