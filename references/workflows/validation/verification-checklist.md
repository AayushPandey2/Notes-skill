# Semantic Verification Checklist

## Purpose & Activation Trigger

Perform an explicit manual review of educational quality, source fidelity, representation alignment, and Markdown/Obsidian structure before concluding any note-creation or update task. This is a manual review checklist, not an automated software test.

## Review Gates

- **Direct-Authoring & Safety:** Confirm no scripts or builder files were created or executed during note generation, and no existing unrelated Obsidian notes or assets were overwritten.
- **Metadata & YAML:** Line 1 starts with valid `--- ... ---` YAML matching either the 5-key comprehensive `M1` profile (`id`, `aliases`, `topic`, `tags`, `nexttopics`) or Obsidian Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type`), with zero leaked scaffold comments or internal planning logs.
- **Educational Spine & Clarity:** Beginner-first progression (motivation and intuition before equations), natural paragraph spacing, prerequisite bridges before first use, causal comparisons before summary tables, and explicit limitations (`Use when / When not to use`).
- **Mathematical Fold Parity:** Every displayed `$$...$$` equation is preceded by orienting prose and immediately followed by a properly quoted `> [!note]- 📐 Understand this formula` callout explaining relevant symbols, units/shapes, derivations, and numerical walkthroughs without nested `$$` delimiters.
- **Visual & Source Honesty:** Confirm each embedded image is local, exists, has inspected content and checked rights, and carries attribution. Citations have actual locators. Label unexecuted educational code `Status: static review (not executed)`.
- **Links & Completeness:** Internal `[[wikilinks]]` resolve to existing or planned notes, all fenced code blocks are closed, and any unverified aspect (such as code execution, cryptographic hashing, or Obsidian UI rendering) is disclosed honestly.
- **Source Coverage:** For a supplied source, compare its important sections and claims with the final note headings; mark omitted or inaccessible parts rather than claiming complete coverage.
- **Safe Saving:** Before revising, inspect the original note and assets. After saving, inspect the written files, confirm custom YAML and unrelated files remain, and report any partial write. Manual review is not an atomic transaction or an automated test.
