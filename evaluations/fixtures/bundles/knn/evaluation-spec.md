# Evaluation Specification: K-Nearest Neighbors

## Resolved artifact plan

The simulated request is a complete beginner `M1` bundle with a Python-only lab, independently authored teaching material and original supported illustrations. Deliver [theory](k-nearest-neighbors.md), [Experimental Lab](knn-experimental-lab.md), and [Cheatsheet and Interview Q&A](knn-cheatsheet-qa.md). The miniature geometry and five-case weighted examples are shared across artifacts. The lab's held-out fixture has a separate purpose and does not estimate production performance.

Compare the rewritten bundle with [the preserved original note](../../blind/knn-compressed-flawed.md) using eval 62. Keep the corresponding expected-findings file outside the model's inputs. Eval 49 tests fallback with no image capability and eval 50 isolates the weighted vote. Exact search and weighting terminology were checked against the [scikit-learn nearest-neighbors guide](https://scikit-learn.org/stable/modules/neighbors).

## Verification

Run `python evaluations/verify_knn_bundle.py` from the repository root to rerun both Python lab tracks and verify the shared fixtures. The [execution record](verification-results.json) captures observed results and file hashes. The standard-library lab ran on Python 3.11.18. The repository author visually inspected all eight raster figures, checked their inputs against the accompanying explanations and verified their local links. Live Obsidian rendering remains unverified.
