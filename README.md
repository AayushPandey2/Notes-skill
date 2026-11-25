# Scriptorium

**Scriptorium** is an instruction-and-reference-only agentic skill for authoring, organizing, and reviewing **Obsidian Markdown learning notes**. It consists purely of declarative Markdown instructions, templates, domain subtemplates, and routing metadata—with zero custom Python/JavaScript runtimes, download scripts, or build dependencies.

---

## 1. Public Commands (`skills/`)

| Command | Entrypoint | What It Does | Writes to Vault? |
|---|---|---|---|
| `/scribe-notes` | [skills/scribe-notes/SKILL.md](skills/scribe-notes/SKILL.md) | Creates or revises 3-file topic bundles (`M1`–`M7` notes, experimental labs, and cheatsheet & interview Q&A files). | Yes (notes, labs, cheatsheet/Q&A, inspected local assets) |
| `/scribe-ytnotes` | [skills/scribe-ytnotes/SKILL.md](skills/scribe-ytnotes/SKILL.md) | Creates one self-contained, transcript-first note per video using downloaded web visuals and clickable timestamps (no lab, no frame capture). | Yes (1 note per video + local web images) |
| `/scribe-doubt` | [skills/scribe-doubt/SKILL.md](skills/scribe-doubt/SKILL.md) | Answers questions strictly from existing vault notes with exact `[[Note Title#Heading]]` citations. | No (read-only) |
| `/scribe-quiz` | [skills/scribe-quiz/SKILL.md](skills/scribe-quiz/SKILL.md) | Runs an interactive, one-question-per-turn recall or viva quiz grounded in existing vault notes. | No by default (optional body review note only if requested) |
| `/scribe-setfolder` | [skills/scribe-setfolder/SKILL.md](skills/scribe-setfolder/SKILL.md) | Sets or inspects the default Obsidian vault and target notes folder. | Config only (`~/.scriptorium-config.json`) |

Root orchestration starts at [SKILL.md](SKILL.md), routes note requests through [router.md](router.md), and resolves destinations via [pre-gen-gate.md](docs/procedures/authoring/pre-gen-gate.md) (precedence: explicit vault path > `SCRIPTORIUM_VAULT_PATH` > `~/.scriptorium-config.json`).

---

## 2. How the Authoring Workflow Operates

1. **Intent & Route Resolution:** [router.md](router.md) and [routing-policy.md](docs/dispatch/routing-policy.md) select the output format (`M1`–`M7`, or `video-notes.md` for `/scribe-ytnotes`) and load only the needed files via [docs/README.md](docs/README.md).
2. **Destination & Safety Gate:** [pre-gen-gate.md](docs/procedures/authoring/pre-gen-gate.md) checks existing vault files before writing, preserves custom YAML/notes, and prevents accidental overwrites.
3. **Research & Source Fidelity:** [research-engine.md](docs/procedures/sourcing/research-engine.md) and [source-fidelity.md](docs/procedures/sourcing/source-fidelity.md) ground claims with locators, respect source-only boundaries, and mark unconfirmed claims `[UNVERIFIED]`.
4. **Self-Contained Layered Teaching:** [teaching_core.md](core/teaching_core.md) enforces genuine zero-prerequisite ordering, separated metadata, clickable Obsidian TOC links, multi-level numbered subject-first headings, purposeful callouts (with visible `[!question]` checkpoints), progressive symbol introduction, early visual worked examples on one consistent dataset, and calm reference prose (with no text or formula highlighting). [math_gates.md](core/math_gates.md) enforces individual metric subsections, multiline `aligned` derivations, consistent `\boxed{...}` emphasis, and visible meaning-first explanations.
5. **Visual Acquisition & Six-Phase Narrative:** [representations.md](docs/procedures/authoring/representations.md) plans **at least 4–5 complementary web visuals** per note (prioritizing the running dataset and geometric/trade-off plots), downloads and inspects local raster assets (`.png`, `.jpg`, `.webp` under `assets/scriptorium/<slug>/`; SVG retired) with controlled display widths (`|650`) and theme-aware `<span class="figure-source">` attributions, teaches every figure in calm takeaway-driven prose, and forbids Mermaid or ASCII graphs/diagrams.
6. **Companion Implementation Labs & Cheatsheet/Interview Packs (3-File Bundle for Non-Video Notes):** [experimental-lab.md](docs/procedures/authoring/experimental-lab.md) and [cheatsheet-interview.md](docs/procedures/authoring/cheatsheet-interview.md) require two siblings per new non-video content note (excluding `/scribe-ytnotes`, MOCs, and playlist indexes): `<note stem> - Experimental Lab.md` (lean, implementation-focused with 4 comparable tracks for ML, domain-appropriate realizations for non-ML, collapsed `> [!example]- Understand this implementation: mathematics, code, and numerical dry run` **A–G** walkthroughs directly beneath every implementation, and honest `Source and static review only; not compiled or executed here.` status) and `<note stem> - Cheatsheet & Interview Q&A.md` (with grouped formula sheets, tap-to-reveal `> [!tip]- Answer` interview Q&A, and `> [!tip]- Solution` worked problems).
7. **Manual Verification:** [verification-checklist.md](docs/procedures/review/verification-checklist.md) performs reader-facing prose, formula-fold, local-embed, YAML, and wikilink checks on the saved Markdown before finishing.

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
- **Implementation Lab Templates (`investigations/`):** [machine-learning.md](docs/blueprints/investigations/machine-learning.md) (lean implementation-focused 4-track ML blueprint), plus domain-tailored realization blueprints for [deep-learning.md](docs/blueprints/investigations/deep-learning.md), [coding.md](docs/blueprints/investigations/coding.md), [mathematics.md](docs/blueprints/investigations/mathematics.md), [physics.md](docs/blueprints/investigations/physics.md), [chemistry.md](docs/blueprints/investigations/chemistry.md), and [general.md](docs/blueprints/investigations/general.md).

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
│   ├── teaching_core.md             # 12 teaching layers, 3-tier prerequisites & voice
│   ├── math_gates.md                # Visual-to-math bridge & collapsed formula folds
│   ├── authoring_rules.md           # YAML profiles, Obsidian Markdown & naming rules
│   └── footer_widgets.md            # Vault navigation footer cues
├── docs/                            # Selectively loaded references
│   ├── README.md                    # Reference loading index
│   ├── design/                      # System overview & template-module catalog
│   ├── dispatch/                    # master-registry.yaml & routing-policy.md
│   ├── properties/                  # properties-policy.md & tag-taxonomy.md
│   ├── specs/                       # migration-notes.md
│   ├── blueprints/                  # Formats, domains, presets, components & labs
│   │   ├── formats/                 # M1–M7 + video-notes.md
│   │   ├── domains/                 # 6 knowledge-type subtemplates
│   │   ├── presets/                 # 12 specialized output presets
│   │   ├── components/              # Conditional teaching moves (module-catalog.md)
│   │   └── investigations/          # 7 domain experimental lab templates
│   └── procedures/                  # Conditional authoring, sourcing, updating & review
│       ├── authoring/               # Adaptive planning, playbooks, 3-file contracts, visuals, gate
│       ├── sourcing/                # Research engine, source fidelity & recommendations
│       ├── updating/                # Revision & safe vault linking
│       └── review/                  # Manual reader-facing verification checklist
└── evaluations/                     # Declarative trigger & quality eval prompts
    ├── evals.json
    └── trigger_eval.json
```

---

## 5. Limits & Maintenance

- **Honest verification:** Scriptorium relies on direct Markdown authoring and manual checklist review; it does not provide automated code execution, cryptographic publication receipts, atomic multi-file transactions, or live Obsidian UI rendering checks.
- **Maintenance:** Keep executable scripts out of the repository, update affected callers and `evaluations/` when modifying shared rules, and see [migration-notes.md](docs/specs/migration-notes.md) and [LICENSE](LICENSE) for history and licensing.
