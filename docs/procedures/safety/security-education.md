# Security Education Policy

## Purpose

Enable technically rigorous, accurate cybersecurity and AI-security education within authorized and appropriately isolated environments—without weakening or evading host safety guardrails.

## Required Security-Teaching Standards

For every security topic or vulnerability class, establish:
1. **Asset and security property:** What must be protected (confidentiality, integrity, availability, authenticity, accountability).
2. **Trust boundaries and threat assumptions:** Where privilege or trust changes and what adversarial behavior is in scope.
3. **Underlying technical mechanism:** Why the vulnerability occurs at the code, protocol, or architecture level.
4. **Security impact:** Which property fails and what consequences follow.
5. **Defensive design and remediation:** How secure controls eliminate or mitigate the root cause—and what those controls do **not** solve.
6. **Authorized verification and detection:** How defenders test the control and detect regressions or misuse.
7. **Explicit scope and result status:** State clearly that examples use synthetic fixtures or isolated training targets ([experimental-lab.md](../authoring/experimental-lab.md)).

## Safe Environment & Guardrail Discipline

- **Authorized training targets only:** Prefer synthetic fixtures, intentionally vulnerable training platforms (e.g., OWASP Juice Shop, PortSwigger Web Security Academy, OWASP Web Security Testing Guide), published case studies, and defensive validation tests. Never assume educational framing authorizes testing real systems, scanning external hosts, or accessing real credentials.
- **Preservation on restriction:** When a requested offensive procedure or exploit payload is unsafe or unsupported by host safety policies, **do not** attempt to override, conceal, or evade host restrictions. Preserve all remaining legitimate technical theory, root-cause analysis, defensive implementation, remediation, and safe validation exercises.
- **No automatic execution:** Never run security tools, exploits, or credential checks against local or remote targets.
