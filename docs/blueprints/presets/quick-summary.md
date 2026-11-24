<!-- scaffold:preflight
Purpose: Produce source-faithful, locator-anchored summaries of articles, documentation, or videos while auditing claims independently.
Parent Master: M7 (../formats/synthesis-revision.md) | Route: summary (variant: quick_summary).
Activation Trigger: "summarize <source/URL/video>", standalone article/docs/video URL, or /scribe-ytnotes single-video summary.
Inputs: Accessed article text, docs page, or video transcript/frames; source URL, author, date, and verified access scope.
Dependencies: router.md, core/authoring_rules.md, core/math_gates.md, procedures/sourcing/source-fidelity.md.
Decision Rules: Separate source claims from independent verification; link video entries via verified `` `[MM:SS](https://www.youtube.com/watch?v=<VIDEO_ID>&t=<seconds>s)` `` timestamps; suggest 2–3 follow-up notes passively.
Failure Handling: Never hallucinate timestamps or missing text; mark unavailable full bodies '[PARTIAL SUMMARY — TRANSCRIPT/TEXT UNAVAILABLE]' or request user paste.
Validation: [verification-checklist.md](../../procedures/review/verification-checklist.md).
-->

# Verified Source Deconstruction: Article, Documentation, or Video

- **Header Block:** Line-1 YAML Properties + `# Summary: <Source Title>`.

## 1. What source am I reviewing & what is its core thesis? (Metadata & 3-Bullet Thesis)

- `> [!info] Source Metadata & Accessibility Audit`: Title, Author/Channel (`[UNVERIFIED]` if absent), Publication Date, Original URL, Duration/Reading Time, and **Content Access Status** (`Full Transcript / Article Verified` vs. `Partial Text / Metadata Only`).
- **Degraded-Source Guardrail:** If full text/transcript is inaccessible, disclose access limits clearly under **`[PARTIAL SUMMARY — TRANSCRIPT/TEXT UNAVAILABLE]`**.
- **Three-Bullet Core Thesis:** Distill central argument, mechanism, and conclusion cleanly.

## 2. How does the material unfold section by section? (Anchored Section / Timestamp Breakdown)

Walk chronologically through arguments, examples, and claims:
- **Videos:** Prefix sections with verified `` `[MM:SS](https://www.youtube.com/watch?v=<VIDEO_ID>&t=<seconds>s)` `` links matching exact seconds.
- **Articles / Docs:** Anchor links to verified `#section-headings`.

## 3. Which claims hold up to independent verification? (Critical Evaluation & Fact-Check Audit)

Contrast source statements against independent verification:
`Claim / Practice in Source | Timestamp or Section | Independent Verification Status | Nuance, Correction, or Caveat`
Flag sponsorships, affiliate bias, deprecated APIs, or unsupported claims (`[UNVERIFIED]`).

## 4. What are my actionable takeaways & follow-up vault notes? (Actions, Reflections & Commands)

- **Key Takeaways & Immediate Actions**, **What I learned**, and **Open Confusion** (`**Confusion** :: ...` when real).
- **Suggested Follow-Up Vault Notes (`2–3`):** Propose unexecuted `/scribe-notes` suggestions for concepts worth dedicated `atomic` or `deep-notes` pages.

<!-- optional: conflict -->
## [OPTIONAL] Where does independent evidence disagree? (Source Conflict)

<!-- Include only when an authoritative specification or benchmark directly contradicts a material claim; delete cleanly otherwise. -->

- **Context / Analysis / Check:** Disputed claim, conflicting primary source, condition alignment, and verification status.

- **Contract Summary:** Verify timestamp parity, honest access flags, and [authoring_rules.md](../../../core/authoring_rules.md) / [math_gates.md](../../../core/math_gates.md) / [footer_widgets.md](../../../core/footer_widgets.md).
