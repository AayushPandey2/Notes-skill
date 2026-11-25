# Databases Investigation Lab Blueprint

Use this lean blueprint for Relational & Storage Databases companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed **A–G** walkthroughs, and static review.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Databases Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Schema & Tiny Table Fixture
Use **one consistent small relational schema** (3–6 rows per table) across tracks so joins, indexes, and transaction interleavings are verifiable by hand.

## Four Database Tracks (Apply Track-Applicability Gate)

1. **Track 1 — Relational Reasoning & Representation:** Trace relational algebra, functional dependencies/normalization, or B+ tree page splits manually on the tiny fixture.
2. **Track 2 — SQL Implementation:** Author clean, dialect-identified SQL (`DDL`, queries, constraints, indexes) with expected result tables.
3. **Track 3 — Transaction & Isolation Demonstration:** Trace two concurrent sessions step by step under differing isolation levels (`READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`).
4. **Track 4 — Constraints, Query Plans & Correctness Testing:** Analyze `EXPLAIN` scan choices (seq vs. index scan), constraint violations, dirty/phantom reads, and NULL three-valued logic traps.

Directly beneath each realization, include `> [!example]- Understand this implementation: schema, query, and execution dry run` covering **A–G**: **A** schema, constraints, row fixture; **B** relational/storage/concurrency invariant; **C** logical query evaluation order (`FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY`) or transaction schedule; **D** exact row-by-row dry run; **E** output & plan cost interpretation; **F** NULL traps, missing indexes, write skew/deadlocks; **G** core-concept reconstruction.

## Verification Status

Label query results **Hand-calculated** / **Expected** (never **Executed**) and end with **`Source and static review only; not compiled or executed here.`**
