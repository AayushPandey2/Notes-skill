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
2. Build a dependency-ordered outline with `title`, `purpose`, `impl_weight`, `density`, and `routing_reason`. Set `math_level` from the outcome when it differs from the route default. Preserve the [decision record](shared/notes_decision_matrix.md#decision-record) in `decision_record`. Set `implementation_stack` per note or pass `--stack` to inspect or start when the user supplies a stack.
3. Persist with `python scripts/plan_notes.py start "vault" --request "request" --topic-folder "folder" --outline "outline.json"`. Resume saved plans rather than recreating outputs. Use the [syllabus contract](references/syllabus_template.md) for a multi-note curriculum; a single note needs no syllabus.
4. Load the selected template, [shared decision guide](shared/notes_decision_matrix.md), [authoring rules](shared/authoring_rules.md), and applicable math and footer modules. Use the item's saved `decision_contract` as the authority for domain, effective level, code depth, and stack. The plan reports `clamped_from` when a level was reduced. An explicit user override can use `--allow-math-override` within the route limits. Fetch supporting passages, reuse the source dossier, and record gaps under the [research protocol](references/research_protocol.md).
5. Scaffold into scratch with `python scripts/scaffold_note.py --template ROUTE --math-level LEVEL --title "title" --topic "topic"`. Author the selected modules and remove instructions. Save the item's `decision_contract` as scratch JSON to validate with `python scripts/validate_note.py "draft.md" --contract "contract.json"`. For required implementations, run `python scripts/plan_notes.py verify-runtimes "vault" PLAN ITEM "draft.md"` and record the evidence required by [DM-18](shared/notes_decision_matrix.md#dm-18).
6. Publish with `python scripts/plan_notes.py publish "vault" PLAN ITEM "draft.md"`. Publish verifies required runnable examples in trusted drafts. Pass `--export-code` to save verified examples under `assets/<topic>/examples/`. Keep the draft until success and continue pending items. Finish with `python scripts/verify_vault_notes.py "vault" --files FILES`, `python scripts/vault_graph.py "vault" --topic "topic" --check-cycles`, and the [semantic verification checklist](references/verification_checklist.md).

Planner output includes the authoritative saved plan and per-item status. It does not research or write prose. New topic plans append a practice set; manual practice does not append another. Custom layouts use the manifest workflow rather than built-in heading enforcement.
