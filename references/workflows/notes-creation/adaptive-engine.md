# Instructional planning and composition

Load this for deep study. The [M1 master](../../templates/masters/deep-notes.md) owns document composition; [registry](instructional-registry.json) owns reusable subtemplates, objective depth floors and module contracts. Read only selected registry entries after classification. Python validates decisions, not factual or pedagogical truth.

## Planning input

Before `plan_notes.py start`, add `instructional_plan` to each deep outline item. It contains `audience` (beginner/intermediate/advanced), `source_policy` (independent/strict/expanded/comparative), `sources`, and `concepts`. Each concept has a stable `id`, reader-facing `title`, nonempty `types` and `objectives`, `prerequisites`, `depth`, optional `modules`, and a concise `reason`. Use the concrete example in [evaluation fixtures](../../../examples/adaptive-deepnotes/scenarios.json).

Classify from the intended task and inspected source, never topic keywords alone. Registry types are conceptual, mathematical, programming, algorithmic, architectural, scientific, historical, comparative, procedural and research. Map computational to programming, geometrical to mathematical plus visualization, experimental to scientific, analytical/theoretical to the actual object and objective, and research-oriented to research. Mixed concepts select several types. Examination is an overlay: record syllabus/question expectations in `reason`, align practice to them, and preserve understanding. Source fidelity is a cross-cutting policy, not a separate master.

Prerequisites are objects with `concept` and `treatment`: known, reminder, explain or foundation. Internal dependencies must precede the consuming concept; known external foundations need a reader-baseline reason, while missing external material is explained locally before use. A major missing foundation becomes its own earlier concept. For strict sources retain source order and put necessary reminders immediately before use, clearly labeled; do not silently reorder the source. Cycles require decomposing shared foundations, not guessing an order.

Old outline fields still work: the adapter uses purpose, requested math level and selected tool, records its assumptions, and produces one concept. For substantial work author the richer plan before drafting; title/domain hints cannot substitute for semantic classification. Unknown objectives or malformed plans fail before writing.

## Selection and depth

For each concept, take the union of required objectives and source obligations. Registry objective values are minimum instructional capabilities, not word counts. Set independent `math`, `code`, `visual`, `theory`, `practice`, `assessment` levels. Explicit profiles can raise them; a conflict with a required objective must be resolved by changing scope or the plan, never silently clamped by subject. “Exhaustive” raises coverage of relevant ideas, not every dimension to 5.

| Level | Math | Code | Visual | Theory | Practice | Assessment |
|---|---|---|---|---|---|---|
| 0 | Omit | Omit | Omit | Omit | Omit | Omit |
| 1 | Relationship awareness | Pseudocode | Identify relationship | Recognition | Mention use | Recognize |
| 2 | Formula, symbols, conditions, substitution | Minimal executable case | Labeled representation | Definition and essential explanation | Explained use case | Explain distinction |
| 3 | Applied calculation and interpretation | Complete explained implementation | Trace relationships and values | Mechanism and assumptions | Worked multi-step task | Apply with answer/check |
| 4 | Justified derivation and verification | From scratch, trace, debug, tests | Connect representations or changing conditions | Deep causal/theoretical analysis | Unfamiliar transfer | Justify and diagnose |
| 5 | Rigorous theorem/proof when required | Robust engineering for actual constraints | Detailed multi-scale analysis | Guarantees and limits | Integrated design/project | Synthesis and mastery |

Each module inherits its dimension's level: select the corresponding output from its registry contract and expand only consequential steps. Derivation needs M4+, proof M5, code C2+ for executable blocks; C1 remains pseudocode. A scientific/research classification does not automatically require conducting an experiment: describe and assess the evidence at the required level. Theory depth alone never activates formal proof. A source-mandated formula, example, figure or exercise makes its relevant module required, with enough depth to explain it.

Apply depth to each selected module's particular output:

| Module | Awareness/essential (1–2) | Operational (3) | Deep/exhaustive (4–5) |
|---|---|---|---|
| Motivation | Name the need | Explain the baseline's limitation | Analyze constraints and competing needs |
| Intuition | Mental model; bounded analogy if helpful | Predict a transition from the model | Explain where the model breaks and refine it |
| Definitions | Define terms | Distinguish near misses and conventions | Formal conditions and subtle scope boundaries |
| Mathematics | Awareness/formula | Calculate and interpret | Derive/prove only as separately selected |
| Derivation | Excluded | Excluded | Justify transformations; extend validity analysis |
| Proof | Excluded | Excluded | M4 excluded; M5 complete argument and assumptions |
| Visualization | Identify/labeled relation | Trace values, flow or timeline | Connect multiple useful representations |
| Algorithm | Identify procedure | Pseudocode, trace and stopping conditions | Correctness, cost, variants and adversarial cases |
| Coding | Pseudocode/minimal program | Complete explained program | From scratch/debugging or robust engineering |
| Tracing | Show a state | Track consequential transitions | Isolate a fault and verify its correction |
| Examples | Recognize/direct case | Worked multi-step application | Transfer, counterexample or integrated problem |
| Applications | Mention/explain a use | Execute a workflow | Design or adapt an integrated solution |
| Comparison | Distinguish alternatives | Match criteria and choose | Analyze tradeoffs under changed constraints |
| Limitations | Name assumptions | Explain a failure and correction | Counterexamples and interacting failure regimes |
| History | Context and sequence | Causes, consequences and evidence | Competing interpretations and long-term connections |
| Experiment | Describe method/observations | Reproduce analysis or measurement reasoning | Evaluate uncertainty and alternative explanations |
| Assessment | Recognize/explain | Apply with worked checks | Transfer, justify, diagnose or synthesize |
| Revision | Key terms/relationships | Procedure or retrieval cues | Integrate dependencies and assess mastery |

Every module has required/supporting/optional/excluded status, depth and reason. Required means necessary to an objective, type or source obligation; supporting improves understanding; optional is a separate extension, unloaded by default; excluded is absent. Use `modules` overrides only with a reason. Required modules and dependencies cannot be excluded. Defaults do not force examples, code, visuals or mathematics where their dimension is zero. Promote a module to required for source coverage or a concrete misconception, then recheck its dependencies.

Select a stack only after choosing executable code (`code >= 2`). Prefer one tool at the needed abstraction: plain Python for an algorithm, NumPy for transparent numerical updates (note that `numpy.gradient` estimates finite differences on sampled arrays and does not provide automatic differentiation through a model), scikit-learn for estimator workflow, PyTorch/TensorFlow for tensor/autodiff APIs. Explicit user choices win. Additional tools require a comparison objective and distinct roles (or an explicitly requested stack). Classical threshold perceptron updates are not interchangeable with differentiable neuron training. Retain the existing runtime evidence protocol; unexecuted code stays labeled as such.

## Composition and generation

Choose one dominant subtemplate sequence per concept, then merge the useful steps of additional types. Assign every definition, equation, example and assumption one canonical home. Build one outline in dependency/source order, with domain-natural headings. Attach visuals and worked examples to the concept they explain; connect equations to code by the same symbols and fixture. Summaries serve retrieval, not repeated explanations. Add transitions explaining why the next concept follows. Do not publish module IDs or planning records as headings.

Generate a small coherent note in one pass. For large work, partition at source sections and independently teachable dependency boundaries; keep a derivation or algorithm trace intact. Soft budgets weight centrality, novelty, missing foundations, source elements and active depth. The helper reports an explicitly estimated budget, not provider tokens. If required content will not fit, split at a coherent boundary or increase the budget. Never discard it to meet the estimate.

Keep a run-local handoff containing completed/pending concept IDs, symbol definitions, assumptions, canonical homes, source element receipts, open gaps and next chunk inputs. Receive verified claims, qualifications, contradictions, citations, and unresolved gaps via a compact per-concept `research_package` from the [ARRIE research engine](../research/research-engine.md) (`scriptorium/engines/research.py (`scripts/scribe.py research`)`)—never dump raw scraped webpages into every generation pass. Compatible modules share a generation pass. Separate calls only for tool use, independent review or targeted repair. On correction, find dependent concepts, invalidate their receipts, update the smallest affected region and revalidate it. Do not regenerate unrelated completed notes.

Consolidate after the core: use an integrated case when objectives span concepts; choose recall, solutions, chronology, formula/procedure cues, mastery checks and next learning links to match the objective. Enrich concept delivery, representation alignment, worked examples, visuals, misconceptions, cognitive load, cross-topic connections, and multi-layer revision through [pedagogical-intelligence.md](pedagogical-intelligence.md) (`scriptorium/engines/pedagogy.py (`scripts/scribe.py pedagogy`)`) without overriding this engine's depth/module authority. Respect existing practice-file placement; no fixed example or question count in deep notes. Render with the existing five-key YAML and Markdown rules. Use the [source and QA protocol](../research/source-fidelity.md) before publication.
