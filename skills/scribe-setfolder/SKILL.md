---
name: scribe-setfolder
description: Set or inspect the default Obsidian vault and notes folder used by Scriptorium. Use for /scribe-setfolder or a request to change where Scriptorium writes notes.
---

# `/scribe-setfolder`

Input: a folder path or a request to inspect the current setting. Locate the vault root using its `.obsidian/` directory; if there is no such directory, ask which folder is the vault before saving. Confirm the selected notes folder is inside that vault, reject `..` and links that escape it, and use native file tools to read or update `~/.scriptorium-config.json` directly. Store `vault_path`, vault-relative `notes_folder`, and resolved `notes_path`; preserve unrelated settings.

Output: the saved or current paths, and whether the folder exists. If access is declined or unavailable, report that the setting could not be saved or inspected. Limit changes to configuration and the explicitly approved folder, if it needs to be created. Subsequent note-writing requests use the [destination policy](../../docs/procedures/authoring/pre-gen-gate.md).
