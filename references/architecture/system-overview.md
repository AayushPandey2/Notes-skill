# Scriptorium System Architecture Overview

Scriptorium is an instruction-and-reference-only Obsidian skill system. It coordinates `/scribe-notes` (including `/scribe-ytnote`), `/scribe-doubt`, `/scribe-quiz`, and `/scribe-setfolder` through declarative Markdown instructions, seven canonical masters (`M1`–`M7`), `12` variants, `6` knowledge-type subtemplates, and selective on-demand references—with zero executable scripts or custom runtimes.

## 1. Direct-Authoring Lifecycle

1. **Resolve Scope & Destination:** Resolve vault path (explicit → `SCRIPTORIUM_VAULT_PATH` → `~/.scriptorium-config.json`), master (`M1`–`M7`), variant, depth, and source policy without running a pre-generation knowledge quiz.
2. **Load Only Required Context:** Read [teaching_core.md](../../shared/teaching_core.md), [authoring_rules.md](../../shared/authoring_rules.md), [math_gates.md](../../shared/math_gates.md) (when math applies), and only the active master/variant/subtemplate.
3. **Research & Acquire Visuals First:** Verify claims from primary sources ([research-engine.md](../workflows/research/research-engine.md)). For visual needs, find openly licensed raster images (`png`/`jpg`/`webp`), download them into `<Vault>/assets/scriptorium/<collection-slug>/`, and inspect each image via `read_file` before writing prose ([representations.md](../workflows/notes-creation/representations.md)).
4. **Author Markdown Directly:** Write beginner-first prose, `> [!note]- 📐 Understand this formula` folds beneath every `$$...$$`, `Step 1`–`12` worked examples, and `Explain -> Show -> Decode -> Connect` visual walkthroughs directly to `<Vault>/<Topic>/` (preserving unrelated notes).
5. **Manual Review & Honest Limitations:** Review finished Markdown against [verification-checklist.md](../workflows/validation/verification-checklist.md). Because no custom script engine runs, automated execution, cryptographic hash receipts, and atomic rollback transactions are not guaranteed unless an available native tool establishes them.

## 2. Public Command Footprint

1. `/scribe-notes` — Universal note creation (`M1`–`M7`, variants, collections, and `/scribe-ytnote` video/lecture notes).
2. `/scribe-doubt` — Strictly read-only vault Q&A with `[[Note Title]]` citations.
3. `/scribe-quiz` — Interactive one-question-at-a-time active-recall quiz over existing notes.
4. `/scribe-setfolder` — Persist default Obsidian vault and target subfolder in `~/.scriptorium-config.json`.

See [template-module-catalog.md](template-module-catalog.md) for the complete Master, Variant, Subtemplate, and Module inventory.
