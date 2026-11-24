---
name: scribe-doubt
description: Answer a learner's question strictly from existing Obsidian vault notes with exact wikilink citations. Use for read-only questions about notes already in the user's vault.
---

# `/scribe-doubt`

Input: a question and an explicit or configured vault. Resolve the vault through [the destination policy](../../docs/procedures/authoring/pre-gen-gate.md), search and read the relevant notes, and answer only what they support. Cite each substantive claim with `[[Note Title]]` or `[[Note Title#Heading]]`; follow [Command A](../../docs/procedures/authoring/command-playbooks.md#command-a).

Output: an answer in chat. Do not edit files, create scripts, or browse externally. If the vault or answer is unavailable, say which part is missing; do not fill it from memory.
