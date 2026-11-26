# Programming Language Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md). (For Data Structures & Algorithms, use [algorithms.md](algorithms.md).)

## Applicability & Shared Fixture
Applies to language constructs, type systems, ownership/lifetimes, concurrency primitives, and API semantics. Define types, mutability/lifetime rules, and one concrete miniature program state once. Never force ML splits or 4-language stacks.

## Practical Realizations
1. **Construct + Practical Usage:** Demonstrate the language feature cleanly in a realistic function/module (keep a separate minimal Track 1 only when isolating the primitive materially aids clarity; merge otherwise).
2. **Idiomatic Alternative:** Compare an alternative idiom or standard-library pattern in the requested language (or requested comparison language) with clear trade-offs.
3. **State, Lifetime & Error Analysis:** Trace execution, memory/ownership, aliasing, or invalid-access failures—including an optional **intentionally non-compiling diagnostic example** (explicitly labeled `Intentionally invalid — demonstrates compiler/runtime diagnostic`) without executing undefined behavior.

## Specialized Walkthrough & Verification
Trace variable types, lifetimes and ownership transfers, stack/heap or scope semantics, execution order, and applicable aliasing, borrowing, null or overflow failure modes.
