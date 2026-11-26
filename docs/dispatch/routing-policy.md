# Routing policy

Load when a request names multiple products or its intended format is unclear. The [master registry](master-registry.yaml) maps artifact formats, and [subject-registry.yaml](subject-registry.yaml) maps subject theory, investigation labs, and safety policies; neither installs commands or runs software.

Route across **four independent dimensions** without forcing unrelated domain assumptions:
- **Master format:** Artifact intent (`M1`–`M7` or `video-notes`).
- **Knowledge type:** Broad pedagogical style (`domains/`).
- **Subject specialization:** Domain obligations (`docs/blueprints/subjects/`).
- **Lab profile:** Domain-appropriate practical tracks (`docs/blueprints/investigations/`) and safety policy (`docs/procedures/safety/`) when applicable.

1. Respect the user's explicit command and source limits, and **never** ask *"which type of notes do you want?"* or pause for reverification after a note-making command. Infer everything directly from the prompt after the command. A source-only request uses `R-S0` and never browses outside supplied material. `R-S1` permits targeted external verification only when the user permits source-first verification. An output choice never loosens a source restriction.
2. Honor an explicit requested product such as “formula sheet” or “worked solutions.” Ignore a negated product phrase such as “don't make a cheat sheet.” Otherwise infer the dominant learning objective via [router.md](../../router.md) without prompting.
3. **Canonical Artifact & Route Resolution:**
   - **Independent lesson:** `M1` (`deep-notes.md`), defaulting to `theory_bundle` unless single-file is requested.
   - **Source-ordered textbook/PDF/lecture:** `M2` (`study-notes.md`), defaulting to `theory_bundle` unless single-file is requested.
   - **Comprehensive video notes:** `video_notes` (`video-notes.md`, one note per video—never `M2`).
   - **Brief video summary:** `M7` (`quick-summary.md`).
   - **User-supplied video screenshot explanation:** Source analysis of the supplied image (never authorizes playing videos or capturing frames).
   - **Compact / single-artifact routes (`M3`, `M4`, `M6`, `M7`) & `M5`:** Follow `artifact_policy` in [master-registry.yaml](master-registry.yaml) (exempt from automatic 3-file bundles; `M5` does not duplicate itself into an identical companion lab).
4. **Subject Selection & Maximum Necessary Reference Set:** Choose **one primary subject** from [subject-registry.yaml](subject-registry.yaml) for main progression and lab, pulling secondary subjects selectively only for needed prerequisites, formalism, or verification. Load only the selected master, primary subject, dominant knowledge type, and conditional math/visual/lab/safety files—never full directories.
5. Keep a small summary inside the primary note when it supports that note. For two independently requested artifacts, route each separately and share the same verified facts and notation.

The installed public skill folders are `/scribe-notes`, `/scribe-ytnotes`, `/scribe-doubt`, `/scribe-quiz`, and `/scribe-setfolder`. Old note-command names may be explained as migrated requests; do not claim they are installed commands. If a selected template is missing, state that gap rather than inventing a registry entry.
