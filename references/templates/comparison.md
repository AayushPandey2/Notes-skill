# Comparison

**Purpose:** help choose among alternatives using meaningful differences, equivalent conditions, and explicit trade-offs.



## Which should I choose?

## What are we comparing?

## Side by side

## Worked comparison

## Trade-offs / Edge Cases

## Related notes / Sources

### Authoring contract

- **Which should I choose?** Start with a **Choose X when… / Choose Y when…** verdict. Include a genuine tie or dependency when evidence does not support a universal winner.
- **What are we comparing?** Define each option, its scope, shared task/workload, assumptions, and the reader's decision criteria. Avoid comparing a concept to a product implementation as though they were equivalent categories.
- **Side by side:** Compare mechanism, required assumptions, correctness/guarantees, implementation/operational cost, best use case, and failure mode. Include time and space complexity where meaningful, with defined variables. For conceptual alternatives, use a relevant cost measure and mark algorithmic complexity as not applicable.
- **Worked comparison:** Apply every option to the same input or scenario. Trace how the outcome differs. If implementations are central, use aligned semantics and the shared test contract.
- Benchmarks require a cited experiment or an actually executed reproducible setup, versions/hardware where relevant, metric, and interpretation. Never fabricate speedup numbers or compare unlike workloads.
- **Trade-offs / Edge Cases:** Include at least one case that changes the recommendation, a counterexample to a simplistic ranking, and migration/interoperability costs when they affect the decision.
- **Related notes / Sources:** Link deeper mechanism notes and primary evidence supporting disputed properties or numbers.
- Do not pad the comparison with feature rows that cannot change a real choice.
