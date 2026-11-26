# M5 — Implementation, Design & Technical Verification Guide

*Master ID: `M5` (`implementation_guide`, compatibility route: `dsa`). Artifact policy: `implementation_guide` per [master-registry.yaml](../../dispatch/master-registry.yaml)—do **not** duplicate an `M5` guide into an identical companion Experimental Lab.*

- **Header Block:** Line-1 Standard Obsidian Properties (`note_type: implementation-guide`) + `# Implementation: <Title>` (or `# DSA: <Title>`). Lock code to the user-specified stack (defaulting to Python for Machine Learning when unspecified; **never include Rust by default**, in collapsed blocks, or for performance/production/advanced wording unless explicitly requested); never create project files on disk or execute code; label unexecuted code `Source and static review only; not compiled or executed here.`

## 1. Select the Matching Implementation Progression

Use the progression matching the request instead of forcing DSA complexity/baseline sections onto APIs, applications, infrastructure, or debugging:

| Implementation Mode | Main Progression |
|---|---|
| **Algorithm** | Problem & constraints $\to$ governing invariant $\to$ baseline (if distinct) $\to$ optimal solution $\to$ correctness & complexity $\to$ edge-case suite |
| **Library / API** | Contract & types $\to$ setup & lifecycle $\to$ core operations $\to$ state, ownership & error handling $\to$ usage examples |
| **System** | Requirements & trust/isolation boundaries $\to$ components & interfaces $\to$ end-to-end request/resource flow $\to$ concurrency & failure handling |
| **Application / Full-Stack** | User behavior & file/API contracts $\to$ architecture & schema $\to$ vertical-slice implementation (multi-file Markdown blocks permitted) $\to$ auth/validation/error propagation $\to$ tests |
| **Infrastructure** | Environment & compatibility $\to$ declarative config (`Dockerfile`/IaC/CI) $\to$ lifecycle & secrets/config injection $\to$ verification & rollback recovery |
| **Debugging** | Observed symptoms $\to$ competing hypotheses $\to$ discriminating inspection evidence $\to$ verified fix $\to$ regression prevention |

## 2. Core Implementation, Trace & Static Verification

1. **Specification & Constraints:** Define inputs/outputs, contracts, verified versions (`[ASSUMED / UNVERIFIED]` if unstated), and one discriminating scenario/input.
2. **Mechanism & Implementation:** Explain *why* the design works before code; include complete self-contained code blocks with equation/contract alignment and collapsed step-by-step walkthroughs where non-trivial.
3. **Discriminating Trace & Edge/Failure Matrix:** Trace a non-trivial scenario or input through key branches/error paths, verify boundary cases, and state `Source and static review only; not compiled or executed here.`
4. **Transfer Variations (when useful and permitted):** Give the learner a changed input, constraint or requirement. Keep the prompt visible and place the solution in a collapsed `> [!success]-` answer callout.

*Contract: [authoring_rules.md](../../../core/authoring_rules.md), [math_gates.md](../../../core/math_gates.md), [footer_widgets.md](../../../core/footer_widgets.md), [verification-checklist.md](../../procedures/review/verification-checklist.md).*
