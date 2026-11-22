"""Comprehensive tests for Scriptorium Knowledge Collection Intelligence & Lifecycle (F02-F15).

Covers:
- Explicit Exclusion of Feature 1 (Interactive Knowledge Diagnosis)
- Shared KnowledgeCollectionPlan (KCP)
- All 14 capabilities F02-F15 and Scenarios A-L
- End-to-end CLI checkpoint generation + F15 reader-feedback refinement
"""
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
    INTERACTIVE_KNOWLEDGE_DIAGNOSIS_ENABLED,
    KnowledgeCollectionPlan,
    KnowledgeEngine,
    NoteCollectionPlan,
    OrchestrationEngine,
    PedagogyEngine,
    QualityEngine,
    ResolvedNotePreferences,
    TopicNode,
    VaultEngine,
    parse_note,
)

PYTHON = sys.executable


def _make_ml_plan_and_prefs(depth: str = "comprehensive", source_policy: str = "adaptive"):
    orch = OrchestrationEngine(ROOT)
    s = orch.start_notes_session("/scribe-notes Machine Learning")
    r1 = orch.respond_to_session(s, f"{depth}, hierarchical collection")
    r2 = orch.respond_to_session(r1["state"], "proceed")
    prefs = r2["state"].resolved_preferences
    prefs.source_policy = source_policy
    return r2["state"].collection_plan, prefs


# ---------------------------------------------------------------------------
# Explicit Exclusion Guard — Feature 1 (Interactive Knowledge Diagnosis)
# ---------------------------------------------------------------------------

def test_feature_1_interactive_knowledge_diagnosis_strictly_excluded(tmp_path):
    assert INTERACTIVE_KNOWLEDGE_DIAGNOSIS_ENABLED is False
    orch = OrchestrationEngine(ROOT)
    plan, prefs = _make_ml_plan_and_prefs()
    kcp = orch.build_kcp(tmp_path, plan, prefs, include_assessment=True)
    assert kcp.diagnostic_quiz_enabled is False
    assert kcp.to_dict()["diagnostic_quiz_enabled"] is False
    assert kcp.assessment_plan["is_pre_generation_diagnostic"] is False


# ---------------------------------------------------------------------------
# F02 — Collection-Level Adaptive Depth Allocation
# ---------------------------------------------------------------------------

def test_f02_adaptive_depth_allocation_centrality_priority_and_budget():
    ped = PedagogyEngine()
    plan, prefs = _make_ml_plan_and_prefs(depth="comprehensive")
    res = ped.allocate_depth(plan, prefs, budget_notes=5, user_priorities=["Feature Scaling"])
    allocs = res["allocations"]

    gd = next(v for v in allocs.values() if v["title"] == "Gradient Descent")
    what_is = next(v for v in allocs.values() if v["title"] == "What is Machine Learning")
    fs = next(v for v in allocs.values() if v["title"] == "Feature Scaling")

    assert gd["allocation"] in {"deep", "detailed"}
    assert fs["priority"] == "high"
    assert "explicit_user_priority" in fs["reasons"]
    assert gd["score"] >= what_is["score"]
    assert gd["expose_scores_in_note"] is False
    assert res["warnings"], "Expected budget warning when planned notes exceed budget_notes=5"


# ---------------------------------------------------------------------------
# F03 — Smart Existing-Note Reuse (Scenario B)
# ---------------------------------------------------------------------------

def test_f03_existing_note_reuse_exact_alias_readonly_and_variant(tmp_path):
    vault = VaultEngine()
    know = KnowledgeEngine()
    plan, prefs = _make_ml_plan_and_prefs(depth="standard")

    # 1. High-quality existing canonical note (should reuse_with_link / reuse_unchanged)
    gd_path = tmp_path / "Mathematics" / "Gradient Descent.md"
    gd_props = vault.build_properties(topic="Gradient Descent", note_type="deep-notes", aliases=["GD Algorithm"])
    gd_body = (
        "# Gradient Descent\n\n## Motivation\n"
        + ("Gradient descent iteratively updates model parameters opposite the loss gradient. " * 12)
        + "\n\n## Convergence\nRequires step size between 0 and 2/L for L-smooth convex objectives.\n"
    )
    vault.write_note(gd_path, vault.render_note(gd_props, gd_body))

    # 2. Thin existing note marked read-only (should trigger request_user_resolution)
    lr_path = tmp_path / "Existing" / "Linear Regression.md"
    lr_props = vault.build_properties(topic="Linear Regression", note_type="deep-notes")
    vault.write_note(lr_path, vault.render_note(lr_props, "# Linear Regression\n\nShort stub.\n"))

    rec = know.reconcile_existing_notes(tmp_path, plan, prefs, readonly_paths={"Existing/Linear Regression.md"})
    by_title = {v["title"]: v for v in rec["decisions"].values()}
    assert by_title["Gradient Descent"]["decision"] in {"reuse_with_link", "reuse_unchanged"}
    assert by_title["Linear Regression"]["decision"] == "request_user_resolution"
    assert rec["reused_count"] >= 1
    assert len(rec["conflicts"]) == 1

    # 3. Distinct artifact variant (M3 quick-reference should NOT overwrite canonical M1 deep-notes)
    prefs_m3 = ResolvedNotePreferences(
        learning_objective="quick_revision",
        master="M3",
        variant="formula_sheet",
        depth="concise",
        prior_knowledge={"level": "intermediate"},
        organization="hierarchical_collection",
        emphasis=[],
        source_policy="adaptive",
    )
    rec_m3 = know.reconcile_existing_notes(tmp_path, plan, prefs_m3)
    by_title_m3 = {v["title"]: v for v in rec_m3["decisions"].values()}
    assert by_title_m3["Gradient Descent"]["decision"] == "create_distinct_variant"


# ---------------------------------------------------------------------------
# F04 — Knowledge Graph Gap Analysis (G1-G5 & Strict Source Policy)
# ---------------------------------------------------------------------------

def test_f04_prerequisite_gaps_g1_to_g5_and_strict_mode():
    know = KnowledgeEngine()
    prefs = ResolvedNotePreferences(
        learning_objective="conceptual_mastery",
        master="M1",
        variant=None,
        depth="comprehensive",
        prior_knowledge={"level": "beginner", "known_concepts": ["Computational Graphs"]},
        organization="hierarchical_collection",
        emphasis=["mathematics"],
        source_policy="strict",
    )
    n1 = TopicNode("nn.backprop", "Backpropagation", None, prerequisite_ids=["nn.missing_ref", "nn.opt"], proposed_path="Backpropagation.md", note_role="child")
    n2 = TopicNode("nn.opt", "Gradient Descent", None, prerequisite_ids=["a", "b", "c", "d", "e", "f"], proposed_path="GD.md", note_role="child")
    plan = NoteCollectionPlan(
        collection_id="col-nn",
        title="Neural Networks",
        root_topic_id="nn.root",
        organization="hierarchical_collection",
        nodes=[n1, n2],
        planned_paths=["Backpropagation.md", "GD.md"],
        learning_order=["nn.backprop", "nn.opt"],  # Deliberate G3 ordering violation (opt after backprop)
        generation_order=["nn.backprop", "nn.opt"],
    )

    res = know.analyze_prerequisite_gaps(plan, prefs)
    assert res["used_diagnostic_quiz"] is False
    gap_types = {g["gap_type"] for g in res["gaps"]}
    assert "G1" in gap_types  # Missing Chain Rule / Partial Derivatives
    assert "G3" in gap_types  # Ordering violation (Gradient Descent after Backpropagation)
    assert "G4" in gap_types  # Broken concept_id reference nn.missing_ref
    assert "G5" in gap_types  # Excessive 6 prerequisites on n2
    # Computational Graphs was self-reported known -> must NOT appear as G1!
    g1_prereqs = {g.get("prerequisite") for g in res["gaps"] if g["gap_type"] == "G1"}
    assert "Computational Graphs" not in g1_prereqs
    # Strict mode must flag strict compliance
    for g in res["gaps"]:
        if g["gap_type"] == "G1":
            assert g["respects_strict_source_policy"] is True
            assert g["recommended_action"] == "flag_gap_or_source_compatible_bridge"


# ---------------------------------------------------------------------------
# F05 — Intelligent Collection Size Negotiation (Scenario C)
# ---------------------------------------------------------------------------

def test_f05_unmanageable_scope_negotiation_and_honesty():
    orch = OrchestrationEngine(ROOT)
    prefs = ResolvedNotePreferences(
        learning_objective="conceptual_mastery",
        master="M1",
        variant=None,
        depth="exhaustive",
        prior_knowledge={"level": "beginner"},
        organization="hierarchical_collection",
        emphasis=[],
        source_policy="adaptive",
    )
    neg = orch.negotiate_scope(
        "Computer Science",
        "/scribe-notes Everything about Computer Science in exhaustive detail",
        prefs,
        planned_note_count=30,
    )
    assert neg["needs_negotiation"] is True
    assert neg["exhaustive_completeness_claimed"] is False
    assert len(neg["packages"]) >= 4


# ---------------------------------------------------------------------------
# F06 — Dependency-Aware Checkpoints, Failure Injection & Idempotent Resume (Scenario D)
# ---------------------------------------------------------------------------

def test_f06_checkpointed_generation_failure_recovery_and_idempotent_resume(tmp_path):
    orch = OrchestrationEngine(ROOT)
    vault = VaultEngine()
    quality = QualityEngine(ROOT)

    plan, prefs = _make_ml_plan_and_prefs(depth="standard")
    kcp = orch.build_kcp(tmp_path, plan, prefs)

    # 1. Inject failure on 6th child node
    target_fail = [n.concept_id for n in plan.nodes if n.note_role == "child"][5]
    run1 = vault.generate_with_checkpoints(tmp_path, kcp, prefs, batch_size=3, fail_on_concept_id=target_fail)
    assert run1["complete"] is False
    assert run1["failed_count"] == 1
    assert run1["note_states"][target_fail] == "FAILED"
    # Root index MUST be deferred, never falsely marked committed while a child failed!
    assert run1["note_states"][plan.root_topic_id] == "DEFERRED"
    assert Path(run1["checkpoint_path"]).is_file()

    # 2. Resume cleanly -> skips already-committed notes, completes failed + deferred indexes idempotently!
    run2 = vault.generate_with_checkpoints(tmp_path, kcp, prefs, batch_size=3, resume=True)
    assert run2["complete"] is True
    assert run2["failed_count"] == 0
    assert run2["skipped_already_committed"] >= 5
    assert run2["note_states"][plan.root_topic_id] == "COMMITTED"

    val = quality.validate_collection(tmp_path, plan, manifest=run2["manifest"])
    assert val["valid"] is True, val["issues"]


# ---------------------------------------------------------------------------
# F07 — Adaptive Note Granularity Revision (Scenario E)
# ---------------------------------------------------------------------------

def test_f07_granularity_split_preserves_canonical_id_and_bounds_revisions():
    ped = PedagogyEngine()
    prefs = ResolvedNotePreferences(
        learning_objective="conceptual_mastery",
        master="M1",
        variant=None,
        depth="comprehensive",
        prior_knowledge={"level": "intermediate"},
        organization="single_note",
        emphasis=[],
        source_policy="adaptive",
    )
    node = TopicNode(
        concept_id="ml.opt.gd_variants",
        title="Gradient Descent Variants",
        parent_id=None,
        proposed_path="Optimization/Gradient Descent Variants.md",
        note_role="single",
        template_plan={"master": "M1"},
    )
    plan = NoteCollectionPlan(
        collection_id="col-gdv",
        title="Gradient Descent Variants",
        root_topic_id="ml.opt.gd_variants",
        organization="single_note",
        nodes=[node],
        planned_paths=[node.proposed_path],
        learning_order=[node.concept_id],
        generation_order=[node.concept_id],
    )

    ev = ped.evaluate_granularity(plan, prefs, committed_paths={"Optimization/Gradient Descent Variants.md"})
    assert len(ev["proposed_changes"]) == 1
    assert ev["proposed_changes"][0]["action"] == "split"
    assert ev["proposed_changes"][0]["requires_approval"] is True

    split_plan = ped.split_note_in_plan(plan, node.concept_id, ev["proposed_changes"][0]["proposed_children"])
    assert split_plan.organization == "hierarchical_collection"
    assert len(split_plan.nodes) == 4  # 1 group/root index + 3 child notes
    assert any(n.concept_id == "ml.opt.gd_variants" for n in split_plan.nodes)

    # Verify bounded revision cap prevents oscillation
    capped = ped.evaluate_granularity(split_plan, prefs, max_revisions=2, current_revision_count=2)
    assert capped["revision_cap_reached"] is True


# ---------------------------------------------------------------------------
# F08 — Cross-Note Learning Path Generation
# ---------------------------------------------------------------------------

def test_f08_learning_paths_order_known_skips_and_cycle_handling():
    ped = PedagogyEngine()
    plan, prefs = _make_ml_plan_and_prefs()
    lp = ped.generate_learning_paths(plan, prefs, strategy="math_first", known_concepts=["What is Machine Learning"])
    assert lp["strategy"] == "math_first"
    assert lp["cycles_detected"] == []
    assert lp["distinct_from_folder_hierarchy"] is True
    # Known concept is marked skippable but stays in full_prerequisite_order
    known_step = next(s for s in lp["steps"] if s["title"] == "What is Machine Learning")
    assert known_step["skippable_known_concept"] is True
    assert known_step["keep_prerequisite_link"] is True
    assert known_step["concept_id"] not in lp["active_reading_order"]
    assert known_step["concept_id"] in lp["full_prerequisite_order"]

    # Prerequisite always precedes dependent in full_prerequisite_order
    idx_loss = lp["full_prerequisite_order"].index(next(n.concept_id for n in plan.nodes if n.title == "Loss Functions"))
    idx_gd = lp["full_prerequisite_order"].index(next(n.concept_id for n in plan.nodes if n.title == "Gradient Descent"))
    assert idx_loss < idx_gd


# ---------------------------------------------------------------------------
# F09 — Collection-Wide Terminology & Notation Registry (Scenario F)
# ---------------------------------------------------------------------------

def test_f09_terminology_scoping_source_notation_and_conflict_detection():
    know = KnowledgeEngine()
    reg = know.create_terminology_registry()

    # Same symbol 'T' in three different scopes -> ZERO conflict!
    reg.register_notation(concept_id="phys.temp", preferred_term="temperature", preferred_symbol="T", scope="thermodynamics", units="K")
    reg.register_notation(concept_id="la.transpose", preferred_term="transpose", preferred_symbol="T", scope="linear_algebra")
    reg.register_notation(concept_id="nlp.seq_len", preferred_term="sequence_length", preferred_symbol="T", scope="transformers")
    reg.register_notation(concept_id="ml.loss", preferred_term="loss_function", preferred_symbol="J", accepted_symbols=["L", "E"], scope="machine_learning")

    ok = reg.validate_consistency([
        {"concept_id": "ml.loss", "symbol": "E", "source_specific": True, "mapping_explained": True},
        {"concept_id": "phys.temp", "symbol": "T", "units": "K"},
    ])
    assert ok["consistent"] is True
    assert ok["mappings_explained"]

    # Unit mismatch + unexplained alias + same-scope symbol collision -> caught!
    reg.register_notation(concept_id="phys.period", preferred_term="period", preferred_symbol="T", scope="thermodynamics", units="s")
    bad = reg.validate_consistency([
        {"concept_id": "ml.loss", "symbol": "L", "mapping_explained": False},
        {"concept_id": "phys.temp", "symbol": "T", "units": "Celsius"},
    ])
    assert bad["consistent"] is False
    types = {c["type"] for c in bad["conflicts"]}
    assert {"same_scope_symbol_collision", "unexplained_symbol_alias", "unit_inconsistency"} <= types


# ---------------------------------------------------------------------------
# F10 (Synthesis M7), F11 (Progressive Disclosure), F12 (Outcomes), F13 (Assessment M6)
# ---------------------------------------------------------------------------

def test_f10_f11_f12_f13_synthesis_disclosure_outcomes_and_assessment(tmp_path):
    ped = PedagogyEngine()
    quality = QualityEngine(ROOT)
    vault = VaultEngine()
    plan, prefs = _make_ml_plan_and_prefs(depth="comprehensive")

    # F10: Cross-note synthesis reusing M7
    synths = ped.plan_synthesis_notes(plan, prefs)
    assert len(synths) >= 1
    s0 = synths[0]
    assert s0["master"] == "M7"
    assert s0["note_type"] == "synthesis-revision"
    assert "[[Gradient Descent]]" in s0["content"]
    assert quality.validate_properties(s0["content"]) == []

    # F11: Progressive disclosure (M1 adds optional collapsed advanced callout while keeping essentials visible)
    vault.generate_collection(tmp_path, plan, prefs)
    gd_node = next(n for n in plan.nodes if n.title == "Gradient Descent")
    gd_text = (tmp_path / gd_node.proposed_path).read_text(encoding="utf-8")
    pd_res = ped.apply_progressive_disclosure(gd_text, master="M1", topic="Gradient Descent", advanced_note="Nesterov acceleration improves convergence rate on L-smooth convex losses.")
    assert pd_res["essential_content_visible"] is True
    assert "> [!note]- Advanced Considerations" in pd_res["content"]

    # F12: Learning outcomes & competency coverage (never claims learner mastery!)
    outcomes = ped.define_learning_outcomes(gd_node, prefs)
    cov = quality.validate_competencies(gd_text, outcomes)
    assert cov["covered"] is True
    assert cov["claims_learner_mastery"] is False

    # F13: Collection-wide assessment blueprint reusing M6
    comp_map = {n.concept_id: ped.define_learning_outcomes(n, prefs) for n in plan.nodes if n.note_role == "child"}
    assess = ped.build_collection_assessment(plan, prefs, comp_map, answer_mode="hints_then_solutions")
    assert assess["master"] == "M6"
    assert assess["is_pre_generation_diagnostic"] is False
    assert "integrative" in assess["skill_types_covered"]
    assert quality.validate_properties(assess["content"], expected_note_type="assessment") == []


# ---------------------------------------------------------------------------
# F14 (Change-Impact) & F15 (Post-Generation Personalization) (Scenarios K & L)
# ---------------------------------------------------------------------------

def test_f14_change_impact_formatting_vs_equation_correction():
    know = KnowledgeEngine()
    plan, _ = _make_ml_plan_and_prefs()
    gd_cid = next(n.concept_id for n in plan.nodes if n.title == "Gradient Descent")

    base = "---\ntopic: Gradient Descent\ntags: [domain/ai]\nmaster_topic: ML\ndomain: AI\nnote_type: deep-notes\n---\n\n# Gradient Descent\n\n## Convergence\nRequires $0 < \\alpha < 2/L$.\n"
    fmt_only = base.replace("Requires $0", "Requires  $0")
    eq_fixed = base.replace("2/L", "1/L")

    # Formatting-only -> zero downstream review!
    res_fmt = know.analyze_collection_change_impact(plan, gd_cid, base, fmt_only)
    assert res_fmt["change_type"] == "formatting"
    assert res_fmt["requires_downstream_review"] is False
    assert res_fmt["review_queue"] == []

    # Equation correction -> targeted downstream review queue!
    res_eq = know.analyze_collection_change_impact(plan, gd_cid, base, eq_fixed)
    assert res_eq["change_type"] == "equation_correction"
    assert res_eq["requires_downstream_review"] is True
    assert any("Regularization" in item["title"] or "Optimization" in item["title"] for item in res_eq["review_queue"])


def test_f15_post_generation_feedback_approval_safety_and_cli(tmp_path):
    vault = VaultEngine()
    quality = QualityEngine(ROOT)
    plan, prefs = _make_ml_plan_and_prefs()
    vault.generate_collection(tmp_path, plan, prefs)

    gd_node = next(n for n in plan.nodes if n.title == "Gradient Descent")
    gd_path = tmp_path / gd_node.proposed_path
    # Add a personal section to prove F15 never destroys unrelated user content
    orig_text = gd_path.read_text(encoding="utf-8") + "\n## Personal Notes\nMy private study reminder.\n"
    gd_path.write_text(orig_text, encoding="utf-8")

    # 1. Without approval (apply_approved=False) -> proposes repair, disk untouched!
    prop = quality.process_feedback(
        tmp_path,
        plan,
        "The mathematical motivation in Gradient Descent is too fast and confusing.",
        apply_approved=False,
    )
    assert prop["status"] == "proposal_ready"
    assert prop["applied"] is False
    assert prop["claims_learner_mastery"] is False
    assert gd_path.read_text(encoding="utf-8") == orig_text

    # 2. With approval via CLI `scribe.py notes refine --apply` -> applies localized update safely!
    proc = subprocess.run(
        [
            PYTHON, "-B", str(ROOT / "scripts" / "scribe.py"),
            "notes", "refine",
            "--vault", str(tmp_path),
            "--feedback", "The mathematical motivation in Gradient Descent is too fast.",
            "--apply",
        ],
        capture_output=True, text=True, check=True,
    )
    out = json.loads(proc.stdout)
    assert out["status"] == "applied"
    assert out["applied"] is True
    updated_text = gd_path.read_text(encoding="utf-8")
    assert "My private study reminder." in updated_text
    assert "Step-by-Step Intuition" in updated_text
    assert quality.validate_properties(updated_text) == []
