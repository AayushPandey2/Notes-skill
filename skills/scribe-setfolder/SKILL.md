---
name: scribe-setfolder
description: Configure and persist the default Obsidian vault and target notes folder path in ~/.scriptorium-config.json so all generated notes save to the chosen location. Use whenever the user runs /scribe-setfolder or wants to set, change, or verify where Scriptorium writes Obsidian notes.
---

# `/scribe-setfolder`

Persist the user's preferred Obsidian vault root and notes subfolder so every downstream `/scribe-notes`, `/scribe-doubt`, and `/scribe-quiz` run resolves the same destination reliably.

## Procedure

1. Validate the supplied folder path: confirm it exists (or create it only if the user explicitly confirms) and locate the vault root (nearest parent containing `.obsidian/`, or the folder itself if no `.obsidian/` exists).
2. Read `~/.scriptorium-config.json` if present, update `vault_path`, `notes_folder` (relative path from `vault_path`, or `""` if root), and `notes_path`, and write clean formatted JSON back to `~/.scriptorium-config.json` directly using native file tools (never generate a helper script).
3. Report the saved `vault_path`, `notes_folder`, and resolved `notes_path` (`create_category_folders=false` remains default so Scriptorium writes collections directly under that configured target rather than inventing extra nested category directories).
