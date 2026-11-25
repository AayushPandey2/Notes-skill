# Instructional planning and composition

Load this for deep study. The [M1 master](../../blueprints/formats/deep-notes.md) owns document composition; [registry](instructional-registry.json) maps knowledge types to subtemplates. Read only selected entries after classification. Review depth choices against the learner request; no program validates them.

## Planning input

Before authoring, identify audience, source policy (`independent`, `strict`, `source_first`, `expanded`, or `comparative`), learning objectives, and important concepts. For each concept, note its prerequisites, needed depth, and main teaching home. Keep this as a short plan; do not create a JSON builder.

Classify from the intended task and inspected source, never topic keywords alone. Registry types are conceptual, mathematical, programming, algorithmic, architectural, scientific, historical, comparative, procedural and research. Map computational to programming, geometrical to mathematical plus visualization, experimental to scientific, analytical/theoretical to the actual object and objective, and research-oriented to research. Mixed concepts select several types. Examination is an overlay: record syllabus/question expectations in `reason`, align practice to them, and preserve understanding. Source fidelity is a cross-cutting policy, not a separate master.

Treat prerequisites using the 3-tier rule in [teaching_core.md](../../../core/teaching_core.md): **essential now** (explain locally before first use), **useful but secondary** (short bridge + optional link), and **outside the learning objective** (state boundary + link for further study). A link must never substitute for a missing essential explanation. For source-ordered notes, retain the source sequence and label necessary bridges; do not silently reorder it. Break cycles by explaining a shared foundation first.

### Audience & Scope Presets

Scale scope and support consistently without removing the reasoning necessary to understand the preset's stated learning objective (history remains optional):
- **Beginner presets:** Supply more local prerequisite bridges, one conceptual burden at a time, and concrete examples beside definitions.
- **Advanced presets:** Increase causal/formal depth, boundary conditions, and technical qualifications without skipping necessary definitions.
- **Comprehensive presets:** Expand mechanisms, worked examples, evidence, and transfer across [teaching_core.md](../../../core/teaching_core.md), paired with the companion lab and companion cheatsheet/tiered-Q&A/worked-problems file.
- **Compact presets (`M3`, `quick-summary`, `atomic-card`):** Narrow scope and reduce repetition while preserving all reasoning needed for the retained objective.

Old outline fields still work: the adapter uses purpose, requested math level and selected tool, records its assumptions, and produces one concept. For substantial work author the richer plan before drafting; title/domain hints cannot substitute for semantic classification. Unknown objectives or malformed plans fail before writing.

## Selection and depth

For each concept, combine the learner's objectives with important source material. Choose the needed depth for math, code, visuals, theory, practice, and assessment separately; these are planning judgments, not word counts or domain-wide defaults. For `Math`, map directly to the five internal concept-level profiles in [math_gates.md](../../../core/math_gates.md) (`Conceptual`, `Quantitative intuition`, `Working formulation`, `Derivation and mechanism`, `Formal reasoning`)—using the minimum depth that satisfies the objective. If a requested scope conflicts with required source material, resolve the scope openly. “Exhaustive” means covering relevant ideas, not maximizing every dimension.

| Level | Math | Code | Visual | Theory | Practice | Assessment |
|---|---|---|---|---|---|---|
| 0 | Omit | Omit | Omit | Omit | Omit | Omit |
| 1 | Relationship awareness | Pseudocode | Identify relationship | Recognition | Mention use | Recognize |
| 2 | Formula, symbols, conditions, substitution | Minimal executable case | Labeled representation | Definition and essential explanation | Explained use case | Explain distinction |
| 3 | Applied calculation and interpretation | Complete explained implementation | Trace relationships and values | Mechanism and assumptions | Worked multi-step task | Apply with answer/check |
| 4 | Justified derivation and verification | From scratch, trace, debug, tests | Connect representations or changing conditions | Deep causal/theoretical analysis | Unfamiliar transfer | Justify and diagnose |
| 5 | Rigorous theorem/proof when required | Robust engineering for actual constraints | Detailed multi-scale analysis | Guarantees and limits | Integrated design/project | Synthesis and mastery |

Use the [module guide](../../blueprints/components/module-catalog.md) only for teaching moves that serve the objective. Explain derivations or proofs when requested or needed for the claim; include educational code only when it serves the lesson. Scientific or research notes may explain an experiment without conducting one. A source-mandated formula, example, figure, or exercise needs enough explanation to preserve its meaning.

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

Use a teaching move when the objective or source requires it, or when it materially improves understanding. Omit moves that add no value; a default template must not force code, diagrams, or mathematics into an unrelated subject. Recheck prerequisite explanations when adding a new concept or misconception correction.

Select a computational tool only after choosing executable code (`code >= 2`). Prefer the minimal abstraction matching the pedagogical goal—pure host-language logic for core algorithms, lightweight array/matrix operations for transparent mathematical mechanics, or higher-level libraries when the learning objective requires them. Companion ML labs always follow the 4-track implementation contract in [experimental-lab.md](experimental-lab.md). Distinguish discrete finite-difference approximations from exact symbolic/automatic differentiation, and preserve distinct algorithmic formulations without conflating incompatible models. Explicit user tool choices always take precedence; verify code statically against official docs without local execution and label it `Source and static review only; not compiled or executed here.`

## Composition and generation

Choose one dominant subtemplate sequence per concept, then merge the useful steps of additional types. Assign every definition, equation, example and assumption one canonical home. Build one outline in dependency/source order, with domain-natural headings. Attach visuals and worked examples to the concept they explain; connect equations to code by the same symbols and fixture. Summaries serve retrieval, not repeated explanations. Add transitions explaining why the next concept follows. Do not publish module IDs or planning records as headings.

Generate a small coherent note in one pass. For large work, partition at source sections and independently teachable dependency boundaries; keep a derivation or algorithm trace intact. Soft budgets weight centrality, novelty, missing foundations, source elements and active depth. The helper reports an explicitly estimated budget, not provider tokens. If required content will not fit, split at a coherent boundary or increase the budget. Never discard it to meet the estimate.

Keep a run-local mental/outline checklist of completed/pending concept IDs, symbol definitions, assumptions, canonical homes, and open gaps. Gather verified claims, qualifications, contradictions, citations, and unresolved gaps via [ARRIE](../sourcing/research-engine.md)—never dump raw scraped webpages into every pass. On correction, find dependent concepts, update the smallest affected region, and re-review it. Do not regenerate unrelated completed notes.

Consolidate after the core: use an integrated case when objectives span concepts; choose recall, solutions, chronology, formula/procedure cues, mastery checks and next learning links to match the objective. Enrich concept delivery, representation alignment, worked examples, visuals, misconceptions, cognitive load, cross-topic connections, and multi-layer revision through [pedagogical-intelligence.md](pedagogical-intelligence.md). Respect existing practice-file placement; no fixed example or question count in deep notes. Render with the existing five-key YAML and Markdown rules. Use the [source and QA protocol](../sourcing/source-fidelity.md) before finishing.
