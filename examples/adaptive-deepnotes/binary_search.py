"""A verified educational fixture: return a matching index, or -1 if absent."""


def binary_search(values, target):
    lo, hi = 0, len(values)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < target:
            lo = mid + 1
        elif values[mid] > target:
            hi = mid
        else:
            return mid
    return -1


values = [2, 5, 9, 14, 20]
assert binary_search(values, 14) == 3
assert binary_search(values, 2) == 0
assert binary_search(values, 20) == 4
assert binary_search(values, 8) == -1
assert binary_search([], 8) == -1
assert binary_search([5], 5) == 0
assert binary_search([5], 4) == -1
duplicates = [2, 5, 5, 5, 9]
assert duplicates[binary_search(duplicates, 5)] == 5
print("Binary search: present, absent, boundary, empty, singleton and duplicate checks passed.")
