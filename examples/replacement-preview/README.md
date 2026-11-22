# Scriptorium Replacement Architecture Preview Collection

> **Isolation Notice:** Generated in a dedicated preview directory (`examples/replacement-preview/`). Original notes under `Notes Vault\6 - Full Notes\6 - Full Notes\Supervised Learning` were read-only inputs and remain bit-for-bit untouched.

## Verified Live Raster Web-Image Acquisitions

| Key | Local Asset Path | Format & Size | License | SHA-256 (12-char) | Source Page |
|---|---|---|---|---|---|
| `ols_geom` | `assets/scriptorium/supervised-learning-preview/least-squares-projection-bd92be15b65c.png` | `image/png` (`2000x2000`) | CC BY-SA 4.0 | `bd92be15b65c` | https://commons.wikimedia.org/wiki/File:Least_squares_projection_geometry.png |
| `loss_cmp` | `assets/scriptorium/supervised-learning-preview/comparison-of-loss-functions-8e57447d079c.png` | `image/png` (`1545x811`) | CC BY-SA 4.0 | `8e57447d079c` | https://commons.wikimedia.org/wiki/File:Comparison_of_loss_functions.png |
| `sigmoid` | `assets/scriptorium/supervised-learning-preview/sigmoidal-curves-2ad05db99108.jpg` | `image/jpeg` (`826x509`) | CC BY 4.0 | `2ad05db99108` | https://commons.wikimedia.org/wiki/File:Quatre_fonctions_sigmo%C3%AFdes_%E2%80%94_four_sigmoidal_functions.jpg |
| `bias_var` | `assets/scriptorium/supervised-learning-preview/bias-variance-decomposition-78e1dbbf12de.png` | `image/png` (`1000x600`) | CC BY-SA 4.0 | `78e1dbbf12de` | https://commons.wikimedia.org/wiki/File:Bias-variance_decomposition.png |

## Before vs. After Teaching Improvements (Original vs. Replacement Preview)

1. **Preview 1 (Scalar Prediction & Non-Square Matrices):**
   - *Before (`03 - Linear Regression.md` L18–L20, L43–L49, L117):* Repeated `# Linear Regression` and `## Linear Regression`, ran rapidly through quadratic expansion to $(X^\top X)^{-1} X^\top \mathbf{y}$ without a fold under any equation, placed its SVG *after* Python code, and omitted collinearity qualification on scaling (`L75–L77`).
   - *After (`01 - Scalar Prediction and Non-Square Matrix Regression.md`):* Clean single H1 title, scalar $\hat{y}=wx+b$ intuition first, verified downloaded projection PNG embedded **before** code via `Explain -> Show -> Decode -> Connect`, explicit $(3\times 2)(2\times 1)$ vs. invalid $(1\times 2)(3\times 2)$ shape check inside folded `> [!example]-` callouts, and explicit scaling qualification.
2. **Preview 2 (Loss Functions & Numerical Comparison):**
   - *Before (`02 - Loss Functions.md` L29–L32, L105):* Introduced $R(h)$ expectation and $R_{\text{emp}}$ in rapid succession with all folds delayed to chapter end.
   - *After (`02 - Loss Functions and Outlier Sensitivity.md`):* Live Wikimedia loss-comparison PNG introduced before piecewise formulas, plus individual `> [!example]-` folds explaining summation indexing and concrete $r=3$ ($2.5$ vs. $9$) and $r=20$ ($19.5$ vs. $400$) outlier scaling.
3. **Preview 3 (Logistic Chain Rule & Bounded Loss Fix):**
   - *Before (`04 - Logistic Regression.md` L65, L155):* Compressed BCE chain rule into one multi-step line and misstated in `L155` that cross-entropy decreases *'without bound'*.
   - *After (`03 - Logistic Regression Chain-Rule Derivation.md`):* Live Wikimedia sigmoid JPEG, chain rule split into $\partial L/\partial \hat{p}$ then $\partial L/\partial z = \hat{p}-y$ cancellation folds, and assessment fold correcting the lower bound ($J \to 0$ while $\|\mathbf{w}\|_2 \to \infty$).
4. **Preview 4 (Bias–Variance Randomness):**
   - *Before (`06 - Bias-Variance Tradeoff.md` L38–L49, L88):* Used expectation notation $\mathbb{E}_{\mathcal{D},\varepsilon}$ with step labels and post-example SVG.
   - *After (`04 - Bias-Variance Decomposition and Randomness.md`):* Live Wikimedia bias-variance PNG placed at motivation and folded walkthrough explicitly naming random draw $\mathcal{D}$ vs. test noise $\varepsilon$ inside $\mathbb{E}$.
5. **Preview 5 (Ridge Conventions & Scaling):**
   - *Before (`07 - Regularization.md` L26, L29, L64, L84):* Changed from averaged loss $1/n$ (`L26`) to unnormalized sum (`L64`), conflicted with intercept absorption (`03` L28) vs. unpenalized bias (`07` L29), and ran an uncentered 1D example (`L84`) right after centered-data derivation (`L64`).
   - *After (`05 - Ridge Regularization Conventions and Scaling.md`):* Explicit penalty mask $I_0 = \operatorname{diag}(0,1,\dots,1)$, exact $\lambda_{\text{sum}} = n\lambda_{\text{avg}}$ scaling formula+fold, and explicit uncentered trace callout.
6. **Preview 6 & 7 (Video Adapter Demos):**
   - Demonstrates `/scribe-ytnotes` and `/scribe-ytlecture` unified routing with **labeled fixture frames** preserving intermediate step states (since `ffmpeg`/`yt-dlp` are absent on host), honest `transcript_only` limitation + preserved `[uncertain: ...]` marker, and `metadata_only` blocking fabricated lecture notes.
