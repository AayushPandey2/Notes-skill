# Central Tag Taxonomy

All generated notes use one consistent hierarchical Obsidian tag taxonomy:

```text
topic/<specific-topic-slug>
subject/<parent-subject-slug>
domain/<domain-slug>
master-topic/<master-topic-slug>
subdomain/<subdomain-slug>       # when known
concept/<concept-slug>           # primary + up to 3 central secondary concepts
type/<canonical-note-type>
level/<beginner|intermediate|advanced>   # optional, only when justified
skill/<skill-slug>                       # optional, only when useful
```

## Normalization & Anti-Inflation Rules

1. All managed tags are lowercase kebab-case with no `#` prefix.
2. Synonyms canonicalize deterministically (e.g., `ml` / `machinelearning` / `machine_learning` → `machine-learning`; `dsa` → `data-structures-algorithms`; `ai` → `artificial-intelligence`).
3. Never treat every mentioned word as a tag; emit focused, high-signal tags for filtering and discovery.
4. Never inject unrelated discipline tags (e.g., ML tags in Physics or History notes).
5. In strict source-only mode, derive tags strictly from the source or clearly established topic context.
6. Preserve user-defined tags during incremental note updates.

Comprehensive five-key notes require `topic/`, `subject/`, `domain/` roots from the
same generator. Topic tags describe owned concepts; collection classification
supplies the parent subject/domain. Legacy tags remain for compatibility.
`validate_semantic_tags` rejects generic-only, malformed and duplicate tags; it
cannot certify an author's classification. Unknown topics retain a general
fallback until the author supplies an explicit reviewed classification.
