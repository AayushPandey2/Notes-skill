# Claim-Level Evidence & Contradiction Intelligence

## Purpose

Verify **consequential, uncertain, or disputed claims** at the claim level rather than assuming a source supporting one aspect of a topic establishes every statement about it. Apply selectively to high-impact claims—never mechanically tag every sentence.

## 1. Internal Claim Record & Verification Dimensions

Verify internally using three distinct dimensions rather than conflating uncertainty with invalidity:
- **Claim validity:** `supported` · `contradicted` · `uncertain`
- **Evidence status:** `verified` · `partially_verified` · `unavailable`
- **Conditional applicability:** whether the hypotheses/regime under which the claim holds have been established (a claim can be both well-supported and conditional).

Record alongside them `claim_text`, `claim_type`, `assumptions`, `evidence_locators`, and `limitations`. Handle contradictions by source context rather than silently overwriting supplied sources:

| Contradiction / Source Situation | Required Treatment |
|---|---|
| **Author-generated error** | Correct the statement directly |
| **Supplied-source error** (`M2` / source notes) | Preserve accurate source attribution while identifying the error clearly |
| **Externally verified discrepancy** | Separate the source's claim from the verified correction |
| **Strict source forbids external research** | Flag internal inconsistency or uncertainty without unauthorized lookup |
| **Genuine scholarly disagreement** | Explain competing interpretations, evidence, and assumptions transparently |
| **Insufficient evidence** | Qualify scope explicitly or omit the unsupported claim |

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
