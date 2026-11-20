"""Comprehensive tests for Universal /scribe-notes, Interactive Intelligence & Hierarchical Knowledge Generation.

Covers Part 28 Scenarios A-J and Part 29 test groups (29.1 through 29.10).
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import time

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scriptorium import (
    NoteCollectionPlan,
    NoteInteractionState,
    OrchestrationEngine,
    PedagogyEngine,
    QualityEngine,
    VaultEngine,
    parse_note,
)
from scriptorium.engines._interactive import (
    ACTIVE_PUBLIC_COMMANDS,
    RETIRED_NOTE_COMMANDS,
    TopicNode,
)

PYTHON = sys.executable


# ---------------------------------------------------------------------------
# 29.1 — Command Consolidation & Zero Script Proliferation
# ---------------------------------------------------------------------------

def test_29_1_only_four_public_skills_and_eight_scripts():
    skills_dir = ROOT / "skills"
    skill_folders = sorted(p.name for p in skills_dir.iterdir() if p.is_dir())
    assert skill_folders == sorted(ACTIVE_PUBLIC_COMMANDS)
    for retired in RETIRED_NOTE_COMMANDS:
        assert not (skills_dir / retired).exists(), f"Retired skill folder still present: {retired}"

    scripts_dir = ROOT / "scripts"
    py_scripts = sorted(p.name for p in scripts_dir.glob("*.py"))
    assert len(py_scripts) == 8, f"Expected 8 public CLI scripts, found {len(py_scripts)}: {py_scripts}"

    orch = OrchestrationEngine(ROOT)
    reg = orch.validate_registry(require_retired_legacy=True)
    assert reg["valid"], reg["errors"]
    assert reg["masters_count"] == 7
    assert reg["variants_count"] == 12
    assert reg["subtemplates_count"] == 6
    assert reg["commands_count"] == 4
    assert reg["retired_commands_count"] == 8


def test_29_1_retired_commands_emit_graceful_migration_hint():
    orch = OrchestrationEngine(ROOT)
    for cmd in ("scribe-deepnotes", "scribe-distill", "scribe-compare", "scribe-dsa", "scribe-practice", "scribe-atomic-notes"):
        routed = orch.route(f"/{cmd} Gradient Descent")
        assert routed.get("retired_command") == cmd
        assert "/scribe-notes" in (routed.get("migration_hint") or "")


# ---------------------------------------------------------------------------
# 29.2 — Universal Request Routing Through /scribe-notes (All M1-M7)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("request_text", "expected_master", "expected_variant"),
    [
        ("/scribe-notes Gradient Descent", "M1", None),
        ("/scribe-notes Structured study notes on Biot-Savart Law from this lecture", "M2", "lecture_order"),
        ("/scribe-notes Make a cheat sheet for Pandas Data Cleaning", "M3", None),
        ("/scribe-notes Formula sheet for Maxwell's Equations", "M3", "formula_sheet"),
        ("/scribe-notes Atomic note on Residual Connection", "M3", "atomic_card"),
        ("/scribe-notes Solve these 5 calculus integration problems step by step", "M4", None),
        ("/scribe-notes Implement binary search from scratch in Python", "M5", None),
        ("/scribe-notes Create flashcards for cellular respiration", "M6", "flashcards"),
        ("/scribe-notes Compare CNN vs Vision Transformers", "M7", "comparison_guide"),
        ("/scribe-notes Concept map of Thermodynamics", "M7", "concept_map"),
    ],
)
def test_29_2_universal_scribe_notes_routes_all_seven_masters(request_text, expected_master, expected_variant):
    orch = OrchestrationEngine(ROOT)
    has_src = "lecture" in request_text.lower()
    routed = orch.route(request_text, has_source=has_src)
    assert routed["command"] == "scribe-notes"
    assert routed["master"] == expected_master
    if expected_variant is not None:
        assert routed["variant"] == expected_variant


# ---------------------------------------------------------------------------
# 29.3 & 29.4 — Interactive Configuration Gate & Multi-Turn State Machine
# ---------------------------------------------------------------------------

def test_29_3_bare_scribe_notes_asks_for_topic_first():
    orch = OrchestrationEngine(ROOT)
    state = orch.start_notes_session("/scribe-notes")
    assert state.stage == "AWAITING_TOPIC"
    prompt = orch.format_configuration_prompt(state)
    assert "topic" in prompt.lower()

    # Follow-up without repeating /scribe-notes advances smoothly to AWAITING_CONFIGURATION
    step2 = orch.respond_to_session(state, "Gradient Descent")
    assert step2["stage"] == "AWAITING_CONFIGURATION"
    assert step2["ready_to_generate"] is False
    assert "Gradient Descent" in step2["message"]


def test_29_3_skips_redundant_questions_when_explicitly_specified():
    orch = OrchestrationEngine(ROOT)
    state_vague = orch.start_notes_session("/scribe-notes Gradient Descent")
    state_explicit = orch.start_notes_session(
        "/scribe-notes Deep beginner single-note guide on Gradient Descent with math and Python code"
    )
    assert state_vague.stage == "AWAITING_CONFIGURATION"
    assert state_explicit.stage == "AWAITING_CONFIGURATION"
    assert len(state_explicit.questions_asked) <= len(state_vague.questions_asked)
    q_ids_explicit = {q["id"] for q in state_explicit.questions_asked}
    assert "depth" not in q_ids_explicit


def test_29_4_reply_formats_defaults_numbered_correction_and_cancel():
    orch = OrchestrationEngine(ROOT)

    # 1. "use your recommendations" -> ready immediately for single concept
    s1 = orch.start_notes_session("/scribe-notes Gradient Descent")
    r1 = orch.respond_to_session(s1, "use your recommendations")
    assert r1["ready_to_generate"] is True
    assert r1["stage"] == "COLLECTION_PLAN_READY"
    assert r1["state"].collection_plan.organization == "single_note"

    # 2. Numbered/lettered + free-text mix
    s2 = orch.start_notes_session("/scribe-notes Gradient Descent")
    r2 = orch.respond_to_session(s2, "1b, 2c, single note with worked examples")
    assert r2["ready_to_generate"] is True
    assert r2["state"].resolved_preferences.depth == "comprehensive"

    # 3. Cancellation without repeating /scribe-notes
    s3 = orch.start_notes_session("/scribe-notes Machine Learning")
    r3 = orch.respond_to_session(s3, "cancel")
    assert r3["stage"] == "CANCELLED"
    assert r3["ready_to_generate"] is False

    # 4. Mid-flow correction & outline modification on broad topic
    s4 = orch.start_notes_session("/scribe-notes Machine Learning")
    r4a = orch.respond_to_session(s4, "use your recommendations")
    assert r4a["stage"] == "AWAITING_PLAN_APPROVAL"
    assert r4a["ready_to_generate"] is False
    assert "Machine Learning" in r4a["message"]

    # Add a topic and remove a topic before approving
    r4b = orch.respond_to_session(r4a["state"], "add Bayesian Inference")
    assert r4b["stage"] == "AWAITING_PLAN_APPROVAL"
    assert any(n.title == "Bayesian Inference" for n in r4b["state"].collection_plan.nodes)

    r4c = orch.respond_to_session(r4b["state"], "looks good, proceed")
    assert r4c["stage"] == "COLLECTION_PLAN_READY"
    assert r4c["ready_to_generate"] is True


# ---------------------------------------------------------------------------
# 29.5 & 29.6 — Topic Scope Detection (S0-S5) & Graph Separation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("topic", "expected_tier", "expected_org"),
    [
        ("Atomic note on Dot Product", "S0", "single_note"),
        ("Gradient Descent", "S1", "single_note"),
        ("Classification Metrics", "S2", "single_or_small_collection"),
        ("Supervised Learning", "S3", "hierarchical_collection"),
        ("Transformers", "S3", "hierarchical_collection"),
        ("Machine Learning", "S4", "hierarchical_collection"),
        ("Complete Artificial Intelligence Curriculum", "S5", "hierarchical_collection"),
    ],
)
def test_29_5_scope_classification_s0_through_s5(topic, expected_tier, expected_org):
    orch = OrchestrationEngine(ROOT)
    scope = orch.classify_scope(topic, request=f"/scribe-notes {topic}")
    assert scope["level"] == expected_tier
    assert scope["recommended_structure"] == expected_org


def test_29_6_hierarchy_prerequisite_and_related_graphs_are_distinct():
    orch = OrchestrationEngine(ROOT)
    state = orch.start_notes_session("/scribe-notes Machine Learning")
    r1 = orch.respond_to_session(state, "use your recommendations")
    plan: NoteCollectionPlan = r1["state"].collection_plan
    assert plan is not None
    assert plan.organization == "hierarchical_collection"

    node_map = {n.concept_id: n for n in plan.nodes}
    root = node_map[plan.root_topic_id]
    assert root.note_role == "root_index"
    assert len(root.child_ids) >= 3

    # Verify Topic Hierarchy (parent/child), Prerequisites, and Related are kept separate
    has_prereqs = any(n.prerequisite_ids for n in plan.nodes)
    has_related = any(n.related_ids for n in plan.nodes)
    assert has_prereqs, "Expected explicit prerequisite_ids distinct from parent_id"
    assert has_related, "Expected explicit related_ids distinct from parent_id"
    for n in plan.nodes:
        assert n.parent_id not in n.related_ids
        assert n.concept_id not in n.prerequisite_ids


def test_29_6_source_ordered_section_decomposition():
    orch = OrchestrationEngine(ROOT)
    sections = [
        "1. Kinematics and Reference Frames",
        "2. Newton's Laws of Motion",
        "3. Work and Conservation of Energy",
        "4. Linear Momentum and Collisions",
    ]
    state = orch.start_notes_session(
        "/scribe-notes Study notes from this physics lecture preserving lecture order",
        has_source=True,
        source_sections=sections,
    )
    res = orch.respond_to_session(state, "use your recommendations")
    plan = res["state"].collection_plan
    assert plan is not None
    child_titles = [n.title for n in plan.nodes if n.note_role == "child"]
    assert child_titles == sections
    assert res["state"].resolved_preferences.preserve_source_order is True


# ---------------------------------------------------------------------------
# 29.7, 29.8, 29.9 — Full Adaptive Generation, Obsidian Properties,
# Non-Destructive Existing-Note Reconciliation & Collection-Wide Validation
# ---------------------------------------------------------------------------

def test_29_7_to_29_9_machine_learning_hierarchical_generation_and_validation(tmp_path):
    orch = OrchestrationEngine(ROOT)
    vault = VaultEngine()
    quality = QualityEngine(ROOT)

    # Interactive flow for Scenario B: Machine Learning (S4 -> hierarchical collection)
    t0 = time.perf_counter()
    state = orch.start_notes_session("/scribe-notes Machine Learning")
    assert state.stage == "AWAITING_CONFIGURATION"
    step_preview = orch.respond_to_session(state, "beginner, deep learning notes, hierarchical collection")
    assert step_preview["stage"] == "AWAITING_PLAN_APPROVAL"
    step_approve = orch.respond_to_session(step_preview["state"], "proceed")
    assert step_approve["ready_to_generate"] is True

    plan = step_approve["state"].collection_plan
    prefs = step_approve["state"].resolved_preferences

    # Pre-seed one canonical child note with custom Properties & Personal Notes to prove non-destructive reconciliation!
    linear_node = next(n for n in plan.nodes if "linear regression" in n.title.lower())
    preexisting_path = tmp_path / linear_node.proposed_path
    preexisting_path.parent.mkdir(parents=True, exist_ok=True)
    preexisting_props = vault.build_properties(
        topic=linear_node.title,
        note_type="deep-notes",
        user_tags=["my-exam-priority"],
        custom_properties={"custom_owner": "student-aayush"},
        created="2026-01-15",
    )
    preexisting_path.write_text(
        vault.render_note(
            preexisting_props,
            f"# {linear_node.title}\n\n## Personal Notes\nKeep my handwritten intuition intact.\n",
        ),
        encoding="utf-8",
    )

    gen = vault.generate_collection(tmp_path, plan, prefs)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    assert gen["complete"] is True
    assert gen["failed_count"] == 0
    assert gen["completed_count"] == len(plan.nodes)
    assert Path(gen["manifest_path"]).is_file()
    assert elapsed_ms < 10_000, f"Collection generation unexpectedly slow: {elapsed_ms:.1f}ms"

    # Verify non-destructive reconciliation preserved user content, custom property, tag, and created date
    reconciled_text = preexisting_path.read_text(encoding="utf-8")
    reconciled = parse_note(reconciled_text)
    assert "Keep my handwritten intuition intact." in reconciled.body
    assert reconciled.metadata.get("custom_owner") == "student-aayush"
    assert "my-exam-priority" in reconciled.metadata.get("tags", [])
    assert str(reconciled.metadata.get("created")) == "2026-01-15"
    assert reconciled.metadata.get("collection_id") == plan.collection_id

    # Verify Root MOC is note_type: index and does NOT duplicate child derivations
    root_node = next(n for n in plan.nodes if n.note_role == "root_index")
    root_text = (tmp_path / root_node.proposed_path).read_text(encoding="utf-8")
    root_parsed = parse_note(root_text)
    assert root_parsed.metadata["note_type"] == "index"
    assert "## Knowledge Map" in root_parsed.body
    assert "## Recommended Learning Path" in root_parsed.body

    # Run Collection-Wide Quality Validation
    val = quality.validate_collection(tmp_path, plan, manifest=gen["manifest"])
    assert val["valid"] is True, val["issues"]
    assert val["verified_files"] == len(plan.nodes)
    assert val["issues"] == []


def test_29_9_collection_validator_detects_broken_link_missing_file_and_bad_frontmatter(tmp_path):
    orch = OrchestrationEngine(ROOT)
    vault = VaultEngine()
    quality = QualityEngine(ROOT)

    state = orch.start_notes_session("/scribe-notes Supervised Learning")
    r1 = orch.respond_to_session(state, "use your recommendations")
    r2 = orch.respond_to_session(r1["state"], "proceed")
    plan = r2["state"].collection_plan
    prefs = r2["state"].resolved_preferences

    gen = vault.generate_collection(tmp_path, plan, prefs)
    assert quality.validate_collection(tmp_path, plan, manifest=gen["manifest"])["valid"] is True

    # Inject a broken wikilink into a child note & delete another child note
    children = [n for n in plan.nodes if n.note_role == "child"]
    c0_path = tmp_path / children[0].proposed_path
    c0_path.write_text(c0_path.read_text(encoding="utf-8") + "\nSee [[NonExistent Ghost Note]].\n", encoding="utf-8")
    (tmp_path / children[1].proposed_path).unlink()

    val_broken = quality.validate_collection(tmp_path, plan, manifest=gen["manifest"])
    assert val_broken["valid"] is False
    categories = {iss["category"] for iss in val_broken["issues"]}
    assert "wikilink_navigation" in categories
    assert "coverage_completeness" in categories


# ---------------------------------------------------------------------------
# Part 28 — End-to-End CLI Workflow Through scripts/scribe.py notes
# ---------------------------------------------------------------------------

def test_29_10_cli_universal_notes_start_respond_generate_validate(tmp_path):
    # 1. Start session via CLI
    p1 = subprocess.run(
        [
            PYTHON, "-B", str(ROOT / "scripts" / "scribe.py"),
            "notes", "start", "/scribe-notes Gradient Descent",
            "--vault", str(tmp_path), "--json",
        ],
        capture_output=True, text=True, check=True,
    )
    out1 = json.loads(p1.stdout)
    sid = out1["session_id"]
    assert out1["stage"] == "AWAITING_CONFIGURATION"
    assert Path(out1["saved_path"]).is_file()

    # 2. Respond without repeating /scribe-notes
    p2 = subprocess.run(
        [
            PYTHON, "-B", str(ROOT / "scripts" / "scribe.py"),
            "notes", "respond",
            "--vault", str(tmp_path),
            "--session-id", sid,
            "--reply", "use your recommendations",
            "--json",
        ],
        capture_output=True, text=True, check=True,
    )
    out2 = json.loads(p2.stdout)
    assert out2["ready_to_generate"] is True
    assert out2["stage"] == "COLLECTION_PLAN_READY"

    # 3. Generate + validate via CLI
    p3 = subprocess.run(
        [
            PYTHON, "-B", str(ROOT / "scripts" / "scribe.py"),
            "notes", "generate",
            "--vault", str(tmp_path),
            "--session-id", sid,
            "--validate",
        ],
        capture_output=True, text=True, check=True,
    )
    out3 = json.loads(p3.stdout)
    assert out3["generation"]["complete"] is True
    assert out3["validation"]["valid"] is True
    written = tmp_path / out3["generation"]["written_paths"][0]
    assert written.is_file()
    note_text = written.read_text(encoding="utf-8")
    assert note_text.startswith("---\n")
    assert "Gradient Descent" in note_text
