"""Behavioral tests for the replacement Writer and its teaching gates."""
import pytest

from scriptorium.engines.pedagogy import build_explanation_blueprint, compose_explanation_note
from scriptorium.engines.composition import writing
from scriptorium.engines.mathematics import render_formula_component


def test_public_writer_is_replacement_and_records_executed_stages():
    assert compose_explanation_note is writing.compose_explanation_note
    blueprint = build_explanation_blueprint("A supplied concept", source_mode="strict",
                                            preserve_source_order=True)
    note = compose_explanation_note(blueprint, source_facts=["The first supplied statement.",
                                                            "The second supplied statement."])
    assert note.index("first supplied") < note.index("second supplied")
    assert "Applicability Conditions" not in note
    assert "Reconstructing the Reasoning" not in note
    trace = blueprint.context["composition_result"]["trace"]
    assert [entry["component"] for entry in trace] == [
        "composition.writing.plan_depth", "composition.writing.teach",
        "composition.writing.write", "composition.writing.validate"]


def test_depth_obligations_block_explicit_complete_output_with_missing_example():
    blueprint = build_explanation_blueprint("A concept", context={"require_complete": True})
    with pytest.raises(ValueError, match="example"):
        compose_explanation_note(blueprint)
    assert not blueprint.context["composition_result"]["validation"]["complete"]


def test_display_formula_in_source_cannot_bypass_mathematical_gate():
    blueprint = build_explanation_blueprint("Calculation", source_mode="strict", preserve_source_order=True)
    with pytest.raises(ValueError, match="Formula teaching gate failed"):
        compose_explanation_note(blueprint, source_facts=["The calculation is shown below.\n\n$$y = 2x$$"])


def test_visual_inspection_is_required_before_composition():
    blueprint = build_explanation_blueprint("Visual concept", context={"assets": [{"path": "figure.png"}]})
    with pytest.raises(ValueError, match="inspection record"):
        compose_explanation_note(blueprint)


def test_formula_stage_coverage_does_not_claim_missing_stages():
    result = render_formula_component({"equation": "y = 2x", "purpose": "Calculate output from input.",
                                       "symbols": [{"symbol": "x", "meaning": "input quantity"},
                                                   {"symbol": "y", "meaning": "output quantity"}]})
    assert len(result["stage_status"]) == 12
    assert result["stage_status"]["1"] == "supplied"
    assert result["stage_status"]["6"] == "not_supplied"
    assert result["record"].validation_status == "structurally_checked"


def test_formula_stages_reject_nested_display_math():
    with pytest.raises(ValueError, match="nested display"):
        render_formula_component({"equation": "y = x", "purpose": "An identity.",
                                  "derivation_reasoning": "$$x = x$$"})


def test_inspection_of_another_image_cannot_ground_the_writer():
    blueprint = build_explanation_blueprint("Visual concept", context={
        "assets": [{"path": "figure.png", "hash": "image-one"}],
        "inspections": [{"inspection_performed": True, "content_hash": "image-two"}],
    })
    with pytest.raises(ValueError, match="exact acquired asset hash"):
        compose_explanation_note(blueprint)


def test_derivation_objective_cannot_be_satisfied_by_headings_alone():
    blueprint = build_explanation_blueprint("A rule", context={
        "objectives": ["Derive the governing relation"], "require_complete": True,
    })
    with pytest.raises(ValueError, match="mathematical_reasoning"):
        compose_explanation_note(blueprint)
