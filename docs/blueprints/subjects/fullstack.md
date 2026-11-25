# Subject Theory Blueprint: Full-Stack Web Development

## Purpose

Ensure Full-Stack, Frontend, and Backend notes teach the **underlying web-platform and computing principles** plus the **complete request/response lifecycle** rather than listing framework syntax or hooks in isolation.

## 1. Core Principle: Web Fundamentals Before Framework Syntax

- Explain **why** a browser or server mechanism exists before teaching framework wrappers (e.g., DOM reconciliation & state-driven UI before React `useState`/`useEffect`; HTTP semantics & statelessness before Express/FastAPI middleware).
- Trace concrete **browser $\to$ HTTP $\to$ router/middleware $\to$ validation/auth $\to$ business logic $\to$ database $\to$ response $\to$ UI state** flows whenever a full-stack interaction is central.

## 2. Selectable Topic-Family Obligations

| Topic Family | Theory That Should Not Be Omitted |
|---|---|
| **HTML** | DOM tree, semantic elements, accessibility (ARIA/keyboard), forms & document structure |
| **CSS** | Cascade, specificity, inheritance, box model, normal flow, Flexbox/Grid, responsive breakpoints |
| **JavaScript** | Execution context, lexical scope & closures, prototypes, event loop, microtasks vs. macrotasks, promises/`async` |
| **TypeScript** | Structural typing, type narrowing, inference, generics, compile-time erasure vs. runtime validation |
| **React / Frontend UI** | Component trees, props vs. state, ownership, rendering & reconciliation, effect lifecycles & stale closures |
| **Backend** | Routing, middleware pipeline, request lifecycle, schema validation, business logic, error propagation |
| **REST & Web APIs** | Resources, representations, HTTP methods, status codes, idempotency, pagination & versioning |
| **Databases** | Schema design, constraints, foreign keys, indexes, queries, transactions & N+1 pitfalls |
| **Authentication** | Identity verification, password hashing, sessions, cookies (`HttpOnly`/`SameSite`), signed tokens & expiry |
| **Authorization** | Roles, permissions, resource ownership checks, trust boundaries & server-side enforcement |
| **Testing & Deployment** | Unit vs. integration vs. E2E vs. contract tests; builds, environment config, secrets & observability |
| **Performance** | Caching headers/layers, network waterfalls, rendering cost, DB query bottlenecks |
