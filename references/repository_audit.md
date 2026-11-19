# Repository audit

Inventory captured before edits. Word counts are whitespace counts, not tokenizer measurements.

| File | Stage | Before words |
|---|---|---|
| `.gitignore` | 1 | 3 |
| `LICENSE` | 1 | 169 |
| `README.md` | 1 | 2251 |
| `router.md` | 1 | 1742 |
| `SKILL.md` | 1 | 143 |
| `.agents/skills.json` | 1 | 9 |
| `references/command_playbooks.md` | 2 | 1657 |
| `references/pre_gen_gate.md` | 2 | 350 |
| `references/research_protocol.md` | 2 | 876 |
| `references/syllabus_template.md` | 2 | 303 |
| `references/verification_checklist.md` | 2 | 494 |
| `scripts/note_layout.py` | 3 | 855 |
| `scripts/patch_links.py` | 3 | 1921 |
| `scripts/plan_notes.py` | 3 | 2476 |
| `scripts/scaffold_note.py` | 3 | 1064 |
| `scripts/validate_note.py` | 3 | 2672 |
| `scripts/vault_graph.py` | 3 | 1400 |
| `scripts/vault_index.py` | 3 | 2829 |
| `scripts/verify_vault_notes.py` | 3 | 3754 |
| `shared/authoring_rules.md` | 2 | 698 |
| `shared/footer_widgets.md` | 2 | 189 |
| `shared/math_gates.md` | 2 | 292 |
| `templates/api-table.md` | 4 | 597 |
| `templates/atomic.md` | 4 | 402 |
| `templates/cheat-sheet.md` | 4 | 348 |
| `templates/comparison.md` | 4 | 506 |
| `templates/deepstudy-coding.md` | 4 | 41 |
| `templates/deepstudy-general.md` | 4 | 41 |
| `templates/deepstudy-master.md` | 4 | 2972 |
| `templates/dsa.md` | 4 | 715 |
| `templates/notes_decision_matrix.md` | 2 | 6067 |
| `templates/paper-breakdown.md` | 4 | 683 |
| `templates/practice.md` | 4 | 687 |
| `templates/studynotes.md` | 4 | 2181 |
| `templates/summary.md` | 4 | 501 |
| `tests/test_adaptive_deepstudy.py` | 3 | 638 |
| `tests/test_patch_and_graph.py` | 3 | 562 |
| `tests/test_routed_workflow.py` | 3 | 2491 |
| `tests/test_syllabus_boundary.py` | 3 | 230 |
| `tests/test_token_optimizations.py` | 3 | 543 |
| `tests/test_vault_aware.py` | 3 | 786 |
| `skills/scribe-atomic-notes/SKILL.md` | 1 | 93 |
| `skills/scribe-compare/SKILL.md` | 1 | 55 |
| `skills/scribe-deepnotes/SKILL.md` | 1 | 80 |
| `skills/scribe-distill/SKILL.md` | 1 | 74 |
| `skills/scribe-doubt/SKILL.md` | 1 | 58 |
| `skills/scribe-dsa/SKILL.md` | 1 | 38 |
| `skills/scribe-expand/SKILL.md` | 1 | 51 |
| `skills/scribe-ingest/SKILL.md` | 1 | 53 |
| `skills/scribe-notes/SKILL.md` | 1 | 166 |
| `skills/scribe-practice/SKILL.md` | 1 | 67 |
| `skills/scribe-quiz/SKILL.md` | 1 | 51 |

## Consolidation map

Formatting, YAML, evidence status, style and links -> shared/authoring_rules.md. Math -> shared/math_gates.md. Routing -> shared/note_decision_matrix.md. Detailed deep-study decisions retain DM-01 through DM-20; do not renumber them. Footer implementation -> shared/footer_widgets.md. Optional module declarations remain exclusively in templates.

## Execution log

Stage 0: inventoried every source file; retained a pre-edit snapshot outside the repository.

Stage 1 complete: root SKILL, router and all command wrappers streamlined. Stage 4 files untouched.

Stage 2 complete: shared rules, routing index, detailed matrices, math/footer and reference contracts consolidated. Template source retained unchanged pending Stage 4.

Stage 3 complete: 101 existing tests plus 2 new contract tests passed before template edits. All script ASTs and CLI help validated. Added structured note diagnostics, shared schema constants, body-based strict review logging, optional heading matching and repository link audit.

Stage 4 complete: retained inquiry hierarchy and granular content; removed repeated directive paragraphs; added stripped preflight bindings and purpose-specific optional activation guides. Deep-study aliases remain redirects. Detailed DM anchors moved to shared with compatibility links.

## Efficiency measurements

Markdown words before: 25522; after (excluding this audit log): 22823; reduction: 10.6%. Whitespace counts are a size proxy, not measured model tokens. Detailed matrices remain available through branch loading.

## Verification scope

The audit checks local Markdown links and anchors, concrete script paths and documented flags, plus Python syntax. CLI help was checked for every executable script. Tests exercise note validation, graph/index behavior, patching, optional omission/inclusion and five-key review logging. No live vault was modified. External URLs and Obsidian visual rendering are outside this static audit. Historical/custom schemas remain readable for compatibility; generated built-in notes use the strict schema.

Final integration correction: declared the existing optional study-note procedure/reference/caveat sections explicitly, and ensured scaffold numbering stays consecutive after omission. This closes a prose/validator mismatch discovered during Stage 4.
