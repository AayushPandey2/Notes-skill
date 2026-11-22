---
name: scribe-doubt
description: Answer questions strictly read-only from existing Obsidian vault notes using exact wikilink citations. Use whenever the user asks a doubt, clarification, lookup, or /scribe-doubt question about notes already stored in their Obsidian vault without editing files or fetching external web facts.
---

# `/scribe-doubt`

Answer learner questions strictly from existing vault notes so the user can trust every claim as grounded in their own library rather than external speculation.

## Procedure

1. Follow [router.md](../../router.md) and [Command A](../../references/workflows/notes-creation/command-playbooks.md#command-a) strictly (skip note-creation templates and interactive configuration gates).
2. Index only the relevant vault scope (`python scripts/vault_index.py "<vault>" --discover --topic "<topic>"`) and read the matching notes directly.
3. Explain clearly from those notes, citing every claim with exact wikilinks (`[[Note Title]]` or `[[Note Title#Heading]]`).
4. **Hard boundaries:** Perform zero file writes and zero external web research. If the vault does not cover part of the question, state the gap explicitly instead of filling it from memory.
