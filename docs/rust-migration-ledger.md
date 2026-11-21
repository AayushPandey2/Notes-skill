# Rust migration evidence and parity gates

This ledger covers the Python reference implementation before removal. The machine-readable [inventory](rust-migration-inventory.json) includes all tracked Python files: AST function inputs and return annotations, purpose, static callers and dependencies, exception handlers, filesystem and subprocess/network call sites, test references, removal decisions and parity status. Static reachability does not prove a function is unused. Missing annotations and dynamic imports require fixture review.

Python remains required for behaviors whose Rust replacements have not passed semantic and regression parity checks. A Rust asset subsystem alone does not establish parity for the complete note-generation architecture. The inventory marks these entries pending until test evidence is attached. Example and educational code are retained independently of runtime migration.

## Baseline

Reference commit is recorded in the inventory. On Windows 11, Python 3.14.7:

- `python -m pytest -q`: **564 passed in 111.90 seconds**.
- `python -m unittest discover -s tests -v` discovers no tests because the suite uses pytest functions. Use pytest.
- `python tests/parity_capture.py`: records seven measured samples after one warmup for local deterministic operations in [the baseline](rust-migration-python-baseline.json).

Recorded CLI medians are 326.19 ms for startup plus `--help`, 366.00 ms for Properties generation and 357.95 ms for routing. These include interpreter startup and import overhead. Frontmatter parse is 0.424 ms, metadata validation 0.459 ms and scientific SVG render plus validation 0.354 ms. Values are environment-specific observations. They are not model reasoning, network or end-to-end generation measurements. The filesystem sample is buffered write/read, not durable atomic publication. The development environment had other work active; rerun both language implementations in isolation for a fair performance comparison. No Rust speedup is established by this report.

Only the third-party `yaml` package is imported by the audited runtime (PyYAML). Scientific rendering already uses standard-library deterministic SVG; no maintained runtime imports NumPy, Matplotlib or SymPy. Educational examples and requested learner stacks can still contain Python. The verification subsystem optionally invokes external language runtimes to check educational code; this capability must be explicit, with no Python bootstrap dependency in a completed Rust runtime.

## Ownership and replacement strategy

| Python file(s) | Existing input/output and responsibility | Rust strategy and acceptance evidence needed |
|---|---|---|
| `scriptorium/models.py` | Text/bytes, YAML and note sections → typed metadata, sections, hashes; shared errors and stack aliases | Shared types, duplicate-key-rejecting YAML, SHA-256, normalized stack aliases; malformed YAML, Unicode, duplicate keys, custom metadata and hash fixtures |
| `scriptorium/layout.py` | Template/note aliases → canonical type, required sections and skeleton | Load canonical registry once; preserve all layout aliases and optional sections across seven masters |
| `scriptorium/__init__.py`, `engines/__init__.py` | Public package/export boundaries | Rust library exports and documented migration API; no Python shim in maintained Rust execution |
| `engines/orchestration.py` | Request/preferences/registry → route, locks, context and execution plans; source-policy and instruction-authority gates | Typed request/route/source-policy contracts; M1–M7, scope S0–S5 and explicit constraints fixtures; preserve token and lifecycle integration |
| `engines/_decision.py` | Request, source and study options → locked decisions | Pure decision module; cross-domain, explicit override, contradictory request and syllabus boundary fixtures |
| `engines/_interactive.py` | Request/reply + vault/session ID → state transitions, questions, preview and collection plan | Serializable session state machine; reject invalid transitions; source sections and approved preference persistence; avoid pre-generation diagnostic quizzes |
| `engines/_collection_intelligence.py` | Collection plan, evidence, vault reuse and feedback → KCP F02–F15, batches, assessments, synthesis and impact plans | Versioned KCP and dependency graph, checkpoint/reuse/repair states; all existing lifecycle fixtures and safe resumed generation |
| `engines/knowledge.py` | Concept/alias/claim/change records → identities, coverage, uncertainty and impact graph | Typed domain-aware identity registry, evidence/uncertainty enums, graph traversal; homonym, contradiction and source-only enforcement fixtures |
| `engines/research.py` | Concepts, source metadata, evidence and policies → ARRIE requirements, queries, coverage and citations | Preserve deterministic research policy evaluation separately from async retrieval; provenance and independence contracts; no fabricated fetched evidence |
| `engines/pedagogy.py` | Plans/concepts → instructional and composition facade, gap/detail/example allocation | Composition and pedagogy services; preserve shared policy authority and all public contracts |
| `engines/_instructional.py` | Adaptive raw plan → normalized Contract v3, DAG, sequence, coverage findings | Typed planner and explicit legacy adapter; malformed plans, missing prerequisites and activation matrix fixtures |
| `engines/_pedagogical_core.py` | Concept/example/representation/revision records → P01–P11 plans and quality findings | Restricted mathematical expression evaluation and pedagogical validators; units, shape, numerical trace and executable example fixtures |
| `engines/_explanation.py` | Topic/audience/master/source policy → EIS blueprint, explanatory prose and trace checks | Preserve EIS-01–07 activation, clarity and audience/source order; structural and semantic parity rather than identical AI prose |
| `engines/_token_optimizer.py` | Dependencies, user scope, source segments, KCP and prompt bundle → cache/IR/context/repair output | Content-addressed versioned cache with TTL, dependency invalidation, privacy isolation and secret rejection; compact context and coverage parity |
| `engines/quality.py` | Markdown/plans/repository tree → quality issues, repair, golden evaluation and audits | Unified structured issue reports and selective verification; repository Markdown/CLI references must still resolve after migration |
| `engines/_verification.py` | Fenced educational code and runtime choices → compiled/executed evidence and trace findings | Explicit external tool adapters with bounded subprocess execution; do not execute examples as part of parsing; retain educational Python support as optional external tool |
| `engines/vault.py` | Properties/note patches/vault path → normalized metadata, preserved custom fields, atomic writes and publication | YAML/section model, taxonomy and conflict-aware atomic writer; preserve custom metadata, no-op byte stability, date handling and rollback semantics |
| `engines/_composition.py`, `_composition_visuals.py` | Legacy import paths → canonical composition modules | Remove compatibility aliases only after all callers use canonical Rust services and old regression paths are accounted for |
| `engines/composition/__init__.py` | Composition spec/drafts/evidence/reviews → chapter plan, embeds, receipts, selective context, published manifest | Typed composition service with artifact-bound reviews, source evidence and critical obligation gates; publication with all assets delivered |
| `engines/composition/planning.py` | Concept prerequisite graph → adaptive 5–10 chapters and workload rationale | Deterministic DAG ordering/partitioning; cycle, unknown prerequisite, workload and stable chapter allocation fixtures |
| `engines/composition/contracts.py` | Plan and drafts → objective/assessment/table obligations, receipts and repair dependencies | One canonical obligation validator; independently folded assessment answers, review hash binding, source gap and targeted repair fixtures |
| `engines/composition/checks.py` | Drafts/evidence/notation → reviewable structural and semantic issues | Preserve notation, shape, prose density, source binding and authored depth gates; fail closed on unfulfilled critical obligations |
| `engines/composition/visuals.py` | Visual specifications, chapters and vault → stored artifacts, embedded drafts, verified/failed renderer receipts | Rust renderer/asset integration, scientific SVG/architecture/mask/flow output; artifacts must exist, hash-match and be embedded before fulfillment |
| `engines/composition/renderers.py` | Visual objective/category/backend availability → R1–R12 selection and SVG/HTML/Mermaid | Preserve twelve families and real capabilities; graph/coordinate integrity, finite values, escaping, missing adapter and family mismatch tests |
| `engines/composition/media.py` | Source URL, rights/relevance and asset policy → bounded PNG snapshot, immutable receipt and embed | Rust secure downloader with DNS pinning on redirects, MIME+decode, size/time limits, hash deduplication; remove remote publication branch while retaining provenance |
| `scripts/scribe.py` | CLI flags and JSON specs → routed commands, JSON/text/YAML, exit status | Canonical Rust CLI; preserve nested command behavior and output contracts before changing the primary skill command |
| `scripts/plan_notes.py` | Inspect/save/publish/update options → resolved plan and safe validated publication | Rust planning/publication CLI adapter; runtime verification, stack constraints, source policy, hash conflict and path containment parity |
| `scripts/scaffold_note.py` | Template/topic/classification options → scaffold with Properties | Rust template scaffolder for all seven masters and legacy aliases; never claim an empty scaffold is an authored note |
| `scripts/validate_note.py` | Markdown file + optional vault/contract → template, assessment, math and links findings | Markdown parser with code/comment-aware scanning, YAML and vault-aware anchors; preserve all meaningful gate behavior |
| `scripts/verify_vault_notes.py` | Vault, scoped files/manifest, optional fix → read-only audit or scoped safe repair | Vault scanner/manifest validator; exact scope, tag snapshot, templates, anchors and safe fix fixtures |
| `scripts/vault_index.py` | Vault/topic/discovery/cache options → metadata/template/tag/collision placement index | Canonical path containment, exclusion-aware scan, external cache, template data reads without plugin JS execution; custom configured notes folder |
| `scripts/vault_graph.py` | Indexed notes/topic → DAG order, cycles, broken/ambiguous links, orphans; JSON/text/Mermaid | Typed graph analysis; topology and ambiguous target fixtures; reuse one safe scanner |
| `scripts/patch_links.py` | Scoped note metadata/rename patch + dry-run → diff or preserved-body update | Conflict-aware YAML patching and code/comment-aware wikilink rewrite; exact body preservation and escaping fixtures |

All entries above begin **pending semantic parity**. A module's replacement path and verified tests must be recorded in the JSON ledger before its runtime file is removed. The table describes replacement requirements, not completed Rust functionality.

The new Rust v1 services in `crates/scriptorium-core/src/` implement separate typed contracts for configuration, bounded source retrieval, integrity-checked caching, visual requirement planning, local assets, deterministic rendering and artifact publication. These services are exercised through `crates/scriptorium-cli/src/main.rs`. Their interfaces intentionally differ from the legacy unified CLI. Available renderer adapters include scientific series/equations, coordinate graphs, graph layouts, architecture/flow diagrams, segment permission masks, structured tables, Mermaid source and fixed interactive output. External raster import supports PNG, JPEG and WebP. A declared renderer family or successful compile does not establish educational parity or browser rendering correctness.

Run `python tests/parity_check.py --binary target/release/scribe.exe` (omit `.exe` on Unix) after building to compare migrated PNG dimensions, byte hashes and scientific plot geometry against the retained Python reference. It also verifies deduplication, corrupted-asset rejection, deterministic rendering and equation mismatch errors. Its JSON report records the tested scope; routing, adaptive pedagogy, assessment, all F02–F15 KCP behaviors and full publication review parity remain pending.

## CLI and side-effect contracts

The unified CLI exposes `route`, `properties`, `update`, `migrate`, `validate`, `explain`, `notes`, `optimize`, `evaluate`, `audit` and `validate-registry`, with nested `research` and `pedagogy` passthroughs. `notes` supports `start`, `respond`, `generate`, `compose`, `validate` and `refine`. `compose` has prepare/publish/validate/context/repair modes with mutually exclusive actions. CLI parse errors, invalid plan errors and failed validation must retain nonzero exits; empty successful JSON is not equivalent behavior.

Mutation boundaries include session files under `.scriptorium`, metadata patches, collection manifests and checkpoints, immutable content-addressed assets/receipts, vault notes and external cache files. Some utilities update `~/.scriptorium-config.json` only for explicit folder-configuration actions. Dry runs and default read-only audits must remain read-only. Canonical containment includes symlink escape rejection. Publication must bind review receipts and evidence to actual authored artifacts and preserve unrelated notes.

Network access currently lives in media acquisition, with HTTPS-only input, public-address resolution and pinned TLS sockets on each redirect, bounded image sizes/timeouts, a strict PNG decoder, immutable local snapshots and tamper-detecting receipts. ARRIE research planning does not itself establish live source retrieval. Rights and relevance are supplied editorial assertions in the old media contract; the new design must record verification evidence and allowed reuse scope, not infer permission from an HTTP 200 response. Obsidian attachment-folder configuration must be resolved rather than replacing every path with a hard-coded `assets/` prefix.

## Removal and performance gates

1. Attach representative old/new input/output fixtures and run all relevant regression contracts for each migrated capability.
2. Verify unsupported capabilities fail explicitly instead of silently invoking Python or claiming success.
3. Exercise source fidelity, adaptive pedagogy, assessment integrity and cross-domain collections separately from image unit tests.
4. Measure release Rust CLI and Python with the same workload, local cache state and machine; separate startup, filesystem, model, network and rendering durations.
5. Remove a Python runtime file only when its callers, API contracts and parity evidence have been reconciled. Keep educational code and historical examples intentionally classified.

This document and its capture harness remain migration tooling until the migration is complete. Their presence is not a runtime Python dependency. No runtime Python files were removed by the audit.
