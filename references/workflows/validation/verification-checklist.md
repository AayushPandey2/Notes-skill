# Semantic Verification Checklist

## Purpose & Activation Trigger

Verify educational quality, source fidelity, representation alignment, and mathematical/runtime honesty after mechanical syntax checks pass (`A9 Checker`, `T13`, `validate_note.py` / `notes compose --validate`).

## Semantic Inspection Gates

- **Plan & Source Alignment:** Outcome matches `instructional_plan`, ARRIE `research_plan`, and active `source_policy` (strict/expanded element order, `[UNVERIFIED]` gaps, verified `evidence_registry` entries with `content_verified: true`, separate `resource-recommendations.md` list).
- **Educational Spine (`EIS-01`–`EIS-07`):** Run `QualityEngine.review_explanatory_clarity()` / `scripts/scribe.py explain --review` and confirm beginner-first progression, central-question resolution, intuitive transitions before equations, zero `CF-01`–`CF-12` cognitive friction, zero leaked scaffold/blueprint headings, and atomic `> [!example]- Understand this formula step by step` folds beneath every `$$...$$`.
- **Cross-Representation Parity & Honesty:** Definitions, units, shapes, equations, prose, inspected raster visuals (`Explain -> Show -> Decode -> Connect`), and code match cleanly; execution claims match actual observed runtime status (`plan_notes.py verify-runtimes`); omitted optional blocks leave zero `N/A` placeholders or broken numbering.

## Failure Handling & Validation

- Repair only the smallest defective span + dependents ([authoring_rules.md](../../../shared/authoring_rules.md)), invalidate stale review receipts, and confirm `QualityEngine.evaluate_teaching()` and `scripts/verify_vault_notes.py` pass without modifying unrelated vault notes.
