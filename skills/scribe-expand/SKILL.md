---
name: scribe-expand
description: "Audit existing Obsidian vault coverage and template style (deepnotes vs notes) via index and incrementally expand missing or advanced subtopics."
---

Dispatch `/scribe-expand` with the user arguments through [the router](../../router.md). Load only its matching command branch (`Command B`). Inspect `detected_workflow` from `vault_index.py --discover` (`"deepnotes"` vs `"notes"`) so missing subtopics automatically match the topic's existing research depth and template (`deepstudy-master` vs `studynotes`).
