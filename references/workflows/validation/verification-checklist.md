# Semantic verification

Run mechanical checks from [router](../../../router.md#plan-and-publish), then inspect what automation cannot establish:

- Outcome and scope match the saved `instructional_plan`, ARRIE `research_plan`, and supplied source policy.
- Deep plans: inspect required modules and per-concept depths, prerequisite order, source inventory receipts, verified `evidence_registry` citations (`validate_note.py --evidence`), contradiction handling, and cross-chunk consistency under [research-engine.md](../research/research-engine.md) and [source-fidelity.md](../research/source-fidelity.md#semantic-review-and-correction).
- Every important claim traces to inspected evidence (`content_verified: true`) under [evidence rules](../../../shared/authoring_rules.md#evidence); recommended further-learning resources follow [resource-recommendations.md](../research/resource-recommendations.md) and stay distinct from factual citations.
- Definitions, dimensions, tensor shapes, units, assumptions, equations, visuals, and code agree across retained representations (`scriptorium/engines/pedagogy.py (`scripts/scribe.py pedagogy`)` / [pedagogical-intelligence.md](../notes-creation/pedagogical-intelligence.md)).
- Implementations teach distinct purposes; observed execution tier differs explicitly from static checks or proofs.
- Worked examples are non-redundant and attributed; point-of-need misconceptions avoid invented statistics; revision summaries preserve applicability conditions and link back to Layer A headings.
- Explanation Intelligence (`EIS-01`–`EIS-07`): verify central-question resolution, coherent transitions without invented causality, motivated derivation steps, explicit applicability boundaries, verified procedural traces/invariants (only where applicable), reasoning-preserving retrieval cues, and absence of `CF-01`–`CF-12` friction or leaked blueprint headings (`QualityEngine.review_explanatory_clarity()` / `scripts/scribe.py explain --review`).
- Optional modules meet their activation guides; omitted modules leave no empty headings or broken numbering.
- Apply [cohesion](../../../shared/authoring_rules.md#cohesion). A passing linter establishes neither mathematical proof nor factual correctness.
