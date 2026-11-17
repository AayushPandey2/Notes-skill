# Scriptorium

A modular, token-efficient Obsidian knowledge-engineering agent skill. Scriptorium researches topics from primary sources, builds interconnected seven-section Markdown lessons into an Obsidian vault, expands existing coverage incrementally, and answers learner questions strictly read-only from existing vault notes.

## Commands

- `/scribe-notes <topic>` — Research a topic from primary sources, build an acyclic subtopic DAG, and generate verified interconnected Markdown lessons.
- `/scribe-expand <topic name>` — Inspect existing vault coverage via the metadata index and incrementally add missing or advanced subtopics.
- `/scribe-doubt <topic name> <your doubt>` — Answer a question strictly read-only using existing vault notes with `[[Note Title]]` citations.
- `/scribe-distill <topic>` — Distill a topic's existing vault notes into a 1-page `<topic-slug>-CHEAT-SHEET.md` rapid-revision sheet.

## Repository Structure

```text
scriptorium/
├── SKILL.md                          # Progressive-loading command router
├── README.md
├── LICENSE                           # MIT License
├── references/
│   ├── research_protocol.md          # Phase 1 deterministic research SOP
│   ├── note_templates.md             # Authoritative 7-section note template
│   ├── cheatsheet_template.md        # 5-section 1-page cheat sheet template
│   └── verification_checklist.md     # Semantic quality rubric
└── scripts/
    ├── vault_index.py                # Compact JSON metadata & H2 heading indexer
    └── verify_vault_notes.py         # Read-by-default validator with --fix repairs
```

## Tools & Usage

### 1. Index the Obsidian Vault

```bash
python3 scripts/vault_index.py "<vault_path>" [--topic "<topic_filter>"]
```

Outputs a compact JSON array containing `file`, `id`, `title`, `aliases`, `topic`, `master_topic`, `depends_on`, `next_topic`, `status`, and level-2 `headings` without loading full note bodies.

### 2. Validate & Auto-Repair Notes

```bash
# Read-only audit
python3 scripts/verify_vault_notes.py "<vault_path>"

# Apply mechanical repairs (inline math spacing, quoted headings, title aliases, callout blank lines)
python3 scripts/verify_vault_notes.py "<vault_path>" --fix
```

## Configuration

Set `[PATH_TO_OBSIDIAN_VAULT]` via `SCRIPTORIUM_VAULT_PATH` or `~/.scriptorium-config.json`:

```json
{
  "vault_path": "C:\\path\\to\\YourObsidianVault"
}
```

## License

Released under the [MIT License](LICENSE).
