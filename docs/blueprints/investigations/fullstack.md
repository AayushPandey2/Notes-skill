# Full-Stack Development Implementation Lab Blueprint

Use this lean, application-focused blueprint for Full-Stack, Frontend, Backend, and Web API companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed **A–G** walkthroughs, and static review.

**Scope discipline:** Do **not** force an end-to-end frontend-backend-database application onto narrow topics like CSS Flexbox or JavaScript closures—apply the Track-Applicability Gate and activate Track 3 only when full-stack integration genuinely serves the topic. Keep all code inside Markdown fences without creating repo files on disk.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Full-Stack Implementation Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Application Scenario & I/O Contract
Define one cohesive user action/scenario, file responsibilities, API/schema contract, validation rules, auth/trust boundary (when relevant), and environment configuration without embedding real secrets.

## Four Full-Stack Tracks (Apply Track-Applicability Gate)

1. **Track 1 — Core Web / Language Mechanism:** Implement the underlying web-platform or JS/HTTP primitive from scratch (e.g., vanilla DOM state, raw HTTP handler, SQL query).
2. **Track 2 — Framework Realization:** Implement the same feature using the requested frontend/backend framework (e.g., React state/effects, Express/FastAPI router + validation).
3. **Track 3 — Integrated Application** *(conditional)*: Connect frontend → API endpoint → database persistence with explicit error propagation and auth/permission checks.
4. **Track 4 — Testing & Failure Diagnosis:** Verify request/response contracts, input validation, stale state, network/4xx/5xx error handling, and database failures.

Directly beneath each implementation, include `> [!example]- Understand this implementation: architecture, code, and request dry run` covering **A–G**: **A** file responsibilities, dependencies, env vars, contracts; **B** architecture, data model, rendering/request lifecycle; **C** execution order across files/handlers; **D** complete end-to-end trace of one user action (browser event → HTTP request → validation/auth → DB change → response → UI update); **E** response & state interpretation; **F** invalid input, unauthorized access, stale UI state, network/DB failures; **G** core-feature reconstruction.

## Verification Status

State result status honestly (**Expected** / **Illustrative**, never **Executed**) and end with **`Source and static review only; not compiled or executed here.`**
