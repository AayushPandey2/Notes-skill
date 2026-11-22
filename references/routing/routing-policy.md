# Intelligent Routing Policy

## Purpose & Single Authority

Select exactly one canonical master (`M1`–`M7`) and optional variant (`master-registry.yaml`) per requested artifact independently of academic domain, owned by `scriptorium/engines/orchestration.py` (`scripts/scribe.py route`).

## Activation Trigger & Precedence Rules

1. **Public Commands:** `/scribe-notes` is the sole note-creation entrypoint (`M1`–`M7`, variants, KCP collections, plus `/scribe-ytnotes`/`/scribe-ytlecture` video aliases). `/scribe-doubt`, `/scribe-quiz`, and `/scribe-setfolder` remain standalone utilities. Invoke of any retired note command (`/scribe-deepnotes`, `/scribe-distill`, `/scribe-atomic-notes`, `/scribe-compare`, `/scribe-dsa`, `/scribe-practice`, `/scribe-ingest`, `/scribe-expand`) returns a migration hint to `/scribe-notes`.
2. **Negation-Aware Explicit Selectors:** Honor explicit deliverable phrases (`"formula sheet"`, `"compare X vs Y"`, `"worked solutions"`, etc.) unless negated (`"don't make a cheat sheet; explain deeply"` strips the negated form before classification).
3. **Dominant Objective:** Classify primary intent (`comprehensive_learning`, `structured_study`, `rapid_reference`, `worked_problem_solving`, `practical_implementation`, `knowledge_assessment`, `synthesis_and_revision`).
4. **Source-Policy Invariance:** Source constraints (`strict` / `source_first` / `R-S0`) never flip an explicit format request, and brevity rules never silence required source concepts.
5. **Documented Defaults:** Bare topic -> `M1`; supplied lecture/PDF with sequential/study request -> `M2/lecture_order`; standalone research paper URL -> `M7/paper_breakdown`; standalone article/docs/video URL -> `M7/quick_summary`.

## Multi-Artifact & Failure Handling

- **Multi-Artifact Split:** Integrated add-ons (`"... with a formula summary at the end"`) stay modules inside the primary master; explicit multi-deliverable asks emit linked routes sharing one evidence registry and notation table.
- **Failure Handling & Validation:** Raise a structured error if a registered template/variant is missing; verify routing determinism via `OrchestrationEngine.validate_registry()` (`scripts/scribe.py validate-registry`).
