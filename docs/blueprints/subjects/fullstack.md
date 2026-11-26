# Subject Theory Blueprint: Full-Stack Web Development

## Purpose

Ensure Full-Stack, Frontend, and Backend notes teach **browser behavior, state transitions, HTTP request contracts, accessibility, security boundaries, and integration reasoning** rather than isolated framework syntax.

## 1. Core Principle: Web Fundamentals & Complete Contracts Before Framework Syntax

- Explain **why** a browser, runtime, or server mechanism exists before framework wrappers (e.g., DOM reconciliation & state ownership before React hooks; HTTP semantics & statelessness before Express/FastAPI middleware).
- Trace concrete **browser event $\to$ HTTP request $\to$ router/middleware $\to$ validation/auth $\to$ business logic $\to$ database $\to$ response $\to$ UI state** flows when full-stack integration is central, opening with a concrete user action while closing JS/HTTP prerequisites inline, pairing event-loop/layout/request models with verified web-sourced diagrams per [representations.md](../../procedures/authoring/representations.md) (never generated/Mermaid/ASCII), and progressing from a worked flow to an independent extension or debugging exercise.

## 2. Selectable Topic-Family Obligations

| Topic Family | Theory That Should Not Be Omitted |
|---|---|
| **HTML & Accessibility** | DOM tree, semantic landmarks, keyboard navigation, ARIA roles/states, native form semantics |
| **CSS** | Cascade, specificity, inheritance, box model, normal flow, Flexbox/Grid layout, responsive breakpoints |
| **JavaScript** | Execution context, lexical scope & closures, prototypes, event loop, microtasks vs. macrotasks, promises/`async` |
| **TypeScript** | Structural typing, narrowing, inference, generics, compile-time erasure vs. runtime schema validation |
| **Frontend UI (e.g., React)** | Component trees, props vs. state, state transitions, rendering/reconciliation, effect lifecycles & stale closures |
| **Backend & REST APIs** | Routing, middleware pipeline, request/response contracts, HTTP methods/status codes, idempotency, error propagation |
| **Databases** | Schema design, constraints, indexes, queries, transactions & N+1 pitfalls |
| **Security (AuthN / AuthZ)** | Password hashing, sessions/`HttpOnly` cookies vs. tokens, CSRF/XSS awareness, server-side ownership/role checks |
| **Testing & Performance** | Unit/integration/E2E/contract tests; caching headers, network waterfalls, rendering & DB bottlenecks |
