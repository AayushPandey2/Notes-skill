# Subject Theory Blueprint: DevOps, Cloud & Infrastructure

## Purpose

Teach DevOps and Infrastructure through **reproducibility, isolation mechanisms, immutable artifacts, declarative state, and operational recovery** rather than memorizing CLI flags.

## Core Theory Obligations

1. **OS & Environment Foundations First:** For containers, explain Linux namespaces, cgroups, union/overlay filesystems, images vs. containers, and layers *before* Dockerfile syntax.
2. **Reproducibility & Dependency Management:** Separate build-time vs. runtime dependencies, lockfiles, multi-stage builds, immutable artifacts, and configuration injection (`env` vs. secrets).
3. **Networking, Storage & Orchestration:** Trace container/service DNS, port mapping, reverse proxies, ephemeral vs. persistent volumes, health checks, and declarative reconciliation loops.
4. **CI/CD & Delivery Safety:** Explain test gates, artifact caching, zero-downtime rollouts (blue/green, canary), observability (logs, metrics, traces), and rollback strategies.
5. **Safety & Authority:** Never embed real credentials or assume production cluster authority; separate read-only inspection from mutating deploys.
