# Subject Theory Blueprint: Distributed Systems & System Design

## Purpose

Teach Distributed Systems and System Design through **partial failure, time/ordering uncertainty, replication/partitioning invariants, and explicit trade-offs**.

## Core Theory Obligations

1. **Failure & Network Models:** Distinguish synchronous vs. asynchronous vs. partial-synchrony assumptions, crash-stop vs. crash-recovery vs. Byzantine faults, and why clocks drift (physical vs. Lamport/vector logical clocks).
2. **Replication & Consistency:** Contrast leader-follower, multi-leader, and leaderless/quorum ($R + W > N$) designs; distinguish **CAP/PACELC** trade-offs, linearizability, sequential consistency, causal consistency, and eventual consistency.
3. **Partitioning & Coordination:** Explain key-range vs. hash vs. consistent hashing, hot-shard mitigation, rebalancing, consensus intuition (Raft/Paxos safety vs. liveness), and distributed locks/leases.
4. **Reliability & Messaging:** Teach at-most-once, at-least-once, and effectively-once (idempotency keys) semantics, backpressure, circuit breakers, retries with exponential backoff + jitter, and dead-letter queues.
5. **System Design Grounding:** Connect throughput, tail latency ($p_{95}/p_{99}$), storage/bandwidth back-of-the-envelope constraints, and bottleneck migration without hand-waving.
