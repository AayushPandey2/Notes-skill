# Subject Theory Blueprint: Databases

## Purpose

Teach Databases across **relational and non-relational data models, storage/indexing mechanics, query execution, and transaction concurrency**—qualifying storage and isolation behavior by database engine rather than treating SQL syntax as database theory.

## Core Theory Obligations

1. **Data Models & Relational Foundations:** Ground SQL queries in relations, tuples, keys, foreign-key integrity, normalization (1NF–BCNF/anomalies vs. denormalization trade-offs), and relational algebra. Where applicable, cover **non-relational models** (document, key-value, wide-column, graph) and when access-pattern locality justifies their trade-offs.
2. **Storage & Indexing (Engine-Qualified):** Explain pages/slotted storage, B+ tree vs. hash vs. LSM-tree trade-offs, clustered vs. secondary indexes, selectivity, and write/read/space amplification—qualifying engine-specific mechanics (e.g., PostgreSQL heap+MVCC vs. InnoDB clustered B+ tree vs. RocksDB LSM).
3. **Query Execution & Optimization:** Trace logical SQL evaluation order (`FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY`), scan vs. seek vs. join algorithms (nested loop, hash, sort-merge), and reading `EXPLAIN` plans.
4. **Transactions, ACID & Isolation:** Distinguish atomicity, consistency, isolation, and durability; trace dirty/non-repeatable/phantom reads and write skew across isolation levels (`READ COMMITTED`, `REPEATABLE READ`/Snapshot Isolation, `SERIALIZABLE`), MVCC vs. 2PL locking, and WAL crash recovery—noting engine-specific snapshot behavior.
5. **Common Pitfalls:** Address three-valued `NULL` logic, `COUNT(*)` vs. `COUNT(col)`, non-sargable predicates breaking index use, and N+1 queries.
6. **Beginner Progression, Visuals & Practice:** Ground schema, indexing, and concurrency mechanics in a tiny concrete table and workload (closing disk-I/O or relational prerequisites inline), pair B+ tree/LSM/MVCC layouts with verified web-sourced storage diagrams per [representations.md](../../procedures/authoring/representations.md) (never generated/Mermaid/ASCII) or compact version-chain traces, and trace one concrete `EXPLAIN` or two-transaction schedule before an independent diagnostic question.
