# Scriptorium routing

## Intent

Parse with `python scripts/plan_notes.py inspect "request"`. Explicit command locks outrank selectors; selectors outrank standalone-source defaults. A source inside a broader request supplies evidence, not a route lock.

| Command | Contract | Load next |
|---|---|---|
| `/scribe-deepnotes` | Primary-source research; first-principles multi-file curriculum (`00` syllabus + `3–6` subtopics unless single-note locked); independent math & multi-library/language code stacks | Decisions D01?D15 as applicable |
| `/scribe-notes` | Source-faithful structured multi-file subtopic notes (`4–10+` notes, min `3` unless single-source locked); preserve scope and emphasis; label supplemental explanation | D01?D15 as applicable; `studynotes` core route |
| `/scribe-expand` | Audit existing coverage and `detected_workflow` (`notes` vs `deepnotes`); create only missing units in the matching workflow & template | Playbook B |
| `/scribe-doubt` | Read existing notes only; no edits or external research | Playbook A only |
| `/scribe-quiz` | One question at a time from existing notes; log weak spots in body | Playbook G only |
| `/scribe-dsa` | Problem plus required language; missing either -> usage/clarification | D01, D05, D11?D15 |
| `/scribe-practice`, `/scribe-compare`, `/scribe-distill` | Existing-note derivation | Playbooks F/D or D01 |
| `/scribe-ingest`, `/scribe-atomic-notes` | Source ingestion / one direct source fetch | Playbooks E/H |

[Decision index](shared/note_decision_matrix.md) owns route and module choices. [Command playbooks](references/command_playbooks.md) own command-specific operations. Deep-study aliases resolve to the master, never independent templates. A broad request without a command defaults to deep study. If missing source material prevents faithful coverage, request the missing source; independent explanation may proceed only with its origin labeled.

## Plan and publish

1. Resolve vault: explicit path, `SCRIPTORIUM_VAULT_PATH`, then local configuration. Use `python scripts/vault_index.py "vault" --discover --topic "topic"`. Preserve existing placement, IDs, tags and filenames; see [pre-generation gate](references/pre_gen_gate.md).
2. Build a dependency-ordered outline. Required fields: `title`, `purpose`, `impl_weight`, `density`, `math_level`, `routing_reason`. Preserve the decision record in `decision_record`; optional language, verification stack, source profile, dependency IDs and output path remain planning data.
3. Persist with `python scripts/plan_notes.py start "vault" --request "request" --topic-folder "folder" --outline "outline.json"`. Resume saved plans rather than recreating outputs. Use the [syllabus contract](references/syllabus_template.md) for a multi-note curriculum; a single note needs no syllabus.
4. Load one selected template, [authoring rules](shared/authoring_rules.md), and only the applicable math/footer modules. Before drafting, resolve the item's `decision_contract` with `python scripts/decision_matrix.py resolve --request "request" --topic "topic" --title "title"` (and never emit code blocks when `code_depth` is `"none"`). Research with [research protocol](references/research_protocol.md). Fetch full supporting passages, reuse the source dossier, and record gaps.
5. Scaffold into scratch with `python scripts/scaffold_note.py --template ROUTE --math-level LEVEL --title "title" --topic "topic"`. Author selected modules, remove instructions, then `python scripts/validate_note.py "draft.md" --template ROUTE` (which also runs `decision_matrix.py` contract checks). For JSON diagnostics add `--format json`.
6. Publish with `python scripts/plan_notes.py publish "vault" PLAN ITEM "draft.md"`. Keep the draft until success; continue pending items. Finish with `python scripts/verify_vault_notes.py "vault" --files FILES` and `python scripts/vault_graph.py "vault" --topic "topic" --check-cycles`. Apply [semantic verification](references/verification_checklist.md); a format pass is not a factual guarantee.

Planner output includes the authoritative saved plan and per-item status. It does not research or write prose. New topic plans append a practice set; manual practice does not append another. Custom layouts use the manifest workflow rather than built-in heading enforcement.
