# Scriptorium routing

## Pass 1 — Resolve command, selector, and source

Start here with the raw request and read only this file during routing. Use `python3 scripts/plan_notes.py inspect "<request>"` for deterministic command/source parsing. Classify paraphrases by intent before requesting evidence. Accept slash commands on hosts that register the wrappers and the same request as plain text (for example, `scribe-dsa cpp Two Sum` or “Create a practice set for my CNN notes”). An explicit named vault template still follows the custom-template gate.

- DSA: `/scribe-dsa <language> <problem or URL>` locks DSA and the language. A URL anywhere in its problem is evidence. Return usage on missing language/problem or an unsupported language.
- Practice: `/scribe-practice <topic-or-note>` locks practice. Resolve one existing topic folder and the requested sibling note(s) through vault discovery. Save `Practice Set/<Target> - Practice.md` within it. Never append a second practice item.
- Compare and distill lock comparison and cheat-sheet. Ingest with a topic and a source retains deduplication and local placement. Notes and expand retain their syllabus/coverage contracts. Doubt and quiz dispatch immediately with no authoring or external research.
- An explicit template selector or natural-language format request locks the route beneath command locks. “Summarize this paper” therefore selects summary. A bare paper URL selects paper-breakdown (arXiv, DOI, OpenReview, ACL Anthology, conference proceedings and IEEE). A bare article, docs or video URL selects summary. A reference inside a broader study request supplies evidence without locking the routes.

For writing requests, read the applicable [command playbook](references/command_playbooks.md) section after routing (B expand, C notes, D distill, E ingest, F compare). For existing-note requests dispatch directly to A for doubt or G for quiz. A plain study topic follows the notes workflow. Explicit single notes and standalone links do not require a syllabus.

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

The YAML output contains the topic folder, plan ID, status and per-note routing decisions. The saved plan is authoritative on retry. The planner checks all targets before writing, saves the plan before creating a topic folder, and appends `Practice Set/<Topic> - Practice Test.md` for a new folder. Practice inherits the highest sibling math level and up to three sibling stacks. Its path sits outside the curriculum allowlist. To resume, rerun `start` with the same request and folder. The outline is optional once the plan is saved. Use `status "<vault>" <plan-id>` to inspect it directly.

## One note at a time

1. For a scoped curriculum write the existing syllabus MOC first; its allowlist contains exact planned curriculum filenames and its graph uses planned dependencies. For a retry reuse its existing locked scope. For each pending note, load only `templates/<template>.md` and `shared/authoring_rules.md`, plus `shared/math_gates.md` when math level is positive. The scaffolder includes the shared footer. Never read the template directory as a bundle.
2. Only now fetch evidence relevant to the selected source profile. Use Waves 2–4 for deep study. Maintain a run-local dossier keyed by canonical source URL: cache access status, exact quotes/locations, equations, API signatures, and transcript spans. Reuse it across siblings and practice. Persist the dossier in scratch if retry reuse is needed; confirm a missing source before setting its status. Scoped extraction from existing notes remains the default for compare, distill, and practice.
3. Render into scratch (stdout when `--output` is omitted). Use the existing scaffold arguments for aliases, tags, and dependency links. Pass the planned route and math level:

   ```sh
   python3 scripts/scaffold_note.py --template <route> --math-level <level> --number <id> --id <note_id> --title "<title>" --base-domain "<domain>" --master-topic "<master>" --topic "<topic>" --language <language>
   ```

4. Populate the scaffold using the selected spec. Translate plan edges into filename-based `--depends-on` and `--next-topic` links. Remove scaffold placeholders and record observed executions or unavailable runtimes. Run `python3 scripts/validate_note.py "<draft.md>"`, then `python3 scripts/plan_notes.py publish "<vault>" <plan-id> <item-id> "<draft.md>"`. Keep the draft until publication succeeds so a retry can reuse the exact bytes. Finish all pending notes before final graph and scoped vault checks.

The Python planner consumes an agent-produced outline. It does not perform semantic research, source fetching, or prose authoring. Host slash registration is optional. Custom vault templates retain the existing manifest workflow and validation contract.
