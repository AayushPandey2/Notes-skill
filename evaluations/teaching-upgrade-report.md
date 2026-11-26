# Scriptorium teaching upgrade report

## Root causes

The preceding release set expectations for depth and visuals, but the runtime did not explicitly check that required policy files were readable before claiming compliance. The planner treated concept completion as a general field without asking for observable reasoning in the finished passage. The original KNN source illustrated the consequence: correct formulas and a broad table of contents coexisted with a compressed prediction mechanism, premature formal notation and unrepresented geometry. The earlier KNN fixture covered only theory and could not reveal disagreements across the requested lab and mastery pack.

## Architecture and conflicts

The runtime now checks governing instruction dependencies before drafting and applies the existing capability fallbacks only to optional tools. A representative core unit is reviewed before its structure is reused. The planner looks for evidence that the learner can trace, explain, predict or apply the concept. Related policies retain their existing ownership, while verification treats practical reasoning and independent learning as applicable checks in their own right. The upgrade integrates these requirements into the existing runtime and review path.

## Pedagogy, mathematical reasoning and presentation

Teaching guidance now asks for the operating choice between stages, local prerequisite bridges at first use, and examples that actually change a result or explain why it stays fixed. Editorial review follows the reasoning across prose, formulas, examples and captions, with flexible paragraph length.

The expanded KNN chapter teaches an ordinary count before the weighted indicator expression, sums actual weights to explain the vote reversal, and shows why a local mean stays in the selected target range. It distinguishes selection ties from vote ties, vote share from calibration, and fixed neighbor count from neighborhood radius. Exact pruning gets a trace with a verified numerical bound. The two new companions reuse the same cases for testing, boundary diagnosis and retrieval practice. The original audited theory is preserved byte-for-byte as a separate fixture.

## Visual instruction

Eight visually inspected plots are embedded where the corresponding mechanism is taught. Four new figures cover the weighted-vote reversal, density and neighborhood radius, regression smoothing, and an exact KD-tree pruning decision. Each figure has a textual interpretation and uses labels, markers, line styles or patterns in addition to color. The unrelated image in the circle regression fixture tests whether review checks the figure itself.

## Evaluation and verification

The [matched benchmark](teaching-upgrade-benchmark.md) records twelve paired prompts and three additional behavioral regressions. The blinded reviewer scored each version 24/24 on the matched criteria. The suite therefore documents observable differences in individual passages without establishing an improvement in overall pass rate.

Both KNN lab tracks ran on Python 3.11.18. The checks cover rankings, weighting, exact-match ties, invalid inputs, independent validation scores, note links, embeds and callout boundaries. [KNN verification record](fixtures/bundles/knn/verification-results.json)

The repository review also checked local Markdown links, all evaluation fixture paths, the separation of flawed fixtures from their keys, and the path rules used to build upload archives.

## Remaining limits and next evidence

There is one generated output per condition and topic. The criteria reached a ceiling and do not measure full-chapter quality or learner performance. Live Obsidian rendering and signed-in Claude import were outside the verified checks. Next, test closed-callout continuity and figure interpretation on full-length outputs using stronger discriminating criteria, then repeat runs or conduct a learner study before making aggregate improvement claims.

## Changed files

- `core/authoring_rules.md`
- `core/math_gates.md`
- `core/runtime_pipeline.md`
- `core/teaching_core.md`
- `core/theory_quality_contract.md`
- `docs/blueprints/components/example-engineering.md`
- `docs/blueprints/formats/deep-notes.md`
- `docs/blueprints/subjects/machine-learning.md`
- `docs/procedures/authoring/adaptive-engine.md`
- `docs/procedures/authoring/concept-reasoning.md`
- `docs/procedures/authoring/learner-model.md`
- `docs/procedures/authoring/representations.md`
- `docs/procedures/review/adversarial-theory-review.md`
- `docs/procedures/review/educational-editor.md`
- `docs/procedures/review/verification-checklist.md`
- `evaluations/evals.json`
- `evaluations/fixtures/blind/circle-mechanism-flawed.expected-findings.md`
- `evaluations/fixtures/blind/circle-mechanism-flawed.md`
- `evaluations/fixtures/blind/knn-compressed-flawed.expected-findings.md`
- `evaluations/fixtures/blind/knn-compressed-flawed.md`
- `evaluations/fixtures/bundles/knn/assets/density-radius.png`
- `evaluations/fixtures/bundles/knn/assets/kd-tree-pruning.png`
- `evaluations/fixtures/bundles/knn/assets/regression-smoothing.png`
- `evaluations/fixtures/bundles/knn/assets/weight-reversal.png`
- `evaluations/fixtures/bundles/knn/evaluation-spec.md`
- `evaluations/fixtures/bundles/knn/k-nearest-neighbors.md`
- `evaluations/fixtures/bundles/knn/knn-cheatsheet-qa.md`
- `evaluations/fixtures/bundles/knn/knn-experimental-lab.md`
- `evaluations/fixtures/bundles/knn/verification-results.json`
- `evaluations/rubrics/theory.md`
- `evaluations/teaching-upgrade-benchmark.md`
- `evaluations/teaching-upgrade-report.md`
- `evaluations/verify_knn_bundle.py`
