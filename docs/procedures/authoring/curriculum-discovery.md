# Academic Curriculum Discovery & Concept Coverage

## Purpose

Prevent substantive independent notes from relying solely on ad-hoc model recall or mistaking length for completeness. Combine **research-driven syllabus discovery**, an **internal knowledge coverage matrix**, **prerequisite closure**, and an **explicit exclusion audit**.

## Activation & Source-Policy Precedence

- **Activate on:** Comprehensive independent `M1` notes, multi-branch collections, and unfamiliar disciplines where no specialized user syllabus is supplied.
- **Strict source-mode precedence:** Under `source_policy = strict`, **do not browse externally**. Perform curriculum discovery and coverage mapping strictly within the supplied source material, recording any source omissions as honest gaps.

## 1. Academic Curriculum Discovery Phase

Before drafting a comprehensive independent note on a subject, consult authoritative academic references (via [research-engine.md](../sourcing/research-engine.md)) to identify:

1. Standard concepts, canonical terminology, and notation conventions.
2. Conventional pedagogical progression, simpler baselines improved upon, and essential prerequisites.
3. Core theorems, governing laws, mechanisms, or mathematical tools required before advanced formulas.
4. Major task types, variants, special cases, and ideal-to-real refinements.
5. Practical configuration/parameters, workflows, inference/deployment usage, and official versioned behaviors.
6. Established student difficulties and common misconceptions.
7. Foundational experiments, empirical evidence, canonical benchmarks, or primary references.
8. Comparisons with nearest alternatives and advanced extensions inside vs. outside scope.
9. Section-level visual opportunities across foundational intuition, mathematics/geometry, structures, mechanisms, algorithmic steps, parameter behavior, comparisons, worked examples, failure regimes, and advanced extensions—planning targeted web searches for verified existing illustrations per [representations.md](../authoring/representations.md) (never generating images).

### Preferred Reference Categories by Discipline

| Discipline | Preferred Authoritative Curriculum References |
|---|---|
| **Computer Science** | University courses, ACM/IEEE curricular guidance, established textbooks |
| **Programming** | Language specifications, official documentation, established texts |
| **Mathematics** | University syllabi, OpenStax, established mathematical textbooks |
| **Physics** | OpenStax, university lecture notes, established physics texts |
| **Chemistry** | IUPAC references, university courses, established chemistry textbooks |
| **Biology** | Established biology textbooks, NCBI resources, university curricula |
| **Economics** | CORE Econ, university courses, established economics textbooks |
| **Engineering** | Accredited curricula, engineering textbooks, applicable standards |
| **History** | Academic histories, archival collections, scholarly reference works |
| **Philosophy** | Stanford Encyclopedia of Philosophy, peer-reviewed academic texts |

### Discipline-Specific Discovery Lenses *(Planning Only — Never Compulsory Headings or Forced Computational Structures)*
- **Algorithms:** Problem solved, why simpler approaches fall short, core ideas, algorithm structure, training vs. inference, objective & optimization mechanism, data representation, parameters, computational behavior & assumptions, failures, applications, comparisons, variants.
- **Mathematics:** Motivation, definitions, intuition, mathematical objects, theorems, derivations/proofs, geometrical interpretation, numerical examples, problem types, conditions, counterexamples, applications.
- **Natural Sciences:** Relevant phenomena, physical/biological structures, governing principles, causal mechanisms, evidence & experiments, mathematical relationships with units, assumptions, limitations, real-world significance.
- **History / Philosophy:** Necessary context, central concepts, chronology (where relevant), causal relationships, arguments, evidence, competing interpretations, distinctions, consequences, evidence limits.

## 2. Internal Knowledge Coverage Matrix & Classification

Before drafting a major theory note or collection, enrich the [shared internal concept record](adaptive-engine.md) with a compact **internal** coverage check classifying discovered concepts into: `Essential foundation`, `Central theory`, `Consequential mathematical reasoning`, `Important application`, `Important limitation`, `Supporting detail`, `Advanced extension`, or `Out-of-scope material` (do **not** publish this planning table as clutter in the finished note):

| Column | Meaning |
|---|---|
| **Concept & Coverage Class** | Distinct concept, mechanism, or distinction + classification above |
| **Role** | `Prerequisite`, `Core`, `Extension`, or `Advanced` |
| **Required depth** | Unified `0–5` theory depth (`1 Recognition` through `5 Independent transfer` in [adaptive-engine.md](adaptive-engine.md)) |
| **Observable completion condition** | Concrete test proving the concept was taught (e.g., *"Trace a complete virtual-to-physical address translation and contrast a TLB miss with a page/permission fault"*) |

**Adaptive Educational Depth & Completion Rule:** Allocate explanation proportionally to conceptual importance: develop central theory comprehensively, teach essential prerequisites strictly to the depth needed for dependent reasoning, treat supporting details proportionally, and clearly distinguish advanced extensions. Simply mentioning a concept (`Level 1`) never satisfies a `Core` (`Level 3–5`) or `Central theory` completion condition. For comprehensive `M1` notes, map all major pillars of the subject (foundations/baselines, core mechanism & mathematical tools, major task types/variants, practical parameters/workflows, limitations, comparisons, and primary references) so no central pillar is silently omitted. Before acceptance, compare finished prose against planned objectives to catch omitted, mentioned-but-untaught, or prerequisite-missing concepts; if scope exceeds output capacity, deliver complete bounded learning units and disclose remaining material rather than mislabeling a partial summary as comprehensive.

## 3. Prerequisite Closure & Coverage/Exclusion Audit

1. **Prerequisite closure check:** For every `Core` concept in the matrix, verify that every prerequisite it depends on is either taught locally beforehand (essential) or explicitly bridged (supporting). If a late section introduces an unexplained term, symbol, or mechanism, add the missing prerequisite bridge upstream.
2. **Cross-chapter continuity (for multi-branch collections):** Carry consistent notation, running examples where appropriate, and explicit backward/forward links across chapters so quality and depth do not degrade in later chapters.
3. **Explicit exclusion audit:** Identify adjacent advanced concepts intentionally left out of scope (e.g., *"Huge pages and NUMA-aware page migration are out of scope here"*). State the scope boundary cleanly in the note's closing or `nexttopics` so omissions are deliberate rather than accidental.
