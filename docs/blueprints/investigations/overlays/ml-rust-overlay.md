# Conditional Overlay: ML in Rust (Explicit Opt-In Only)

- **Load:** ONLY when the user explicitly requests Rust in an ML lab/implementation. **Do NOT load** on default Python requests, wording like *"performance/production/optimization/advanced"*, or explicit non-Rust languages (e.g., C++).
- **Parents:** [machine-learning.md](../machine-learning.md), [experimental-lab.md](../../../procedures/authoring/experimental-lab.md).

## Rust Track Obligations (Alongside Active A–G Tracks)
1. **Rust from Scratch:** Teach explicit types, ownership/borrowing, `&[f64]` slices, numeric casts, tie/error handling (`Result`/`Option`), and sequential vs. simultaneous updates.
2. **Ecosystem (`linfa` / `smartcore`):** Verify crate versions, feature flags, matrix types, fit/predict APIs, and error handling against `docs.rs` when permitted; otherwise mark unverified APIs `[UNVERIFIED]` without inventing signatures.
3. **Equivalence Table (Multi-Language):** When paired with Python (or another requested language), compare parameters, objective/scaling conventions, tie handling, and numerical tolerances—adding zero unrequested languages.
4. **Non-Execution:** Keep all Rust code in Markdown fences only (`Source and static review only; not compiled or executed here.`).

