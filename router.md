# Scriptorium routing

## Pass 1 — Resolve command, selector, and source

Start here with the raw request and read only this file during routing. Use `python3 scripts/plan_notes.py inspect "<request>"` for deterministic command/source parsing. Classify paraphrases by intent before requesting evidence. Accept slash commands on hosts that register the wrappers and the same request as plain text (for example, `scribe-dsa cpp Two Sum` or “Create a practice set for my CNN notes”). An explicit named vault template still follows the custom-template gate.

- DSA: `/scribe-dsa <language> <problem or URL>` locks DSA and the language. A URL anywhere in its problem is evidence. Return usage on missing language/problem or an unsupported language.
- Practice: `/scribe-practice <topic-or-note>` locks practice (`templates/practice.md`). Resolve one existing topic folder and the requested sibling note(s) through vault discovery. Save `Practice Sets/<Target> - Practice.md` inside the centralized `Practice Sets/` folder located at the same directory level (sibling level) as the `<subtopic>/` folders. Never append a second practice item.
- Atomic Notes: `/scribe-atomic-notes <topic name>` locks atomic (`templates/atomic.md`). Bypass deep/multi-hop research workflows: perform a single, direct web search/fetch for `<topic name>` to gather core facts quickly, apply the mandatory Humanization & Cohesion Pass, and save inside the centralized `Atomic Notes/` folder (`Atomic Notes/<topic_name>.md`) located at the same directory level (sibling level) as the `<subtopic>/` folders.
- Class Notes: `/scribe-classnotes <topic name>` replicates `/scribe-notes`'s multi-subtopic folder and multi-file DAG structure (`00-MOC-<topic-slug>.md` + numbered subtopic files, routing auxiliary practice sets/cheatsheets/atomic notes to sibling `Practice Sets/`, `Cheatsheets/`, and `Atomic Notes/`), but **bypasses deep multi-wave research** in favor of fast, direct web searches/fetches. Core subtopics default strictly to `templates/classnotes.md`; supplementary/auxiliary templates (`practice`, `cheat-sheet`, `comparison`, `atomic`, `api-table`) are allowed when appropriate, while **`deepstudy-coding` and `deepstudy-general` (`deepnotes-coding` / `deepnotes-general`) are strictly prohibited under all circumstances**. Default to `math_level: 0` (plain language, intuitive analogies, structured text); only include formal math/LaTeX when strictly essential to an inherently mathematical, physical, or quantitative engineering topic.
- Compare and distill lock comparison and cheat-sheet. Distill (`/scribe-distill <topic>`) and `cheat-sheet` notes save inside the centralized `Cheatsheets/` folder located at the same directory level (sibling level) as the `<subtopic>/` folders, using clear topic/subtopic identifiers (`Cheatsheets/<topic-slug>-CHEAT-SHEET.md` or `Cheatsheets/<topic-slug>-<subtopic-slug>-CHEAT-SHEET.md`) so notes from different topics never collide. Ingest with a topic and a source retains deduplication and local placement. Notes and expand retain their syllabus/coverage contracts. Doubt and quiz dispatch immediately with no authoring or external research.
- An explicit template selector or natural-language format request locks the route beneath command locks. “Summarize this paper” therefore selects summary. A bare paper URL selects paper-breakdown (arXiv, DOI, OpenReview, ACL Anthology, conference proceedings and IEEE). A bare article, docs or video URL selects summary. A reference inside a broader study request supplies evidence without locking the routes.

For writing requests, read the applicable [command playbook](references/command_playbooks.md) section after routing (B expand, C notes, D distill, E ingest, F compare, H atomic-notes, I classnotes). For existing-note requests dispatch directly to A for doubt or G for quiz. A plain study topic follows the notes workflow. Explicit single notes and standalone links do not require a syllabus.

## Pass 2 — Decompose and score each note

Resolve the vault from the explicit path, `SCRIPTORIUM_VAULT_PATH`, or `~/.scriptorium-config.json`. Run `vault_index.py "<vault>" --discover --topic "<topic>"` for compact title, heading, placement, tag and template evidence. Use local filenames and numbering when established. Honor configured or strongly matched custom layouts for otherwise unlocked requests and follow their [manifest workflow](references/pre_gen_gate.md) after routing. Outline a dependency-ordered DAG without source requests. Keep cohesive mechanisms together and split independently reusable definitions. Audit the requested scope across foundations, mechanisms, theory, variants and failure regimes. A bounded outline such as CNN convolution, history and Conv2d parameters is sufficient when it covers the requested scope.

| Signal | Select using evidence specific to this subtopic |
|---|---|
| `purpose` | Decision (`compare`), signature lookup (`reference`), rapid recall (`revise`), reusable definition (`definition`), implementation/trace (`implement`), or conceptual architecture (`explain`). |
| `impl_weight` | `high` when mastery requires first-principles code, shape/state tracing or production parity. Otherwise `low`. Pure callable lookup remains reference. |
| `density` | `callables` for a catalog of roughly 8–10+ members or one dense callable. `micro` for one indivisible definition. Otherwise `cohesive`. |
| `math_level` | 0 for logical/state constraints, 1 to apply formulas, 2 when deriving/proving why they hold is central. Independent of route. |
| `verification_stack` | Explicit requested language > established vault convention > applicable ecosystem default. Pick 1–3 substantive implementations or a manual check when code is inapplicable. |

Apply precedence deterministically: command/explicit lock → standalone source lock → compare → reference or callable catalog → revise → definition or micro → implementation/high weight → general. Math and stack never select a route. Use `docs-and-papers`, `papers-and-textbooks`, `official-docs`, `source-only`, `primary-paper`, `problem-and-docs`, `vault-notes`, or `planned-notes` as applicable. Select the smallest sufficient depth and give a concrete reason for it.

## Persist the plan before research

Write an outline JSON array to scratch space. Each entry needs `title`, `purpose`, `impl_weight`, `density`, `math_level`, and a concrete `routing_reason`. Optional fields are `id`, `note_id`, `template` (user selector for this subtopic), `output_path` (relative to the topic folder), `language`, `verification_stack`, `source_profile`, `domain`, `depends_on` (earlier item IDs) and `next_topic` (a later item ID). Use `--template` and `--language` for request-level overrides, `--topic` for a display name when the folder is a slug, and `--legacy-names` for established numbered slug filenames. Use topic-folder `.` for vault-relative destinations.

```sh
python3 scripts/plan_notes.py start "<vault>" --request "<request>" --topic-folder "CNN" --outline "<outline.json>"
```

The YAML output contains the topic folder, plan ID, status and per-note routing decisions. The saved plan is authoritative on retry. The planner checks all targets before writing, saves the plan before creating a topic folder, and appends `Practice Sets/<Topic> - Practice Test.md` for a new topic folder. Practice sets (`Practice Sets/...`), atomic notes (`Atomic Notes/...`), and cheatsheets (`Cheatsheets/...`) resolve to their centralized sibling folders at the same directory level as the `<subtopic>/` folders rather than inside an individual `<subtopic>/` folder. Practice inherits the highest sibling math level and up to three sibling stacks. Its path sits outside the curriculum allowlist. To resume, rerun `start` with the same request and folder. The outline is optional once the plan is saved. Use `status "<vault>" <plan-id>` to inspect it directly.

## One note at a time

1. For a scoped curriculum write the existing syllabus MOC first; its allowlist contains exact planned curriculum filenames and its graph uses planned dependencies. For a retry reuse its existing locked scope. For each pending note, load only `templates/<template>.md` and `shared/authoring_rules.md`, plus `shared/math_gates.md` when math level is positive. The scaffolder includes the shared footer. Never read the template directory as a bundle.
2. Only now fetch evidence relevant to the selected source profile. For `/scribe-atomic-notes <topic name>`, bypass multi-wave deep research and perform a single, direct web search/fetch for `<topic name>` to gather core facts quickly. For `/scribe-classnotes <topic name>`, bypass multi-wave deep research (`Waves 1–4`) completely and use fast, direct web searches/fetches only, prioritizing speed and immediate synthesis over exhaustive multi-hop research. For `/scribe-notes` deep study, use Waves 2–4 and maintain a run-local dossier keyed by canonical source URL: cache access status, exact quotes/locations, equations, API signatures, and transcript spans. Reuse it across siblings and practice. Persist the dossier in scratch if retry reuse is needed; confirm a missing source before setting its status. Scoped extraction from existing notes remains the default for compare, distill, and practice.
3. Render into scratch (stdout when `--output` is omitted). Use the existing scaffold arguments for aliases, tags, and dependency links. Pass the planned route and math level:

   ```sh
   python3 scripts/scaffold_note.py --template <route> --math-level <level> --number <id> --id <note_id> --title "<title>" --base-domain "<domain>" --master-topic "<master>" --topic "<topic>" --language <language>
   ```

4. Populate the scaffold using the selected spec from `templates/`. Translate plan edges into filename-based `--depends-on` and `--next-topic` links. Remove scaffold placeholders and record observed executions or unavailable runtimes. Before finalizing, run a mandatory **Humanization & Cohesion Pass** per `shared/authoring_rules.md`:
   - **Conversational yet rigorous tone:** Write like an experienced student or engineer explaining concepts clearly to their future self—direct, intuitive, and insightful rather than encyclopedic or robotic.
   - **Logical narrative transitions:** Connect sections and concepts naturally (explain *why* one concept leads to the next, rather than dropping isolated blocks of bullet points).
   - **Eliminate AI clichés:** Ban robotic filler phrases (`"In conclusion,"`, `"It is important to note,"`, `"Delving into,"`, `"Crucial aspect,"`, `"Let's explore"`).
   - **Synthesize, don't paste:** Rephrase retrieved web/source material into digestible mental models, intuitive analogies, and concrete examples rather than dumping raw definitions.
   Then run `python3 scripts/validate_note.py "<draft.md>"`, and `python3 scripts/plan_notes.py publish "<vault>" <plan-id> <item-id> "<draft.md>"`. Keep the draft until publication succeeds so a retry can reuse the exact bytes. Finish all pending notes before final graph and scoped vault checks.

The Python planner consumes an agent-produced outline. It does not perform semantic research, source fetching, or prose authoring. Host slash registration is optional. Custom vault templates retain the existing manifest workflow and validation contract.
