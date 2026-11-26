# Evaluation Fixture (Flawed): Binary Search (`evaluations/fixtures/algorithms/`)

*Evaluation-only intentionally flawed example—illustrates polished-looking prose that fails adversarial theory & practical review.*

## Defects Demonstrated Here (For Grader Calibration)
1. **Stated without proof:** Claims `O(log n)` and "always works" without stating the sorted-input precondition or loop invariant.
2. **Broken midpoint & termination bug:** Uses `mid = (lo + hi) / 2` (overflows on large signed indices) and `hi = mid` inside `while (lo <= hi)` (infinite loop when `lo == hi` and `A[mid] > target`).
3. **Missing boundary & transfer coverage:** Ignores empty arrays, duplicates (first/last position), and fails to connect to monotonic predicates.
4. **Dishonest execution claim:** Prints `"Verified runtime: 0.02 ms on 10^6 elements"` despite zero code execution.
