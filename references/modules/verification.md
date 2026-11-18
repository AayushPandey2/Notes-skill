# Verification contract

- Define a **Selected verification stack** and **Shared test contract** before multiple implementations.
- Use the same named running-example inputs, expected outputs, a valid boundary/degenerate case, and an invalid-input guard where one is meaningful. Preserve corresponding variable names across implementations as far as language/API constraints permit.
- Explain differences in layout, dtype, padding, indexing, reduction, mutation, or defaults before comparing outputs. Do not claim parity for different operations.
- Include complete runnable code with imports/includes, dependencies, invocation, and representative input. Explain tensor shape changes or memory/ownership transitions beside the relevant operations.
- State expected output separately from observed output. Set execution status to **not executed** unless the code was actually run. An unavailable runtime is a verification limit, not permission to fabricate results.
- State numerical tolerance, precision, stability, seed, and device when they materially affect the comparison. Do not make nondeterministic results look exact.
- Define input-size variables for time and space complexity. Distinguish auxiliary space, output storage, and relevant allocations. A complexity claim needs its assumptions.
- Explain what the checks establish and what they do not prove. A few passing tests do not establish a theorem or production readiness.
- For non-code topics, use a reproducible worked analysis, evidence comparison, trace, or counterexample instead of compulsory code.
