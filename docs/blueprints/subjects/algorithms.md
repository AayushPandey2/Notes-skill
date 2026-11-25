# Subject Theory Blueprint: Algorithms & Data Structures

## Purpose

Teach Algorithms and Data Structures through **problem representation, governing invariants, correctness proofs, and complexity/memory trade-offs** rather than memorized code templates.

## Core Theory Obligations

1. **Problem & Representation:** State exact input/output contracts, preconditions (e.g., sorted order, non-negative weights, acyclic graph), and how data representation shapes allowed operations.
2. **Governing Invariant:** Explicitly establish the loop invariant (initialization, maintenance, termination), recursion invariant, or structural invariant (e.g., heap property, BST ordering, balance invariant) *before* code.
3. **Correctness & Termination:** Prove why the algorithm terminates and returns the right answer on normal and boundary cases (empty, single element, duplicates, missing targets, ties).
4. **Complexity & Memory Models:** Derive time and auxiliary space complexity (best/average/worst/amortized), distinguish asymptotic complexity from constant factors and cache/memory-hierarchy behavior, and explain *why* a baseline bottlenecks before introducing the optimization.
5. **Transfer & Failure Modes:** Show how invariants generalize to monotonic predicates, variants, or dual formulations, and diagnose off-by-one errors, integer mid-overflow, and broken preconditions.
