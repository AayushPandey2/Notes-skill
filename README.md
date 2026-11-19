# Scriptorium

Deep-study notes use [deepstudy-master.md](templates/deepstudy-master.md) with the authoritative [notes_decision_matrix.md](templates/notes_decision_matrix.md). Complete the decision record, then keep only the modules justified by its 20 matrices. The coding/general filenames and selectors are compatibility aliases. Deep-study scaffolding and validation accept optional sections, math depths 0–3, and purpose-selected code without the older fixed table/footer requirements.

A modular Obsidian study-note skill. Scriptorium routes individual subtopics to purpose-selected note formats, researches primary sources, expands existing coverage, and creates practice sets and quizzes.

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

To expose each `/scribe-*` command (`/scribe-deepnotes`, `/scribe-notes`, `/scribe-atomic-notes`, `/scribe-expand`, `/scribe-doubt`, `/scribe-distill`, `/scribe-ingest`, `/scribe-compare`, `/scribe-quiz`, `/scribe-dsa`, `/scribe-practice`, `/scribe-setfolder`) as its own `/` autocomplete entry in Antigravity globally, add `~/.gemini/config/skills.json`:

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

### 1. `/scribe-deepnotes <topic>` — Full Research & Multi-Note Generation
Builds a complete, interconnected subtopic tree (`01-...`, `02-...`, ...) from scratch.
- **When to use:** Learning a new subject deeply from first principles.
- **How it works:**
  1. Loads [pre_gen_gate.md](references/pre_gen_gate.md) and [research_protocol.md](references/research_protocol.md), and runs `vault_index.py --discover` to avoid duplicating existing notes.
  2. Plans each subtopic and its dependencies before source retrieval, then writes the syllabus MOC.
  3. Reuses evidence across siblings, scaffolds each selected template, executes the mandatory **Humanization & Cohesion Pass**, and validates each draft before publication. A new topic gets a practice test in the centralized `Practice Sets/` folder.
  4. Verifies DAG acyclicity (`vault_graph.py --check-cycles`), runs scoped mechanical fixes (`verify_vault_notes.py --fix`), and audits semantics against [verification_checklist.md](references/verification_checklist.md).
- **Example:** `/scribe-deepnotes Gradient Descent`

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
  1. Never loads `research_protocol.md`, `templates/*.md`, or `verification_checklist.md`.
  2. Locates 1–3 matching notes via `vault_index.py --fields file,title,aliases,headings` and extracts only relevant sections via `--extract ... --sections ...`.
  3. Distinguishes note facts from interpretation and explicitly flags anything missing from the vault.
- **Example:** `/scribe-doubt Gradient Descent why does a step size > 2/L diverge?`

### 4. `/scribe-distill <topic>` — 1-Page Rapid-Revision Cheat Sheet
Compresses an entire topic's existing notes into the centralized `Cheatsheets/` folder (`Cheatsheets/<topic-slug>-CHEAT-SHEET.md`, or `Cheatsheets/<topic-slug>-<subtopic-slug>-CHEAT-SHEET.md` for subtopic-scoped cheatsheets) located at the same directory level as `<subtopic>/` folders.
- **When to use:** Exam/interview revision or quick reference after building a topic.
- **How it works:**
  1. Extracts the abstract, synthesis, mechanism, and final traps from existing notes.
  2. Builds a [cheat sheet](templates/cheat-sheet.md) with a 350-word body cap, links back to its source notes, and saves it in `Cheatsheets/` with clear topic/subtopic naming to avoid collisions.
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
  1. Locates `<A>` and `<B>` via `vault_index.py --fields file,title,aliases,topic,tags_unique` and reads those two notes and the [comparison spec](templates/comparison.md).
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

### 8. `/scribe-dsa <language> <problem>`

Locks the selected language for a DSA study note with brute-force and optimized solutions, a dry run, and edge tests. Examples include `/scribe-dsa cpp Two Sum` and `scribe-dsa python https://leetcode.com/problems/two-sum/`. A prompt such as “Solve Two Sum in C++” also works.

### 9. `/scribe-practice <topic-or-note>` — Centralized Active-Recall Practice Set

Creates a three-tier practice set inside the centralized `Practice Sets/` folder located at the same directory level (sibling level) as the `<subtopic>/` folders. For example, use `/scribe-practice CNN` or “Create a practice set for my CNN notes” (saved as `Practice Sets/CNN - Practice.md`). An automatic topic-wide set is saved as `Practice Sets/<Topic> - Practice Test.md`.

### 10. `/scribe-atomic-notes <topic name>` — Fast Lightweight Atomic Note

Generates a compact, transcludable `<150`-word atomic note without triggering a slow, multi-stage deep research pipeline.
- **When to use:** Quickly capturing an indivisible concept, governing formula/invariant, micro-example, and vault connections.
- **How it works:**
  1. Bypasses multi-wave (`Waves 1–4`) deep research workflows.
  2. Performs a single, direct web search/fetch for `<topic name>` to gather core facts quickly.
  3. Populates [templates/atomic.md](templates/atomic.md) while applying the mandatory **Humanization & Cohesion Pass** (conversational yet rigorous student/engineer-to-future-self tone, logical narrative transitions, zero AI clichés, and synthesized mental models rather than copy-pasted definitions).
  4. Saves the generated file inside the centralized shared `Atomic Notes/` folder (`Atomic Notes/<topic_name>.md`) at the same directory level (sibling level) as the `<subtopic>/` folders.
- **Example:** `/scribe-atomic-notes Residual Connection`

### 11. `/scribe-notes <topic name>` — Fast Multi-Subtopic Source-Faithful Study Notes

Replicates `/scribe-deepnotes`'s multi-subtopic decomposition, `00-MOC-<topic-slug>.md`, and multi-file output structure while **bypassing deep research** and defaulting strictly to [templates/studynotes.md](templates/studynotes.md).
- **When to use:** Fast, source-faithful multi-subtopic study notes without multi-stage primary-source deep research or heavy math.
- **How it works:**
  1. Explicitly disables and bypasses `references/research_protocol.md` (`Waves 1–4`), using fast, direct web searches/fetches only.
  2. Decomposes `<topic name>` into logical subtopics inside `<topic-folder>/` (`00-MOC-<topic-slug>.md` + numbered notes), routing auxiliary practice sets, cheatsheets, and atomic notes to their shared sibling folders (`Practice Sets/`, `Cheatsheets/`, `Atomic Notes/`).
  3. Defaults all core notes strictly to [templates/studynotes.md](templates/studynotes.md); permits auxiliary templates (`practice`, `cheat-sheet`, `comparison`, `atomic`, `api-table`), while **strictly banning `deepstudy-master`**.
  4. Minimizes mathematical notation (`math_level: 0` by default—plain language, intuitive analogies, structured text), allowing LaTeX/equations only when strictly essential to a Mathematics, Physics, or quantitative engineering topic.
  5. Applies the mandatory **Humanization & Cohesion Pass** for conversational, intuitive flow.
- **Example:** `/scribe-notes Operating Systems Scheduling`

### Output Directory Hierarchy

All practice sets, atomic notes, and cheatsheets are centralized at the sibling level alongside the `<subtopic>/` folders:

```text
<Topic / Root Workspace>/
├── <subtopic_1>/
│   └── (subtopic notes...)
├── <subtopic_2>/
│   └── (subtopic notes...)
├── Practice Sets/
│   └── (all practice sets for all topics/subtopics saved here, clearly named by topic/subtopic)
├── Atomic Notes/
│   └── (all atomic notes saved here, e.g., <topic_name>.md)
└── Cheatsheets/
    └── (all cheatsheets for all topics/subtopics saved here, clearly named by topic/subtopic)
```

### Prompt and source routing

When slash commands are unavailable, use the same command without the slash or ask in natural language. Examples include “Create an atomic note about a residual connection,” “Use the api-table template for Conv2d,” and “Summarize this paper https://arxiv.org/abs/1512.03385.” A standalone research link routes to paper-breakdown. A standalone article, docs, or video URL routes to summary. A source referenced in a broader study request supplies evidence to the relevant subtopics.

---

## Python Helper Scripts (`scripts/`)

| Script | Purpose | Key Flags |
|---|---|---|
| [vault_index.py](scripts/vault_index.py) | Cached, read-only metadata, tag, template & section extractor | `--topic`, `--discover`, `--full-registry`, `--fields`, `--extract <file> --sections ...`, `--no-cache` |
| [plan_notes.py](scripts/plan_notes.py) | Resolve requests and manage resumable plans | `inspect`, `start`, `status`, `publish` |
| [scaffold_note.py](scripts/scaffold_note.py) | Routed, legacy, and syllabus skeletons | `--template`, `--math-level`, `--output`, `--id`, `--title`, `--topic`, `--depends-on`, `--narrow-practice` |
| [validate_note.py](scripts/validate_note.py) | Check routed notes and resolve links when a vault is provided | `<note.md>`, `--vault` |
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
├── SKILL.md                              # Dispatcher
├── router.md                             # Per-note planning and workflow
├── shared/                               # Authoring rules, math gates and footer
├── templates/                            # Eleven individually loaded route specs
├── skills/                               # Optional command wrappers
├── README.md                             # Project overview, setup guide & CLI docs
├── LICENSE                               # MIT License
├── .gitignore
├── references/
│   ├── command_playbooks.md              # Per-command workflows (loaded by section)
│   ├── pre_gen_gate.md                   # 7-step pre-generation resolution gate
│   ├── research_protocol.md              # Phase 1 deterministic research SOP (Waves 0–4)
│   ├── syllabus_template.md              # Curriculum scope and learning graph
│   └── verification_checklist.md         # Semantic-only quality rubric
├── scripts/
│   ├── vault_index.py                    # Cached metadata indexer (--discover, --fields, --extract)
│   ├── plan_notes.py                     # Request locks, plans and safe publication
│   ├── note_layout.py                    # Shared per-route structural contract
│   ├── scaffold_note.py                  # Deterministic note skeleton generator
│   ├── validate_note.py                   # Routed-note linter
│   ├── patch_links.py                    # Non-destructive frontmatter & wikilink patcher (--dry-run)
│   ├── vault_graph.py                    # Read-only DAG cycle, broken-link, orphan & Mermaid analyzer
│   └── verify_vault_notes.py             # Scoped validator with --fix mechanical repairs
└── tests/
    ├── test_vault_aware.py               # Indexer, template discovery, tag & scoped validation tests
    ├── test_patch_and_graph.py           # Frontmatter/link patching & graph topology tests
    ├── test_routed_workflow.py           # Routing, layouts, validation and retries
    └── test_token_optimizations.py       # Scaffolding, --fields & --extract section tests
```

## License

Released under the [MIT License](LICENSE).

Repository maintenance: run [audit_repository.py](scripts/audit_repository.py) for local links, anchors, documented CLI flags and Python syntax; see [the staged audit](references/repository_audit.md) for inventory and results.
