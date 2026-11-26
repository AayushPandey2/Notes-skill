---
name: scribe-quiz
description: Quiz a learner interactively, one question at a time, using existing Obsidian vault notes. Use for /scribe-quiz, active recall, viva practice, or oral review of material already in the vault.
---

# `/scribe-quiz`

## Purpose & Activation

Run an interactive, **one-question-per-turn** active-recall or viva quiz grounded strictly in the learner's existing Obsidian vault notes, powered by [mastery-design.md](../../docs/procedures/authoring/mastery-design.md) and [revision-strategy.md](../../docs/procedures/learning/revision-strategy.md). Activate on `/scribe-quiz`, `"quiz me on my notes"`, or oral/viva review requests over existing vault material (for static Markdown practice files, route to `M6` in [assessment.md](../../docs/blueprints/formats/assessment.md) via `/scribe-notes`).

## Inputs & Discovery

- **Inputs:** Target topic, note title, or scope, plus the vault path from [pre-gen-gate.md](../../docs/procedures/authoring/pre-gen-gate.md).
- **Discovery:** Read only matching existing vault notes; do **not** browse the web or invent material absent from the notes.

## 7-Step Interactive Quiz Progression (One Question Per Turn)

Follow [Command G](../../docs/procedures/authoring/command-playbooks.md#command-g--interactive-vault-quiz-scribe-quiz):
1. **Select objective & mastery dimension:** Choose one concept and reasoning dimension (`Recognition`, `Explanation`, `Prediction`, `Diagnosis`, `Transfer`, etc.) from the existing note.
2. **Ask one question:** Present a prompt matched to the learner's demonstrated knowledge and wait for their reply.
3. **Classify the response:** Categorize as `correct`, `partially_correct`, `incorrect`, `ambiguous`, `unsupported_by_note`, or **`note_conflict`** (when the learner's response conflicts with an existing vault claim yet appears technically sound or highlights a potential error in the note—distinguish possible note defect from learner error without silently rewriting the vault or browsing externally).
4. **Diagnose likely gap with misconception uncertainty:** A wrong answer rarely establishes a single root cause on its own (e.g., an incorrect gradient might stem from derivative confusion, sign reversal, arithmetic slip, or misreading). Form a working hypothesis (*missing prerequisite, terminology confusion, invalid assumption, calculation error, mechanism misunderstanding, failed transfer*) without fabricating unstated history, and use a discriminating follow-up question to confirm which gap actually occurred.
5. **Repair understanding:** Cite supporting `[[Note Title#Heading]]` and provide a targeted explanation + discriminating example.
6. **Retest:** Before advancing on a missed concept, ask a **different** question testing the same underlying reasoning.
7. **Transfer & revision progression:** Advance to transfer/interleaved prompts only once understanding is demonstrated; keep vault notes unchanged by default unless the user explicitly asks to save weak spots to an existing body section (never add quiz-state YAML keys or create scripts).

## Failure Handling

- If the vault path is unconfigured or the target note is missing, ask for the vault/note or suggest `/scribe-notes`—never fabricate quiz answers.
- If a topic goes beyond the notes, state that the vault notes do not cover it and stay within covered material.
