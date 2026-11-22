# Multi-Layer Revision, Knowledge Synthesis & Vault Linking

## Purpose & Activation Trigger

Govern condensed Layer B/C revision sections inside `M1`/`M2` notes, standalone `M3`/`M7` revision outputs (`revision_pack`, `concept_map`), and safe vault wikilink maintenance (`T02`, `T14`, `P08`, `P11`).

## Decision Rules & Integrity Contract

1. **Three Layers Without Duplication:** Keep **Layer A** (`M1`/`M2` main note) authoritative for complete derivations and citations; build **Layer B** (definitions, key formulas + conditions, critical distinctions) and **Layer C** (`M3`/`M7` rapid review) as structured retrieval cues pointing to Layer A headings rather than copying paragraphs or inventing claims.
2. **Preserve Formula Hypotheses:** Every condensed equation retains domain/applicability assumptions (`validate_revision_integrity`).
3. **Link & Acyclicity Hygiene:** Distinguish verified `existing_note` wikilinks from `planned_note` (`nexttopics`), external URLs, and plain-text `unresolved_concept` items. Avoid link inflation—link only prerequisite, contrast, or revision anchors resolving cleanly via `vault_index.py` / `vault_graph.py`.

## Execution & Validation

- Patch vault links safely with `scripts/patch_links.py --dry-run` before writing, and verify DAG acyclicity with `scripts/vault_graph.py --check-cycles` and `scripts/verify_vault_notes.py`.
