# Pre-Generation Resolution Gate

## Purpose & Activation Trigger

Resolve user intent, approved vault target (or fallback delivery mode), existing coverage, placement, template route, and metadata **before** writing any note prose via `/scribe-notes` or `/scribe-ytnotes`.

## Standing Vault-Write Authorization Policy

- **Remember approved vault:** Once the user approves the exact notes-vault path, remember it via `~/.scriptorium-config.json` (`/scribe-setfolder`). Do not ask again before creating requested notes, folders, or supporting image assets within that scope.
- **Explicit revisions:** For explicitly requested revisions, update the intended notes without redundant confirmation. This does **not** independently authorize deleting notes, overwriting unrelated content, or changing the vault destination.
- **Per-write boundary check:** Before each write, verify that the resolved destination remains inside the approved vault (reject `..` traversal and escaping symlinks). Ask again only when the requested action exceeds that scope, authorization has been revoked, or platform controls require approval. Never claim this rule bypasses app permissions.
- **Permission-declined / vault-unavailable fallback:** If permission is declined, **do not** repeatedly request it or attempt another route into the vault—continue producing the notes and deliver them in chat instead (also use this fallback whenever vault access is unavailable):
  1. When supported, provide each completed note as a separate downloadable `.md` attachment with its intended filename using an authorized temporary or output location (without writing to the vault), and include acquired image assets in a downloadable package preserving relative links.
  2. If downloadable attachments are unavailable, present each complete note separately in a clearly labeled, copyable Markdown block and state that it must be saved manually—never describe displayed text as a downloadable file or claim notes were saved to the vault.
  3. Preserve all teaching, formatting, source, and verification requirements in either delivery mode.

## Execution Sequence

0. **Configuration Check:** Resolve master (`M1`–`M7` or `video-notes.md`), depth, scope (`S0`–`S5`), and `single_note` vs `hierarchical_collection`. Ask only genuinely unanswered scope/format questions (never run a pre-gen knowledge quiz or re-ask vault-write permission inside an already-approved vault).
1. **Resolve Approved Vault Root (or Fallback):** Explicit vault path → `SCRIPTORIUM_VAULT_PATH` → `~/.scriptorium-config.json` (`/scribe-setfolder`), verifying the resolved write target stays inside the approved vault. If vault access is declined or unavailable, switch to the chat/downloadable fallback above.
2. **Index Existing Coverage:** When vault access is active, search existing vault Markdown files directly using native file/search tools to detect existing notes.
3. **Non-Destructive Reuse:** Link existing notes via `[[Exact Filename|Title]]`; update intended notes incrementally without deleting notes or overwriting unrelated custom user sections or YAML.
4. **Resolve Placement & Metadata:** Use `<Vault>/<Topic>/` (`create_category_folders=false` default; specialized files in `Practice Sets/`, `Atomic Notes/`, `Cheatsheets/`, `comparison/`) and attach profile-appropriate YAML ([properties-policy.md](../../properties/properties-policy.md), [tag-taxonomy.md](../../properties/tag-taxonomy.md)).
5. **Select Template:** Load only templates under `docs/blueprints/` matching the routed format/variant; never run Templater JS or emit unresolved placeholders.

## Failure Handling & Review

- Review output against [verification-checklist.md](../review/verification-checklist.md) so unrelated vault files stay untouched and delivery status (vault write vs. downloadable attachment vs. copyable chat Markdown) is reported honestly.
