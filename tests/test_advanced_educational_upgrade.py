"""Acceptance and regression tests for the advanced educational intelligence upgrade."""
from __future__ import annotations

from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageDraw
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scriptorium import (
    KnowledgeCollectionPlan,
    NoteCollectionPlan,
    OrchestrationEngine,
    QualityEngine,
    ResolvedNotePreferences,
    TopicNode,
)
from scriptorium.engines import mathematics as math_eng
from scriptorium.engines.composition import learning, publication, video, writing
from scriptorium.models import content_hash


def _make_png(width: int = 480, height: int = 300, label: str = "Gradient Step") -> bytes:
    img = Image.new("RGB", (width, height), (244, 247, 252))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, width - 20, height - 20], outline=(30, 60, 120), width=4)
    draw.line([(40, 220), (220, 90), (420, 200)], fill=(190, 45, 45), width=4)
    draw.text((40, 40), label, fill=(15, 25, 45))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_multiline_assessment_verification_and_remediation():
    from scriptorium.engines.pedagogy import build_explanation_blueprint

    bp = build_explanation_blueprint(
        "Gradient Descent",
        concept_id="gd-1",
        master="M1",
        audience="beginner",
        context={
            "teaching_extensions": {
                "require_complete": True,
                "objectives": ["explain gradient descent", "apply update rule"],
                "teaching": {
                    "why": "Finding parameter minima analytically is often intractable for large models.",
                    "intuition": "Walk downhill along the steepest local slope until the valley flattens.",
                    "what": "Iterative first-order optimization updating parameters opposite the gradient.",
                    "how": "Compute the loss gradient, scale by learning rate, and subtract from current weights.",
                    "when_use": "Use when objective is differentiable and datasets are large.",
                    "when_not_use": "Avoid when objective is non-smooth or learning rate causes divergence.",
                    "apply": "Update w_new = w - eta * grad_L(w) over each mini-batch.",
                    "reinforcement": "Check that loss decreases monotonically for sufficiently small step sizes.",
                },
                "mechanism": {
                    "inputs": "Initial weights w0, learning rate eta, loss function L(w)",
                    "steps": [
                        {
                            "component": "Gradient Evaluator",
                            "receives": "Current parameter vector w_t",
                            "operation": "Computes partial derivatives nabla L(w_t)",
                            "reason": "Identifies the direction of steepest ascent",
                            "produces": "Gradient vector g_t",
                            "next": "Passes g_t to the parameter update step",
                        }
                    ],
                    "outputs": "Updated parameter vector w_{t+1}",
                    "interpretation": "Each step moves opposite g_t to reduce training loss.",
                },
                "assessments": [
                    {
                        "id": "q1",
                        "type": "conceptual",
                        "objectives": ["explain gradient descent"],
                        "question": "Why do we subtract rather than add the gradient?",
                        "hint": "Line 1: Recall what direction the gradient points.\nLine 2: We want to minimize, not maximize, loss.",
                        "reasoning": "Step 1: Gradient points uphill.\nStep 2: Negating points downhill.",
                        "answer": "Subtracting moves opposite steepest ascent, toward lower loss.",
                    }
                ],
            }
        },
    )
    rendered = writing.compose_explanation_note(bp)
    assert "> [!hint]- Hint" in rendered
    assert "> Line 2: We want to minimize, not maximize, loss." in rendered
    assert bp.context["composition_result"]["validation"]["complete"] is True

    # Remediation strictly from actual learner responses
    comp = writing.Composition(**bp.context["composition_result"]["contract"])
    no_resp = learning.build_remediation(comp, [])
    assert no_resp["status"] == "no_learner_responses"
    rem = learning.build_remediation(comp, [{"question_id": "q1", "correct": False, "answer": "To go uphill"}])
    assert rem["status"] == "remediation_generated" and len(rem["remediation"]) == 1


def test_math_stage_omissions_reject_trivial_and_core_bypasses():
    with pytest.raises(ValueError, match="Stage 1"):
        math_eng.render_formula_component({
            "equation": "y = m x + b",
            "symbols": [{"symbol": "y", "meaning": "output"}],
            "stage_omissions": {"1": "Not needed for this note"},
        })
    with pytest.raises(ValueError, match="substantive domain-specific reason"):
        math_eng.render_formula_component({
            "equation": "y = m x + b",
            "purpose": "Models a linear relationship.",
            "stage_omissions": {"8": "skip"},
        })
    with pytest.raises(ValueError, match="Stage 3"):
        math_eng.render_formula_component({
            "equation": "y = m x + b",
            "purpose": "Models a linear relationship.",
            "required_stages": [1, 3],
            "stage_omissions": {"3": "Symbols omitted intentionally here"},
        })


def test_practical_controlled_execution_and_visual_roles(tmp_path):
    code = "def step(w, grad, lr=0.1):\n    return round(w - lr * grad, 4)\nassert step(2.0, 4.0) == 1.6\n"
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert proc.returncode == 0

    png_bytes = _make_png()
    asset_hash = content_hash(png_bytes)

    from scriptorium.engines.pedagogy import build_explanation_blueprint

    bp = build_explanation_blueprint(
        "Optimization Step",
        concept_id="opt-1",
        master="M5",
        audience="beginner",
        context={
            "teaching_extensions": {
                "require_complete": True,
                "objectives": ["implement update step", "visualize descent"],
                "teaching": {
                    "why": "Numerical optimization requires concrete update rules.",
                    "intuition": "Take controlled steps downhill.",
                    "what": "First-order parameter update.",
                    "how": "Multiply gradient by learning rate and subtract.",
                    "when_use": "Use for smooth differentiable objectives.",
                    "when_not_use": "Avoid on discontinuous step functions.",
                    "apply": "Run step(2.0, 4.0) to obtain 1.6.",
                    "reinforcement": "Verify output matches hand calculation.",
                },
                "mechanism": {
                    "inputs": "w=2.0, grad=4.0, lr=0.1",
                    "steps": [{
                        "component": "Scaler",
                        "receives": "grad=4.0",
                        "operation": "Multiplies by lr=0.1",
                        "reason": "Controls step size",
                        "produces": "delta=0.4",
                        "next": "Subtracts delta from w",
                    }],
                    "outputs": "w_new=1.6",
                    "interpretation": "Parameter moved closer to minimum.",
                },
                "practical": {
                    "domain": "programming",
                    "stages": {
                        "problem": "Compute one gradient descent update accurately.",
                        "environment": "Python 3.12 standard library.",
                        "workflow": "Define step function, assert output, inspect value.",
                        "implementation": "Implement scalar update with default learning rate.",
                        "evaluation": "Verify step(2.0, 4.0) == 1.6.",
                        "debugging": "Watch for sign flip when adding instead of subtracting.",
                        "end_to_end": "Execute script and confirm exit code 0.",
                        "challenge": "Extend step() to vector inputs using a list comprehension.",
                    },
                    "code": code,
                    "language": "python",
                    "execution": {
                        "code_sha256": content_hash(code),
                        "status": "passed",
                        "expected": 1.6,
                        "observed": 1.6,
                        "method": "subprocess_python_assert",
                    },
                },
                "comparisons": [{
                    "title": "Fixed vs Adaptive Step Size",
                    "causal_explanation": "Fixed learning rates scale every coordinate identically, whereas adaptive methods normalize by historical gradient magnitude.",
                    "suitability": "Fixed rate suits well-conditioned convex problems.",
                    "table": "| Method | Scaling | Best Regime |\n|---|---|---|\n| Fixed LR | Uniform | Smooth convex |\n| Adaptive | Per-coordinate | Sparse or ill-conditioned |",
                }],
                "visual_requirements": [{"role": "mechanism", "objective": "Show descent step"}],
                "assets": [{"path": "assets/scriptorium/opt/step.png", "hash": asset_hash}],
                "inspections": [{"inspection_performed": True, "content_hash": asset_hash, "semantic_findings": ["Downhill curve"]}],
                "visual_walkthroughs": ["Inspect the downhill step.\n\n![[assets/scriptorium/opt/step.png]]\n\nFollow the curve from left to right."],
            }
        },
    )
    rendered = writing.compose_explanation_note(bp)
    assert "### Core implementation or procedure" in rendered
    assert "Fixed vs Adaptive Step Size" in rendered
    assert bp.context["composition_result"]["validation"]["complete"] is True


def test_multifile_acceptance_in_isolated_vault(tmp_path):
    png_bytes = _make_png(label="Loss Curve")
    img_hash = content_hash(png_bytes)

    def fake_img_get(url: str, timeout: int = 15) -> dict:
        return {"status": 200, "headers": {"content-type": "image/png"}, "body": png_bytes}

    prefs = ResolvedNotePreferences(
        learning_objective="Master iterative optimization",
        master="M1",
        variant=None,
        depth="beginner",
        prior_knowledge={"level": "beginner"},
        organization="hierarchical_collection",
        emphasis=["intuition", "worked_examples"],
        source_policy="adaptive",
    )
    nodes = [
        TopicNode(concept_id="moc", title="Optimization", parent_id=None, child_ids=["c1", "c2"], note_role="root_index", proposed_path="Optimization/00 - Map of Contents.md"),
        TopicNode(concept_id="c1", title="01 - Loss Functions", parent_id="moc", note_role="child", proposed_path="Optimization/01 - Loss Functions.md", template_plan={"master": "M1"}),
        TopicNode(concept_id="c2", title="02 - Gradient Step", parent_id="moc", note_role="child", proposed_path="Optimization/02 - Gradient Step.md", prerequisite_ids=["c1"], template_plan={"master": "M1"}),
    ]
    plan = NoteCollectionPlan(
        collection_id="col-opt",
        title="Optimization",
        root_topic_id="moc",
        organization="hierarchical_collection",
        nodes=nodes,
        planned_paths=[n.proposed_path for n in nodes],
        learning_order=["c1", "c2", "moc"],
        generation_order=["c1", "c2", "moc"],
    )
    kcp = KnowledgeCollectionPlan(plan=plan)
    teaching = {
        "c1": {
            "require_complete": True,
            "objectives": ["explain loss"],
            "teaching": {
                "why": "Models need a scalar measure of error.",
                "intuition": "Loss measures how far predictions sit from targets.",
                "what": "A non-negative penalty over prediction residuals.",
                "how": "Square each residual and average across samples.",
                "when_use": "Use squared error for continuous targets.",
                "when_not_use": "Avoid when heavy outliers dominate.",
                "apply": "Compute (3 - 5)^2 = 4 for a single sample.",
                "reinforcement": "Zero loss means exact prediction.",
            },
            "mechanism": {
                "inputs": "y=5, y_hat=3",
                "steps": [{"component": "Residual", "receives": "y, y_hat", "operation": "Subtracts y_hat from y", "reason": "Measures signed error", "produces": "e=2", "next": "Squares e"}],
                "outputs": "L=4",
                "interpretation": "Larger residuals grow quadratically.",
            },
            "worked_problems": [{
                "problem": "Compute squared error for y=5, y_hat=3.",
                "given": {"y": 5, "y_hat": 3},
                "find": "Find squared error L",
                "assumptions": ["Scalar regression target"],
                "formula": "L = (y - \\hat{y})^2",
                "symbols": [{"symbol": "y", "meaning": "target"}, {"symbol": "\\hat{y}", "meaning": "prediction"}],
                "steps": [{"label": "residual", "expr": "(y - y_hat)**2", "result": 4}],
                "expected_result": 4,
                "interpretation": "Squared error is 4.",
                "common_mistakes": ["Forgetting to square negative residuals"],
                "generalization": "Average across N samples for MSE.",
            }],
        },
        "c2": {
            "require_complete": True,
            "objectives": ["derive update"],
            "teaching": {
                "why": "Minimizing loss requires adjusting parameters.",
                "intuition": "Step opposite the local slope.",
                "what": "First-order update rule.",
                "how": "Evaluate derivative and subtract scaled gradient.",
                "when_use": "Use on differentiable losses.",
                "when_not_use": "Avoid if step size exceeds stability bound.",
                "apply": "Update w from 2.0 to 1.6.",
                "reinforcement": "Verify loss decreases after update.",
            },
            "mechanism": {
                "inputs": "w=2.0, lr=0.1",
                "steps": [{"component": "Update", "receives": "w, grad", "operation": "Subtracts lr * grad", "reason": "Moves downhill", "produces": "w_new=1.6", "next": "Re-evaluate loss"}],
                "outputs": "w_new=1.6",
                "interpretation": "New weight lowers loss.",
            },
            "equations": [{
                "equation": "w_{t+1} = w_t - \\eta g_t",
                "purpose": "Updates weight opposite gradient.",
                "operation_breakdown": ["Scale gradient by learning rate", "Subtract from current weight"],
                "symbols": [
                    {"symbol": "w_t", "meaning": "current weight"},
                    {"symbol": "\\eta", "meaning": "learning rate"},
                    {"symbol": "g_t", "meaning": "gradient"},
                ],
                "pronunciation": "w at t plus 1 equals w at t minus eta times g at t.",
                "derivation_reasoning": "First-order Taylor expansion L(w - eta g) approx L(w) - eta ||g||^2 shows descent for small eta > 0.",
                "numerical_example": {
                    "inputs": {"w": 2.0, "eta": 0.1, "g": 4.0},
                    "steps": [{"label": "update", "expr": "w - eta * g", "result": 1.6}],
                    "expected_result": 1.6,
                    "interpretation": "Weight moves from 2.0 to 1.6.",
                },
                "assumptions": ["Objective is locally differentiable"],
                "interpretation": "Smaller eta gives slower but safer steps.",
            }],
            "visual_specs": [{
                "id": "vis-loss-curve",
                "kind": "source_figure",
                "renderer": "external",
                "section": "Visual Explanation",
                "concept": "c2",
                "objective": "Show loss curve descent",
                "url": "https://upload.wikimedia.org/wikipedia/commons/demo_loss.png",
                "source": "https://commons.wikimedia.org/wiki/File:Demo_loss.png",
                "rights": "CC0",
                "alt": "Convex loss curve",
                "relevance": "Illustrates downhill step",
                "origin": "supplied",
                "inspection_findings": {
                    "content_hash": img_hash,
                    "text_labels_extracted": ["Loss", "Weight"],
                    "review_method": "inspected_fixture",
                },
            }],
        },
    }

    res = publication.generate_collection_with_checkpoints(
        tmp_path, kcp, prefs, teaching_by_node=teaching, http_get=fake_img_get
    )
    assert res["failed_nodes"] == []
    assert res["complete"] is True
    assert res["failed_count"] == 0
    assert len(res["written_paths"]) == 3
    assert not list(tmp_path.rglob("*.svg"))
    val = QualityEngine(ROOT).validate_collection(tmp_path, plan, manifest=res["manifest"])
    assert val["valid"] is True, val
