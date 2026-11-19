# Command playbooks

Load only the active branch. All writing uses [router workflow](../router.md#plan-and-publish) and [shared contracts](../shared/authoring_rules.md).

## Command A

Doubt: index and extract only relevant existing notes. Answer with exact wikilink citations. No external research or edits; state missing coverage.

## Command B

Expand: inspect coverage with `vault_index.py --discover` and read `detected_workflow` (`"deepnotes"`, `"notes"`, `"mixed"`, or `null`). Match the existing workflow: if `"notes"`, bypass multi-wave deep research in favor of bounded direct lookup and author missing subtopics with `studynotes` (never `deepstudy-master`); if `"deepnotes"` (or `null` when starting deep coverage), use full primary-source research and `deepstudy-master` (`--template deepstudy-master` / `research_protocol.md`); if `"mixed"`, match the dominant existing subtopic style or ask the user. Identify gaps within requested scope, update the syllabus allowlist before new files, preserve existing notes, and run `patch_links` with `--dry-run` for metadata-only edits.

## Command C

Deepnotes: build the [instructional plan](adaptive-engine.md) from objectives, reader baseline and inspected sources, then persist through `plan_notes.py start`. Select subtemplates and module depths per concept; code needs a learning purpose and a justified primary tool. Compose with the single master, complete pending notes, and apply source coverage, runtime, structural and semantic checks. Never emit internal module headings or legacy markers.

## Command D

Distill: extract relevant definitions, equations, choices and pitfalls from existing notes. Route to cheat-sheet; retain its compact limit. New research only for an explicit evidence gap.

## Command E

Ingest: extract the actual PDF/URL/raw notes; inspect equations against source where extraction is uncertain. Avoid duplicate coverage and destructive overwrites. Label inaccessible passages; never invent missing pages.

## Command F

Compare: resolve both existing notes, compare shared axes fairly, publish to comparison and echo the exact generated Markdown in chat. Clarify ambiguous note identity before writing.

## Command G

Quiz: ask one question, wait, grade against the note, then continue. Record weak spots in a body review field using patch_links; do not introduce YAML keys or load templates.

## Command H

Atomic: one bounded direct search/fetch, then atomic template. Resolve existing vault links; future concepts stay plain text.

## Command I

Study notes: decompose any topic without an explicit single-unit source lock into multiple focused, numbered subtopic files (`4–10+` notes, minimum `3`, plus `00-MOC-<topic>.md`) using `studynotes` for core outputs — never collapse a whole topic into one file. Preserve supplied source terminology, scope and emphasis; label supplemental examples. A topic without sources permits bounded authoritative lookup; an inaccessible specified source requires a gap notice. Do not switch to deep-study aliases. Math depth follows the actual source/outcome, not the subject label alone.
