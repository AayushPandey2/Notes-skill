# Obsidian Properties Policy

Every generated Markdown note MUST begin on line 1 with an Obsidian-compatible YAML frontmatter block (`---` ... `---`) before the first Markdown heading. Never place a `# Properties` heading or Markdown code fence before the YAML frontmatter.

## Required Properties

| Property | Type | Meaning |
|---|---|---|
| `topic` | string | Human-readable primary subject preserving technical terminology and Unicode. |
| `tags` | YAML list | Normalized hierarchical Obsidian tags (no leading `#` prefix). |
| `master_topic` | string | Broader conceptual parent (e.g., `Machine Learning`, `Electromagnetism`). Distinct from master output template. |
| `domain` | string | Broad academic or technical domain (e.g., `Artificial Intelligence`, `Physics`, `History`, `General`). |
| `note_type` | string | Canonical M1–M7 output product (`deep-notes`, `study-notes`, `quick-reference`, `worked-solutions`, `implementation-guide`, `assessment`, `synthesis-revision`). |

## Optional Managed Properties

Populate only when meaningful: `subdomain`, `id`, `aliases`, `nexttopics`, `concept_ids`, `prerequisites`, `related`, `source_mode`, `source_refs`, `difficulty`, `status`, `created`, `updated`, `template_id`, `coverage_status`.

## Update Preservation Rules

When updating an existing note via `VaultEngine.update_note()` or `scripts/scribe.py update`:
- Preserve all unrelated custom user properties (e.g., `custom_property`).
- Preserve user-managed custom tags alongside canonical managed tags without duplication.
- Preserve original `created` date; update `updated` only when content or managed metadata actually changes.
- Prevent duplicate frontmatter blocks; re-running an identical update is strictly idempotent.

Deterministic implementation: `scriptorium/engines/vault.py` (`build_obsidian_properties`, `validate_obsidian_properties`, `incremental_update_note`).
