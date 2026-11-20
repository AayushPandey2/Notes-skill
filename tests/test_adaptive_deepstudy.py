"""Adaptive authoring contracts, compatibility, and meaningful route regressions."""

import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from scriptorium import layout as note_layout
import plan_notes
from validate_note import validate_text


def note(body, tags=None, topic="Template QA"):
    metadata = {"id": "adaptive-check", "aliases": ["Adaptive check"], "topic": topic,
                "tags": tags or ["deepstudy-master"], "nexttopics": []}
    return "---\n" + yaml.safe_dump(metadata, sort_keys=False) + "---\n\n# Adaptive check\n\n" + body


def test_master_gates_and_engine_links_resolve():
    master = (ROOT / "references/templates/masters/deep-notes.md").read_text(encoding="utf-8")
    engine = (ROOT / "references/workflows/notes-creation/adaptive-engine.md").read_text(encoding="utf-8")
    assert "../../workflows/notes-creation/adaptive-engine.md" in master
    assert "../../workflows/notes-creation/instructional-registry.json" in master
    assert "Authoring gate" not in master
    assert "notes_decision_matrix.md" not in master
    assert "note_decision_matrix.md" not in master
    assert "instructional-registry.json" in engine
    for target in re.findall(r"\]\(([^)]+)\)", master):
        if target.startswith("https://"):
            continue
        name, _, anchor = target.partition("#")
        path = (ROOT / "references/templates/masters" / name).resolve()
        assert path.is_file(), target
        if anchor:
            headings = re.findall(r"^#+ (.+)$", path.read_text(encoding="utf-8"), re.M)
            assert anchor in {re.sub(r"[^\w -]", "", h).lower().replace(" ", "-") for h in headings}


@pytest.mark.parametrize("route", sorted(note_layout.DEEP_ROUTES))
@pytest.mark.parametrize("level", (0, 1, 2, 3))
def test_legacy_selectors_share_adaptive_scaffold(route, level):
    scaffold = note_layout.body_skeleton(route, level, "01", "Check", narrow=False)
    assert scaffold == note_layout.body_skeleton("deepstudy-master", level, "01", "Check", narrow=False)
    assert "references/workflows/notes-creation/adaptive-engine.md" in scaffold
    assert "notes_decision_matrix.md" not in scaffold
    assert "## " not in scaffold
    assert "dataviewjs" not in scaffold


@pytest.mark.parametrize("body,level", [
    ("## Definition\nA forward pass computes an output from inputs and fixed parameters.\n", 0),
    ("## Implementation\nIllustrative Python; expected output is 5. Not executed.\n\n"
     "```python\ndef affine(x):\n    return 2 * x + 1\nassert affine(2) == 5\n```\n", 0),
    ("## Worked trace\nLet $M$ denote storage in bytes for a $B$ by $d$ matrix with $s$ bytes per entry.\n\n"
     "$$\nM = B d s\n$$\n\nFor example, 2 rows, 3 columns and 4 bytes yield 24 bytes.\n\n"
     "## Implementation\nIllustrative NumPy; not executed.\n\n```python\nimport numpy as np\n"
     "output = np.zeros((2, 3), dtype=np.float32)\nassert output.nbytes == 24\n```\n", 1),
    ("## Theorem\nFor every positive real $x$, its reciprocal is positive.\n\n"
     "## Proof\nFor $x > 0$, division of the strict inequality by $x^2 > 0$ yields $1/x > 0$.\n\n"
     "## Counterexample\nWith $x = -1$, the reciprocal is negative.\n", 3),
])
def test_independent_concept_code_hybrid_and_proof_routes(body, level):
    content = note(body, topic="Real Analysis" if level == 3 else "Template QA")
    assert not validate_text(content, route="deepstudy-master", math_level=level)
    assert not validate_text(content)  # Batch validation recognizes the route tag.


def test_adaptive_notes_still_reject_residue_empty_sections_and_broken_links(tmp_path):
    for body, expected in [
        ("<!-- scaffold: unfinished -->", "Unresolved scaffold"),
        ("## Unused\n\n## Definition\nAn actual explanation.\n", "Empty section"),
        ("An explanation.\n\n> [!note] Authoring gate\n> **Decision-matrix IDs:** DM-01", "Remove authoring"),
        ("An explanation with $unclosed math", "Unclosed inline math"),
    ]:
        assert any(expected in message for _, message in validate_text(note(body)))
    assert any("Unresolved wikilink" in message for _, message in validate_text(
        note("An explanation linking [[Missing]]."), vault=tmp_path, target=tmp_path / "check.md"))


def test_code_only_subsection_and_state_diagram_are_not_forced_into_flowchart():
    body = "An event changes the state.\n\n## Visual\n```mermaid\nstateDiagram-v2\nIdle --> Busy: request\n```\n"
    body += "\n## Implementation\n```python\nstate = 'Busy'\n```\n\n## Limits\nNo concurrency is modeled.\n"
    assert not validate_text(note(body))


def test_planner_preserves_independent_record_and_does_not_invent_frameworks(tmp_path):
    record = {"reader": "familiar/intermediate", "track": "hybrid", "scope": "atomic mechanism",
              "outcome": "verify", "research_need": "current documentation check",
              "math": "proof-level", "code_depth": "standard library/framework"}
    item = {"title": "Check", "purpose": "implement", "impl_weight": "high", "density": "cohesive",
            "math_level": 3, "routing_reason": "Verify the selected behavior.", "decision_record": record}
    plan = plan_notes.build_plan(tmp_path, "/scribe-deepnotes Check", ".", [item])
    entry = plan["plan"][0]
    assert entry["template"] == "deepstudy-master"
    assert entry["decision_record"] == record
    assert entry["verification_stack"] == ["python"]
    assert entry["math_level"] == 3
    assert "clamped_from" not in entry
    assert entry["decision_contract"]["contract_version"] == 2
    for alias in note_layout.DEEP_ROUTES:
        routed = plan_notes.build_plan(tmp_path, "Study Check", ".", [{**item, "template": alias}])
        assert routed["plan"][0]["template"] == "deepstudy-master"
    # A specific requested tool is preserved; code depth does not dictate math depth.
    routed = plan_notes.build_plan(tmp_path, "Study Check", ".", [{**item, "math_level": 0,
                                 "language": "rust", "verification_stack": ["Rust"]}])
    assert routed["plan"][0]["verification_stack"] == ["Rust"]


def test_synthesized_practice_supports_proof_level_parent_without_changing_its_route(tmp_path):
    item = {"title": "Check", "purpose": "explain", "impl_weight": "low", "density": "cohesive",
            "math_level": 3, "routing_reason": "Establish the stated guarantee."}
    plan = plan_notes.build_plan(tmp_path, "Study Real Analysis", "Real Analysis", [item])["plan"]
    assert plan[0]["math_level"] == 3
    assert plan[1]["template"] == "practice"
    assert plan[1]["math_level"] == 2  # Existing practice semantics include derivation/proof here.
