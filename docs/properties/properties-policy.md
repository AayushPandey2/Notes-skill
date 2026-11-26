# Obsidian Properties, Placement & Naming Policy

## Purpose

Canonical specification for line-1 YAML frontmatter, vault filename conventions, sibling artifact directories, and cross-artifact alignment (merging previous `note-naming.md` rules into one owner).

## Activation Trigger & Dependencies

- **Activate on:** Every note generation, companion artifact split, or incremental vault update.
- **Dependencies:** [tag-taxonomy.md](tag-taxonomy.md).

## Execution & Output Contract

### 1. Frontmatter Profiles (Line 1 Strict YAML)

New Scriptorium notes must start on line 1 with a YAML block delimited by `---`. Preserve existing note layouts and user properties on revision:
- **Standard Profile (`M2`–`M7`, single notes, legacy nested collections):**

| Property | Type | Meaning |
|---|---|---|
| `topic` | string | Human-readable primary subject preserving technical terminology and Unicode |
| `tags` | YAML list | Hierarchical Obsidian tags (no leading `#` prefix) |
| `master_topic` | string | Broader conceptual parent (e.g., a parent discipline, distinct from template ID) |
| `domain` | string | Broad academic or technical field (e.g., `<Field>`, `<Discipline>`) |
| `note_type` | string | Canonical artifact role: `deep-notes`, `study-notes`, `quick-reference`, `worked-solutions`, `implementation-guide`, `assessment`, `synthesis-revision`, `video-notes`, `experimental-lab`, `cheatsheet-qa`, `moc`, or `playlist-index` |

Populate optional managed fields only when meaningful under the Standard Profile: `subdomain`, `id`, `aliases`, `nexttopics`, `prerequisites`, `related`, `parent_note`, `source_refs`, `difficulty`, `status`, `created`, `updated`. **Schema Integrity Rule:** New notes must use only keys authorized by the active profile (plus explicit user-requested customizations)—never invent ad-hoc YAML keys to expose internal planning, routing, source-mode, or verification state (e.g., `source_mode`, `template_id`, `coverage_status`, `concept_ids`); express source restrictions in body prose or authorized `source_refs`. Existing user-defined custom properties are always preserved on revisions (see Section 3).
- **Comprehensive `M1` Profile (New Collections):** Use exactly these ordered keys: `id`, `aliases`, `topic`, `tags`, and `nexttopics`. Use nonempty strings for `id` and `topic`, lists for the rest, and include the title in `aliases`. Use the canonical tag taxonomy and link to future notes only when their targets exist. Distinguish companion roles with unique per-artifact IDs (e.g., `<topic-slug>-<nn>`, `<topic-slug>-<nn>-lab`, `<topic-slug>-<nn>-cheatsheet`, `<topic-slug>-moc`), standardized filenames, and reciprocal links.

### 2. Filenames, Placement & Multi-Artifact Alignment

- **Artifact-Class Naming Conventions:**
  - *Multi-branch collections:* `00 - Map of Contents.md` and `01 - <Title>.md` per branch (consistent numbered prefixes).
  - *Focused single notes & companions:* `<Topic>.md`, `<Topic> - Experimental Lab.md`, and `<Topic> - Cheatsheet & Interview Q&A.md` (unnumbered natural titles).
- **Planned Paths First, Physical Creation After Acceptance:** Plan `<Configured Target>/<Topic>/` paths and filenames cleanly first, creating physical topic directories and writing accepted notes/companions/assets only once pre-save acceptance succeeds (preserving an existing collection's names and layout when revising it).
- **Standalone Specialized Directories (Exception):** `Practice Sets/`, `Atomic Notes/`, `Cheatsheets/`, and `comparison/` are used **only** when the user explicitly requests a standalone cross-topic or single-artifact output (`M3` cheat sheet, `atomic-card`, standalone `M6` practice set, or standalone `M7` comparison) outside a topic folder; when generated as part of a topic bundle or collection, keep them inside `<Configured Target>/<Topic>/`.
- **Multi-Artifact Alignment & Link Hygiene:** Use a shared `topic` and keep overlapping notation, example data, and formula conditions consistent. Under the Standard Profile, `note_type` reflects each role and an ID, if used, is distinct. Apply the [link policy](../procedures/updating/revision-and-linking.md) to existing notes, companions and future topics.

### 3. Safe Incremental Update Preservation

- Preserve custom user properties and user-managed tags without duplication; preserve `created`, refresh `updated` only on real diffs, and prevent duplicate YAML blocks.

## Failure Handling & Validation

- Reject `..` path traversal, Windows reserved names, escaping symlinks, missing mandatory keys, or multi-artifact notation drift during review ([verification-checklist.md](../procedures/review/verification-checklist.md)).
