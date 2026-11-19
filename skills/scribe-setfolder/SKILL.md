---
name: scribe-setfolder
description: "Set the target Obsidian notes folder path in ~/.scriptorium-config.json so all generated notes are saved there. Usage: /scribe-setfolder <folder path>"
---

# `/scribe-setfolder`

Resolve the Scriptorium base directory (`../scriptorium/`, `~/.gemini/config/skills/scriptorium/`, `~/.claude/skills/scriptorium/`, or `~/.codex/skills/scriptorium/`) and run:

```sh
python3 <skill_dir>/scripts/plan_notes.py setfolder "$ARGUMENTS"
```

Report the saved `vault_path`, `notes_folder`, and `notes_path` from `~/.scriptorium-config.json`.
