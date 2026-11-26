# Algorithms & Data Structures Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Fixture
Applies to algorithmic mechanisms, data structures, correctness, complexity, and implementation trade-offs. **Honor the user's requested language** (never force Python and Rust together unless requested). Define input/output types, ordering/structural bounds, cost model, and one discriminating fixture once.

## Practical Realizations
1. **Baseline** *(only when educationally distinct and exposing a bottleneck)*.
2. **Core / Improved Algorithm or Data Structure:** Efficient implementation maintaining the governing invariant.
3. **Alternative Representation:** Recursive vs. iterative, or standard-library comparison showing API/complexity trade-offs.
4. **Verification & Boundary Suite:** Discriminating edge cases derived from the **actual invariant and problem contract** (e.g., empty, single element, duplicates, missing target, negative/zero weights, disconnected components, integer mid-overflow).

## Specialized Walkthrough & Verification
Establish and maintain the problem-family correctness argument (loop invariant, induction, greedy exchange, DP recurrence, or amortized potential), derive time/auxiliary-space complexity under the stated cost model, trace consequential transitions on the fixture, and diagnose broken preconditions. End with **`Source and static review only; not compiled or executed here.`**
