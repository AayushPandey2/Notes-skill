---
name: scribe-quiz
description: Quiz a learner interactively, one question at a time, using existing Obsidian vault notes. Use for /scribe-quiz, active recall, viva practice, or oral review of material already in the vault.
---

# `/scribe-quiz`

## Purpose & Activation

Run an interactive, **one-question-per-turn** active-recall or viva quiz in chat grounded strictly in the learner's existing Obsidian vault notes. Activate on `/scribe-quiz`, `"quiz me on my notes"`, or oral/viva review requests over existing vault material (for static Markdown practice sheets or mock-exam files, route to `M6` in [assessment.md](../../docs/blueprints/formats/assessment.md) via `/scribe-notes` instead).

## Inputs & Discovery

- **Inputs:** Target topic, note title, or scope (e.g., recall, calculation, viva), plus the vault path from [the destination gate](../../docs/procedures/authoring/pre-gen-gate.md).
- **Discovery:** Read only the matching existing vault notes; do **not** browse the web or invent material absent from the notes.

## Interactive Workflow

Follow [Command G](../../docs/procedures/authoring/command-playbooks.md#command-g--interactive-vault-quiz-scribe-quiz):
1. **Ask one question per turn:** Start with foundational recall or intuition, then escalate to mechanism, worked application/trace, and boundary/viva stress-tests based on the learner's answers. Wait for the learner's reply before grading or asking the next question.
2. **Grade & remediate:** Evaluate the learner's response against the notes, cite the exact supporting `[[Note Title#Heading]]`, explain *why* any mistake occurred, and offer a targeted follow-up or the next question.
3. **No unsolicited file writes:** Keep all vault notes unchanged by default and never add YAML keys for quiz state. Only if the learner explicitly asks to save weak spots, append a concise note to an existing body review section without altering custom YAML or unrelated text.

## Failure Handling

- If the vault path is unconfigured or the target note does not exist, ask for the vault/note or suggest creating it with `/scribe-notes`—never fabricate quiz answers.
- If a question goes beyond what the notes cover, state that the vault notes do not support it and stick to covered material. Do not create scripts.
