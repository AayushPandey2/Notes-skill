# Migration history and changed guarantees

Scriptorium's former Python engine, Node runtime, scripts, executable tests, and stored generated-note fixtures have all been removed so the entire repository remains strictly instruction-only and declarative. The six public skill folders are `/scribe-notes`, `/scribe-ytnotes`, `/scribe-doubt`, `/scribe-quiz`, `/scribe-audit`, and `/scribe-setfolder`. Retired note-command names can be interpreted by `/scribe-notes`; they are not separately installed by this repository.

The assistant now researches within permitted sources, writes Markdown directly, and follows the [manual review](../procedures/review/verification-checklist.md). Local code execution is outside the workflow. Host-supported direct inspection can establish specific checks such as viewing an asset. Automatic coverage, cryptographic binding, atomic multi-file publication, cache invalidation, and checkpoint recovery are former engine capabilities.
