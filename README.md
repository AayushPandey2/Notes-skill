# Scriptorium

**Scriptorium** is an instruction-and-reference-only agentic skill for authoring, organizing, and reviewing **Obsidian Markdown learning notes**. It consists purely of declarative Markdown instructions, templates, domain subtemplates, and routing metadata—with zero custom Python/JavaScript runtimes, download scripts, or build dependencies.

---

## 1. Public Commands (`skills/`)

| Command | Entrypoint | What It Does | Writes to Vault? |
|---|---|---|---|
| `/scribe-notes` | [skills/scribe-notes/SKILL.md](skills/scribe-notes/SKILL.md) | Creates or revises notes per `artifact_policy` in [master-registry.yaml](docs/dispatch/master-registry.yaml) (`M1`/`M2` default to 3-file bundles; `M3`–`M7` emit single/implementation artifacts). | Yes (notes, conditional companions, inspected local assets) |
| `/scribe-ytnotes` | [skills/scribe-ytnotes/SKILL.md](skills/scribe-ytnotes/SKILL.md) | Creates one self-contained, transcript-first note per video using downloaded web visuals and clickable timestamps (no lab, no frame capture). | Yes (1 note per video + local web images) |
| `/scribe-doubt` | [skills/scribe-doubt/SKILL.md](skills/scribe-doubt/SKILL.md) | Answers questions strictly from existing vault notes with exact `[[Note Title#Heading]]` citations. | No (read-only) |
| `/scribe-quiz` | [skills/scribe-quiz/SKILL.md](skills/scribe-quiz/SKILL.md) | Runs an interactive, one-question-per-turn recall or viva quiz grounded in existing vault notes. | No by default (optional body review note only if requested) |
| `/scribe-setfolder` | [skills/scribe-setfolder/SKILL.md](skills/scribe-setfolder/SKILL.md) | Sets or inspects the default Obsidian vault and target notes folder. | Config only (`~/.scriptorium-config.json`) |

Root orchestration starts at [SKILL.md](SKILL.md) (with an 8-level governance precedence hierarchy), routes across four independent dimensions via [router.md](router.md), [master-registry.yaml](docs/dispatch/master-registry.yaml), and [subject-registry.yaml](docs/dispatch/subject-registry.yaml), and resolves destinations via [pre-gen-gate.md](docs/procedures/authoring/pre-gen-gate.md) (precedence: explicit vault path > `SCRIPTORIUM_VAULT_PATH` > `~/.scriptorium-config.json`).

---

## 2. How the Authoring Workflow Operates

1. **Intent & Route Resolution:** [router.md](router.md) and [routing-policy.md](docs/dispatch/routing-policy.md) select the output format (`M1`–`M7`, or `video-notes.md` for `/scribe-ytnotes`) and load only the needed files via [docs/README.md](docs/README.md).
2. **Destination & Safety Gate:** [pre-gen-gate.md](docs/procedures/authoring/pre-gen-gate.md) checks existing vault files before writing, preserves custom YAML/notes, and prevents accidental overwrites.
3. **Research & Source Fidelity:** [research-engine.md](docs/procedures/sourcing/research-engine.md) and [source-fidelity.md](docs/procedures/sourcing/source-fidelity.md) ground claims with locators, respect source-only boundaries, and mark unconfirmed claims `[UNVERIFIED]`.
4. **Self-Contained Layered Teaching, Theory Quality & Unified Math Policy:** [teaching_core.md](core/teaching_core.md) and [theory_quality_contract.md](core/theory_quality_contract.md) enforce genuine zero-prerequisite ordering, separated metadata, clickable Obsidian TOC links, progressive abstraction, multi-perspective explanations, forward/reverse reasoning, ideal-to-real model progression, epistemic claim classification, question-specific reasoning patterns, and calm reference prose. [curriculum-discovery.md](docs/procedures/authoring/curriculum-discovery.md) and [subject-theory-profiles.md](docs/blueprints/components/subject-theory-profiles.md) provide research-driven syllabus discovery, shared internal concept records, selectable topic-family completeness checklists, and a misconception library. [math_gates.md](core/math_gates.md) governs objective-driven math inclusion across five internal concept profiles, coherent unit grouping, compact-reference exceptions, non-recursive `> [!example]- Understand this formula step by step` folds, and equation-to-code alignment.
5. **Relevance-Governed Visuals & Source Hierarchy:** [representations.md](docs/procedures/authoring/representations.md) uses a 5-level visual source hierarchy, adaptive image sizing, diagram-to-model correspondence, and relevance-based acquisition (disabled under `strict` source-only mode), while forbidding Mermaid or ASCII graphs/diagrams.
6. **Artifact Cardinality & Subject-Tailored Labs:** `artifact_policy` in [master-registry.yaml](docs/dispatch/master-registry.yaml) controls bundle emission (`M1`/`M2` default to 3-file bundles; `M3`/`M4`/`M6`/`M7` emit single artifacts; `M5` emits an implementation guide without duplicating an identical lab; `/scribe-ytnotes` emits one self-contained note per video). [experimental-lab.md](docs/procedures/authoring/experimental-lab.md) uses four universal practical perspectives, shared-foundation + track-specific walkthroughs, and 3-attribute experiment integrity (*Origin*, *Method*, *Verification*).
7. **Lean 6-Stage Review & Adversarial Verification:** [verification-checklist.md](docs/procedures/review/verification-checklist.md) and [adversarial-theory-review.md](docs/procedures/review/adversarial-theory-review.md) perform 6-stage quality, unified 0–5 theory-depth, safety-policy, and delivery checks against the actual saved Markdown.

---

## 3. Output Formats, Domains, Presets & Labs (`docs/blueprints/`)

- **Formats (`formats/`):**
  - `M1` [deep-notes.md](docs/blueprints/formats/deep-notes.md) — First-principles comprehensive notes & collections
  - `M2` [study-notes.md](docs/blueprints/formats/study-notes.md) — Source-ordered lecture/PDF/chapter study notes
  - `M3` [quick-reference.md](docs/blueprints/formats/quick-reference.md) — Dense cheat sheets & reference cards
  - `M4` [worked-solutions.md](docs/blueprints/formats/worked-solutions.md) — Step-by-step problem solving
  - `M5` [implementation-guide.md](docs/blueprints/formats/implementation-guide.md) — Algorithms, data structures & verification guides
  - `M6` [assessment.md](docs/blueprints/formats/assessment.md) — Tiered active-recall practice sets
  - `M7` [synthesis-revision.md](docs/blueprints/formats/synthesis-revision.md) — Cross-note comparisons, paper breakdowns & revision packs
  - [video-notes.md](docs/blueprints/formats/video-notes.md) — Single-file, transcript-first, web-image-led notes for `/scribe-ytnotes`
- **Knowledge-Type Subtemplates (`domains/`):** [conceptual.md](docs/blueprints/domains/conceptual.md), [mathematical.md](docs/blueprints/domains/mathematical.md), [computational.md](docs/blueprints/domains/computational.md), [scientific.md](docs/blueprints/domains/scientific.md), [empirical.md](docs/blueprints/domains/empirical.md), [historical.md](docs/blueprints/domains/historical.md).
- **Presets (`presets/`):** `atomic-card`, `command-reference`, `comparison-guide`, `concept-map`, `flashcards`, `formula-sheet`, `lecture-order`, `mock-exam`, `paper-breakdown`, `quick-summary`, `revision-pack`, `syntax-reference`.
- **Subject Theory & Investigation Blueprints (`subjects/` & `investigations/`):** Mapped cleanly via [subject-registry.yaml](docs/dispatch/subject-registry.yaml) across `machine-learning`, `deep-learning`, `generative-ai`, `fullstack`, `cybersecurity`, `electrical`, `algorithms`, `operating-systems`, `networking`, `databases`, `devops`, `distributed-systems`, `mathematics`, `statistics`, `physics`, `chemistry`, `biology`, `coding`, and `general`, with safety boundaries in [security-education.md](docs/procedures/safety/security-education.md) and [physical-lab-safety.md](docs/procedures/safety/physical-lab-safety.md).

---

## 4. Repository File Structure

```text
scriptorium/
├── .agents/skills.json              # Skill discovery manifest pointing to skills/
├── SKILL.md                         # Root entrypoint & authoring rule
├── router.md                        # Master format selector (M1–M7 & video-notes)
├── README.md                        # Project overview, workflows & directory map
├── LICENSE                          # MIT License
├── skills/                          # Public slash-command entrypoints
│   ├── scribe-notes/SKILL.md
│   ├── scribe-ytnotes/SKILL.md
│   ├── scribe-doubt/SKILL.md
│   ├── scribe-quiz/SKILL.md
│   └── scribe-setfolder/SKILL.md
├── core/                            # Cross-command authoring & teaching rules
│   ├── runtime_pipeline.md          # Direct-authoring workflow (no scripts)
│   ├── teaching_core.md             # Zero-prerequisite flow, tiered concepts & voice
│   ├── theory_quality_contract.md   # Progressive abstraction, perspectives, claim status & transfer
│   ├── math_gates.md                # Objective-driven math profiles & formula folds
│   ├── authoring_rules.md           # YAML profiles, Obsidian Markdown & naming rules
│   └── footer_widgets.md            # Vault navigation footer cues
├── docs/                            # Selectively loaded references
│   ├── README.md                    # Reference loading index
│   ├── design/                      # System overview & template-module catalog
│   ├── dispatch/                    # master-registry.yaml, subject-registry.yaml & routing-policy.md
│   ├── properties/                  # properties-policy.md & tag-taxonomy.md
│   ├── specs/                       # migration-notes.md
│   ├── blueprints/                  # Formats, domains, subjects, presets, components & labs
│   │   ├── formats/                 # M1–M7 + video-notes.md
│   │   ├── domains/                 # 6 knowledge-type subtemplates
│   │   ├── subjects/                # 17 domain-specific theory blueprints
│   │   ├── presets/                 # 12 specialized output presets
│   │   ├── components/              # Module catalog & subject theory/misconception profiles
│   │   └── investigations/          # 19 domain experimental lab templates
│   └── procedures/                  # Conditional authoring, sourcing, safety, updating & review
│       ├── authoring/               # Adaptive planning, curriculum discovery, playbooks, 3-file contracts, visuals, gate
│       ├── sourcing/                # Research engine, source fidelity & recommendations
│       ├── safety/                  # Security education & physical/wet-lab safety policies
│       ├── updating/                # Revision & safe vault linking
│       └── review/                  # Manual verification checklist & adversarial theory review
└── evaluations/                     # Declarative trigger, adversarial & cross-domain evals
    ├── evals.json
    ├── trigger_eval.json
    ├── rubrics/                     # Evaluation-only theory, practical & presentation rubrics
    └── fixtures/                    # Evaluation-only golden vs. flawed contrast fixtures
```

---

## 5. Limits & Maintenance

- **Honest verification:** Scriptorium relies on direct Markdown authoring and manual checklist review; it does not provide automated code execution, cryptographic publication receipts, atomic multi-file transactions, or live Obsidian UI rendering checks.
- **Maintenance:** Keep executable scripts out of the repository, update affected callers and `evaluations/` when modifying shared rules, and see [migration-notes.md](docs/specs/migration-notes.md) and [LICENSE](LICENSE) for history and licensing.
