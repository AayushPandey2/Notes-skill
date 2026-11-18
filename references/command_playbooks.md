# Scriptorium Command Playbooks

Read **only** the section matching the active command.

---

## Command A: `/scribe-doubt <topic name> <your doubt>` (Read-Only)

**Restrictions:** Never load `research_protocol.md`, `templates/*.md`, `verification_checklist.md`, initiate external research, create notes, or modify any vault file.

1. **Index Discovery:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic name>" --fields file,title,aliases,headings` to locate the 1–3 most relevant notes.
2. **Targeted Retrieval:** Use `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --extract "<rel_file>" --sections "<matching_sections>"` (or `read_file` on specific line ranges) to read only the relevant sections—never scan unrelated notes.
3. **Grounded Answer:** Answer strictly from retrieved notes using `[[Note Title]]` citations, preserving note terminology. Distinguish note facts from interpretation, and state explicitly what is missing if unanswerable.

---

## Command B: `/scribe-expand <topic name>` (Exhaustive Five-Layer Incremental)

1. **Index Coverage:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic name>" --fields file,title,aliases,depends_on,next_topic,headings` without reading full note bodies.
2. **Five-Layer Gap Audit:** Run the Wave 1 Five-Layer Coverage Audit (Foundations, Core Mechanisms, Formal Theory/Proofs, Variants/Extensions, Pathology/Edge Cases) against existing notes. Identify **all** remaining gaps across Layers 1–5 at once (never just 2–3 items) without duplicating existing concepts.
3. **Conditional Generation (Non-Stopping Queue):**
   - If only metadata/links need updating, apply targeted edits via `python3 <skill_dir>/scripts/patch_links.py` (`--dry-run` to preview) without loading research/template docs or rewriting whole files.
   - Route new notes via `router.md` before research. Persist the plan, then update the syllabus allowlist before authoring every pending note in order using its canonical template in `templates/` and executing the mandatory **Humanization & Cohesion Pass** (`shared/authoring_rules.md`). Keep local filenames and numbering.
4. **Minimal Relationship Updates & Batch Validation:** Patch `depends_on`, `next_topic`, and MOC links in place via `scripts/patch_links.py` without rewriting entire existing notes or imposing a new template retroactively. Run `python3 <skill_dir>/scripts/vault_graph.py "<vault_path>" --topic "<topic name>" --check-cycles` and `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files <modified_files> --fix` until `0 errors`; if semantic errors remain, load `references/verification_checklist.md` and inspect only flagged sections.

---

## Command C: `/scribe-notes <topic>` (Exhaustive Sequential Research & Generation)

### Phase 1 — Exhaustive Research Planning & Indexing
1. Load `references/pre_gen_gate.md` and `references/research_protocol.md`.
2. Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --discover --topic "<topic>"` to inventory existing notes and avoid duplication.
3. Use Waves 0–1 and `router.md` to scope the Five-Layer DAG. Persist the routed plan before creating the folder or fetching sources. Retain numbered slug filenames unless local conventions or a user override specify otherwise. Then write the locked syllabus MOC and show the complete manifest.

### Phase 2 — Non-Stopping Sequential Write-and-Flush Loop (`k = 1..NN`)
1. Follow the one-note workflow in `router.md` for every pending item.
2. Research, scaffold, author with the selected `templates/<route>.md`, run the mandatory **Humanization & Cohesion Pass** (conversational yet rigorous tone, logical narrative transitions, zero AI clichés, synthesized mental models), and publish in dependency order. Reuse existing tags, the run's source dossier, and compact link metadata.
3. Complete every pending item at its selected depth, including automatic practice (`Practice Sets/<Topic> - Practice Test.md` saved in the centralized `Practice Sets/` sibling directory) for a newly created topic.

### Phase 3 — Batch Automated & Semantic Verification
1. Once the queue is complete, run `vault_graph.py "<vault_path>" --topic "<topic>" --check-cycles` and `verify_vault_notes.py "<vault_path>" --files <generated_files>`. Use `--manifest` for the existing custom-layout validation contract.
2. Use each built-in route's own directive in `templates/` and `references/verification_checklist.md` for semantic and humanization checks. Return the completion manifest and each note's verification status.

---

## Command D: `/scribe-distill <topic>` (1-Page Cheat Sheet)

1. **Index Discovery (Wave 0):** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic>" --fields file,title,aliases,status,headings` per `references/research_protocol.md` §0/Wave 0 (skip Waves 2–3 unless `[UNVERIFIED]` gaps exist in the vault).
2. Extract the abstract, synthesis, mechanism, and final traps via `vault_index.py --extract` using the indexed headings. Follow `router.md` and `templates/cheat-sheet.md` to author a `cheat-sheet`, applying the **Humanization & Cohesion Pass** while respecting the 350-word cap. Save into the centralized `Cheatsheets/` folder located at the **same directory level** (sibling level) as the `<subtopic>/` folders, using clear topic/subtopic identifiers (`Cheatsheets/<topic-slug>-CHEAT-SHEET.md` or `Cheatsheets/<topic-slug>-<subtopic-slug>-CHEAT-SHEET.md`) and `note_type: cheatsheet`.
3. **Validation Gate:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files "Cheatsheets/<cheatsheet_filename>.md" --fix` and resolve any reported errors until exit code is `0`.

---

## Command E: `/scribe-ingest <topic> <pdf|url|notes>` (Source Ingestion)

1. Resolve placement, numbering, existing coverage, and tags with the pre-generation gate. Plan the route from the request and cheap metadata before source extraction. Persist the plan before creating a folder.
2. **Source Extraction:**
   - **PDF:** Extract text/equations cleanly using Python (`pypdf` / `pdfplumber` / `pymupdf` if available) without dumping unformatted noise into context.
   - **URL:** Fetch primary content directly.
   - **Raw notes:** Parse directly from user input.
3. Link existing coverage. Use the routed workflow (`templates/<route>.md`) at `<nn>-<ingested-topic-slug>.md` or the selected custom vault template under its manifest contract, and execute the mandatory **Humanization & Cohesion Pass** (synthesizing retrieved material rather than pasting raw definitions).
4. **Validation:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files "<new_file>" --fix` until `0 errors`.

---

## Command F: `/scribe-compare <A> vs <B>` (Trade-Off Matrix)

1. Resolve A and B via `vault_index.py --fields file,title,aliases,topic,tags_unique`. Plan a `comparison` with topic-folder `.`. Read those two notes and `templates/comparison.md`. Search only when a critical assumption is missing from both.
2. Author with the mandatory **Humanization & Cohesion Pass** and publish `comparison/<slug-a>-vs-<slug-b>.md` with `note_type: comparison` and `compared_notes` linking the source notes.
3. **Verify & Echo in Chat:** Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files "comparison/<slug-a>-vs-<slug-b>.md" --fix`, then **output the complete, exact Markdown content of the generated comparison note directly in the agent chat** alongside its saved vault path.

---

## Command G: `/scribe-quiz <topic>` (Interactive Chat Active Recall)

1. **Targeted Load:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --topic "<topic>" --fields file,title,review_log,headings`. Select 1–2 target notes (prioritizing notes with empty `review_log` or previously logged weak concepts) and read only those 1–2 `.md` files. Do **not** load `templates/*.md` or `research_protocol.md`.
2. **One-Question-at-a-Time Loop:** Internally design 3–5 transfer questions probing governing invariants, validity boundaries, edge cases, and traces.
   - **Turn 1:** Present **only Question 1** and **stop immediately** to wait for the user's answer. Never output multiple questions at once.
   - **Subsequent Turns:** Grade explicitly (`Correct`, `Partially Correct`, or `Incorrect`) against the note's exact invariants/equations, explain any missed edge case/assumption with section/equation citations, then present the next single question and wait.
3. **Metadata-Only `review_log` Patch:** After the final question, show a concise **Quiz Summary & Weak-Spot Breakdown** in chat and patch **only** the YAML frontmatter of the tested note(s) via `python3 <skill_dir>/scripts/patch_links.py "<vault_path>" --file "<note.md>" --append-review-log "YYYY-MM-DD | Score: <X>/<N> | Weak: <comma-separated weak invariants/concepts or 'None'>"`.

---

## Command H: `/scribe-atomic-notes <topic name>` (Fast Single-Search Atomic Note)

1. **Bypass Multi-Stage Deep Research:** Do **not** load `references/research_protocol.md` or trigger multi-hop Waves 1–4 research. Load only `templates/atomic.md` and `shared/authoring_rules.md` (plus `shared/math_gates.md` if `math_level >= 1`). Optionally run `vault_index.py "<vault_path>" --discover --topic "<topic name>"` to resolve existing vault tags and real `[[Wikilinks]]`.
2. **Single Direct Web Search / Fetch:** Perform a **single, direct web search or fetch** for `<topic name>` to gather core facts, the governing relationship/formula, and a concrete micro-example quickly.
3. **Populate `templates/atomic.md` with Humanization & Cohesion Pass:** Plan/scaffold with `--template atomic` and populate the Atomic Note Template (`<150` words body cap). Enforce the mandatory **Humanization & Cohesion Pass**:
   - **Conversational yet rigorous tone:** Write like an experienced student or engineer explaining `<topic name>` clearly to their future self—direct, intuitive, and insightful.
   - **Logical narrative transitions:** Connect the definition, micro-example, and boundary condition naturally.
   - **Eliminate AI clichés:** Ban robotic filler phrases (`"In conclusion,"`, `"It is important to note,"`, `"Delving into,"`, `"Crucial aspect,"`, `"Let's explore"`).
   - **Synthesize, don't paste:** Rephrase retrieved facts into a crisp mental model and concrete micro-example rather than dumping raw definitions.
4. **Centralized Destination & Validation:** Save all generated atomic notes inside the single shared `Atomic Notes/` folder located at the **same directory level** (sibling level) as the `<subtopic>/` folders (`Atomic Notes/<topic_name>.md`). Validate with `validate_note.py` and `verify_vault_notes.py "<vault_path>" --files "Atomic Notes/<topic_name>.md" --fix` until `0 errors`.

---

## Command I: `/scribe-classnotes <topic name>` (Fast Multi-Subtopic Class Notes)

Replicates `/scribe-notes`'s multi-subtopic decomposition, `00-MOC-<topic-slug>.md`, and multi-file output structure while **bypassing deep research** and defaulting strictly to `templates/classnotes.md`.

### Phase 1 — Fast Decomposition & Vault Discovery (No Deep Research Protocol)
1. **Explicitly Bypass Deep Research:** Do **not** execute `references/research_protocol.md` multi-wave deep research (`Waves 1–4` exhaustive primary-source chasing). Load `references/pre_gen_gate.md` (skipping `research_protocol.md`).
2. Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --discover --topic "<topic name>"` to inventory existing notes, tags, and local folder conventions.
3. Decompose `<topic name>` into a logical dependency-ordered DAG of numbered subtopics (`01` ... `NN`) inside `<topic-folder>/`.
4. **Template Enforcement & Hard Ban:**
   - Default all core subtopic notes strictly to `templates/classnotes.md` (`classnotes`).
   - Auxiliary templates (`practice`, `cheat-sheet`, `comparison`, `atomic`, `api-table`) are permitted when appropriate (routed to their centralized sibling folders `Practice Sets/`, `Cheatsheets/`, `Atomic Notes/`).
   - **Hard Exclusion (Strict Ban):** NEVER select or use `deepstudy-coding` or `deepstudy-general` (`deepnotes-coding` / `deepnotes-general`) under any circumstances.
5. **Mathematical Notation Guardrail:** Set `math_level: 0` by default (plain language, intuitive analogies, structured text, no formal mathematical formulas or LaTeX derivations). Only permit `math_level: 1` or `2` when `<topic name>` is inherently a Mathematics, Physics, or quantitative engineering topic where omitting equations would make the explanation incomplete.
6. Persist the plan via `plan_notes.py start` before creating the topic folder, then write `00-MOC-<topic-slug>.md`.

### Phase 2 — Fast Web Fetch & Sequential Multi-File Generation (`k = 1..NN`)
1. **Fast Direct Web Fetch Only:** For each subtopic, perform fast, direct web searches/fetches to gather core explanations, sequence, and concrete examples—prioritizing speed and immediate synthesis over multi-hop verification.
2. Scaffold with `--template classnotes` (or allowed auxiliary template) and author in clear, approachable lesson sequence using `templates/classnotes.md`.
3. Execute the mandatory **Humanization & Cohesion Pass** (`shared/authoring_rules.md`: conversational yet rigorous tone, logical narrative transitions, zero AI clichés, synthesized mental models rather than pasted raw text).
4. Validate with `validate_note.py` and publish via `plan_notes.py publish` in dependency order (including any centralized `Practice Sets/` or `Cheatsheets/` outputs).

### Phase 3 — Batch Graph & Scoped Validation
1. Run `vault_graph.py "<vault_path>" --topic "<topic name>" --check-cycles` and `verify_vault_notes.py "<vault_path>" --files <generated_files> --fix` until `0 errors`. Return the completion manifest.
