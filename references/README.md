# Scriptorium Reference Library (Selective Loading Index)

Load **only** the reference matching the active request and trigger. Bulk-loading `references/` defeats progressive disclosure (`scripts/scribe.py optimize --compile` handles automated bundle selection).

## Selective Reference Map

| Domain | Canonical File | Load Only When |
|---|---|---|
| **Architecture & Ownership** | [architecture/system-overview.md](architecture/system-overview.md) | Inspecting the six-engine ownership map (`E1`–`E6`), lifecycle, or token optimizer |
| **Template & Module Catalog** | [architecture/template-module-catalog.md](architecture/template-module-catalog.md) | Resolving `M1`–`M7`, variants, subtemplates, or module compatibility |
| **Routing & Precedence** | [routing/routing-policy.md](routing/routing-policy.md), [routing/master-registry.yaml](routing/master-registry.yaml) | Resolving command precedence, negation handling, or multi-artifact splits |
| **Pre-Generation Gate** | [workflows/notes-creation/pre-gen-gate.md](workflows/notes-creation/pre-gen-gate.md) | Running interactive session setup, vault indexing, and placement resolution |
| **Command Playbooks** | [workflows/notes-creation/command-playbooks.md](workflows/notes-creation/command-playbooks.md) | Dispatching `/scribe-doubt`, `/scribe-quiz`, `/scribe-ytnotes`, or `/scribe-notes` branches |
| **Adaptive Planning (`M1`/`M2`)** | [workflows/notes-creation/adaptive-engine.md](workflows/notes-creation/adaptive-engine.md), [workflows/notes-creation/instructional-registry.json](workflows/notes-creation/instructional-registry.json) | Planning concept depths (`0–5`), prerequisites, and subtemplate sequences |
| **Pedagogy & Clarity (`P01`–`P11`, `EIS`)** | [workflows/notes-creation/pedagogical-intelligence.md](workflows/notes-creation/pedagogical-intelligence.md) | Enriching explanations, analogies, cognitive load, or `CF-01`–`CF-12` clarity |
| **KCP v2 Composition & Integrity** | [workflows/notes-creation/composition-contract.md](workflows/notes-creation/composition-contract.md), [contracts/composition-integrity.md](contracts/composition-integrity.md) | Publishing comprehensive 5–10 chapter `M1` topic collections with 5-key YAML |
| **Syllabus Boundary** | [workflows/notes-creation/syllabus-template.md](workflows/notes-creation/syllabus-template.md) | Locking allowed subtopics in a multi-note curriculum MOC |
| **Visuals & Media (`BVIA`/`LAVIA`)** | [workflows/notes-creation/representations.md](workflows/notes-creation/representations.md) | Acquiring external web/video raster visuals under `assets/scriptorium/<slug>/` |
| **ARRIE Research & Sources** | [workflows/research/research-engine.md](workflows/research/research-engine.md), [workflows/research/source-fidelity.md](workflows/research/source-fidelity.md) | Planning evidence (`R-S0`–`R-R`), citations, or source coverage receipts |
| **Further-Learning Resources** | [workflows/research/resource-recommendations.md](workflows/research/resource-recommendations.md) | Curating graded learning resources separately from factual citations |
| **Revision & Vault Linking** | [workflows/revision/revision-and-linking.md](workflows/revision/revision-and-linking.md) | Writing Layer B/C revision summaries or patching vault links safely |
| **Semantic Validation** | [workflows/validation/verification-checklist.md](workflows/validation/verification-checklist.md) | Running post-draft factual, representation, and clarity checks |
| **Obsidian Properties & Naming** | [metadata/properties-policy.md](metadata/properties-policy.md), [metadata/tag-taxonomy.md](metadata/tag-taxonomy.md) | Building frontmatter, normalized tags, filenames, or multi-artifact updates |
| **Masters, Variants, Subtemplates, Modules** | `templates/masters/`, `templates/variants/`, `templates/subtemplates/`, [templates/modules/module-catalog.md](templates/modules/module-catalog.md) | Loading the single selected output product and active knowledge-type structure |
| **Migration History** | [contracts/migration-notes.md](contracts/migration-notes.md) | Tracing retired command aliases (`from_legacy`) or historical template renames |
