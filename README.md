# Scriptorium

Scriptorium builds structured, domain-independent Obsidian study notes around progressive beginner-to-advanced explanations, `M01`–`M14` mathematical deconstruction, `Step 1`–`12` worked numerical solutions, web-image-first local assets (`assets/scriptorium/<slug>/`), image-grounded visual reading guides, and deterministic quality verification.

Start with [SKILL.md](SKILL.md), [router.md](router.md), [shared/teaching_core.md](shared/teaching_core.md), [the system overview](references/architecture/system-overview.md), and [the composition contract](references/workflows/notes-creation/composition-contract.md).

---

## Active Public Commands (`skills/`)

| Command | Role | Primary Authority |
|---|---|---|
| `/scribe-notes` | Universal note creation across masters `M1`–`M7`, variants, `S0`–`S5` scopes, and interactive configuration | [skills/scribe-notes/SKILL.md](skills/scribe-notes/SKILL.md) |
| `/scribe-doubt` | Read-only vault Q&A with exact `[[Note Title]]` citations (no edits/research) | [skills/scribe-doubt/SKILL.md](skills/scribe-doubt/SKILL.md) |
| `/scribe-quiz` | Interactive one-question-at-a-time recall quiz grounded in existing vault notes | [skills/scribe-quiz/SKILL.md](skills/scribe-quiz/SKILL.md) |
| `/scribe-setfolder` | Configure default vault root/folder in `~/.scriptorium-config.json` | [skills/scribe-setfolder/SKILL.md](skills/scribe-setfolder/SKILL.md) |

---

## Logical Architecture (`A0`–`A11`) & Code Layout

Runtime logic maps 12 canonical responsibilities (`A0 Director`–`A11 Speed`, defined in [triggers.py](scriptorium/triggers.py)) across cohesive Python engines and 8 CLI tools:

```text
scriptorium/
├── SKILL.md, router.md            # Entry routing, triggers (T01-T16, MATH-01..10, TEACH-01..10)
├── shared/                        # teaching_core.md, authoring_rules.md, math_gates.md, footer_widgets.md
├── skills/                        # Public slash-command skills (/scribe-notes, doubt, quiz, setfolder)
├── references/                    # Selective-loaded templates (masters/variants/subtemplates/modules),
│                                  #   routing registry, metadata policy, workflows & contracts
├── scriptorium/
│   ├── models.py, layout.py       # Shared ParsedNote cache, path/frontmatter/slug helpers, schemas
│   ├── triggers.py                # Executable A0-A11, T01-T16, MATH-01..10, TEACH-01..10 dispatch
│   └── engines/
│       ├── orchestration.py       # A0 Director (plus _interactive.py, _decision.py, _token_optimizer.py)
│       ├── knowledge.py           # A1 Map (plus _collection_intelligence.py)
│       ├── pedagogy.py            # A2 Tutor / A5 Writer (_instructional.py, _pedagogical_core.py, _explanation.py)
│       ├── mathematics.py         # M01-M14 equation deconstruction, shape checks & 12-step solving
│       ├── research.py            # A4 Researcher (ARRIE evidence & web-image discovery)
│       ├── quality.py             # A9 Checker (12-dim teaching quality, Beginner Simulation, audit)
│       ├── vault.py               # A10 Vault (Obsidian Properties, atomic writes, checkpoints)
│       └── composition/           # A3 Planner / A6 Visuals / A7 Assets / A8 Quiz (BVIA, LAVIA, media)
├── scripts/                       # 8 CLI entry points (scribe.py, plan_notes.py, scaffold_note.py,
│                                  #   validate_note.py, vault_index.py, vault_graph.py, patch_links.py, verify_vault_notes.py)
├── examples/                      # Read-only reference plans & runner fixtures
└── tests/                         # Unit, integration, visual, topic-independence & teaching suites
```

---

## Setup & Verification

1. **Prerequisites:** Python 3.10+, `PyYAML`, `Pillow`, and `pytest`.
2. **Vault Config:** Resolve target vault via CLI `--vault`, `SCRIPTORIUM_VAULT_PATH`, or `~/.scriptorium-config.json` (`/scribe-setfolder`). Comprehensive `M1` collections write directly under `<Vault>/<Topic>/` (`resolve_collection_layout`, `create_category_folders=false` default) with downloaded media under `assets/scriptorium/<slug>/`.
3. **Common Commands:**
```bash
python -m pytest -q
python scripts/scribe.py audit --inventory
python scripts/scribe.py notes start "/scribe-notes <Topic>" --vault "<Vault>"
python scripts/scribe.py notes compose --spec spec.json --vault "<Vault>" --drafts drafts.json --prepare
python scripts/vault_index.py "<Vault>" --discover --topic "<Topic>"
```

See [LICENSE](LICENSE), [system-overview.md](references/architecture/system-overview.md), [migration-notes.md](references/contracts/migration-notes.md), and [examples/adaptive-deepnotes/README.md](examples/adaptive-deepnotes/README.md).
