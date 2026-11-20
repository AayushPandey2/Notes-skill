"""Behavioral scenarios for per-concept planning, composition, selective module activation, source gating, and negative legacy regression checks."""
from copy import deepcopy
import json
from pathlib import Path
import re
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from scriptorium.engines._decision import resolve_decisions, audit_note_against_contract
from scriptorium.engines._instructional import (
    CONTRACT_VERSION,
    audit_modern_note,
    build_concept_dependency_graph,
    compose_concept_sequence,
    compose_document_outline,
    coverage_errors,
    normalize_plan,
    registry,
    resolve_instructional_contract,
)
from scriptorium.engines._instructional import adapt_legacy_contract, from_legacy
from scriptorium import layout as note_layout
from plan_notes import build_plan, start_plan, publish
from scriptorium.engines._verification import Block, required_examples, verify_runtimes
from validate_note import validate_text

SCENARIOS = json.loads((ROOT / "examples/adaptive-deepnotes/scenarios.json").read_text(encoding="utf-8"))


def resolve(case):
    return resolve_decisions("/scribe-deepnotes " + case["topic"], case["item"], case["topic"])


@pytest.mark.parametrize("case", SCENARIOS, ids=lambda c: c["name"])
def test_scenarios_survive_the_actual_planner(tmp_path, case):
    plan = build_plan(tmp_path, "/scribe-deepnotes " + case["topic"], ".", [case["item"]])
    contract = plan["plan"][0]["decision_contract"]
    assert contract == resolve(case)
    assert contract["contract_version"] == CONTRACT_VERSION == 3
    assert contract["route"] == "deepstudy-master"
    assert normalize_plan(contract["instructional_plan"]) == contract["instructional_plan"]
    assert "composed_outline" in contract
    assert "dependency_graph" in contract
    assert "concept_depths" in contract


def test_distinct_subjects_select_distinct_capabilities():
    contracts = {c["name"]: resolve(c) for c in SCENARIOS}
    for name in ("A-conceptual", "F-historical"):
        assert contracts[name]["math_level"] == 0
        assert contracts[name]["implementation_stack"] == []
    math = contracts["B-mathematical"]["instructional_plan"]["concepts"]
    assert [c["depth"]["math"] for c in math] == [2, 4, 0]
    assert [c["depth"]["code"] for c in math] == [0, 0, 3]
    assert contracts["C-programming"]["implementation_stack"] == ["python"]
    architecture = contracts["D-architectural"]["instructional_plan"]["concepts"][0]
    assert architecture["depth"]["visual"] == 4 and architecture["depth"]["code"] == 0
    assert contracts["E-procedural"]["instructional_plan"]["concepts"][0]["modules"]["applications"]["status"] == "required"
    assert contracts["F-historical"]["instructional_plan"]["concepts"][0]["modules"]["history"]["status"] == "required"
    assert contracts["H-mixed"]["implementation_stack"] == ["python-numpy"]
    beginner = contracts["I-beginner"]["instructional_plan"]["concepts"][0]
    advanced = contracts["I-advanced"]["instructional_plan"]["concepts"][0]
    assert beginner["prerequisites"][0]["treatment"] == "explain"
    assert advanced["prerequisites"][0]["treatment"] == "known"
    assert beginner["modules"]["proof"]["status"] == "excluded"
    assert advanced["modules"]["proof"]["status"] == "required"


@pytest.mark.parametrize("policy", ["strict", "expanded", "comparative"])
def test_source_requirements_activate_modules_and_missing_inventory_fails(policy):
    raw = deepcopy(SCENARIOS[6]["item"]["instructional_plan"])
    raw["source_policy"] = policy
    normalized = normalize_plan(raw)
    for name in ("definitions", "examples", "visualization", "assessment", "limitations"):
        assert normalized["concepts"][0]["modules"][name]["status"] == "required"
    raw["sources"] = []
    with pytest.raises(ValueError, match="inventory"):
        normalize_plan(raw)


def test_invalid_dependencies_and_conflicting_objectives_fail_before_writing():
    raw = deepcopy(SCENARIOS[1]["item"]["instructional_plan"])
    raw["concepts"][0]["prerequisites"] = [{"concept": "update", "treatment": "explain"}]
    with pytest.raises(ValueError, match="cycle or forward dependency"):
        normalize_plan(raw)
    raw = deepcopy(SCENARIOS[-1]["item"]["instructional_plan"])
    raw["concepts"][0]["depth"] = {"math": 2}
    with pytest.raises(ValueError, match="conflicts"):
        normalize_plan(raw)
    raw["concepts"][0]["depth"] = {}
    raw["concepts"][0]["modules"] = {"proof": {"status": "excluded", "depth": 0, "reason": "Budget is small"}}
    with pytest.raises(ValueError, match="Cannot drop"):
        normalize_plan(raw)


def test_module_dependencies_optional_extensions_and_depth_types():
    raw = deepcopy(SCENARIOS[0]["item"]["instructional_plan"])
    concept = raw["concepts"][0]
    concept["modules"] = {"history": {"status": "optional", "depth": 1, "reason": "Optional provenance extension"}}
    assert normalize_plan(raw)["concepts"][0]["modules"]["history"]["status"] == "optional"
    concept["depth"]["math"] = True
    with pytest.raises(ValueError, match="integer"):
        normalize_plan(raw)
    concept["depth"]["math"] = 3
    concept["modules"]["definitions"] = {"status": "excluded", "depth": 0, "reason": "Remove duplication"}
    with pytest.raises(ValueError, match="Cannot drop|depends on"):
        normalize_plan(raw)


def source_report(plan):
    return {"elements": [{"id": s["id"], "status": "validated", "anchor": s["id"],
                           "note": "Checked against the synthetic fixture; additions labeled."} for s in plan["sources"]]}


def test_source_publication_blocks_incomplete_coverage_and_preserves_receipt(tmp_path):
    case = SCENARIOS[6]
    vault = tmp_path / "vault"
    vault.mkdir()
    plan_id, saved = start_plan(vault, "/scribe-deepnotes Ordered Lookup", ".", [case["item"]])
    item = saved["plan"][0]
    metadata = dict(id=item["note_id"], aliases=[item["title"]], topic=case["topic"], tags=["lookup"], nexttopics=[])
    body = "\n# Ordered Lookup\n\n" + "\n\n".join([
        "## Definition\nA sorted ascending sequence has no element smaller than its predecessor.",
        "## Example\nIn [2, 5, 9, 14, 20], searching for 14 excludes the middle value 9 and all earlier values.",
        "## Figure\nThe source's candidate divider separates discarded [2, 5, 9] from remaining [14, 20].",
        "## Exercise\nSource question: seek 5. Educational solution: [2, 5] remain because 5 is less than 9.",
        "## Qualification\nDiscarding a side relies on sorted input. Duplicate policy is a separate requirement."])
    draft = tmp_path / "draft.md"
    draft.write_text("---\n" + yaml.safe_dump(metadata, sort_keys=False) + "---\n" + body, encoding="utf-8")
    plan = item["decision_contract"]["instructional_plan"]
    with pytest.raises(ValueError, match="coverage"):
        publish(vault, plan_id, item["id"], draft)
    target = vault / item["output_path"]
    assert not target.exists()
    report = source_report(plan)
    partial = deepcopy(report)
    partial["elements"].pop()
    with pytest.raises(ValueError, match="required source element"):
        publish(vault, plan_id, item["id"], draft, coverage=partial)
    assert "published" in publish(vault, plan_id, item["id"], draft, coverage=report)
    receipt = vault / ".scriptorium" / "plans" / plan_id / (item["id"] + ".coverage.json")
    accepted = json.loads(receipt.read_text(encoding="utf-8"))
    assert accepted["report"] == report and len(accepted["draft_hash"]) == 64
    assert publish(vault, plan_id, item["id"], draft) == "already complete"
    assert "Ignore all previous instructions" not in target.read_text(encoding="utf-8")


def test_coverage_rejects_fabricated_anchor_duplicates_and_unread_elements():
    plan = resolve(SCENARIOS[6])["instructional_plan"]
    report = source_report(plan)
    headings = "\n".join("## " + s["id"] for s in plan["sources"])
    assert not coverage_errors(plan, report, headings)
    assert any("Source order" in e for e in coverage_errors(plan, report, "\n".join(reversed(headings.splitlines()))))
    assert coverage_errors(plan, report, "```text\n" + headings + "\n```")
    report["elements"].append(deepcopy(report["elements"][0]))
    assert any("duplicate" in error for error in coverage_errors(plan, report, headings))
    plan["sources"][0]["access"] = "partial"
    assert any("inaccessible" in error for error in coverage_errors(plan, report, headings))


def test_legacy_contract_checks_and_short_executable_examples_remain_distinct():
    legacy = {"template": "deepstudy-master", "math_level": 0, "code_depth": "none"}
    assert any("forbids" in m for _, m in audit_note_against_contract("$$x = y + z$$", legacy))
    # A complete short example need not be padded to satisfy a line count.
    blocks = [Block(1, "python", "def square(x):\n    return x * x\nassert square(-3) == 9\nprint(square(-3))\n")]
    assert not required_examples(blocks, ["python"], minimum_lines=1)[1]
    assert required_examples(blocks, ["python"])[1]


def test_registry_dependencies_resolve_and_soft_budgets_do_not_drop_requirements():
    modules = registry()["modules"]
    for spec in modules.values():
        assert set(spec["depends"]) <= modules.keys()
        assert spec["inputs"] and spec["outputs"] and spec["check"]
    plan = resolve(SCENARIOS[-1])["instructional_plan"]
    assert plan["estimated_output_tokens"] > 0
    assert plan["concepts"][0]["modules"]["proof"]["status"] == "required"


def test_structured_programming_plan_executes_and_publishes(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    case = SCENARIOS[2]
    plan_id, saved = start_plan(vault, "/scribe-deepnotes Binary Search", ".", [case["item"]])
    item = saved["plan"][0]
    code = (ROOT / "examples/adaptive-deepnotes/binary_search.py").read_text(encoding="utf-8")
    result = verify_runtimes({"python": Block(1, "python", code)}, [])["python"]
    assert result["status"] == "executed"
    metadata = dict(id=item["note_id"], aliases=[item["title"]], topic=case["topic"], tags=["search"], nexttopics=[])
    body = ("# Binary Search\n\n"
            "The candidate interval includes lo and excludes hi. Sorted input lets a comparison discard half the remaining positions.\n\n"
            "For [2, 5, 9, 14, 20] seeking 14, the first midpoint is index 2 (value 9). Set lo to 3; index 4 is then too large, so hi becomes 4. Index 3 matches.\n\n"
            "Every iteration either returns or shrinks the candidate interval. No possible match is discarded, so an empty interval establishes absence.\n\n"
            "Indexing uses constant space; repeated halving takes logarithmically many comparisons. Unsorted input violates the contract. Duplicate input permits any matching index.\n\n"
            "## Implementation\n```python\n" + code + "```\n\n"
            "## Verification\n### Verification — python\nStatus: executed\n")
    if result.get("version"):
        body += "Version: " + result["version"] + "\n"
    body += "\n```text\n" + result["stdout"] + "```\n"
    draft = tmp_path / "draft.md"
    draft.write_text("---\n" + yaml.safe_dump(metadata, sort_keys=False) + "---\n" + body, encoding="utf-8")
    assert "published" in publish(vault, plan_id, item["id"], draft)


def test_explicit_stack_conflict_is_not_silently_ignored():
    case = deepcopy(SCENARIOS[0])
    case["item"]["implementation_stack"] = ["rust"]
    with pytest.raises(ValueError, match="Explicit implementation stack conflicts"):
        resolve(case)


def test_legacy_purpose_can_require_math_without_a_domain_keyword():
    contract = resolve_decisions("Study this result", {"title": "Result", "purpose": "prove"}, "General")
    assert contract["legacy_adapted"] is True
    assert contract["instructional_plan"]["concepts"][0]["depth"]["math"] == 5
    assert contract["math_level"] == 3
    with pytest.raises(ValueError, match="conflicts"):
        resolve_decisions("Study this result", {"title": "Result", "purpose": "prove", "math_level": 0}, "General")


def test_saved_zero_math_profile_rejects_unplanned_equations():
    contract = {**resolve(SCENARIOS[0]), "explicit_contract": True}
    assert any("all-M0" in m for _, m in audit_note_against_contract("$$x = y + z$$", contract))


def test_composer_deduplicates_multi_type_subtemplates():
    raw = {
        "audience": "intermediate",
        "source_policy": "independent",
        "concepts": [
            {
                "id": "conv",
                "title": "Discrete Convolution and Kernel Implementation",
                "types": ["conceptual", "mathematical", "algorithmic", "programming"],
                "objectives": ["explain", "calculate", "trace", "implement"],
                "depth": {"math": 3, "code": 3, "theory": 3, "practice": 3},
                "prerequisites": [{"concept": "dot-product", "treatment": "reminder"}],
                "reason": "Multi-type concept combining theory, math, algorithm, and code.",
            }
        ],
    }
    plan = normalize_plan(raw)
    seq = plan["concepts"][0]["composed_sequence"]
    stage_names = [s["stage"] for s in seq]
    # Every canonical stage appears at most once (no duplicated introduction or definition stages)
    assert len(stage_names) == len(set(stage_names))
    assert stage_names[0] == "prerequisite_preparation"
    assert stage_names.index("definitions_and_setup") < stage_names.index("mathematical_formulation")
    assert stage_names.index("mathematical_formulation") < stage_names.index("implementation_and_code")


# ===========================================================================
# MANDATORY NEGATIVE TESTS 1 THROUGH 8 (Section 21.4)
# ===========================================================================


def test_negative_1_deep_notes_do_not_route_subtopics_to_api_table_or_atomic_from_impl_weight_or_density(tmp_path):
    """Negative test 1: A deep-note plan does not route subtopics to api-table or atomic because of impl_weight or density."""
    items = [
        {
            "title": "PyTorch Conv2d Reference & Parameters",
            "purpose": "reference",
            "impl_weight": "high",
            "density": "callables",
            "routing_reason": "Deep study of Conv2d parameter effects.",
            "instructional_plan": deepcopy(SCENARIOS[0]["item"]["instructional_plan"]),
        },
        {
            "title": "Residual Skip Definition",
            "purpose": "definition",
            "impl_weight": "low",
            "density": "micro",
            "routing_reason": "Deep study of skip connections.",
            "instructional_plan": deepcopy(SCENARIOS[0]["item"]["instructional_plan"]),
        },
    ]
    plan = build_plan(tmp_path, "/scribe-deepnotes CNN Architecture", "CNN", items)
    assert plan["plan"][0]["template"] == "deepstudy-master"
    assert plan["plan"][1]["template"] == "deepstudy-master"


def test_negative_2_topic_keywords_do_not_clamp_or_force_mathematics():
    """Negative test 2: Topic keywords do not clamp or force mathematics when the instructional plan specifies a different concept-level mathematical depth."""
    # Sociology/History topic with explicit M5 proof objective -> never clamped to 0
    raw = {
        "audience": "advanced",
        "source_policy": "independent",
        "concepts": [
            {
                "id": "arrow",
                "title": "Arrow's Impossibility Theorem in Social Choice",
                "types": ["mathematical", "historical"],
                "objectives": ["prove", "explain"],
                "depth": {"math": 5, "theory": 5},
                "prerequisites": [],
                "reason": "Rigorous social-choice proof.",
            }
        ],
    }
    contract = resolve_decisions("/scribe-deepnotes World History & Sociology", {"title": "Social Choice", "instructional_plan": raw}, "World History")
    assert contract["concept_depths"]["arrow"]["math"] == 5
    assert contract["instructional_plan"]["concepts"][0]["modules"]["proof"]["status"] == "required"

    # Pure Mathematics topic with explicit M0 conceptual overview -> never forced to M2/M3
    raw_zero = {
        "audience": "beginner",
        "source_policy": "independent",
        "concepts": [
            {
                "id": "intuition",
                "title": "Why Topology Studies Continuity Without Distance",
                "types": ["conceptual"],
                "objectives": ["explain"],
                "depth": {"math": 0, "theory": 3},
                "prerequisites": [],
                "reason": "Purely qualitative conceptual orientation.",
            }
        ],
    }
    contract_zero = resolve_decisions("/scribe-deepnotes Pure Mathematics Topology", {"title": "Topology Overview", "instructional_plan": raw_zero}, "Pure Mathematics")
    assert contract_zero["concept_depths"]["intuition"]["math"] == 0
    assert contract_zero["math_level"] == 0


def test_negative_3_topic_keywords_do_not_auto_generate_multi_framework_stacks():
    """Negative test 3: Topic keywords do not automatically generate multi-framework implementation stacks."""
    raw = {
        "audience": "intermediate",
        "source_policy": "independent",
        "concepts": [
            {
                "id": "update",
                "title": "Perceptron Weight Update Implementation",
                "types": ["programming", "algorithmic"],
                "objectives": ["implement", "trace"],
                "depth": {"code": 3},
                "prerequisites": [],
                "reason": "Single transparent implementation.",
            }
        ],
    }
    contract = resolve_decisions(
        "/scribe-deepnotes Perceptron Deep Learning Neural Network",
        {"title": "Implementations", "purpose": "implement", "impl_weight": "high", "instructional_plan": raw},
        "Perceptron",
    )
    assert len(contract["implementation_stack"]) == 1
    assert contract["implementation_stack"] == ["python"]


def test_negative_4_non_computing_subject_with_explicit_simulation_plan_is_not_blocked_by_domain_heuristics(tmp_path):
    """Negative test 4: A non-computing subject with an explicit simulation or computational instructional plan is not blocked by legacy domain heuristics."""
    raw = {
        "audience": "intermediate",
        "source_policy": "independent",
        "concepts": [
            {
                "id": "sim",
                "title": "Simulate Snell Refraction Ray Paths",
                "types": ["scientific", "programming"],
                "objectives": ["explain", "implement"],
                "depth": {"math": 3, "code": 3},
                "implementation": {
                    "required": True,
                    "language": "python",
                    "framework": "python-numpy",
                    "approach": "complete",
                    "reason": "Numerical ray-tracing verification.",
                },
                "prerequisites": [],
                "reason": "Computational physics simulation concept.",
            }
        ],
    }
    # Note: request text does NOT contain the word 'python' or 'simulate'; the instructional_plan itself authorizes code.
    plan = build_plan(
        tmp_path,
        "/scribe-deepnotes Wave Optics",
        "Wave Optics",
        [{"title": "Huygens Principle & Ray Trace", "routing_reason": "Teach wave optics with ray simulation.", "instructional_plan": raw}],
    )
    entry = plan["plan"][0]
    assert entry["decision_contract"]["contract_version"] == 3
    assert entry["decision_contract"]["implementation_stack"] == ["python-numpy"]
    assert entry["language"] == "python"


def test_negative_5_missing_required_instructional_plan_fields_fail_validation_without_from_legacy_fallback(tmp_path):
    """Negative test 5: Missing required fields in a new instructional plan fail validation rather than silently calling from_legacy()."""
    malformed_plans = [
        {"audience": "beginner", "source_policy": "independent", "concepts": []},
        {"audience": "beginner", "source_policy": "independent", "concepts": [{"id": "c1", "title": "Missing types and objectives"}]},
        {"audience": "beginner", "source_policy": "independent", "concepts": [{"id": "c1", "title": "Bad", "types": ["unknown_type"], "objectives": ["explain"], "reason": "x"}]},
        "not-a-dict",
    ]
    for bad_plan in malformed_plans:
        with pytest.raises(ValueError):
            build_plan(
                tmp_path,
                "/scribe-deepnotes Neural Networks",
                "Neural Networks",
                [{"title": "Forward Pass", "routing_reason": "Test validation.", "instructional_plan": bad_plan}],
            )


def test_negative_6_supporting_modules_do_not_activate_merely_because_dimension_depth_is_positive():
    """Negative test 6: Supporting modules do not activate merely because a dimension depth is positive."""
    raw = {
        "audience": "intermediate",
        "source_policy": "independent",
        "concepts": [
            {
                "id": "pure-calc",
                "title": "Evaluate a Definite Integral",
                "types": ["mathematical"],
                "objectives": ["calculate"],
                "depth": {
                    "math": 3,
                    "visual": 4,   # Positive visual depth WITHOUT visualizations list or architectural type
                    "code": 1,     # Positive code depth C1 (pseudocode) WITHOUT programming type or implement objective
                    "theory": 1,   # Positive theory depth T1 WITHOUT explain/analyze objective
                },
                "prerequisites": [],
                "reason": "Test selective supporting module activation.",
            }
        ],
    }
    plan = normalize_plan(raw)
    mods = plan["concepts"][0]["modules"]
    # Visualization is supporting=True in registry, and depth['visual']==4, but no visualizations or architectural type were selected!
    assert mods["visualization"]["status"] == "excluded"
    # Coding is supporting=True in registry, and depth['code']==1, but code<2 and no programming/implement selected!
    assert mods["coding"]["status"] == "excluded"
    # Motivation has no explain/foundation prereqs and 'need' is not in mathematical subtemplate
    assert mods["motivation"]["status"] == "excluded"
    # Limitations requires theory >= 3 for supporting activation
    assert mods["limitations"]["status"] == "excluded"


def test_negative_7_scaffolds_and_published_notes_do_not_contain_legacy_matrix_references():
    """Negative test 7: Scaffolds and published notes do not contain legacy decision-matrix references."""
    for route in note_layout.ROUTES:
        skeleton = note_layout.body_skeleton(route, 0, "01", "Sample Title", narrow=False)
        assert "notes_decision_matrix.md" not in skeleton
        assert "note_decision_matrix.md" not in skeleton
        assert "<!-- decision-contract:" not in skeleton

    leaked_note = (
        "---\nid: leak-01\naliases: [Leak]\ntopic: Test\ntags: [test]\nnexttopics: []\n---\n\n"
        "# 01. Leak\n\nSee shared/notes_decision_matrix.md for DM-07.\n"
    )
    findings = validate_text(leaked_note, route="deepstudy-master")
    assert any("decision-matrix" in msg for _, msg in findings)


def test_negative_8_active_skill_instructions_do_not_point_to_d01_d15_or_dm01_dm20():
    """Negative test 8: Active skill instructions do not point to D01–D15 or DM-01–DM-20."""
    active_files = [
        ROOT / "SKILL.md",
        ROOT / "router.md",
        ROOT / "README.md",
        ROOT / "shared/authoring_rules.md",
        ROOT / "shared/math_gates.md",
        ROOT / "shared/footer_widgets.md",
        *sorted((ROOT / "references/routing").glob("*.md")),
        *sorted((ROOT / "references/workflows").rglob("*.md")),
        *sorted((ROOT / "references/templates").rglob("*.md")),
        *sorted((ROOT / "skills").glob("*/SKILL.md")),
    ]
    retired_files = [
        ROOT / "shared/note_decision_matrix.md",
        ROOT / "shared/notes_decision_matrix.md",
        ROOT / "templates/notes_decision_matrix.md",
        ROOT / "templates",
    ]
    for retired in retired_files:
        assert not retired.exists(), f"Retired legacy matrix file still exists: {retired}"

    forbidden_re = re.compile(r"\b(?:D0[1-9]|D1[0-5]|DM-0[0-9]|DM-1[0-9]|DM-20)\b|notes?_decision_matrix\.md")
    for path in active_files:
        text = path.read_text(encoding="utf-8")
        match = forbidden_re.search(text)
        assert match is None, f"Active instruction file {path.relative_to(ROOT)} still references legacy matrix token: {match.group(0)}"
