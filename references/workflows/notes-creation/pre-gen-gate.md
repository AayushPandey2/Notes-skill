# Pre-Generation Resolution Gate

## Purpose & Activation Trigger

Resolve user intent, vault target, existing coverage, placement, template route, and metadata **before** writing any note prose via `/scribe-notes`.

## Execution Sequence

0. **Interactive Configuration Gate:** Resolve master (`M1`–`M7`), variant, depth, scope (`S0`–`S5`), and `single_note` vs `hierarchical_collection`. Ask only unanswered configuration questions (never run a pre-gen knowledge quiz) and preview substantial hierarchical collections before writing.
1. **Resolve Vault Root:** Explicit vault path → `SCRIPTORIUM_VAULT_PATH` → `~/.scriptorium-config.json` (`/scribe-setfolder`); reject `..` traversal and escaping symlinks.
2. **Index Existing Coverage:** Search existing vault Markdown files directly using native file/search tools to detect existing workflows and notes.
3. **Non-Destructive Reuse:** Link existing notes via `[[Exact Filename|Title]]`; update existing notes incrementally rather than overwriting custom user sections or YAML.
4. **Resolve Placement & Metadata:** Use `<Vault>/<Topic>/` (`create_category_folders=false` default; specialized files in `Practice Sets/`, `Atomic Notes/`, `Cheatsheets/`, `comparison/`) and attach profile-appropriate YAML ([properties-policy.md](../../metadata/properties-policy.md), [tag-taxonomy.md](../../metadata/tag-taxonomy.md)).
5. **Select Template:** Load only templates under `references/templates/` matching the routed master/variant (`M1`–`M7`); never run Templater JS or emit unresolved placeholders.

## Failure Handling & Review

- Review changed files against [verification-checklist.md](../validation/verification-checklist.md) so unrelated vault files stay untouched.
