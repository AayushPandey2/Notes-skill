# Scriptorium

Scriptorium routes every learning request across **Seven Canonical Master Output Templates (`M1–M7`)** under [references/templates/masters/](references/templates/masters/README.md) using the [Intelligent Routing Engine](scripts/scribe.py) ([routing-policy.md](references/routing/routing-policy.md), [master-registry.yaml](references/routing/master-registry.yaml)). Deep learning notes (`M1`) use [deep-notes.md](references/templates/masters/deep-notes.md) with the authoritative [adaptive instructional engine](references/workflows/notes-creation/adaptive-engine.md), [instructional registry](references/workflows/notes-creation/instructional-registry.json), [ARRIE research engine](references/workflows/research/research-engine.md), and [pedagogical intelligence layer](references/workflows/notes-creation/pedagogical-intelligence.md).

A modular Obsidian study-note skill. Scriptorium routes requests to purpose-selected master output products, researches primary sources, expands existing coverage, solves worked problems, builds verified implementations, and creates assessments and revision packs.

---

## Key Capabilities

- [SKILL.md](SKILL.md) opens the [two-pass router](router.md). Each planned note gets one lazily loaded template, an independent math level, and a verification stack.
- **Deterministic Python Tooling:** Offloads indexing, note scaffolding, frontmatter/wikilink patching, graph/DAG analysis, and formatting repairs to Python scripts in `scripts/`, saving context tokens and preventing accidental rewrites.
- **Vault-Aware & Template-Respecting:** Detects existing `.obsidian/templates.json` and Templater folder mappings, reuses existing vault tags and naming conventions, and validates only newly created or edited files (`--files` / `--manifest`) so unrelated notes stay byte-for-byte untouched.
- **Read-Only & Containment Safety:** Rejects `..` path traversal and symlinks escaping the vault root, never executes Templater or Dataview JavaScript, and caches the vault index outside the vault (`~/.cache/scriptorium/`).

---

## Setup Guide

### 1. Prerequisites
- **Python 3.10+**
- **PyYAML** (`pip install pyyaml`) — required by `vault_index.py`, `patch_links.py`, and `verify_vault_notes.py`
- **pytest** (`pip install pytest`) — optional, for running the test suite

### 2. Clone the Repository
```bash
git clone https://github.com/AayushPandey2/scriptorium.git
cd scriptorium
```
If installing as an agent skill, place or symlink the `scriptorium/` folder inside your agent's skills directory (for example, `~/.gemini/config/skills/scriptorium` or your workspace skill path).

To expose the 4 active public `/scribe-*` commands (`/scribe-notes`, `/scribe-doubt`, `/scribe-quiz`, `/scribe-setfolder`) as `/` autocomplete entries in Antigravity globally, add `~/.gemini/config/skills.json`:

```json
{
  "entries": [
    {
      "path": "~/.gemini/config/skills/scriptorium/skills"
    }
  ]
}
```

### 3. Configure Your Obsidian Vault Path
Scriptorium resolves `[PATH_TO_OBSIDIAN_VAULT]` in this order:
1. Explicit CLI argument passed to a script (`"<vault_path>"`)
2. `SCRIPTORIUM_VAULT_PATH` environment variable
3. `~/.scriptorium-config.json`

Create `~/.scriptorium-config.json`:

**Windows (PowerShell):**
```powershell
@'
{
  "vault_path": "C:\\Users\\YourName\\Documents\\ObsidianVault"
}
'@ | Set-Content "$HOME\.scriptorium-config.json" -Encoding UTF8
```

**macOS / Linux:**
```bash
cat << 'EOF' > ~/.scriptorium-config.json
{
  "vault_path": "/path/to/YourObsidianVault"
}
EOF
```

### 4. Verify Your Setup
Run the test suite and test the vault indexer against your vault:
```bash
pytest -v
python3 scripts/vault_index.py "<vault_path>" --fields file,title,topic
```

---

## Commands Reference

Scriptorium exposes **4 public slash commands** — one universal note-creation command (`/scribe-notes`) plus 3 non-note utilities (`/scribe-doubt`, `/scribe-quiz`, `/scribe-setfolder`):

### 1. `/scribe-notes <topic, source, or request>` — Universal Adaptive Note Creation
The **sole public note-creation command**. Automatically detects the best output master (`M1`–`M7`), variant, scope tier (`S0`–`S5`), and organization (`single_note` vs. `hierarchical_collection`), asks only unanswered interactive configuration questions, previews substantial collections, and generates verified Obsidian notes with mandatory Obsidian Properties and `EIS-01..EIS-07` explanatory clarity.
- **Supports all 7 internal masters automatically:**
  - **M1 (`deep-notes`):** `/scribe-notes Gradient Descent` or `/scribe-notes Machine Learning` (hierarchical collection)
  - **M2 (`study-notes` / `lecture_order`):** `/scribe-notes Study notes from this lecture PDF preserving lecture order`
  - **M3 (`quick-reference` / `formula_sheet` / `atomic_card`):** `/scribe-notes Make a cheat sheet for Pandas Data Cleaning`
  - **M4 (`worked-solutions`):** `/scribe-notes Solve these 5 calculus integration problems step by step`
  - **M5 (`implementation-guide`):** `/scribe-notes Implement binary search from scratch in Python`
  - **M6 (`assessment` / `flashcards`):** `/scribe-notes Create flashcards for cellular respiration`
  - **M7 (`synthesis-revision` / `comparison_guide` / `concept_map` / `paper_breakdown`):** `/scribe-notes Compare CNN vs ViT`
- **Interactive workflow:** Always starts with inferred recommendations + concise adaptive configuration questions (`scripts/scribe.py notes start`), accepts natural follow-up replies without repeating `/scribe-notes` (`scripts/scribe.py notes respond`), previews broad hierarchical collections, generates notes + collection manifest (`scripts/scribe.py notes generate --validate`), and reconciles existing files non-destructively.
- **Retired legacy commands unified into `/scribe-notes`:** `/scribe-deepnotes`, `/scribe-distill`, `/scribe-atomic-notes`, `/scribe-compare`, `/scribe-dsa`, `/scribe-practice`, `/scribe-ingest`, and `/scribe-expand`.

### 2. `/scribe-doubt <topic name> <your doubt>` — Read-Only Q&A from Vault
Answers a conceptual or mathematical question **strictly** from your existing notes using `[[Note Title]]` citations without triggering web research or modifying any files.
- **Example:** `/scribe-doubt Gradient Descent why does a step size > 2/L diverge?`

### 3. `/scribe-quiz <topic>` — Interactive Active-Recall Quiz
Runs a multi-turn, one-question-at-a-time quiz in chat grounded in 1–2 existing notes and records weak concepts in `review_log`.
- **Example:** `/scribe-quiz Attention`

### 4. `/scribe-setfolder <folder path>` — Configure Default Notes Folder
Sets the target Obsidian notes subfolder inside `~/.scriptorium-config.json`.
- **Example:** `/scribe-setfolder StudyNotes/AI`

### Output Directory Hierarchy

Hierarchical collections organize Parent Maps of Content (`note_type: index`) and child notes cleanly by topic hierarchy, while standalone practice sets, atomic notes, and cheatsheets can target sibling folders when requested:

```text
<Vault Root>/
├── Machine Learning/
│   ├── Machine Learning.md                  # Root Parent MOC (note_type: index)
│   ├── Foundations/
│   │   ├── Foundations.md                   # Group MOC (note_type: index)
│   │   └── ...                              # Adaptive child notes
│   ├── Supervised Learning/
│   │   ├── Supervised Learning.md           # Group MOC (note_type: index)
│   │   ├── Linear Regression.md
│   │   └── Logistic Regression.md
│   └── ...
└── .scriptorium/
    ├── sessions/                            # Pending interactive configuration sessions
    └── collections/                         # Collection manifests & completion status
```

### Prompt and source routing

When slash commands are unavailable, use the same command without the slash or ask in natural language. Examples include “Create an atomic note about a residual connection,” “Use the api-table template for Conv2d,” and “Summarize this paper https://arxiv.org/abs/1512.03385.” A standalone research link routes to paper-breakdown. A standalone article, docs, or video URL routes to summary. A source referenced in a broader study request supplies evidence to the relevant subtopics.

---

## Python Engines (`scriptorium/`) & Public CLI Entry Points (`scripts/`)

Core runtime logic is consolidated into six cohesive engines under `scriptorium/engines/` (`orchestration.py`, `research.py`, `knowledge.py`, `pedagogy.py`, `quality.py`, `vault.py`) plus shared `scriptorium/models.py` and `scriptorium/layout.py`, exposed through 8 thin CLI entry points in `scripts/`:

| Script | Purpose | Key Flags / Subcommands |
|---|---|---|
| [scribe.py](scripts/scribe.py) | Unified CLI across all six engines (universal `/scribe-notes` interactive sessions, KCP checkpoints & refinement, selective prompt compilation & token benchmarks, routing, Properties, EIS explanation blueprints/clarity review, incremental updates, ARRIE research, pedagogy, golden evaluations, repository/authority audit) | `notes`, `optimize`, `route`, `properties`, `explain`, `update`, `migrate`, `validate`, `research`, `pedagogy`, `evaluate`, `audit`, `validate-registry` |
| [vault_index.py](scripts/vault_index.py) | Cached, read-only metadata, tag, template & section extractor | `--topic`, `--discover`, `--full-registry`, `--fields`, `--extract <file> --sections ...`, `--no-cache` |
| [plan_notes.py](scripts/plan_notes.py) | Resolve requests and manage resumable plans | `inspect`, `start`, `status`, `publish` (`--coverage`, `--evidence`) |
| [scaffold_note.py](scripts/scaffold_note.py) | Routed M1–M7 and syllabus skeletons with mandatory Obsidian Properties | `--template`, `--math-level`, `--output`, `--id`, `--title`, `--topic`, `--depends-on`, `--narrow-practice` |
| [validate_note.py](scripts/validate_note.py) | Check routed notes, Obsidian Properties, and resolve vault links | `<note.md>`, `--vault` |
| [patch_links.py](scripts/patch_links.py) | Non-destructive YAML frontmatter & wikilink patcher | `--file`, `--add-depends-on`, `--remove-depends-on`, `--set-next-topic`, `--append-review-log`, `--rename-link OLD NEW`, `--dry-run` |
| [vault_graph.py](scripts/vault_graph.py) | Read-only dependency DAG, cycle, broken-link & Mermaid analyzer | `--topic`, `--format json\|mermaid\|text`, `--include-body-links`, `--check-cycles`, `--strict` |
| [verify_vault_notes.py](scripts/verify_vault_notes.py) | Scoped schema-aware validator and mechanical auto-repair tool | `--files`, `--manifest`, `--fix` |

### Common CLI Examples
```bash
# 1. Discover templates, tags, and placement conventions for a topic
python3 scripts/vault_index.py "<vault_path>" --discover --topic "Machine Learning"

# 2. Extract only > [!abstract] and Sections 1, 3, 7 from a note
python3 scripts/vault_index.py "<vault_path>" --extract "ml/01-gd.md" --sections abstract,1,3,7

# 3. Preview a routed scaffold to populate as a draft
python3 scripts/scaffold_note.py "<vault_path>" \
  --template deepstudy-master --math-level 2 --number "02" --title "Stochastic Gradient Descent" \
  --base-domain "Computer Science" --master-topic "Machine Learning" --topic "Optimization" \
  --depends-on "[[01-gd|Gradient Descent]]"

# 4. Preview a frontmatter link/review_log patch without writing to disk
python3 scripts/patch_links.py "<vault_path>" --file "ml/02-sgd.md" \
  --append-review-log "2026-11-18 | Score: 4/5 | Weak: variance bound" --dry-run

# 5. Safely rename a wikilink across the vault (skips code blocks & HTML comments)
python3 scripts/patch_links.py "<vault_path>" --rename-link "Old Note" "New Note" --dry-run

# 6. Check for dependency cycles and render a Mermaid graph
python3 scripts/vault_graph.py "<vault_path>" --topic "Optimization" --check-cycles
python3 scripts/vault_graph.py "<vault_path>" --topic "Optimization" --format mermaid

# 7. Validate & auto-fix only specific generated/edited files
python3 scripts/verify_vault_notes.py "<vault_path>" --files "ml/02-sgd.md" --fix
```

For a full write, follow the [plan and publish workflow](router.md#plan-and-publish). Plans live under `.scriptorium/plans/` in the vault. Reuse the request and topic folder to resume. Exclusive publication uses same-directory hard links, supported by NTFS and common Linux/macOS filesystems. Obsidian requires Dataview JavaScript queries enabled for **Mark Revisited**.

---

## Repository Structure

```text
scriptorium/
├── SKILL.md                                           # Dispatcher
├── router.md                                          # Multi-master routing & workflow
├── shared/                                            # Authoring rules, math gates and footer
├── skills/                                            # Optional /scribe-* command wrappers
├── README.md                                          # Project overview, setup guide & CLI docs
├── LICENSE                                            # MIT License
├── .gitignore
├── references/
│   ├── README.md                                      # Reference index (progressive loading)
│   ├── architecture/
│   │   ├── system-overview.md                         # End-to-end architecture, KCP (F02-F15) & 6-engine map
│   │   └── template-module-catalog.md                 # Full Master/Variant/Subtemplate/Module catalog & matrix
│   ├── routing/
│   │   ├── master-registry.yaml                       # Authoritative M1–M7, variants, subtemplates, commands
│   │   └── routing-policy.md                          # Deterministic-first + semantic routing rules
│   ├── workflows/
│   │   ├── research/                                  # ARRIE engine, policy registry, source-fidelity, resources
│   │   ├── notes-creation/                            # Adaptive engine, instructional registry, P01–P11, playbooks
│   │   ├── revision/                                  # Multi-layer revision & vault linking
│   │   └── validation/                                # Semantic verification checklist
│   ├── templates/
│   │   ├── masters/                                   # Seven Canonical Master Output Templates (M1–M7)
│   │   ├── variants/                                  # 12 specialized variants mapped cleanly to M2/M3/M6/M7
│   │   ├── subtemplates/                              # 6 domain-independent knowledge-type subtemplates
│   │   └── modules/                                   # Reusable adaptive module catalog
│   ├── metadata/                                      # Obsidian Properties policy, tag taxonomy, note naming
│   └── contracts/                                     # Routing schema & migration notes
├── scriptorium/
│   ├── __init__.py                                    # Public facade exports
│   ├── models.py                                      # Shared YAML/ParsedNote cache, errors, Properties schema
│   ├── layout.py                                      # Shared per-route structural contract
│   └── engines/
│       ├── orchestration.py                           # E1: M1–M7 routing, intent normalization, constraints, authority, tracing
│       ├── research.py                                # E2: ARRIE research, verification, curation, freshness cache
│       ├── knowledge.py                               # E3: Concept identity, coverage, claims, uncertainty, multi-artifact, diffs
│       ├── pedagogy.py                                # E4: Contract v3, P01–P11, gaps, density, examples, compression
│       ├── quality.py                                 # E5: Representation checks, targeted repair, golden harness, repo audit
│       └── vault.py                                   # E6: Obsidian Properties, tag taxonomy, incremental updates, safe writes
├── scripts/
│   ├── scribe.py                                      # Unified thin CLI across all six engines
│   ├── plan_notes.py                                  # Request locks, plans and safe publication
│   ├── scaffold_note.py                               # Deterministic note skeleton generator with Properties
│   ├── validate_note.py                               # Routed-note & Properties linter
│   ├── vault_index.py                                 # Cached metadata indexer (--discover, --fields, --extract)
│   ├── vault_graph.py                                 # Read-only DAG cycle, broken-link, orphan & Mermaid analyzer
│   ├── patch_links.py                                 # Non-destructive frontmatter & wikilink patcher (--dry-run)
│   └── verify_vault_notes.py                          # Scoped validator with --fix mechanical repairs
└── tests/
    ├── test_unified_engines_and_properties.py         # Consolidation, Properties (A–J), 20 mechanisms (1–20)
    ├── test_routing_and_masters.py                    # M1–M7 masters, routing edge cases, differentiation & registry
    ├── test_research_engine.py                        # ARRIE modes, discovery, verification, curation & citations
    ├── test_pedagogical_engine.py                     # P01–P11 cognitive, representation, visual, load & revision tests
    ├── test_instructional_engine.py                   # Contract v3 planner, composer & coverage tests
    ├── test_vault_aware.py                            # Indexer, template discovery, tag & scoped validation tests
    ├── test_patch_and_graph.py                        # Frontmatter/link patching & graph topology tests
    ├── test_routed_workflow.py                        # Routing, layouts, validation and retries
    └── test_token_optimizations.py                    # Scaffolding, --fields & --extract section tests
```

## License

Released under the [MIT License](LICENSE).

Repository maintenance: run `python scripts/scribe.py audit` ([scribe.py](scripts/scribe.py)) for local links, anchors, documented CLI flags, instruction authority, and Python syntax.

Deep learning notes (`M1`) use the [per-concept instructional engine](references/workflows/notes-creation/adaptive-engine.md), the [ARRIE adaptive research engine](references/workflows/research/research-engine.md), and [deep-notes.md](references/templates/masters/deep-notes.md). Supply `instructional_plan` (and optional `research_plan` / `evidence_registry`) in an outline to specify learner, objectives, prerequisites, source policy, concept-specific research depth (`R0–R5`), and independent instructional depth profiles (`0–5`). Source-grounded deep publication accepts `--coverage` and `--evidence` receipts; see [source fidelity](references/workflows/research/source-fidelity.md) and [resource recommendations](references/workflows/research/resource-recommendations.md). The [migration audit](references/contracts/migration-notes.md) records intentional behavior changes, and [evaluation examples](examples/adaptive-deepnotes/README.md) show the tested scenarios and measurement limits.
