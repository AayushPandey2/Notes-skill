---
name: scriptorium
description: >-
  Token-efficient Obsidian knowledge-engineering router. Supports /scribe-notes
  <topic>, /scribe-expand <topic name>, and /scribe-doubt <topic name> <doubt>.
---

# Scriptorium — Progressive-Loading Router

Identify the active command first, load **only** the resources permitted for that route, and delegate indexing/mechanical checks to Python (`scripts/vault_index.py`, `scripts/verify_vault_notes.py`).

## Progressive Loading Policy

| Command | `research_protocol.md` | `note_templates.md` | `verification_checklist.md` | `vault_index.py` |
|---|---|---|---|---|
| `/scribe-doubt` | **No** | **No** | **No** | **Yes (`--topic`)** |
| `/scribe-expand` | Only when researching new content | Only when generating new notes | Only for final semantic review | **Yes (`--topic`)** |
| `/scribe-notes` | Phase 1 | Phase 2 | Phase 3 semantic review | **Yes** |

Resolve `[PATH_TO_OBSIDIAN_VAULT]` from explicit argument, `SCRIPTORIUM_VAULT_PATH`, or `~/.scriptorium-config.json` before running any command; reject traversal (`..`) and symlinks escaping the vault.

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
4. **Minimal Relationship Updates & Validation:** Patch `depends_on`, `next_topic`, and MOC links in place. Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --fix`; if semantic errors remain, load `references/verification_checklist.md` and inspect only flagged sections.

---

## Command C: `/scribe-notes <topic>` (Sequential Research & Generation)

### Phase 1 — Research, Planning & Indexing
1. Load `references/research_protocol.md`.
2. Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>"` to inventory existing notes and avoid duplication.
3. Execute Steps 1–5 of `research_protocol.md`: build an acyclic subtopic DAG (`topic-01`, `topic-02`, ...), verify Tier 1–3 primary sources, and complete the 7-part internal research dossier per subtopic.

### Phase 2 — Sequential Note Generation
1. Load `references/note_templates.md`.
2. Generate each note sequentially in dependency order using the full 7-section template, updating a compact in-memory link registry `{id, filename, title, aliases}` after each file. Keep uncreated future topics as plain text until written.

### Phase 3 — Automated & Semantic Verification
1. Run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --fix` to apply mechanical repairs and detect blocking errors.
2. Load `references/verification_checklist.md` and perform semantic checks on flagged or newly created sections only. Apply targeted fixes without rewriting valid notes, and report final status (`0 errors` required; report `BLOCKED` if vault unavailable).
