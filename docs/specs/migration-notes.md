# Migration history and changed guarantees

Scriptorium's former Python engine, Node runtime, scripts, and executable tests were removed before this instruction-only rewrite. The public skill folders are `/scribe-notes`, `/scribe-ytnotes`, `/scribe-doubt`, `/scribe-quiz`, and `/scribe-setfolder`. Retired note-command names can be interpreted by `/scribe-notes`; they are not separately installed by this repository.

The assistant now researches with available tools, writes Obsidian Markdown directly, and reviews the actual result. The [manual checklist](../procedures/review/verification-checklist.md) preserves practical checks for source claims, mathematics, YAML, links, visual rights, and existing-note safety. It does not replace engine guarantees: automatic source coverage, code or numeric execution, cryptographic binding, renderer checks, atomic multi-file publication, cache invalidation, and checkpoint recovery are unavailable unless a separate available native tool establishes a particular check.

For the former implementation's detailed rules, consult the verified pre-rewrite backup recorded in the implementation handoff. Do not recreate a runtime to recover them.
