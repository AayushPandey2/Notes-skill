# Variant: Active-Recall Flashcards

- **Purpose:** Generate atomic spaced-repetition front/back cards enforcing crisp condition and trap awareness.
- **Parent Master:** [M6 — Practice & Assessment](../masters/assessment.md) (`flashcards`)
- **Activation Trigger:** `"flashcards"`, `"spaced-repetition cards"` via `/scribe-notes`.
- **Inputs & Dependencies:** Verified note claims, definitions, bounds, and common misconceptions; [authoring_rules.md](../../../shared/authoring_rules.md).
- **Execution Overrides:**
  1. Enforce one testable claim per card (definition, distinction, condition, or complexity bound—never essays).
  2. Pair a visible **Front** prompt with an unquoted blank line and collapsed `> [!tip]- Back` callout (`>` on every interior line) stating the concise answer, condition, and 1-line trap.
  3. Order progression: recognition -> distinction -> boundary application.
- **Failure Handling & Validation:** Reject unquoted callout blanks or multi-concept prompts via `scripts/validate_note.py`.
