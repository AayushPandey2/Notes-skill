# Verified Source Deconstruction: Article, Documentation, or Video

- **Header Block**: YAML frontmatter (`type: summary`) + `# Summary: <Source Title>`.

## 1. What source am I reviewing & what is its core thesis? (Metadata & 3-Bullet Thesis)

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

- Chronological, deep-context breakdown of the argument, examples, and technical claims:
    - **For YouTube / Video sources**: Prefix every section with a verified clickable Markdown timestamp link formatted as `[03:42](https://www.youtube.com/watch?v=VIDEO_ID&t=222s)`.
    - **For Articles / Docs**: Link directly to verified `#section-anchors` whenever the document exposes them.

## 3. Which claims hold up to independent verification? (Critical Evaluation & Fact-Check Audit)

- Distinguish the author's claims from independent technical verification using a structured table:`Claim / Practice in Source | Timestamp or Section | Independent Verification Status | Nuance, Correction, or Caveat`
- Explicitly flag commercial sponsorships, affiliate bias, deprecated API calls, outdated best practices, or unbacked assertions (`[UNVERIFIED]`).

## 4. What are my actionable takeaways & follow-up vault notes? (Actions, Reflections & Commands)

- **Key Takeaways & Immediate Actions**: Bullet list of concrete techniques or mental models to apply.
- **What I learned** (`2–3` sentences) & **Open Confusion** (`**Confusion** :: ...`).
- **Suggested Follow-Up Vault Notes (`2–3` Recommendations)**: Identify `2–3` high-leverage concepts from the source that deserve their own `Atomic` or `DeepStudy` note. Provide the project's **exact single-command invocation** to create each note, keeping them strictly as unexecuted suggestions until the user requests them.

Follow [shared authoring rules](../shared/authoring_rules.md) and the [footer contract](../shared/footer_widgets.md). Apply the math gate only at the planned level. Scaffold comments are editing slots and must be removed before publication.

> [!important] AGENT AUTHORING DIRECTIVE — `summary` Treat source fidelity as sacred: never guess or fabricate video timestamps, quotes, publication dates, or author claims. Always separate what the source _claims_ from what you can _independently verify_, flag outdated practices or sponsorships transparently, and degrade gracefully to an honest labeled partial summary whenever a transcript or page body cannot be fetched.
