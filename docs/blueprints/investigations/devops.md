# DevOps, Cloud & Infrastructure Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Contract
Applies to build systems, containers, CI/CD, IaC, cloud networking, and SRE reliability. Specify **versioned dependencies, runtime environment compatibility, permission boundaries**, and placeholder config/secrets once (never embed real credentials or assume production authority).

## Practical Realizations
1. **Manual Underlying Construction:** Explain and trace the underlying primitive (e.g., container namespaces/layers, lockfile resolution, desired-state diff) before tooling.
2. **Declarative Configuration / Automation:** Author the version-pinned configuration (`Dockerfile`, Compose, workflow/IaC YAML) explaining each directive.
3. **Reproducible Delivery Workflow:** Connect build caching, test gates, config injection, and health checks cleanly.
4. **Inspection, Testing, Compatibility, Recovery & Independent Practice:** Document read-only inspection checks, misconfiguration debugging (cache busting, root privileges, runtime mismatch, ephemeral volume loss), rollback steps, and 1–2 **Independent Exercises** (`> [!hint]-` / `> [!success]-`).

## Specialized Walkthrough & Verification
Honor requested tooling/languages without unsolicited extras, describe illustrative infrastructure behavior as a prediction (attributing live evidence only to supplied/published logs), and close with **`Source and static review only; not compiled or executed here.`**
