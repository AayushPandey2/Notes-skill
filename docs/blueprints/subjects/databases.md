# Subject Theory Blueprint: Databases

## Purpose

Teach Databases through **relational foundations, storage/indexing mechanics, query execution, and transaction concurrency** rather than reducing database theory to a SQL syntax list.

## Core Theory Obligations

1. **Data Modeling & Relational Algebra:** Ground SQL queries in relations, tuples, keys, foreign-key integrity, normalization (1NF–BCNF/anomalies vs. denormalization trade-offs), and relational algebra operators.
2. **Storage & Indexing:** Explain pages/slotted storage, B+ tree vs. hash vs. LSM-tree trade-offs, clustered vs. secondary indexes, selectivity, and write amplification.
3. **Query Execution & Optimization:** Trace logical evaluation order (`FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY`), scan vs. seek vs. join algorithms (nested loop, hash, sort-merge), and reading `EXPLAIN` plans.
4. **Transactions, ACID & Isolation:** Distinguish atomicity, consistency, isolation, and durability; trace dirty/non-repeatable/phantom reads and write skew across isolation levels, MVCC vs. locking, and WAL recovery.
5. **Common Pitfalls:** Address three-valued `NULL` logic, `COUNT(*)` vs. `COUNT(col)`, index-invalidating predicates, and N+1 queries.
