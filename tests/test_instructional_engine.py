"""Behavioral scenarios for per-concept planning, source gating and compatibility."""
from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from decision_matrix import resolve_decisions, audit_note_against_contract
from instructional_plan import normalize_plan, coverage_errors, registry
from plan_notes import build_plan, start_plan, publish
from note_verification import Block, required_examples, verify_runtimes

SCENARIOS = json.loads((ROOT / "examples/adaptive-deepnotes/scenarios.json").read_text(encoding="utf-8"))


def resolve(case):
    return resolve_decisions("/scribe-deepnotes " + case["topic"], case["item"], case["topic"])


@pytest.mark.parametrize("case", SCENARIOS, ids=lambda c: c["name"])
def test_scenarios_survive_the_actual_planner(tmp_path, case):
    plan = build_plan(tmp_path, "/scribe-deepnotes " + case["topic"], ".", [case["item"]])
    contract = plan["plan"][0]["decision_contract"]
    assert contract == resolve(case)
    assert contract["contract_version"] == 2
    assert normalize_plan(contract["instructional_plan"]) == contract["instructional_plan"]


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
    assert contract["instructional_plan"]["concepts"][0]["depth"]["math"] == 5
    assert contract["math_level"] == 3
    with pytest.raises(ValueError, match="conflicts"):
        resolve_decisions("Study this result", {"title": "Result", "purpose": "prove", "math_level": 0}, "General")


def test_saved_zero_math_profile_rejects_unplanned_equations():
    contract = {**resolve(SCENARIOS[0]), "explicit_contract": True}
    assert any("all-M0" in m for _, m in audit_note_against_contract("$$x = y + z$$", contract))
