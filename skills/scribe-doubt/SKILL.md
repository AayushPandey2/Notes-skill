---
name: scribe-doubt
description: Answer questions strictly read-only from existing Obsidian vault notes using exact wikilink citations. Use whenever the user asks a doubt, clarification, lookup, or /scribe-doubt question about notes already stored in their Obsidian vault without editing files or fetching external web facts.
---

# `/scribe-doubt`

Answer learner questions strictly from existing vault notes so every claim is grounded in the user's own library rather than external speculation.

## Procedure

1. Follow [router.md](../../router.md) and [Command A](../../references/workflows/notes-creation/command-playbooks.md#command-a) strictly (skip note-creation templates and interactive configuration gates).
2. Resolve the active vault (`~/.scriptorium-config.json` or explicit path), search matching Markdown files directly using native file/search tools, and read the relevant notes.
3. Explain clearly from those notes, citing every claim with exact wikilinks (`[[Note Title]]` or `[[Note Title#Heading]]`).
4. **Hard boundaries:** Perform zero file writes, zero script generation, and zero external web research. If the vault does not cover part of the question, state the gap explicitly instead of filling it from memory.
