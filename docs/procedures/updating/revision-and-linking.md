# Revision, Knowledge Synthesis & Vault Linking

## Purpose & Activation Trigger

Govern condensed revision sections inside `M1`/`M2` notes, standalone `M3`/`M7` revision outputs (`revision_pack`, `concept_map`), and safe vault wikilink maintenance.

## Decision Rules & Integrity Contract

1. **No Paragraph Duplication:** Keep the full `M1`/`M2` note authoritative for derivations and citations; build revision sections and `M3`/`M7` packs as structured retrieval cues pointing back to canonical headings rather than copying paragraphs or inventing claims.
2. **Preserve Formula Hypotheses:** Retain domain and applicability assumptions on every condensed equation.
3. **Concept vs. File Relationships & Acyclicity:** Distinguish verified `existing_note` wikilinks from `planned_note` (`nexttopics`), external URLs, and plain-text unresolved concepts. **Apply DAG acyclicity strictly to `requires` (prerequisite) dependencies**—related-topic links, bidirectional contrasts, and genuine conceptual cycles (such as feedback loops) are allowed.
4. **Link & Identifier Edge-Case Hygiene:** Use path-qualified wikilinks when identical note names exist in different folders, resolve ambiguous aliases before linking, recheck heading anchors after edits, keep excluded concepts out of automatic prerequisite/`nexttopics` links, and create reciprocal companion links **only** for artifacts that actually exist.

## Execution & Review

Inspect target notes before updating wikilinks, verify prerequisite (`requires`) acyclicity manually, and review against [verification-checklist.md](../review/verification-checklist.md).
