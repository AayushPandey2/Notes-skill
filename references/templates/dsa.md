# DSA

**Purpose:** understand a problem, derive an efficient solution, justify it, and implement it in the requested language.



## Problem / Constraints

## Pattern / Key Idea

## Start with brute force

## How to improve it

## Better solution, step by step

## Code / Verification

## Edge Cases / Mistakes

## Similar problems

## Related notes / Sources

### Authoring contract

- Support at least `/scribe-dsa cpp <problem>` and `/scribe-dsa python <problem>`. Resolve the problem text from supplied content or an accessible source. If the actual problem is unavailable, request it rather than solving an invented one.
- **Problem / Constraints:** State inputs, outputs, valid domain, examples, verified constraints, and any missing information. Define `N` and other size variables. Add a constraint-to-complexity guide, qualified by time limits, hardware, constants, and language. Do not assert that a bound alone guarantees a timeout.
- **Pattern / Key Idea:** Identify the useful pattern and the problem feature that suggests it. State a central invariant or recurrence in words before notation.
- **Start with brute force:** Explain the straightforward correct approach, give complete code in the selected language, and derive time/space complexity. Quantify the bottleneck where possible. If this approach is already optimal for the given task, say so and avoid a fake optimization.
- **How to improve it:** Explain exactly which repeated work or unnecessary state is removed and why correctness is preserved. Introduce required data structures, assumptions, and trade-offs.
- **Better solution, step by step:** Explain the algorithm, its invariant/recurrence, termination, and why the result solves the stated problem. Give a proof appropriate to the technique, such as an exchange argument, induction, monotonicity, or a loop invariant. Label any claim of optimality with the computational model/justification it actually has.
- Dry-run a tricky valid input with a Markdown state table showing the relevant indices, pointers, stack/queue, DP states, or running aggregate. Use the same input in verification where useful.
- **Code / Verification:** Give the complete selected-language implementation, setup/invocation, expected results, execution status, and observed results only if run. For C++, specify the standard, integer widths, overflow reasoning, and ownership where relevant. Distinguish auxiliary space from output storage.
- Where feasible, compare brute-force and improved implementations on small valid inputs under the same contract. This supplements the correctness argument; it does not replace it.
- **Edge Cases / Mistakes:** Give 4–5 distinct valid edge-case tests with expected outputs. Use empty input only if allowed; otherwise explain the invalid-input policy separately. Include duplicates, one element, negative values, extreme bounds, ties, or overflow when relevant.
- **Similar problems:** Give 2–3 meaningful related problems. Keep each prompt visible; collapse its key twist, reasoning, and solution using native callouts. Use sourced problem links when known, and label original practice variants as original rather than claiming they are existing platform problems.
- **Related notes / Sources:** Link the pattern, prerequisite data structures, original problem, and relevant authoritative references. Never claim a specific source problem number or title without verification.
