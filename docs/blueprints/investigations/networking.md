# Computer Networking Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Fixture
Applies to network protocols, routing, transport reliability, DNS/HTTP/TLS, and diagnostics. Select **only** the parameters required by the actual protocol under study (e.g., seq/ack and window for TCP; datagram boundaries for UDP; stream IDs for QUIC; RTT/TTL for DNS)—never force unused topology variables.

## Practical Realizations
1. **Manual Packet / State Trace:** Trace headers, encapsulation, state machine transitions, or routing convergence by hand.
2. **Protocol / Timing Simulation:** Analytical or minimal scripted model of congestion window, RTT, or queueing delay.
3. **Local Socket / Handler** *(only when code adds insight)*: Minimal loopback handler illustrating framing, timeouts, or handshake state.
4. **Diagnostic, Defensive Verification & Independent Practice:** Trace packet loss, reordering, MTU fragmentation, or TLS/DNS failures alongside read-only inspection syntax (`ss`, `dig`, `tcpdump` clearly marked unexecuted) and 1–2 **Independent Exercises** (`> [!hint]-` / `> [!success]-`).

## Specialized Walkthrough & Verification
Qualify guarantees by protocol (TCP, UDP, or QUIC), honor any requested socket/handler language cleanly without unsolicited stacks, distinguish illustrative traces from supplied/published captures, and end with **`Source and static review only; not compiled or executed here.`** (or **`Manual packet and protocol trace review only (no network commands or code executed).`** when no code appears).
