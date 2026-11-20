# Adaptive-engine evaluation

[Scenarios](scenarios.json) are author-supplied classifications and learning goals used by the actual planner. They are not inferred from a keyword oracle. [Sample notes](sample-notes.md) demonstrate coherent explanatory excerpts; [binary search](binary_search.py) is executable. [Source fixture](source-fixture.md) is original synthetic material containing definitions, an example, figure, exercise, qualification and an untrusted instruction. No external source or model benchmark is implied.

| Scenario | Expected adaptation |
|---|---|
| A: What is AI? | Definitions, intuition, distinctions; no forced math/code |
| B: Gradient descent | Local M2/M4/M0 and C0/C0/C3 profiles; derivation and implementation separated by dependency |
| C: Binary search | Algorithm, trace, implementation, debugging, boundaries and correctness reasoning |
| D: Transformer encoder | Mathematical relations and detailed component/shape visuals; no unrequested implementation |
| E: Pandas preprocessing | Procedure, comparison, code, intermediate states and validation |
| F: ML history | Chronology, evidence and comparison; no forced derivation |
| G: Source fidelity | Required element inventory, source order and validated publication receipts |
| H: Perceptron | Model, geometry, mistake-driven learning and one NumPy implementation |
| I: Beginner vs advanced | Explain missing foundations and apply versus assume known foundations and prove |
| J: Efficiency | Static instruction size and selected module context measured separately from quality |

The tests exercise these plans through `build_plan`, missing dependencies, conflicting depth, protected required modules, selective module activation, malformed receipts, inaccessible elements, invented anchors, source ordering, publication, receipt persistence and idempotent retries. The programming fixture checks presence, absence, boundaries, empty/singleton input and duplicates in a real Python runtime, then publishes a note with observed evidence. Source claims themselves still require semantic review. The hostile-source fixture is a manual review case: the deterministic helper never executes it, but these tests do not establish a model's resistance to prompt injection.

Run `python -m pytest -q -p no:cacheprovider` with pytest and PyYAML installed. The repository audit and skill-creator validator additionally check local references, Python syntax and skill frontmatter. The original suite passed 119 tests before migration. Updated tests retain command, alias, source-study, metadata, scoped editing, publication/retry and runtime contracts; expectations for the intentionally removed deep quotas/defaults were revised.

Final local verification: **143 tests passed** (40.66 seconds). The repository audit found no broken local references or CLI declarations, and skill-creator validation passed for the root skill and changed deepnotes wrapper. These are observed local results, not a model-quality benchmark.

## Resource measurements and limits

[Measurements](measurements.json) compare normalized Unicode character counts against the recorded local Git baseline. The master shrank from **31,285 to 3,610 characters**; the existing decision guide shrank from **54,345 to 51,341** at the recorded measurement. Routing now loads only its relevant branches. New engine and source instructions add capabilities; selected registry entries add context only when used. These numbers are component sizes, not a claim that all task prompts shrink by the same amount. The wrapper grew to expose the new workflow.

The measurements also record active module counts and serialized selected-module sizes for each scenario. Per-concept output-token budgets are explicitly heuristic estimates. No provider input/output tokens, costs, latency, retry savings, educational scores or learner outcomes were available. No API-based before/after generation experiment was run. Coverage and correctness gates must pass independently of size; reduced output length is not an acceptance criterion.

## Maintenance and remaining evaluation

Change objective floors, types or module contracts in [the registry](../../references/workflows/notes-creation/instructional-registry.json), and add a scenario proving the intended distinction. Keep prose composition rules in [the master](../../references/templates/masters/deep-notes.md) and operational mechanics in [the engine](../../references/workflows/notes-creation/adaptive-engine.md). Add a registry version/migration if changing the meaning of persisted decisions; never rewrite completed plans in place.

The implementation remains an agent skill, not an autonomous prose-generation service. Future evaluation can run blinded model-generated lessons against the same source inventory and review accuracy, coherence, transfer questions and measured usage. Actual figure rendering, external source retrieval and learner outcomes are outside this offline regression run. Legacy source-study and compact routes retain their established formatting/validation contracts.
