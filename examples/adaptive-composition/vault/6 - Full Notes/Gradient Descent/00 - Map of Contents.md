---
id: gradient-descent.moc
aliases:
- Map of Contents
topic: Gradient Descent
tags:
- topic/gradient-descent
- subject/machine-learning
- domain/artificial-intelligence
- master-topic/machine-learning
- subdomain/optimization
- concept/gradient-descent
- type/full-notes
nexttopics:
- '[[01 - Why Local Descent Works]]'
---
# Gradient Descent

## Learning path

1. [[01 - Why Local Descent Works]]
2. [[02 - Deriving the Update and Its Limits]]
3. [[03 - Tracing the Algorithm]]
4. [[04 - Implementing and Testing Descent]]
5. [[05 - Curvature and Failure Analysis]]

## Concept prerequisites

```mermaid
flowchart TD
    n0["First-order descent model"]
    n1["Descent direction and finite step length"]
    n0 --> n1
    n2["Exact quadratic recurrence"]
    n1 --> n2
    n3["Stability boundaries and exceptional initialization"]
    n2 --> n3
    n4["Simultaneous state updates"]
    n3 --> n4
    n5["Trace indexing and memory"]
    n4 --> n5
    n6["Scalar implementation and independent oracle"]
    n5 --> n6
    n7["Finite checks and numerical tolerance"]
    n6 --> n7
    n8["SPD eigenbasis reduction"]
    n7 --> n8
    n9["Eigenvalue spread and conditional diagnostics"]
    n8 --> n9
```

| Concept | Canonical chapter | Prerequisites |
|---|---|---|
| First-order descent model | [[01 - Why Local Descent Works#Why Local Descent Works|Why Local Descent Works]] | none |
| Descent direction and finite step length | [[01 - Why Local Descent Works#Why Local Descent Works|Why Local Descent Works]] | gd.c1 (covered) |
| Exact quadratic recurrence | [[02 - Deriving the Update and Its Limits#Deriving the Update and Its Limits|Deriving the Update and Its Limits]] | gd.direction (covered) |
| Stability boundaries and exceptional initialization | [[02 - Deriving the Update and Its Limits#Deriving the Update and Its Limits|Deriving the Update and Its Limits]] | gd.c2 (covered) |
| Simultaneous state updates | [[03 - Tracing the Algorithm#Tracing the Algorithm|Tracing the Algorithm]] | gd.boundary (covered) |
| Trace indexing and memory | [[03 - Tracing the Algorithm#Tracing the Algorithm|Tracing the Algorithm]] | gd.c3 (covered) |
| Scalar implementation and independent oracle | [[04 - Implementing and Testing Descent#Implementing and Testing Descent|Implementing and Testing Descent]] | gd.trace (covered) |
| Finite checks and numerical tolerance | [[04 - Implementing and Testing Descent#Implementing and Testing Descent|Implementing and Testing Descent]] | gd.c4 (covered) |
| SPD eigenbasis reduction | [[05 - Curvature and Failure Analysis#Curvature and Failure Analysis|Curvature and Failure Analysis]] | gd.tolerance (covered) |
| Eigenvalue spread and conditional diagnostics | [[05 - Curvature and Failure Analysis#Curvature and Failure Analysis|Curvature and Failure Analysis]] | gd.c5 (covered) |
