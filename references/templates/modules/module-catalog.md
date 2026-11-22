# Reusable Instructional Module Catalog

Every module below is declared in [instructional-registry.json](../../workflows/notes-creation/instructional-registry.json) and governed by [pedagogical-intelligence.md](../../workflows/notes-creation/pedagogical-intelligence.md). Activate selectively (`required`, `supporting`, `optional`, `excluded`)—never force every module into every master.

| Module | Primary Purpose | Typical Masters | Validation Hook |
|---|---|---|---|
| `prerequisites` (`P01`) | Readiness-calibrated prerequisite bridges (`assume`/`remind`/`bridge`/`teach`/`defer`) | M1, M2, M5 | `build_cognitive_dependency_graph`, `detect_dependency_gaps` |
| `progressive_explanation` (`P02`) | Conditional `L1–L8` progression (`motivation` -> `limitations`) | M1, M2 | `plan_explanation_layers` |
| `mathematical_derivation` | Symbol-defined governing relations, `M4` stepped derivations, `M5` proofs | M1, M2, M4 | `shared/math_gates.md`, `validate_representations` |
| `worked_examples` (`P04`) | Non-redundant examples by role (conceptual in M1, primary in M4, compact in M3, runnable in M5) | M1, M2, M3, M4, M5 | `audit_examples` |
| `visual_reasoning` (`P05`) | Obsidian-compatible diagrams (`function_graph`, `flowchart`, `timeline`, `geometric_diagram`, etc.) | M1, M2, M5, M7 | `validate_visuals`, `validate_note._mermaid` |
| `representation_alignment` (`P03`) | Canonical symbol, unit, equation-code, and tensor-shape consistency | M1, M2, M3, M4, M5 | `validate_representations` |
| `misconception_prevention` (`P06`) | Point-of-need corrections without invented frequency stats | M1, M2, M4, M5, M6, M7 | `audit_misconceptions` |
| `code_explanation` & `executable_verification` (`P10`) | Equation-to-code mapping and truthful runtime verification tiers | M1, M3 (`syntax_reference`), M5 | `verify_executable_example`, `plan_notes.py verify-runtimes` |
| `comparisons` | Equivalent-criteria trade-off matrices and crossover edge cases | M1, M3, M7 | `comparison-guide.md` |
| `cross_topic_connections` (`P08`) | Typed semantic vault links (`existing_note` vs. `planned_note`) with link-inflation guard | M1, M2, M7 | `resolve_cross_topic_connections` |
| `cognitive_load` (`P09`) | Concept-level detail facets and beginner symbol-density protection | M1, M2 | `audit_cognitive_load` |
| `active_recall` | Tiered questions, hidden answers, flashcards, and diagnostic checks | M1, M2, M6 | `assessment.md`, `validate_note._practice` |
| `revision_summary` (`P11`) | Layer B/C concept review preserving formula conditions & Layer A anchors | M1, M2, M3, M7 | `validate_revision_integrity` |
