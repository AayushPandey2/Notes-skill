"""Comprehensive Verification Suite for Scriptorium Teaching-Architecture Reconstruction (T01-T18, Parts 6, 24, 25, 26)."""
from __future__ import annotations

import binascii
import hashlib
from pathlib import Path
import re
import struct
import sys
import zlib

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scriptorium import (
    OrchestrationEngine,
    PedagogyEngine,
    QualityEngine,
    VaultEngine,
    parse_note,
)
from scriptorium.engines import mathematics as math_eng
from scriptorium.engines.composition import (
    build_composition,
    bvia,
    contracts,
    lavia,
    media,
    prepare_composition,
    publish_composition,
    resolve_collection_layout,
)
from scriptorium.engines.quality import (
    BEGINNER_READER_SIMULATION_QUESTIONS,
    TEACHING_QUALITY_DIMENSIONS,
)

PROTECTED_REGRESSION_NOTE = Path(
    r"C:\Users\aayus\OneDrive\Desktop\Notes Vault\6 - Full Notes\6 - Full Notes\Supervised Learning\02 - Linear and Regularized Regression.md"
)
PROTECTED_REGRESSION_SHA256 = "A1548AE0BFE8E19CF45506A5501378775D09CD81A608F01FF46F34A693B5D84C"


def _png_bytes(width: int = 440, height: int = 260) -> bytes:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    raw = b"".join(b"\x00" + (b"\x14\x32\x64" if (y % 24) < 12 else b"\xe8\xf0\xf8") * width for y in range(height))
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


# ---------------------------------------------------------------------------
# T01 & T17 — Source Comparison Integrity & Read-Only Protected Baseline
# ---------------------------------------------------------------------------

def test_t01_t17_protected_reference_unchanged_and_defects_detected():
    if not PROTECTED_REGRESSION_NOTE.is_file():
        pytest.skip("External read-only reference note not present on this host")
    actual_sha = hashlib.sha256(PROTECTED_REGRESSION_NOTE.read_bytes()).hexdigest().upper()
    assert actual_sha == PROTECTED_REGRESSION_SHA256

    source_a_text = PROTECTED_REGRESSION_NOTE.read_text(encoding="utf-8-sig")
    qe = QualityEngine(ROOT)
    # Existing compressed reference note must fail the new beginner teaching & math deconstruction gate.
    audit = qe.evaluate_teaching(source_a_text, learner_level="beginner")
    assert audit["passed"] is False
    assert audit["critical_defects"] or audit["failing_dimensions"]
    assert any("Claim stub" in d or "stub" in d.lower() for d in audit["critical_defects"])


# ---------------------------------------------------------------------------
# T02, T03, T04 — Formula Prep, Symbols & Vector/Matrix Shapes (Part 6.1 Oracle)
# ---------------------------------------------------------------------------

def test_t02_t03_t04_part6_regression_prediction_math_oracle():
    ped = PedagogyEngine()

    # Matrix dimension compatibility checks (T04)
    bad_dim = ped.check_matrix_dimensions(
        [{"name": "w", "shape": [3, 1]}, {"name": "x", "shape": [3, 1]}],
        operation="matmul",
    )
    assert bad_dim["valid"] is False
    assert "Dimension mismatch" in bad_dim["error"]

    good_dim = ped.check_matrix_dimensions(
        [{"name": "w", "shape": [3, 1], "transpose": True}, {"name": "x", "shape": [3, 1]}],
        operation="matmul",
    )
    assert good_dim["valid"] is True
    assert good_dim["output_shape"] == (1, 1)
    assert good_dim["output_type"] == "scalar"

    # Full M01-M14 deconstruction of y_hat = w^T x + b (Part 6.1 test oracle)
    spec = {
        "equation": r"\hat{y} = \mathbf{w}^T \mathbf{x} + b",
        "purpose": "This equation calculates one scalar prediction by multiplying each input feature by its learned weight, summing the contributions, and adding a baseline bias.",
        "pronunciation": "y-hat equals w transpose times x plus b (or the dot product of w and x, plus bias b).",
        "symbols": [
            {"symbol": r"\hat{y}", "meaning": "predicted output value", "type": "scalar", "shape": "1x1", "role": "final prediction"},
            {"symbol": r"\mathbf{w}", "meaning": "weight column vector", "type": "vector", "shape": "3x1", "role": "feature slopes"},
            {"symbol": r"\mathbf{w}^T", "meaning": "transposed weight row vector", "type": "vector", "shape": "1x3", "role": "row orientation for valid matrix multiplication"},
            {"symbol": r"\mathbf{x}", "meaning": "input feature column vector", "type": "vector", "shape": "3x1", "role": "observed inputs"},
            {"symbol": "b", "meaning": "scalar bias intercept", "type": "scalar", "shape": "1x1", "role": "baseline value when features equal zero"},
        ],
        "dimension_operands": [{"name": "w", "shape": [3, 1], "transpose": True}, {"name": "x", "shape": [3, 1]}],
        "dimension_operation": "matmul",
        "expanded_form": r"\mathbf{w}^T\mathbf{x} + b = w_1 x_1 + w_2 x_2 + w_3 x_3 + b",
        "operation_breakdown": [
            "Transpose column vector w (3x1) into row vector w^T (1x3).",
            "Multiply w^T (1x3) by column vector x (3x1), multiplying corresponding entries and summing to one (1x1) scalar.",
            "Add scalar bias b to shift the baseline prediction.",
        ],
        "numerical_example": {
            "inputs": {"w1": 2, "w2": 3, "w3": 4, "x1": 5, "x2": 6, "x3": 7, "b": 1},
            "steps": [
                {"label": "term_1", "assign": "t1", "expr": "w1 * x1", "result": 10, "explanation": "first feature contribution"},
                {"label": "term_2", "assign": "t2", "expr": "w2 * x2", "result": 18, "explanation": "second feature contribution"},
                {"label": "term_3", "assign": "t3", "expr": "w3 * x3", "result": 28, "explanation": "third feature contribution"},
                {"label": "dot_sum", "assign": "dot", "expr": "t1 + t2 + t3", "result": 56, "explanation": "combined weighted sum"},
                {"label": "final_prediction", "assign": "y_hat", "expr": "dot + b", "result": 57, "explanation": "add bias baseline"},
            ],
            "expected_result": 57,
            "interpretation": "With weights [2, 3, 4], features [5, 6, 7], and bias 1, the predicted output is 57.",
            "sanity_check": "Increasing any positive weight or positive input increases the prediction; (1x3)(3x1) produces a scalar.",
        },
        "misconceptions": [
            "Two 3x1 column vectors cannot be matrix-multiplied directly without transposing the first vector.",
        ],
        "generalization": "For d features, the sum extends from i=1 to d while producing a scalar prediction.",
    }
    decon = ped.deconstruct_math(spec, learner_level="beginner")
    assert decon["calculation_check"]["final_value"] == 57.0
    assert "57" in decon["markdown"]
    assert "y-hat equals w transpose times x plus b" in decon["markdown"]
    assert "(1×3) × (3×1) = (1×1)" in decon["markdown"]

    # Equation-dumping & abrupt heading-into-$$ check (T02 / T08)
    bad_note = "# Equations\n\n$$\n\\hat{y} = \\mathbf{w}^T \\mathbf{x} + b\n$$\n\n$$\nJ(w) = \\|y - Xw\\|_2^2\n$$\n"
    mcheck = ped.verify_math_teaching(bad_note, learner_level="beginner")
    assert mcheck["passed"] is False
    codes = {i["code"] for i in mcheck["issues"]}
    assert {"MATH-DECON-01", "MATH-DECON-02", "MATH-DECON-03", "MATH-DECON-05"} <= codes


# ---------------------------------------------------------------------------
# T05, T06, T07 — Intermediate Steps & 12-Step Numerical Verification
# ---------------------------------------------------------------------------

def test_t05_t06_t07_worked_numerical_verification_catches_errors():
    ped = PedagogyEngine()

    # Deterministic arithmetic verifier catches wrong intermediate/final values (T07)
    with pytest.raises(ValueError, match="disagrees"):
        ped.build_worked_problem(
            {
                "title": "Faulty Ridge Shrinkage",
                "problem": "Compute 1D orthogonal Ridge weight.",
                "given": {"w_ols": 3.0, "lam": 1.5},
                "find": "w_ridge",
                "assumptions": ["orthonormal coordinates"],
                "formula": r"w_{\text{ridge}} = \frac{w_{\text{ols}}}{1 + \lambda}",
                "steps": [
                    {"label": "denominator", "assign": "denom", "expr": "1 + lam", "result": 2.5},
                    {"label": "shrink", "assign": "w_ridge", "expr": "w_ols / denom", "result": 2.0},  # wrong! actual 1.2
                ],
                "expected_result": 1.2,
            }
        )

    valid_prob = ped.build_worked_problem(
        {
            "title": "1D Ridge Shrinkage",
            "problem": "Compute 1D Ridge weight when OLS gives 3.0 and penalty lambda is 1.5.",
            "given": {"w_ols": 3.0, "lam": 1.5},
            "find": "w_ridge",
            "assumptions": ["orthonormal coordinates with standardized feature"],
            "formula": r"w_{\text{ridge}} = \frac{w_{\text{ols}}}{1 + \lambda}",
            "steps": [
                {"label": "denominator", "assign": "denom", "expr": "1 + lam", "result": 2.5, "explanation": "add penalty to curvature 1"},
                {"label": "shrunk_weight", "assign": "w_ridge", "expr": "w_ols / denom", "result": 1.2, "explanation": "divide unregularized weight by 2.5"},
            ],
            "expected_result": 1.2,
            "interpretation": "The weight shrinks from 3.0 to 1.2 without reaching zero.",
            "verification_note": "Sanity check: when lambda=0, w_ridge equals 3.0; for lambda>0, weight strictly shrinks.",
            "common_mistakes": ["Setting weight to exact zero; L2 shrinkage never reaches zero for finite lambda."],
            "generalization": "In SVD coordinates, each mode scales by s^2 / (s^2 + lambda).",
        },
        learner_level="beginner",
    )
    assert valid_prob["calculation"]["final_value"] == 1.2
    assert ped.validate_worked_problem(valid_prob["markdown"], learner_level="beginner")["valid"] is True


# ---------------------------------------------------------------------------
# T08, T09, T10, T11, T12, T13 — Quality Gate, Visual Reading Guide & Anti-Overcompression
# ---------------------------------------------------------------------------

def test_t09_t10_t11_t12_teaching_quality_and_visual_walkthrough():
    qe = QualityEngine(ROOT)

    # T10: Caption-only figure embed must FAIL structured reading check!
    caption_only = (
        "## Shrinkage\n\nSee the curve below.\n\n"
        "![[assets/scriptorium/demo/fig.png]]\n\n"
        "*Figure: Ridge shrinkage curves across lambda values.*"
    )
    cap_res = bvia.validate_explain_show_decode_connect(caption_only, {"id": "v1"})
    assert cap_res["passed"] is False

    # Full reading walkthrough PASSES cleanly!
    vis_md = bvia.compose_visual_walkthrough(
        {
            "id": "v1",
            "objective": "Shrinkage behavior",
            "alt": "Coefficient magnitude versus penalty strength",
            "explain": "To see how increasing the penalty pulls coefficients toward zero at different rates, look at the curves below.",
            "reading_entry": "Start at the left edge where lambda = 0 (unregularized fit) and move right as penalty increases.",
            "decode_components": ["Each solid curve tracks one coefficient toward zero smoothly under L2 regularization."],
            "connect": "Notice that smooth shrinkage prevents weights from collapsing abruptly, motivating the sharp-corner geometry of L1 next.",
        },
        embed="![[assets/scriptorium/demo/fig.png|520]]",
    )
    assert bvia.validate_explain_show_decode_connect(vis_md, {"id": "v1"})["passed"] is True

    # T11: Overcompression detected by evaluate_chapter_depth_contract (A3 Planner)
    depth_report = qe.evaluate_teaching(
        "## Overview\n\nRidge adds L2. Lasso adds L1. Elastic Net adds both. Huber handles outliers.",
        concept_spec={"subconcepts": ["OLS", "Polynomial", "Ridge", "Lasso", "Elastic Net"]},
        learner_level="beginner",
    )
    assert depth_report["passed"] is False
    assert depth_report["dimensions"]["appropriate_depth"]["score"] == 1
    assert any("Overcompressed" in d for d in depth_report["critical_defects"])


# ---------------------------------------------------------------------------
# T14 & Topic Independence — No Hardcoded Regression Lessons in Production Code
# ---------------------------------------------------------------------------

def test_t14_production_code_contains_no_hardcoded_regression_oracle_text():
    prod_targets = [
        ROOT / "scriptorium/engines/mathematics.py",
        ROOT / "scriptorium/engines/_explanation.py",
        ROOT / "scriptorium/triggers.py",
        ROOT / "shared/teaching_core.md",
        ROOT / "references/templates/masters/deep-notes.md",
        ROOT / "references/templates/subtemplates/mathematical.md",
    ]
    forbidden_snippets = ["58 marks", "Practice tests", "Study hours", "Classes missed", "w1 * x1", "dot + b"]
    for path in prod_targets:
        text = path.read_text(encoding="utf-8")
        for snippet in forbidden_snippets:
            assert snippet not in text, f"Hardcoded lesson fixture '{snippet}' leaked into production file {path.name}"


# ---------------------------------------------------------------------------
# T15 & T16 — Executable MATH-01..10 & TEACH-01..10 Trigger Dispatch
# ---------------------------------------------------------------------------

def test_t15_executable_math_and_teach_triggers():
    orch = OrchestrationEngine(ROOT)
    assert set(orch.math_triggers()) == {f"MATH-{i:02d}" for i in range(1, 11)}
    assert set(orch.teach_triggers()) == {f"TEACH-{i:02d}" for i in range(1, 11)}

    detected = orch.detect_triggers("## Intro\n\n$$\n\\hat{y} = \\mathbf{w}^T \\mathbf{x} + b\n$$\n\nCompare options.", learner_level="beginner")
    assert "MATH-03" in detected["math_triggers"]
    assert "TEACH-04" in detected["teach_triggers"]

    res_dim = orch.execute_trigger(
        "MATH-03",
        {"operands": [{"name": "A", "shape": [2, 3]}, {"name": "B", "shape": [3, 4]}], "operation": "matmul"},
    )
    assert res_dim["trigger"] == "MATH-03" and res_dim["result"]["output_shape"] == (2, 4)

    res_quality = orch.execute_trigger("TEACH-10", {"note_text": "## Thin\n\nOnly a few words.", "learner_level": "beginner"})
    assert res_quality["trigger"] == "TEACH-10" and len(res_quality["result"]["dimensions"]) == 12
    assert set(TEACHING_QUALITY_DIMENSIONS) == set(res_quality["result"]["dimensions"])
    assert set(k for k, _ in BEGINNER_READER_SIMULATION_QUESTIONS) == set(res_quality["result"]["beginner_reader_simulation"])


# ---------------------------------------------------------------------------
# Part 24 & Part 25 — Isolated Vault E2E Regression & Cross-Domain Generalization
# ---------------------------------------------------------------------------

def test_part24_isolated_temp_vault_regression_note_pipeline(tmp_path: Path):
    ped = PedagogyEngine()
    qe = QualityEngine(ROOT)
    ve = VaultEngine()

    folder, moc_path, _ = resolve_collection_layout("Supervised Learning", vault_root=tmp_path)
    assert folder == "Supervised Learning"
    assert "6 - Full Notes" not in moc_path

    # Store a local raster asset under assets/scriptorium/supervised-learning/ via LAVIA/media
    fig_dir = tmp_path / "source_figs"
    fig_dir.mkdir()
    (fig_dir / "ridge_demo.png").write_bytes(_png_bytes())
    acquired = media.media_artifact(
        tmp_path,
        {
            "id": "sl-fig-1",
            "collection_slug": "supervised-learning",
            "asset_name": "ridge-shrinkage",
            "source": "https://commons.wikimedia.org/wiki/File:Ridge_example.png",
            "url": "https://upload.wikimedia.org/wikipedia/commons/ridge.png",
            "rights": "CC-BY-4.0",
            "alt": "Shrinkage paths showing L2 smooth reduction vs L1 exact sparsity",
            "relevance": "Illustrates coefficient magnitude versus penalty parameter lambda.",
            "asset_policy": "offline_only",
            "local_fallback": "source_figs/ridge_demo.png",
            "embed_style": "wikilink",
            "embed_width_px": 560,
        },
        "digest-sl-reg-1",
        execute=True,
    )
    assert acquired["inspection"]["inspection_performed"] is True

    vis_walkthrough = bvia.compose_visual_walkthrough(
        {
            "objective": "Coefficient shrinkage paths under Ridge and Lasso penalties",
            "alt": "Shrinkage paths comparing L2 smooth decay to L1 zeroing",
            "explain": "Before selecting between penalties, trace visually how each method compresses weights as penalty strength increases.",
            "reading_entry": "Begin on the vertical axis where penalty lambda = 0 matches unregularized OLS, then read rightward.",
            "decode_components": [
                "Larger penalties pull coefficients smoothly toward zero without touching zero exactly in L2.",
                "Sharp geometric corners allow L1 to clamp weak features strictly to zero.",
            ],
            "connect": "Use this visual contrast when deciding between coefficient stability and sparse selection.",
        },
        embed=acquired["embed"],
        inspection=acquired["inspection"],
    )

    eq_spec = {
        "equation": r"\hat{y} = \mathbf{w}^T \mathbf{x} + b",
        "purpose": "Predicting a continuous number from multiple measurable inputs requires combining weighted contributions plus a baseline bias.",
        "pronunciation": "y-hat equals w transpose times x plus b.",
        "symbols": [
            {"symbol": r"\hat{y}", "meaning": "predicted response value", "type": "scalar", "shape": "1x1"},
            {"symbol": r"\mathbf{w}^T", "meaning": "transposed row of feature weights", "type": "vector", "shape": "1x3"},
            {"symbol": r"\mathbf{x}", "meaning": "column of observed input features", "type": "vector", "shape": "3x1"},
            {"symbol": "b", "meaning": "baseline scalar bias", "type": "scalar", "shape": "1x1"},
        ],
        "dimension_operands": [{"name": "w", "shape": [3, 1], "transpose": True}, {"name": "x", "shape": [3, 1]}],
        "dimension_operation": "matmul",
        "expanded_form": r"\hat{y} = w_1 x_1 + w_2 x_2 + w_3 x_3 + b",
        "operation_breakdown": [
            "Orient the 3x1 weight column vector as a 1x3 row via transpose.",
            "Match inner dimension 3 to multiply pair-by-pair and sum.",
            "Add scalar bias b.",
        ],
        "numerical_example": {
            "inputs": {"w1": 5, "w2": 10, "w3": -2, "x1": 2, "x2": 3, "x3": 1, "b": 20},
            "steps": [
                {"label": "study_contrib", "assign": "s", "expr": "w1 * x1", "result": 10},
                {"label": "practice_contrib", "assign": "p", "expr": "w2 * x2", "result": 30},
                {"label": "missed_contrib", "assign": "m", "expr": "w3 * x3", "result": -2},
                {"label": "sum_with_bias", "assign": "y_hat", "expr": "s + p + m + b", "result": 58},
            ],
            "expected_result": 58,
            "interpretation": "Predicted score equals 58 under those declared hypothetical feature values.",
            "sanity_check": "With zero inputs (x=0), prediction equals bias 20 cleanly.",
        },
        "misconceptions": ["Multiplying two 3x1 columns directly violates inner matrix dimension matching."],
    }

    bp = ped.build_explanation_blueprint(
        "Linear and Regularized Regression",
        master="M1",
        audience="beginner",
        context={
            "familiar_anchor": "Consider predicting house prices or exam marks from several measurable traits.",
            "starting_intuition": "Just like weighting subscores in a course grade, each feature adds a proportional push to the baseline guess.",
            "analogy_limit": "Weights describe linear model associations, not guaranteed real-world causation or curves.",
            "prerequisite_bridges": [
                {"term": "Straight-line slope", "explanation": "A rate of change telling how much y rises per unit step in one feature x."},
                {"term": "Matrix transpose", "explanation": "Flipping rows and columns so inner dimensions match for multiplication."},
            ],
            "equations": [eq_spec],
            "visual_walkthroughs": [vis_walkthrough],
            "comparisons": [
                {
                    "title": "Ridge vs Lasso vs Elastic Net",
                    "causal_explanation": "Because squared L2 penalties curve smoothly, weights shrink evenly without hitting exact zero, making Ridge strong on correlated features; L1 diamond corners hit axes directly to zero irrelevant features, while Elastic Net blends both behaviors.",
                    "table": "| Method | Penalty | Sparsity | Collinearity |\n|---|---|---|---|\n| Ridge | L2 | No | Stable |\n| Lasso | L1 | Yes | Picks one |",
                }
            ],
            "misconceptions": ["Zero weight under Lasso does not prove causal irrelevance; it reflects correlated selection under that penalty."],
            "practical_application": "Standardize feature scales before regularizing so units like dollars vs counts receive fair penalties.",
            "transition": "With continuous numerical prediction grounded, classification next shows why predicting probabilities requires a bounded S-curve.",
        },
    )
    chapter_text = ped.compose_explanation(bp)
    chapter_text += (
        "\n\n## Check Your Understanding\n\n"
        "**Question 1:** Why must features be standardized before fitting Ridge or Lasso?\n\n"
        "> [!hint]- Show hint\n> Notice how penalty terms square or sum raw weight magnitudes.\n\n"
        "> [!answer]- Show detailed answer\n> Unstandardized features measured in large units have tiny weights and receive smaller penalties than small-unit features with huge weights, skewing shrinkage unfairly.\n"
    )

    out_path = tmp_path / folder / "02 - Linear and Regularized Regression.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(chapter_text, encoding="utf-8")
    assert out_path.is_file()

    q_res = qe.evaluate_teaching(chapter_text, worked_examples=[{
        "steps": eq_spec["numerical_example"]["steps"],
        "given": eq_spec["numerical_example"]["inputs"],
        "expected_result": 58,
    }], visuals=[{"id": "sl-fig-1"}], learner_level="beginner")
    assert q_res["passed"] is True, q_res
    assert all(q_res["beginner_reader_simulation"].values()), q_res["beginner_reader_simulation"]


@pytest.mark.parametrize(
    ("topic", "concept_type", "eq_spec"),
    [
        (
            "RC Circuit Time Constant",
            "scientific",
            {
                "equation": r"\tau = R C",
                "purpose": "Quantifies how fast a capacitor voltage decays or charges through a resistor.",
                "pronunciation": "tau equals R times C.",
                "symbols": [
                    {"symbol": r"\tau", "meaning": "time constant", "type": "scalar", "units": "seconds"},
                    {"symbol": "R", "meaning": "series resistance", "type": "scalar", "units": "ohms"},
                    {"symbol": "C", "meaning": "capacitance", "type": "scalar", "units": "farads"},
                ],
                "numerical_example": {
                    "inputs": {"R": 2000.0, "C": 0.0005},
                    "steps": [{"label": "time_constant", "assign": "tau", "expr": "R * C", "result": 1.0}],
                    "expected_result": 1.0,
                    "interpretation": "Voltage drops to 36.8% of initial value after 1.0 second.",
                    "sanity_check": "Doubling R doubles charging duration.",
                },
            },
        ),
        (
            "Treaty of Westphalia",
            "historical",
            None,
        ),
    ],
)
def test_part25_cross_domain_generalization(topic, concept_type, eq_spec):
    ped = PedagogyEngine()
    qe = QualityEngine(ROOT)

    ctx = {
        "familiar_anchor": f"Consider why learners study {topic} before advanced topics in this field.",
        "starting_intuition": f"At its core, {topic} explains how primary constraints govern outcomes.",
        "misconceptions": [f"Avoid applying {topic} outside its stated historical or physical assumptions."],
        "transition": f"Understanding {topic} prepares the foundation for downstream case studies.",
    }
    if eq_spec:
        ctx["equations"] = [eq_spec]

    bp = ped.build_explanation_blueprint(topic, master="M1", concept_type=concept_type, audience="beginner", context=ctx)
    note = ped.compose_explanation(bp)
    res = qe.evaluate_teaching(note, learner_level="beginner")
    assert res["passed"] is True, res
    if concept_type == "historical":
        assert res["dimensions"]["mathematical_explanation"]["applicable"] is False
