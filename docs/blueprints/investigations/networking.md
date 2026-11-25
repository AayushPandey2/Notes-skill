# Computer Networking Investigation Lab Blueprint

Use this lean blueprint for Computer Networking companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed **A–G** walkthroughs, and static review.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Networking Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Topology, Addressing & Packet Fixture
Define endpoints, link RTT/bandwidth/loss assumptions, protocol state variables (seq/ack numbers, window size, routing table), and one concrete message exchange.

## Four Networking Tracks (Apply Track-Applicability Gate)

1. **Track 1 — Manual Packet / State Trace:** Trace headers, encapsulation, seq/ack updates, or routing-table convergence step by step by hand.
2. **Track 2 — Protocol / Network Simulation:** Model packet timing, congestion-window evolution, or queueing delay analytically or in a small bounded script.
3. **Track 3 — Local Client/Server Implementation** *(when relevant)*: Minimal loopback socket/protocol handler demonstrating framing, timeouts, or handshake state.
4. **Track 4 — Diagnostic & Defensive Verification:** Trace packet loss, reordering, duplicate ACKs, DNS/TLS misconfiguration, and safe inspection commands (`ss`, `dig`, `tcpdump` syntax clearly labeled unexecuted).

Directly beneath each realization, include `> [!example]- Understand this realization: protocol state, trace, and dry run` covering **A–G**: **A** topology & header fields; **B** protocol state machine & reliability/routing invariant; **C** step-by-step message/execution order; **D** full timeline dry run with seq/ack or delay values; **E** throughput/latency/state interpretation; **F** packet loss, half-open state, MTU/loop failures; **G** core-protocol reconstruction.

## Verification Status

Label traces **Illustrative** / **Expected** (never live captures unless supplied); if code is present, end with **`Source and static review only; not compiled or executed here.`**
