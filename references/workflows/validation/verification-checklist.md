# Semantic Verification Checklist

## Purpose & Activation Trigger

Perform an explicit manual review of educational quality, source fidelity, representation alignment, and Markdown/Obsidian structure before concluding any note-creation or update task. This is a manual review checklist, not an automated software test.

## Review Gates

- **Direct-Authoring & Safety:** Confirm no scripts or builder files were created or executed during note generation, and no existing unrelated Obsidian notes or assets were overwritten.
- **Metadata & YAML:** Line 1 starts with valid `--- ... ---` YAML matching either the 5-key comprehensive `M1` profile (`id`, `aliases`, `topic`, `tags`, `nexttopics`) or Obsidian Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type`), with zero leaked scaffold comments or internal planning logs.
- **Educational Spine & Clarity:** Beginner-first progression (motivation and intuition before equations), natural paragraph spacing, prerequisite bridges before first use, causal comparisons before summary tables, and explicit limitations (`Use when / When not to use`).
- **Mathematical Fold Parity:** Every displayed `$$...$$` equation is preceded by orienting prose and immediately followed by a properly quoted `> [!note]- 📐 Understand this formula` callout explaining relevant symbols, units/shapes, derivations, and numerical walkthroughs without nested `$$` delimiters.
- **Visual & Source Honesty:** Review visual needs section by section and their distribution, counting downloaded images, native Mermaid, tables, and actual frames separately. For each needed external figure, check the source page and reuse information, actual raster download, local image inspection, vault-relative embed, saved target, caption, attribution, and interpretation beside the concept. A search hit or planned filename is incomplete; mark the failed stage and disclose unmet needs. Check Mermaid syntax and prose walkthrough; claim rendering only if observed. Citations have actual locators. Label unexecuted educational code `Status: static review (not executed)`.
- **Companion Lab:** Each new content note has one existing or newly created sibling lab; MOCs, labs, assets, and internal documents do not recurse. Check the chosen domain template, its ordered headings and substantive subsections, opening fields, specific reasons for genuine inapplicability, one primary structure for interdisciplinary topics, and no forced domain-inappropriate machinery. Check reciprocal body links, metadata compatibility, formula folds, matched comparison inputs, and observed versus expected result labels.
- **Links & Completeness:** Internal `[[wikilinks]]` resolve to existing or planned notes, all fenced code blocks are closed, and any unverified aspect (such as code execution, cryptographic hashing, or Obsidian UI rendering) is disclosed honestly.
- **Source Coverage:** For a supplied source, compare its important sections and claims with the final note headings; mark omitted or inaccessible parts rather than claiming complete coverage.
- **Safe Saving:** Before revising, inspect the original note and assets. After saving, inspect the written files, confirm custom YAML and unrelated files remain, and report any partial write. Manual review is not an atomic transaction or an automated test.
