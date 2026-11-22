# Intelligent Routing Policy

One routing authority ([scriptorium/engines/orchestration.py (`scripts/scribe.py route`)](../../scriptorium/engines/orchestration.py) backed by [master-registry.yaml](master-registry.yaml)) selects the canonical output master (`M1`–`M7`) and optional variant for each requested artifact.

## 1. Precedence Order

1. **Active public commands & universal `/scribe-notes`:**
   - `/scribe-notes` is the sole public note-creation command and routes dynamically across ALL seven canonical masters (`M1`–`M7`), all 12 variants, and single-note vs. hierarchical multi-note collections via the interactive configuration gate (`scripts/scribe.py notes start`).
   - Non-note utilities remain separate: `/scribe-doubt` (read-only vault Q&A), `/scribe-quiz` (`M6/mock_exam` interactive quiz on existing notes), and `/scribe-setfolder` (vault target configuration).
   - Retired note-creation commands (`/scribe-deepnotes`, `/scribe-distill`, `/scribe-atomic-notes`, `/scribe-compare`, `/scribe-dsa`, `/scribe-practice`, `/scribe-ingest`, `/scribe-expand`) are listed under `retired_commands` in `master-registry.yaml` for graceful migration guidance to `/scribe-notes`.
2. **Explicit artifact format (negation-aware):** Detect explicit requests for cheat sheets / formula sheets / syntax refs (`M3`), worked solutions (`M4`), from-scratch implementations / build guides (`M5`), quizzes / flashcards / mock exams (`M6`), or revision packs / comparisons / concept maps / paper breakdowns / summaries (`M7`). Ignore negated clauses (e.g., `"Don't make a cheat sheet; explain in depth"` -> `M1`, never `M3`).
3. **Dominant user objective:** Classify primary intent (`comprehensive_learning`, `structured_study`, `rapid_reference`, `worked_problem_solving`, `practical_implementation`, `knowledge_assessment`, `synthesis_and_revision`) independent of topic difficulty or domain.
4. **Source & structural constraints:** Source-only (`R-S0`) or source-order (`strict`/`expanded`) constraints never override an explicit product request (e.g., `"formula sheet from this PDF only"` -> `M3/formula_sheet` + `R-S0`), and never silently drop required source concepts when brevity is requested.
5. **Depth & learner preferences:** Adjust depth inside the chosen master rather than switching masters.
6. **Documented defaults:**
   - Bare topic with no format/command -> `M1` (`deep-notes`).
   - Supplied source with `"study notes"` / `"chapter order"` / `"lecture transcript"` -> `M2` (`study-notes`, `lecture_order` variant).
   - Standalone research paper URL -> `M7` (`paper_breakdown` variant).
   - Standalone article/docs/video URL -> `M7` (`quick_summary` variant).

## 2. Single vs. Multi-Artifact Routing

- **Single integrated artifact:** Secondary requests (`"... and include a formula summary at the end"`) activate modules inside the primary master rather than spawning unsolicited files.
- **Multiple separate artifacts:** Explicit multi-output phrasing (`"Create a separate deep-notes file, cheat-sheet file, and standalone flashcards"`) emits distinct artifact routes (`M1`, `M3`, `M6/flashcards`) sharing one verified evidence registry, concept IDs, definitions, and notation.

## 3. Fallback & Error Handling

If a canonical master or variant file is missing from `master-registry.yaml`, raise a structured configuration error rather than silently loading an unrelated template.
