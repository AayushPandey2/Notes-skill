# Teaching input contract

Use for `notes generate --teaching <json>`. The JSON object maps concept IDs or exact chapter titles from the approved session plan to records. These are researched content inputs, not assertions that quality has been verified.

Each record may supply:

- `objectives`: concrete learning goals; `sections`: ordered `{heading, content}` narrative sections.
- `teaching`: structured six-question teaching roles (`what`, `why`, `how`, `when_use`, `when_not_use`, `apply`, plus optional `intuition` and `reinforcement`), or `teaching_bindings` mapping canonical roles to `sections` headings.
- `mechanism`: causal mechanism record with `inputs`, `steps` (`component`, `receives`, `operation`, `reason`, `produces`, `next`), `outputs`, and `interpretation`.
- `depth_profile`: explicit instructional demand (`complexity`: `trivial` | `simple` | `standard` | `complex`, `internal_mechanisms`, `prerequisite_burden`, `mathematical_difficulty`, `implementation_importance`, `advanced_connections`, `assessment_types`).
- `practical`: adaptive 12-stage laboratory (`domain`: `programming` | `machine_learning` | `mathematics` | `experimental` | `humanities` | `general`, `stages`, optional `omissions`, `code`, `language`, and bound `execution` receipt `{code_sha256, status, expected, observed, method}`).
- `starting_intuition`, `familiar_anchor`, `prerequisite_bridges` (`{term, explanation}`), `comparisons` (causal prose + `suitability`/`assumptions`/`mechanism`/`strengths`/`limitations`/`resources`/`reliability`/`interpretability`/`practical_constraints` + optional `table`), `misconceptions` and `practical_application`.
- `equations`: mathematical component specifications described in [math gates](../../shared/math_gates.md), including symbol meanings, operation order, assumptions, `required_stages`, `stage_omissions` (substantive reasons only), and numerical traces.
- `worked_problems`: problem, given inputs, objective, assumptions, formula, symbols, intermediate steps and expected result. Arithmetic expressions use the bounded evaluator.
- `assessments`: `{id, type, objectives, question, hint, reasoning, answer}` records rendered as questions with separate collapsed hint and answer callouts.
- `visual_requirements`: learning objectives (with optional `role` from `overview`, `motivation`, `mechanism`, `mathematical`, `worked_example`, `comparison`, `application`, `synthesis`) that activate web research, or `visual_specs`: explicit acquisition specifications. Set `visual_required` when a chapter cannot be complete without its visual support.
- A visual specification can include `inspection_findings` with the exact `content_hash`, observed `text_labels_extracted`, and review method. The downloaded hash must match before those findings enter composition.

The Writer tracks orientation, mechanism, examples, interpretation, limitations, intuition, prerequisite bridges and formula folds as applicable. `require_complete` rejects pending structural obligations; comprehensive public generation enables it automatically. Use the canonical narrative roles when supplying complete authored sections, or use the corresponding teaching fields so the Tutor supplies their headings. A record with headings alone cannot establish scientific or educational accuracy.

The Publisher acquires declared visuals before composition, checks final formula folds after reconciliation, normalizes generated links to real note paths, and atomically writes notes and state. Resume is bound to both input specifications and file hashes. Existing personal sections are preserved; a validation failure blocks writing rather than deleting them.

`complete` in the file-generation manifest reports committed files; `verified` remains false until educational review is established outside structural generation. Do not describe this as full educational acceptance or UI verification.
