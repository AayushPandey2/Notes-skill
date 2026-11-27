# Scriptorium development handoff — Prompt 11

## Current phase

Candidate H is implemented as a narrow instruction correction, but **acceptance is withheld** because no fresh matched G/H generations or independent scorecards were completed. It is not release ready. Read `scriptorium_p11_implementation_report.md` and the untracked Prompt 10 report before further work.

## Identity and state

- Branch: `NewApproach`; G baseline: `173ca50f13bc9bcf4af1826c67492d5c6d9ed84d`; H local instruction commit: `beecf2b`.
- H changes: `docs/blueprints/presets/formula-sheet.md` and `core/math_gates.md` only. The formula-sheet edit existed uncommitted when Prompt 11 began; its source-example intent was preserved and its precision clause refined.
- F/G historical snapshots and artifacts: `/home/main/.gemini/antigravity/brain/13219d6f-eaa5-479d-812b-ce2ec1dfa512/scratch/` (`p08_snapshots`, `p09_snapshots`, `p09_eval`). These are historical evidence, not fresh H outputs.
- `scriptorium_p10_evaluation_and_optimization_report.md` was untracked at Prompt 11 start; do not silently remove or conflate it with H.

## Completed

- Read Prompt 10 report; inspected branch, HEAD, worktree, local tracking and relevant instruction path.
- Confirmed G r2's unqualified heat-capacity product error and the strict-source example wording conflict.
- Replaced existing preset/math-gate wording without adding a new policy layer.
- Audited historical Michaelis–Menten, Catalase and Euler terminology findings and classified them as artifact-level or behavioral-evaluation work.
- Ran `git diff --check` and static routing/reference inspection; no protected release fixture or user vault was modified.

## Pending and exact next action

1. Freeze a development-only R-S0 fixture containing a worked example outside production runtime content.
2. Run fresh, matched G/H generations for ID 03 (prefer two each), the worked-example strict fixture, and ID 75's no-example source. Use the same model, reasoning level, host settings, tools, source and output contract; log actual reads, tool calls and provider counters where observable.
3. Grade complete artifacts with the unchanged canonical rubric, keeping H identity hidden from a genuinely separate reviewer if available. Apply the critical-error override. Expand regression to ID 76/77 and non-ML math transfer as justified by the shared math-gate change.
4. Update the Prompt 11 report with actual artifacts, passage citations, scorecards, telemetry and an evidence-based accept/revise/retain-G decision. Do not treat the historical Prompt 10 manual scores as matched H evidence.

Unresolved: whether the local wording repair changes behavior; whether compactness, source fidelity, and cross-domain depth regress; actual retrieval/token costs; fresh remote state. No publication test was performed.
