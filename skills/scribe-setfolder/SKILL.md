---
name: scribe-setfolder
description: Configure and persist the default Obsidian vault and target notes folder path in ~/.scriptorium-config.json so all generated notes save to the chosen location. Use whenever the user runs /scribe-setfolder or wants to set, change, or verify where Scriptorium writes Obsidian notes.
---

# `/scribe-setfolder`

Persist the user's preferred Obsidian vault root and notes subfolder so every downstream `/scribe-notes`, `/scribe-doubt`, and `/scribe-quiz` run resolves the same destination reliably.

## Procedure

1. Resolve the active Scriptorium base directory (repository root, `~/.gemini/antigravity/skills/scriptorium/`, `~/.gemini/config/skills/scriptorium/`, or `~/.codex/skills/scriptorium/`).
2. Execute the folder setup CLI with the supplied path arguments:
   ```sh
   python "<skill_dir>/scripts/plan_notes.py" setfolder "<folder path>"
   ```
3. Report the saved `vault_path`, `notes_folder`, and resolved `notes_path` from `~/.scriptorium-config.json` (remember `create_category_folders=false` remains default so Scriptorium writes collections directly under that configured target rather than inventing extra nested category directories).
