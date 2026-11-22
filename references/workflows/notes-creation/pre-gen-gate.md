# Pre-Generation Resolution Gate

## Purpose & Activation Trigger

Resolve user intent, vault target, existing coverage, placement, template route, and metadata **before** writing any note prose via `/scribe-notes` (`T01`–`T04`).

## Execution Sequence

0. **Interactive Configuration Gate:** Run `python scripts/scribe.py notes start "<request>" --vault "<vault_path>"` to infer master (`M1`–`M7`), variant, depth, scope (`S0`–`S5`), and `single_note` vs `hierarchical_collection`. Ask only unanswered configuration questions (never run a pre-gen knowledge quiz) and preview substantial hierarchical collections before writing.
1. **Resolve Vault Root:** Explicit `--vault`, `SCRIPTORIUM_VAULT_PATH`, or `~/.scriptorium-config.json` (`/scribe-setfolder`); reject `..` traversal and escaping symlinks.
2. **Index Existing Coverage:** Run `python scripts/vault_index.py "<vault_path>" --discover --topic "<topic>"` to detect existing workflows and notes.
3. **Non-Destructive Reuse:** Link existing notes via `[[Exact Filename|Title]]`; reconcile existing canonical files via `VaultEngine.update_note()` rather than overwriting custom notes.
4. **Resolve Placement & Metadata:** Use `<Vault>/<Topic>/` via `resolve_collection_layout` (`create_category_folders=false` default; specialized files in `Practice Sets/`, `Atomic Notes/`, `Cheatsheets/`, `comparison/`) and attach profile-appropriate YAML (`properties-policy.md`, `tag-taxonomy.md`).
5. **Select Template & Lock Plan:** Load only templates under `references/templates/` matching the routed master/variant (`M1`–`M7`); persist state under `.scriptorium/collections/` or `.scriptorium/plans/`; never run Templater JS or emit unresolved placeholders.

## Failure Handling & Scoped Validation

- Run `QualityEngine.review_explanatory_clarity()` + `scripts/scribe.py notes validate`, plus `python scripts/verify_vault_notes.py "<vault_path>" --files <changed_files> --fix` (or `--manifest`) so unrelated vault files stay untouched byte for byte.
