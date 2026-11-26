# Subject Theory Blueprint: DevOps, Cloud & Infrastructure

## Purpose

Teach DevOps, Cloud, and Infrastructure across **build systems, CI/CD pipelines, containers/orchestration, infrastructure-as-code, observability, and reliability engineering**—never forcing container theory onto unrelated build or SRE topics.

## Core Theory Obligations

1. **Subdomain Principle First:** Identify the specific layer before tooling syntax:
   - *Build systems & CI/CD:* Dependency resolution, lockfiles, deterministic/reproducible builds, caching, test gates, artifact promotion.
   - *Containers & runtime isolation:* Linux namespaces, cgroups, union filesystems, images vs. containers, multi-stage builds *before* Dockerfile syntax.
   - *Infrastructure-as-Code & Cloud:* Declarative desired state vs. imperative scripts, state files/drift, reconciliation loops, IAM/network isolation, secret management.
   - *Observability & Reliability (SRE):* SLIs/SLOs/error budgets, structured logs/metrics/traces, health probes, zero-downtime rollouts (blue/green, canary), and rollback/incident recovery.
2. **Environment & Failure Modes:** Trace port/volume/DNS mismatches, cache invalidation bugs, ephemeral storage loss, config drift, and privilege leaks.
3. **Safety & Authority:** Never embed real credentials or assume production cluster authority; separate read-only inspection from mutating deploys.
4. **Beginner Progression, Visuals & Practice:** Motivate each infrastructure layer with a concrete shipping or outage scenario (closing OS/networking prerequisites inline), pair pipeline, isolation, and rollout topologies with verified web-sourced architecture visuals per [representations.md](../../procedures/authoring/representations.md) (never generated/Mermaid/ASCII) or declarative state tables, and trace one concrete config or failure diagnosis before an independent troubleshooting exercise.
