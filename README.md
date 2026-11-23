# Scriptorium

Scriptorium is an instruction-and-reference-only Obsidian skill system centered on progressive beginner-first explanations, atomic 12-stage folded formula walkthroughs, worked numerical solving (`Step 1`–`12`), web-image-first local visual acquisition (`assets/scriptorium/<slug>/`), video transcript/frame grounding (`/scribe-ytnote`), and explicit review checklists—with zero executable scripts or custom runtimes.

Start with [SKILL.md](SKILL.md), [router.md](router.md), [shared/teaching_core.md](shared/teaching_core.md), and [references/README.md](references/README.md).

## Public Slash Commands (`skills/`)

| Command | Purpose | Specification |
|---|---|---|
| `/scribe-notes` | Universal note creation across masters `M1`–`M7`, variants, and video sources (`/scribe-ytnote`, `/scribe-ytnotes`, `/scribe-ytlecture`) | [skills/scribe-notes/SKILL.md](skills/scribe-notes/SKILL.md) |
| `/scribe-doubt` | Read-only Q&A strictly from existing vault notes with `[[Note Title]]` citations | [skills/scribe-doubt/SKILL.md](skills/scribe-doubt/SKILL.md) |
| `/scribe-quiz` | Interactive one-question-at-a-time recall quiz over existing vault notes | [skills/scribe-quiz/SKILL.md](skills/scribe-quiz/SKILL.md) |
| `/scribe-setfolder` | Persist default Obsidian vault and target subfolder in `~/.scriptorium-config.json` | [skills/scribe-setfolder/SKILL.md](skills/scribe-setfolder/SKILL.md) |

## Repository Layout

```text
scriptorium/
├── SKILL.md, router.md   # Entry routing, direct-authoring workflow, and master table
├── skills/               # Public slash-command skills (/scribe-notes, doubt, quiz, setfolder)
├── shared/               # Direct-authoring pipeline, teaching core, math gates, authoring rules, footer widgets
├── references/           # Selective-loaded masters, variants, subtemplates, modules, routing, workflows
└── evals/                # Skill-creator evaluation & trigger query suites
```

## Vault Resolution

Explicit vault path → `SCRIPTORIUM_VAULT_PATH` → `~/.scriptorium-config.json` (`/scribe-setfolder`). New `M1` collections write directly under `<Vault>/<Topic>/` (`create_category_folders=false` default) with downloaded raster visuals under `assets/scriptorium/<slug>/`.

See [LICENSE](LICENSE), [system-overview.md](references/architecture/system-overview.md), and [migration-notes.md](references/contracts/migration-notes.md).
