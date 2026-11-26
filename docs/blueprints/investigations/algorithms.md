# Algorithms & Data Structures Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Worked Example
Applies to algorithmic mechanisms, data structures, correctness, complexity, and implementation trade-offs. **Honor the user's requested language** (never force Rust or unsolicited parallel languages unless explicitly requested). Define input/output types, ordering/structural bounds, cost model, and one discriminating worked example once.

## Practical Realizations
1. **Baseline** *(only when educationally distinct and exposing a bottleneck)*.
2. **Core / Improved Algorithm or Data Structure:** Efficient implementation maintaining the governing invariant, explaining intermediate states and data transformations.
3. **Alternative Representation:** Recursive vs. iterative, or standard-library comparison showing API/complexity trade-offs.
4. **Verification, Testing & Independent Practice:** Discriminating edge cases derived from the **actual invariant and problem contract** (empty, single element, duplicates, missing target, cycles/negative weights, overflow), debugging & testing strategy, plus 1–2 **Independent Exercises** (`> [!hint]-` / `> [!success]-`).

## Specialized Walkthrough & Verification
Establish the problem-family correctness argument, derive time/space complexity under stated assumptions, trace intermediate states, and label unexecuted code **`Source and static review only; not compiled or executed here.`** (never claiming execution/benchmarking without external evidence).
