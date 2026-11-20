"""Golden Evaluation & Cross-Domain Suite for the Explanation Intelligence System (EIS-01..EIS-07)."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from scriptorium import (
    ExplanationBlueprint,
    PedagogyEngine,
    QualityEngine,
    VaultEngine,
)
from scriptorium.engines._explanation import INTERNAL_BLUEPRINT_HEADINGS_RE


# ===========================================================================
# GROUP A — EXPLANATORY SPINE (A1-A4)
# ===========================================================================

def test_a1_disconnected_facts_become_coherent_prose_without_blueprint_leakage():
    ped = PedagogyEngine()
    qual = QualityEngine(ROOT)
    vault = VaultEngine()

    bp = ped.build_explanation_blueprint("Gradient Descent", master="M1", audience="intermediate")
    note = ped.compose_explanation(bp)

    assert note.startswith("---\n")
    assert vault.validate_properties(note, expected_note_type="deep-notes") == []
    assert INTERNAL_BLUEPRINT_HEADINGS_RE.search(note) is None
    assert "loss" in note.lower() and "gradient" in note.lower() and "learning rate" in note.lower()

    review = qual.review_explanatory_clarity(note, bp, learner_profile="intermediate")
    assert review["passed"] is True, review


def test_a2_abrupt_formula_drop_without_transition_detected():
    ped = PedagogyEngine()
    qual = QualityEngine(ROOT)
    bp = ped.build_explanation_blueprint("Gradient Descent", master="M1")
    abrupt = (
        "---\ntopic: Gradient Descent\ntags: [domain/artificial-intelligence]\n"
        "master_topic: Machine Learning\ndomain: Artificial Intelligence\nnote_type: deep-notes\n---\n\n"
        "# Gradient Descent\n\n"
        "## Update Rule\n"
        "$$\\theta_{t+1} = \\theta_t - \\alpha \\nabla J(\\theta_t)$$\n"
    )
    review = qual.review_explanatory_clarity(abrupt, bp, learner_profile="beginner")
    codes = {i["type"] for i in review["friction_issues"]}
    assert "CF-04" in codes


def test_a3_strict_source_order_preserved_and_reordering_flagged():
    ped = PedagogyEngine()
    qual = QualityEngine(ROOT)
    facts = [
        "First, empirical risk averages the per-sample loss over the training set.",
        "Second, gradient evaluation computes partial derivatives with respect to each weight.",
        "Third, stepping opposite the gradient updates the parameter vector.",
    ]
    bp = ped.build_explanation_blueprint(
        "Gradient Descent",
        master="M2",
        source_mode="strict",
        preserve_source_order=True,
        source_facts=facts,
    )
    note = ped.compose_explanation(bp, source_facts=facts)
    assert note.find(facts[0]) < note.find(facts[1]) < note.find(facts[2])
    assert ped.validate_explanation(note, bp) == []

    # Deliberately reorder facts -> EIS-SPINE-003 caught
    reordered = note.replace(facts[0], "TMP").replace(facts[2], facts[0]).replace("TMP", facts[2])
    issues = ped.validate_explanation(reordered, bp)
    assert any(i["code"] == "EIS-SPINE-003" for i in issues)


def test_a4_false_causality_on_noncausal_topic_flagged():
    ped = PedagogyEngine()
    bp = ped.build_explanation_blueprint("Correlation and Causation", master="M1", concept_type="conceptual")
    assert bp.explanatory_spine["relation_type"] == "conceptual_association"
    bad_causal = (
        "---\ntopic: Correlation and Causation\ntags: [domain/general]\n"
        "master_topic: General Knowledge\ndomain: General\nnote_type: deep-notes\n---\n\n"
        "# Correlation and Causation\n\n## Link\nStrong correlation proves causation in observational data.\n"
    )
    issues = ped.validate_explanation(bad_causal, bp)
    assert any(i["code"] == "EIS-SPINE-002" for i in issues)


# ===========================================================================
# GROUP B — CENTRAL QUESTIONS & ANTICIPATION (B1-B4)
# ===========================================================================

def test_b1_b2_central_question_and_backprop_anticipation():
    ped = PedagogyEngine()
    bp_nn = ped.build_explanation_blueprint("Neural Networks", master="M1")
    assert bp_nn.central_question["question"].endswith("?")

    bp_bp = ped.build_explanation_blueprint("Backpropagation", master="M1")
    assert "efficiently" in bp_bp.central_question["question"].lower()
    q_ids = [q["question_id"] for q in bp_bp.anticipated_questions]
    assert "why_chain_rule" in q_ids and "why_reverse_mode" in q_ids


def test_b3_question_explosion_detected():
    ped = PedagogyEngine()
    bp = ped.build_explanation_blueprint("Loss Function", master="M1", concept_type="definition")
    faq_spam = (
        "---\ntopic: Loss Function\ntags: [domain/artificial-intelligence]\n"
        "master_topic: Machine Learning\ndomain: Artificial Intelligence\nnote_type: deep-notes\n---\n\n"
        "# Loss Function\n\n"
        "## What is a loss?\nError.\n\n"
        "## Why is there a loss?\nPredictions err.\n\n"
        "## How do we calculate loss?\nCompare y and y_hat.\n\n"
        "## Why is calculating loss useful?\nGuides training.\n"
    )
    issues = ped.validate_explanation(faq_spam, bp)
    assert any(i["code"] == "EIS-Q-002" for i in issues)


def test_b4_cheat_sheet_mode_keeps_questions_minimal_and_compact():
    ped = PedagogyEngine()
    bp = ped.build_explanation_blueprint("Gradient Descent", master="M3")
    assert bp.activation_levels["eis_02_questions"] == "lightweight"
    assert len(bp.anticipated_questions) <= 1
    note = ped.compose_explanation(bp)
    assert "guiding question" not in note.lower()
    assert "## Core Reference" in note


# ===========================================================================
# GROUP C — MATHEMATICAL & CAUSAL MOTIVATION (C1-C4)
# ===========================================================================

def test_c1_c2_c3_c4_motivation_shortcuts_local_vs_global_and_history():
    ped = PedagogyEngine()
    bp_gd = ped.build_explanation_blueprint("Gradient Descent", master="M1")

    # C1: Unmotivated algebraic step narration
    unmotivated = "# GD\n\n## Steps\nNow differentiate both sides. Substitute the values.\n"
    issues_c1 = ped.validate_explanation(unmotivated, bp_gd)
    assert any(i["code"] == "EIS-MOTIV-001" for i in issues_c1)

    # C2: Invalid mathematical shortcut
    bad_alg = "# Algebra\n\n## Expand\nNote that (a + b)^2 = a^2 + b^2.\n"
    issues_c2 = ped.validate_explanation(bad_alg, bp_gd)
    assert any(i["code"] == "EIS-MOTIV-003" for i in issues_c2)

    # C3: Local vs global overclaim rejected
    overclaim = "# GD\n\n## Result\nGradient descent always finds the global minimum for any neural network.\n"
    issues_c3 = ped.validate_explanation(overclaim, bp_gd)
    assert any(i["code"] == "EIS-MOTIV-002" for i in issues_c3)

    # C4: Historical topic avoids false determinism & notes competing interpretations
    bp_hist = ped.build_explanation_blueprint("French Revolution", master="M1", concept_type="historical")
    assert bp_hist.mechanism["causality_justified"] is False
    assert "competing_interpretations" in bp_hist.explanatory_spine["domain_pattern"]


# ===========================================================================
# GROUP D — BOUNDARIES & CONTRASTS (D1-D4)
# ===========================================================================

def test_d1_d2_d3_d4_boundaries_contrasts_and_no_caveat_bloat():
    ped = PedagogyEngine()

    # D1: Binary search unsorted overclaim
    bp_bs = ped.build_explanation_blueprint("Binary Search", master="M5")
    bad_bs = "# Binary Search\n\n## Complexity\nBinary search always finds an element in O(log n) time.\n"
    assert any(i["code"] == "EIS-BOUND-001" for i in ped.validate_explanation(bad_bs, bp_bs))

    # D3: Parameter vs hyperparameter contrast
    bp_gd = ped.build_explanation_blueprint("Gradient Descent", master="M1")
    pairs = {(c["concept_a"], c["concept_b"]) for c in bp_gd.contrasts}
    assert ("Parameter", "Hyperparameter") in pairs

    # D4: Simple definition avoids unnecessary caveat blocks
    bp_def = ped.build_explanation_blueprint("Scalar", master="M1", concept_type="definition", complexity="trivial")
    assert bp_def.boundaries.get("minimal_caveats_only") is True
    note_def = ped.compose_explanation(bp_def)
    assert "Applicability Conditions and Distinctions" not in note_def


# ===========================================================================
# GROUP E — VARIABLE ROLES, INVARIANTS & STATE REASONING (E1-E5)
# ===========================================================================

def test_e1_e2_e3_e4_e5_state_traces_invariants_and_nonprocedural_guard():
    ped = PedagogyEngine()

    # E1: Binary search verified trace & invariant
    bp_bs = ped.build_explanation_blueprint("Binary Search", master="M5")
    assert bp_bs.execution_state["applicable"] is True
    assert bp_bs.execution_state["invariant"]["applicable"] is True
    assert ped.verify_trace(bp_bs.execution_state["example_trace"], rule="binary_search")["valid"] is True

    # E2: Gradient descent exact numerical trace (4.0 -> 3.2 -> 2.56 -> 2.048)
    bp_gd = ped.build_explanation_blueprint("Gradient Descent", master="M1")
    trace = bp_gd.execution_state["example_trace"]
    assert [row["theta"] for row in trace] == [4.0, 3.2, 2.56, 2.048]
    assert [row["loss"] for row in trace] == [16.0, 10.24, 6.5536, 4.1943]
    assert ped.verify_trace(trace, rule="quadratic_gd", alpha=0.1)["valid"] is True

    # E3: Recursion trace
    bp_rec = ped.build_explanation_blueprint("Recursion", master="M5")
    assert bp_rec.execution_state["applicable"] is True
    assert any(r.get("returns") == 6 for r in bp_rec.execution_state["example_trace"])

    # E4: Nonprocedural concept disables traces and flags forced loop invariants
    bp_cc = ped.build_explanation_blueprint("Correlation and Causation", master="M1")
    assert bp_cc.execution_state["applicable"] is False
    assert bp_cc.execution_state["invariant"]["applicable"] is False
    forced = "# Correlation\n\n## Loop Invariant\nIteration | State\n"
    assert any(i["code"] == "EIS-STATE-003" for i in ped.validate_explanation(forced, bp_cc))

    # E5: Invalid trace / violated descent invariant rejected
    bad_trace = [{"iteration": 0, "theta": 4.0, "loss": 16.0}, {"iteration": 1, "theta": 5.0, "loss": 25.0}]
    res_bad = ped.verify_trace(bad_trace, rule="quadratic_gd", alpha=0.1)
    assert res_bad["valid"] is False
    assert any("invariant violated" in e for e in res_bad["errors"])


# ===========================================================================
# GROUP F — RETRIEVAL RECONSTRUCTION (F1-F4)
# ===========================================================================

def test_f1_f2_f3_f4_retrieval_cues_assumptions_master_modes_and_inflation():
    ped = PedagogyEngine()

    # F1 & F2: Cues & preserved assumptions, never claiming measured human retention
    bp_gd = ped.build_explanation_blueprint("Gradient Descent", master="M1")
    ret = bp_gd.retrieval
    assert ret["cues"] == ["objective", "direction", "magnitude", "iteration"]
    assert "0 < α < 2/L" in ret["summary"]
    assert ret["claims_measured_retention"] is False

    # F3: M7 deep retrieval vs M6 answer-leak protection
    bp_m7 = ped.build_explanation_blueprint("Gradient Descent", master="M7")
    assert bp_m7.activation_levels["eis_06_retrieval"] == "deep"
    bp_m6 = ped.build_explanation_blueprint("Gradient Descent", master="M6")
    assert bp_m6.retrieval["internal_only"] is True
    assert bp_m6.retrieval["summary"] == ""

    # F4: Summary inflation flagged
    bloated = "# GD\n\n## Summary\nA.\n\n## Key Takeaways\nB.\n\n## Recap\nC.\n"
    assert any(i["code"] == "EIS-RET-003" for i in ped.validate_explanation(bloated, bp_gd))


# ===========================================================================
# GROUP G — READER SIMULATION & COGNITIVE FRICTION (G1-G7)
# ===========================================================================

def test_g1_to_g7_reader_simulation_friction_and_strict_source_repair():
    qual = QualityEngine(ROOT)
    ped = PedagogyEngine()
    bp = ped.build_explanation_blueprint("Gradient Descent", master="M1", audience="beginner")

    noisy_draft = (
        "---\ntopic: Gradient Descent\ntags: [domain/artificial-intelligence]\n"
        "master_topic: Machine Learning\ndomain: Artificial Intelligence\nnote_type: deep-notes\n---\n\n"
        "# Gradient Descent\n\n"
        "## Introduction\n"
        "Gradient descent is just like rolling a ball down a hill over a Hessian manifold. "
        "It reduces the error quickly. "
        "Gradient descent updates parameters iteratively using the negative gradient. "
        "Gradient descent updates parameters iteratively using the negative gradient.\n\n"
        "## Update\n"
        "$$\\theta_{t+1} = \\theta_t - \\lambda \\nabla f(\\theta_t)$$\n"
        "Now differentiate both sides. Hence the method converges.\n"
    )
    rev_beg = qual.review_explanatory_clarity(noisy_draft, bp, learner_profile="beginner")
    assert rev_beg["hypothetical_review"] is True
    assert rev_beg["claims_measured_mastery"] is False
    assert rev_beg["passed"] is False
    codes = {i["type"] for i in rev_beg["friction_issues"]}
    assert "CF-11" in codes  # G1: premature jargon (Hessian/manifold) for beginner
    assert "CF-03" in codes  # unmotivated differentiation
    assert "CF-06" in codes  # repeated sentence
    assert "CF-07" in codes  # hidden assumption for convergence
    assert "CF-08" in codes  # G5: analogy without breakdown disclosure
    assert "CF-09" in codes  # G4: ambiguous "It reduces..."

    # G6: Advanced reader suppresses beginner-only jargon warnings (CF-01 / CF-11)
    rev_adv = qual.review_explanatory_clarity(noisy_draft, bp, learner_profile="advanced")
    adv_codes = {i["type"] for i in rev_adv["friction_issues"]}
    assert "CF-01" not in adv_codes and "CF-11" not in adv_codes

    # G7: Strict source-only mode blocks external factual additions during repair, allows editorial clarification
    blocked = qual.repair_clarity(
        noisy_draft,
        find_text="It reduces the error quickly.",
        replace_text="According to Cauchy (1847), the descent step reduces the error quickly.",
        issue_code="CF-09",
        source_mode="strict",
        introduces_external_facts=True,
    )
    assert blocked["repaired"] is False and blocked["blocked_by_source_policy"] is True

    editorial = qual.repair_clarity(
        noisy_draft,
        find_text="It reduces the error quickly.",
        replace_text="The negative-gradient update reduces the loss locally.",
        issue_code="CF-09",
        source_mode="strict",
        introduces_external_facts=False,
    )
    assert editorial["repaired"] is True
    assert "The negative-gradient update reduces the loss locally." in editorial["content"]


# ===========================================================================
# PART 20 — CROSS-DOMAIN REGRESSION & SCRIBE CLI INTEGRATION
# ===========================================================================

@pytest.mark.parametrize(("topic", "master", "expected_domain"), [
    ("Chain Rule", "M1", "Mathematics"),
    ("Binary Search", "M5", "Computer Science"),
    ("Backpropagation", "M1", "Artificial Intelligence"),
    ("Biot–Savart Law", "M1", "Physics"),
    ("Correlation and Causation", "M7", "General"),
])
def test_cross_domain_blueprint_compose_properties_and_zero_blueprint_leaks(topic, master, expected_domain):
    ped = PedagogyEngine()
    vault = VaultEngine()
    bp = ped.build_explanation_blueprint(topic, master=master)
    note = ped.compose_explanation(bp)
    assert vault.validate_properties(note) == []
    assert INTERNAL_BLUEPRINT_HEADINGS_RE.search(note) is None
    assert bp.to_dict()["schema_version"] == "1.0"
    if expected_domain != "General":
        assert f"domain: {expected_domain}" in note


def test_scribe_explain_cli_and_no_script_proliferation(tmp_path):
    # Ensure zero new scripts added to scripts/
    assert len(list((ROOT / "scripts").glob("*.py"))) == 8

    # 1. Blueprint JSON via scribe.py explain
    p_bp = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "scribe.py"), "explain", "--topic", "Chain Rule", "--master", "M1"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    bp_json = json.loads(p_bp.stdout)
    assert bp_json["schema_version"] == "1.0"
    assert bp_json["central_question"]["question"].endswith("?")

    # 2. Composed note with Obsidian Properties via --compose + clarity review via --review
    p_comp = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "scribe.py"), "explain", "--topic", "Binary Search", "--master", "M5", "--compose"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    assert p_comp.stdout.startswith("---\n")
    out_file = tmp_path / "binary_search.md"
    out_file.write_text(p_comp.stdout, encoding="utf-8")

    p_rev = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "scribe.py"), "explain", "--topic", "Binary Search", "--master", "M5", "--review", str(out_file)],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    rev = json.loads(p_rev.stdout)
    assert rev["passed"] is True
