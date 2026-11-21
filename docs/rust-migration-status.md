# Verified migration milestone; full migration incomplete

The Rust CLI and library execute local visual planning, deterministic rendering,
secure source retrieval, decoded image storage, caching, local embed checks and
create-only collection publication without invoking Python. Twelve logical renderer
families remain represented. Mermaid and interactive outputs retain their explicit
host-rendering limitations. Image-generation model access still requires a host adapter.

The retained Python publisher now uses verified local snapshots even for the legacy
`remote_allowed` acquisition policy. Original source URLs remain in its provenance.

Validation performed on Windows with Rust 1.100.0 GNU and Python 3.14.7:

- Full retained Python suite: 564 passed after the publication change.
- Rust: 29 unit tests and one CLI integration test passed. The CLI test publishes
  complementary local assets across mathematics, engineering, AI, computer science
  and history fixtures, then detects tampering.
- Seven Python/Rust parity checks passed for image dimensions, SHA-256, deduplication,
  corruption rejection, deterministic scientific geometry and equation agreement.
- Release build, rustfmt check and Clippy with warnings denied passed.
- Skill frontmatter validation and repository/authority/registry audits passed.
- The checked-in [two-visual example](../examples/rust-local-visuals/README.md) was
  actually generated, published and audited by the release Rust binary.

[Raw measurements](rust-migration-benchmarks.json) report seven samples each. Local
median help startup was 303.03 ms for Python and 8.78 ms for release Rust. These
commands expose different command sets; this measures launch/import/help overhead,
not full application parity or educational quality. The report also records local
rendering, metadata validation, hashing, asset verification and cache lookup samples.
Network/model latency and complete note-generation latency are not benchmarked.

No Python runtime files were removed. The audited 35 runtime/CLI files contain
24,420 lines and 581 function contracts. Full routing, interactive sessions, ARRIE
policy evaluation, pedagogy, adaptive chapters, assessment integrity, knowledge
identity, feedback/refinement, vault graph/patching and other KCP lifecycle behavior
still require Rust implementations and semantic parity evidence. The
[per-file ledger](rust-migration-ledger.md) records those requirements. The canonical
educational `/scribe-notes` command therefore still needs Python. This milestone
does not satisfy the full specification's Python removal or Rust-primary acceptance.

Other limitations: publication refuses existing destination folders; configured
note-relative attachments inside that destination need a staged-bundle integration
before create-only publication can support them. Scientific SVG inspection validates
passive XML, dimensions and reproducible inputs; scientific relevance, label readability
and permission evidence still require review. External research retrieval supports
UTF-8 text/HTML/JSON, with PDF extraction and model APIs pending. The `meval` dependency
brings `nom 1.2.4`, which Rust currently reports as future-incompatible; replace this
equation parser before a future compiler update makes that warning an error.

Linux/Windows CI jobs are defined; local validation does not establish their remote
results. No claim of complete migration, full renderer parity, or model-quality
improvement is made.
