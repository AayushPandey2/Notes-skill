# Command playbooks

Load only the active branch. All note-creation playbooks (`B`, `C`, `D`, `E`, `F`, `H`, `I`) execute internally through the universal `/scribe-notes` interactive workflow (`scripts/scribe.py notes`), while `A` (`/scribe-doubt`) and `G` (`/scribe-quiz`) remain standalone non-note utilities. All writing uses [router workflow](../../../router.md#plan-and-publish) and [shared contracts](../../../shared/authoring_rules.md).

## Command A

**Trigger:** `/scribe-doubt` — Answer read-only questions from existing vault notes.
Index and extract only relevant existing notes. Answer with exact wikilink citations. No external research or edits; state missing coverage.

## Command B

**Trigger:** Expansion of an existing vault topic or folder via `/scribe-notes`.
Inspect coverage with `vault_index.py --discover` and read `detected_workflow` (`"deep-notes"`, `"study-notes"`, `"mixed"`, or `null`). Match the dominant existing style (`M2` `study-notes` for structured series; `M1` `deep-notes` for deep concept notes) or clarify when mixed. Identify gaps within requested scope, update the index/syllabus allowlist before adding new files, preserve existing notes, and run `patch_links` with `--dry-run` for metadata-only edits.

## Command C

**Trigger:** Comprehensive learning request routed to `M1` (`deep-notes`).
Build the [instructional plan](adaptive-engine.md) from objectives, reader baseline, and inspected sources, run concept-specific evidence planning and verification via the [ARRIE research engine](../research/research-engine.md) (`scripts/scribe.py research`), then persist through `plan_notes.py start`. Select subtemplates, `teaching_core.md` rules (`M01`–`M14`, `Step 1`–`12` for math/worked solutions), and module depths per concept; code needs a learning purpose and a justified primary tool. Compose with the `M1` master from the compact `research_package`, curate further-learning resources separately via [resource-recommendations.md](../research/resource-recommendations.md) when helpful, complete pending notes, and run structural, semantic, and 12-dimension teaching quality checks (`scripts/scribe.py quality`). Never emit internal module headings or legacy markers.

## Command D

**Trigger:** Rapid reference / formula / syntax / command / cheat-sheet request routed to `M3` (`quick-reference`).
Extract relevant definitions, equations, choices, and pitfalls from existing notes or bounded references. Retain compact reference density. Run new research only for an explicit evidence gap.

## Command E

**Trigger:** Source-faithful note ingestion from PDF, URL, lecture, or raw notes routed to `M2` (`study-notes` / `lecture_order`).
Extract the actual PDF/URL/raw notes; inspect equations against source where extraction is uncertain. Avoid duplicate coverage and destructive overwrites. Label inaccessible passages; never invent missing pages.

## Command F

**Trigger:** Multi-item comparison or contrast request routed to `M7` (`comparison_guide`).
Resolve both existing notes or compared items, compare shared axes fairly, publish to `comparison_guide`, and echo the exact generated Markdown in chat when asked. Clarify ambiguous note identity before writing.

## Command G

**Trigger:** `/scribe-quiz` — Interactive one-question-at-a-time active recall on existing notes.
Ask one question, wait, grade against the note, then continue. Record weak spots in the body review field using `patch_links`; do not introduce extra YAML keys or load composition templates.

## Command H

**Trigger:** Single-concept transcludable card request routed to `M3` (`atomic_card`).
Perform one bounded direct search/fetch, then apply the `atomic_card` template. Resolve existing vault links; keep future concepts as plain text.

## Command I

**Trigger:** Multi-note curriculum or structured topic series request routed to `M2` (`study-notes`).
Decompose any topic without an explicit single-unit source lock into multiple focused, numbered subtopic files (`4–10+` notes, minimum `3`, plus an index/syllabus note `<Topic> Index.md` or `00-MOC-<topic>.md`) using `M2` (`study-notes`) for core outputs — never collapse a whole topic into one file. Preserve supplied source terminology, scope, and emphasis; label supplemental examples. Topics without sources permit bounded authoritative lookup; inaccessible specified sources require an explicit gap notice. Math depth follows actual concept/source needs via `teaching_core.md` (`M01`–`M14`), not subject labels alone.
