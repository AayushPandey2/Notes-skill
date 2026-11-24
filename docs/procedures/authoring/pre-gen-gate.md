# Pre-Generation Resolution Gate

## Purpose & Activation Trigger

Resolve user intent, approved vault target (or fallback delivery mode), existing coverage, placement, template route, and metadata **before** writing any note prose via `/scribe-notes` or `/scribe-ytnotes`.

## Standing Vault-Write Authorization & Zero-Prompt Policy

- **Direct execution inside configured vault (no reverification):** Once the vault path is configured via explicit path, `SCRIPTORIUM_VAULT_PATH`, or `~/.scriptorium-config.json` (`/scribe-setfolder`), proceed immediately without sending any pre-write confirmation or reverification prompt before creating requested notes, subtopic folders, companion labs, cheatsheet/Q&A packs, or supporting image assets within that scope.
- **Zero note-type or scope questions:** Never ask *"which type of notes do you want?"* or pause for format/scope confirmation after any note-making command. Infer format, depth, source mode, and file structure directly from the user's message after the command; if only a topic name is given, default directly to **`M1` Deep Learning Notes** from scratch (zero-prerequisite comprehensive coverage).
- **Topic-branching 3-file structure:**
  - *Single concept / focused topic (no distinct sub-branches):* Generate one **3-file bundle** (`<Topic>.md`, `<Topic> - Experimental Lab.md`, `<Topic> - Cheatsheet & Interview Q&A.md`).
  - *Multi-branch topic (has distinct subtopics/branches):* Generate `00 - Map of Contents.md` plus a **separate 3-file bundle for every subtopic** (`01 - <Subtopic>.md`, `01 - <Subtopic> - Experimental Lab.md`, `01 - <Subtopic> - Cheatsheet & Interview Q&A.md`, and so on).
- **Explicit revisions & boundary check:** Update intended notes incrementally without deleting unrelated notes, overwriting custom sections/YAML, or changing the vault destination. Before each write, verify the resolved destination stays inside the approved vault (reject `..` traversal and escaping symlinks). Only pause if vault access is genuinely unconfigured/revoked or platform controls block writing.
- **Permission-declined / vault-unavailable fallback:** If permission is declined, **do not** repeatedly request it or attempt another route into the vault—continue producing the notes and deliver them in chat instead (also use this fallback whenever vault access is unavailable):
  1. When supported, provide each completed note as a separate downloadable `.md` attachment with its intended filename using an authorized temporary or output location (without writing to the vault), and include acquired image assets in a downloadable package preserving relative links.
  2. If downloadable attachments are unavailable, present each complete note separately in a clearly labeled, copyable Markdown block and state that it must be saved manually—never describe displayed text as a downloadable file or claim notes were saved to the vault.
  3. Preserve all teaching, formatting, source, and verification requirements in either delivery mode.

## Execution Sequence

0. **Self-Inferred Configuration (No Prompts):** Infer master (`M1`–`M7` or `video-notes.md`), depth, scope (`S0`–`S5`), and layout (`single_bundle` vs. `multi_branch_collection`) directly from the user's command message. A bare topic name defaults automatically to `M1` comprehensive from-scratch deep notes; select `single_bundle` (3 files) for an atomic/focused topic and `multi_branch_collection` (`00 - Map of Contents.md` + 3 files per subtopic) for a topic with distinct sub-branches. Never ask the user which note type they want, never send a reverification prompt, and never run a pre-gen knowledge quiz.
1. **Resolve Approved Vault Root (or Fallback):** Explicit vault path → `SCRIPTORIUM_VAULT_PATH` → `~/.scriptorium-config.json` (`/scribe-setfolder`), verifying the resolved write target stays inside the approved vault. If vault access is declined or unavailable, switch to the chat/downloadable fallback above.
2. **Index Existing Coverage:** When vault access is active, search existing vault Markdown files directly using native file/search tools to detect existing notes.
3. **Non-Destructive Reuse:** Link existing notes via `[[Exact Filename|Title]]`; update intended notes incrementally without deleting notes or overwriting unrelated custom user sections or YAML.
4. **Resolve Placement & Metadata:** Use `<Vault>/<Topic>/` (`create_category_folders=false` default; specialized files in `Practice Sets/`, `Atomic Notes/`, `Cheatsheets/`, `comparison/`) and attach profile-appropriate YAML ([properties-policy.md](../../properties/properties-policy.md), [tag-taxonomy.md](../../properties/tag-taxonomy.md)).
5. **Select Template:** Load only templates under `docs/blueprints/` matching the routed format/variant; never run Templater JS or emit unresolved placeholders.

## Failure Handling & Review

- Review output against [verification-checklist.md](../review/verification-checklist.md) so unrelated vault files stay untouched and delivery status (vault write vs. downloadable attachment vs. copyable chat Markdown) is reported honestly.
