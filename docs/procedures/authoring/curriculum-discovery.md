# Academic Curriculum Discovery & Concept Coverage

## Purpose

Prevent substantive independent notes from relying solely on ad-hoc model recall or mistaking length for completeness. Combine **research-driven syllabus discovery**, an **internal knowledge coverage matrix**, **prerequisite closure**, and an **explicit exclusion audit**.

## Activation & Source-Policy Precedence

- **Activate on:** Comprehensive independent `M1` notes, multi-branch collections, and unfamiliar disciplines where no specialized user syllabus is supplied.
- **Strict source-mode precedence:** Under `source_policy = strict`, **do not browse externally**. Perform curriculum discovery and coverage mapping strictly within the supplied source material, recording any source omissions as honest gaps.

## 1. Academic Curriculum Discovery Phase

Before drafting a comprehensive independent note on a subject, consult authoritative academic references (via [research-engine.md](../sourcing/research-engine.md)) to identify:

1. Standard concepts, canonical terminology, and notation conventions.
2. Conventional pedagogical progression and essential prerequisites.
3. Core theorems, governing laws, mechanisms, or frameworks.
4. Important variants, special cases, and ideal-to-real refinements.
5. Established student difficulties and common misconceptions.
6. Foundational experiments, empirical evidence, or canonical benchmarks.
7. Advanced extensions that belong inside vs. outside the requested scope.

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

## 2. Internal Knowledge Coverage Matrix (Aligned to Unified Concept Record)

Before drafting a major theory note or collection, enrich the [shared internal concept record](adaptive-engine.md) with a compact **internal** coverage check (do **not** publish this planning table as clutter in the finished note):

| Column | Meaning |
|---|---|
| **Concept** | Distinct concept, mechanism, or distinction to teach |
| **Role** | `Prerequisite`, `Core`, `Extension`, or `Advanced` |
| **Required depth** | Unified `0–5` theory depth (`1 Recognition` through `5 Independent transfer` in [adaptive-engine.md](adaptive-engine.md)) |
| **Observable completion condition** | Concrete test proving the concept was taught (e.g., *"Trace a complete virtual-to-physical address translation and contrast a TLB miss with a page/permission fault"*) |

**Rule:** Simply mentioning a concept (`Level 1`) never satisfies a `Core` (`Level 3–5`) completion condition. Every high-priority concept must meet its observable completion condition before review passes.

## 3. Prerequisite Closure & Coverage/Exclusion Audit

1. **Prerequisite closure check:** For every `Core` concept in the matrix, verify that every prerequisite it depends on is either taught locally beforehand (essential) or explicitly bridged (secondary). If a late section introduces an unexplained term, symbol, or mechanism, add the missing prerequisite bridge upstream.
2. **Cross-chapter continuity (for multi-branch collections):** Carry consistent notation, running examples where appropriate, and explicit backward/forward links across chapters so quality and depth do not degrade in later chapters.
3. **Explicit exclusion audit:** Identify adjacent advanced concepts intentionally left out of scope (e.g., *"Huge pages and NUMA-aware page migration are out of scope here"*). State the scope boundary cleanly in the note's closing or `nexttopics` so omissions are deliberate rather than accidental.
