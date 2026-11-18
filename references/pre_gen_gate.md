# Pre-Generation Resolution Gate (Mandatory Before Writing)

Before creating or expanding notes (`/scribe-notes`, `/scribe-expand`, `/scribe-ingest`), execute this 7-step gate:

1. **Resolve Vault:** Validate `[PATH_TO_OBSIDIAN_VAULT]` canonically (explicit argument, `SCRIPTORIUM_VAULT_PATH`, or `~/.scriptorium-config.json`; reject `..` traversal and escaping symlinks).
2. **Refresh Index:** Run `python3 <skill_dir>/scripts/vault_index.py "<vault_path>" --discover --topic "<topic>"`.
3. **Retrieve Existing Concepts:** Link existing coverage via `[[Exact Filename|Title]]` instead of duplicating; distinguish a brief recap from duplicate content.
4. **Resolve Placement & Naming:** Prefer local folder conventions and existing numbering (`01-`, `02-`, ...) over vault-wide averages; disambiguate duplicate basenames with vault-relative paths.
5. **Resolve Template Precedence:** (1) Explicit user choice $\to$ (2) Configured `.obsidian/templates.json` / Templater folder mapping $\to$ (3) Strong semantic match $\to$ (4) Sibling convention $\to$ (5) Scriptorium built-in default (`scripts/scaffold_note.py` + `references/note_templates.md`). Ask one focused question if materially different templates tie. Never execute Templater JS or save unresolved `<% ... %>` / `{{...}}` placeholders. Follow custom template structure/frontmatter/style (including `<details>` or literal YAML LaTeX if required) instead of forcing Scriptorium's 7-section layout.
6. **Resolve Tags & Metadata:** Reuse exact existing tags and metadata values/types from `tag_candidates` / sibling notes; check `--full-registry` before proposing a new tag.
7. **Lock Operational Manifest:** Record `{operation_id, template_path, template_hash, template_type, outputs, pre_generation_tags}` for scoped validation (`--manifest`), without injecting validation metadata into user notes. *(Optional cross-skill teaching context may personalize notes as factual input without modifying external skill state.)*

**Scoped Validation:** Always run `python3 <skill_dir>/scripts/verify_vault_notes.py "<vault_path>" --files <created_or_edited_files> --fix` (or `--manifest <manifest.json> --fix`) so unrelated vault notes remain byte-for-byte unchanged.
