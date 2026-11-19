# Adaptive deep-notes migration

## Inspection before implementation

The repository is a prompt-driven skill with Python helpers, not an API-based text generator. `SKILL.md` dispatches through `router.md`; command wrappers in `skills/` retain their names and relative links. `.agents/skills.json` discovers those wrappers. There are no installed model dependencies or provider usage records. Python helpers depend on PyYAML; tests additionally require pytest.

| Stage | Existing implementation | Finding / migration |
|---|---|---|
| Intent | `plan_notes.inspect_request`, command locks and template selectors | Preserve commands and explicit format locks. |
| Sources | Research protocol and run-local source dossier | Preserve inspected-passage rule; add four policies, element inventory and coverage receipts. |
| Outline | Agent-authored JSON; earlier-item dependencies | Preserve resumability and note paths; add concept-level prerequisites and instructional plans. |
| Template | One adaptive master, general/coding aliases, separate source-study format | Preserve one master and both aliases; replace repetitive authoring gates with composition rules. |
| Classification | Title/topic regexes and broad domain | Useful fallback hints, insufficient for instructional decisions; structured types/objectives now take precedence. |
| Mathematics | M0–3, domain ceilings, display quotas and heading tests | Legacy CLI numbers remain adapters; remove subject ceilings and quotas for new deep plans. |
| Coding | Implementation purpose automatically selects several specialty frameworks | Select one primary tool; comparisons require explicit stacks or separate justified roles. |
| Visuals | Domain hints plus Mermaid/image rules | Keep rendering; choose each visual for a specific relationship. |
| Examples | Small fixtures, shared numerical parity | Preserve reproducibility; vary difficulty and count by outcome and error risk. |
| Assembly | Agent writes selected modules; scaffold has no forced deep headings | Preserve; add explicit canonical homes, dependency ordering and compact chunk state. |
| Fidelity | Attribution and access limits, no inventory gate | Add source inventory and publication receipts; source text never supplies execution instructions. |
| QA | Schema, links, math heuristics, runnable evidence, semantic checklist | Preserve mechanical and runtime checks; distinguish structural evidence from semantic verification. |
| Tokens | Progressive loading, cached vault index, selective extraction | Preserve; reduce duplicated master instructions and measure static instruction size separately from model usage. |
| Delivery | Five-key YAML, syllabus, safe publication, practice, vault graph | Preserve output contracts and unaffected commands. |

## Migration inventory

- **Preserve:** command wrappers, discovery, source-study route, vault index/graph, safe file handling, runtime evidence, five-key metadata, practice placement, general/coding aliases.
- **Refactor:** router, detailed decision guide, math gates, research and verification guidance, planner/decision contract integration.
- **Replace:** deep master section checklist, automatic multi-framework defaults, domain-based deep math clamps and equation quotas.
- **Deprecate:** those defaults, not filenames or command names. Existing saved contracts retain their validation semantics; new plans use the versioned adaptive contract.
- **Add:** compact knowledge subtemplates/module registry, per-concept profiles, source coverage gate, realistic evaluation fixtures and regression checks.

No user notes or unrelated functionality are removed. Repository changes are local; installing this checkout into a user-wide skill directory is a separate action.

## Compatibility

`/scribe-deepnotes`, `/scribe-notes`, `/scribe-expand`, deep template aliases and existing CLI flags remain. `/scribe-notes` continues to use `studynotes`, with its established source sequence and multi-file contract. Legacy `math_level` values 0/1/2/3 translate to adaptive M0/M3/M4/M5; they are not renamed to the new scale. Structured `instructional_plan` concepts use independent M/C/V/T/P/A levels 0–5. New deep plans no longer clamp explicit mathematics by discipline or require automatic framework tours. Old plans are not rewritten on resume.

## Validation and measurement

See [evaluation](../examples/adaptive-deepnotes/README.md) for scenario coverage, executable fixtures, measurements and limits. Static instruction size is an input-context proxy, not measured model tokens, latency, cost, or proof of educational improvement. No generation API is added; semantic planning and coherent prose remain the skill agent's responsibility.

## Changed artifacts

Existing files changed: the deep command wrapper, `router.md`, deep master, shared decision index/guide, math and authoring rules, research/verification protocols, command playbook and README. Python changes integrate the versioned plan in `decision_matrix.py`, source coverage receipts in `plan_notes.py`, adaptive executable-example checks in `note_verification.py`, and dependency-directory exclusion in the repository audit. Existing regression expectations changed only for the superseded deep quotas, automatic stacks and math clamps; publication fixtures retain their originally intended math depth explicitly.

Added: `references/adaptive-engine.md`, `references/instructional-registry.json`, `references/source-fidelity.md`, this audit, `scripts/instructional_plan.py`, `tests/test_instructional_engine.py`, and the evaluation fixtures/reports under `examples/adaptive-deepnotes/`. No files or command names were removed. The old master content was replaced in place. Local test dependencies were installed in ignored `.test-deps/`; no runtime model dependency was added.

Remaining limitations: prose and factual/source review still require the skill agent; structural receipts cannot prove source support, and heading order cannot prove within-section source order. Legacy source-study/compact formatting remains intentionally unchanged. Old outlines receive a compatibility plan; substantial or supplied-source work requires the agent to populate the structured plan before drafting. Provider usage and independent model-generation quality comparisons were unavailable. Global skill installation and GitHub publication were not part of this local migration.
