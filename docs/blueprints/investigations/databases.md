# Databases Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Schema Example
Applies to relational and non-relational databases, SQL, indexing, query plans, and transactions. Use **one tiny schema example** (3–6 rows per table) for logical correctness and transaction interleavings; **explicitly separate** published or clearly hypothetical scale/cost examples when teaching query-planner scan vs. seek cost choices (tiny tables cannot demonstrate real planner I/O cutoffs).

## Practical Realizations
1. **Data Modeling & Relational Reasoning:** Trace relational algebra, normalization, or index/storage page behavior manually on the tiny schema example.
2. **Query Implementation:** Clean, dialect/engine-identified SQL or non-relational queries with expected logical output tables.
3. **Concurrency & Isolation Trace:** Step-by-step two-session schedule under differing isolation levels (`READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`) noting engine-specific behavior.
4. **Constraints, Plans, Testing & Independent Practice:** Verify constraint enforcement, three-valued `NULL` traps, non-sargable predicates, debugging queries via `EXPLAIN` plans, and 1–2 **Independent Exercises** (`> [!hint]-` / `> [!success]-`).

## Specialized Walkthrough & Verification
State database engine and dialect assumptions, honor requested query/application stacks cleanly without unsolicited languages, distinguish a hand-derived result table from database output via shared evidence rules, and close with **`Manual relational/transaction trace review only (no database engine executed).`** (or **`Source and static review only; not compiled or executed here.`** when application code appears).
