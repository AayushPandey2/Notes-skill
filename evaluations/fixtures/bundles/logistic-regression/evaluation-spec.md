# Evaluation Specification: Logistic Regression Golden Bundle

*Evaluation-only fixture metadata—do not require this file inside normal learner vaults.*

- **Simulated User Request:** `/scribe-notes Create comprehensive M1 learning notes on Logistic Regression in Python only (first principles through L2 regularization and thresholding).`
- **Routed Configuration:**
  - *Master / Subject / Knowledge Type:* `M1` (`deep-notes.md`), `machine-learning`, `mathematical` + `computational`
  - *Language Override:* Explicit Python-only (`NumPy 1.26.4` + `scikit-learn 1.4.2`, `Python 3.11`; Rust tracks intentionally omitted per request)
  - *Target Depth & Audience:* Unified Depth `Level 5` (Formal reasoning + Analytical transfer), Intermediate learner (local bridges provided for derivatives and probability odds)
- **Available Host Tools & Environment Conditions:**
  - *Code Execution:* Unavailable (`Source and static review only; not compiled or executed here.`)
  - *Visual Asset Generation / Download:* Unavailable (relying on native Markdown tables and exact mathematical characterizations; visual diagrams omitted honestly with limitations disclosed)
  - *Source Permissions:* Standard technical knowledge verified against pinned `NumPy 1.26.4` / `scikit-learn 1.4.2` objective conventions (`C = 1 / (m * lambda)` for unweighted mean BCE + $L_2$)
- **Required Artifact Roles (`artifact_plan`):**
  1. `Logistic Regression.md` (`theory`, `M1`)
  2. `Logistic Regression - Experimental Lab.md` (`experimental_lab`, `Python-only`)
  3. `Logistic Regression - Cheatsheet & Interview Q&A.md` (`mastery_pack`)
- **Verification Actually Performed:** Manual mathematical derivation review, hand arithmetic trace verification, static code review (`author-derived / manual_arithmetic / statically_reviewed`), and cross-artifact claim/notation check.
