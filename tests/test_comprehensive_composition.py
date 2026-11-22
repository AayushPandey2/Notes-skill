"""Observable comprehensive composition, publication, and recovery behavior."""
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scriptorium.engines.composition import (
    FIVE_KEYS, allocate_depth, build_composition, capabilities, evidence_status,
    inventory_migration, publish_composition, render_table, resolve_capabilities,
    select_visual, to_collection_plan, validate_chapter,
)
from scriptorium.engines.composition.media import validate_svg_markup as validate_svg
from scriptorium.engines._collection_intelligence import build_knowledge_collection_plan
from scriptorium.engines._interactive import ResolvedNotePreferences
from scriptorium.models import content_hash, parse_note


def specification():
    return {"topic": "Gradient Descent", "source_policy": "strict",
            "chapters": [{"id": f"ch{i}", "title": f"Chapter {i}", "concepts": [f"c{i}"], "sections": [f"Concept {i}"]} for i in range(1, 6)],
            "concepts": [{"id": f"c{i}", "title": f"Concept {i}", "objectives": ["explain the mechanism"],
                          "capabilities": ["S01"], "prerequisites": [f"c{i-1}"] if i > 1 else []} for i in range(1, 6)],
            "assessments": [{"id": f"q{i}.{j}", "chapter": f"ch{i}", "objectives": [f"c{i}:objective:0"],
                              "type": kind, "question": question, "hint": "Use the stated local quadratic assumptions.",
                              "solution": solution}
                             for i in range(1, 6) for j, (kind, question, solution) in enumerate([
                                 ("conceptual", "What does the update use?", "It uses the current gradient and a chosen positive step."),
                                 ("numerical", "What is x minus one half x at x=2?", "2 - 0.5(2) = 1, using the stipulated scalar state."),
                                 ("diagnosis", "Can a local direction guarantee a finite decrease?", "No; the higher-order remainder can dominate for a finite step."),
                                 ("comparison", "How do alpha=1 and alpha=2 differ for x squared over two?", "The first reaches zero in one update; the second alternates without contracting.")])]}


def reviews_for(plan, drafts):
    """Test-only reviewer assertions; these fixtures do not certify teaching quality."""
    def receipt(chapters):
        return {"verifier": "pytest fixture reviewer", "method": "fixture-scoped review",
                "result": "pass", "limitations": "Synthetic contract fixture; not an independent factual review.",
                "evidence": [{"chapter": cid, "hash": content_hash(drafts[cid]), "excerpt": drafts[cid].splitlines()[0]}
                             for cid in chapters]}
    return {**{r: receipt(drafts) for r in plan["review_required"]},
            "obligations": {o["id"]: receipt([o["owner"]]) for o in plan["obligations"]}}


def inputs(plan):
    from scriptorium.engines.composition.contracts import prepare_drafts
    drafts = {f"ch{i}": f"# Chapter {i}\n\n## Concept {i}\n\nAn authored explanation, reviewed separately.\n" for i in range(1, 6)}
    drafts = {cid: text.strip()+"\n" for cid, text in prepare_drafts(plan, drafts).items()}
    evidence = {o["id"]: {"verified": True, "source": "supplied textbook", "location": "section 9.3", "origin": "supplied"}
                for c in plan["concepts"] for o in c["research_obligations"]}
    for record in evidence.values():
        record.update(claim="The fixture uses a local update under explicit assumptions.", classification="definition",
                      version="fixture-v1", verification_method="supplied fixture inspection", limits="fixture only")
    reviews = reviews_for(plan, drafts)
    return drafts, evidence, reviews


def test_capability_dependencies_and_unique_stage_owners():
    selected = resolve_capabilities(["S04", "S02", "S12", "S13", "S10"])
    assert selected[:3] == ["S01", "S03", "S04"]
    assert len(selected) == len(set(selected))
    spec = specification()
    spec["concepts"][0]["capabilities"] = selected
    plan = build_composition(spec)
    sequence = plan["concepts"][0]["sequence"]
    assert len({s["stage"] for s in sequence}) == len(sequence)
    setup = next(s for s in sequence if s["stage"] == "definitions_and_setup")
    assert setup["owner"] == "S01"
    assert len(capabilities()) == 18
    with pytest.raises(ValueError, match="Unknown capability"):
        resolve_capabilities(["S99"])


def test_depth_is_independent_and_escalates_without_violating_strict_policy():
    depth = allocate_depth({"objectives": ["trace state", "derive update"], "depth": {"implementation": 0},
                            "signals": {"conflicting_evidence": True, "source_gap": True}}, source_policy="strict")
    assert depth["levels"]["algorithmic"] == depth["levels"]["mathematical"] == 3
    assert depth["levels"]["implementation"] == 0
    assert depth["levels"]["research"] == 4
    assert not depth["external_retrieval_permitted"] and depth["unresolved"]


@pytest.mark.parametrize("fault", ["missing_owner", "duplicate_owner", "cycle", "unknown", "chapter_count"])
def test_invalid_knowledge_graphs_are_rejected(fault):
    spec = specification()
    if fault == "missing_owner":
        spec["concepts"].append({"id": "orphan"})
    if fault == "duplicate_owner":
        spec["chapters"][1]["concepts"].append("c1")
    if fault == "cycle":
        spec["concepts"][0]["prerequisites"] = ["c5"]
    if fault == "unknown":
        spec["concepts"][2]["prerequisites"] = ["missing"]
    if fault == "chapter_count":
        spec["chapters"].pop()
    with pytest.raises(ValueError):
        build_composition(spec)


def test_source_policy_and_contradictions_block_evidence_stop():
    plan = build_composition(specification())
    _, evidence, _ = inputs(plan)
    obligations = [o for c in plan["concepts"] for o in c["research_obligations"]]
    assert evidence_status(obligations, evidence)["stop_retrieval"]
    oid = obligations[0]["id"]
    evidence[oid]["origin"] = "web"
    assert not evidence_status(obligations, evidence)["sufficient"]
    evidence[oid]["origin"] = "supplied"
    evidence[oid]["contradictions"] = ["different assumptions"]
    assert oid in evidence_status(obligations, evidence)["escalate"]


def test_full_collection_publishes_six_clean_files_and_resumes_without_rewrites(tmp_path):
    plan = build_composition(specification())
    drafts, evidence, reviews = inputs(plan)
    result = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)
    assert result["complete"] and len(result["written_paths"]) == 6
    folder = tmp_path / plan["folder"]
    assert len(list(folder.iterdir())) == 6
    for path in folder.glob("*.md"):
        assert set(parse_note(path.read_text(encoding="utf-8")).metadata) == FIVE_KEYS
    moc = (tmp_path / plan["moc_path"]).read_text(encoding="utf-8")
    assert "n0 --> n1" in moc
    result = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)
    assert result["complete"] and not result["written_paths"]


def test_kcp_uses_shared_composition_and_keeps_optional_outputs_inside_chapters(tmp_path):
    composition = build_composition(specification())
    plan = to_collection_plan(composition)
    prefs = ResolvedNotePreferences("understand", "M1", None, "comprehensive", {}, "hierarchical_collection", [], "strict")
    kcp = build_knowledge_collection_plan(tmp_path, plan, prefs, include_synthesis=True, include_assessment=True)
    assert kcp.composition == composition
    assert not kcp.synthesis_notes and not kcp.assessment_plan


@pytest.mark.parametrize("fault", ["draft", "review", "evidence", "placeholder", "link", "asset", "section"])
def test_publication_preflight_writes_nothing_on_failure(tmp_path, fault):
    plan = build_composition(specification())
    drafts, evidence, reviews = inputs(plan)
    if fault == "draft": drafts.pop("ch1")
    if fault == "review": reviews.clear()
    if fault == "evidence": evidence.clear()
    if fault == "placeholder": drafts["ch1"] += "\nTODO complete this"
    if fault == "link": drafts["ch1"] += "\n[[Missing]]"
    if fault == "asset": drafts["ch1"] += "\n![[assets/missing.svg]]"
    if fault == "section": drafts["ch1"] = "# Missing planned concept\n\nOther text."
    result = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)
    assert not result["complete"] and result["errors"] and not list(tmp_path.rglob("*.md"))


def test_targeted_update_requires_reviewed_hash_and_preserves_other_chapters(tmp_path):
    plan = build_composition(specification())
    drafts, evidence, reviews = inputs(plan)
    publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)
    snapshots = {p: p.read_bytes() for p in tmp_path.rglob("*.md")}
    relative = plan["chapters"][0]["path"]
    digest = content_hash((tmp_path / relative).read_text(encoding="utf-8"))
    drafts["ch1"] += "\nA localized correction with its justification."
    assert not publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)["complete"]
    from scriptorium.engines.composition import prepare_composition
    drafts, _ = prepare_composition(tmp_path, plan, drafts)
    reviews = reviews_for(plan, drafts)
    result = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews, expected_hashes={relative: digest})
    assert result["complete"] and result["written_paths"] == [relative]
    for path, data in snapshots.items():
        if path != tmp_path / relative: assert path.read_bytes() == data
    inventory = inventory_migration(tmp_path, [relative])
    assert inventory["status"] == "inventory_only" and not inventory["deletion_permitted"]
    assert inventory["backlinks"]


def test_table_comparison_rejects_incomparable_units_and_conditions():
    table = {"type": "experimental", "objective": "Compare latency under the same setup.", "interpretation": "Conditions determine applicability.",
             "rows": [{"method": m, "metric": "latency", "value": 2, "units": "ms", "conditions": "same CPU", "source": "measured fixture", "uncertainty": "not measured"} for m in ("A", "B")]}
    assert "| method | metric |" in render_table(table)
    table["rows"][1]["units"] = "s"
    with pytest.raises(ValueError, match="Incomparable"):
        render_table(table)


def test_web_image_first_visual_selection_and_svg_retirement():
    visual = select_visual(
        {"kind": "equation", "objective": "Show curvature", "search_queries": ["quadratic curve diagram"]},
        available={"external"},
    )
    assert visual["renderer"] == "external"
    assert select_visual({"kind": "intuition", "objective": "Build intuition"}, available=set())["status"] == "unavailable"
    with pytest.raises(ValueError, match="removed"):
        select_visual({"kind": "equation", "objective": "Plot", "renderer": "svg"}, available={"external"})
    assert validate_svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10"/></svg>') == []


def test_cli_plans_without_writing_and_rejects_bad_spec(tmp_path):
    spec = tmp_path / "spec.json"
    spec.write_text(json.dumps(specification()), encoding="utf-8")
    result = subprocess.run([sys.executable, str(ROOT / "scripts/scribe.py"), "notes", "compose", "--spec", str(spec)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["output_profile"] == "comprehensive_multifile"
    assert not list(tmp_path.rglob("*.md"))


def test_mathematical_and_code_truncation_are_detected():
    plan = build_composition(specification())
    from scriptorium.engines.composition import five_key_note
    text = five_key_note(plan, "c", "Chapter", "# Chapter\n\n$$x=1", None)
    assert "unclosed display mathematics" in validate_chapter(text)
    assert "unclosed code fence" in validate_chapter(text + "\n```python\nx = 1\n")


def test_spec_changes_invalidate_identity():
    spec = specification()
    before = build_composition(spec)["spec_hash"]
    spec["concepts"][0]["depth"] = {"mathematical": 4}
    assert build_composition(spec)["spec_hash"] != before


def test_validation_detects_manual_changes_and_dirty_topic_folder(tmp_path):
    from scriptorium.engines.composition import validate_published_composition
    plan = build_composition(specification())
    drafts, evidence, reviews = inputs(plan)
    publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)
    assert validate_published_composition(tmp_path, plan)["valid"]
    chapter = tmp_path / plan["chapters"][0]["path"]
    chapter.write_text(chapter.read_text(encoding="utf-8") + "\nManual edit", encoding="utf-8")
    assert any("changed since review" in e for e in validate_published_composition(tmp_path, plan)["errors"])
    (tmp_path / plan["folder"] / "temporary.json").write_text("{}")
    assert any("only the 6 planned" in e for e in validate_published_composition(tmp_path, plan)["errors"])


def test_partial_write_failure_is_reported_and_resumable(tmp_path, monkeypatch):
    from scriptorium.engines import vault as vault_module
    original = vault_module.safe_write_note
    plan = build_composition(specification())
    drafts, evidence, reviews = inputs(plan)
    def failing(path, *args, **kwargs):
        if path.name.startswith("03 -"):
            raise OSError("simulated disk failure")
        return original(path, *args, **kwargs)
    monkeypatch.setattr(vault_module, "safe_write_note", failing)
    result = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)
    assert not result["complete"] and len(result["written_paths"]) == 2
    assert result["errors"] and len(result["checkpoints"]) == 2
    monkeypatch.setattr(vault_module, "safe_write_note", original)
    resumed = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)
    assert resumed["complete"] and len(resumed["written_paths"]) == 4


def test_dependency_cycle_is_rejected(monkeypatch):
    import scriptorium.engines.composition as module
    specs = capabilities()
    specs["S01"]["dependencies"] = ["S04"]
    monkeypatch.setattr(module, "capabilities", lambda: specs)
    with pytest.raises(ValueError, match="cycle"):
        resolve_capabilities(["S04"])
