# Claim-Level Evidence & Contradiction Intelligence

## Purpose

Verify **consequential, uncertain, or disputed claims** at the claim level rather than assuming a source supporting one aspect of a topic establishes every statement about it. Apply selectively to high-impact claims—never mechanically tag every sentence.

## 1. Internal Claim Record & Verification Dimensions

Verify internally: `claim_text`, `claim_type`, `assumptions`, `evidence_locators`, `limitations`, and `verification_status` (`supported`, `conditional`, `disputed`, `contradicted`, `insufficient_evidence`, or `[UNVERIFIED]`).
- **`contradicted`** by inspected evidence requires **correction**.
- **`insufficient_evidence`** requires **qualification or omission**.

Check three evidence dimensions alongside claim type:
1. **Evidence sufficiency:** Does the source actually establish the exact claim (e.g., explaining Adam does not establish that Adam always beats SGD)?
2. **Evidence independence:** Do not treat multiple pages echoing the same secondary claim as independent corroboration.
3. **Evidence freshness:** Distinguish timeless mathematical theorems from version-sensitive library/API/standard claims.

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

Whenever two sources or notes disagree during authoring, classify the discrepancy before writing: **notation difference**, **different assumptions**, **software/library version difference**, **distinct algorithm/model variant**, **methodology difference**, or **genuine unresolved question**. Explain transparently instead of blending incompatible claims.
