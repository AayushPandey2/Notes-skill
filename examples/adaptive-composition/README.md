# Reproducible composition demonstration

Run `python examples/adaptive-composition/run.py` from the repository root.
Only Python, PyYAML and the repository are required. The example builds and
publishes a six-file collection about gradient descent on quadratic objectives,
executes its numerical implementation, generates scientific SVG curves and a
Transformer attention architecture SVG, and records measured contract sizes and
execution times in `measurements.json`. Assets go in `vault/assets/`.

The authored collection is a focused teaching demonstration, not a comprehensive
textbook on every optimization method. Its mathematics is derived directly from
the stated quadratic model. No generated measurements represent real experiments.
Source pointers and their verification scope are recorded in `sources.json`.

`scenarios.json` exercises gradient descent, Transformers, quantization, operating
systems, a shared research collection, and a narrow definition. These are contract
and selection demonstrations; the latter topics are not fully authored textbooks.
No model calls, live retrieval benchmark, or pedagogical-quality score is claimed.
The measurements compare actual serialized capability bytes and deterministic
operations; model-token counts are unavailable. Existing optimizer benchmarks are
separate estimator-based workloads, not live model measurements.
