# Subject Theory Blueprint: Computer Networking

## Purpose

Teach Computer Networking as **layered protocol responsibilities, transport-specific state models, encapsulation, addressing, and diagnostic reasoning** rather than isolated acronym lists or generalizing TCP to every transport.

## Core Theory Obligations

1. **Layered Encapsulation & Addressing:** Trace how application payloads are framed through transport, network (IPv4/IPv6, CIDR, longest-prefix routing, NAT), and link (MAC/ARP/switching, wireless CSMA/CA & interference differences) layers, distinguishing port, IP, and link-layer addresses.
2. **Protocol-Specific Transport Guarantees:** Contrast **TCP** (byte-stream, connection state, seq/ack, sliding window, loss/congestion control), **UDP** (unreliable datagrams, minimal framing, application-level reliability), and **QUIC** (UDP-based multiplexed streams without TCP head-of-line blocking, integrated TLS 1.3)—never generalizing one protocol's behavior across all transports.
3. **Latency, Bandwidth & Path Dynamics:** Distinguish propagation delay, transmission delay, queueing delay, bandwidth-delay product, and packet loss.
4. **Application & Security Protocols:** Explain DNS resolution/caching/TTL, HTTP/1.1 vs. HTTP/2 vs. HTTP/3, and TLS handshake trust/certificate/encryption guarantees.
5. **Layered Failure & Diagnosis:** Trace packet loss, reordering, duplicate ACKs, asymmetric routing, MTU fragmentation, wireless drops, and DNS/TLS failures systematically across layers.
6. **Beginner Progression, Visuals & Practice:** Open protocol mechanics with a concrete end-to-end packet journey (closing binary/CIDR or socket prerequisites inline), pair encapsulation, handshakes, and congestion windows with verified web-sourced protocol diagrams per [representations.md](../../procedures/authoring/representations.md) (never generated/Mermaid/ASCII) or step-by-step sequence tables, and include one worked numerical or packet-trace example (e.g., CIDR, BDP, or seq/ack recovery) before an independent fault-diagnosis prompt.
