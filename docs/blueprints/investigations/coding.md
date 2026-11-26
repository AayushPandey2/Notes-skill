# Programming Language Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md). (For Data Structures & Algorithms, use [algorithms.md](algorithms.md).)

## Applicability & Shared Fixture
Applies to language constructs, type systems, ownership/lifetimes, concurrency primitives, and API semantics. Define I/O types, mutability/lifetime rules, and one concrete miniature program state once, strictly honoring the user's requested language (never force ML splits or unsolicited Rust/multi-language stacks).

## Practical Realizations
1. **Construct + Practical Usage:** Demonstrate the feature cleanly in a realistic function/module, explaining intermediate execution states and data transformations.
2. **Idiomatic Alternative & Complexity:** Compare an alternative idiom or standard-library pattern in the requested language with clear time/memory and readability trade-offs.
3. **Testing, Debugging, Failure Analysis & Independent Exercises:** Trace execution, memory/ownership, aliasing, null/overflow edge cases, optional **intentionally non-compiling diagnostic example** (`Intentionally invalid — demonstrates compiler/runtime diagnostic`), unit-testing/debugging approach, and 1–2 **Independent Exercises** (`> [!hint]-` / `> [!success]-`).

## Specialized Walkthrough & Verification
Trace types, lifetimes/ownership transfers, stack/heap or scope semantics, edge cases, and failure modes, and close code-containing labs with **`Source and static review only; not compiled or executed here.`** (never claiming compilation/testing without external evidence).
