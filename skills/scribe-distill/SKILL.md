---
name: scribe-distill
description: "Compress a topic's existing Obsidian notes into a 1-page cheatsheet in the centralized Cheatsheets/ folder. Usage: /scribe-distill <topic>"
---

# `/scribe-distill`

Resolve the Scriptorium base directory (`../scriptorium/`, `~/.gemini/config/skills/scriptorium/`, `~/.claude/skills/scriptorium/`, or `~/.codex/skills/scriptorium/`). Read its `router.md` and dispatch `/scribe-distill $ARGUMENTS`, saving the generated cheatsheet inside the centralized `Cheatsheets/` folder (`Cheatsheets/<topic-slug>-CHEAT-SHEET.md` or `Cheatsheets/<topic-slug>-<subtopic-slug>-CHEAT-SHEET.md`) at the same sibling directory level as the `<subtopic>/` folders. Use the matching command playbook and the per-note loading rules.
