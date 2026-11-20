# Note Naming and Multi-Artifact Consistency

## Filenames & Placement

- Multi-note curricula: `<Topic Folder>/00-MOC-<topic-slug>.md` and numbered subtopic notes `<nn> - <Title>.md` (or `--legacy-names` `<nn>-<slug>.md`).
- Centralized sibling folders: `Practice Sets/`, `Atomic Notes/`, `Cheatsheets/`, and `comparison/`.
- Reject `..` path traversal, Windows reserved names, and symlinks escaping the vault root.

## Multi-Artifact Alignment

When one request generates separate companion artifacts (e.g., `deep-notes` + `quick-reference` + `flashcards`):
- Share consistent `domain`, `master_topic`, canonical `topic`, and `concept_ids`.
- Assign distinct canonical `note_type` values matching each artifact's master (`M1`–`M7`).
- Verify notation equivalence, numerical agreement, and preserved formula applicability conditions through `KnowledgeEngine.check_multi_artifact()`.
