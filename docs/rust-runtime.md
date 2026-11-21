# Rust services and migration status

Build with `cargo build --release --locked`; run `target/release/scribe` (`.exe`
on Windows). A Rust toolchain and platform linker are build dependencies; the
resulting CLI does not invoke Python. Two crates separate reusable deterministic
services from argument parsing. Existing Python teaching engines remain because
their complete behavioral parity has not been established. See
[the per-file ledger](rust-migration-ledger.md).

The `notes plan --spec plan.json` command validates typed concepts, prerequisite
ordering and explicit visual needs. It reports insufficient representation diversity
for complex concepts; the authoring agent supplies learning objectives and distinct
visual needs based on the subject. It does not invent scientific content or claim
that a filename proves relevance. Plan schema examples live in the Rust tests.

Use `assets render --vault VAULT --note Collection/01.md --spec visual.json` to
store deterministic SVGs, or `assets import` with `--file`, `--mime` and
`--provenance` to inspect local PNG/JPEG/WebP files. `assets fetch` accepts `--url`
and `--provenance`; every redirect must resolve only to public addresses, and the
connection pins the validated DNS addresses. Transport and decoded-image limits
apply. External SVGs are rejected. All source, creator, license, permission evidence,
relevance, original filename and retrieval fields must be supplied; this is an
editorial attestation, not an automated legal or visual-relevance determination.

Each asset command prints an `AssetRecord`. Adding `--visual-id ID` instead prints
a `VisualReceipt` for the publication ledger. Persist these JSON outputs and combine
receipts into an array. The asset content hash deduplicates unchanged images. Use
`assets verify` or `assets embed` with `--record record.json` to recheck stored bytes.
Obsidian `.obsidian/app.json` attachment settings are respected, including note-relative
folders. Explicit `--config config.json` can override `attachment_directory`.

`renderers` reports twelve logical families and backend limitations. The generic
`render --spec visual.json --output figure.svg` interface writes standalone SVG,
Markdown table text (`.txt`), Mermaid source (`.mmd`), or fixed interactive HTML
(`.html`), according to the backend. Existing output files are preserved. Mermaid
source and HTML production do not prove host rendering or browser execution.
Host image generation requires a separate adapter. Use `assets render` for image
artifacts that must enter the verified local publication pipeline.

`notes publish --vault VAULT --destination Collection --plan plan.json
--receipts receipts.json --drafts drafts.json` accepts authored `{path, content}`
draft records. It validates YAML, images, critical visual fulfillment and hashes
before staging a fresh collection and renaming its directory. It refuses to overwrite
an existing collection. Prepared journals survive interrupted publication and must be
inspected before retrying. `notes audit` accepts the same vault, plan and receipts
for post-publication checks. Artifact completeness never certifies educational truth.
For this create-only publisher, configure attachments outside the destination
collection (for example vault-level `figures/`). Creating note-relative attachments
inside the destination first makes that directory exist, and publication refuses
it. Staged bundle ingestion and conflict-aware incremental updates remain pending.

`research --url https://example.org/source --cache CACHE` retrieves supplied UTF-8
text/HTML/JSON sources with bounded workers, three attempts, deterministic result order,
provenance and a versioned, TTL-bound, hash-verified cache. It does not search for
sources, extract PDF text, establish evidence quality, or call an LLM. Those existing
educational research contracts remain pending migration. Model reasoning can be
supplied by the authoring agent runtime without implementing inference in Rust.

Run `cargo test --workspace --locked`, `cargo fmt --all --check`, and
`cargo clippy --workspace --all-targets --locked -- -D warnings`. Run
`python tests/parity_check.py --binary target/release/scribe.exe` for the narrow
asset/scientific comparison, and `python -m pytest -q` for retained legacy regression
coverage. CI defines Linux and Windows jobs; local Windows tests do not establish
that the remote CI jobs passed. Benchmarks must identify build profile and measurement
scope, and must not attribute network or model latency improvements to Rust.
