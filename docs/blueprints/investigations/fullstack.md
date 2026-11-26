# Full-Stack Development Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Contract
Applies to Frontend, Backend, Web APIs, and Full-Stack applications. **Scope guard:** For narrow frontend/language topics (e.g., CSS Flexbox, JS closures), use only the relevant browser/component tracks—do **not** force a backend or database vertical slice unless integration is central. Define file responsibilities, API/schema contracts, validation rules, and placeholder env config (no real secrets) once inside Markdown fences.

## Practical Realizations
1. **Core Web / Runtime Mechanism:** Minimal vanilla DOM/JS/HTTP/SQL primitive explaining what frameworks wrap.
2. **Framework Realization:** Clean implementation in the requested frontend/backend framework.
3. **Minimal Vertical Slice** *(only when full-stack integration is central)*: Frontend $\to$ API endpoint $\to$ validation/auth $\to$ persistence $\to$ response/UI update.
4. **Contract Testing & Failure Diagnosis:** Verify validation, authz checks, 4xx/5xx propagation, stale UI state, and network/DB error handling.

## Specialized Walkthrough & Verification
Trace one complete user action across the boundaries in scope. Inspect state updates and error paths at each boundary.
