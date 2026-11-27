# Scriptorium development handoff — Prompt 15

## Current system identities

- **Production candidate:** H, `beecf2bce22df9e612f26ff7604989571c9ccfd1`, unchanged and unaccepted. G remains `173ca50f13bc9bcf4af1826c67492d5c6d9ed84d`. Candidate I does not exist.
- **Development branch/starting commit:** `NewApproach` at `4b01ae22e278d2043783579b1a2c2415619848ad`. The current documentation HEAD is recoverable with `git rev-parse HEAD`.
- **Evaluation protocol:** EP14, unchanged in Prompt 15.
- **Host capability profile:** `HCP15-unchanged-blocked`.
- **Production modifications:** none. No runtime, routing, visual, source, metadata, or math instruction changed.

Read `scriptorium_p15_host_resolution_and_visual_validation_report.md` for the full evidence record. No release readiness is claimed.

## Prompt 15 outcome

The current host inventory still exposes web discovery and `view_image` for an existing local file, but no general compliant existing-image URL-to-local-binary operation. The only potentially changed route was checked once: CUA returned `apps: []`, `browsers: []`, and `Browsers: Error: The browser access host is unavailable`, matching Prompt 14. No newly exposed relevant integration was present. Prompt 13's escalated `curl` remains outside Scriptorium's non-execution authoring contract and was not repeated.

Selected outcome: **H15-C**.

```text
Compliant acquisition: BLOCKED
Local binary persistence: NOT RUN
Generation-agent capability: UNAVAILABLE
Visual inspection of a new asset: NOT RUN
Natural M1 generation: NOT RUN
Independent EP14 evaluation: NOT RUN
Strict-source negative control: NOT APPLICABLE
```

The dependent experiments were stopped before prompt/topic preregistration because their capability prerequisite failed. This is not a failed H generation, and it does not waive H's applicable visual benchmark gap.

## Preserved findings

- EP14 remains the prospective bundle/visual evaluation protocol. No score or rule changed in Prompt 15.
- The runtime/EP14 scope distinction may legitimately allow a bounded publishable fallback to fail a richer benchmark. The shared theory rubric's retrieval-failure/inapplicability phrase remains ambiguous relative to EP14. No Prompt 15 artifact produced a contradictory verdict, so no runtime defect or policy edit is established.
- Prompt 14's metadata calibration remains narrow positive evidence: the complete fixture passed and the fixture missing `tags`/`domain` required repair. No new failure justified another metadata test or instruction.
- The pre-existing working-tree deletion of `scriptorium_p11_implementation_report.md` remains preserved. Protected release fixtures, the real user vault, and remote branches were untouched.

## Evidence locations and retention

Prompt 15 scratch evidence:

`/home/main/.gemini/antigravity/brain/13219d6f-eaa5-479d-812b-ce2ec1dfa512/scratch/p15_diagnostics/`

It contains manifests, current capability inventory/delta, the blocked acquisition gate, runtime/EP14 comparison, candidate decision, blockers, and `artifact_hashes.txt`. There are no placeholder natural-generation/review/control artifacts. The tracked Prompt 15 report preserves the conclusion if scratch later disappears. The scratch directory has project precedent but no formal retention guarantee. Original Prompt 12 and most Prompt 13 packages remain unavailable.

Measured Prompt 15 activity: 0 fresh generations, 0 independent artifact reviews, 0 acquisition attempts, 0 successful acquisitions, 0 new persisted/inspected assets, 0 authoring repairs, 1 browser inventory check, and 2 relevant tool-inventory searches. Model identity was exposed as `gpt-5.6-sol`; reasoning setting, provider token/cache counters, exact returned instruction bytes, and centralized complete tool logs were unavailable.

## Exact next action

Do not run another identical diagnostic without a host change. The owner must provision or explicitly authorize a constrained purpose-built existing-image acquisition operation accessible to the generation context, or accept fallback-only behavior with unmet applicable local-visual benchmarks. Once it exists, run one direct acquisition/persistence/inspection validation, one frozen natural visually meaningful H task, one fresh EP14 review with actual assets, and one strict-source negative control. Keep H and EP14 unchanged so the effect is attributable to host capability.
