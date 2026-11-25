# DevOps, Cloud & Infrastructure Investigation Lab Blueprint

Use this lean blueprint for Containers, CI/CD, Infrastructure-as-Code, and Cloud Operations companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed **A–G** walkthroughs, and static review.

**Safety boundary:** Never embed real credentials, API keys, private endpoints, or assume authority over production infrastructure. Keep configurations declarative, minimal, and reproducible for isolated educational environments.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — DevOps & Infrastructure Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Service & Environment Contract
Define the target workload, isolation boundary (namespaces/cgroups/network/storage), environment variables (placeholder only), and reliability criteria.

## Four DevOps Tracks (Apply Track-Applicability Gate)

1. **Track 1 — Manual Underlying Construction:** Explain and trace the underlying OS/build/network primitive (e.g., container image layers, namespace isolation, DNS/reverse-proxy routing) before tooling.
2. **Track 2 — Automation / Container Configuration:** Author the declarative artifact (`Dockerfile`, Compose, IaC/workflow YAML) explaining every directive.
3. **Track 3 — Reproducible Delivery Workflow:** Connect build, test, artifact caching, config injection, and health checks into a clean reproducible pipeline.
4. **Track 4 — Reliability, Inspection & Recovery Verification:** Document read-only inspection checks, misconfiguration diagnosis (layer cache busting, root privileges, port/volume mismatch), and rollback/recovery steps.

Directly beneath each configuration/workflow, include `> [!example]- Understand this configuration: architecture, directives, and dry run` covering **A–G**: **A** inputs, base images, env/secret boundaries; **B** isolation/reproducibility mechanism; **C** build/deploy step order; **D** trace of one build/request/failover cycle; **E** expected state & observability signals; **F** cache invalidation, ephemeral storage loss, secret leaks, crash loops; **G** core-workflow reconstruction.

## Verification Status

Label behavior **Expected** (never **Executed** against live infra) and end with **`Source and static review only; not compiled or executed here.`**
