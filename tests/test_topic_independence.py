"""Topic-independence and canonical architecture verification tests for Scriptorium."""
from __future__ import annotations

import ast
from pathlib import Path
import re
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scriptorium import (
    OrchestrationEngine,
    PedagogyEngine,
    QualityEngine,
    VaultEngine,
)
from scriptorium.engines import _decision as dm
from scriptorium.engines.composition import (
    PUBLICATION_READINESS_STATES,
    build_composition,
    bvia,
    contained,
    lavia,
    media,
    prepare_composition,
    publish_composition,
    renderers,
    resolve_collection_layout,
    visuals,
)
from scriptorium.engines.vault import safe_write_note


# ---------------------------------------------------------------------------
# 1. AST / source scan: zero hardcoded educational lesson presets
# ---------------------------------------------------------------------------

def test_ast_no_hardcoded_educational_lesson_presets():
    """Verify scriptorium/ and scripts/ contain zero hardcoded educational lesson presets."""
    forbidden_preset_names = re.compile(
        r"(CONCEPT_PRESETS|TOPIC_PRESETS|LESSON_PRESETS|SAMPLE_LESSONS|CURATED_TOPICS|DEMO_TOPICS)",
        re.IGNORECASE,
    )
    forbidden_topic_keys = {
        "gradient_descent",
        "binary_search",
        "french_revolution",
        "backpropagation",
        "transformer_attention",
        "biot_savart_law",
        "correlation_and_causation",
    }
    py_roots = [ROOT / "scriptorium", ROOT / "scripts"]
    violations: list[str] = []

    for base in py_roots:
        for py_file in sorted(base.rglob("*.py")):
            rel = py_file.relative_to(ROOT).as_posix()
            text = py_file.read_text(encoding="utf-8")
            tree = ast.parse(text, filename=rel)

            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and forbidden_preset_names.search(node.id):
                    violations.append(f"{rel}:{node.lineno}: preset identifier {node.id!r}")
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and forbidden_preset_names.search(target.id):
                            violations.append(f"{rel}:{node.lineno}: preset assignment {target.id!r}")
                elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                    val_lower = node.value.strip().lower()
                    if val_lower in forbidden_topic_keys:
                        violations.append(f"{rel}:{node.lineno}: hardcoded topic key {node.value!r}")

    assert violations == [], f"Found hardcoded educational lesson presets: {violations}"


# ---------------------------------------------------------------------------
# 2. Zero versioned Scriptorium <N> display branding in active files
# ---------------------------------------------------------------------------

def test_no_versioned_display_branding_in_active_files():
    """Verify active docs, skills, and Python modules use unversioned 'Scriptorium' branding."""
    versioned_branding_re = re.compile(r"\bScriptorium\s+\d+(?:\.\d+)?\b")
    targets: list[Path] = [
        ROOT / "SKILL.md",
        ROOT / "router.md",
        ROOT / "README.md",
    ]
    targets.extend(sorted((ROOT / "skills").rglob("*.md")))
    targets.extend(sorted((ROOT / "scriptorium").rglob("*.py")))

    hits: list[str] = []
    for path in targets:
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        for lineno, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            if versioned_branding_re.search(line):
                hits.append(f"{rel}:{lineno}: {line.strip()}")

    assert hits == [], f"Found versioned 'Scriptorium <N>' display branding: {hits}"


# ---------------------------------------------------------------------------
# 3-7. End-to-end domain-neutral planning, explanation, decision & collection
# ---------------------------------------------------------------------------

def _assert_domain_end_to_end(
    tmp_path: Path,
    *,
    topic: str,
    request_text: str,
    chapters: list[dict],
    concepts: list[dict],
    expected_subject_family: str,
):
    orch = OrchestrationEngine(ROOT)
    ped = PedagogyEngine()
    vault = VaultEngine()
    qual = QualityEngine(ROOT)

    # Routing & decision matrix
    routed = orch.route(request_text)
    assert routed["master"] in {"M1", "M2", "M3", "M4", "M5", "M6", "M7"}
    decision = dm.resolve_decisions(request_text, {"title": topic, "math_level": 2}, topic)
    assert decision["subject_family"] in {"computing", "non-computing", "general"}

    # Explanation blueprint & prose
    bp = ped.build_explanation_blueprint(topic, master="M1", audience="intermediate")
    note = ped.compose_explanation(bp)
    assert note.startswith("---\n")
    assert topic.lower() in note.lower()
    assert vault.validate_properties(note, expected_note_type="deep-notes") == []
    review = qual.review_explanatory_clarity(note, bp, learner_profile="intermediate")
    assert review["passed"] is True, review

    # Composition planning & preparation (5+ chapters required for comprehensive M1 plans)
    prefix = re.sub(r"[^a-z0-9]+", "_", topic.lower()).strip("_")
    all_concepts = list(concepts)
    all_chapters = list(chapters)
    extra_defs = [
        ("foundations", "Foundational Motivation", "Foundations", "Motivate core prerequisites and context"),
        ("applications", "Applied Case Studies", "Applications", "Examine realistic system behavior"),
        ("synthesis", "Synthesis and Boundaries", "Synthesis", "Compare trade-offs and limitations"),
    ]
    while len(all_chapters) < 5:
        suffix, title, section, obj = extra_defs[len(all_chapters) - 2]
        cid = f"{prefix}.{suffix}"
        chid = f"ch{len(all_chapters) + 1}"
        all_concepts.append({
            "id": cid,
            "title": title,
            "section": section,
            "objectives": [obj],
            "capabilities": ["S01"],
            "prerequisites": [all_concepts[0]["id"]],
        })
        all_chapters.append({"id": chid, "title": title, "concepts": [cid], "sections": [section]})

    spec = {
        "topic": topic,
        "chapters": all_chapters,
        "concepts": all_concepts,
        "visuals": [],
        "assessments": [],
        "web_image_first": True,
        "organize_by_collection": True,
        "learner_level": "intermediate",
    }
    plan = build_composition(spec)
    assert plan["topic"] == topic
    assert len(plan["chapters"]) == len(all_chapters)
    drafts = {
        ch["id"]: f"# {ch['title']}\n\n## {ch['sections'][0]}\n\nAnalytical overview of {ch['title']} within {topic}.\n"
        for ch in all_chapters
    }
    prep_drafts, prep_render = prepare_composition(tmp_path, plan, drafts)
    assert set(prep_drafts) == {ch["id"] for ch in all_chapters}
    assert isinstance(prep_render, dict)


def test_domain_raft_consensus_end_to_end(tmp_path: Path):
    """Test 3: Distributed systems domain (Raft Consensus)."""
    _assert_domain_end_to_end(
        tmp_path,
        topic="Raft Consensus",
        request_text="/scribe-notes Explain Raft Consensus leader election and log replication.",
        chapters=[
            {"id": "ch1", "title": "Leader Election", "concepts": ["raft.election"], "sections": ["Terms and Votes"]},
            {"id": "ch2", "title": "Log Replication", "concepts": ["raft.replication"], "sections": ["AppendEntries"]},
        ],
        concepts=[
            {"id": "raft.election", "title": "Leader Election", "section": "Terms and Votes", "objectives": ["explain randomized election timeouts"], "capabilities": ["S01"]},
            {"id": "raft.replication", "title": "Log Replication", "section": "AppendEntries", "objectives": ["explain log matching invariant"], "capabilities": ["S01"], "prerequisites": ["raft.election"]},
        ],
        expected_subject_family="computing",
    )


def test_domain_crispr_cas9_end_to_end(tmp_path: Path):
    """Test 4: Molecular biology domain (CRISPR-Cas9 Gene Editing)."""
    _assert_domain_end_to_end(
        tmp_path,
        topic="CRISPR-Cas9 Gene Editing",
        request_text="/scribe-notes Explain CRISPR-Cas9 Gene Editing mechanisms and PAM recognition.",
        chapters=[
            {"id": "ch1", "title": "Guide RNA Targeting", "concepts": ["crispr.grna"], "sections": ["PAM Sequence"]},
            {"id": "ch2", "title": "Double-Strand Break Repair", "concepts": ["crispr.repair"], "sections": ["NHEJ and HDR"]},
        ],
        concepts=[
            {"id": "crispr.grna", "title": "Guide RNA Targeting", "section": "PAM Sequence", "objectives": ["explain sgRNA hybridization and PAM constraint"], "capabilities": ["S01"]},
            {"id": "crispr.repair", "title": "Double-Strand Break Repair", "section": "NHEJ and HDR", "objectives": ["compare NHEJ vs HDR repair outcomes"], "capabilities": ["S01"], "prerequisites": ["crispr.grna"]},
        ],
        expected_subject_family="non-computing",
    )


def test_domain_bretton_woods_end_to_end(tmp_path: Path):
    """Test 5: Economic history domain (Bretton Woods Monetary System)."""
    _assert_domain_end_to_end(
        tmp_path,
        topic="Bretton Woods Monetary System",
        request_text="/scribe-notes Explain the Bretton Woods Monetary System and its collapse.",
        chapters=[
            {"id": "ch1", "title": "Gold-Dollar Peg", "concepts": ["bw.peg"], "sections": ["Fixed Exchange Rates"]},
            {"id": "ch2", "title": "Triffin Dilemma", "concepts": ["bw.triffin"], "sections": ["Liquidity vs Confidence"]},
        ],
        concepts=[
            {"id": "bw.peg", "title": "Gold-Dollar Peg", "section": "Fixed Exchange Rates", "objectives": ["explain convertibility at $35 per ounce"], "capabilities": ["S01"]},
            {"id": "bw.triffin", "title": "Triffin Dilemma", "section": "Liquidity vs Confidence", "objectives": ["explain reserve currency tension"], "capabilities": ["S01"], "prerequisites": ["bw.peg"]},
        ],
        expected_subject_family="non-computing",
    )


def test_domain_noethers_theorem_end_to_end(tmp_path: Path):
    """Test 6: Theoretical physics domain (Noether's Theorem)."""
    _assert_domain_end_to_end(
        tmp_path,
        topic="Noether's Theorem",
        request_text="/scribe-notes Derive Noether's Theorem connecting continuous symmetries and conservation laws.",
        chapters=[
            {"id": "ch1", "title": "Variational Symmetries", "concepts": ["noether.sym"], "sections": ["Action Invariance"]},
            {"id": "ch2", "title": "Conserved Currents", "concepts": ["noether.current"], "sections": ["Euler-Lagrange Identity"]},
        ],
        concepts=[
            {"id": "noether.sym", "title": "Variational Symmetries", "section": "Action Invariance", "objectives": ["define continuous action symmetry"], "capabilities": ["S01"]},
            {"id": "noether.current", "title": "Conserved Currents", "section": "Euler-Lagrange Identity", "objectives": ["derive conserved Noether charge"], "capabilities": ["S01"], "prerequisites": ["noether.sym"]},
        ],
        expected_subject_family="non-computing",
    )


def test_domain_cardiac_action_potential_end_to_end(tmp_path: Path):
    """Test 7: Physiology domain (Cardiac Action Potential)."""
    _assert_domain_end_to_end(
        tmp_path,
        topic="Cardiac Action Potential",
        request_text="/scribe-notes Explain the phases of the Cardiac Action Potential in ventricular myocytes.",
        chapters=[
            {"id": "ch1", "title": "Depolarization and Plateau", "concepts": ["cardiac.plateau"], "sections": ["Ion Channels"]},
            {"id": "ch2", "title": "Repolarization and Refractory Period", "concepts": ["cardiac.repol"], "sections": ["Potassium Efflux"]},
        ],
        concepts=[
            {"id": "cardiac.plateau", "title": "Depolarization and Plateau", "section": "Ion Channels", "objectives": ["explain Na+ influx and L-type Ca2+ plateau"], "capabilities": ["S01"]},
            {"id": "cardiac.repol", "title": "Repolarization and Refractory Period", "section": "Potassium Efflux", "objectives": ["explain delayed rectifier K+ repolarization"], "capabilities": ["S01"], "prerequisites": ["cardiac.plateau"]},
        ],
        expected_subject_family="non-computing",
    )


# ---------------------------------------------------------------------------
# 8. Canonical A0-A11 architectures & T01-T15 triggers in SKILL.md / router.md
# ---------------------------------------------------------------------------

def test_canonical_architectures_and_triggers_in_docs():
    """Verify A0-A11 architectures and T01-T16 triggers exist in SKILL.md, router.md, and executable registry."""
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    router_text = (ROOT / "router.md").read_text(encoding="utf-8")

    canonical_roles = [
        ("A0", "Director"),
        ("A1", "Map"),
        ("A2", "Tutor"),
        ("A3", "Planner"),
        ("A4", "Researcher"),
        ("A5", "Writer"),
        ("A6", "Visuals"),
        ("A7", "Assets"),
        ("A8", "Quiz"),
        ("A9", "Checker"),
        ("A10", "Vault"),
        ("A11", "Speed"),
    ]
    for arch_id, role in canonical_roles:
        assert arch_id in skill_text or role in skill_text, f"SKILL.md missing {arch_id}/{role}"
        assert arch_id in router_text or role in router_text, f"router.md missing {arch_id}/{role}"

    for idx in range(1, 17):
        tid = f"T{idx:02d}"
        assert tid in skill_text, f"SKILL.md missing trigger {tid}"
        assert tid in router_text, f"router.md missing trigger {tid}"

    orch = OrchestrationEngine(ROOT)
    archs = orch.architectures()
    trigs = orch.triggers()
    assert len(archs) == 12
    assert set(trigs) == {f"T{i:02d}" for i in range(1, 17)}
    # Ensure no SVG-generation trigger exists
    assert not any("svg" in (spec.get("name", "") + spec.get("handler", "")).lower() for spec in trigs.values())

    t01_res = orch.execute_trigger("T01", {"request": "/scribe-notes Explain Thermodynamics"})
    assert t01_res["trigger"] == "T01" and t01_res["result"]["master"] in {"M1", "M2", "M3", "M4", "M5", "M6", "M7"}
    t06_res = orch.execute_trigger(
        "T06",
        {
            "concept_title": "Thermodynamics",
            "objective": "Illustrate Carnot cycle",
            "http_get": lambda url, timeout=8: {"query": {"pages": {}}},
        },
    )
    assert t06_res["trigger"] == "T06" and t06_res["result"]["search_status"] == "NO_IMAGE_EXISTS"


# ---------------------------------------------------------------------------
# 9. Web-Image-First visual research, zero SVG generation, and compliance audit
# ---------------------------------------------------------------------------

def test_retrieval_first_visual_planner_topic_agnostic():
    """Verify lavia/media enforce Web-Image-First discovery, zero SVG creators, and honest unmet obligations."""
    req = lavia.build_image_research_request(
        job_id="job-raft-1",
        chapter_id="ch1",
        concept_id="raft.election",
        objective="Illustrate Raft leader election state transitions",
        subject="Raft consensus follower candidate leader state machine",
        queries=["Raft consensus leader election state diagram"],
    )
    assert req["schema_version"] == "image-research-request/v2"
    assert req["search_queries"] == ["Raft consensus leader election state diagram"]

    route = lavia.resolve_visual_route(
        {"id": "v1", "concept": "raft.election", "objective": "Show state transitions"},
        host_candidates=[
            {
                "url": "https://example.org/raft-states.png",
                "source": "Raft Paper",
                "rights": "CC-BY-4.0",
            }
        ],
    )
    assert route["route"] == "external_image_download"
    assert route["search_status"] == "FOUND"

    # Retired SVG diagram generators must not exist anywhere in active composition modules
    for name in ("architecture_svg", "scientific_svg", "mask_svg", "flow_svg", "validate_svg"):
        assert not hasattr(visuals, name), f"Retired SVG symbol {name} still present in visuals.py"
    for name in ("graph_svg", "coordinate_svg"):
        assert not hasattr(renderers, name), f"Retired SVG symbol {name} still present in renderers.py"
    assert not hasattr(lavia, "evaluate_svg_fallback_gate")

    unmet = lavia.record_unmet_visual_obligation(
        {"id": "v2", "concept": "raft.log"},
        search_status="NO_IMAGE_EXISTS",
        queries_attempted=["Raft append entries diagram"],
    )
    assert unmet["unmet_obligation"] is True
    assert unmet["fallback_generation"] == "prohibited"

    compliance = QualityEngine(ROOT).audit_compliance()
    assert compliance["passed"] is True, compliance


def test_isolated_temp_vault_layout_and_readiness_states(tmp_path: Path, monkeypatch):
    """Verify collections land cleanly under vault root (no category folder) and readiness states hold."""
    folder, moc_path, flat_prefix = resolve_collection_layout("Cardiac Action Potential", vault_root=tmp_path)
    assert folder == "Cardiac Action Potential"
    assert moc_path == "Cardiac Action Potential/00 - Map of Contents.md"
    assert flat_prefix is None
    assert "6 - Full Notes" not in folder

    assert {"complete", "complete_with_justified_omissions", "draft", "partial", "blocked", "failed"} == set(PUBLICATION_READINESS_STATES)

    # Verify PIL image inspection + Explain -> Show -> Decode -> Connect + T08 trigger execution
    import binascii, struct, zlib
    def _png(w=400, h=260):
        def chunk(k, d):
            return struct.pack(">I", len(d)) + k + d + struct.pack(">I", binascii.crc32(k + d) & 0xFFFFFFFF)
        ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
        raw = b"".join(
            b"\x00" + (b"\x18\x30\x60" if (y % 20) < 10 else b"\xe0\xec\xf4") * w
            for y in range(h)
        )
        return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")

    fig_bytes = _png()
    orch = OrchestrationEngine(ROOT)
    t08_res = orch.execute_trigger("T08", {"source": fig_bytes, "mime": "image/png"})
    insp = t08_res["result"]["inspection"]
    assert insp["width"] == 400 and insp["height"] == 260 and insp["inspection_performed"] is True
    walkthrough = bvia.compose_visual_walkthrough(
        {"objective": "Illustrate action potential", "alt": "Ventricular action potential waveform"},
        embed="![[assets/scriptorium/cardiac/ap.png|400]]",
        inspection=insp,
    )
    check = bvia.validate_image_grounded_explanation(
        walkthrough,
        {"objective": "Illustrate action potential"},
        inspection=insp,
    )
    assert check["passed"] is True


# ---------------------------------------------------------------------------
# 10. Protected vault / non-destructive path guard verification
# ---------------------------------------------------------------------------

def test_protected_vault_and_non_destructive_path_guards(tmp_path: Path):
    """Verify path containment and safe_write_note prevent escapes outside the target vault."""
    vault = tmp_path / "vault"
    vault.mkdir()

    with pytest.raises(ValueError):
        contained(vault, "../outside.md")

    with pytest.raises(ValueError):
        contained(vault, str(tmp_path / "escape.md"))

    protected_like = Path(r"C:\Users\aayus\OneDrive\Desktop\Notes Vault\6 - Full Notes\Transformer Architecture\00 - Map of Contents.md")
    with pytest.raises(ValueError):
        contained(vault, str(protected_like))

    target = contained(vault, "Raft Consensus/01 - Leader Election.md")
    assert target.resolve().is_relative_to(vault.resolve())
    ve = VaultEngine()
    props = ve.build_properties(topic="Raft Consensus", note_type="deep-notes")
    note_text = ve.render_note(props, "# Leader Election\n\nRandomized election timeouts.\n")
    safe_write_note(target, note_text)
    assert target.is_file()
