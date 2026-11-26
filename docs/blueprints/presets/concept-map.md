# Preset: Concept Map & Knowledge Network (`M7` / `concept_map`)

- **Parent Master:** [M7 — Synthesis & Revision](../formats/synthesis-revision.md) (`single_artifact`).
- **Activation Trigger:** `"concept map"`, `"knowledge map"`, `"dependency graph for <topic>"` via `/scribe-notes`.

## Execution Overrides
1. **Typed Semantic Relationships:** Map concepts using explicit relationship types: `requires` (prerequisite—must remain acyclic), `causes`, `part_of`, `implements`, `measures`, `approximates`, `generalizes`, `contrasts`, and `contradicts`. Genuine conceptual cycles (e.g., feedback loops, bidirectional contrasts) are permitted outside `requires` edges ([revision-and-linking.md](../../procedures/updating/revision-and-linking.md)).
2. **Structured Representation:** Emit a clean `Concept | Relation | Target | Concise Bridge | Canonical Vault Link` table (paired with an inspected structural diagram from the permitted source hierarchy in [representations.md](../../procedures/authoring/representations.md) whenever permitted and available—falling back to the table alone only when visuals are unavailable or prohibited; never Mermaid or ASCII).
3. **Link Hygiene:** Separate `existing_note` wikilinks from `planned_note` (`nexttopics`) and plain-text `unresolved_concept` labels.
