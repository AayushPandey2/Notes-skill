# Subject Theory Blueprint: Programming Languages & Semantics

## Purpose

Teach programming languages through **exact language semantics, memory/lifetime models, type systems, and execution behavior**—never importing C pointer semantics into Python or confusing language guarantees with illustrative stack/heap diagrams. Activate only the overlay matching the requested language.

## Conditional Language Overlays

| Language | Theory That Must Be Explained When Relevant |
|---|---|
| **C** | Storage durations (static, **thread**, automatic, allocated), pointers & provenance, object representation/alignment, undefined behavior (UB) vs. implementation-defined |
| **C++** | Value-category taxonomy (**`glvalue` / `rvalue`** classification and **`lvalue` / `xvalue` / `prvalue`** distinctions), ownership & RAII, move semantics, templates/instantiation, object lifetime & UB |
| **Python** | Language-level object identity (`id`), name-to-object binding/references, mutability vs. aliasing, LEGB scope, exceptions—kept distinct from **CPython/build-specific GIL** behavior |
| **Rust** | Ownership, moves vs. `Copy`, **reference validity, borrowing relationships, and lifetime annotations** (not merely "compile-time guarantees"), traits/generics, `Result`/`Option` error handling |
| **JavaScript / TS** | **ECMAScript semantics** (lexical environments, closures, prototypes, promises/`async`) vs. **host event-loop** queues vs. **TypeScript's compile-time structural type system** |

## Cross-Language & Mechanism Overlays

- **Conditional execution overlays:** Function call mechanics, evaluation order (and unsequenced evaluation traps), error/exception propagation, deterministic vs. GC resource cleanup, concurrency models, and language-specific mutability.
- **Lifetime vs. storage location:** Distinguish language storage-duration/lifetime guarantees from compiler/runtime placement (e.g., stack vs. heap vs. escape analysis).
- **Diagnostics:** Explain *why* an intentionally invalid snippet fails type-checking or borrow-checking rather than treating compiler errors as magic.
