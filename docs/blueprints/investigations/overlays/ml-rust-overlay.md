# Conditional Language Overlay: Machine Learning in Rust (Explicit Opt-In Only)

## When to Load

Load this overlay **only** when the user explicitly requests Rust for a Machine Learning implementation, experimental lab, or comparison (e.g., *"Implement KNN in Rust"*, *"compare Python and Rust"*).

## When NOT to Load

- Never load on default Python Machine Learning requests.
- Never infer Rust activation from wording about *"implementation"*, *"optimization"*, *"performance"*, *"production readiness"*, or *"advanced experiments"*.
- Never load on explicit non-Rust language requests (e.g., C++ or Python-only).

## Required Parent Policies

- [machine-learning.md](../machine-learning.md) (shared ML fixture, hand-trace, and numerical static-verification rules)
- [experimental-lab.md](../../../procedures/authoring/experimental-lab.md) (shared structure, YAML, A–G deduplication, 3-attribute experiment integrity, and non-execution rules)

## Additional Rust Obligations

Apply these requirements alongside the active Tracks in [machine-learning.md](../machine-learning.md) **without omitting** shared A–G walkthroughs, baseline comparisons, or failure analyses:

1. **Rust from Scratch:** Teach explicit types, ownership/borrowing, slices (`&[f64]`), explicit numeric casts (`as f64`, `usize`), tie-handling and error handling (`Result`/`Option`), and sequential vs. simultaneous state updates.
2. **Rust Ecosystem Libraries (`linfa` / `smartcore`):** Check crate versions, feature flags, dataset matrices (`ndarray` / `DatasetBase` / `DenseMatrix`), fit/predict methods, and error handling against official `docs.rs` documentation when `source_policy` permits web research; when unverified or under restricted sources, mark API details honestly as `[UNVERIFIED]` without inventing methods or crate signatures.
3. **Multi-Language Equivalence Table (When Paired with Python or Another Language):** Include a compact Equivalence Table comparing parameter names, objective/scaling conventions, index/tie handling, and numerical tolerances across requested languages, adding no languages beyond those requested.
4. **Static Review & Non-Execution Boundary:** Never compile Cargo crates, write Rust project files to disk outside instructional Markdown fences, or execute tests. End with **`Source and static review only; not compiled or executed here.`**
