# Routing Authority

- [master-registry.yaml](master-registry.yaml) — Canonical registry of the seven masters (`M1`–`M7`), template variants, knowledge-type subtemplates, and `/scribe-*` command mappings.
- [routing-policy.md](routing-policy.md) — Deterministic-first routing precedence, negation handling, multi-artifact rules, and safe defaults.
- Deterministic implementation: [scriptorium/engines/orchestration.py (`scripts/scribe.py route`)](../../scriptorium/engines/orchestration.py) integrated with [scripts/plan_notes.py](../../scripts/plan_notes.py).
