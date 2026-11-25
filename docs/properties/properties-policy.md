# Obsidian Properties, Placement & Naming Policy

## Purpose

Canonical specification for line-1 YAML frontmatter, vault filename conventions, sibling artifact directories, and cross-artifact alignment (merging previous `note-naming.md` rules into one owner).

## Activation Trigger & Dependencies

- **Activate on:** Every note generation, companion artifact split, or incremental vault update.
- **Dependencies:** [tag-taxonomy.md](tag-taxonomy.md), [authoring_rules.md](../../core/authoring_rules.md).

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
- **Comprehensive `M1` Profile:** Follow [composition-contract.md](../procedures/authoring/composition-contract.md) (the five keys `id`, `aliases`, `topic`, `tags`, `nexttopics`).

### 2. Filenames, Placement & Multi-Artifact Alignment

- **Topic-First Placement Rule:** Always create `<Configured Target>/<Topic>/` first and place all notes, companions (`Experimental Lab`, `Cheatsheet & Interview Q&A`), MOCs, subtopic bundles, and `assets/` for that topic inside `<Topic>/`. Preserve an existing collection's names and layout when revising it.
- **Standalone Specialized Directories (Exception):** `Practice Sets/`, `Atomic Notes/`, `Cheatsheets/`, and `comparison/` are used **only** when the user explicitly requests a standalone cross-topic or single-artifact output (`M3` cheat sheet, `atomic-card`, standalone `M6` practice set, or standalone `M7` comparison) outside a topic folder; when generated as part of a topic bundle or collection, keep them inside `<Configured Target>/<Topic>/`.
- **Multi-Artifact Alignment:** Companion outputs from one request always share identical `topic`, symbol definitions, datasets, and formula applicability conditions while respecting their active YAML profile:
  - *Under the Standard Profile (`M2`–`M7`, single notes):* share `domain`, `master_topic`, `topic`, and `concept_ids` while setting distinct per-artifact `note_type` values.
  - *Under the Strict 5-Key `M1` Collection Profile:* keep **only** the 5 allowed keys (`id`, `aliases`, `topic`, `tags`, `nexttopics`) — never add `domain`, `master_topic`, `concept_ids`, or `note_type` — and align via shared `topic`, matching `domain/`/`subject/`/`topic/` tags, and reciprocal links.

### 3. Safe Incremental Update Preservation

- Preserve custom user properties and user-managed tags without duplication; preserve `created`, refresh `updated` only on real diffs, and prevent duplicate YAML blocks.

## Failure Handling & Validation

- Reject `..` path traversal, Windows reserved names, escaping symlinks, missing mandatory keys, or multi-artifact notation drift during review ([verification-checklist.md](../procedures/review/verification-checklist.md)).
