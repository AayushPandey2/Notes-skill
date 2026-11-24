---
name: scribe-quiz
description: Quiz a learner interactively, one question at a time, using existing Obsidian vault notes. Use for active recall, viva practice, or review of material already in the vault.
---

# `/scribe-quiz`

Input: a topic or note and an explicit or configured vault. Read the relevant notes and follow [Command G](../../docs/procedures/authoring/command-playbooks.md#command-g). Ask one question and wait for the learner's answer before grading or asking another. Ground feedback in the notes with exact wikilinks, and state when they do not support an answer.

Output: an interactive quiz in chat. Keep notes unchanged by default; record weak spots in an existing body review section only if the learner asks for a saved record. Preserve YAML and unrelated note text. Do not create scripts.
