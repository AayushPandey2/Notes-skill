# Scriptorium

**Scriptorium** is a strictly **instruction-and-reference-only** agentic skill for authoring, organizing, and reviewing **Obsidian Markdown learning notes**. The entire repository (`SKILL.md`, `core/`, `docs/`, `skills/`, and `evaluations/`) consists purely of declarative Markdown instructions, templates, domain subtemplates, routing metadata, and manual evaluation rubrics—with **zero** executable scripts, custom validators, stored sample vaults, or pre-generated educational note bundles.

---

## Repository-local skills

Open the full checkout as the project or workspace so the agent can discover `scriptorium` and the six `scribe-*` skills using the paths below.

| Agent | Discovery path |
|---|---|
| Claude Code | `.claude/skills/` |
| Codex and Antigravity | `.agents/skills/` |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` |

The discovery files forward to the canonical instructions in `SKILL.md` and `skills/`. A copied wrapper needs the surrounding checkout to resolve its references.

### Upload to Claude

For the six slash-menu entries in Claude Desktop Chat or Cowork, open **Plugins** and upload a plugin ZIP. For one combined Scriptorium skill, use the **Skills** upload instead. Create the corresponding ZIP from a checkout of this repository:

```sh
git archive --format=zip --output=../scriptorium-plugin.zip HEAD \
  .claude-plugin SKILL.md LICENSE router.md core docs skills

git archive --format=zip --prefix=scriptorium/ --output=../scriptorium-skill.zip HEAD \
  SKILL.md LICENSE router.md core docs skills
```

These commands archive committed `HEAD` only. The plugin archive places [the manifest](.claude-plugin/plugin.json) at the root, and the skill archive uses a single `scriptorium/` folder. Both include the policies required by the canonical skills. [Claude plugin installation](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) · [Claude custom skill installation](https://support.claude.com/en/articles/12512180-use-skills-in-claude)

## 1. Public Commands (`skills/`)

| Command | Entrypoint | What It Does | Writes to Vault? |
|---|---|---|---|
| `/scribe-notes` | [skills/scribe-notes/SKILL.md](skills/scribe-notes/SKILL.md) | Creates or revises notes per `artifact_policy` in [master-registry.yaml](docs/dispatch/master-registry.yaml) and the resolved `artifact_plan` (`M1`/`M2` default to conditional bundles up to 3 files; `M3`–`M7` emit single/implementation artifacts). | Yes (notes, conditional companions, inspected local assets) |
| `/scribe-ytnotes` | [skills/scribe-ytnotes/SKILL.md](skills/scribe-ytnotes/SKILL.md) | Creates one self-contained, transcript-first note per video using conditional downloaded web visuals when helpful/permitted and clickable timestamps (no lab, no frame capture). | Yes (1 note per video + conditional local web images) |
| `/scribe-doubt` | [skills/scribe-doubt/SKILL.md](skills/scribe-doubt/SKILL.md) | Answers questions strictly from existing vault notes with exact `[[Note Title#Heading]]` citations. | No (read-only) |
| `/scribe-quiz` | [skills/scribe-quiz/SKILL.md](skills/scribe-quiz/SKILL.md) | Runs an interactive, one-question-per-turn recall or viva quiz grounded in existing vault notes. | No by default (optional body review note only if requested) |
| `/scribe-audit` | [skills/scribe-audit/SKILL.md](skills/scribe-audit/SKILL.md) | Audits existing vault notes read-only across theory, math, prerequisites, lab integrity, evidence, presentation, and consistency dimensions. | No (read-only by default) |
| `/scribe-setfolder` | [skills/scribe-setfolder/SKILL.md](skills/scribe-setfolder/SKILL.md) | Sets or inspects the default Obsidian vault and target notes folder. | Config only (`~/.scriptorium-config.json`) |

The root skill establishes the order of authority. The routing policy separates format, knowledge type, subject and practical investigation. The destination policy resolves explicit paths, environment settings and saved configuration in that order. [Root skill](SKILL.md) · [Routing policy](docs/dispatch/routing-policy.md) · [Destination policy](docs/procedures/authoring/pre-gen-gate.md)

---

## 2. How the Authoring Workflow Operates

1. **Intent & Route Resolution:** [router.md](router.md) and [routing-policy.md](docs/dispatch/routing-policy.md) select the output format (`M1`–`M7`, or `video-notes.md` for `/scribe-ytnotes`) and load only the needed files via [docs/README.md](docs/README.md), orchestrated by [runtime_pipeline.md](core/runtime_pipeline.md).
2. **Destination & Safety Gate:** [pre-gen-gate.md](docs/procedures/authoring/pre-gen-gate.md) resolves paths without premature folder creation, preserves custom YAML/notes, and prevents accidental overwrites.
3. **Research & Source Fidelity:** [research-engine.md](docs/procedures/sourcing/research-engine.md) and [source-fidelity.md](docs/procedures/sourcing/source-fidelity.md) ground claims with locators, respect source-only boundaries, and mark unconfirmed claims `[UNVERIFIED]`.
4. **Self-Contained Layered Teaching, Theory Quality & Unified Math Policy:** [teaching_core.md](core/teaching_core.md) and [theory_quality_contract.md](core/theory_quality_contract.md) enforce prerequisite closure, separated metadata, clickable Obsidian TOC links, progressive abstraction, multi-perspective explanations, forward/reverse reasoning, ideal-to-real model progression, epistemic claim classification, question-specific reasoning patterns, and textbook-clear prose. [curriculum-discovery.md](docs/procedures/authoring/curriculum-discovery.md) and [subject-theory-profiles.md](docs/blueprints/components/subject-theory-profiles.md) provide research-driven syllabus discovery, shared internal concept records, selectable topic-family completeness checklists, and a misconception library. [math_gates.md](core/math_gates.md) governs objective-driven math inclusion across five internal concept profiles, visible reasoning units, complete descriptive derivation folds, source boundaries, and equation-to-code alignment.
5. **Relevance-Governed Visuals & Source Hierarchy:** [representations.md](docs/procedures/authoring/representations.md) uses a 5-level visual source hierarchy, adaptive image sizing, diagram-to-model correspondence, and relevance-governed acquisition (disabled under `strict` source-only mode), while forbidding Mermaid or ASCII graphs/diagrams.
6. **Artifact Cardinality & Subject-Tailored Labs:** The extensible `artifact_plan` in [adaptive-engine.md](docs/procedures/authoring/adaptive-engine.md) and `artifact_policy` in [master-registry.yaml](docs/dispatch/master-registry.yaml) control bundle emission (`M1`/`M2` default to conditional bundles resolved against source constraints and user overrides; `M3`/`M4`/`M6`/`M7` emit single artifacts; `M5` emits an implementation guide without duplicating an identical lab; `/scribe-ytnotes` emits one self-contained note per video). [experimental-lab.md](docs/procedures/authoring/experimental-lab.md) uses four universal practical perspectives, shared-foundation + track-specific walkthroughs, and 3-attribute experiment integrity (*Origin*, *Method*, *Verification*).
7. **Manual 6-Stage Review & Adversarial Verification:** [verification-checklist.md](docs/procedures/review/verification-checklist.md) and [adversarial-theory-review.md](docs/procedures/review/adversarial-theory-review.md) run Stages 1–5 completely before saving and Stage 6 after saving against the actual saved Markdown.

---

## 3. Output Formats, Domains, Presets & Labs (`docs/blueprints/`)

- **Formats (`formats/`):**
  - `M1` [deep-notes.md](docs/blueprints/formats/deep-notes.md) — First-principles comprehensive notes & collections
  - `M2` [study-notes.md](docs/blueprints/formats/study-notes.md) — Source-ordered lecture/PDF/chapter study notes
  - `M3` [quick-reference.md](docs/blueprints/formats/quick-reference.md) — Dense cheat sheets & reference cards
  - `M4` [worked-solutions.md](docs/blueprints/formats/worked-solutions.md) — Step-by-step problem solving
  - `M5` [implementation-guide.md](docs/blueprints/formats/implementation-guide.md) — Algorithms, systems, models & software implementation guides
  - `M6` [assessment.md](docs/blueprints/formats/assessment.md) — Tiered active-recall practice sets
  - `M7` [synthesis-revision.md](docs/blueprints/formats/synthesis-revision.md) — Cross-note comparisons, paper breakdowns & revision packs
  - [video-notes.md](docs/blueprints/formats/video-notes.md) — Single-file, transcript-first notes with conditional web visuals for `/scribe-ytnotes`
- **Knowledge-Type Subtemplates (`domains/`):** [conceptual.md](docs/blueprints/domains/conceptual.md), [mathematical.md](docs/blueprints/domains/mathematical.md), [computational.md](docs/blueprints/domains/computational.md), [scientific.md](docs/blueprints/domains/scientific.md), [empirical.md](docs/blueprints/domains/empirical.md), [historical.md](docs/blueprints/domains/historical.md).
- **Presets (`presets/`):** `atomic-card`, `command-reference`, `comparison-guide`, `concept-map`, `flashcards`, `formula-sheet`, `lecture-order`, `mock-exam`, `paper-breakdown`, `quick-summary`, `revision-pack`, `syntax-reference`.
- **Subject Theory & Investigation Blueprints (`subjects/` & `investigations/`):** Mapped cleanly via [subject-registry.yaml](docs/dispatch/subject-registry.yaml) across `21` specialized subject theory blueprints plus the `general` fallback (`22` registry entries total: `machine_learning`, `deep_learning`, `generative_ai`, `programming`, `algorithms`, `fullstack`, `cybersecurity`, `electrical`, `operating_systems`, `computer_architecture`, `numerical_computing`, `information_theory`, `networking`, `databases`, `devops`, `distributed_systems`, `mathematics`, `statistics`, `physics`, `chemistry`, `biology`, and `general`), with safety boundaries in [security-education.md](docs/procedures/safety/security-education.md) and [physical-lab-safety.md](docs/procedures/safety/physical-lab-safety.md).

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
│   ├── scribe-audit/SKILL.md
│   └── scribe-setfolder/SKILL.md
├── core/                            # Cross-command authoring & teaching rules
│   ├── runtime_pipeline.md          # Direct-authoring workflow (no scripts)
│   ├── teaching_core.md             # Zero-prerequisite flow, tiered concepts & voice
│   ├── theory_quality_contract.md   # Progressive abstraction, perspectives, claim status & transfer
│   ├── math_gates.md                # Objective-driven math profiles & formula folds
│   ├── authoring_rules.md           # Obsidian Markdown, presentation & prose rules
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
│   │   ├── subjects/                # 21 domain-specific theory blueprints
│   │   ├── presets/                 # 12 specialized output presets
│   │   ├── components/              # Module catalog, example engineering & subject/misconception profiles
│   │   └── investigations/          # 22 domain experimental lab templates
│   └── procedures/                  # Conditional authoring, sourcing, safety, learning, updating & review
│       ├── authoring/               # Adaptive planning, concept reasoning, learner model, consistency, mastery, playbooks, contracts, visuals, gate
│       ├── sourcing/                # Research engine, claim verification, source fidelity & recommendations
│       ├── learning/                # Spaced-retrieval & retention strategy
│       ├── safety/                  # Security education & physical/wet-lab safety policies
│       ├── updating/                # Revision, lifecycle & safe vault linking
│       └── review/                  # Manual verification gate, educational editor & adversarial theory review
└── evaluations/                     # Declarative manual scenarios, triggers, rubrics & benchmark protocol
    ├── evals.json                   # Manual scenarios, some requiring evaluator-supplied inputs
    ├── trigger_eval.json            # Declarative command-triggering queries
    ├── benchmark-protocol.md        # Manual blind comparison & scoring methodology
    └── rubrics/                     # Manual theory, practical & presentation rubrics
```

---

## 5. Manual Evaluation, Limits & Maintenance

- **Honest verification & manual evaluation:** Scriptorium relies solely on direct Markdown authoring and manual checklist review; all scenarios in `evaluations/` are evaluated manually on freshly generated outputs using evaluator-supplied material under [benchmark-protocol.md](evaluations/benchmark-protocol.md). It does not provide automated script validators, code execution, automatic YAML parsing, cryptographic publication receipts, atomic multi-file transactions, or live Obsidian UI rendering checks.
- **Maintenance:** Keep executable scripts and generated note bundles out of the repository entirely, update affected callers and declarative `evaluations/` scenarios when modifying shared rules, and see [migration-notes.md](docs/specs/migration-notes.md) and [LICENSE](LICENSE) for history and licensing.
