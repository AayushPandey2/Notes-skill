# Hidden Grading Key: `binary-search-flawed.md`

*Evaluation-only answer key—never provide to the blind reviewer.*

1. **Critical — Termination bug (infinite loop):** Uses `hi = mid` inside `while (lo <= hi)`. When `lo == hi` and `A[mid] > target`, `hi` does not decrease and the loop never terminates.
2. **Critical — Dishonest execution claim:** Claims `"Verified runtime: 0.02 ms on 10^6 elements"` despite static-only authoring (`Source and static review only; not compiled or executed here.` required).
3. **Major — Missing precondition & invariant:** Claims binary search works `"on any array"` without stating the sorted-input precondition, loop invariant, initialization, maintenance, or complexity derivation.
4. **Major — Overflow bug:** Uses `mid = (lo + hi) / 2` instead of `lo + (hi - lo) / 2`, risking signed integer overflow.
5. **Moderate — Missing boundary & transfer coverage:** Omits empty-array behavior, duplicate-handling (lower/upper bound), and monotonic-predicate generalization.
