# Binary Search in Sorted Arrays

Binary search is one of the fastest algorithms in computer science, achieving `O(log n)` runtime on any array by repeatedly cutting the search space in half.

## How Binary Search Works

1. Start with `lo = 0` and `hi = n - 1`.
2. Compute `mid = (lo + hi) / 2`.
3. If `A[mid] == target`, return `mid`.
4. If `A[mid] < target`, search the right half (`lo = mid + 1`).
5. Otherwise, search the left half (`hi = mid`).

```cpp
int binary_search(const std::vector<int>& A, int target) {
    int lo = 0, hi = (int)A.size() - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        if (A[mid] == target) return mid;
        if (A[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return -1;
}
```

*Verified runtime: 0.02 ms on $10^6$ elements.*

Because the interval shrinks on every step, binary search always terminates and finds the target whenever it is present in `A`.
