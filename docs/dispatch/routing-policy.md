# Routing policy

Load when a request names multiple products or its intended format is unclear. The [master registry](master-registry.yaml) maps artifact formats, and [subject-registry.yaml](subject-registry.yaml) maps subject theory, investigation labs, and safety policies; neither installs commands or runs software.

Route across **four independent dimensions** without forcing unrelated domain assumptions:
- **Master format:** Artifact intent (`M1`–`M7` or `video-notes`).
- **Knowledge type:** Broad pedagogical style (`domains/`).
- **Subject specialization:** Domain obligations (`docs/blueprints/subjects/`).
- **Lab profile:** Domain-appropriate practical tracks (`docs/blueprints/investigations/`) and safety policy (`docs/procedures/safety/`) when applicable.

1. Respect the user's explicit command and source limits, and **never** ask *"which type of notes do you want?"* or pause for reverification after a note-making command. Infer everything directly from the prompt after the command. A source-only request uses `R-S0` and never browses outside supplied material. `R-S1` permits targeted external verification only when the user permits source-first verification. An output choice never loosens a source restriction.
2. Honor an explicit requested product such as “formula sheet” or “worked solutions.” Ignore a negated product phrase such as “don't make a cheat sheet.” Otherwise infer the dominant learning objective via [router.md](../../router.md) without prompting.
3. A bare topic name (with no explicit alternate format) defaults automatically to **`M1` deep-notes** taught comprehensively from scratch (zero prerequisites). Topic structure follows natural branching: a focused concept with no distinct sub-branches produces one 3-file bundle (notes, experimental lab, cheatsheet & interview Q&A), whereas a multi-branch topic produces `00 - Map of Contents.md` plus a separate 3-file bundle for each subtopic. Supplied lectures or chapters requested in order use `M2`; a paper analysis or comparison uses `M7`; a video request uses `M2` (`video-notes.md`).
4. Keep a small summary inside the primary note when it supports that note. For two independently requested artifacts, route each separately and share the same verified facts and notation.

The installed public skill folders are `/scribe-notes`, `/scribe-ytnotes`, `/scribe-doubt`, `/scribe-quiz`, and `/scribe-setfolder`. Old note-command names may be explained as migrated requests; do not claim they are installed commands. If a selected template is missing, state that gap rather than inventing a registry entry.
