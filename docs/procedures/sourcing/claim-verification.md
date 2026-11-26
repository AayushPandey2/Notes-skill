# Claim-Level Evidence & Contradiction Intelligence

## Purpose

Verify **consequential, uncertain, or disputed claims** at the claim level rather than assuming a source supporting one aspect of a topic establishes every statement about it. Apply selectively to high-impact claims—never mechanically tag every sentence.

## 1. Internal Claim Record & Evidence Standards

For high-consequence or uncertain claims, verify internally: `claim_text`, `claim_type`, `assumptions`, `evidence_locators`, `limitations`, and `verification_status` (`supported`, `conditional`, `disputed`, or `[UNVERIFIED]`). Match evidence to the claim type:

| Claim Type | Appropriate Verification Evidence |
|---|---|
| **Mathematical theorem** | Valid proof and exact hypotheses |
| **Software API / version** | Official version-specific documentation (when `source_policy` permits) |
| **Statistical property** | Derivation or authoritative statistical reference |
| **Empirical superiority** | Comparable published experiments with matched baselines & uncertainty |
| **Historical claim** | Primary or peer-reviewed scholarly evidence |
| **Scientific mechanism** | Established scientific evidence and validity regime |
| **Security property** | Threat assumptions and authorized defensive validation |
| **Engineering guarantee** | Applicable standards, component models, and operating limits |

## 2. General Contradiction-Resolution Intelligence

Whenever two sources or notes disagree during authoring (not only in `M7` comparisons), classify the discrepancy before writing: **notation difference**, **different assumptions**, **software/library version difference**, **distinct algorithm/model variant**, **methodology difference**, or **genuine unresolved question**. Explain the discrepancy transparently instead of silently blending incompatible claims.
