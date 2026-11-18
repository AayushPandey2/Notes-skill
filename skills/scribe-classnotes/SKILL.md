---
name: scribe-classnotes
description: "Fast multi-subtopic class notes generator replicating /scribe-notes structure without deep research, defaulting strictly to templates/classnotes.md and banning deepstudy-coding/deepstudy-general. Usage: /scribe-classnotes <topic name>"
---

# `/scribe-classnotes`

Resolve the Scriptorium base directory (`../scriptorium/`, `~/.gemini/config/skills/scriptorium/`, `~/.claude/skills/scriptorium/`, or `~/.codex/skills/scriptorium/`). Read its `router.md` and dispatch `/scribe-classnotes $ARGUMENTS` (`## Command I` in `references/command_playbooks.md`).

- **Multi-File Subtopic Architecture:** Replicate `/scribe-notes` topic decomposition and multi-file output structure (`00-MOC-<topic-slug>.md` + numbered subtopic files in `<topic-folder>/`, with auxiliary practice sets, cheatsheets, and atomic notes routed to sibling `Practice Sets/`, `Cheatsheets/`, and `Atomic Notes/`).
- **Bypass Deep Research:** Skip `references/research_protocol.md` multi-wave deep research; perform fast, direct web searches/fetches only.
- **Template Rules:** Default core subtopic notes strictly to `templates/classnotes.md` (auxiliary `cheat-sheet`, `comparison`, `practice`, `atomic`, `api-table` allowed when appropriate). **Strictly prohibit `deepstudy-coding` and `deepstudy-general`** (`deepnotes-coding` / `deepnotes-general`) under all circumstances.
- **Math & Style Guardrails:** Minimize mathematical notation (`math_level: 0` by default; include LaTeX equations only when strictly essential to an inherently mathematical, physical, or quantitative engineering topic). Apply the mandatory **Humanization & Cohesion Pass**.
