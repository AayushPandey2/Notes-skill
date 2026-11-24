# Variant: Concept Map & Knowledge Network

- **Purpose:** Map prerequisite, generalization, contrast, and dependency structure across an entire topic or vault cluster cleanly.
- **Parent Master:** [M7 — Synthesis & Revision](../formats/synthesis-revision.md) (`concept_map`)
- **Activation Trigger:** `"concept map"`, `"knowledge map"`, `"dependency graph for <topic>"` via `/scribe-notes`.
- **Inputs & Dependencies:** Existing vault notes, canonical concept relationships, [revision-and-linking.md](../../procedures/updating/revision-and-linking.md).
- **Execution Overrides:**
  1. Embed an inspected local web concept/architecture diagram ([representations.md](../../procedures/authoring/representations.md)) where available (never Mermaid or ASCII), and structure every relationship explicitly via typed edges (`requires`, `generalizes`, `contrasts`, `feeds`) in the Semantic Connection Table below.
  2. Follow with a Semantic Connection Table: `Concept | Relation | Target | Concise Bridge | Canonical Vault Link`.
  3. Separate `existing_note` wikilinks from `planned_note` (`nexttopics`) and plain-text `unresolved_concept` labels.
- **Failure Handling & Validation:** Reject cyclic prerequisite graphs or fabricated links ([verification-checklist.md](../../procedures/review/verification-checklist.md)).
