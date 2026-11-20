"""Comprehensive validation for the Seven Canonical Master Templates (M1-M7),
Intelligent Routing Engine, and Repository Reorganization.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from scriptorium.engines import quality as audit_repository
from scriptorium import layout as note_layout
import plan_notes
from scriptorium.engines import orchestration as re_eng


# ---------------------------------------------------------------------------
# 1. Registry Integrity & Repository Structure Verification
# ---------------------------------------------------------------------------

def test_master_registry_valid_and_legacy_templates_dir_retired():
    res = re_eng.validate_registry(ROOT, require_retired_legacy=True)
    assert res["valid"], res["errors"]
    assert res["masters_count"] == 7
    assert res["variants_count"] == 12
    assert res["subtemplates_count"] == 6
    assert res["commands_count"] == 4
    assert res["retired_commands_count"] == 8
    assert not (ROOT / "templates").exists(), "Legacy top-level templates/ directory must be retired."


def test_reorganized_references_hierarchy_and_zero_audit_errors():
    required_dirs = [
        ROOT / "references",
        ROOT / "references/routing",
        ROOT / "references/workflows/research",
        ROOT / "references/workflows/notes-creation",
        ROOT / "references/workflows/revision",
        ROOT / "references/workflows/validation",
        ROOT / "references/templates",
        ROOT / "references/templates/masters",
        ROOT / "references/templates/variants",
        ROOT / "references/templates/subtemplates",
        ROOT / "references/templates/modules",
        ROOT / "references/contracts",
    ]
    for directory in required_dirs:
        assert directory.is_dir(), f"Missing reorganized directory: {directory}"
        assert (directory / "README.md").is_file(), f"Missing README.md in {directory}"

    audit = audit_repository.audit_repository(ROOT)
    assert audit["errors"] == [], f"Broken local links or CLI flags: {audit['errors']}"


# ---------------------------------------------------------------------------
# 2. Section 30 — Canonical Routing Table (16 Standard Scenarios)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(("request_text", "expected_master", "expected_variant"), [
    # 1. M1 Deep Learning Notes
    ("Explain transformers deeply from first principles", "M1", None),
    # 2. M2 Structured Study Notes (lecture/source order)
    ("Make notes on this lecture without skipping anything", "M2", "lecture_order"),
    # 3. M3 Cheat Sheet (base)
    ("Give me a cheat sheet for linear algebra", "M3", None),
    # 4. M3 Formula Sheet
    ("Make a formula sheet for thermodynamics", "M3", "formula_sheet"),
    # 5. M3 Syntax / API Reference
    ("Give me a PyTorch tensor syntax reference", "M3", "syntax_reference"),
    # 6. M3 Command / CLI Reference
    ("Give me a Git command reference", "M3", "command_reference"),
    # 7. M3 Atomic Card
    ("Create an atomic note for Vanishing Gradient", "M3", "atomic_card"),
    # 8. M4 Worked Problems (problem set)
    ("Solve these 10 calculus integration problems step by step", "M4", None),
    # 9. M4 Worked Examples
    ("Show worked examples of Bayes theorem", "M4", None),
    # 10. M5 Implementation from scratch
    ("Implement gradient descent from scratch in NumPy", "M5", None),
    # 11. M5 Build & debug technical guide
    ("Build a REST API in FastAPI and debug authentication", "M5", None),
    # 12. M6 Practice test / quiz
    ("Make a practice test on neural networks", "M6", None),
    # 13. M6 Flashcards
    ("Create flashcards for cellular respiration", "M6", "flashcards"),
    # 14. M6 Mock exam / viva
    ("Create a mock exam on operating systems", "M6", "mock_exam"),
    # 15. M7 Comparison guide
    ("Compare CNN vs ViT", "M7", "comparison_guide"),
    # 16. M7 Exam revision pack / synthesis
    ("Create an exam revision pack from my 5 calculus notes", "M7", "revision_pack"),
    # Additional M7 variants
    ("Make a concept map of machine learning algorithms", "M7", "concept_map"),
    ("Break down this paper https://arxiv.org/abs/1706.03762", "M7", "paper_breakdown"),
    ("Summarize this article https://example.org/attention-guide", "M7", "quick_summary"),
])
def test_canonical_routing_table_scenarios(request_text, expected_master, expected_variant):
    res = re_eng.route_request(request_text)
    assert res["master"] == expected_master, res
    assert res["variant"] == expected_variant, res
    assert res["multi_artifact"] is False
    assert len(res["artifacts"]) == 1


# ---------------------------------------------------------------------------
# 3. Section 30.1 — Edge Cases A-J (Negation, Mixed, Multi-Artifact, Source Lock)
# ---------------------------------------------------------------------------

def test_edge_a_negated_cheat_sheet_routes_to_m1():
    res = re_eng.route_request("Don't make a cheat sheet. I want detailed explanations of entropy.")
    assert res["master"] == "M1"
    assert "cheat sheet" in res["routing_trace"]["negated_artifacts"]


def test_edge_b_negated_summary_routes_to_m1():
    res = re_eng.route_request("Not a summary, give me deep first-principles notes on backpropagation.")
    assert res["master"] == "M1"
    assert "summary" in res["routing_trace"]["negated_artifacts"]


def test_edge_c_negated_study_guide_routes_to_mock_exam():
    res = re_eng.route_request("Instead of a study guide, build a mock exam on operating systems.")
    assert res["master"] == "M6"
    assert res["variant"] == "mock_exam"
    assert "study guide" in res["routing_trace"]["negated_artifacts"]


def test_edge_d_embedded_secondary_module_stays_single_artifact():
    res = re_eng.route_request("Explain backpropagation deeply and include a short formula cheat sheet at the end.")
    assert res["master"] == "M1"
    assert res["multi_artifact"] is False
    assert len(res["artifacts"]) == 1
    assert "formula_reference" in res["artifacts"][0]["secondary_modules"]


def test_edge_e_separate_companion_artifact_triggers_multi_artifact_shared_context():
    res = re_eng.route_request("Create deep notes on Gradient Descent and a separate formula sheet.")
    assert res["multi_artifact"] is True
    assert res["shared_context"] is True
    pairs = [(a["master"], a["variant"]) for a in res["artifacts"]]
    assert pairs == [("M1", None), ("M3", "formula_sheet")]


def test_edge_f_both_explicit_artifacts_trigger_multi_artifact():
    res = re_eng.route_request("Create both study notes and flashcards for organic chemistry.")
    assert res["multi_artifact"] is True
    assert res["shared_context"] is True
    pairs = [(a["master"], a["variant"]) for a in res["artifacts"]]
    assert pairs == [("M2", None), ("M6", "flashcards")]


def test_edge_g_strict_source_policy_and_lecture_order_preserved_on_m2():
    res = re_eng.route_request(
        "Make notes on this lecture PDF using only its formulas and preserving its lecture order",
        has_source=True,
    )
    assert res["master"] == "M2"
    assert res["variant"] == "lecture_order"
    assert res["source_policy"] == "strict"
    assert res["research_mode"] == "R-S0"
    assert res["routing_trace"]["source_order_preserved"] is True


def test_edge_h_strict_source_policy_preserved_on_m4():
    res = re_eng.route_request(
        "Solve these 5 homework problems using only the lecture formulas",
        has_source=True,
    )
    assert res["master"] == "M4"
    assert res["source_policy"] == "strict"
    assert res["research_mode"] == "R-S0"


def test_edge_i_worked_solutions_vs_practice_assessment_distinction():
    m4 = re_eng.route_request("Solve these 5 integration problems step by step")
    m6 = re_eng.route_request("Give me 10 practice integration problems to test myself")
    assert m4["master"] == "M4"
    assert m6["master"] == "M6"


def test_edge_j_implementation_vs_deep_no_code_explanation_distinction():
    m5 = re_eng.route_request("Implement gradient descent from scratch in NumPy")
    m1 = re_eng.route_request("Explain the mathematical intuition behind gradient descent without code")
    assert m5["master"] == "M5"
    assert m1["master"] == "M1"
    assert "code" in m1["routing_trace"]["negated_artifacts"]


# ---------------------------------------------------------------------------
# 4. Section 30.2 — Domain Independence (Master != Subject)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(("request_text", "expected_master", "expected_variant", "expected_kt"), [
    ("Make a cheat sheet for organic chemistry reactions", "M3", None, "scientific"),
    ("Create a formula sheet for microeconomics elasticities", "M3", "formula_sheet", "conceptual"),
    ("Solve these 5 organic chemistry synthesis problems step by step", "M4", None, "scientific"),
    ("Make flashcards for World War II treaties", "M6", "flashcards", "historical"),
    ("Compare Mitosis vs Meiosis", "M7", "comparison_guide", "scientific"),
    ("Explain the French Revolution from first principles", "M1", None, "historical"),
    ("Compare Keynesian vs Monetarist economics", "M7", "comparison_guide", "conceptual"),
])
def test_domain_independence_across_non_cs_subjects(request_text, expected_master, expected_variant, expected_kt):
    res = re_eng.route_request(request_text)
    assert res["master"] == expected_master
    assert res["variant"] == expected_variant
    assert expected_kt in res["knowledge_types"]


# ---------------------------------------------------------------------------
# 5. Section 39 & 39.1 — All 7 Masters & Cross-Master Differentiation on Gradient Descent
# ---------------------------------------------------------------------------

GRADIENT_DESCENT_OUTPUTS = {
    "M1": (
        None,
        """# Gradient Descent

## Why Gradient Descent Exists
When training differentiable models, closed-form optima are rarely tractable in high dimensions. Gradient descent iteratively reduces a differentiable loss function by stepping opposite to its local steepest ascent vector.

## Geometric Intuition and Mathematical Formalism
For a differentiable objective $f: \\mathbb{R}^d \\to \\mathbb{R}$, the update rule at step $t$ with learning rate $\\eta > 0$ is:
$$\\theta_{t+1} = \\theta_t - \\eta \\nabla f(\\theta_t)$$
When $f$ is $L$-smooth, choosing $0 < \\eta < 2/L$ guarantees monotonic descent at every step.

## Worked Numerical Trace
Take $f(\\theta) = (\\theta - 3)^2$, so $f'(\\theta) = 2(\\theta - 3)$ and $L = 2$. Starting at $\\theta_0 = 0$ with $\\eta = 0.25$:
- Step 1: $\\theta_1 = 0 - 0.25 \\cdot (-6) = 1.5$, $f(\\theta_1) = 2.25$.
- Step 2: $\\theta_2 = 1.5 - 0.25 \\cdot (-3) = 2.25$, $f(\\theta_2) = 0.5625$.

## Failure Modes and Pitfalls
If $\\eta > 2/L$ (here $\\eta > 1$), iterates overshoot and diverge geometrically. Ill-conditioned Hessians induce zig-zagging along high-curvature directions.

## Revision Summary
Gradient descent follows $-\\nabla f(\\theta_t)$; stability requires $\\eta < 2/L$ under $L$-smoothness.
""",
    ),
    "M2": (
        "lecture_order",
        """# Lecture 4: Gradient Descent

## 1. Source Context & Learning Goals
> [!info] Source & Scope Context
> - **Primary Source**: Lecture 4 Slides (pp. 1-14)
> - **Access & Scope**: Complete slide deck; preserves exact lecture sequence.

## 2. Sequential Concepts & Explanations
### 2.1 Loss Landscape Setup
The lecture defines empirical risk $J(\\theta)$ and motivates iterative minimization.

### 2.2 Update Rule and Step Size
Following slide 7, $\\theta_{t+1} = \\theta_t - \\eta \\nabla J(\\theta_t)$.

## 3. Key Takeaways & Active Recall
- Steepest descent uses the negative gradient; verify step size against curvature.
""",
    ),
    "M3": (
        "formula_sheet",
        """# Gradient Descent — Formula Sheet

| Equation | Symbols & Units | Applicability Condition |
|---|---|---|
| $\\theta_{t+1} = \\theta_t - \\eta \\nabla f(\\theta_t)$ | $\\theta_t \\in \\mathbb{R}^d$, $\\eta > 0$ | Differentiable $f$ |
| $0 < \\eta < 2/L$ | $L$: Lipschitz constant of $\\nabla f$ | $L$-smooth objective |
| $f(\\theta_T) - f(\\theta^*) \\le \\frac{\\|\\theta_0 - \\theta^*\\|^2}{2 \\eta T}$ | $T$: iterations | Convex + $L$-smooth, $\\eta \\le 1/L$ |

- **Trap**: $\\eta > 2/L$ causes divergence on quadratics.
""",
    ),
    "M4": (
        None,
        """# Worked Solutions: Gradient Descent

## Problem 1: Quadratic Minimization
**Given**: $f(\\theta) = 2(\\theta - 4)^2$, initial point $\\theta_0 = 1$, learning rate $\\eta = 0.1$. Find $\\theta_1$, $\\theta_2$, and check stability.

### Method Selection
Use exact first-order gradient descent because $f$ is strictly convex and smooth with $L = f''(\\theta) = 4$.

### Step-by-Step Solution
1. Differentiate: $f'(\\theta) = 4(\\theta - 4)$.
2. Compute step 1: $f'(1) = -12$, so $\\theta_1 = 1 - 0.1(-12) = 2.2$.
3. Compute step 2: $f'(2.2) = 4(-1.8) = -7.2$, so $\\theta_2 = 2.2 - 0.1(-7.2) = 2.92$.

### Final Answer & Verification Check
- **Final Answer**: $\\theta_1 = 2.2$, $\\theta_2 = 2.92$.
- **Sanity Check**: Loss decreased monotonically: $f(1) = 18 > f(2.2) = 6.48 > f(2.92) = 2.3328$, and $\\eta = 0.1 < 2/L = 0.5$ confirms stability.
""",
    ),
    "M5": (
        None,
        """# Implementation Guide: Gradient Descent in NumPy

## Architecture & Core Invariant
Keep parameter updates pure and track the monotonic descent invariant on convex $L$-smooth objectives.

## Implementation
```python
import numpy as np

def gradient_descent(grad_fn, theta0, lr=0.1, steps=50):
    theta = np.array(theta0, dtype=float)
    for _ in range(steps):
        theta = theta - lr * grad_fn(theta)
    return theta

opt = gradient_descent(lambda x: 2.0 * (x - 3.0), [0.0], lr=0.25, steps=30)
assert np.allclose(opt, [3.0], atol=1e-6)
```

## Verification & Edge Cases
- **Test**: Converges to `3.0` within `1e-6` tolerance.
- **Edge Case**: Guard against `lr <= 0` or `NaN` gradients when step size exceeds $2/L$.
""",
    ),
    "M6": (
        None,
        """# Gradient Descent — Active Recall Assessment

## Tier 1: Core Recall
### Q1. What condition on learning rate $\\eta$ guarantees descent for an $L$-smooth quadratic?
> [!hint]- Need a nudge?
> Relate $\\eta$ to the Lipschitz constant $L$ of the gradient.

> [!tip]- Reveal approach and solution
> **Final answer:** $0 < \\eta < 2/L$. Values above $2/L$ flip sign with magnitude $> 1$ and diverge.

### Q2. Why does poor conditioning slow down vanilla gradient descent?
> [!hint]- Need a nudge?
> Compare curvature along the steepest and shallowest eigenvectors.

> [!tip]- Reveal approach and solution
> **Final answer:** The maximum stable step size is limited by the largest eigenvalue $L$, causing slow progress along small-eigenvalue directions.
""",
    ),
    "M7": (
        "comparison_guide",
        """# Gradient Descent vs Newton's Method

## Executive Decision Rule
Choose Gradient Descent for high-dimensional problems where $O(d^2)$ Hessian storage and $O(d^3)$ inversion are prohibitive; choose Newton's Method for low-dimensional strongly convex problems needing quadratic convergence.

## Trade-Off Matrix
| Criterion | Gradient Descent | Newton's Method |
|---|---|---|
| Per-step Cost | $O(d)$ | $O(d^3)$ |
| Convergence Rate (Strongly Convex) | Linear | Local Quadratic |
| Sensitivity to Conditioning | High | Affine-invariant |

## Synthesis Takeaway
Quasi-Newton methods (L-BFGS) bridge these two extremes using curvature approximations in $O(md)$ memory.
""",
    ),
}


@pytest.mark.parametrize("master_id", ("M1", "M2", "M3", "M4", "M5", "M6", "M7"))
def test_all_seven_masters_validate_and_scaffold(master_id):
    variant, sample_text = GRADIENT_DESCENT_OUTPUTS[master_id]
    errors = re_eng.validate_master_output(sample_text, master_id, variant=variant)
    assert errors == [], f"{master_id} sample failed validation: {errors}"

    reg = re_eng.load_master_registry(ROOT)
    route = reg["masters"][master_id]["route"]
    assert route in note_layout.ROUTES
    skeleton = note_layout.body_skeleton(route, 0, "01", "Gradient Descent", narrow=False)
    assert "# " in skeleton


def test_cross_master_differentiation_rejects_mismatched_products():
    # Essay prose from M1 is NOT a valid M3 quick reference, M5 code guide, or M6 assessment
    m1_text = GRADIENT_DESCENT_OUTPUTS["M1"][1]
    assert re_eng.validate_master_output(m1_text, "M5")  # missing fenced code
    assert re_eng.validate_master_output(m1_text, "M6")  # missing numbered Qs & hidden answers

    # Long essay fails M3 quick-reference scannability check
    long_essay = "# GD\n\n" + ("word " * 90) + "\n"
    assert re_eng.validate_master_output(long_essay, "M3")

    # M3 formula sheet is NOT a valid M1 deep note (too short / < 3 H2s)
    m3_text = GRADIENT_DESCENT_OUTPUTS["M3"][1]
    assert re_eng.validate_master_output(m3_text, "M1")

    # M4 worked solution is NOT a valid M6 hidden-answer assessment
    m4_text = GRADIENT_DESCENT_OUTPUTS["M4"][1]
    assert re_eng.validate_master_output(m4_text, "M6")

    # M7 comparison guide without a table fails
    assert re_eng.validate_master_output("# Compare\n\nNo table here.", "M7", variant="comparison_guide")


# ---------------------------------------------------------------------------
# 6. CLI & plan_notes Integration Checks
# ---------------------------------------------------------------------------

def test_plan_notes_inspect_attaches_master_routing_fields():
    inspected = plan_notes.inspect_request("Create a cheat sheet on Gradient Descent")
    assert inspected["template"] == "cheat-sheet"
    assert inspected["master"] == "M3"
    assert inspected["multi_artifact"] is False
    assert "mathematical" in inspected["knowledge_types"]

    deep = plan_notes.inspect_request("/scribe-deepnotes Backpropagation")
    assert deep["template"] == "deepstudy-master"
    assert deep["master"] == "M1"
    assert deep["retired_command"] == "scribe-deepnotes"
    assert "/scribe-notes" in (deep.get("migration_hint") or "")

    notes_cmd = plan_notes.inspect_request("/scribe-notes Operating Systems")
    assert notes_cmd["template"] == "deepstudy-master"
    assert notes_cmd["master"] == "M1"

    study_cmd = plan_notes.inspect_request("/scribe-notes structured study notes on Operating Systems")
    assert study_cmd["template"] == "studynotes"
    assert study_cmd["master"] == "M2"


def test_routing_engine_cli_end_to_end(tmp_path):
    proc_reg = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "scribe.py"), "validate-registry"],
        capture_output=True, text=True, check=True,
    )
    assert json.loads(proc_reg.stdout)["valid"] is True

    proc_route = subprocess.run(
        [
            sys.executable, "-B", str(ROOT / "scripts" / "scribe.py"),
            "route", "Create deep notes on Gradient Descent and a separate formula sheet",
        ],
        capture_output=True, text=True, check=True,
    )
    routed = json.loads(proc_route.stdout)["routed"]
    assert routed["multi_artifact"] is True
    assert [a["master"] for a in routed["artifacts"]] == ["M1", "M3"]

    from scriptorium.engines.vault import ensure_obsidian_properties
    note_file = tmp_path / "m4.md"
    note_file.write_text(
        ensure_obsidian_properties(GRADIENT_DESCENT_OUTPUTS["M4"][1], topic="Gradient Descent", note_type="worked-solutions"),
        encoding="utf-8",
    )
    proc_val = subprocess.run(
        [
            sys.executable, "-B", str(ROOT / "scripts" / "scribe.py"),
            "validate", str(note_file), "--master", "M4",
        ],
        capture_output=True, text=True, check=True,
    )
    assert json.loads(proc_val.stdout)["valid"] is True
