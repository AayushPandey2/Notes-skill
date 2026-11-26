# Subject Theory Blueprint: Cybersecurity & AI Security

## Purpose

Teach cybersecurity through **security-property and trust-boundary reasoning** plus specialized reasoning patterns by subdomain, within the bounds of [security-education.md](../../procedures/safety/security-education.md).

## 1. Seven-Step Security-Property Framework

Develop major security topics through: **Asset $\to$ Trust boundary $\to$ Threat model $\to$ Vulnerability mechanism $\to$ Security impact $\to$ Defense (and its limits) $\to$ Authorized verification**.

## 2. Specialized Subdomain Reasoning Patterns

- **Cryptography:** Security goal (IND-CPA, EUF-CMA, collision resistance) $\to$ hardness/key/nonce assumptions $\to$ primitive composition $\to$ misuse/side-channel failures (nonce reuse, timing, ECB).
- **Access Control & Identity:** Principal/identity $\to$ authentication proof vs. authorization policy check $\to$ object/action enforcement boundary $\to$ privilege-escalation/IDOR/confused-deputy failure.
- **Web & Application Security:** Trust boundary between untrusted client input and interpreter/engine $\to$ parser/encoding mismatch $\to$ code-vs.-data separation (parameterized queries, contextual output encoding) $\to$ residual gaps (e.g., SQL parameterization does not fix broken authz).
- **Network & Cloud Security:** Network/IAM perimeter & segmentation $\to$ shared-responsibility boundary $\to$ least-privilege policy evaluation $\to$ misconfiguration detection.
- **Digital Forensics & Incident Response:** Volatile-to-persistent artifact preservation $\to$ chain of custody & integrity hashing $\to$ timeline reconstruction $\to$ triage, containment, eradication, recovery.
- **Security Testing & AI Security:** Explicit authorization & scope $\to$ model/tool trust boundaries (prompt injection, untrusted tool outputs, data leakage) $\to$ deterministic controls outside the LLM.

## 3. Beginner Progression, Visuals & Practice
Introduce abstract security properties through a concrete everyday trust-boundary scenario (closing underlying web, OS, or networking prerequisites inline), pair trust-boundary and attack/defense data flows with verified web-sourced reference diagrams per [representations.md](../../procedures/authoring/representations.md) (never generated/Mermaid/ASCII) or clean request-flow tables, and walk through one sanitized end-to-end threat-and-defense trace before an independent defensive threat-modeling prompt.
