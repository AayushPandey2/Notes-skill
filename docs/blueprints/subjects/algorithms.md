# Subject Theory Blueprint: Algorithms & Data Structures

## Purpose

Teach Algorithms and Data Structures through **problem representation, problem-family-specific correctness arguments, complexity/memory trade-offs, and failure analysis** rather than memorized code templates.

## Core Theory Obligations

1. **Problem & Representation:** State exact input/output contracts, preconditions (e.g., sorted order, non-negative weights, DAG), and how data representation shapes supported operations.
2. **Problem-Family-Specific Correctness:** Match the correctness argument to the algorithm family rather than forcing one generic loop-invariant template everywhere:
   - *Iterative / searching / pointers:* Loop invariants (initialization, maintenance, termination).
   - *Recursive / divide-and-conquer:* Structural/strong induction and base-case progress.
   - *Greedy:* Greedy-choice property (exchange argument) and optimal substructure.
   - *Dynamic programming:* Overlapping subproblems, optimal substructure, state/transition recurrence, topological/base-case ordering.
   - *Graph algorithms:* Reachability/cut/cycle/relaxation invariants and negative-weight/cycle preconditions.
   - *Data structures:* Structural & balance invariants plus **amortized analysis** (aggregate, accounting, or potential method) where relevant.
3. **Complexity & Memory Models:** Derive time and auxiliary space complexity (best/average/worst/amortized), distinguish asymptotic complexity from constant factors and cache/memory-hierarchy behavior, and explain *why* a baseline bottlenecks before introducing the optimization.
4. **Transfer & Failure Modes:** Show how invariants generalize (e.g., binary search to monotonic predicates), and diagnose off-by-one errors, integer mid-overflow, stale states, and broken preconditions.

## Conditional Topic-Family Overlays
- *Searching & Sorting:* Stability, in-place vs. auxiliary memory, comparison lower bounds ($\Omega(n \log n)$) vs. non-comparison assumptions.
- *Trees & Heaps:* Height/balance invariants, recursive subtree contracts, heapify $O(n)$ vs. $O(n \log n)$ analysis.
- *Graphs:* Adjacency list vs. matrix trade-offs, BFS shortest unweighted paths, DFS discovery/finish structure, relaxation invariants.
- *DP & Greedy:* State definition, transition DAG/topological order, memoization vs. tabulation; greedy exchange proof vs. counterexample.
- *Beginner Progression, Visuals & Practice:* Trace a small concrete example (4–6 elements or tiny graph) before formal invariants/recurrences while closing asymptotic/recursion prerequisites inline, retrieve verified web-sourced tree/graph/algorithm diagrams per [representations.md](../../procedures/authoring/representations.md) (never generated/Mermaid/ASCII) alongside explicit state tables, and progress from a worked trace to an independent variant or edge-case check.
