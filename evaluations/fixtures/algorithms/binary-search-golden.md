# Evaluation Fixture (Golden): Binary Search (`evaluations/fixtures/algorithms/`)

*Evaluation-only reference excerpt showing desired invariant, correctness, boundary, and transfer quality—never copy as a mandatory template.*

## Governing Invariant & Initialization
Suppose `A[0..n-1]` is sorted in non-decreasing order (`A[i] <= A[j]` for all `i < j`). Maintain closed bounds `[lo, hi]` with the **loop invariant**: *if `target` appears in `A`, then `target` lies inside `A[lo..hi]`*. Initially `lo = 0` and `hi = n - 1`, so `[lo..hi]` covers the entire array and the invariant holds vacuously even when `n = 0` (`hi = -1 < lo`).

## Maintenance, Termination & Overflow-Safe Midpoint
Compute `mid = lo + (hi - lo) / 2` (avoiding signed 32-bit overflow in `(lo + hi) / 2` when `lo + hi > INT_MAX`).
- If `A[mid] == target`, return `mid`.
- If `A[mid] < target`, sortedness guarantees `A[0..mid] < target`, so setting `lo = mid + 1` preserves the invariant while strictly shrinking `hi - lo + 1` by at least half.
- If `A[mid] > target`, sortedness guarantees `A[mid..n-1] > target`, so setting `hi = mid - 1` preserves the invariant and strictly shrinks the interval.
Since `hi - lo + 1` is a non-negative integer that strictly decreases on every non-returning step, the loop terminates in at most $\lfloor \log_2 n \rfloor + 1$ comparisons (`O(log n)` time, `O(1)` auxiliary space).

## Boundary Cases & Generalization to Monotonic Predicates
- **Empty (`n = 0`) / missing target:** Loop exits with `lo > hi`; returns not-found without out-of-bounds access.
- **Duplicates:** Exact-match binary search returns *an* arbitrary matching index; to find the first/last occurrence, replace early return with a monotonic boundary predicate (`P(x): A[x] >= target`) and maintain `P(hi)` true vs. `P(lo)` false.
- **Violated assumption:** On unsorted `[4, 1, 3, 2]` searching for `1`, `A[1] = 1` or `mid` comparisons can discard the half containing `1` because `A[0..mid]` no longer bounds smaller elements.
