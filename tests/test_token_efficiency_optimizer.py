"""Tests for Scriptorium Token Efficiency, Prompt Compilation, Multi-Level Cache & Zero-Quality-Loss Optimization."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scriptorium import (
    CACHE_LEVELS,
    VALIDATION_PRESERVATION_MATRIX,
    MultiLevelCache,
    OrchestrationEngine,
    QualityEngine,
    SourceSegmentStore,
    TokenEfficiencyController,
    VaultEngine,
)
from scriptorium.engines._token_optimizer import (
    build_targeted_repair_context,
    compact_plan_ir,
    filter_tool_output,
    measure_naive_full_context_tokens,
)

PYTHON = sys.executable


# ---------------------------------------------------------------------------
# Opt A & Q — Selective Context Loading + Dependency Closure
# ---------------------------------------------------------------------------

def test_opt_a_selective_context_loading_reduces_overhead_without_dropping_dependencies():
    orch = OrchestrationEngine(ROOT)
    naive = measure_naive_full_context_tokens(ROOT)
    bundle = orch.select_context(
        master="M5",
        variant=None,
        knowledge_types=["computational"],
        source_policy="adaptive",
        has_source=False,
        code_depth=4,
    )
    # Must load M5 + computational + properties policy, NOT history/physics/unrelated masters
    assert "references/templates/masters/implementation-guide.md" in bundle["loaded_files"]
    assert "references/templates/subtemplates/computational.md" in bundle["loaded_files"]
    assert all("historical.md" not in f for f in bundle["loaded_files"])
    assert all("worked-solutions.md" not in f for f in bundle["loaded_files"])
    # Dependency closure: executable_verification depends on code_explanation -> definitions
    assert "definitions" in bundle["active_modules"]
    assert "code_explanation" in bundle["active_modules"]
    assert "executable_verification" in bundle["active_modules"]
    # Substantial reduction vs naive full-directory load
    assert bundle["estimated_tokens"] < naive["estimated_tokens"] * 0.15


# ---------------------------------------------------------------------------
# Opt B & O — Canonical Prompt Compilation, Deduplication & Prefix Caching
# ---------------------------------------------------------------------------

def test_opt_b_o_canonical_prompt_compilation_preserves_distinct_contracts_and_prefix():
    orch = OrchestrationEngine(ROOT)
    bundle = orch.select_context(
        master="M1",
        knowledge_types=["mathematical"],
        source_policy="strict",
        has_source=True,
        math_depth=4,
    )
    compiled = orch.compile_prompt(
        bundle,
        preferences_ir={"master": "M1", "depth": "comprehensive", "source_policy": "strict"},
        source_constraints={"source_policy": "strict"},
        validation_contracts=["source_fidelity", "citation_correctness", "factual_correctness", "obsidian_properties"],
        provider_prefix_caching=True,
    )
    assert compiled["verified"] is True, compiled["verification_errors"]
    assert "<!--" not in compiled["compiled_prompt"]
    # Distinct contracts preserved separately
    for contract in ("source_fidelity", "citation_correctness", "factual_correctness", "obsidian_properties"):
        assert contract in compiled["compiled_prompt"]
    # Processed tokens reported separately from cacheable prefix tokens
    toks = compiled["tokens"]
    assert toks["total_processed_tokens"] == toks["cacheable_prefix_tokens"] + toks["uncached_dynamic_tokens"]
    assert toks["cacheable_prefix_tokens"] > 0
    assert toks["total_processed_tokens"] <= toks["uncompiled_bundle_tokens"]


# ---------------------------------------------------------------------------
# Opt D — Source Segmentation, Single-Pass Extraction & Coverage Ledger
# ---------------------------------------------------------------------------

def test_opt_d_source_segmentation_reuse_adjacent_context_and_coverage_ledger():
    store = SourceSegmentStore()
    chapter = "\n\n".join(
        f"## Section {i}: {'Gradient Descent' if i == 4 else f'Topic {i}'}\n"
        + (f"Detailed authoritative textbook paragraph for section {i}. " * 40)
        for i in range(1, 9)
    )
    ing1 = store.ingest_source("ch3", chapter)
    ing2 = store.ingest_source("ch3", chapter)
    assert ing1["reused_extraction"] is False
    assert ing2["reused_extraction"] is True
    assert ing1["segment_count"] == 8

    # Targeted retrieval returns matched section + adjacent sections (3, 4, 5) preserving theorem context
    ret = store.retrieve_passages("ch3", ["Gradient Descent"], include_adjacent_context=True)
    headings = [p["heading"] for p in ret["passages"]]
    assert len(headings) == 3
    assert any("Section 4" in h for h in headings)
    assert any("Section 3" in h for h in headings)
    assert any("Section 5" in h for h in headings)
    assert ret["token_savings"] > 0

    # Coverage ledger honestly shows remaining pending sections (never silently drops coverage!)
    ledger = store.coverage_ledger("ch3")
    assert ledger["covered_sections"] == 1
    assert ledger["complete"] is False
    assert len(ledger["pending_sections"]) == 7


# ---------------------------------------------------------------------------
# Opt E & Part 30 — Multi-Level Cache (L1-L10), Isolation, TTL, Corruption & Secret Guard
# ---------------------------------------------------------------------------

def test_opt_e_multi_level_cache_isolation_ttl_corruption_and_secret_safety(tmp_path):
    assert len(CACHE_LEVELS) == 10
    cache = MultiLevelCache(disk_dir=tmp_path / "cache")

    k_a = cache.build_key("L3_research_evidence", user_scope="user_a", dependencies={"q": "gradient descent", "v": 1})
    cache.put(k_a, {"facts": ["descent step"]}, user_scope="user_a", ttl_seconds=60, now=1000.0)

    # Hit for user_a within TTL
    hit_ok, val = cache.get(k_a, expected_user_scope="user_a", now=1030.0)
    assert hit_ok is True and val["facts"] == ["descent step"]

    # Strict user isolation: user_b cannot read user_a entry
    hit_other, _ = cache.get(k_a, expected_user_scope="user_b", now=1030.0)
    assert hit_other is False

    # Freshness TTL expiry invalidates stale evidence
    hit_expired, _ = cache.get(k_a, expected_user_scope="user_a", now=1090.0)
    assert hit_expired is False

    # Corrupted disk entry is evicted cleanly without crashing
    bad_key = cache.build_key("L9_validation_result", user_scope="user_a", dependencies={"id": "corrupt"})
    bad_file = tmp_path / "cache" / f"{bad_key.replace(':', '_')}.json"
    bad_file.parent.mkdir(parents=True, exist_ok=True)
    bad_file.write_text("{not valid json", encoding="utf-8")
    hit_bad, _ = cache.get(bad_key, expected_user_scope="user_a")
    assert hit_bad is False
    assert cache.stats["corrupt_evictions"] == 1

    # Part 30.3 Credential safety: refuse API keys/tokens in cache keys & payloads
    with pytest.raises(ValueError, match="credential"):
        cache.build_key("L6_prompt_compilation", dependencies={"token": "sk-1234567890abcdef1234"})
    with pytest.raises(ValueError, match="credentials"):
        cache.put("L6_prompt_compilation:default:safe", {"secret": "api_key=supersecretvalue12345"})


# ---------------------------------------------------------------------------
# Opt F & K — Partitioned Shared Collection Context
# ---------------------------------------------------------------------------

def test_opt_f_partitioned_collection_context_saves_tokens_and_preserves_direct_links(tmp_path):
    orch = OrchestrationEngine(ROOT)
    s = orch.start_notes_session("/scribe-notes Machine Learning")
    r1 = orch.respond_to_session(s, "comprehensive, hierarchical collection")
    r2 = orch.respond_to_session(r1["state"], "proceed")
    plan, prefs = r2["state"].collection_plan, r2["state"].resolved_preferences
    kcp = orch.build_kcp(tmp_path, plan, prefs, include_synthesis=True, include_assessment=True)

    gd_node = next(n for n in plan.nodes if n.title == "Gradient Descent")
    part = orch.partition_collection_context(kcp, gd_node.concept_id)
    assert part["partitioned_tokens"] < part["full_kcp_tokens"]
    assert part["token_savings"] > 0
    assert part["note_context"]["title"] == "Gradient Descent"
    assert any(p["title"] == "Loss Functions" for p in part["note_context"]["direct_prerequisites"])
    assert part["note_context"]["outcomes"], "Direct learning outcomes must survive context partitioning"


# ---------------------------------------------------------------------------
# Opt I, J, M, N, U — Zero-Redundancy Validation, Targeted Repair, Compaction & Filtering
# ---------------------------------------------------------------------------

def test_opt_i_zero_redundancy_validation_preserves_all_checks_at_zero_llm_tokens(tmp_path):
    assert len(VALIDATION_PRESERVATION_MATRIX) == 14
    assert all(row["must_remain"] is True for row in VALIDATION_PRESERVATION_MATRIX)

    orch = OrchestrationEngine(ROOT)
    vault = VaultEngine()
    quality = QualityEngine(ROOT)
    cache = MultiLevelCache()

    s = orch.start_notes_session("/scribe-notes Gradient Descent")
    r1 = orch.respond_to_session(s, "use your recommendations")
    plan, prefs = r1["state"].collection_plan, r1["state"].resolved_preferences
    vault.generate_collection(tmp_path, plan, prefs)
    gd_text = (tmp_path / plan.nodes[0].proposed_path).read_text(encoding="utf-8")

    # First run: deterministic, 0 LLM tokens
    v1 = quality.validate_zero_redundancy(gd_text, master="M1", cache=cache)
    assert v1["llm_tokens_used"] == 0
    assert v1["cache_hit"] is False
    assert v1["valid"] is True

    # Second run on unchanged note: valid L9 cache hit with audit trail
    v2 = quality.validate_zero_redundancy(gd_text, master="M1", cache=cache)
    assert v2["cache_hit"] is True
    assert all(a["execution"] == "cached_valid" for a in v2["audit_trail"])

    # Modified note -> cache miss, re-executes deterministically!
    v3 = quality.validate_zero_redundancy(gd_text + "\nExtra line.\n", master="M1", cache=cache)
    assert v3["cache_hit"] is False


def test_opt_j_m_n_targeted_repair_compaction_and_tool_filtering():
    long_note = (
        "---\ntopic: Gradient Descent\ntags: [domain/artificial-intelligence]\n"
        "master_topic: Machine Learning\ndomain: Artificial Intelligence\nnote_type: deep-notes\n---\n\n"
        "# Gradient Descent\n\n"
        + "\n\n".join(f"## Section {i}\n" + ("Detailed explanation prose. " * 70) for i in range(1, 11))
        + "\n\n## Numerical Table\n| iter | loss |\n|---|---|\n| 1 | 99.0 |\n"
    )
    rep = build_targeted_repair_context(long_note, target_section="Numerical Table", issue_description="Row 1 loss wrong.")
    assert rep["reduction_percent"] > 85.0
    assert rep["full_regeneration_recommended"] is False

    orch = OrchestrationEngine(ROOT)
    s = orch.start_notes_session("/scribe-notes Machine Learning")
    r1 = orch.respond_to_session(s, "use your recommendations")
    verbose_hist = [{"role": "user", "text": "Long superseded outline discussion. " * 40} for _ in range(6)]
    comp = orch.compact_working_state(r1["state"], conversation_history=verbose_hist)
    assert comp["compact_state_tokens"] < comp["raw_history_tokens"]
    assert comp["compact_state"]["topic"] == "Machine Learning"

    # Tool output filter preserves 100% of failures while trimming passing noise
    noisy = {
        "results": [{"id": f"ok_{i}", "passed": True} for i in range(30)] + [{"id": "bad_1", "passed": False, "error": "wrong bound"}],
        "errors": ["wrong bound"],
    }
    filt = filter_tool_output("evaluate", noisy)
    assert filt["filtered_tokens"] < filt["raw_tokens"]
    assert filt["filtered_payload"]["results"] == [{"id": "bad_1", "passed": False, "error": "wrong bound"}]
    assert filt["filtered_payload"]["passed_count"] == 30


# ---------------------------------------------------------------------------
# Opt R — 12-Workload Benchmark & CLI `scripts/scribe.py optimize`
# ---------------------------------------------------------------------------

def test_opt_r_twelve_workload_benchmark_and_cli_execution():
    proc = subprocess.run(
        [PYTHON, "-B", str(ROOT / "scripts" / "scribe.py"), "optimize", "--benchmark"],
        capture_output=True, text=True, check=True,
    )
    report = json.loads(proc.stdout)
    assert report["workloads_count"] == 12
    assert report["all_compilations_verified"] is True
    assert report["instruction_reduction_percent"] > 80.0
    assert report["targeted_repair_benchmark"]["reduction_percent"] > 85.0
    assert report["source_retrieval_benchmark"]["reduction_percent"] > 50.0
    assert report["validation_checks_preserved"] == 14
