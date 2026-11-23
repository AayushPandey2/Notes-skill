# Scriptorium

Scriptorium helps an assistant create, revise, question, and quiz from Obsidian learning notes. It is made of Markdown instructions, templates, and declarative routing data. It has no project runtime or dependency installation step.

## Use

| Request | Entry |
|---|---|
| Create notes, study guides, worked solutions, assessments, or video notes | [skills/scribe-notes/SKILL.md](skills/scribe-notes/SKILL.md) |
| Answer only from existing vault notes | [skills/scribe-doubt/SKILL.md](skills/scribe-doubt/SKILL.md) |
| Run an interactive recall quiz | [skills/scribe-quiz/SKILL.md](skills/scribe-quiz/SKILL.md) |
| Set the default vault and notes folder | [skills/scribe-setfolder/SKILL.md](skills/scribe-setfolder/SKILL.md) |

Start with [SKILL.md](SKILL.md). [router.md](router.md) selects the note product; [references/README.md](references/README.md) points to conditional guidance. An explicit vault destination takes precedence over `SCRIPTORIUM_VAULT_PATH`, then the user's `~/.scriptorium-config.json`.

## Organization

`skills/` holds public commands; `shared/` holds rules used by several commands; `references/routing/` holds route data; `references/templates/` holds seven output masters, variants, knowledge-type subtemplates, and teaching modules; `references/workflows/` holds conditional procedures; `references/metadata/` holds Obsidian conventions; `evals/` holds declarative examples for skill evaluation. The [reference index](references/README.md) explains when to load each part.

## Limits and maintenance

The assistant writes Markdown directly and reviews what it can inspect. The skill does not provide automatic source coverage, mathematical execution, atomic multi-file writes, cryptographic receipts, or Obsidian UI checks. Keep claims about these checks tied to tools actually used. When changing a shared rule, update its consumers and the relevant entries in `evals/`; keep executable code out of this project.

See [migration history](references/contracts/migration-notes.md) and [LICENSE](LICENSE).
