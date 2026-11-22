"""Comprehensive test suite for:
- Section 34: Python Consolidation (6 cohesive engines + 8 thin public CLI scripts)
- Section 35: Mandatory Obsidian Properties & Tag Taxonomy (Tests A-J)
- Section 36: All 20 Advanced Knowledge Intelligence & Lifecycle Mechanisms (Tests 1-20)
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from scriptorium import (
    KnowledgeEngine,
    OrchestrationEngine,
    PedagogyEngine,
    QualityEngine,
    ResearchEngine,
    VaultEngine,
    parse_note,
)
from scriptorium.engines.knowledge import ConceptIdentityRegistry
from scriptorium.engines.quality import IssueReport, RepairEngine
from scriptorium.models import (
    ConceptIdentityError,
    UnsafeUpdateConflictError,
    content_hash,
    parse_frontmatter,
)


# ===========================================================================
# SECTION 34 — PYTHON CONSOLIDATION VERIFICATION
# ===========================================================================

def test_python_consolidation_script_reduction_and_six_engines():
    scripts = sorted(p.name for p in (ROOT / "scripts").glob("*.py"))
    # Consolidated from 18 scripts down to 8 pure CLI entry points
    assert len(scripts) == 8, f"Expected 8 public CLI scripts, found {scripts}"
    assert set(scripts) == {
        "patch_links.py",
        "plan_notes.py",
        "scaffold_note.py",
        "scribe.py",
        "validate_note.py",
        "vault_graph.py",
        "vault_index.py",
        "verify_vault_notes.py",
    }

    # Verify all 6 cohesive engines instantiate cleanly
    orch = OrchestrationEngine(ROOT)
    res = ResearchEngine()
    know = KnowledgeEngine()
    ped = PedagogyEngine()
    qual = QualityEngine(ROOT)
    vault = VaultEngine()
    assert all(x is not None for x in (orch, res, know, ped, qual, vault))


def test_shared_parse_note_caches_and_reuses_parsed_representation():
    sample = (
        "---\ntopic: Gradient Descent\ntags:\n  - domain/artificial-intelligence\n"
        "master_topic: Machine Learning\ndomain: Artificial Intelligence\nnote_type: deep-notes\n---\n\n"
        "# Gradient Descent\n\n## Intuition\nFollow negative gradient.\n\n## Code\n```python\nx = 1\n```\n"
    )
    p1 = parse_note(sample)
    p2 = parse_note(sample)
    assert p1 is p2  # exact cached ParsedNote instance reused without reparsing
    assert p1.title == "Gradient Descent"
    assert [s.heading for s in p1.sections] == ["Intuition", "Code"]
    assert len(p1.code_blocks) == 1


# ===========================================================================
# SECTION 35 — MANDATORY OBSIDIAN PROPERTIES SUITE (TESTS A-J)
# ===========================================================================

def test_properties_a_deep_ml_note():
    vault = VaultEngine()
    props = vault.build_properties(
        topic="Gradient Descent",
        note_type="deep-notes",
        secondary_concepts=["Learning Rate", "Loss Landscape"],
    )
    note = vault.render_note(props, "# Gradient Descent\n\n## Intuition\nIterative optimization.\n")
    assert note.startswith("---\n")
    assert vault.validate_properties(note, expected_note_type="deep-notes") == []
    assert props["topic"] == "Gradient Descent"
    assert props["domain"] == "Artificial Intelligence"
    assert props["master_topic"] == "Machine Learning"
    assert props["subdomain"] == "Optimization"
    assert props["note_type"] == "deep-notes"
    assert "domain/artificial-intelligence" in props["tags"]
    assert "master-topic/machine-learning" in props["tags"]
    assert "concept/gradient-descent" in props["tags"]
    assert "type/deep-notes" in props["tags"]


def test_properties_b_physics_note_has_zero_ml_tags():
    vault = VaultEngine()
    props = vault.build_properties(topic="Biot–Savart Law", note_type="study-notes")
    note = vault.render_note(props, "# Biot–Savart Law\n\n## 1. Setup\nMagnetic field from steady current.\n")
    assert vault.validate_properties(note, expected_note_type="study-notes") == []
    assert props["domain"] == "Physics"
    assert props["master_topic"] == "Electromagnetism"
    assert props["subdomain"] == "Magnetostatics"
    assert props["note_type"] == "study-notes"
    joined = " ".join(props["tags"]).lower()
    assert "machine-learning" not in joined and "artificial-intelligence" not in joined


def test_properties_c_programming_cheat_sheet():
    vault = VaultEngine()
    props = vault.build_properties(topic="Pandas Data Cleaning", note_type="cheat-sheet")
    note = vault.render_note(props, "# Pandas Data Cleaning\n\n| Op | Usage |\n|---|---|\n| `dropna()` | Drop NaNs |\n")
    assert vault.validate_properties(note, expected_note_type="quick-reference") == []
    assert props["domain"] == "Computer Science"
    assert props["master_topic"] == "Python Programming"
    assert props["note_type"] == "quick-reference"
    assert "type/quick-reference" in props["tags"]
    assert "concept/pandas-data-cleaning" in props["tags"]


def test_properties_d_mathematical_worked_solutions():
    vault = VaultEngine()
    props = vault.build_properties(topic="Integration by Parts", note_type="worked-solutions")
    note = vault.render_note(props, "# Integration by Parts\n\n## Problem 1\nSolve integral.\n")
    assert vault.validate_properties(note, expected_note_type="worked-solutions") == []
    assert props["domain"] == "Mathematics"
    assert props["master_topic"] == "Calculus"
    assert props["note_type"] == "worked-solutions"


def test_properties_e_history_revision_pack():
    vault = VaultEngine()
    props = vault.build_properties(topic="French Revolution", note_type="synthesis-revision")
    note = vault.render_note(props, "# French Revolution Revision Pack\n\n## Timeline\n1789-1799.\n")
    assert vault.validate_properties(note, expected_note_type="synthesis-revision") == []
    assert props["domain"] == "History"
    assert props["master_topic"] == "World History"
    assert props["note_type"] == "synthesis-revision"


def test_properties_f_unknown_topic_falls_back_defensibly():
    vault = VaultEngine()
    props = vault.build_properties(topic="Artisanal Sourdough Scoring Patterns", note_type="study-notes")
    assert props["domain"] == "General"
    assert props["master_topic"] == "General Knowledge"
    assert "subdomain" not in props
    assert "domain/general" in props["tags"]
    assert "type/study-notes" in props["tags"]


def test_properties_g_duplicate_frontmatter_and_tags_prevented():
    vault = VaultEngine()
    raw = "# Gradient Descent\n\n## Core\nDescent direction.\n"
    once = vault.ensure_properties(raw, topic="Gradient Descent", note_type="deep-notes")
    twice = vault.ensure_properties(once, topic="Gradient Descent", note_type="deep-notes")
    assert once == twice
    assert twice.count("\n---\n") == 1
    assert vault.validate_properties(twice) == []

    # Validator rejects manually duplicated frontmatter blocks
    dup = once.replace("# Gradient Descent", "---\ntopic: Dup\n---\n\n# Gradient Descent", 1)
    assert any("Duplicate YAML frontmatter" in err for err in vault.validate_properties(dup))


def test_properties_h_special_characters_and_unicode_parse_cleanly():
    vault = VaultEngine()
    special_topic = 'Biot–Savart Law: "B(r)" & α-Coupling (3D)'
    props = vault.build_properties(topic=special_topic, note_type="deep-notes")
    note = vault.render_note(props, f"# {special_topic}\n\n## Overview\nMagnetic field integral.\n")
    assert vault.validate_properties(note) == []
    parsed_meta, _, _ = parse_frontmatter(note)
    assert parsed_meta["topic"] == special_topic


def test_properties_i_existing_user_tags_and_custom_properties_preserved():
    vault = VaultEngine()
    existing = (
        "---\n"
        'topic: "Gradient Descent"\n'
        "tags:\n"
        "  - machine-learning\n"
        "  - my-personal-tag\n"
        'master_topic: "Machine Learning"\n'
        'domain: "Artificial Intelligence"\n'
        'note_type: "deep-notes"\n'
        'custom_property: "Important for my project"\n'
        'created: "2026-01-15"\n'
        "---\n\n"
        "# Gradient Descent\n\n"
        "## Intuition\nOld intuition.\n\n"
        "## My Manual Notes\nDo not touch my personal summary.\n"
    )
    upd = vault.update_note(
        existing,
        section_updates={"Intuition": "Refined intuition with Lipschitz smoothness."},
        update_date="2026-11-20",
    )
    assert upd["changed"] is True
    assert upd["properties"]["custom_property"] == "Important for my project"
    assert upd["properties"]["created"] == "2026-01-15"
    assert upd["properties"]["updated"] == "2026-11-20"
    assert "my-personal-tag" in upd["properties"]["tags"]
    assert "domain/artificial-intelligence" in upd["properties"]["tags"]
    assert "Do not touch my personal summary." in upd["content"]
    assert "Refined intuition with Lipschitz smoothness." in upd["content"]

    # Idempotence check: applying the exact same update again makes zero changes
    upd2 = vault.update_note(
        upd["content"],
        section_updates={"Intuition": "Refined intuition with Lipschitz smoothness."},
        update_date="2026-11-20",
    )
    assert upd2["changed"] is False
    assert upd2["content"] == upd["content"]


def test_properties_j_multi_artifact_consistent_hierarchy_distinct_note_types():
    vault = VaultEngine()
    p_deep = vault.build_properties(topic="Gradient Descent", note_type="deep-notes")
    p_cheat = vault.build_properties(topic="Gradient Descent", note_type="quick-reference")
    p_quiz = vault.build_properties(topic="Gradient Descent", note_type="assessment")
    assert p_deep["domain"] == p_cheat["domain"] == p_quiz["domain"] == "Artificial Intelligence"
    assert p_deep["master_topic"] == p_cheat["master_topic"] == p_quiz["master_topic"] == "Machine Learning"
    assert len({p_deep["note_type"], p_cheat["note_type"], p_quiz["note_type"]}) == 3


# ===========================================================================
# SECTION 36 — ALL 20 ADVANCED KNOWLEDGE INTELLIGENCE TESTS (TESTS 1-20)
# ===========================================================================

def test_01_intent_normalization_multi_artifact_from_scratch():
    orch = OrchestrationEngine(ROOT)
    norm = orch.normalize("Make notes from scratch and a separate formula sheet.")
    assert norm["artifact_relationship"]["separate_files"] is True
    assert norm["artifact_relationship"]["artifact_count"] == 2
    assert norm["requested_outputs"] == ["deep-notes", "quick-reference"]


def test_02_constraint_precedence_source_only_prevails_over_external_derivations():
    orch = OrchestrationEngine(ROOT)
    norm = orch.normalize("Source-only notes, but explain all derivations.", has_source=True)
    res = orch.resolve_constraints(norm)
    assert res["effective_source_policy"] == "strict"
    assert any(c["prevailing_layer"] == "source_policy" for c in res["conflicts"])
    assert "restrict_derivations_to_source_premises" in res["adaptations"]


def test_03_authority_conflict_detection_and_resolution():
    orch = OrchestrationEngine(ROOT)
    norm = orch.normalize("Explain backpropagation deeply")
    res = orch.resolve_constraints(
        norm,
        extra_constraints=[{
            "layer_a": "primary_master",
            "rule_a": "Keep M1 deep conceptual derivation",
            "layer_b": "optional_module",
            "rule_b": "Omit derivation to stay brief",
        }],
    )
    assert res["conflicts"][0]["prevailing_layer"] == "primary_master"
    lint = orch.lint_authority()
    assert lint["valid"] is True, lint["issues"]


def test_04_concept_identity_aliases_disambiguation_and_source_notation():
    reg = ConceptIdentityRegistry()
    gd = reg.register({
        "concept_id": "ml.optimization.gradient_descent",
        "canonical_name": "Gradient Descent",
        "aliases": ["GD", "Steepest Descent"],
        "domain": "Artificial Intelligence",
        "master_topic": "Machine Learning",
        "subdomain": "Optimization",
        "symbols": {"learning_rate": {"preferred": "alpha", "aliases": ["eta"]}},
    })
    assert reg.resolve("GD").concept_id == gd.concept_id
    eq = reg.explain_symbol_equivalence(gd.concept_id, r"\eta")
    assert eq["equivalent"] is True and eq["preserve_source_notation"] is True and eq["preferred"] == "alpha"

    # Homonym disambiguation: "Normalization" in ML vs Databases must NOT falsely collapse
    reg.register({"canonical_name": "Normalization", "domain": "Artificial Intelligence", "master_topic": "Deep Learning"})
    reg.register({"canonical_name": "Normalization", "domain": "Computer Science", "master_topic": "Databases"})
    with pytest.raises(ConceptIdentityError):
        reg.resolve("Normalization")
    assert reg.resolve("Normalization", domain="Computer Science").master_topic == "Databases"
    assert reg.resolve("Normalization", domain="Artificial Intelligence").master_topic == "Deep Learning"


def test_05_coverage_ledger_detects_missing_essential_concept():
    know = KnowledgeEngine()
    note = "# Backpropagation\n\n## Core\nBackpropagation uses derivatives and the chain rule.\n"
    ledger = know.track_coverage(
        [
            {"concept": "derivatives", "requirement": "essential", "keywords": ["derivatives"]},
            {"concept": "chain_rule", "requirement": "essential", "keywords": ["chain rule"]},
            {"concept": "computational_graph", "requirement": "essential", "keywords": ["computational graph"], "intended_section": "Computational Graph"},
            {"concept": "vectorized_backprop", "requirement": "advanced_optional"},
        ],
        note,
        master="M1",
        deferrals={"vectorized_backprop": "Introductory scope defers Jacobian vectorization."},
    )
    assert ledger["complete"] is False
    assert [m["concept"] for m in ledger["missing_essential"]] == ["computational_graph"]
    assert ledger["missing_essential"][0]["repair_target"]["intended_location"] == "Computational Graph"


def test_06_explanation_gap_detector_catches_skipped_chain_rule_and_undefined_symbol():
    ped = PedagogyEngine()
    note = (
        "# Gradient Step\n\n"
        "## Update\n"
        "$$\\theta_{t+1} = \\theta_t - \\lambda \\nabla f(\\theta_t)$$\n"
        "Compute d/dx sin(x^2) = 2x cos(x^2) directly; hence the method converges.\n"
    )
    report = ped.detect_gaps(note, required_prerequisites=["Chain Rule"], reader_level="beginner")
    assert report["has_gaps"] is True
    gap_types = {g["type"] for g in report["gaps"]}
    assert "hidden_prerequisite" in gap_types
    assert "skipped_derivation_step" in gap_types
    assert "missing_assumption" in gap_types


def test_07_information_density_controller_flags_overloaded_intro_preserving_depth():
    ped = PedagogyEngine()
    dense_note = (
        "# Transformer\n\n"
        "## Introduction\n"
        "Consider **Multi-Head Self-Attention**, **Positional Encoding**, **Layer Normalization**, "
        "**Residual Pathways**, **Feed-Forward Projections**, **Scaled Dot-Product**, and **Cross-Entropy Loss** "
        "with symbols $\\alpha$, $\\beta$, $\\gamma$, $\\delta$, $\\epsilon$, $\\lambda$.\n"
    )
    res = ped.control_density(dense_note, reader_level="beginner", preserve_exhaustive_depth=True)
    assert res["needs_restructuring"] is True
    assert res["preserve_exhaustive_depth"] is True
    assert "break_into_staged_subsections_and_define_terms_before_use" in res["overloaded_sections"][0]["interventions"]


def test_08_example_selection_optimizer_identifies_redundant_examples():
    ped = PedagogyEngine()
    res = ped.optimize_examples([
        {"id": "e1", "role": "worked", "mechanism": "gd_step", "content": "Minimize quadratic loss f(theta) = (theta - 3)^2 starting at theta=0 with step size 0.25."},
        {"id": "e2", "role": "worked", "mechanism": "gd_step", "content": "Minimize quadratic loss f(theta) = (theta - 4)^2 starting at theta=0 with step size 0.25."},
        {"id": "e3", "role": "boundary", "mechanism": "divergence", "content": "Choose step size eta = 2.5 / L exceeding stability threshold so iterates diverge."},
    ])
    assert res["has_redundancy"] is True
    assert [r["id"] for r in res["redundant"]] == ["e2"]
    assert [k["id"] for k in res["kept"]] == ["e1", "e3"]


def test_09_representation_consistency_checker_detects_mismatched_equation_code_and_shapes():
    qual = QualityEngine(ROOT)
    bad = qual.check_representations({
        "concept_id": "linear_model",
        "equation": "w * x + b",
        "variables": {"w": 2, "x": 3, "b": 1},
        "expected_output": 7,
        "code_output": 8,  # disagrees with 2*3 + 1 = 7!
        "tensor_shapes": {"input": (4, 8), "weight": (6, 3), "output": (4, 3)},  # 8 != 6!
    })
    assert bad["consistent"] is False
    types = {c["type"] for c in bad["conflicts"]}
    assert "numerical_mismatch" in types
    assert "tensor_shape_mismatch" in types

    good = qual.check_representations({
        "concept_id": "linear_model",
        "equation": "w * x + b",
        "variables": {"w": 2, "x": 3, "b": 1},
        "expected_output": 7,
        "code_output": 7,
        "prose_output": 7,
        "tensor_shapes": {"input": (4, 8), "weight": (8, 3), "output": (4, 3)},
    })
    assert good["consistent"] is True and good["canonical_value"] == 7.0


def test_10_claim_traceability_flags_unsupported_and_external_claims_in_strict_mode():
    know = KnowledgeEngine()
    audit = know.verify_claim_links(
        [
            {"id": "c1", "concept_id": "gd", "statement": "Step size < 2/L converges.", "origin": "source_fact",
             "evidence": [{"source_id": "SRC-1", "location": "Slide 8"}]},
            {"id": "c2", "concept_id": "gd", "statement": "Adam always beats SGD.", "origin": "source_fact", "evidence": []},
            {"id": "c3", "concept_id": "gd", "statement": "External paper claim.", "origin": "additional_research",
             "evidence": [{"source_id": "SRC-EXT", "location": "Section 2"}]},
        ],
        verified_sources={
            "SRC-1": {"content_verified": True, "role": "supplied"},
            "SRC-EXT": {"content_verified": True, "role": "external"},
        },
        source_policy="strict",
    )
    assert audit["valid"] is False
    issues = {f["issue"] for f in audit["findings"]}
    assert "unsupported_claim" in issues
    assert "strict_source_policy_violation" in issues
    assert "external_citation_in_strict_mode" in issues


def test_11_uncertainty_and_assumption_ledger_records_limitations():
    know = KnowledgeEngine()
    know.uncertainty.record_assumption("reader_math_level", "introductory_calculus", basis="inferred", certainty="assumed")
    know.uncertainty.record_limitation("example_code", status="not_executed", reason="runtime_unavailable")
    out = know.uncertainty.to_dict()
    assert out["assumptions"][0]["certainty"] == "assumed"
    assert out["verification_limitations"][0]["certainty"] == "unverified"


def test_12_adaptive_clarification_policy_proceeds_on_safe_default_and_asks_on_missing_source():
    orch = OrchestrationEngine(ROOT)
    # Safe default -> proceed without pestering user
    broad = orch.normalize("Backpropagation")
    assert orch.check_clarification(broad)["action"] == "proceed"

    # Missing referenced source -> ask cleanly
    missing_src = orch.normalize("Make notes on this lecture PDF without skipping anything", has_source=False)
    ask = orch.check_clarification(missing_src)
    assert ask["action"] == "ask"
    assert len(ask["questions"]) >= 1


def test_13_multi_artifact_consistency_catches_and_reconciles_notation():
    vault = VaultEngine()
    know = KnowledgeEngine()
    n_deep = vault.render_note(
        vault.build_properties(topic="Gradient Descent", note_type="deep-notes"),
        "# Gradient Descent\n\nWhen $f$ is $L$-smooth and $0 < \\eta < 2/L$, updates converge.\n",
    )
    n_cheat_bad = vault.render_note(
        vault.build_properties(topic="Gradient Descent", note_type="quick-reference"),
        "# Gradient Descent — Cheat Sheet\n\nUpdate uses learning rate $\\alpha$.\n",
    )
    res_bad = know.check_multi_artifact([
        {"note_text": n_deep, "symbols": {"learning_rate": "eta"}, "conditions": ["L-smooth"]},
        {"note_text": n_cheat_bad, "symbols": {"learning_rate": "alpha"}},
    ])
    assert res_bad["consistent"] is False
    issue_types = {i["type"] for i in res_bad["issues"]}
    assert "unexplained_notation_divergence" in issue_types
    assert "dropped_applicability_condition" in issue_types

    n_cheat_good = vault.render_note(
        vault.build_properties(topic="Gradient Descent", note_type="quick-reference"),
        "# Gradient Descent — Cheat Sheet\n\nAssuming $L$-smooth objective, learning rate $\\alpha$ (denoted $\\eta$ in deep notes).\n",
    )
    res_good = know.check_multi_artifact([
        {"note_text": n_deep, "symbols": {"learning_rate": "eta"}, "conditions": ["L-smooth"]},
        {"note_text": n_cheat_good, "symbols": {"learning_rate": "alpha"}},
    ])
    assert res_good["consistent"] is True
    assert len(res_good["reconciliations"]) == 1


def test_14_knowledge_compression_preserves_applicability_conditions():
    ped = PedagogyEngine()
    auth_note = (
        "# Gradient Descent\n\n"
        "## Mathematical Definition\n"
        "Assuming $f$ is differentiable and $L$-smooth, choosing $0 < \\eta < 2/L$ guarantees descent:\n\n"
        "$$\\theta_{t+1} = \\theta_t - \\eta \\nabla f(\\theta_t)$$\n\n"
        "- **Stability Condition**: Fails and diverges when $\\eta > 2/L$.\n"
    )
    comp = ped.compress(auth_note, target_product="quick-reference", required_conditions=["0 < \\eta < 2/L", "L-smooth"], source_link="01 - Gradient Descent")
    assert comp["validation"]["valid"] is True
    assert "[[01 - Gradient Descent]]" in comp["compressed_body"]

    bad_comp = ped.validate_compression(auth_note, "# GD\nGradient descent always converges.\n", required_conditions=["L-smooth"])
    assert bad_comp["valid"] is False
    assert any("overgeneralized" in i for i in bad_comp["issues"])


def test_15_incremental_update_safe_write_and_conflict_detection(tmp_path):
    vault = VaultEngine()
    note_path = tmp_path / "01 - Gradient Descent.md"
    initial = vault.render_note(
        vault.build_properties(topic="Gradient Descent", note_type="deep-notes", custom_properties={"owner": "aayush"}),
        "# Gradient Descent\n\n## Definition\nOld def.\n\n## Examples\nUnchanged example.\n",
    )
    vault.write_note(note_path, initial)
    digest = content_hash(initial)

    upd = vault.update_note(initial, section_updates={"Definition": "Updated precise definition."})
    res = vault.write_note(note_path, upd["content"], expected_digest=digest)
    assert res["written"] is True
    written = note_path.read_text(encoding="utf-8")
    assert "Updated precise definition." in written
    assert "Unchanged example." in written
    assert "owner: aayush" in written

    # Stale digest triggers UnsafeUpdateConflictError instead of silent overwrite
    with pytest.raises(UnsafeUpdateConflictError):
        vault.write_note(note_path, initial, expected_digest="stale-digest")


def test_16_semantic_change_detection_and_impact_graph():
    know = KnowledgeEngine()
    v1 = "# GD\n\n## Definition\nStep size $\\eta = 0.1$.\n"
    v1_ws = "# GD\n\n## Definition\nStep size   $\\eta = 0.1$.\n\n"
    v2 = "# GD\n\n## Definition\nStep size $\\eta = 0.05$.\n"
    assert know.detect_changes(v1, v1_ws)["change_type"] == "cosmetic"
    sem = know.detect_changes(v1, v2)
    assert sem["change_type"] == "semantic"
    assert sem["requires_downstream_check"] is True

    impact = know.detect_impacted_concepts(
        ["learning_rate_def"],
        {
            "learning_rate_def": ["gd_deep_notes"],
            "gd_deep_notes": ["gd_cheat_sheet", "gd_flashcards"],
            "gd_cheat_sheet": ["gd_revision_pack"],
        },
        manually_edited={"gd_cheat_sheet"},
    )
    assert "gd_deep_notes" in impact["impacted"]
    assert "gd_flashcards" in impact["safe_to_update"]
    assert impact["manual_edit_conflicts"] == ["gd_cheat_sheet"]


def test_17_failure_aware_targeted_repair_and_retry_cap():
    repair = RepairEngine(max_retries=2)
    draft = (
        "# Gradient Descent\n\n"
        "## Intuition\nKeep this untouched.\n\n"
        "## Worked Example\nWith $\\theta_0=0, \\eta=0.25, g=-6$: $\\theta_1 = 999$.\n"
    )
    issue = IssueReport(
        issue_id="MATH-042",
        concept_id="gradient_descent",
        location="worked_example",
        severity="major",
        type="numerical_mismatch",
        description="Parameter update disagrees with stated learning rate.",
        repair_scope="worked_example",
        dependent_checks=["equation_consistency", "revision_summary"],
    )
    res = repair.apply_local_repair(
        draft,
        issue,
        find_text=r"$\theta_1 = 999$",
        replace_text=r"$\theta_1 = 1.5$",
        validator=lambda txt: [] if r"$\theta_1 = 1.5$" in txt else ["still wrong"],
    )
    assert res["repaired"] is True
    assert res["full_regeneration_avoided"] is True
    assert "Keep this untouched." in res["content"]

    # Retry cap enforcement on unfixable issue
    bad_issue = IssueReport("ERR-1", "c", "loc", "major", "bad", "desc", "loc")
    repair.apply_local_repair(draft, bad_issue, find_text="NONEXISTENT", replace_text="X")
    repair.apply_local_repair(draft, bad_issue, find_text="NONEXISTENT", replace_text="X")
    capped = repair.apply_local_repair(draft, bad_issue, find_text="NONEXISTENT", replace_text="X")
    assert capped["stopped_reason"] == "max_retries_exceeded"


def test_18_golden_evaluation_harness_all_13_cases_pass():
    qual = QualityEngine(ROOT)
    report = qual.run_golden_evaluations()
    assert report["total"] == 13
    assert report["all_passed"] is True, report["results"]


def test_19_decision_trace_observability_scrubs_secrets_and_stays_out_of_notes():
    orch = OrchestrationEngine(ROOT)
    routed = orch.route("Explain gradient descent deeply")
    trace = orch.trace(
        routed=routed,
        metadata={"topic": "Gradient Descent", "domain": "Artificial Intelligence", "master_topic": "Machine Learning", "note_type": "deep-notes", "tags": ["a", "b"]},
        validation={"coverage": "passed", "debug_note": "api_key=sk-1234567890abcdefghij"},
    )
    assert trace["route"]["master"] == "M1"
    assert trace["metadata"]["yaml_valid"] is True
    assert "sk-1234567890abcdefghij" not in json.dumps(trace)
    assert "[REDACTED]" in json.dumps(trace)


def test_20_unified_scribe_cli_end_to_end(tmp_path):
    # 1. properties subcommand
    p_props = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "scribe.py"), "properties", "--topic", "Biot–Savart Law", "--note-type", "study-notes"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    assert p_props.stdout.startswith("---\n")
    meta, _, _ = parse_frontmatter(p_props.stdout)
    assert meta["domain"] == "Physics" and meta["note_type"] == "study-notes"

    # 2. migrate + update subcommands on a real file
    note_file = tmp_path / "gd.md"
    note_file.write_text("# Gradient Descent\n\n## Intuition\nOld text.\n\n## Extra\nKeep me.\n", encoding="utf-8")
    subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "scribe.py"), "migrate", str(note_file), "--note-type", "deep-notes"],
        capture_output=True, text=True, check=True,
    )
    migrated = note_file.read_text(encoding="utf-8")
    assert migrated.startswith("---\n")

    subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "scribe.py"), "update", str(note_file), "--section", "Intuition=New text.", "--add-tag", "exam-prep"],
        capture_output=True, text=True, check=True,
    )
    final = note_file.read_text(encoding="utf-8")
    assert "New text." in final and "Keep me." in final and "exam-prep" in final

    # 3. evaluate & audit subcommands
    p_eval = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "scribe.py"), "evaluate"],
        capture_output=True, text=True, check=True,
    )
    assert json.loads(p_eval.stdout)["all_passed"] is True

    p_audit = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "scribe.py"), "audit"],
        capture_output=True, text=True, check=True,
    )
    assert json.loads(p_audit.stdout)["valid"] is True
