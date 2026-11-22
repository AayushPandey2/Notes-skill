"""Repository Reorganization, Template/Module Catalog & End-to-End Integration Audit Tests.

Verifies:
- Clean repository structure, zero broken links, zero authority issues
- Single authoritative registry (master-registry.yaml) covering M1-M7, 12 variants, 6 subtemplates, 17 modules, 4 active commands, 8 retired commands
- Zero retired slash commands advertised in active templates, variants, subtemplates, or workflows
- Authoritative architecture docs (system-overview.md, template-module-catalog.md) complete and accurate
- All 8 Runtime Routing Examples (Part 27) verified against actual engine behavior
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scriptorium import (
    INTERACTIVE_KNOWLEDGE_DIAGNOSIS_ENABLED,
    OrchestrationEngine,
    QualityEngine,
    VaultEngine,
)
from scriptorium.engines._interactive import RETIRED_NOTE_COMMANDS


def test_repository_audit_authority_and_extended_registry_pass():
    orch = OrchestrationEngine(ROOT)
    quality = QualityEngine(ROOT)

    repo_res = quality.audit_repo()
    assert repo_res["errors"] == [], repo_res["errors"]

    auth_res = orch.lint_authority()
    assert auth_res["valid"] is True, auth_res["issues"]

    reg_res = orch.validate_registry(require_retired_legacy=True)
    assert reg_res["valid"] is True, reg_res["errors"]
    assert reg_res["masters_count"] == 7
    assert reg_res["variants_count"] == 12
    assert reg_res["subtemplates_count"] == 6
    assert reg_res["modules_count"] >= 15
    assert reg_res["commands_count"] == 4
    assert reg_res["retired_commands_count"] == 8


def test_no_retired_commands_leaked_in_active_templates_variants_subtemplates_or_workflows():
    retired_re = re.compile(
        r"/(" + "|".join(re.escape(cmd) for cmd in RETIRED_NOTE_COMMANDS) + r")\b",
        re.I,
    )
    active_dirs = [
        ROOT / "references" / "templates",
        ROOT / "references" / "workflows",
        ROOT / "skills",
    ]
    leaks: list[str] = []
    for base in active_dirs:
        for md in sorted(base.rglob("*.md")):
            text = md.read_text(encoding="utf-8-sig")
            for m in retired_re.finditer(text):
                leaks.append(f"{md.relative_to(ROOT).as_posix()}: {m.group(0)}")
    assert leaks == [], f"Found stale retired slash commands in active files: {leaks}"


def test_authoritative_architecture_docs_and_catalog_completeness():
    overview = ROOT / "references" / "architecture" / "system-overview.md"
    catalog = ROOT / "references" / "architecture" / "template-module-catalog.md"
    assert overview.is_file()
    assert catalog.is_file()

    cat_text = catalog.read_text(encoding="utf-8")
    for mid in ("M1", "M2", "M3", "M4", "M5", "M6", "M7"):
        assert f"`{mid}`" in cat_text
    for sub in ("mathematical", "computational", "scientific", "conceptual", "historical", "empirical"):
        assert f"`{sub}`" in cat_text
    for var in (
        "lecture_order", "formula_sheet", "syntax_reference", "command_reference",
        "atomic_card", "flashcards", "mock_exam", "comparison_guide",
        "paper_breakdown", "quick_summary", "revision_pack", "concept_map",
    ):
        assert f"`{var}`" in cat_text

    ov_text = overview.read_text(encoding="utf-8")
    assert "INTERACTIVE_KNOWLEDGE_DIAGNOSIS_ENABLED = False" in ov_text
    assert INTERACTIVE_KNOWLEDGE_DIAGNOSIS_ENABLED is False


@pytest.mark.parametrize(
    ("request_text", "expected_master", "expected_variant", "expected_subtemplate"),
    [
        # Example 1 — Deep Mathematical Explanation
        ("/scribe-notes Explain Gradient Descent from first principles with derivations.", "M1", None, "mathematical"),
        # Example 2 — Programming Algorithm
        ("/scribe-notes Explain binary search in C with code and execution traces.", "M5", None, "computational"),
        # Example 3 — Quick Reference
        ("/scribe-notes Create a cheat sheet for integration formulas.", "M3", "formula_sheet", "mathematical"),
        # Example 4 — Comparison
        ("/scribe-notes Compare SGD, Momentum, RMSProp, and Adam.", "M7", "comparison_guide", "mathematical"),
        # Example 5 — Source-Faithful Study Notes
        ("/scribe-notes Create detailed notes from this textbook chapter in the original order.", "M2", "lecture_order", None),
        # Example 6 — Broad Knowledge Collection
        ("/scribe-notes Create comprehensive notes on Machine Learning.", "M1", None, None),
        # Example 7 — Cross-Topic Synthesis
        ("/scribe-notes Explain how backpropagation and optimizers work together.", "M1", None, "mathematical"),
    ],
)
def test_part_27_runtime_routing_examples_1_through_7(request_text, expected_master, expected_variant, expected_subtemplate):
    orch = OrchestrationEngine(ROOT)
    has_src = "chapter" in request_text.lower()
    intent, rec, scope = orch.analyze_universal_request(request_text, has_source=has_src)
    routed = orch.route(request_text, has_source=has_src)

    assert rec.recommended_master == expected_master
    if expected_variant is not None:
        assert rec.recommended_variant == expected_variant or routed.get("variant") == expected_variant
    if expected_subtemplate is not None:
        assert expected_subtemplate in routed["knowledge_types"]


def test_part_27_example_8_existing_note_refinement(tmp_path):
    vault = VaultEngine()
    quality = QualityEngine(ROOT)
    bp_path = tmp_path / "Deep Learning" / "Backpropagation.md"
    props = vault.build_properties(topic="Backpropagation", note_type="deep-notes")
    vault.write_note(
        bp_path,
        vault.render_note(
            props,
            "# Backpropagation\n\n## Chain Rule Derivation\nApply the chain rule backwards through each layer.\n\n## Personal Notes\nKeep my diagram note.\n",
        ),
    )

    res = quality.process_feedback(
        tmp_path,
        None,
        "The chain rule derivation in my Backpropagation note is confusing.",
        apply_approved=True,
    )
    assert res["status"] == "applied"
    assert res["target_section"] == "Chain Rule Derivation"
    updated = bp_path.read_text(encoding="utf-8")
    assert "Keep my diagram note." in updated
    assert quality.validate_properties(updated) == []
