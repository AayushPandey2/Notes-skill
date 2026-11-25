# Subject Theory Blueprint: Cybersecurity & AI Security

## Purpose

Teach cybersecurity through rigorous **security-property and trust-boundary reasoning** within the bounds of [security-education.md](../../procedures/safety/security-education.md).

## 1. Seven-Step Security-Property Framework

Develop major security topics through this causal chain (as interconnected reasoning, not rigid boilerplate):
1. **Asset:** What data, capability, or service requires protection?
2. **Trust boundary:** Where does control pass between untrusted and privileged contexts?
3. **Threat model:** What realistic adversary capabilities and assumptions apply?
4. **Vulnerability:** Which design assumption, validation step, or control fails?
5. **Security impact:** Which property (confidentiality, integrity, availability, authenticity) breaks?
6. **Defense:** How the remediation eliminates the root cause (and what adjacent risks it does **not** solve).
7. **Verification:** How authorized tests and monitoring confirm the control holds.

## 2. Subdomain Theory Obligations

- **Network security:** Protocol trust assumptions, segmentation, firewalls, TLS/transport security, traffic & anomaly analysis.
- **Web security:** Browser same-origin/trust model, encoding vs. sanitization, session security, CSRF/XSS/SSRF/injection root causes, access control.
- **Cryptography:** Confidentiality/integrity/authenticity properties, symmetric vs. asymmetric primitives, hashing/KDFs, nonce/IV reuse failures, key management & assumptions.
- **Application security:** Input validation, code-vs.-data separation (e.g., parameterized queries), authorization on every object/action, dependency/supply-chain hygiene.
- **Operating system security:** Privilege separation, users/groups/capabilities, filesystem permissions, sandboxing, hardening.
- **Cloud security:** Shared responsibility, IAM least privilege, policy evaluation, network/storage exposure, secret management.
- **Digital forensics & Incident response:** Evidence integrity, volatile vs. persistent artifacts, timelines, chain of custody, detection, triage, containment, recovery, lessons learned.
- **Security testing:** Written authorization, scope boundaries, reproducible findings, severity context, remediation verification.
- **AI security:** Model vs. application trust boundaries, direct/indirect prompt injection, untrusted tool outputs, training/retrieval data leakage, guardrails vs. deterministic controls.
