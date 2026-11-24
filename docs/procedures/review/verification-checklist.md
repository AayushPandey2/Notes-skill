# Semantic Verification Checklist

## Purpose & Activation Trigger

Perform an explicit manual review of reader-facing teaching quality, source fidelity, representation alignment, lab completeness, and Markdown/Obsidian structure before concluding any note-creation or update task. Review the actual generated content, not merely headings. **Do not treat heading count, word count, or image count as proof of teaching quality.** This is a manual review checklist, not an automated software test or validator script.

## Reader-Facing Quality Questions

Before finishing any substantive note or lab, verify every applicable question honestly:
1. Does the opening establish a real learner problem or question before naming the method?
2. Are prerequisites and unfamiliar terms introduced immediately before first use?
3. Is every analogy explained clearly (what corresponds to what) and bounded (where it breaks down)?
4. Are formal definitions unpacked term by term rather than dropped whole?
5. Does every image receive preparation (what to look for), element-by-element decoding, concrete tracing, limit qualification, and a reading check?
6. Can the reader trace one concrete running example end to end?
7. Are equations connected to the mechanism and visual meaning (`Question → intuition → visual meaning → symbols → formula → calculation → interpretation → check`)?
8. Are difficult transformations and non-obvious steps explained rather than skipped?
9. Are calculated results interpreted accurately (stating what the number measures and what it does **not** establish)?
10. Are assumptions, conditions, and failure limits explicit?
11. Does practice progress from guided examples toward independent application with separately explained answers?
12. Can the note support understanding with collapsed folds closed and deeper study with them open?
13. Are sources, citations, and execution status honest?

## Structural, Visual & Lab Gates

- **Direct-Authoring & Safety:** Confirm no scripts, downloaders, or builder files were created or executed, and no existing unrelated Obsidian notes or assets were overwritten.
- **Metadata & YAML:** Line 1 starts with valid `--- ... ---` YAML matching either the 5-key comprehensive `M1` profile (`id`, `aliases`, `topic`, `tags`, `nexttopics`) or Obsidian Properties (`topic`, `tags`, `master_topic`, `domain`, `note_type`), with zero leaked scaffold comments or internal planning logs.
- **Mathematical Fold Parity & Delimiters:** Every displayed `$$...$$` equation is preceded by orienting prose and immediately followed by a properly quoted `> [!note]- 📐 Understand this formula` callout without nested `$$` delimiters. Reject incompatible `\(...\)` / `\[...\]` delimiters or raw mathematical commands (such as `\frac`) outside math delimiters.
- **Visual Coverage & Local Acquisition:** Count downloaded web images separately from native Mermaid, Markdown tables, and video frames. Reject visually rich notes with unexplained missing image coverage (recheck long visually rich notes with 0 or 1 downloaded image), planned/remote image URLs without local raster assets, or images inserted without the six-phase narrative. Check Mermaid syntax and prose walkthrough; claim rendering only if observed.
- **Substantive Explanations & Companion Lab:** Reject patronizing shortcuts (`"obviously"`, `"trivially"`, `"as you know"`), visible opening inventory dumps (`Level`, `Estimated prerequisites`, `Implementation languages`, `Libraries and tools`, `Practical objective`, `Experiment objective`), repeated mathematical walkthroughs, dataset or unit changes without explanation, unsupported numerical predictions, anticipated results labeled as observed findings, baseline comparisons across different partitions, cross-reference-only explanations, long code without detailed line-by-line collapsed walkthroughs, workflow steps reduced to one sentence, grouped placeholder ranges, broken section numbers/anchors, or four ML implementations solving incomparable tasks. Confirm each new content note has one sibling lab with reciprocal links, complete code before breakdown, and `Status: static review (not executed)` on unexecuted code.
- **Links, Source Coverage & Safe Saving:** Internal `[[wikilinks]]` resolve to existing or planned notes, all fenced code blocks are closed, citations have actual locators, and supplied source coverage gaps or unverified steps (execution, hashing, Obsidian UI rendering) are disclosed honestly. Inspect written files after saving and confirm unrelated files remain intact.
