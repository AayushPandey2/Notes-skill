# Obsidian Properties, Placement & Naming Policy

## Purpose

Canonical specification for line-1 YAML frontmatter, vault filename conventions, sibling artifact directories, and cross-artifact alignment (merging previous `note-naming.md` rules into one owner).

## Activation Trigger & Dependencies

- **Activate on:** Every note generation, companion artifact split, or incremental vault update.
- **Dependencies:** [tag-taxonomy.md](tag-taxonomy.md), [authoring_rules.md](../../shared/authoring_rules.md).

## Execution & Output Contract

### 1. Frontmatter Profiles (Line 1 Strict YAML)

Every Markdown file MUST begin on line 1 with `---` ... `---` before any heading or fence:
- **Standard Profile (`M2`–`M7`, single notes, legacy nested collections):**

| Property | Type | Meaning |
|---|---|---|
| `topic` | string | Human-readable primary subject preserving technical terminology and Unicode |
| `tags` | YAML list | Hierarchical Obsidian tags (no leading `#` prefix) |
| `master_topic` | string | Broader conceptual parent (e.g., a parent discipline, distinct from template ID) |
| `domain` | string | Broad academic or technical field (e.g., `<Field>`, `<Discipline>`) |
| `note_type` | string | Canonical `M1`–`M7` type (`deep-notes`, `study-notes`, `quick-reference`, `worked-solutions`, `implementation-guide`, `assessment`, `synthesis-revision`) |

Populate optional managed fields only when meaningful: `subdomain`, `id`, `aliases`, `nexttopics`, `concept_ids`, `prerequisites`, `related`, `source_mode`, `source_refs`, `difficulty`, `status`, `created`, `updated`, `template_id`, `coverage_status`.
- **Comprehensive `M1` Profile:** Follow [composition-contract.md](../workflows/notes-creation/composition-contract.md) (the five keys `id`, `aliases`, `topic`, `tags`, `nexttopics`).

### 2. Filenames, Placement & Multi-Artifact Alignment

- **Topic Collections:** Use the authorized `<Vault>/<Topic>/` folder, `00 - Map of Contents.md`, and sequential child notes `<nn> - <Title>.md`. Preserve an existing collection's names and layout when revising it; do not create category folders without a request.
- **Specialized Siblings:** `Practice Sets/`, `Atomic Notes/`, `Cheatsheets/`, and `comparison/`.
- **Multi-Artifact Alignment:** Companion outputs from one request share identical `domain`, `master_topic`, canonical `topic`, `concept_ids`, symbol definitions, and formula applicability conditions while setting distinct per-artifact `note_type` values.

### 3. Safe Incremental Update Preservation

- Preserve custom user properties and user-managed tags without duplication; preserve `created`, refresh `updated` only on real diffs, and prevent duplicate YAML blocks.

## Failure Handling & Validation

- Reject `..` path traversal, Windows reserved names, escaping symlinks, missing mandatory keys, or multi-artifact notation drift during review ([verification-checklist.md](../workflows/validation/verification-checklist.md)).
