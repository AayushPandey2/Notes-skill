# Multi-Layer Revision, Knowledge Synthesis & Vault Linking

Use this workflow when generating revision layers within `M1`/`M2` notes or standalone `M3`/`M7` revision artifacts.

## 1. Three Complementary Layers
- **Layer A (Authoritative Full Note):** Primary learning note (`M1` or `M2`) holding complete derivations, mechanisms, examples, and citations.
- **Layer B (Structured Concept Review):** Core definitions, key equations with applicability conditions, critical distinctions, and point-of-need caveats pointing back to Layer A headings.
- **Layer C (Rapid Revision):** Compact scannable retrieval cues or linked `M3`/`M7` artifact (`Cheatsheets/`, `comparison/`). Never repeat Layer A paragraphs verbatim and never introduce unsupported new claims.

## 2. Revision Integrity Rules
1. Every condensed formula must preserve its domain/applicability assumptions (`pedagogical_engine.validate_revision_integrity`).
2. Every internal anchor (`[[#Heading]]`) must resolve to an existing Layer A heading.
3. Cross-topic links resolve through `vault_index.py` / `vault_graph.py`, distinguishing `existing_note`, `planned_note` (listed in YAML `nexttopics`), `external_resource`, and `unresolved_concept` (plain text).
4. Avoid link inflation—link only concepts supporting prerequisite review, comparison, application, or revision.
5. For safe frontmatter/link maintenance across an existing vault, use `scripts/patch_links.py --dry-run` first and verify acyclicity with `scripts/vault_graph.py --check-cycles`.
