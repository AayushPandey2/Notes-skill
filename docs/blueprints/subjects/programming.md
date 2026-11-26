# Subject Theory Blueprint: Programming Languages & Semantics

## Purpose

Teach programming languages through **exact language semantics, memory/lifetime models, type systems, and execution behavior**—never importing C pointer semantics into Python or confusing language guarantees with illustrative stack/heap diagrams. Activate only the overlay matching the requested language.

## Conditional Language Overlays

| Language | Theory That Must Be Explained When Relevant |
|---|---|
| **C** | Object lifetime (static/automatic/allocated), pointers & provenance, representation/alignment, undefined behavior (UB) vs. implementation-defined |
| **C++** | Value categories (`lvalue`/`rvalue`/`prvalue`), ownership & RAII, move semantics, templates/instantiation, object lifetime & UB |
| **Python** | Object identity (`id`), name-to-object binding/references, mutability vs. aliasing, LEGB scope, interpreter/GIL & exception semantics |
| **Rust** | Ownership, moves vs. `Copy`, shared vs. mutable borrowing rules, lifetimes as compile-time guarantees, traits/generics, `Result`/`Option` error handling |
| **JavaScript / TS** | Lexical environments, closures, prototype chain, event loop (call stack, microtasks, macrotasks), promises/`async` |

## Cross-Language Discipline

- **Lifetime vs. storage location:** Distinguish language storage-duration/lifetime guarantees from compiler/runtime placement (e.g., stack vs. heap vs. escape analysis).
- **Diagnostics:** Explain *why* an intentionally invalid snippet fails type-checking or borrow-checking rather than treating compiler errors as magic.
