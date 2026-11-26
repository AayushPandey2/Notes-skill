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
  1. `logistic-regression.md` (`theory`, `M1`)
  2. `logistic-regression-lab.md` (`experimental_lab`, `Python-only`)
  3. `logistic-regression-mastery.md` (`mastery_pack`)
- **Simulated author verification:** Manual mathematical derivation review, hand arithmetic trace verification, static code review (`author-derived / manual_arithmetic / statically_reviewed`), and cross-artifact claim/notation check.

**Repository verification:** Run `python evaluations/verify_logistic_bundle.py` from the repository root under the pinned environment to execute all three lab tracks and the independent regression checks. [Recorded numeric results and file hashes](verification-results.json) cover input validation, stopping status, gradient stability, solver agreement and held-out scores. The validator also checks that visible text is separated from callouts. Live Obsidian rendering was verified on the earlier 21-fold revision (`4b74e96`); rendering for this revision remains unverified.
