# DevOps, Cloud & Infrastructure Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Contract
Applies to build systems, containers, CI/CD, IaC, cloud networking, and SRE reliability. Specify **versioned dependencies, runtime environment compatibility, permission boundaries**, and placeholder config/secrets once (never embed real credentials or assume production authority).

## Practical Realizations
1. **Manual Underlying Construction:** Explain and trace the underlying primitive (e.g., container namespaces/layers, lockfile resolution, desired-state diff) before tooling.
2. **Declarative Configuration / Automation:** Author the version-pinned configuration (`Dockerfile`, Compose, workflow/IaC YAML) explaining each directive.
3. **Reproducible Delivery Workflow:** Connect build caching, test gates, config injection, and health checks cleanly.
4. **Inspection, Compatibility & Recovery:** Document read-only inspection checks, misconfiguration diagnosis (cache busting, root privileges, runtime mismatch, ephemeral volume loss), and rollback steps.

## Specialized Walkthrough & Verification
Describe illustrative infrastructure behavior as a prediction. Attribute live-infrastructure evidence only to a supplied or published source, using the shared lab contract.
