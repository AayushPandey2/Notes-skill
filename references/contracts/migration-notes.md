# Migration & Historical Architecture Notes

Scriptorium has been migrated to a **pure instruction-and-reference-only skill** with zero executable scripts or custom runtimes.

- **Public Entry Commands:** `/scribe-notes` (including `/scribe-ytnote` / `/scribe-ytnotes` / `/scribe-ytlecture`), `/scribe-doubt`, `/scribe-quiz`, and `/scribe-setfolder`.
- **Retired Public Wrappers:** `/scribe-deepnotes`, `/scribe-distill`, `/scribe-atomic-notes`, `/scribe-compare`, `/scribe-dsa`, `/scribe-practice`, `/scribe-ingest`, and `/scribe-expand` are unified into `/scribe-notes`.
- **Retired Executable Infrastructure:** The prior Python (`scriptorium/`, `scripts/`, `tests/`) and intermediate Node.js (`runtime/`, `package.json`) architectures were removed. Educational composition, 12-stage formula folds, web-image-first visual acquisition/inspection, and Obsidian publishing now execute directly via native assistant tools and [verification-checklist.md](../workflows/validation/verification-checklist.md).
