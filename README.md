# Scriptorium

A modular, token-efficient **Obsidian knowledge-engineering agent skill**. Scriptorium researches topics from primary sources, scaffolds and generates interconnected route-selected Markdown lessons, expands existing coverage incrementally, distills 1-page cheat sheets, ingests external sources, compares concepts side-by-side, runs interactive active-recall quizzes, and answers learner questions strictly read-only from existing vault notes.

---

## Key Capabilities

- **Progressive-Loading Architecture:** [SKILL.md](SKILL.md) acts as a thin router (~2.8 KB) that loads only the matching section of [command_playbooks.md](references/command_playbooks.md) and only the reference files required for the active command.
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

To expose each `/scribe-*` command (`/scribe-notes`, `/scribe-expand`, `/scribe-doubt`, `/scribe-distill`, `/scribe-ingest`, `/scribe-compare`, `/scribe-quiz`, `/scribe-dsa`, `/scribe-practice`) as its own `/` autocomplete entry in Antigravity globally, add `~/.gemini/config/skills.json`:

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

### 1. `/scribe-notes <topic>` — Full Research & Multi-Note Generation
Builds a complete, interconnected subtopic tree (`01-...`, `02-...`, ...) from scratch.
- **When to use:** Learning a new subject deeply from first principles.
- **How it works:**
  1. Loads [pre_gen_gate.md](references/pre_gen_gate.md) and [research_protocol.md](references/research_protocol.md), and runs `vault_index.py --discover` to avoid duplicating existing notes.
  2. Executes **Waves 0–4** research (primary papers/textbooks/RFCs + practitioner traps) and builds an acyclic `depends_on` DAG.
  3. Scaffolds each note via `scripts/scaffold_note.py` and writes the selected template sections, with conditional math and purposeful domain implementations per [note_templates.md](references/note_templates.md).
  4. Verifies DAG acyclicity (`vault_graph.py --check-cycles`), runs scoped mechanical fixes (`verify_vault_notes.py --fix`), and audits semantics against [verification_checklist.md](references/verification_checklist.md).
- **Example:** `/scribe-notes Gradient Descent`

### 2. `/scribe-expand <topic name>` — Index-First Incremental Expansion
Audits existing notes in `<topic name>` and fills missing foundational gaps or adds advanced subtopics without rewriting valid notes.
- **When to use:** A topic folder already exists and needs missing subtopics, deeper follow-ups, or updated `depends_on` / `next_topic` links.
- **How it works:**
  1. Scans metadata via `vault_index.py --fields file,title,aliases,depends_on,next_topic,headings` (without reading full note bodies).
  2. If only metadata/links need updating, patches them in place with `scripts/patch_links.py` (`--dry-run` supported).
  3. If new notes are needed, scaffolds and generates only the missing subtopics, checks cycles with `vault_graph.py`, and validates only modified files.
- **Example:** `/scribe-expand Backpropagation`

### 3. `/scribe-doubt <topic name> <your doubt>` — Read-Only Q&A from Vault
Answers a conceptual or mathematical question **strictly** from your existing notes using `[[Note Title]]` citations.
- **When to use:** You want an answer grounded in your own notes without triggering web research or modifying any files.
- **How it works:**
  1. Never loads `research_protocol.md`, `note_templates.md`, or `verification_checklist.md`.
  2. Locates 1–3 matching notes via `vault_index.py --fields file,title,aliases,headings` and extracts only relevant sections via `--extract ... --sections ...`.
  3. Distinguishes note facts from interpretation and explicitly flags anything missing from the vault.
- **Example:** `/scribe-doubt Gradient Descent why does a step size > 2/L diverge?`

### 4. `/scribe-distill <topic>` — 1-Page Rapid-Revision Cheat Sheet
Compresses an entire topic's existing notes into `<topic-slug>/<topic-slug>-CHEAT-SHEET.md`.
- **When to use:** Exam/interview revision or quick reference after building a topic.
- **How it works:**
  1. Extracts the relevant legacy sections or readable Overview, How it works, Details, Limitations and Connection from each note using `vault_index.py --extract <file> --sections abstract,1,3,7`.
  2. Synthesizes a strict 5-section sheet (`Definition`: 25–30 words, `Theory`: 50–60 words, `Formulas`, `Glossary`, `Traps`) following [cheatsheet_template.md](references/cheatsheet_template.md) with `[[Exact Filename|Title]]` backlinks.
- **Example:** `/scribe-distill Linear Algebra`

### 5. `/scribe-ingest <topic> <pdf|url|notes>` — Non-Destructive Source Ingestion
Extracts claims, definitions, derivations, and equations from a PDF, URL, or raw lecture notes into a new `.md` note inside `<topic>`.
- **When to use:** Turning a paper, documentation page, or raw lecture dump into a structured vault note without overwriting existing completed notes.
- **How it works:**
  1. Checks existing coverage with `vault_index.py --discover --topic "<topic>"` and links already-covered concepts instead of duplicating them.
  2. Extracts source content, scaffolds `<nn>-<ingested-topic-slug>.md`, populates it using existing vault tags/templates, and validates with `verify_vault_notes.py --fix`.
- **Example:** `/scribe-ingest Transformers https://arxiv.org/abs/1706.03762`

### 6. `/scribe-compare <A> vs <B>` — Architectural & Trade-Off Matrix
Synthesizes a structured comparison between two existing vault notes without web re-research.
- **When to use:** Contrasting two algorithms, architectures, or theorems side-by-side.
- **How it works:**
  1. Locates `<A>` and `<B>` via `vault_index.py --fields file,title,aliases,topic,tags_unique` and reads only those two files plus [comparison.md](references/templates/comparison.md) (or the explicitly selected legacy/custom template).
  2. Saves `<vault_path>/comparison/<slug-a>-vs-<slug-b>.md` (`note_type: comparison`), validates it, and echoes the complete Markdown note directly in chat.
- **Example:** `/scribe-compare Adam vs SGD`

### 7. `/scribe-quiz <topic>` — Interactive Active-Recall Quiz
Runs a multi-turn, one-question-at-a-time quiz in chat grounded in 1–2 existing notes and records weak concepts in YAML frontmatter.
- **When to use:** Testing retention, edge-case diagnosis, and derivation transfer on notes you've already studied.
- **How it works:**
  1. Selects 1–2 notes via `vault_index.py --fields file,title,review_log,headings` (prioritizing empty `review_log` or previously logged weak spots).
  2. Asks 3–5 transfer questions **one per turn**, grading each answer (`Correct`, `Partially Correct`, `Incorrect`) against the note's invariants.
  3. At the end, patches only `review_log` in YAML frontmatter using `patch_links.py --append-review-log "YYYY-MM-DD | Score: X/N | Weak: ..."`.
- **Example:** `/scribe-quiz Attention`

---

## Python Helper Scripts (`scripts/`)

| Script | Purpose | Key Flags |
|---|---|---|
| [vault_index.py](scripts/vault_index.py) | Cached, read-only metadata, tag, template & section extractor | `--topic`, `--discover`, `--full-registry`, `--fields`, `--extract <file> --sections ...`, `--no-cache` |
| [scaffold_note.py](scripts/scaffold_note.py) | Deterministic route-selected deep-note skeleton generator | `--output`, `--number`, `--title`, `--topic`, `--depends-on`, `--next-topic`, `--tags`, `--dry-run`, `--overwrite` |
| [patch_links.py](scripts/patch_links.py) | Non-destructive YAML frontmatter & wikilink patcher | `--file`, `--add-depends-on`, `--remove-depends-on`, `--set-next-topic`, `--append-review-log`, `--rename-link OLD NEW`, `--dry-run` |
| [vault_graph.py](scripts/vault_graph.py) | Read-only dependency DAG, cycle, broken-link & Mermaid analyzer | `--topic`, `--format json\|mermaid\|text`, `--include-body-links`, `--check-cycles`, `--strict` |
| [verify_vault_notes.py](scripts/verify_vault_notes.py) | Scoped schema-aware validator and mechanical auto-repair tool | `--files`, `--manifest`, `--fix`, `--allow-cross-vault-writes` |

### Common CLI Examples
```bash
# 1. Discover templates, tags, and placement conventions for a topic
python3 scripts/vault_index.py "<vault_path>" --discover --topic "Machine Learning"

# 2. Extract only > [!abstract] and Sections 1, 3, 7 from a note
python3 scripts/vault_index.py "<vault_path>" --extract "ml/01-gd.md" --sections abstract,1,3,7

# 3. Scaffold a new route-selected note skeleton
python3 scripts/scaffold_note.py "<vault_path>" \
  --output "ml/02-sgd.md" --number "02" --title "Stochastic Gradient Descent" \
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

---

## Repository Structure

```text
scriptorium/
├── SKILL.md                              # Thin progressive-loading command router
├── README.md                             # Project overview, setup guide & CLI docs
├── LICENSE                               # MIT License
├── .gitignore
├── references/
│   ├── command_playbooks.md              # Per-command workflows (loaded by section)
│   ├── pre_gen_gate.md                   # 7-step pre-generation resolution gate
│   ├── research_protocol.md              # Phase 1 deterministic research SOP (Waves 0–4)
│   ├── note_templates.md                 # Authoritative route-selected note authoring rules
│   ├── cheatsheet_template.md            # 5-section 1-page cheat sheet template
│   ├── comparison_template.md            # Architectural & trade-off comparison template
│   └── verification_checklist.md         # Semantic-only quality rubric
├── scripts/
│   ├── vault_index.py                    # Cached metadata indexer (--discover, --fields, --extract)
│   ├── scaffold_note.py                  # Deterministic route-selected note skeleton generator
│   ├── patch_links.py                    # Non-destructive frontmatter & wikilink patcher (--dry-run)
│   ├── vault_graph.py                    # Read-only DAG cycle, broken-link, orphan & Mermaid analyzer
│   └── verify_vault_notes.py             # Scoped validator with --fix mechanical repairs
└── tests/
    ├── test_vault_aware.py               # Indexer, template discovery, tag & scoped validation tests
    ├── test_patch_and_graph.py           # Frontmatter/link patching & graph topology tests
    └── test_token_optimizations.py       # Scaffolding, --fields & --extract section tests
```

## License

Released under the [MIT License](LICENSE).


## Integrated routing defaults

All existing commands and optimized Python helpers remain supported. New notes use
one of ten contracts registered in `references/routes.json`: deepstudy-coding,
deepstudy-general, api-table, cheat-sheet, atomic, comparison, summary, practice,
dsa, paper-breakdown. The two deep routes use eleven readable headings. Explicit
custom vault templates and existing legacy notes retain their schemas. The old
seven-section scaffolder is available with `--template legacy-deep`.

Examples supported by the prompt dispatcher (host-native slash registration varies):

```text
/scribe-notes How convolution filters work
/scribe-distill CNN
/scribe-compare SQL views vs materialized views
/scribe-dsa cpp Given a nonempty integer array, return its maximum value.
/scribe-dsa python Given a nonempty integer array, return its maximum value.
/scribe-practice CNN
```

Cheap route planning, followed by the existing scaffold/author/validate workflow:

```bash
python scripts/route_request.py "/scribe-dsa cpp Find the maximum in a nonempty array"
python scripts/route_request.py "Convolution" --purpose implementation --domain ml --math-level 2
python scripts/scaffold_note.py --topic CNN --title Convolution --template deepstudy-coding --math-level 2 --dry-run
```

Routing fixes the note's purpose; math level (0/1/2) and language are separate.
`route_request.py` helps with command/source/purpose decisions; the agent resolves
vault/custom-template precedence and broad topic outlines before calling it per note.
Scaffolds are unfinished drafts; populate them from inspected evidence before
validation. Saved practice tracks the new-folder obligation in the operational
manifest; `/scribe-quiz` remains an interactive one-question-per-turn workflow.
No service, database, runtime research engine or automatic plugin execution is added.

Development checks: `python -m pip install -r requirements.txt pytest`, then
`python -m pytest -q`. Static checks do not establish Obsidian rendering, factual
accuracy or measured speedups; inspect those separately when the host supports them.
