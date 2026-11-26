# Evaluation Fixture (Golden): Binary Search (`evaluations/fixtures/algorithms/`)

*Evaluation-only reference excerpt showing desired invariant, correctness, boundary, and transfer quality—never copy as a mandatory template.*

## Governing Invariant & Initialization
Suppose `A[0..n-1]` is sorted in non-decreasing order (`A[i] <= A[j]` for all `i < j`). Maintain closed bounds `[lo, hi]` with the **loop invariant**: *if `target` appears in `A`, then `target` lies inside `A[lo..hi]`*. Initially `lo = 0` and `hi = n - 1`, so `[lo..hi]` covers the entire array and the invariant holds vacuously even when `n = 0` (`hi = -1 < lo`).

## Maintenance, Termination & Overflow-Safe Midpoint
Compute `mid = lo + (hi - lo) / 2` (avoiding signed 32-bit overflow in `(lo + hi) / 2` when `lo + hi > INT_MAX`).
- If `A[mid] == target`, return `mid`.
- If `A[mid] < target`, sortedness guarantees `A[0..mid] < target`, so setting `lo = mid + 1` preserves the invariant while strictly shrinking `hi - lo + 1` by at least half.
- If `A[mid] > target`, sortedness guarantees `A[mid..n-1] > target`, so setting `hi = mid - 1` preserves the invariant and strictly shrinks the interval.
When `n = 0`, the loop exits immediately (`0` iterations). For $n \ge 1$, `hi - lo + 1` is a positive integer that is at least halved on every non-returning step, so the loop executes at most $\lfloor \log_2 n \rfloor + 1$ **iterations** (`O(log n)` time, `O(1)` auxiliary space; note that an iteration may perform both an equality and an ordering comparison).

## Boundary Cases & Generalization to Monotonic Predicates
- **Empty (`n = 0`) / missing target:** Loop exits with `lo > hi`; returns not-found without out-of-bounds access.
- **Duplicates (First vs. Last Occurrence):** Exact-match binary search returns *an* arbitrary matching index. To find the **first occurrence (lower bound)**, use half-open `[lo, hi)` initialized to `[0, n]` with predicate $P_{\text{lb}}(i): A[i] \ge \text{target}$ (smallest `i` where $P_{\text{lb}}(i)$ holds, then verify `i < n && A[i] == target`). To find the **last occurrence (upper bound minus 1)**, use $P_{\text{ub}}(i): A[i] > \text{target}$ on `[0, n]` to find the first index `j` strictly greater than `target`, then verify `j > 0 && A[j - 1] == target` (returning `j - 1`).
- **Violated sortedness precondition:** On unsorted `[4, 1, 3, 2]` searching for `4`, `lo = 0, hi = 3` gives `mid = 1` (`A[1] = 1`). Since `1 < 4`, binary search discards `[0..1]` (`lo = 2`), permanently losing `4` at index `0`.
