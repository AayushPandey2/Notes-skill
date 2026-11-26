# Distributed Systems & System Design Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Failure Model
Applies to replication, partitioning, consensus, coordination, and distributed messaging. Define node count, network model (asynchrony/partial synchrony), failure model (crash-stop/partition/clock skew), and one small fixture once—never require a production-scale cluster for a single mechanism.

## Practical Realizations
1. **Manual State & Message Trace:** Hand-trace node states, logical clocks, quorum intersections (with versioning/conflict assumptions), or hash-ring key placement.
2. **Small Coordination / Service Primitive:** Implement a clean core primitive (e.g., consistent hash ring, token bucket, idempotency boundary + atomic state check).
3. **Bounded Multi-Node Simulation:** Single-process simulation illustrating replication, partitioning, or leader election transitions.
4. **Counterexamples & Failure Scenarios:** Inject partitions, stale leaders, or retry storms and **explicitly include counterexamples** showing where invariants fail—never treat one passing trace as a formal proof of safety or liveness.

## Specialized Walkthrough & Verification
Label traces **analytical / statically_reviewed** (never live-cluster **observed**) and end with **`Source and static review only; not compiled or executed here.`**
