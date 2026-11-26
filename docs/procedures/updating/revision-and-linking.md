# Revision, Knowledge Synthesis & Vault Linking

## Purpose & Activation Trigger

Govern condensed revision sections inside `M1`/`M2` notes, standalone `M3`/`M7` revision outputs (`revision_pack`, `concept_map`), and safe vault wikilink maintenance.

## Decision Rules & Integrity Contract

1. **No Paragraph Duplication:** Keep the full `M1`/`M2` note authoritative for derivations and citations; build revision sections and `M3`/`M7` packs as structured retrieval cues pointing back to canonical headings rather than copying paragraphs or inventing claims.
2. **Preserve Formula Hypotheses:** Retain domain and applicability assumptions on every condensed equation.
3. **Four Link Cases & Prerequisite DAG Acyclicity:** Distinguish every target before writing links:
   - *Existing note:* Verified `[[Wikilink]]` (resolved to its inspected title/path).
   - *Companion in the same bundle:* Plan the reciprocal link, but verify acceptance and actual publication before keeping it—update or remove broken reciprocal links cleanly on partial publication failure and report what actually wrote.
   - *Planned future learning topic:* Keep in plain text or authorized `nexttopics` metadata—never emit standalone dead wikilinks that imply a nonexistent file exists, and never auto-generate extra notes merely to satisfy a link.
   - *Explicitly requested placeholder link:* Use unresolved placeholder wikilinks *only* when the user explicitly requests Obsidian's unresolved-link workflow (never by default).
   **Apply DAG acyclicity strictly to `requires` (prerequisite) dependencies**—related-topic links, bidirectional contrasts, and genuine conceptual cycles (such as feedback loops) are allowed.
4. **Link & Identifier Edge-Case Hygiene:** Use path-qualified wikilinks when identical note names exist in different folders, resolve ambiguous aliases before linking, recheck heading anchors after edits, keep excluded concepts out of automatic prerequisite/`nexttopics` links, and create reciprocal companion links **only** for artifacts that actually exist.

## Knowledge Lifecycle & Version Intelligence

Classify revisions explicitly (**factual correction**, **clearer explanation**, **new convention**, **API update**, **source update**, or **scope expansion**), check affected companion files (Theory/Lab/Mastery), and **never overwrite learner-customized sections or YAML** when refreshing external details. Match revision triggers to knowledge stability:

| Knowledge Type | Stability & Revision Strategy |
|---|---|
| **Mathematical theorem** | Stable unless a factual/logical error or missing hypothesis is found |
| **Language semantics** | Track applicable language-standard revisions (e.g., C11/C++20/Rust edition) |
| **Library API** | Track official versioned documentation and deprecations |
| **Scientific consensus** | Revisit when substantive empirical/mechanistic evidence shifts |
| **Engineering standard** | Identify the applicable standard/protocol revision |
| **Empirical benchmark** | Preserve dataset, evaluation conditions, and publication context |

## Execution & Review

Inspect target notes before updating wikilinks, verify prerequisite (`requires`) acyclicity manually, and review against [verification-checklist.md](../review/verification-checklist.md).
