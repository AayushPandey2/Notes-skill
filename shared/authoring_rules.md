# Shared authoring rules

- Frontmatter requires `id`, `title`, `aliases`, `type`, `area`, `base_domain`, `master_topic`, `topic`, `template`, `math_level`, `tags`, `created` (YYYY-MM-DD), `mastery`, and `revisited_date`. Include optional `depends_on`, `next_topic`, and legacy keys when required by the command. `type` and `template` match the route. Include the title and verified acronym/alternative names as aliases. Reuse exact existing tags, otherwise use kebab-case. No raw LaTeX in YAML.
- Use one named, small, concrete running example in the first applicable prerequisites/mechanism section. Keep the same values, shapes, and names through intuition, equations, behavior tables, manual traces, and runnable assertions. Define all symbols and operators before using them, including in the equation preview. Introduce prerequisites in dependency order, with meaning, shape/domain/units, and an example for each.
- Cite primary claims inline and record precise page, theorem, equation, doc section, or timestamp in the final primary-source table where the template calls for it. Label unsupported claims and unknown metrics `[UNVERIFIED]`. Keep source observations distinct from independent measurements. Never guess dates, quotations, or transcripts.
- Use `[[Exact Filename|Title]]` for existing notes or siblings in the active plan. Disambiguate basenames with a vault-relative path. Use plain text for future concepts (`(pending note)` in atomic relationships). Transclude existing atomic notes with `![[Canonical Title]]`.
- Escape every literal table pipe, even inside code or wiki aliases, as `\|`. Use native Obsidian `$...$` and `$$...$$` and keep code out of math. Use `flowchart TD` or `sequenceDiagram`, double-quote flowchart node labels, and use Unicode instead of LaTeX. Follow a diagram with 2–3 sentences tracing the mechanism.
- For verification, define one shared contract with the running example and expected result, a boundary case, and an invalid-input guard. Use 1–3 materially distinct implementations with explicit assertions, runtime/version/dependencies and execution status. Log actual observations separately from expectations. Prefer a manual check if executable code adds no evidence.

| Domain | Default verification choices |
|---|---|
| ML / deep learning | Python + NumPy, scikit-learn for classical APIs, PyTorch for tensors/autodiff |
| DSA | C++20 or Python 3, optionally Rust or Java |
| Systems / OS / concurrency | C17 or Rust, with a Python 3 simulation when useful |
| Databases / data engineering | SQL (PostgreSQL or DuckDB), Python (pandas or polars) |
| Web / distributed systems / APIs | TypeScript / Node.js or Go, with Python 3 when useful |
| Pure math / logic | Python + SymPy / NumPy or a reproducible proof/counterexample check |
