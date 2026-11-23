---
name: scribe-quiz
description: Run an interactive one-question-at-a-time active-recall quiz over existing Obsidian vault notes and log weak spots cleanly. Use whenever the user wants to test themselves, review flashcards/viva prompts, practice recall on existing notes, or run /scribe-quiz.
---

# `/scribe-quiz`

Run focused active-recall quizzing against existing vault notes without overwhelming the learner or polluting note frontmatter.

## Procedure

1. Follow [router.md](../../router.md) and [Command G](../../references/workflows/notes-creation/command-playbooks.md#command-g) under master `M6` (`mock_exam` behavior) without loading full M1 composition specs.
2. Read the target note(s), then ask **one question at a time** and wait for the learner's answer before revealing feedback or moving on—multi-question dumps defeat active recall.
3. Grade the response strictly against what the note supports, give concise corrective feedback referencing `[[Note Title#Heading]]`, and optionally record weak spots in the note's body review section directly (never inject extra YAML frontmatter keys or generate scripts).
