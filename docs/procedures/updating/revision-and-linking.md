# Revision, Knowledge Synthesis & Vault Linking

## Purpose & Activation Trigger

Govern condensed revision sections inside `M1`/`M2` notes, standalone `M3`/`M7` revision outputs (`revision_pack`, `concept_map`), and safe vault wikilink maintenance.

## Decision Rules & Integrity Contract

1. **No Paragraph Duplication:** Keep the full `M1`/`M2` note authoritative for derivations and citations; build revision sections and `M3`/`M7` packs as structured retrieval cues pointing back to canonical headings rather than copying paragraphs or inventing claims.
2. **Preserve Formula Hypotheses:** Retain domain and applicability assumptions on every condensed equation.
3. **Link & Acyclicity Hygiene:** Distinguish verified `existing_note` wikilinks from `planned_note` (`nexttopics`), external URLs, and plain-text unresolved concepts. Link only prerequisite, contrast, or revision anchors that resolve cleanly.

## Execution & Review

Inspect target notes before updating wikilinks, verify DAG acyclicity manually, and review against [verification-checklist.md](../review/verification-checklist.md).
