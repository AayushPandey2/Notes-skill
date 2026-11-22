# Scriptorium

Scriptorium is an educational Obsidian note-generation and vault-learning system centered on progressive beginner-first explanations, atomic folded formula walkthroughs (`M01`–`M14`), worked numerical solving (`Step 1`–`12`), web-image-first local visual acquisition (`assets/scriptorium/<slug>/`), video transcript/frame grounding (`/scribe-ytnotes`), and deterministic validation.

Start with [SKILL.md](SKILL.md), [router.md](router.md), [shared/teaching_core.md](shared/teaching_core.md), and [references/README.md](references/README.md).

## Public Slash Commands (`skills/`)

| Command | Purpose | Specification |
|---|---|---|
| `/scribe-notes` | Universal note creation across masters `M1`–`M7`, variants, `S0`–`S5` scopes, and video sources (`/scribe-ytnotes`, `/scribe-ytlecture`) | [skills/scribe-notes/SKILL.md](skills/scribe-notes/SKILL.md) |
| `/scribe-doubt` | Read-only Q&A strictly from existing vault notes with `[[Note Title]]` citations | [skills/scribe-doubt/SKILL.md](skills/scribe-doubt/SKILL.md) |
| `/scribe-quiz` | Interactive one-question-at-a-time recall quiz over existing vault notes | [skills/scribe-quiz/SKILL.md](skills/scribe-quiz/SKILL.md) |
| `/scribe-setfolder` | Persist default Obsidian vault and target subfolder in `~/.scriptorium-config.json` | [skills/scribe-setfolder/SKILL.md](skills/scribe-setfolder/SKILL.md) |

## Repository Layout

```text
scriptorium/
├── SKILL.md, router.md            # Entry routing, triggers (T01–T16, VIDEO-01..04, MATH-01..10, TEACH-01..10)
├── skills/                        # Public slash-command skills (/scribe-notes, doubt, quiz, setfolder)
├── shared/                        # Canonical teaching core, math gates, authoring rules, footer widgets
├── references/                    # Selective-loaded templates (masters/variants/subtemplates/modules),
│                                  #   routing registry, metadata policy, workflows & integrity contracts
├── evals/                         # Skill-creator evaluation & trigger query suites
├── scriptorium/                   # Runtime Python package (models, layout, triggers, 6 engines, composition)
├── scripts/                       # 8 CLI entry points (scribe, plan_notes, scaffold_note, validate_note,
│                                  #   vault_index, vault_graph, patch_links, verify_vault_notes)
├── examples/                      # Read-only reference fixtures and preview demonstrations
└── tests/                         # Automated verification, skill-creator, and architecture suites
```

## Setup & Common Commands

1. **Dependencies:** Python 3.10+, `PyYAML`, `Pillow`, and `pytest`.
2. **Vault Resolution:** Explicit `--vault`, `SCRIPTORIUM_VAULT_PATH`, or `~/.scriptorium-config.json` (`/scribe-setfolder`). New `M1` collections write directly under `<Vault>/<Topic>/` (`resolve_collection_layout`, `create_category_folders=false` default) with downloaded raster visuals under `assets/scriptorium/<slug>/`.
3. **CLI Commands:**
```bash
python -m pytest -q
python scripts/scribe.py audit --inventory
python scripts/scribe.py optimize --benchmark
python scripts/scribe.py notes start "/scribe-notes <Topic>" --vault "<Vault>"
python scripts/scribe.py ytnotes --title "<Lecture>" --url "<URL>" --vault "<Vault>"
python scripts/vault_index.py "<Vault>" --discover --topic "<Topic>"
```

See [LICENSE](LICENSE), [system-overview.md](references/architecture/system-overview.md), and [migration-notes.md](references/contracts/migration-notes.md).
