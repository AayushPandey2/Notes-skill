---
name: scribe-atomic-notes
description: "Generate a fast, lightweight atomic note in Atomic Notes/<topic_name>.md via a single direct web search/fetch without deep multi-wave research. Usage: /scribe-atomic-notes <topic name>"
---

# `/scribe-atomic-notes`

Resolve the Scriptorium base directory (`../scriptorium/`, `~/.gemini/config/skills/scriptorium/`, `~/.claude/skills/scriptorium/`, or `~/.codex/skills/scriptorium/`). Read its `router.md` and dispatch `/scribe-atomic-notes $ARGUMENTS` (`## Command H` in `references/command_playbooks.md`). Bypass deep multi-hop research workflows: perform a single, direct web search/fetch for `$ARGUMENTS`, populate `templates/atomic.md` applying the mandatory **Humanization & Cohesion Pass**, and save to the centralized `Atomic Notes/` folder (`Atomic Notes/<topic_name>.md`) at the same directory level as the `<subtopic>/` folders.
