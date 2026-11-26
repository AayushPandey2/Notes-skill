# Subject Theory Blueprint: Distributed Systems & System Design

## Purpose

Teach Distributed Systems and System Design through **explicit failure assumptions, time/ordering uncertainty, replication/partitioning invariants, counterexamples, and concrete trade-offs**.

## Core Theory Obligations

1. **Failure & Network Models:** Distinguish synchronous vs. asynchronous vs. partial-synchrony assumptions, crash-stop vs. crash-recovery vs. Byzantine faults, and why physical clocks drift (comparing physical vs. Lamport/vector logical clocks and message histories).
2. **Replication & Consistency (Qualify Quorum Guarantees):** Contrast leader-follower, multi-leader, and leaderless/quorum designs. **Never claim $R + W > N$ alone guarantees linearizability or strong consistency**—explicitly explain quorum intersection alongside version vectors/timestamps, conflict resolution, read repair/sloppy quorums, and protocol assumptions. Distinguish **CAP/PACELC** trade-offs, linearizability, sequential consistency, causal consistency, and eventual consistency, using counterexamples where guarantees fail.
3. **Partitioning & Coordination:** Explain key-range vs. hash vs. consistent hashing, hot-shard mitigation, rebalancing, consensus intuition (Raft/Paxos safety vs. liveness under FLP/partitions), and distributed locks/leases (fencing tokens).
4. **Reliability & Messaging (Qualify Effectively-Once):** Contrast at-most-once, at-least-once, and **effectively-once** processing—explicitly explaining atomicity, deduplication window/storage boundaries, retry storms, and idempotent side effects rather than attributing end-to-end safety to an idempotency key alone. Cover backpressure, circuit breakers, exponential backoff + jitter, and dead-letter queues.
5. **System Design Grounding:** Connect throughput, tail latency ($p_{95}/p_{99}$), storage/bandwidth back-of-the-envelope constraints, and bottleneck migration without hand-waving.
6. **Beginner Progression, Visuals & Practice:** Open abstract consistency or impossibility proofs with a concrete 2–3 node message-delay scenario (closing networking/storage prerequisites inline), pair ordering, replication, and partitioning flows with verified web-sourced protocol diagrams per [representations.md](../../procedures/authoring/representations.md) (never generated/Mermaid/ASCII) or timeline trace tables, and walk through one counterexample schedule before an independent fault-analysis exercise.
