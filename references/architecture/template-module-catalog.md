# Scriptorium Template, Variant, Subtemplate & Module Usage Catalog

Authoritative inventory of all active templates, variants, subtemplates, and reusable modules registered in [master-registry.yaml](../routing/master-registry.yaml) and [instructional-registry.json](../workflows/notes-creation/instructional-registry.json).

## 1. Taxonomy Boundaries

- **Master Templates (`M1`–`M7`):** The seven canonical output product families.
- **Variants (`12`):** Presentation forms specializing an existing master without creating a new master family.
- **Subtemplates (`6` domain-independent files covering `10` registry knowledge types):** Specialized teaching structures orthogonal to master selection.
- **Modules (`17` registered in `master-registry.yaml`, aligned with `18` fine-grained entries in `instructional-registry.json`):** Distinctly classified into **Instructional**, **Validation**, and **Processing** capabilities.
- **Workflows:** Multi-step operational procedures under `references/workflows/` (never confused with templates or modules).

---

## 2. Master Template Catalog (`M1`–`M7`)

| ID | Name | Canonical Path | Primary Intent | Supported Variants | Default Modules | Reachability |
|---|---|---|---|---|---|---|
| `M1` | Deep Learning Notes | [deep-notes.md](../templates/masters/deep-notes.md) | `comprehensive_learning` | *(none; uses subtemplates + depth 0–5)* | `prerequisites`, `progressive_explanation`, `worked_examples`, `representation_alignment`, `misconception_prevention`, `revision_summary` | Active (default for `/scribe-notes <topic>`) |
| `M2` | Structured Study Notes | [study-notes.md](../templates/masters/study-notes.md) | `structured_study` | `lecture_order` | `progressive_explanation`, `worked_examples`, `revision_summary` | Active (sources, lectures, syllabi) |
| `M3` | Quick Reference & Cheat Sheet | [quick-reference.md](../templates/masters/quick-reference.md) | `rapid_reference` | `formula_sheet`, `syntax_reference`, `command_reference`, `atomic_card` | `representation_alignment`, `revision_summary` | Active (cheat sheets, formula sheets, atomic cards) |
| `M4` | Worked Problems & Solutions | [worked-solutions.md](../templates/masters/worked-solutions.md) | `worked_problem_solving` | *(none)* | `worked_examples`, `mathematical_derivation`, `misconception_prevention` | Active (problem sets, step-by-step solutions) |
| `M5` | Implementation & Technical Guide | [implementation-guide.md](../templates/masters/implementation-guide.md) | `practical_implementation` | *(none)* | `code_explanation`, `executable_verification`, `worked_examples`, `misconception_prevention` | Active (algorithms, from-scratch builds, debugging) |
| `M6` | Practice & Assessment | [assessment.md](../templates/masters/assessment.md) | `knowledge_assessment` | `flashcards`, `mock_exam` | `active_recall`, `misconception_prevention` | Active (practice sets, F13 assessments, `/scribe-quiz`) |
| `M7` | Synthesis & Revision | [synthesis-revision.md](../templates/masters/synthesis-revision.md) | `synthesis_and_revision` | `comparison_guide`, `paper_breakdown`, `quick_summary`, `revision_pack`, `concept_map` | `comparisons`, `cross_topic_connections`, `revision_summary` | Active (comparisons, F10 synthesis, concept maps, URL summaries) |

---

## 3. Variant Catalog (`12` Registered Variants)

| Variant ID | Parent Master | Canonical Path | Intended Output | Selection Condition | Reachability |
|---|---|---|---|---|---|
| `lecture_order` | `M2` | [lecture-order.md](../templates/variants/lecture-order.md) | Sequential source/chapter notes | Supplied lecture/PDF/chapter + `"preserve order"` / `"study notes"` | Active |
| `formula_sheet` | `M3` | [formula-sheet.md](../templates/variants/formula-sheet.md) | Compact equations + units + conditions | `"formula sheet"`, `"cheat sheet for ... formulas"` | Active |
| `syntax_reference` | `M3` | [syntax-reference.md](../templates/variants/syntax-reference.md) | Workflow-grouped API signatures & recipes | `"syntax reference"`, `"api table"` | Active |
| `command_reference` | `M3` | [command-reference.md](../templates/variants/command-reference.md) | CLI commands, flags, operational warnings | `"command reference"`, `"cli reference"` | Active |
| `atomic_card` | `M3` | [atomic-card.md](../templates/variants/atomic-card.md) | Single-concept transcludable card (`<150` words) | `"atomic note"`, `"atomic card"` | Active |
| `flashcards` | `M6` | [flashcards.md](../templates/variants/flashcards.md) | Active-recall front/back cards | `"flashcards"` | Active |
| `mock_exam` | `M6` | [mock-exam.md](../templates/variants/mock-exam.md) | Timed mock exam / viva prep with rubrics | `"mock exam"`, `"viva"`, `/scribe-quiz` | Active |
| `comparison_guide` | `M7` | [comparison-guide.md](../templates/variants/comparison-guide.md) | Multi-axis trade-off matrix & decision rule | `"compare A vs B"`, `"trade-offs between"` | Active |
| `paper_breakdown` | `M7` | [paper-breakdown.md](../templates/variants/paper-breakdown.md) | Research paper deconstruction & ablation audit | `"paper breakdown"`, standalone arXiv/DOI/OpenReview URL | Active |
| `quick_summary` | `M7` | [quick-summary.md](../templates/variants/quick-summary.md) | Verified article/docs/video summary | `"summarize ..."`, standalone article/video URL | Active |
| `revision_pack` | `M7` | [revision-pack.md](../templates/variants/revision-pack.md) | Consolidated exam revision guide | `"revision pack"`, `"exam revision"` | Active |
| `concept_map` | `M7` | [concept-map.md](../templates/variants/concept-map.md) | Visual Mermaid relationship map & matrix | `"concept map"`, `"knowledge map"` | Active |

---

## 4. Subtemplate Catalog (`6` Domain-Independent Subtemplates)

| Subtemplate ID | Canonical Path | Registry Knowledge Types | Compatible Masters | Required Modules | Reachability |
|---|---|---|---|---|---|
| `mathematical` | [mathematical.md](../templates/subtemplates/mathematical.md) | `mathematical` | `M1`–`M7` | `definitions`, `mathematical_derivation`, `representation_alignment` | Active (`detect_knowledge_types`) |
| `computational` | [computational.md](../templates/subtemplates/computational.md) | `programming`, `algorithmic`, `architectural`, `procedural` | `M1`–`M7` | `definitions`, `code_explanation`, `executable_verification` | Active (`detect_knowledge_types`) |
| `scientific` | [scientific.md](../templates/subtemplates/scientific.md) | `scientific` | `M1`, `M2`, `M3`, `M4`, `M6`, `M7` | `definitions`, `representation_alignment` | Active (`detect_knowledge_types`) |
| `conceptual` | [conceptual.md](../templates/subtemplates/conceptual.md) | `conceptual`, `comparative` | `M1`, `M2`, `M3`, `M6`, `M7` | `definitions`, `progressive_explanation` | Active (`detect_knowledge_types`, default fallback) |
| `historical` | [historical.md](../templates/subtemplates/historical.md) | `historical` | `M1`, `M2`, `M3`, `M6`, `M7` | `definitions` | Active (`detect_knowledge_types`) |
| `empirical` | [empirical.md](../templates/subtemplates/empirical.md) | `research` | `M1`, `M2`, `M3`, `M6`, `M7` | `definitions` | Active (`detect_knowledge_types`) |

---

## 5. Master–Subtemplate–Module Usage Matrix (Verified Against Implementation)

Activation levels below come from [master-registry.yaml](../routing/master-registry.yaml) and [instructional-registry.json](../workflows/notes-creation/instructional-registry.json):

| Module / Capability | Category | Owner Engine | M1 | M2 | M3 | M4 | M5 | M6 | M7 |
|---|---|---|---|---|---|---|---|---|---|
| `definitions` | Instructional | E4 Pedagogy | Required | Required | Required | Required | Required | Required | Required |
| `prerequisites` (`P01` / F04) | Instructional | E4 / E3 | Default | Conditional | Excluded | Conditional | Default | Excluded | Conditional |
| `progressive_explanation` (`P02` / F11) | Instructional | E4 Pedagogy | Strong | Source-Ordered | Minimal | Staged | Staged | Separated | Layered |
| `mathematical_derivation` (`EIS-03`) | Instructional | E4 Pedagogy | Supported | Optional | Incompatible | Required | Optional | Optional | Optional |
| `worked_examples` (`P04`) | Instructional | E4 Pedagogy | Default | Default | Incompatible | Required | Default | Supported | Optional |
| `visual_reasoning` (`P05`) | Instructional | E4 Pedagogy | Supported | Supported | Optional | Optional | Supported | Optional | Supported |
| `representation_alignment` (`P03` / F09) | Validation | E5 / E3 | Default | Supported | Default | Supported | Supported | Supported | Supported |
| `misconception_prevention` (`P06` / `EIS-04`) | Instructional | E4 Pedagogy | Default | Supported | Light | Default | Default | Default | Supported |
| `code_explanation` (`P10` / `EIS-05`) | Instructional | E4 Pedagogy | Supported | Optional | Variant (`syntax_reference`) | Optional | Required | Optional | Optional |
| `executable_verification` (`P10`) | Validation | E5 Quality | Supported | Optional | Variant (`syntax_reference`) | Optional | Required | Optional | Excluded |
| `comparisons` | Instructional | E4 Pedagogy | Optional | Optional | Variant | Optional | Optional | Optional | Default |
| `cross_topic_connections` (`P08` / F10) | Instructional | E3 Knowledge | Supported | Supported | Light | Excluded | Optional | Optional | Default |
| `cognitive_load` (`P09`) | Validation | E4 Pedagogy | Supported | Supported | Enforced (cap) | Supported | Supported | Excluded | Supported |
| `active_recall` (F13) | Instructional | E4 Pedagogy | Optional | Optional | Incompatible | Incompatible | Optional | Required | Optional |
| `revision_summary` (`P11` / `EIS-06`) | Instructional | E4 Pedagogy | Default | Default | Default | Optional | Optional | Optional | Default |
| `explanatory_clarity` (`EIS-07`, `CF-01..12`) | Validation | E5 Quality | Deep | Standard | Lightweight | Standard | Standard | Lightweight | Standard |
| `collection_intelligence` (KCP F02–F15) | Processing | E1/E3/E4/E5/E6 | Full | Source-Safe | Single/Companion | Single/Companion | Full | Collection Assessment | Synthesis/Index |

---

## 6. Knowledge-Type Coverage Report

| Knowledge Type | Primary Masters | Selected Subtemplate | Core Modules Activated | Status |
|---|---|---|---|---|
| Mathematical derivation / optimization | `M1`, `M4` | `mathematical` | `definitions`, `mathematical_derivation`, `worked_examples`, `representation_alignment`, `F09` | Verified |
| Algorithm & code implementation | `M5`, `M1` | `computational` | `definitions`, `code_explanation`, `executable_verification`, `worked_examples`, `EIS-05` | Verified |
| Formula / syntax / CLI quick reference | `M3` (`formula_sheet`, `syntax_reference`, `command_reference`) | `mathematical` / `computational` | `definitions`, `representation_alignment`, `revision_summary` | Verified |
| Scientific law & physical mechanism | `M1`, `M2`, `M4` | `scientific` | `definitions`, `representation_alignment`, `visual_reasoning`, `F09` | Verified |
| Conceptual theory & distinctions | `M1`, `M2`, `M7` | `conceptual` | `definitions`, `progressive_explanation`, `misconception_prevention`, `EIS-04` | Verified |
| Comparative trade-off analysis | `M7` (`comparison_guide`), `M3` | `conceptual` / `mathematical` / `computational` | `comparisons`, `representation_alignment`, `revision_summary` | Verified |
| Source-ordered lecture / textbook chapter | `M2` (`lecture_order`) | Dynamic per section | `progressive_explanation`, `worked_examples`, `source_attribution`, `F04` strict-safe | Verified |
| Historical chronology & interpretation | `M1`, `M2`, `M7` | `historical` | `definitions`, `source_attribution`, `limitations` | Verified |
| Empirical paper / benchmark study | `M7` (`paper_breakdown`), `M1` | `empirical` | `definitions`, `source_attribution`, `comparisons`, `limitations` | Verified |
| Cross-topic synthesis & curriculum | `M7` (F10), `M1`–`M6` (KCP) | Dynamic per child | `cross_topic_connections`, `collection_intelligence` (F02–F15) | Verified |

---

## 7. Runtime Routing Patterns

Every pattern below maps user intent independently of academic domain and is verified in `tests/test_repository_architecture_audit.py`:

1. **First-principles quantitative topic (`"Explain <concept> from first principles with derivations"`):** `M1` (`deep-notes`), subtemplate `mathematical`, deep `EIS` + `mathematical_derivation`, `worked_examples`, `representation_alignment`.
2. **Algorithm & runtime tutorial (`"Explain <algorithm> in <language> with code and traces"`):** `M5` (`implementation-guide`), subtemplate `computational`, `code_explanation`, `executable_verification`, `EIS-05` state narration.
3. **Dense formula/syntax lookup (`"Create a cheat sheet for <topic> formulas"`):** `M3` (`quick-reference`, variant `formula_sheet`), subtemplate `mathematical`, `representation_alignment`, `revision_summary`.
4. **Multi-method comparison (`"Compare <Method A>, <Method B>, and <Method C>"`):** `M7` (`synthesis-revision`, variant `comparison_guide`), `comparisons`, `cross_topic_connections`.
5. **Source-faithful sequence (`"Create detailed notes from this chapter in original order"`):** `M2` (`study-notes`, variant `lecture_order`), `preserve_source_order=True`, active `source_policy` enforced.
6. **Broad multi-chapter curriculum (`"Create comprehensive notes on <Broad Field>"`):** Scope `S4`, interactive configuration + KCP (`F02`–`F13`) + Parent MOC + adaptive child chapters.
7. **Cross-concept integration (`"Explain how <Concept A> and <Concept B> interact"`):** `M1`/`M7` cross-topic synthesis (`F10`), linking existing vault notes via verified wikilinks.
8. **Localized feedback repair (`"The derivation in section X of my note is unclear"`):** Lifecycle repair (`F15` `QualityEngine.process_feedback()` + `F14` impact analysis), updating only the targeted section cleanly via `incremental_update_note()`.
