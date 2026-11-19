<!-- scaffold:preflight
Decision-Matrix Pre-Flight: [routing index](../shared/note_decision_matrix.md) and [shared decision guide](../shared/notes_decision_matrix.md).
Switches: D01 route (`summary`); D02 single-source scope; D03 reader; D04 source synthesis & verification outcome; D05 source access + fact-check;
D06–D09 `math_level`; D10 chronological anchor/timestamp sequence; D11 fact-check table; D12–D13 independent verification; D14 optional module (`conflict`); D15 final audit.
Strip this block before emission. Load detailed DM branches only when active.
-->

# Verified Source Deconstruction: Article, Documentation, or Video

- **Header Block**: Metadata per shared contract + `# Summary: <Source Title>`.

## 1. What source am I reviewing & what is its core thesis? (Metadata & 3-Bullet Thesis)

<!-- Gate: DM-01, DM-03, DM-05.
KEEP source identity, scope, and actual access. Only summarize claims the source supports. Remove this gate before publication. -->

- `> [!info] Source Metadata & Accessibility Audit`:
    - **Title**: Exact source title
    - **Author / Channel / Organization**: Verified creator (`[UNVERIFIED]` if missing)
    - **Publication Date**: Verified date (`[UNVERIFIED]` if missing)
    - **Original URL**: Direct link
    - **Estimated Reading Time / Actual Video Duration**: Verified duration
    - **Content Access Status**: `Full Transcript / Full Article Verified` vs. `Partial Text / Metadata Only`
- _Degraded-Source Guardrail_: If the full transcript or article body is inaccessible, explicitly report what text/metadata was accessible and generate a clearly labeled **`[PARTIAL SUMMARY — TRANSCRIPT/TEXT UNAVAILABLE]`**, or ask the user to paste the text when there is too little evidence to summarize. Never hallucinate timestamps, quotes, authors, or dates.
- **The Three-Bullet Core Thesis**: Distill the central argument, mechanism, and conclusion into exactly 3 dense, high-signal bullets.

## 2. How does the material unfold section by section? (Anchored Section / Timestamp Breakdown)

<!-- Gate: DM-04, DM-05, DM-11.
KEEP the verified order and exact locators for accessible passages. State gaps and label added context. Remove this gate before publication. -->

- Chronological, deep-context breakdown of the argument, examples, and technical claims:
    - **For YouTube / Video sources**: Prefix every section with a verified clickable Markdown timestamp link formatted as `[03:42](https://www.youtube.com/watch?v=VIDEO_ID&t=222s)`.
    - **For Articles / Docs**: Link directly to verified `#section-anchors` whenever the document exposes them.

## 3. Which claims hold up to independent verification? (Critical Evaluation & Fact-Check Audit)

<!-- Gate: DM-05, DM-18, DM-19.
ADAPT the audit to claims that can be checked. Give each independent result a source or mark it unverified. Remove this gate before publication. -->

- Distinguish the author's claims from independent technical verification using a structured table:`Claim / Practice in Source | Timestamp or Section | Independent Verification Status | Nuance, Correction, or Caveat`
- Explicitly flag commercial sponsorships, affiliate bias, deprecated API calls, outdated best practices, or unbacked assertions (`[UNVERIFIED]`).

## 4. What are my actionable takeaways & follow-up vault notes? (Actions, Reflections & Commands)

<!-- Gate: DM-03, DM-19, DM-20.
KEEP applicable actions and links grounded in the source or explicitly labeled analysis. Remove this gate before publication. -->

- **Key Takeaways & Immediate Actions**: Bullet list of concrete techniques or mental models to apply.
- **What I learned** (`2–3` sentences) & **Open Confusion** (`**Confusion** :: ...`).
- **Suggested Follow-Up Vault Notes (`2–3` Recommendations)**: Identify `2–3` high-leverage concepts from the source that deserve their own `Atomic` (via `/scribe-atomic-notes <topic name>`) or `DeepStudy` note. Provide the project's **exact single-command invocation** to create each note, keeping them strictly as unexecuted suggestions until the user requests them.

<!-- optional: conflict -->
## [OPTIONAL] Where does independent evidence disagree? (Source Conflict)

<!-- Gate: DM-05, DM-19.
Include only a documented conflict. Attribute both claims and explain the comparison conditions. Remove this gate before publication. -->

<!-- scaffold:activation
Contextual Activation Guide
- When to Include: A consequential claim in the article, docs, or video conflicts with inspected primary documentation, benchmarks, or specifications; D05, D14.
- When to Omit Cleanly: Omit when Section 3's fact-check table already captures minor caveats or no substantive conflict exists. Delete this heading and block completely; never emit N/A. Renumber following sections and repair links.
- What to Write: Align definitions and conditions between the source and primary authority, quote only necessary text, pinpoint the supported disagreement, and state what remains unresolved.
-->

- **Context:** State the disputed source claim, timestamp/section, and conflicting primary authority.
- **Analysis:** Align definitions and assumptions, isolate the exact supported disagreement, and separate opinion from factual error.
- **Check:** State the primary-source verification status and any still-unverified edge condition.

See [authoring rules](../shared/authoring_rules.md) for 5-key YAML, rendering, evidence, and cohesion.
See [math gates](../shared/math_gates.md) for selected mathematical depth.
See [footer contract](../shared/footer_widgets.md) for reflection behavior.
- **Template Contract (`summary`):** Keep source claims distinct from independent verification, ensure every YouTube `[MM:SS]` timestamp matches `t=<seconds>s`, flag sponsorships/deprecated APIs, and degrade honestly to `[PARTIAL SUMMARY — TRANSCRIPT/TEXT UNAVAILABLE]` if full text is inaccessible.
