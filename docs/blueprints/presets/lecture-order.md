# Variant: Lecture / Source-Order Study Notes

- **Purpose:** Preserve the exact teaching sequence, terminology, and example interleaving of a lecture, video, PDF, or chapter without artificial reorganization.
- **Parent Master:** [M2 — Structured Study Notes](../formats/study-notes.md) (`lecture_order`)
- **Activation Trigger:** Supplied lecture, PDF, slide deck, video (`/scribe-ytnotes`), or `"preserve order"` / `"study notes"` via `/scribe-notes`.
- **Inputs & Dependencies:** Verified source segments, locators (page/heading/timestamp); [source-fidelity.md](../../procedures/sourcing/source-fidelity.md), [math_gates.md](../../../core/math_gates.md). (For videos, use transcript timestamps only—never play video or capture video frames.)
- **Execution Overrides:**
  1. Interleave examples right beside the concept they demonstrate in Section 2 rather than hoisting all examples into a later summary section.
  2. Insert labeled `[Educational Addition — Prerequisite Bridge]` micro-explanations inline right before dependent notation instead of silently reordering sections.
  3. Attach locator anchors (pages, sections, timestamps) and `[UNVERIFIED]` / gap markers cleanly whenever source segments are inaccessible.
- **Failure Handling & Validation:** Reject unattributed section reordering or invented missing source pages ([source-fidelity.md](../../procedures/sourcing/source-fidelity.md)).
