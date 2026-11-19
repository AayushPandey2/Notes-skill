# Semantic verification

Run mechanical checks from [router](../router.md#plan-and-publish), then inspect what automation cannot establish:

- Outcome and scope match the saved `instructional_plan` and supplied source.
- Deep plans: inspect required modules and per-concept depths, prerequisite order, source inventory receipts, and cross-chunk consistency under the [quality gate](source-fidelity.md#semantic-review-and-correction).
- Every important claim has appropriate support under [evidence rules](../shared/authoring_rules.md#evidence).
- Definitions, dimensions, assumptions and example values agree across retained modules.
- Implementations teach distinct purposes; observed execution differs explicitly from expectations.
- Optional modules meet their activation guides; omitted modules leave no empty headings or broken numbering.
- Apply [cohesion](../shared/authoring_rules.md#cohesion). A passing linter establishes neither mathematical proof nor factual correctness.
