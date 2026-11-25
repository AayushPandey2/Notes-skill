# Distributed Systems & System Design Investigation Lab Blueprint

Use this lean blueprint for Distributed Systems & System Design companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed **A–G** walkthroughs, and static review.

**Scope discipline:** Do not require a production-scale cluster to teach a single mechanism (e.g., consistent hashing or Lamport clocks); keep fixtures minimal and concrete.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Distributed Systems Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Cluster Topology & Failure Model
Define node count, network model (asynchronous/partial synchrony), failure model (crash-stop/network partition/clock skew), and one concrete request/state fixture.

## Four Distributed Systems Tracks (Apply Track-Applicability Gate)

1. **Track 1 — Manual State & Message Trace:** Trace node states, logical clocks, quorum counts, or hash-ring key placement step by step by hand.
2. **Track 2 — Small Service / Coordination Implementation:** Implement the core algorithm/coordination primitive (e.g., token bucket, consistent hash ring, idempotency key store) cleanly.
3. **Track 3 — Multi-Component Simulation:** Connect nodes/queues/replicas in a bounded single-process or minimal simulation showing replication, partitioning, or leader election.
4. **Track 4 — Failure Scenarios & Consistency Verification:** Inject packet drop, stale leader, network partition, or retry storm conceptually/statically and verify safety vs. liveness invariants.

Directly beneath each realization, include `> [!example]- Understand this realization: protocol, code, and failure dry run` covering **A–G**: **A** cluster config & assumptions; **B** safety/liveness/consistency invariant; **C** message/execution sequence; **D** step-by-step state trace across nodes; **E** linearizability/availability trade-off interpretation; **F** split-brain, duplicate non-idempotent retries, hot shards; **G** core-mechanism reconstruction.

## Verification Status

Label traces **Analytical** / **Expected** (never live-cluster **Observed**) and end with **`Source and static review only; not compiled or executed here.`**
