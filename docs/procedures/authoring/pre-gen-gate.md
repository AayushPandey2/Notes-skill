# Pre-Generation Resolution Gate

## Purpose & Activation Trigger

Resolve user intent, approved vault target (or fallback delivery mode), existing coverage, placement, template route, and metadata **before** writing any note prose via `/scribe-notes` or `/scribe-ytnotes`.

## Standing Vault-Write Authorization & Zero-Prompt Policy

- **Direct execution inside configured vault (no reverification):** Once the vault path is configured via explicit path, `SCRIPTORIUM_VAULT_PATH`, or `~/.scriptorium-config.json` (`/scribe-setfolder`), proceed immediately without sending any pre-write confirmation or reverification prompt before creating requested notes, subtopic folders, companion labs, cheatsheet/Q&A packs, or supporting image assets within that scope.
- **Zero note-type or scope questions:** Never ask *"which type of notes do you want?"* or pause for format/scope confirmation after any note-making command. Infer format, depth, source mode, and artifact selection directly from the user's message after the command; if only a topic name is given, default directly to **`M1` Comprehensive Theory Notes** from scratch.
- **Artifact Selection First, Then Topic-Folder Layout:** Determine exact included artifacts from the resolved `artifact_plan` ([adaptive-engine.md](adaptive-engine.md), driven by `artifact_policy` in [master-registry.yaml](../../dispatch/master-registry.yaml) and `source_permissions`) **before** creating files. Unless placing an explicit standalone cross-topic sheet (`Cheatsheets/`, `Practice Sets/`, `Atomic Notes/`, `comparison/`), create `<Configured Target>/<Topic>/` first and place everything for that topic inside it:
  - *When `artifact_policy` resolves to `theory_bundle` (`M1`/`M2`):* emit only the artifacts included in the resolved `artifact_plan` (up to 3 files per unit: `<Topic>.md`, plus `<Topic> - Experimental Lab.md` and `<Topic> - Cheatsheet & Interview Q&A.md` when permitted/supported; multi-branch topics emit `00 - Map of Contents.md` plus a resolved bundle per subtopic `01 - <Subtopic>.md`, etc.).
  - *When `artifact_policy` resolves to `single_artifact`, `implementation_guide`, or `one_note_per_video`:* emit only the requested artifact(s) inside `<Topic>/` (or the requested standalone directory).
- **Explicit revisions & boundary check:** Update intended notes incrementally without deleting unrelated notes, overwriting custom sections/YAML, or changing the vault destination. Before each write, verify the resolved destination stays inside the approved vault (reject `..` traversal and escaping symlinks). Only pause if vault access is genuinely unconfigured/revoked or platform controls block writing.
- **Permission-declined / vault-unavailable fallback:** If permission is declined, **do not** repeatedly request it or attempt another route into the vault—continue producing the notes and deliver them in chat instead (also use this fallback whenever vault access is unavailable):
  1. When supported, provide each completed note as a separate downloadable `.md` attachment with its intended filename using an authorized temporary or output location (without writing to the vault), and include acquired image assets in a downloadable package preserving relative links.
  2. If downloadable attachments are unavailable, present each complete note separately in a clearly labeled, copyable Markdown block and state that it must be saved manually—never describe displayed text as a downloadable file or claim notes were saved to the vault.
  3. Preserve all teaching, formatting, source, and verification requirements in either delivery mode.

## Execution Sequence

0. **Self-Inferred Configuration (No Prompts):** Infer master (`M1`–`M7` or `video_notes`), depth, `source_policy`, primary subject, and artifact layout (`artifact_policy` in [master-registry.yaml](../../dispatch/master-registry.yaml)) directly from the user's command message. Never ask which note type is wanted, send a reverification prompt, or run a pre-gen knowledge quiz.
1. **Resolve Approved Vault Root (or Fallback):** Explicit vault path → `SCRIPTORIUM_VAULT_PATH` → `~/.scriptorium-config.json` (`/scribe-setfolder`), verifying the resolved write target stays inside the approved vault. If vault access is declined or unavailable, switch to the chat/downloadable fallback above.
2. **Index Existing Coverage:** When vault access is active, search existing vault Markdown files directly using native file/search tools to detect existing notes.
3. **Non-Destructive Reuse:** Link existing notes via `[[Exact Filename|Title]]`; update intended notes incrementally without deleting notes or overwriting unrelated custom user sections or YAML.
4. **Resolve Placement & Metadata:** Create and target `<Configured Target>/<Topic>/` first (keeping all notes, companions, and `assets/` for that topic inside `<Topic>/`; specialized standalone files go in `Practice Sets/`, `Atomic Notes/`, `Cheatsheets/`, `comparison/` only when explicitly requested as standalone outputs) and attach profile-appropriate YAML ([properties-policy.md](../../properties/properties-policy.md), [tag-taxonomy.md](../../properties/tag-taxonomy.md)).
5. **Select Template:** Load only templates under `docs/blueprints/` matching the routed format/variant; never run Templater JS or emit unresolved placeholders.

## Failure Handling & Review

- Review output against [verification-checklist.md](../review/verification-checklist.md) so unrelated vault files stay untouched and delivery status (vault write vs. downloadable attachment vs. copyable chat Markdown) is reported honestly.
