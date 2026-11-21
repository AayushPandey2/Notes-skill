"""Forward regressions for explicit full-topic and narrow requests."""
import json
from pathlib import Path
import subprocess
import sys

import pytest

from scriptorium import OrchestrationEngine


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("request_text", [
    "comprehensive Kirchhoff circuit notes with units and examples",
    "comprehensive French Revolution notes with causal explanations",
    "full notes on medieval manuscript transmission",
    "complete notes about braided river formation",
    "comprehensive notes on an unfamiliar invented subject",
])
def test_explicit_comprehensive_scope_does_not_depend_on_subject_vocabulary(request_text):
    engine = OrchestrationEngine(ROOT)
    state = engine.start_notes_session(request_text)
    assert state.recommendation.recommended_master == "M1"
    assert state.recommendation.recommended_organization == "hierarchical_collection"
    assert state.recommendation.recommended_depth == "comprehensive"
    result = engine.respond_to_session(state, "use your recommendations")
    assert result["state"].resolved_preferences.organization == "hierarchical_collection"
    assert result["state"].collection_plan.organization == "hierarchical_collection"
    assert result["stage"] == "AWAITING_PLAN_APPROVAL"


@pytest.mark.parametrize("request_text", [
    "comprehensive Kirchhoff circuit notes in a single note",
    "comprehensive French Revolution notes all in one",
    "one full note on medieval manuscript transmission",
    "complete notes about braided river formation in one file",
    "comprehensive notes explaining a single concept",
    "concise notes about Machine Learning",
    "narrow notes about operating systems",
])
def test_explicit_single_or_narrow_scope_wins_over_depth_and_broad_topics(request_text):
    engine = OrchestrationEngine(ROOT)
    state = engine.start_notes_session(request_text)
    assert state.recommendation.recommended_organization == "single_note"
    result = engine.respond_to_session(state, "use your recommendations")
    assert result["state"].collection_plan.organization == "single_note"
    assert result["stage"] == "COLLECTION_PLAN_READY"


def test_quick_reminder_uses_shared_quick_reference_route_and_single_note():
    engine = OrchestrationEngine(ROOT)
    assert engine.route("quick binary search reminder")["master"] == "M3"
    state = engine.start_notes_session("quick binary search reminder")
    assert state.recommendation.recommended_master == "M3"
    assert state.recommendation.recommended_depth == "concise"
    assert state.recommendation.recommended_organization == "single_note"
    result = engine.respond_to_session(state, "use your recommendations")
    assert result["state"].resolved_preferences.master == "M3"
    assert result["state"].collection_plan.organization == "single_note"


@pytest.mark.parametrize("request_text,master", [
    ("comprehensive structured study notes on parliament", "M2"),
    ("comprehensive formula sheet for mechanics", "M3"),
    ("comprehensive worked solutions for these equations", "M4"),
    ("comprehensive implementation guide for a parser", "M5"),
    ("comprehensive flashcards for cellular respiration", "M6"),
    ("comprehensive comparison of markets vs planned economies", "M7"),
])
def test_full_scope_detection_preserves_explicit_other_master_styles(request_text, master):
    state = OrchestrationEngine(ROOT).start_notes_session(request_text)
    assert state.recommendation.recommended_master == master
    assert state.recommendation.recommended_organization == "single_note"


def test_explicit_multi_note_preference_and_source_only_policy_survive_defaults():
    engine = OrchestrationEngine(ROOT)
    state = engine.start_notes_session("comprehensive notes about medieval law using only my source, multiple linked notes")
    result = engine.respond_to_session(state, "use your recommendations")
    preferences = result["state"].resolved_preferences
    assert preferences.organization == "hierarchical_collection"
    assert preferences.source_policy == "strict"


@pytest.mark.parametrize("request_text,master,organization", [
    ("comprehensive Kirchhoff circuit notes with units and examples", "M1", "hierarchical_collection"),
    ("comprehensive French Revolution notes with causal explanations", "M1", "hierarchical_collection"),
    ("quick binary search reminder", "M3", "single_note"),
])
def test_actual_cli_notes_start_keeps_the_chosen_profile(tmp_path, request_text, master, organization):
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "scribe.py"), "notes", "start", request_text,
         "--vault", str(tmp_path), "--json"],
        capture_output=True, text=True, encoding="utf-8", cwd=ROOT,
    )
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    recommendation = output["state"]["recommendation"]
    assert recommendation["recommended_master"] == master
    assert recommendation["recommended_organization"] == organization
    saved = Path(output["saved_path"])
    assert saved.is_file() and saved.is_relative_to(tmp_path)
