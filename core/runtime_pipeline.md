# Direct-authoring workflow

The [authoring rule in the root skill](../SKILL.md#scriptorium) governs every note-creation route. Educational code in a note is lesson content, never a note builder.

1. Resolve the user's request, permitted sources, audience, scope, and authorized Obsidian destination. Check existing notes before choosing filenames.
2. Load the selected master and only relevant variant, subtemplate, teaching module, and policy.
3. Research within the source policy. For needed visuals, complete the acquisition and local-inspection stages in [representations.md](../docs/procedures/authoring/representations.md); search or viewing alone does not acquire an image.
4. Draft the intended Markdown directly. For each newly generated non-video content note, create or update its sibling under [the experimental-lab contract](../docs/procedures/authoring/experimental-lab.md) (`/scribe-ytnotes` produces one self-contained note per video without a lab). Review claims, calculations, YAML, reciprocal links, and embeds against the actual drafts.
5. Verify the resolved destination remains inside the approved vault ([pre-gen-gate.md](../docs/procedures/authoring/pre-gen-gate.md#standing-vault-write-authorization-policy)), then save intended notes, labs, folders, and inspected assets without re-asking permission; for explicit revisions, update intended notes directly without deleting notes or overwriting unrelated content. Reopen saved files to confirm embed targets exist. If vault permission is declined or unavailable, do not re-ask or retry another vault route—deliver each completed note via the downloadable `.md` or copyable chat Markdown fallback and report delivery status honestly.

Use [the manual verification checklist](../docs/procedures/review/verification-checklist.md). Disclose checks that could not be done; do not claim that manual review provided automatic validation, atomic publication, or recovery.
