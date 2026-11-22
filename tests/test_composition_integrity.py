"""Audit-derived regressions exercise refusal, actual artifacts and scoped repair."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest

from test_comprehensive_composition import specification, inputs, reviews_for
from scriptorium.engines.composition import (
    build_composition, allocate_depth, prepare_composition, publish_composition, validate_published_composition,
)
from scriptorium.engines.composition.contracts import repair_plan
from scriptorium.engines.composition.checks import (
    attention_mask, check_cost, check_diagnostics, check_example, check_failure, check_flow,
    check_implementation, check_numerical, check_proof, check_tensor, representation_metrics,
    heldout_linear_probe,
)
from scriptorium.models import content_hash


def proof(**updates):
    record = {"id": "p1", "claim": "An authored explanation, reviewed separately.",
              "assumptions": ["real scalar x and a"], "domain": "real scalars", "scope": "finite_update",
              "approximations": [], "boundary_conditions": ["a=0 is the identity update"],
              "steps": [{"lhs": "(x-a*x)**2", "rhs": "x*x-2*a*x*x+a*a*x*x", "relation": "identity", "reason": "expand the square"}]}
    return {**record, **updates}


def with_record(field, record):
    spec = specification()
    record = {"artifact_excerpt": "An authored explanation, reviewed separately.", **record}
    spec["concepts"][0][field] = [record]
    return build_composition(spec)


def assert_blocked(tmp_path, plan, marker):
    drafts, evidence, reviews = inputs(plan)
    result = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)
    assert not result["complete"] and not list(tmp_path.rglob("*.md"))
    assert marker in "\n".join(result["errors"]), result["errors"]
    assert (tmp_path / ".scriptorium/validation/col-gradient-descent.json").is_file()
    return result


def test_missing_prerequisite_before_equation_requires_a_bridge(tmp_path):
    spec = specification()
    spec["concepts"][0]["prerequisites"] = [{"id": "likelihood", "classification": "missing", "gap": "loss uses undefined likelihood",
                                            "resolved_excerpt": "Likelihood defines a conditional probability.", "before": "L=-log(p)"}]
    plan = build_composition(spec)
    assert_blocked(tmp_path, plan, "actual prerequisite bridge")
    drafts, evidence, _ = inputs(plan)
    drafts["ch1"] += "\nLikelihood defines a conditional probability.\nL=-log(p)\n"
    drafts, _ = prepare_composition(tmp_path, plan, drafts)
    assert publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews_for(plan, drafts))["complete"]


def test_tangent_geometry_does_not_imply_finite_step_norm_preservation(tmp_path):
    plan = with_record("proofs", proof(justification_scope="first_order", checks=[{
        "expression": "(1-0)**2+(0-0.1)**2", "expected": 1.0, "comparison": "allclose"}]))
    result = assert_blocked(tmp_path, plan, "first-order geometry")
    assert "counterexample" in " ".join(result["errors"])
    assert result["validation"]["outcomes"]["mathematical"]["status"] == "fail"


def test_theorem_conclusion_stronger_than_assumptions_is_rejected(tmp_path):
    plan = with_record("proofs", proof(conclusion_assumptions=["positive definiteness"]))
    assert_blocked(tmp_path, plan, "unstated assumptions")


def flow():
    return {"id": "branch1", "artifact_excerpt": "An authored explanation, reviewed separately.", "external_inputs": ["context", "target"], "branches": [
        {"id": "predictor", "inputs": ["context"], "outputs": ["prediction"], "accessible": ["context"], "forbidden": ["target"],
         "requires": ["context"], "attention_permissions": ["context"], "labels": "target outside forward context",
         "readout": "last context token", "shared_parameters": [], "gradient_owner": "predictor"}]}


def test_isolated_branch_cannot_read_forbidden_input(tmp_path):
    record = flow()
    assert not check_flow(record)
    record["branches"][0]["requires"] = ["target"]
    assert_blocked(tmp_path, with_record("information_flows", record), "cannot access")
    indirect = flow()
    indirect["branches"][0]["inputs"] = ["target"]
    assert any("forbidden" in e for e in check_flow(indirect))


def test_stipulated_vectors_are_not_model_forward_states(tmp_path):
    assert_blocked(tmp_path, with_record("examples", {"id": "ex1", "kind": "model_backed_execution", "state_origin": "hand_specified"}),
                   "not executed model states")


def test_component_snippet_cannot_be_called_a_complete_training_step(tmp_path):
    record = {"id": "impl1", "level": "component_snippet", "claims_full_training_step": True, "stages": {"forward": "model(x)"}}
    assert_blocked(tmp_path, with_record("implementations", record), "complete training step")


def test_zero_predictor_tokens_and_stabilized_boundary_behavior():
    tensor = {"name": "predictors", "shape": [2, 0, 8], "dtype": "float32", "role": "optional predictor embeddings",
              "valid_range": "real", "gradient_owner": "predictor", "indexing": "zero_based", "padding": "none",
              "boundaries": "no BOS/EOS here", "tokenizer": "schematic", "label_shift": 0, "readout": None}
    assert not check_tensor(tensor)
    tensor["readout"] = {"axis": 1, "position": 0}
    assert any("outside" in e for e in check_tensor(tensor))
    assert attention_mask([{"id": "c", "length": 2}, {"id": "p", "length": 0}], {"c": ["c"], "p": ["c"]}, causal=True) == [[True, False], [True, True]]
    assert not check_numerical({"expression": "x/(x*x+eps)", "variables": {"x": 0., "eps": 1e-8}, "expected": 0.,
                                "epsilon": 1e-8, "stabilizer_effect": "Changes the ideal singular expression at zero."})
    assert check_numerical({"expression": "1/0", "expected": 0.})
    assert check_numerical({"expression": "1", "expected": 1., "epsilon": 1e-8})
    assert check_numerical({"expression": "0.1+0.2", "expected": 0.3, "comparison": "exact"})
    assert not check_numerical({"expression": "0.1+0.2", "expected": 0.3, "comparison": "allclose"})


def _valid_png(width: int = 360, height: int = 200) -> bytes:
    import binascii, struct, zlib
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    raw = (b"\x00" + b"\x10\x40\x80" * width) * height
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


def visual_spec(vault_root: Path | None = None):
    spec = specification()
    if vault_root is not None:
        (vault_root / "fixture_curve.png").write_bytes(_valid_png())
    spec["concepts"][0]["depth"] = {"visual": 3}
    spec["concepts"][0]["visual_review"] = {"objective": "Understand curvature", "difficulty": "A tangent is local",
                                           "representation": "external retrieved figure", "placement": "Concept 1", "validation": "labels and axes"}
    spec["visuals"] = [{
        "id": "v1",
        "concept": "c1",
        "section": "Concept 1",
        "kind": "source_figure",
        "objective": "Quadratic curvature diagram",
        "url": "https://example.org/quadratic.png",
        "source": "https://example.org/article",
        "rights": "CC-BY-4.0",
        "alt": "Quadratic curvature diagram",
        "relevance": "Shows convex parabolic curvature.",
        "asset_policy": "offline_only",
        "local_fallback": "fixture_curve.png",
        "interpretation": "Slope and objective value are different quantities.",
    }]
    return spec


def test_visual_depth_without_artifact_cannot_silently_complete(tmp_path):
    spec = visual_spec()
    spec["visuals"] = []
    assert_blocked(tmp_path, build_composition(spec), "without a planned artifact")


def test_renderer_selection_without_execution_result_is_rejected(tmp_path):
    plan = build_composition(visual_spec(tmp_path))
    drafts, evidence, _ = inputs(plan)
    drafts, rendered = prepare_composition(tmp_path, plan, drafts)
    assert rendered["v1"]["status"] == "verified" and rendered["v1"]["attempted"]
    assert rendered["v1"]["path"] in drafts["ch1"]
    result = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews_for(plan, drafts))
    assert result["complete"], result["errors"]
    assert validate_published_composition(tmp_path, plan)["valid"]
    manifest = tmp_path / ".scriptorium/collections/col-gradient-descent.json"
    state = json.loads(manifest.read_text(encoding="utf-8"))
    state["renderers"] = {}
    manifest.write_text(json.dumps(state), encoding="utf-8")
    result = validate_published_composition(tmp_path, plan)
    assert not result["valid"] and any("persisted" in e or "renderer" in e for e in result["errors"])


def test_failed_render_attempt_is_persisted_and_does_not_publish(tmp_path):
    spec = visual_spec()
    spec["visuals"][0]["local_fallback"] = "missing_nonexistent.png"
    plan = build_composition(spec)
    result = assert_blocked(tmp_path, plan, "required visual")
    status = result["renderers"]["v1"]
    assert status["attempted"] and status["status"] == "failed" and status["failure_reason"]


def test_benchmark_without_exact_location_or_uncertainty_is_blocked(tmp_path):
    claim = {"id": "benchmark1", "text": "An authored explanation, reviewed separately.", "classification": "empirical_observation",
             "origin": "reported", "source": {"id": "https://example.test/paper"}, "empirical": {"metric": "accuracy"}}
    result = assert_blocked(tmp_path, with_record("claims", claim), "claim provenance missing location")
    assert "uncertainty" in " ".join(result["errors"])


@pytest.mark.parametrize("fault", ["diversity", "coverage", "hint", "solution"])
def test_assessment_quality_is_more_than_question_count(tmp_path, fault):
    spec = specification()
    if fault == "diversity":
        for q in spec["assessments"]: q["type"] = "conceptual"
    elif fault == "coverage":
        for q in spec["assessments"]: q["objectives"] = ["wrong-objective"]
    else:
        spec["assessments"][0][fault] = ""
    if fault == "coverage":
        with pytest.raises(ValueError, match="objective"):
            build_composition(spec)
        return
    plan = build_composition(spec)
    if fault in {"hint", "solution"}:
        with pytest.raises(ValueError, match="Assessment needs"):
            inputs(plan)
    else:
        assert_blocked(tmp_path, plan, "diversity" if fault == "diversity" else "coverage")


def test_valid_yaml_links_and_review_strings_do_not_prove_mathematics(tmp_path):
    plan = with_record("proofs", proof(steps=[{"lhs": "(x-a*x)**2", "rhs": "x*x", "reason": "tangent direction", "relation": "identity"}]))
    result = assert_blocked(tmp_path, plan, "identity fails")
    assert result["validation"]["outcomes"]["structural"]["status"] == "pass"
    assert result["validation"]["outcomes"]["mathematical"]["status"] == "fail"
    valid = build_composition(specification())
    drafts, evidence, _ = inputs(valid)
    result = publish_composition(tmp_path, valid, drafts, evidence=evidence, reviews={r: "checked" for r in valid["review_required"]})
    assert not result["complete"] and any("nonempty string" in e for e in result["errors"])


def test_versioned_source_snapshot_and_claim_are_verified_then_invalidated(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("Version 1, section 2: The update uses the current gradient.\n", encoding="utf-8")
    claim = {"id": "source1", "text": "An authored explanation, reviewed separately.", "classification": "reported_source_claim", "origin": "reported",
             "source": {"id": "supplied-fixture", "origin": "supplied", "version": "1", "location": "section 2", "verification_method": "read supplied snapshot",
                        "status": "verified", "limits": "fixture only; semantic entailment requires reviewer", "snapshot": "source.txt",
                        "excerpt": "The update uses the current gradient.", "hash": content_hash(source.read_bytes())}}
    plan = with_record("claims", claim)
    drafts, evidence, reviews = inputs(plan)
    assert publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)["complete"]
    source.write_text("Updated source with different assumptions.", encoding="utf-8")
    result = validate_published_composition(tmp_path, plan)
    assert not result["valid"] and any("snapshot/hash" in e for e in result["errors"])


def test_historical_tracing_does_not_activate_algorithm_state_depth():
    depth = allocate_depth({"objectives": ["Trace the evolution of an architecture"]}, source_policy="strict")
    assert depth["levels"]["algorithmic"] == 0 and depth["levels"]["conceptual"] >= 2
    assert allocate_depth({"objectives": ["trace scalar states"]}, source_policy="strict")["levels"]["algorithmic"] == 3


def test_targeted_repair_closure_and_cache_preserve_independent_chapter(tmp_path):
    spec = specification()
    spec["concepts"][4]["prerequisites"] = []  # a genuinely independent chapter
    spec["concepts"][0]["proofs"] = [proof()]
    plan = build_composition(spec)
    repair = repair_plan(plan, ["p1"])
    assert repair["obligations"][0] == "p1" and "ch5" in repair["preserve"]
    assert set(repair["chapters"]) == {"ch1", "ch2", "ch3", "ch4"}
    drafts, evidence, reviews = inputs(plan)
    first = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)
    assert first["complete"], first["errors"]
    second = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)
    assert second["complete"] and not second["written_paths"]
    assert second["validation"]["metrics"]["cached_checks"] == len(plan["obligations"])
    snapshots = {p: p.read_bytes() for p in tmp_path.rglob("*.md")}
    drafts["ch1"] += "\nAn explicit local correction.\n"
    reviews = reviews_for(plan, drafts)
    expected = {plan["chapters"][0]["path"]: content_hash(snapshots[tmp_path / plan["chapters"][0]["path"]].decode("utf-8"))}
    updated = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews, expected_hashes=expected)
    assert updated["complete"], updated["errors"]
    assert updated["written_paths"] == [plan["chapters"][0]["path"]]
    assert 0 < updated["validation"]["metrics"]["cached_checks"] < len(plan["obligations"])
    for path, raw in snapshots.items():
        if path != tmp_path / plan["chapters"][0]["path"]: assert path.read_bytes() == raw


def test_diagnostics_cost_and_failure_distinguish_measurements_from_inferences():
    measured = representation_metrics([[1., 0.], [0., 1.], [-1., 0.], [0., -1.]])
    assert measured["participation_ratio"] == 2 and measured["between_example_variance"] == 1
    assert check_diagnostics({"measurement": "2d_projection", "conclusion": "intrinsic_rank"})
    assert check_failure({"cause_established": True, "evidence_status": "symptom_only"})
    assert check_cost({"kind": "measured_benchmark"})
    assert check_example({"kind": "experimental_reproduction", "state_origin": "model_execution", "execution": {"level": "executed"}})


def test_terminology_contract_rejects_definition_after_first_equation(tmp_path):
    record = {"term": "likelihood", "definition": "Likelihood is a conditional probability.", "first_use": "L=-log(p)"}
    plan = with_record("terminology", record)
    drafts, evidence, _ = inputs(plan)
    drafts["ch1"] += "\nL=-log(p)\nLikelihood is a conditional probability.\n"
    result = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews_for(plan, drafts))
    assert not result["complete"] and any("prerequisite must precede" in e for e in result["errors"])


def test_native_disclosure_and_cli_preparation_and_repair(tmp_path):
    plan = build_composition(specification())
    drafts, _, _ = inputs(plan)
    assert "> [!hint]- Show hint" in drafts["ch1"] and "> [!answer]- Show detailed answer" in drafts["ch1"]
    spec = tmp_path / "spec.json"
    spec.write_text(json.dumps(specification()), encoding="utf-8")
    authored = tmp_path / "drafts.json"
    authored.write_text(json.dumps(drafts), encoding="utf-8")
    cli = Path(__file__).resolve().parents[1] / "scripts/scribe.py"
    result = subprocess.run([sys.executable, str(cli), "notes", "compose", "--spec", str(spec), "--vault", str(tmp_path),
                             "--drafts", str(authored), "--prepare"], text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["drafts"] == drafts
    result = subprocess.run([sys.executable, str(cli), "notes", "compose", "--spec", str(spec), "--repair", "c1:objective:0"],
                            text=True, capture_output=True)
    assert result.returncode == 0 and json.loads(result.stdout)["chapters"]


def test_flow_and_mask_verify_permissions_without_programmatic_svg(tmp_path):
    spec = specification()
    contract = flow()
    contract["mask"] = {"segments": [{"id": "context", "length": 2}, {"id": "predictor", "length": 1}],
                        "permissions": {"context": ["context"], "predictor": ["context", "predictor"]},
                        "causal": True, "readout_indices": [2],
                        "expected": [[True, False, False], [True, True, False], [True, True, True]]}
    assert check_flow(contract) == []
    spec["concepts"][0]["information_flows"] = [contract]
    spec["visuals"] = [{
        "id": "architecture-flow",
        "concept": "c1",
        "section": "Concept 1",
        "kind": "workflow",
        "objective": "Show isolated predictor inputs via native Mermaid",
        "nodes": [{"id": "ctx", "label": "Context Tokens"}, {"id": "pred", "label": "Predictor"}],
        "edges": [{"source": "ctx", "target": "pred", "label": "allowed"}],
    }]
    plan = build_composition(spec)
    drafts, evidence, _ = inputs(plan)
    drafts, renders = prepare_composition(tmp_path, plan, drafts)
    assert renders["architecture-flow"]["status"] == "verified"
    assert renders["architecture-flow"]["renderer"] == "mermaid"
    result = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews_for(plan, drafts))
    assert result["complete"], result["errors"]
    assert (tmp_path / ".scriptorium/renderers/col-gradient-descent.json").is_file()


def test_small_singular_spectrum_and_heldout_probe_are_operational_measurements():
    metrics = representation_metrics([[1., 0.], [0., 1.], [-1., 0.], [0., -1.]])
    assert metrics["singular_spectrum"][:2] == pytest.approx([2**.5, 2**.5])
    assert metrics["effective_dimension"] == pytest.approx(2.)
    probe = heldout_linear_probe([[1.], [2.], [3.]], [2., 4., 6.], [[4.], [5.]], [8., 10.])
    assert probe["heldout_mse"] < 1e-10 and probe["heldout_observations"] == 2
    assert representation_metrics([[1., 1.], [1., 1.]])["effective_dimension"] == 0
    with pytest.raises(ValueError, match="overflow"):
        representation_metrics([[1e200, 0.], [0., 1e200]])
    with pytest.raises(ValueError, match="regularization"):
        heldout_linear_probe([[1.]], [2.], [[2.]], [4.], ridge=float("nan"))


def test_context_compiler_loads_only_selected_capabilities_and_dependencies():
    from scriptorium.engines.composition import compile_context
    plan = build_composition(specification())
    compiled = compile_context(plan, ["c1"])
    assert compiled["verified"] and compiled["capability_count"] == 1
    assert compiled["selected_concepts"] == ["c1"] and compiled["actual_model_tokens"] is None
    assert "executable_obligations" in compiled["compiled_prompt"]
    assert "## Shared obligations and reviews" in compiled["compiled_prompt"]
    assert "## Mathematical and technical records" not in compiled["compiled_prompt"]
    assert all("assessment.md" not in f and "implementation-guide.md" not in f for f in compiled["loaded_files"])
    assert "c5:objective:0" not in compiled["dynamic_suffix"]


def test_polynomial_identity_checks_do_not_launder_numerical_samples_as_proof():
    assert not check_proof(proof())
    assert check_proof(proof(verification="numerical_samples", universal=True))
    assert check_proof(proof(steps=[{"lhs": "1/x", "rhs": "x**-1", "relation": "identity", "reason": "inverse"}]))


def test_edited_template_invalidates_existing_selective_context_cache(tmp_path):
    import shutil
    from scriptorium.engines._token_optimizer import MultiLevelCache, select_context_bundle
    root = Path(__file__).resolve().parents[1]
    shutil.copytree(root/"references", tmp_path/"references")
    shutil.copytree(root/"shared", tmp_path/"shared")
    cache = MultiLevelCache()
    kwargs = {"master": "M3", "knowledge_types": ["conceptual"], "root": tmp_path, "cache": cache}
    first = select_context_bundle(**kwargs)
    assert not first["cache_hit"] and select_context_bundle(**kwargs)["cache_hit"]
    unrelated = tmp_path/"references/templates/masters/assessment.md"
    unrelated.write_text(unrelated.read_text(encoding="utf-8")+"\nUnrelated change.\n", encoding="utf-8")
    assert select_context_bundle(**kwargs)["cache_hit"]
    active = tmp_path/"references/templates/masters/quick-reference.md"
    active.write_text(active.read_text(encoding="utf-8")+"\nRequired new reference guidance.\n", encoding="utf-8")
    changed = select_context_bundle(**kwargs)
    assert not changed["cache_hit"]
    assert "Required new reference guidance." in next(d["content"] for d in changed["loaded_docs"] if d["role"] == "master")


@pytest.mark.parametrize("malformed", ["unstructured evidence", ["not an evidence object"], {"unexpected": "mapping"}])
def test_malformed_review_receipts_fail_closed(tmp_path, malformed):
    plan = build_composition(specification())
    drafts, evidence, reviews = inputs(plan)
    reviews["factual_accuracy"]["evidence"] = malformed
    result = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)
    assert not result["complete"] and not list(tmp_path.rglob("*.md"))


def test_moc_and_authored_links_validate_actual_heading_anchors(tmp_path):
    plan = build_composition(specification())
    drafts, evidence, _ = inputs(plan)
    drafts["ch1"] += "\n[[02 - Chapter 2#Nonexistent|wrong anchor]]\n"
    result = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews_for(plan, drafts))
    assert not result["complete"] and any("unresolved wikilink anchor" in e for e in result["errors"])


def test_hybrid_representation_creates_individually_verified_parts(tmp_path):
    spec = visual_spec(tmp_path)
    external_fig = spec["visuals"][0]
    spec["visuals"] = [{"id": "hybrid", "concept": "c1", "section": "Concept 1", "kind": "hybrid",
                        "objective": "Connect retrieved curve figure to causal workflow", "parts": [external_fig,
                            {"id": "branch-diagram", "kind": "workflow", "objective": "Show independent input paths",
                             "nodes": [{"id": "a", "label": "Input A"}, {"id": "b", "label": "Output B"}],
                             "edges": [{"source": "a", "target": "b", "label": "flows to"}]}]}]
    plan = build_composition(spec)
    drafts, evidence, _ = inputs(plan)
    drafts, renders = prepare_composition(tmp_path, plan, drafts)
    assert len(renders) == 2 and all(r["status"] == "verified" for r in renders.values())
    result = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews_for(plan, drafts))
    assert result["complete"], result["errors"]
