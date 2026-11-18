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
   - If new notes are needed, load `references/pre_gen_gate.md`, `references/research_protocol.md`, `references/syllabus_template.md`, and the selected contract from `references/note_templates.md`. Update `allowed_subtopics` in `00-MOC-<topic-slug>.md` *first* (or create it via `scaffold_note.py --syllabus`), print the complete `[1/NN]`–`[NN/NN]` missing-subtopic manifest up front, then iterate `k = 1..NN` sequentially—scaffolding via `scripts/scaffold_note.py`, writing each `.md` immediately to disk, and keeping only `{id, filename, title, aliases}` in memory. Never create files outside `allowed_subtopics`, stop early, abbreviate later notes, or pause mid-batch.
4. **Minimal Relationship Updates & Batch Validation:** Patch `depends_on`, `next_topic`, and MOC links in place via `scripts/patch_links.py` without rewriting entire existing notes or imposing a new template retroactively. Run `python3 <skill_dir>/scripts/vault_graph.py "<vault_path>" --topic "<topic name>" --check-cycles` and `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files <modified_files> --fix` until `0 errors`; if semantic errors remain, load `references/verification_checklist.md` and inspect only flagged sections.

---

## Command C: `/scribe-notes <topic>` (Exhaustive Sequential Research & Generation)

### Phase 1 — Exhaustive Research Planning & Indexing
1. Load `references/pre_gen_gate.md` and `references/research_protocol.md`.
2. Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --discover --topic "<topic>"` to inventory existing notes and avoid duplication.
3. Execute **Waves 0–1** of `references/research_protocol.md`: decompose `<topic>` into a **complete Five-Layer acyclic DAG** (`topic-01` ... `topic-NN`, typically 8–15+ nodes), pass the Pre-Execution Coverage Audit Gate, lock global notation, and **write `00-MOC-<topic-slug>.md` first** (`references/syllabus_template.md` / `scaffold_note.py --syllabus`) with `scope_locked: true`, `allowed_subtopics`, `excluded_adjacent_topics`, and the detailed Mermaid learning-flow graph. Print the `[1/NN]`–`[NN/NN]` manifest up front.

Before Phase 2, route each note via `routing.md` and `routes.json`; resolve independent
math/language signals and preserve explicit vault templates. Include planned Practice
in the syllabus allowlist. Retain per-note provenance and completion state via `pre_gen_gate.md`.

### Phase 2 — Non-Stopping Sequential Write-and-Flush Loop (`k = 1..NN`)
1. Load `references/note_templates.md`.
2. Process one subtopic `k` from `1` to `NN` in dependency order:
   - Run Waves 2–4 research & dossier synthesis for subtopic `k`.
   - Scaffold via `python3 <skill_dir>/scripts/scaffold_note.py` (when using the Scriptorium default template) and write `<nn>-<subtopic-slug>.md` **immediately to disk** inside `<vault_path>/<topic-folder>/` using pre-existing `tag_registry` tags.
   - Keep **only** `{id, filename, title, aliases}` in the active cross-link registry (never retain full bodies of already-written notes in context). Keep uncreated future topics as plain text until written.
3. **Anti-Truncation & Anti-Early-Exit Rule:** Complete the locked queue without abbreviating later notes. Every node fulfills its selected contract; deep notes retain full reasoning, conditional justified derivations, domain-adaptive verification and 5–7 transfer questions. Execute `1..NN` to completion without a mid-batch confirmation pause.

### Phase 3 — Batch Automated & Semantic Verification
1. Once all `NN` files are on disk, run `python3 <skill_dir>/scripts/vault_graph.py "<vault_path>" --topic "<topic>" --check-cycles` and `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --manifest <manifest.json> --fix` (or `--files <generated_files> --fix`) until `0 errors` are returned without modifying unrelated notes.
2. Load `references/verification_checklist.md` and perform semantic checks on flagged or newly created sections only. Output a final completion manifest listing all `NN` created `.md` files and their verification status (report `BLOCKED` if vault unavailable).

---

## Command D: `/scribe-distill <topic>` (1-Page Cheat Sheet)

1. **Index Discovery (Wave 0):** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic>" --fields file,title,aliases,status,headings` per `references/research_protocol.md` §0/Wave 0 (skip Waves 2–3 unless `[UNVERIFIED]` gaps exist in the vault).
2. **Targeted Extraction & Synthesis:** Default to `references/templates/cheat-sheet.md`; honor an explicit legacy `references/cheatsheet_template.md` selection. Extract only `abstract,1,3,7,Overview,How it works,Details,Limitations,Connection` via `vault_index.py --extract --sections` and write `<vault>/<topic-slug>/<topic-slug>-CHEAT-SHEET.md` with `note_type: cheat-sheet`, at most 350 body words and 20-word ordinary bullets. The legacy CS budgets apply only to the explicitly selected old contract. Keep raw LaTeX out of YAML and link successfully saved source notes.
3. **Validation Gate:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files "<cheat_sheet_rel_path>" --fix` and resolve any reported errors until exit code is `0`.

---

## Command E: `/scribe-ingest <topic> <pdf|url|notes>` (Source Ingestion)

1. **Vault Discovery (Wave 0):** Load `references/pre_gen_gate.md`. Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --discover --topic "<topic>"` to locate `<vault>/<topic-slug>/`, existing subtopic numbering (`01`, `02`, ...), and existing tags (create `<vault>/<topic-slug>/` if absent).
2. **Source Extraction:**
   - **PDF:** Extract text/equations cleanly using Python (`pypdf` / `pdfplumber` / `pymupdf` if available) without dumping unformatted noise into context.
   - **URL:** Fetch primary content directly.
   - **Raw notes:** Parse directly from user input.
3. **Deduplication & Non-Destructive Creation:** Cross-check existing titles/headings from `vault_index.py`; reference already-covered concepts via `[[Exact Filename|Title]]` instead of duplicating. Scaffold `<nn>-<ingested-topic-slug>.md` via `scripts/scaffold_note.py` (or follow a pre-existing vault template) and populate it using the selected contract in `references/note_templates.md` (source ingestion defaults to Summary or Paper-Breakdown; supporting references for a study topic do not force a summary route), reusing existing tags. **NEVER** overwrite or delete existing completed notes.
4. **Validation:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files "<new_file>" --fix` until `0 errors`.

---

## Command F: `/scribe-compare <A> vs <B>` (Trade-Off Matrix)

1. **Locate Notes (Zero Web Re-Research):** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --fields file,title,aliases,topic,tags_unique` to find the exact `.md` files for `<A>` and `<B>` (same or different topics). Read only those two target files and `references/templates/comparison.md` (unless an explicit legacy or vault comparison template was selected). Synthesize strictly from notes A and B without web searches unless a critical complexity/assumption is missing from both.
2. **Save at Vault Root:** Ensure `<vault_path>/comparison/` exists alongside all `<topic-name>` folders, and save the note as `<vault_path>/comparison/<slug-a>-vs-<slug-b>.md` with `note_type: comparison` and `math_level` (or select the route in a per-file manifest).
3. **Verify & Echo in Chat:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files "comparison/<slug-a>-vs-<slug-b>.md" --fix`, then **output the complete, exact Markdown content of the generated comparison note directly in the agent chat** alongside its saved vault path.

---

## Command G: `/scribe-quiz <topic>` (Interactive Chat Active Recall)

1. **Targeted Load:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic>" --fields file,title,review_log,headings`. Select 1–2 target notes (prioritizing notes with empty `review_log` or previously logged weak concepts) and read only those 1–2 `.md` files. Do **not** load `note_templates.md` or `research_protocol.md`.
2. **One-Question-at-a-Time Loop:** Internally design 3–5 transfer questions probing governing invariants, validity boundaries, edge cases, and traces.
   - **Turn 1:** Present **only Question 1** and **stop immediately** to wait for the user's answer. Never output multiple questions at once.
   - **Subsequent Turns:** Grade explicitly (`Correct`, `Partially Correct`, or `Incorrect`) against the note's exact invariants/equations, explain any missed edge case/assumption with section/equation citations, then present the next single question and wait.
3. **Metadata-Only `review_log` Patch:** After the final question, show a concise **Quiz Summary & Weak-Spot Breakdown** in chat and patch **only** the YAML frontmatter of the tested note(s) via `python3 <skill_dir>/scripts/patch_links.py "<vault_path>" --file "<note.md>" --append-review-log "YYYY-MM-DD | Score: <X>/<N> | Weak: <comma-separated weak invariants/concepts or 'None'>"`.


## Command H: `/scribe-dsa <cpp|python> <problem>` (Problem Study)

Apply pre_gen_gate.md and route to templates/dsa.md. The command locks DSA even
when its payload contains a URL. Validate language and require the actual problem
text/constraints; ask for missing source content instead of inventing it. Use the
requested language for brute force and the improved solution, proof/invariant,
tricky trace, 4-5 valid edge cases, complexity and honest execution results. Use
only verified problem IDs and links. Save under the resolved topic conventions and
validate only its outputs. Useful usage: `/scribe-dsa cpp <problem>` or
`/scribe-dsa python <problem>`. Native command registration is host-dependent;
these forms are supported by this prompt dispatcher and wrappers.

## Command I: `/scribe-practice <topic-or-note>` (Saved Active Recall)

Index and resolve the actual topic/note first. Read only saved source material,
then load templates/practice.md and its needed modules. Save manual subtopic sets
as `<Topic Folder>/Practice Set/<Subtopic> - Practice.md`. For a normal run that
creates a new topic folder, save one `<Topic> - Practice Test.md` in that folder's
Practice Set directory unless opted out. Track that obligation and completion in
the existing operational manifest (pre_gen_gate.md), retaining it on retries.
Generate only from successful saved material. Use 12-15 distinct questions, 10-11
for narrow scope, with separate collapsed hints and complete solutions. Never
invent a score or recurse into another set. Keep `/scribe-quiz` interactive and
its actual-answer review-log patch behavior; saved Practice is a separate mode.
