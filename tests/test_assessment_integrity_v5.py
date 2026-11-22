"""Behavioral regressions for assessment ownership and calibrated claim evidence."""
from copy import deepcopy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from test_comprehensive_composition import specification, inputs
from scriptorium.engines.composition import build_composition
from scriptorium.engines.composition.checks import check_claim
from scriptorium.engines.composition.contracts import (
    _verify_obligation, check_assessment, insert_at_section, render_question,
)


@pytest.mark.parametrize("kind", ["algorithmic", "historical", "causal", "experimental_design"])
def test_domain_appropriate_task_kinds_support_final_assessment(kind):
    spec = specification()
    spec["assessments"][0]["type"] = kind
    plan = build_composition(spec)
    drafts, _, _ = inputs(plan)
    assert not check_assessment(plan, plan["chapters"][0], drafts["ch1"])


@pytest.mark.parametrize("fault", ["chapter", "unknown_objective", "foreign_objective", "global_duplicate"])
def test_questions_cannot_silently_escape_canonical_ownership(fault):
    spec = specification()
    question = deepcopy(spec["assessments"][0])
    question["id"] = "extra-check"
    if fault == "chapter":
        question["chapter"] = "unplanned-chapter"
    elif fault == "unknown_objective":
        question["objectives"] = ["missing:objective:0"]
    elif fault == "foreign_objective":
        question["objectives"] = ["c2:objective:0"]
    else:
        question["id"] = spec["assessments"][4]["id"]
    spec["assessments"].append(question)
    with pytest.raises(ValueError, match="chapter|objective|globally unique"):
        build_composition(spec)


def test_milestone_check_must_stay_in_its_declared_section():
    spec = specification()
    question = {**deepcopy(spec["assessments"][0]), "id": "milestone-check", "placement": "Concept 1"}
    spec["assessments"].append(question)
    plan = build_composition(spec)
    drafts, _, _ = inputs(plan)
    body = drafts["ch1"]
    assert not check_assessment(plan, plan["chapters"][0], body)
    # Presence elsewhere in the same chapter does not fulfill milestone placement.
    rendered = render_question(question)
    moved = body.replace(rendered, "") + "\n\n" + rendered
    assert any("milestone" in issue for issue in check_assessment(plan, plan["chapters"][0], moved))
    assert rendered.count("> [!hint]-") == rendered.count("> [!answer]-") == 1


def test_fenced_example_heading_cannot_receive_a_live_question():
    body = "# Chapter\n\n```markdown\n## Fake milestone\nExample only.\n```\n\n## Real milestone\nTeaching.\n"
    with pytest.raises(ValueError, match="placement heading"):
        insert_at_section(body, "Fake milestone", "A live section check.")
    updated = insert_at_section(body, "Real milestone", "A live section check.")
    assert updated.index("A live section check.") > updated.index("## Real milestone")


def test_ambiguous_milestone_does_not_select_an_arbitrary_section():
    with pytest.raises(ValueError, match="ambiguous"):
        insert_at_section("## Check\nFirst.\n\n## Check\nSecond.\n", "Check", "Question.")


def test_rendered_hint_and_solution_require_text():
    question = specification()["assessments"][0]
    question["hint"] = ["Malformed hint"]
    with pytest.raises(ValueError, match="nonempty text"):
        render_question(question)


def claim_record():
    return {"id": "claim-1", "text": "A bounded source observation.", "classification": "reported_source_claim",
            "origin": "reported", "source": {"id": "supplied-source", "version": "v1", "location": "section 2",
                "verification_method": "source inspection", "status": "verified", "limits": "the reported setting",
                "snapshot": "source.txt", "excerpt": "A bounded source observation.", "origin": "supplied"}}


@pytest.mark.parametrize("location", ["claim", "source"])
def test_unresolved_contradiction_prevents_verified_claim(location):
    claim = claim_record()
    assert not check_claim(claim, source_policy="strict")
    target = claim if location == "claim" else claim["source"]
    target["contradictions"] = ["Another supplied source reports incompatible assumptions."]
    assert any("contradictory" in issue for issue in check_claim(claim, source_policy="strict"))


def empirical_claim():
    claim = claim_record()
    claim["classification"] = "empirical_observation"
    claim["empirical"] = {"dataset": "fixture", "model": "fixture", "adaptation": "none", "metric": "response",
                          "protocol": "two repeated observations", "hyperparameters": {}, "model_selection": "none",
                          "runs": 2, "uncertainty": {"type": "SD", "value": 0.2}, "compute": "not_reported",
                          "location": "table 1", "value": 3.0, "units": "seconds"}
    return claim


@pytest.mark.parametrize("field,value", [("value", float("nan")), ("value", float("inf")),
                                         ("value", True), ("uncertainty", float("nan")),
                                         ("uncertainty", float("inf")), ("uncertainty", -0.1)])
def test_nonfinite_or_invalid_measurement_cannot_pass_claim_gate(field, value):
    claim = empirical_claim()
    assert not check_claim(claim, source_policy="strict")
    if field == "value":
        claim["empirical"]["value"] = value
    else:
        claim["empirical"]["uncertainty"]["value"] = value
    assert any("finite" in issue for issue in check_claim(claim, source_policy="strict"))


def test_claim_scope_preserves_strict_source_restriction():
    claim = claim_record()
    claim["source"]["origin"] = "external"
    assert any("source-only" in issue for issue in check_claim(claim, source_policy="strict"))
    assert not check_claim(claim, source_policy="adaptive")


def test_visual_verifier_binds_exact_native_or_remote_markup(tmp_path):
    embed = "```mermaid\nflowchart LR\nA --> B\n```"
    obligation = {"id": "visual-1", "owner": "chapter-1", "verifier": "visual", "record": {}}
    result = {"status": "verified", "attempted": True, "hash": "test-receipt", "path": "assets/flow.mmd", "embed": embed}
    assert not _verify_obligation(obligation, {}, {"chapter-1": embed}, {}, {"visual-1": result}, tmp_path)
    assert _verify_obligation(obligation, {}, {"chapter-1": "Diagram omitted."}, {}, {"visual-1": result}, tmp_path)
    result["embed"] = ""
    assert _verify_obligation(obligation, {}, {"chapter-1": "Teaching."}, {}, {"visual-1": result}, tmp_path)
