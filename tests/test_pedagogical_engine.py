"""Comprehensive verification of the Pedagogical Intelligence Layer (P01-P11).

Covers all 19 Required Test Scenarios (Test A through Test S) plus the full
Backpropagation integration workflow through instructional_plan, plan_notes,
and validate_note.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from scriptorium.engines import _instructional as ip
from scriptorium.engines import _pedagogical_core as pe
import plan_notes
from validate_note import validate_text


def _norm(concepts, *, audience="beginner", source_policy="independent", sources=None):
    return ip.normalize_plan({
        "audience": audience,
        "source_policy": source_policy,
        "concepts": concepts,
        **({"sources": sources} if sources is not None else {}),
    })


# ===========================================================================
# Test A — Basic mathematics (Chain rule differentiation; no unnecessary coding)
# ===========================================================================

def test_a_basic_math_chain_rule_progressive_layers_and_no_code():
    plan = _norm([{
        "id": "chain-rule",
        "title": "Differentiation Using the Chain Rule",
        "types": ["mathematical"],
        "objectives": ["explain", "derive", "calculate"],
        "depth": {"math": 4, "theory": 4, "practice": 3},
        "prerequisites": [{"concept": "derivative", "treatment": "explain"}],
        "reason": "Progressive chain-rule derivation and worked examples.",
    }])
    pplan = pe.build_pedagogical_plan(plan)
    cplan = pplan["concepts"]["chain-rule"]
    assert cplan["explanation_plan"]["motivation"] in {"detailed", "standard"}
    assert cplan["explanation_plan"]["formalization"] == "deep"
    assert cplan["explanation_plan"]["worked_application"] in {"detailed", "deep"}
    assert cplan["implementation_plan"]["mode"] == "none"
    assert pplan["revision_plan"]["formula_reference_required"] is True


# ===========================================================================
# Test B — Advanced mathematics (Eigenvalues & eigenvectors)
# ===========================================================================

def test_b_advanced_math_eigenvalues_and_geometric_intuition():
    plan = _norm([{
        "id": "eigen",
        "title": "Eigenvalues and Eigenvectors",
        "types": ["mathematical", "conceptual"],
        "objectives": ["explain", "derive", "analyze"],
        "depth": {"math": 4, "visual": 3, "theory": 4},
        "prerequisites": [{"concept": "linear-transformations", "treatment": "reminder"}],
        "visualizations": [{"id": "V1", "type": "geometric_diagram", "purpose": "Show eigenvector scaling without rotation."}],
        "reason": "Geometric and algebraic treatment of eigen-decomposition.",
    }], audience="intermediate")
    pplan = pe.build_pedagogical_plan(plan)
    cplan = pplan["concepts"]["eigen"]
    assert cplan["explanation_plan"]["intuition"] == "detailed"
    assert cplan["explanation_plan"]["limitations"] == "detailed"
    assert cplan["visual_plan"][0]["type"] == "geometric_diagram"


# ===========================================================================
# Test C — Programming (Binary search in C)
# ===========================================================================

def test_c_programming_binary_search_in_c():
    plan = _norm([{
        "id": "bsearch-c",
        "title": "Binary Search in C",
        "types": ["algorithmic", "programming"],
        "objectives": ["explain", "trace", "implement", "debug"],
        "depth": {"code": 4, "theory": 3, "practice": 4},
        "implementation": {"required": True, "language": "c", "mode": "from_scratch", "reason": "Manual pointer/index bounds."},
        "prerequisites": [],
        "reason": "Precondition, invariant, C implementation, and boundary debugging.",
    }])
    pplan = pe.build_pedagogical_plan(plan)
    cplan = pplan["concepts"]["bsearch-c"]
    assert cplan["implementation_plan"]["mode"] == "from_scratch"
    assert cplan["implementation_plan"]["language"] == "c"
    assert cplan["explanation_plan"]["limitations"] in {"detailed", "standard"}


# ===========================================================================
# Test D — Machine learning (Gradient descent)
# ===========================================================================

def test_d_machine_learning_gradient_descent_with_graph_and_misconceptions():
    plan = _norm([{
        "id": "gd",
        "title": "Gradient Descent",
        "types": ["conceptual", "mathematical", "programming"],
        "objectives": ["explain", "calculate", "implement"],
        "depth": {"math": 3, "code": 3, "visual": 3},
        "prerequisites": [{"concept": "derivatives", "treatment": "reminder"}],
        "visualizations": [{
            "id": "V-GD",
            "type": "function_graph",
            "purpose": "Demonstrate parameter updates on J(theta)=theta^2.",
            "axes": {"x": "theta", "y": "J(theta)"},
            "mathematical_model": {"function": "theta^2", "variable": "theta"},
            "plotted_points": [[4, 16], [3.2, 10.24], [0, 0]],
        }],
        "misconception_plan": [
            {"id": "global_min", "type": "conceptual", "priority": "high", "correction": "Nonconvex losses have local minima/saddles."},
            {"id": "lr_overshoot", "type": "mathematical", "priority": "medium", "correction": "Excessive step size diverges."},
        ],
        "reason": "Full ML optimization treatment.",
    }])
    pplan = pe.build_pedagogical_plan(plan)
    report = pe.validate_pedagogical_quality("# Gradient Descent\n\nFor example, starting at theta=4 with step 0.1 gives theta=3.2.\n", pplan)
    assert not report["blocking"]


# ===========================================================================
# Test E — Neural-network mathematics (Full Backpropagation integration, Sec 21)
# ===========================================================================

def test_e_backpropagation_full_integration_workflow(tmp_path):
    vault = tmp_path / "vault"
    (vault / "Calculus").mkdir(parents=True)
    (vault / "Calculus" / "01 - Chain Rule.md").write_text(
        "---\nid: calc-01\naliases: [Chain Rule]\ntopic: Calculus\ntags: [calculus]\nnexttopics: []\n---\n\n# Chain Rule\n",
        encoding="utf-8",
    )

    inst_plan = {
        "audience": "intermediate",
        "source_policy": "independent",
        "concepts": [{
            "id": "backprop",
            "title": "Backpropagation",
            "types": ["conceptual", "mathematical", "programming"],
            "objectives": ["explain", "derive", "implement", "debug"],
            "depth": {"math": 4, "code": 4, "visual": 3, "theory": 4, "practice": 4},
            "prerequisites": [
                {"concept": "Chain Rule", "treatment": "explain"},
                {"concept": "loss function", "treatment": "reminder"},
            ],
            "canonical_spec": {
                "concept": "backprop",
                "symbols": {
                    "x": {"meaning": "scalar input", "value": 3.0},
                    "w": {"meaning": "scalar weight", "value": 2.0},
                    "dL_dw": {"meaning": "gradient wrt weight", "value": 18.0},
                },
                "equation": "dL_dw = w * x * x",
                "tensor_shapes": {"X": [4, 3], "W": [3, 2], "Y": [4, 2]},
                "tensor_operations": [{"op": "matmul", "left": "X", "right": "W", "output": "Y"}],
            },
            "visualizations": [{"id": "V-CG", "type": "flowchart", "purpose": "Forward and backward computational graph flow."}],
            "misconception_plan": [{"id": "bp_vs_gd", "type": "conceptual", "priority": "high", "correction": "Backprop computes gradients; SGD updates weights."}],
            "connection_plan": [{"target": "Chain Rule", "relation": "builds_upon", "bridge": "Applies the chain rule in reverse mode."}],
            "reason": "Full backpropagation derivation, shapes, and from-scratch implementation.",
        }],
    }
    item = {
        "title": "Backpropagation",
        "routing_reason": "Comprehensive backpropagation note.",
        "instructional_plan": inst_plan,
        "implementation_stack": ["python"],
    }
    plan = plan_notes.build_plan(vault, "/scribe-deepnotes Backpropagation", "Neural Networks", [item])
    contract = plan["plan"][0]["decision_contract"]
    pplan = contract["pedagogical_plan"]

    assert pplan["cross_topic_connections"][0]["status"] == "existing_note"
    assert pplan["concepts"]["backprop"]["implementation_plan"]["equation_mapping_required"] is True

    code = (
        "x, w = 3.0, 2.0\n"
        "def loss(w_val): return (w_val * x) ** 2 / 2\n"
        "dL_dw = w * x * x\n"
        "eps = 1e-5\n"
        "num = (loss(w + eps) - loss(w - eps)) / (2 * eps)\n"
        "assert abs(dL_dw - num) < 1e-7\n"
        "print(dL_dw)\n"
    )
    exec_check = pe.verify_executable_example(code, language="python", execute=True)
    assert exec_check["verification_tier"] == "tests_passed"
    assert exec_check["passed"] is True

    note = (
        "# Backpropagation\n\n"
        "## Prerequisite Bridge: Chain Rule\nThe [[Chain Rule]] multiplies local derivatives along composed functions.\n\n"
        "## Scalar Derivation\nFor input $x=3$ and weight $w=2$, the gradient $dL_dw = w x^2 = 18$.\n"
        "Backpropagation computes gradients; gradient descent uses them to update weights.\n"
    )
    report = pe.validate_pedagogical_quality(note, pplan, code_outputs={"backprop": {"dL_dw": 18.0}})
    assert not report["blocking"]


# ===========================================================================
# Test F — History (Development of the Internet; no forced math/code)
# ===========================================================================

def test_f_history_topic_timeline_and_no_forced_math_or_code():
    plan = _norm([{
        "id": "internet-history",
        "title": "Development of the Internet",
        "types": ["historical"],
        "objectives": ["explain"],
        "depth": {"theory": 3, "visual": 2},
        "visualizations": [{"id": "V-TL", "type": "timeline", "purpose": "ARPANET to TCP/IP and WWW milestones."}],
        "prerequisites": [],
        "reason": "Chronological historical narrative.",
    }])
    pplan = pe.build_pedagogical_plan(plan)
    cplan = pplan["concepts"]["internet-history"]
    assert cplan["implementation_plan"]["mode"] == "none"
    assert cplan["explanation_plan"]["formalization"] == "omitted"
    assert pplan["revision_plan"]["formula_reference_required"] is False


# ===========================================================================
# Test G — Physics (Biot-Savart law)
# ===========================================================================

def test_g_physics_biot_savart_law_prerequisites_geometry_and_units():
    plan = _norm([{
        "id": "biot-savart",
        "title": "Biot-Savart Law",
        "types": ["scientific", "mathematical"],
        "objectives": ["explain", "calculate"],
        "depth": {"math": 3, "visual": 3, "theory": 3},
        "prerequisites": [{"concept": "vector cross product", "treatment": "explain"}],
        "visualizations": [{"id": "V-BS", "type": "geometric_diagram", "purpose": "Current element dl, displacement r, and perpendicular dB."}],
        "reason": "Physical intuition, geometry, units (Tesla), and steady-current assumption.",
    }])
    pplan = pe.build_pedagogical_plan(plan)
    assert pplan["concepts"]["biot-savart"]["implementation_plan"]["mode"] == "none"
    assert pplan["concepts"]["biot-savart"]["visual_plan"][0]["type"] == "geometric_diagram"


# ===========================================================================
# Test H — Concept with few prerequisites (Standalone definition)
# ===========================================================================

def test_h_standalone_definition_avoids_forced_layers_visuals_or_examples():
    plan = _norm([{
        "id": "idempotence",
        "title": "Idempotence",
        "types": ["conceptual"],
        "objectives": ["define"],
        "depth": {"theory": 2},
        "prerequisites": [],
        "reason": "Concise standalone definition.",
    }])
    pplan = pe.build_pedagogical_plan(plan)
    cplan = pplan["concepts"]["idempotence"]
    assert cplan["explanation_plan"]["motivation"] == "omitted"
    assert cplan["explanation_plan"]["formalization"] == "omitted"
    assert "visual_plan" not in cplan
    assert "example_plan" not in cplan
    assert pplan["revision_plan"]["layer_b_concept_review"] is False


# ===========================================================================
# Test I — Source-only material (Strict source order & provenance attribution)
# ===========================================================================

def test_i_source_only_preserves_source_order_and_flags_unlabeled_illustrations():
    # Source order has consumer 'c1' before essential prerequisite 'c2' -> preserve source order + insert local bridge!
    dep_graph = pe.build_cognitive_dependency_graph(
        [
            {"id": "c1", "title": "Loss Reduction", "prerequisites": [{"concept": "c2", "type": "essential", "treatment": "bridge"}]},
            {"id": "c2", "title": "Mean Squared Error", "prerequisites": []},
        ],
        source_policy="strict",
    )
    assert dep_graph["source_order_preserved"] is True
    assert dep_graph["teaching_order"] == ["c1", "c2"]
    assert len(dep_graph["source_order_bridges"]) == 1
    assert dep_graph["source_order_bridges"][0]["action"] == "insert_local_bridge"

    # Unlabeled illustrative example in strict mode is flagged
    ex_issues = pe.audit_examples(
        [{"id": "EX-1", "category": "worked", "mechanism": "mse", "provenance": "illustrative", "labeled_as_addition": False}],
        concept_id="c1",
        source_policy="strict",
    )
    assert any(i["type"] == "unlabeled_illustrative_example_in_strict_mode" for i in ex_issues)


# ===========================================================================
# Test J — Conflicting representations (Inconsistent equation vs code & tensor shapes)
# ===========================================================================

def test_j_conflicting_representations_detected_for_equation_code_and_shapes():
    spec = {
        "concept": "linreg",
        "symbols": {"x": {"value": 3}, "w": {"value": 2}, "b": {"value": 1}, "y_hat": {"value": 7}},
        "equation": "y_hat = w * x + b",
        "tensor_shapes": {"X": [4, 3], "W": [5, 2], "Y": [4, 2]},
        "tensor_operations": [{"op": "matmul", "left": "X", "right": "W", "output": "Y"}],
    }
    # Code erroneously returned 9 instead of 7, AND tensor shapes [4,3] @ [5,2] clash!
    issues = pe.validate_representations(spec, code_outputs={"y_hat": 9.0})
    types = {i["type"] for i in issues}
    assert "equation_code_conflict" in types
    assert "tensor_shape_mismatch" in types
    assert all(i["severity"] == "critical" for i in issues)


# ===========================================================================
# Test K — Missing prerequisite (Chain rule used without bridge)
# ===========================================================================

def test_k_missing_prerequisite_detected_and_actionable():
    dep_graph = pe.build_cognitive_dependency_graph([
        {"id": "backprop", "title": "Backpropagation", "prerequisites": [{"concept": "chain rule", "type": "essential", "treatment": "bridge"}]},
    ])
    gaps = pe.detect_dependency_gaps("# Backpropagation\n\nMultiply upstream sensitivity by local Jacobian.\n", dep_graph)
    assert len(gaps) == 1
    assert gaps[0]["type"] == "missing_prerequisite_bridge"
    assert gaps[0]["severity"] == "major"
    assert gaps[0]["requires_regeneration"] is False

    # Cycle detection on essential dependencies
    cyc_graph = pe.build_cognitive_dependency_graph([
        {"id": "a", "title": "A", "prerequisites": [{"concept": "b", "type": "essential"}]},
        {"id": "b", "title": "B", "prerequisites": [{"concept": "a", "type": "essential"}]},
    ])
    assert cyc_graph["has_essential_cycles"] is True


# ===========================================================================
# Test L — Redundant examples detected and consolidated
# ===========================================================================

def test_l_redundant_examples_detected():
    examples = [
        {"id": "EX-1", "category": "worked", "mechanism": "dot product update", "boundary_or_twist": "standard"},
        {"id": "EX-2", "category": "worked", "mechanism": "dot product update", "boundary_or_twist": "standard"},
        {"id": "EX-3", "category": "counterexample", "mechanism": "dot product update", "boundary_or_twist": "non-separable XOR"},
    ]
    issues = pe.audit_examples(examples, concept_id="perceptron")
    assert len(issues) == 1
    assert issues[0]["type"] == "redundant_example"
    assert issues[0]["location"] == "EX-2"


# ===========================================================================
# Test M — Misleading visualization (Bad plotted point / missing axis / bad HTML)
# ===========================================================================

def test_m_misleading_visualization_axis_value_and_html_detected():
    visuals = [{
        "id": "V-BAD",
        "type": "function_graph",
        "purpose": "Plot parabola J(theta)=theta^2",
        "axes": {"x": "theta"},  # Missing y axis label!
        "mathematical_model": {"function": "theta^2", "variable": "theta"},
        "plotted_points": [[3, 9], [4, 20]],  # 4^2 = 16, not 20!
    }]
    issues = pe.validate_visuals(visuals, note_text="<script>alert(1)</script>")
    types = {i["type"] for i in issues}
    assert "missing_axis_labels" in types
    assert "misleading_plotted_value" in types
    assert "unsupported_obsidian_html" in types


# ===========================================================================
# Test N — Code execution failure & untrusted source guard
# ===========================================================================

def test_n_code_execution_failure_and_untrusted_code_guard():
    buggy = (
        "def binary_search(arr, target):\n"
        "    lo, hi = 0, len(arr) - 1\n"
        "    while lo < hi:\n"  # Boundary bug: misses single-element match!
        "        mid = (lo + hi) // 2\n"
        "        if arr[mid] == target: return mid\n"
        "        elif arr[mid] < target: lo = mid + 1\n"
        "        else: hi = mid - 1\n"
        "    return -1\n"
        "assert binary_search([5], 5) == 0\n"
    )
    res_bug = pe.verify_executable_example(buggy, language="python", execute=True)
    assert res_bug["passed"] is False and res_bug["executed"] is True

    fixed = buggy.replace("while lo < hi:", "while lo <= hi:")
    res_ok = pe.verify_executable_example(fixed, language="python", execute=True)
    assert res_ok["passed"] is True and res_ok["verification_tier"] == "tests_passed"

    # Untrusted retrieved code must never execute
    res_untrusted = pe.verify_executable_example("print('hi')", untrusted_source=True, execute=True)
    assert res_untrusted["executed"] is False and res_untrusted["verification_tier"] == "generated"


# ===========================================================================
# Test O — Cross-topic links & Link-inflation guard
# ===========================================================================

def test_o_cross_topic_vault_resolution_and_link_inflation(tmp_path):
    vault = tmp_path / "vault"
    (vault / "ML").mkdir(parents=True)
    (vault / "ML" / "01 - Gradient Descent.md").write_text(
        "---\nid: ml-gd\naliases: [Gradient Descent]\ntopic: ML\ntags: [ml]\nnexttopics: []\n---\n\n# Gradient Descent\n",
        encoding="utf-8",
    )
    conns = [
        {"target": "Gradient Descent", "relation": "used_together_with", "bridge": "Uses computed gradients to update weights."},
        {"target": "Adam Optimizer", "relation": "alternative_to", "bridge": "Adaptive moments."},
        {"target": "Unknown Future Topic", "relation": "applies"},
    ]
    overlinked = " ".join(f"[[Term{i}]] word" for i in range(25))
    res = pe.resolve_cross_topic_connections(conns, vault=vault, planned_stems={"Adam Optimizer"}, note_text=overlinked)
    statuses = {c["target"]: c["status"] for c in res["connections"]}
    assert statuses["Gradient Descent"] == "existing_note"
    assert statuses["Adam Optimizer"] == "planned_note"
    assert statuses["Unknown Future Topic"] == "unresolved_concept"
    assert any(i["type"] == "link_inflation" for i in res["issues"])


# ===========================================================================
# Test P — Revision integrity (Assumptions preserved, anchors valid, no verbatim copy)
# ===========================================================================

def test_p_revision_integrity_checks_conditions_anchors_and_duplication():
    repeated_para = (
        "Gradient descent updates parameters iteratively by stepping opposite the gradient of a differentiable objective "
        "function with respect to each parameter so that local decreases accumulate over iterations."
    )
    full_note = f"# Gradient Descent\n\n## Update Rule\n{repeated_para}\n\n$$\\theta_{{t+1}} = \\theta_t - \\alpha \\nabla J(\\theta_t)$$\n"
    bad_revision = (
        "## Rapid Revision\n"
        f"{repeated_para}\n\n"
        "Formula: `theta_{t+1} = theta_t - alpha * grad(J)` — see [[#Nonexistent Heading]].\n"
    )
    issues = pe.validate_revision_integrity(
        full_note,
        bad_revision,
        canonical_formulas=[{"formula": "theta_{t+1} = theta_t - alpha * grad(J)", "conditions": ["differentiable objective", "step size bound"]}],
    )
    types = {i["type"] for i in issues}
    assert "formula_stripped_of_conditions" in types
    assert "broken_revision_anchor" in types
    assert "verbatim_revision_duplication" in types


# ===========================================================================
# Test Q — Cognitive load detection on dense introductory note
# ===========================================================================

def test_q_cognitive_load_detects_symbol_overload_and_missing_example_for_beginners():
    dense_note = (
        "# Dense Math\n\n"
        "Consider $a$, $b$, $c$, $d$, $e$, $f$, $g$, and $h$ transforming $\\Omega$ into $\\Lambda$.\n\n"
        "$$y = a x + b$$\n\n$$z = c y + d$$\n\n$$w = e z + f$$\n"
    )
    issues = pe.audit_cognitive_load(dense_note, audience="beginner")
    types = {i["type"] for i in issues}
    assert "symbol_overload_without_definitions" in types
    assert "dense_formalism_without_example" in types


# ===========================================================================
# Test R — Nontechnical topic (Literary theme / philosophical argument)
# ===========================================================================

def test_r_nontechnical_topic_uses_conceptual_layers_without_forced_math_code_or_visuals():
    plan = _norm([{
        "id": "tragedy",
        "title": "Aristotelian Hamartia in Classical Tragedy",
        "types": ["conceptual", "comparative"],
        "objectives": ["explain", "compare"],
        "depth": {"theory": 3},
        "prerequisites": [],
        "reason": "Conceptual literary analysis without technical formulas or code.",
    }])
    pplan = pe.build_pedagogical_plan(plan)
    cplan = pplan["concepts"]["tragedy"]
    assert cplan["implementation_plan"]["mode"] == "none"
    assert cplan["explanation_plan"]["formalization"] == "omitted"
    assert "visual_plan" not in cplan
    assert pplan["revision_plan"]["formula_reference_required"] is False


# ===========================================================================
# Test S — Regression safety, validate_note integration & CLI
# ===========================================================================

def test_s_validate_note_and_cli_enforce_blocking_pedagogical_defects(tmp_path):
    plan = _norm([{
        "id": "c1",
        "title": "Linear Prediction",
        "types": ["mathematical"],
        "objectives": ["explain", "calculate"],
        "depth": {"math": 3},
        "canonical_spec": {
            "concept": "c1",
            "symbols": {"x": {"value": 3}, "w": {"value": 2}, "y": {"value": 99}},  # Wrong! 2*3 = 6 != 99
            "equation": "y = w * x",
        },
        "prerequisites": [],
        "reason": "Verify blocking defect propagates into validate_note.",
    }])
    contract = ip.resolve_instructional_contract("/scribe-deepnotes Linear Prediction", "Linear Prediction", plan)
    note = (
        "---\nid: lin-01\naliases: [Linear Prediction]\ntopic: Linear Prediction\ntags: [math]\nnexttopics: []\n---\n\n"
        "# Linear Prediction\n\nGiven $x=3$ and $w=2$, compute $y = wx$.\n"
    )
    findings = validate_text(note, route="deepstudy-master", decision_contract=contract)
    assert any("PED-001" in msg and "contradicting" in msg for _, msg in findings)

    # CLI check
    ip_file = tmp_path / "ip.json"
    ip_file.write_text(json.dumps(plan), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "scribe.py"), "pedagogy", "plan", "--instructional-plan", str(ip_file)],
        capture_output=True, text=True, check=True,
    )
    cli_out = json.loads(proc.stdout)
    assert cli_out["pedagogical_contract_version"] == 1
    assert "c1" in cli_out["concepts"]
