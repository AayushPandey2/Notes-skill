from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import decision_matrix as dm
import plan_notes
from validate_note import validate_text


def _physics_note(body: str, *, tags: list[str] | None = None) -> str:
    tag_list = tags or ["physics", "wave-optics", "deepstudy-master"]
    return (
        "---\n"
        'id: "wave-optics-01"\n'
        "aliases:\n"
        '  - "Huygens Principle"\n'
        'topic: "Wave Optics"\n'
        "tags:\n"
        + "".join(f'  - "{t}"\n' for t in tag_list)
        + "nexttopics: []\n"
        "---\n\n"
        "# 01. Huygens Principle\n\n"
        f"{body}\n"
    )


def test_non_computing_subjects_lock_code_depth_to_none_unless_explicit(tmp_path: Path) -> None:
    for topic, title in [
        ("Wave Optics", "Huygens' Principle"),
        ("Thermodynamics", "Carnot Cycle"),
        ("Organic Chemistry", "Nucleophilic Substitution"),
        ("World History", "Industrial Revolution"),
    ]:
        contract = dm.resolve_decisions(f"/scribe-deepnotes {topic}", {"title": title, "math_level": 2}, topic)
        assert contract["subject_family"] == "non-computing"
        assert contract["code_depth"] == "none"
        assert contract["language"] == "none"
        assert "code_verification" in contract["omitted_sections"]

        plan = plan_notes.build_plan(
            tmp_path,
            f"/scribe-deepnotes {topic}",
            topic,
            [{"title": title, "purpose": "explain", "impl_weight": "low", "density": "cohesive",
              "math_level": 2, "routing_reason": "First-principles physics/domain note."}],
        )
        assert plan["plan"][0]["language"] == "none"
        assert plan["plan"][0]["decision_contract"]["code_depth"] == "none"

        with pytest.raises(ValueError, match="prohibits code"):
            plan_notes.build_plan(
                tmp_path,
                f"/scribe-deepnotes {topic}",
                topic,
                [{"title": title, "purpose": "implement", "impl_weight": "high", "density": "cohesive",
                  "math_level": 2, "language": "python", "routing_reason": "Unrequested code."}],
            )

    # Explicit user request for numerical simulation permits code
    sim_contract = dm.resolve_decisions(
        "/scribe-deepnotes Write a Python FDTD simulation for Wave Optics",
        {"title": "FDTD Wave Simulation", "math_level": 2, "language": "python"},
        "Wave Optics",
    )
    assert sim_contract["subject_family"] == "computational-science"
    assert sim_contract["code_depth"] != "none"
    assert sim_contract["language"] == "python"


def test_validate_text_rejects_unrequested_physics_code_jargon_legacy_comments_and_bare_urls() -> None:
    bad_code = _physics_note("## Mechanism\nWavefronts propagate.\n\n```python\nimport numpy as np\n```\n")
    assert any("DM-14 violation" in msg for _, msg in validate_text(bad_code))

    bad_legacy = _physics_note("<!-- SECTION: S1-SYNTHESIS -->\n## Core Model\nWavefronts propagate.\n")
    assert any("Legacy <!-- SECTION:" in msg for _, msg in validate_text(bad_legacy))

    bad_jargon = _physics_note("## Core Model\n### Core Problem & Computational Purpose\nWavefronts propagate.\n")
    assert any("DM-00 violation" in msg for _, msg in validate_text(bad_jargon))

    bad_mermaid = _physics_note("## Geometry\n```mermaid\nflowchart TD\nA --> B\n```\n")
    assert any("DM-13 violation" in msg for _, msg in validate_text(bad_mermaid))

    bad_url = _physics_note("## Sources\n| Source | Link |\n|---|---|\n| Fresnel | [BnF](https://gallica.bnf.fr/) |\n")
    assert any("DM-18 violation" in msg for _, msg in validate_text(bad_url))

    bad_qa = _physics_note(
        "## Q&A\n"
        "#### Question 1\nA\n"
        "#### Question 2\nB\n"
        "#### Question 3\nC\n"
        "#### Question 4\nD\n"
    )
    assert any("DM-20 violation" in msg for _, msg in validate_text(bad_qa))

    clean_physics = _physics_note(
        "## Core Model\nEvery point on a wavefront emits secondary wavelets.\n\n"
        "```text\nA --- C (interface)\n \\   /\n  B / E\n```\n\n"
        "## Sources\n[OpenStax Ch 1.6](https://openstax.org/books/university-physics-volume-3/pages/1-6-huygenss-principle)\n"
    )
    assert validate_text(clean_physics) == []


def test_decision_matrix_cli_resolve_and_audit(tmp_path: Path) -> None:
    p_res = subprocess.run(
        [sys.executable, "-B", str(SCRIPTS_DIR / "decision_matrix.py"), "resolve",
         "--request", "/scribe-deepnotes Wave Optics", "--topic", "Wave Optics", "--title", "Huygens Principle"],
        capture_output=True, text=True, check=True,
    )
    contract = json.loads(p_res.stdout)
    assert contract["code_depth"] == "none"
    assert contract["visual_modality"] == "diagram-image"

    ml_contract = dm.resolve_decisions(
        "/scribe-deepnotes Perceptron",
        {"title": "Implementations", "purpose": "implement", "impl_weight": "high", "math_level": 1, "language": "python"},
        "Perceptron",
    )
    assert ml_contract["implementation_stack"] == ["python-numpy", "scikit-learn", "pytorch"]

    note_file = tmp_path / "01 - Huygens.md"
    note_file.write_text(_physics_note("## Mechanism\n```python\nx = 1\n```\n"), encoding="utf-8")
    p_aud = subprocess.run(
        [sys.executable, "-B", str(SCRIPTS_DIR / "decision_matrix.py"), "audit", str(note_file), "--topic", "Wave Optics", "--format", "json"],
        capture_output=True, text=True, check=False,
    )
    assert p_aud.returncode == 1
    assert json.loads(p_aud.stdout)["errors"] >= 1


def test_pillar_gates_yaml_slug_hygiene_exec_claims_and_verify_vault(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    (vault / "Wave Optics").mkdir(parents=True)

    # Clean 5-key YAML WITHOUT deepstudy-master tag passes when route is deepstudy-master
    clean = _physics_note(
        "## Core Model\nEvery point on a wavefront emits secondary wavelets.\n\n"
        "See [[02 - Interference]] for superposition.\n",
        tags=["physics", "wave-optics"],
    ).replace("nexttopics: []", 'nexttopics:\n  - "[[02 - Interference]]"')
    note_path = vault / "Wave Optics" / "01 - Huygens Principle.md"
    note_path.write_text(clean, encoding="utf-8")
    assert validate_text(
        clean,
        vault=vault,
        target=note_path,
        planned=[vault / "Wave Optics" / "02 - Interference.md"],
        route="deepstudy-master",
        math_level=0,
    ) == []

    # Mixed slug style (02-hyphenated-slug alongside 01 - Title) fails
    mixed_slug = _physics_note("## Core Model\nSee [[02-interference-and-slit]] next.\n", tags=["physics"])
    assert any("Mixed filename slug style" in msg for _, msg in validate_text(mixed_slug, vault=vault, target=note_path, route="deepstudy-master"))

    # Forward wikilink missing from disk AND missing from nexttopics fails
    unindexed_fwd = _physics_note("## Core Model\nSee [[02 - Interference]] next.\n", tags=["physics"])
    assert any("nexttopics" in msg for _, msg in validate_text(unindexed_fwd, vault=vault, target=note_path, route="deepstudy-master"))

    # Execution claim without code fails DM-18
    fake_exec = _physics_note("## Verification\nObserved Execution Output: all assertions passed via NumPy 2.5.5.\n")
    assert any("DM-18 violation" in msg for _, msg in validate_text(fake_exec, route="deepstudy-master"))

    # Legacy YAML keys (title, base_domain, master_topic) fail validation
    legacy_yaml = (
        "---\nid: x\ntitle: X\naliases: [X]\nbase_domain: Physics\nmaster_topic: Optics\n"
        "topic: Wave Optics\ntags: [physics]\nnexttopics: []\n---\n\n# X\n\nBody.\n"
    )
    assert any("Unauthorized frontmatter key" in msg for _, msg in validate_text(legacy_yaml, route="deepstudy-master"))

    # verify_vault_notes.py catches legacy SECTION markers, bare root URLs, and mixed slugs on disk
    bad_file = vault / "Wave Optics" / "01 - Bad Note.md"
    bad_file.write_text(
        _physics_note(
            "<!-- SECTION: S1-SYNTHESIS -->\n## Core Model\nSee [[02-hyphenated-slug]].\n"
            "[Fresnel](https://gallica.bnf.fr/)\n",
            tags=["physics"],
        ),
        encoding="utf-8",
    )
    p = subprocess.run(
        [sys.executable, "-B", str(SCRIPTS_DIR / "verify_vault_notes.py"), str(vault), "--files", "Wave Optics/01 - Bad Note.md"],
        capture_output=True, text=True, check=False,
    )
    assert p.returncode == 1
    assert "ROUTED_NOTE_INVALID" in p.stdout or "DECISION_MATRIX_VIOLATION" in p.stdout
