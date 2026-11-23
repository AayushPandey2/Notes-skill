# Scriptorium Reference Library (Selective Loading Index)

Load **only** the reference matching the active request and trigger. Bulk-loading `references/` defeats progressive disclosure.

## Selective Reference Map

| Domain | Canonical File | Load Only When |
|---|---|---|
| **Architecture Overview** | [architecture/system-overview.md](architecture/system-overview.md) | Inspecting Scriptorium's instruction-only role map and boundaries |
| **Template & Module Catalog** | [architecture/template-module-catalog.md](architecture/template-module-catalog.md) | Resolving `M1`–`M7`, variants, subtemplates, or module compatibility |
| **Routing & Precedence** | [routing/routing-policy.md](routing/routing-policy.md), [routing/master-registry.yaml](routing/master-registry.yaml) | Resolving command precedence, negation handling, or multi-artifact splits |
| **Pre-Generation Gate** | [workflows/notes-creation/pre-gen-gate.md](workflows/notes-creation/pre-gen-gate.md) | Resolving vault configuration, overlap checks, and placement |
| **Command Playbooks** | [workflows/notes-creation/command-playbooks.md](workflows/notes-creation/command-playbooks.md) | Dispatching `/scribe-doubt`, `/scribe-quiz`, `/scribe-ytnote`, or `/scribe-notes` branches |
| **Adaptive Planning (`M1`/`M2`)** | [workflows/notes-creation/adaptive-engine.md](workflows/notes-creation/adaptive-engine.md), [workflows/notes-creation/instructional-registry.json](workflows/notes-creation/instructional-registry.json) | Planning concept depths (`0–5`), prerequisites, and subtemplate sequences |
| **Pedagogy & Clarity (`P01`–`P11`, `EIS`)** | [workflows/notes-creation/pedagogical-intelligence.md](workflows/notes-creation/pedagogical-intelligence.md) | Enriching explanations, analogies, cognitive load, or `CF-01`–`CF-12` clarity |
| **Comprehensive `M1` Composition** | [workflows/notes-creation/composition-contract.md](workflows/notes-creation/composition-contract.md), [contracts/composition-integrity.md](contracts/composition-integrity.md) | Authoring comprehensive `M1` topic collections with 5-key YAML |
| **Syllabus Boundary** | [workflows/notes-creation/syllabus-template.md](workflows/notes-creation/syllabus-template.md) | Locking allowed subtopics in a multi-note curriculum MOC |
| **Visuals & Media (`BVIA`/`LAVIA`)** | [workflows/notes-creation/representations.md](workflows/notes-creation/representations.md) | Acquiring external web/video raster visuals under `assets/scriptorium/<slug>/` |
| **ARRIE Research & Sources** | [workflows/research/research-engine.md](workflows/research/research-engine.md), [workflows/research/source-fidelity.md](workflows/research/source-fidelity.md) | Planning evidence (`R-S0`–`R-R`), citations, or source coverage |
| **Further-Learning Resources** | [workflows/research/resource-recommendations.md](workflows/research/resource-recommendations.md) | Curating graded learning resources separately from factual citations |
| **Revision & Vault Linking** | [workflows/revision/revision-and-linking.md](workflows/revision/revision-and-linking.md) | Writing Layer B/C revision summaries or updating vault links safely |
| **Manual Verification** | [workflows/validation/verification-checklist.md](workflows/validation/verification-checklist.md) | Reviewing finished notes for factual, mathematical, visual, and link quality |
| **Obsidian Properties & Naming** | [metadata/properties-policy.md](metadata/properties-policy.md), [metadata/tag-taxonomy.md](metadata/tag-taxonomy.md) | Building frontmatter, normalized tags, filenames, or multi-artifact updates |
| **Masters, Variants, Subtemplates, Modules** | `templates/masters/`, `templates/variants/`, `templates/subtemplates/`, [templates/modules/module-catalog.md](templates/modules/module-catalog.md) | Loading the single selected output product and active knowledge-type structure |
| **Migration History** | [contracts/migration-notes.md](contracts/migration-notes.md) | Tracing retired command aliases or architectural transitions |
