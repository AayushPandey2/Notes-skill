"""Exercise the consolidated collection execution and final publication gates."""
from types import SimpleNamespace
import json
import sys
import pytest

from scriptorium import OrchestrationEngine, VaultEngine
from scriptorium.engines._interactive import ResolvedNotePreferences
from scriptorium.engines.composition import publication
from scriptorium.engines import vault, _collection_intelligence


def plan_and_preferences():
    preferences = ResolvedNotePreferences("Understand the mechanism", "M1", None, "beginner", {},
                                          "hierarchical_collection", [], "adaptive")
    curriculum = {"title": "Scalar Models", "groups": [("Foundations", [
        ("Coordinates", "M1", [], []), ("Rates", "M1", ["Coordinates"], [])])]}
    plan = OrchestrationEngine().plan_collection("Scalar Models", preferences, curriculum=curriculum)
    return plan, preferences


def test_checkpoint_api_resolves_to_canonical_publisher_and_old_writer_is_absent():
    assert _collection_intelligence.generate_collection_with_checkpoints is publication.generate_collection_with_checkpoints
    assert not hasattr(vault, "_compose_child_note")


def test_ordinary_and_checkpoint_api_share_writer_and_moc_publication(tmp_path):
    plan, preferences = plan_and_preferences()
    result = VaultEngine().generate_collection(tmp_path, plan, preferences)
    assert result["complete"], result["failed_nodes"]
    assert len(result["written_paths"]) == len(plan.nodes)
    children = [r for r in result["records"] if r["role"] == "child"]
    assert children
    assert all(any(e["component"] == "composition.writing.write" for e in r["composition"]["trace"])
               for r in children)
    kcp = SimpleNamespace(plan=plan, existing_note_reconciliation={}, generation={})
    resumed = VaultEngine().generate_with_checkpoints(tmp_path, kcp, preferences)
    assert resumed["complete"]
    assert resumed["skipped_already_committed"] == len(plan.nodes)


def test_unspecified_required_visual_blocks_chapter_and_parent_publication(tmp_path):
    plan, preferences = plan_and_preferences()
    child = next(n for n in plan.nodes if n.note_role == "child")
    result = VaultEngine().generate_collection(tmp_path, plan, preferences,
        teaching_by_node={child.concept_id: {"visual_required": True}})
    assert not result["complete"]
    assert any("visual learning obligation" in n["error"] for n in result["failed_nodes"])
    assert result["note_states"][plan.root_topic_id] == "DEFERRED"
    assert not (tmp_path / child.proposed_path).exists()


def test_final_formula_gate_checks_preserved_user_sections_without_modifying_them(tmp_path):
    plan, preferences = plan_and_preferences()
    first = VaultEngine().generate_collection(tmp_path, plan, preferences)
    assert first["complete"]
    child = next(n for n in plan.nodes if n.note_role == "child")
    path = tmp_path / child.proposed_path
    original = path.read_text(encoding="utf-8") + "\n## Personal formula\n\n$$z = q$$\n"
    path.write_text(original, encoding="utf-8")
    snapshot = path.read_bytes()
    result = VaultEngine().generate_collection(tmp_path, plan, preferences)
    assert not result["complete"]
    assert any("Final publication formula gate" in n["error"] for n in result["failed_nodes"])
    assert path.read_bytes() == snapshot


def test_numbered_filenames_use_resolvable_links(tmp_path):
    from scriptorium import QualityEngine
    plan, preferences = plan_and_preferences()
    for index, node in enumerate(plan.nodes):
        node.proposed_path = f"Scalar Models/{index:02d} - {node.title}.md"
    plan.planned_paths = [n.proposed_path for n in plan.nodes]
    result = VaultEngine().generate_collection(tmp_path, plan, preferences)
    assert result["complete"]
    report = QualityEngine().validate_collection(tmp_path, plan, manifest=result["manifest"])
    assert report["valid"], report["issues"]
    root = next(n for n in plan.nodes if n.concept_id == plan.root_topic_id)
    text = (tmp_path / root.proposed_path).read_text(encoding="utf-8")
    child = next(n for n in plan.nodes if n.note_role == "child")
    assert f"[[{child.proposed_path.removesuffix('.md')}|{child.title}]]" in text


def test_changed_inputs_invalidate_resume_checkpoint(tmp_path):
    plan, preferences = plan_and_preferences()
    kcp = SimpleNamespace(plan=plan, existing_note_reconciliation={}, generation={})
    first = VaultEngine().generate_with_checkpoints(tmp_path, kcp, preferences)
    assert first["complete"]
    child = next(n for n in plan.nodes if n.note_role == "child")
    changed = VaultEngine().generate_with_checkpoints(tmp_path, kcp, preferences,
        source_facts_by_node={child.concept_id: ["A newly supplied source statement."]})
    assert changed["complete"]
    assert changed["skipped_already_committed"] == 0


def test_strict_source_policy_blocks_unsupplied_remote_visual_before_download(tmp_path, monkeypatch):
    from scriptorium.engines.composition import media
    plan, preferences = plan_and_preferences()
    preferences.source_policy = "strict"
    child = next(n for n in plan.nodes if n.note_role == "child")
    def unexpected_download(*args, **kwargs):
        raise AssertionError("Network acquisition must not run")
    monkeypatch.setattr(media, "fetch_image", unexpected_download)
    result = VaultEngine().generate_collection(tmp_path, plan, preferences,
        teaching_by_node={child.concept_id: {"visual_required": True, "visual_specs": [{
            "id": "restricted", "kind": "source_figure", "renderer": "external",
            "section": "Visual Explanation", "objective": "Compare coordinates",
            "url": "https://example.org/figure.png", "source": "https://example.org/source",
            "rights": "CC0", "alt": "Coordinates", "relevance": "Coordinate differences",
        }]}})
    assert not result["complete"]
    assert any("Unfulfilled visual obligations" in n["error"] for n in result["failed_nodes"])


def test_wikipedia_article_license_is_never_assumed_for_its_image():
    from scriptorium.engines.composition.lavia import search_web_images
    def article_only(url, timeout):
        return {"query": {"pages": {"1": {"title": "Article", "pageid": 1,
            "thumbnail": {"source": "https://example.org/photo.png", "width": 600, "height": 400}}}}}
    result = search_web_images(["coordinate diagram"], sources=("wikipedia",), http_get=article_only)
    assert not result["candidates"]
    assert any("license metadata unavailable" in item["reason"] for item in result["rejected"])


def test_tampered_download_invalidates_collection_and_resume(tmp_path):
    from scriptorium import QualityEngine
    from test_lavia_local_visuals import _png
    plan, preferences = plan_and_preferences()
    child = next(n for n in plan.nodes if n.note_role == "child")
    visuals = {child.concept_id: [{"id": "coordinates", "kind": "source_figure", "renderer": "external",
        "section": "Visual Explanation", "objective": "Compare coordinates", "url": "https://example.org/coordinates.png",
        "source": "https://example.org/source", "rights": "CC0", "alt": "Coordinates", "relevance": "Coordinate differences"}]}
    raw = _png(640, 400)
    def fetch(url, timeout):
        return {"status": 200, "headers": {"content-type": "image/png"}, "body": raw}
    kcp = SimpleNamespace(plan=plan, existing_note_reconciliation={}, generation={})
    first = VaultEngine().generate_with_checkpoints(tmp_path, kcp, preferences, visual_specs=visuals, http_get=fetch)
    assert first["complete"], first["failed_nodes"]
    record = next(r for r in first["records"] if r["concept_id"] == child.concept_id)
    asset = next(iter(record["visuals"].values()))
    path = tmp_path / asset["path"]
    path.write_bytes(b"tampered asset")
    checked = QualityEngine().validate_collection(tmp_path, plan, manifest=first["manifest"])
    assert any(issue["category"] == "asset_integrity" for issue in checked["issues"])
    resumed = VaultEngine().generate_with_checkpoints(tmp_path, kcp, preferences, visual_specs=visuals, http_get=fetch)
    assert not resumed["complete"]
    assert any("Unfulfilled visual obligations" in n["error"] for n in resumed["failed_nodes"])
    assert path.read_bytes() == b"tampered asset"


@pytest.mark.parametrize("legacy_flag", [[], ["--legacy-layout"]])
def test_public_generation_never_falls_back_to_generic_prose(tmp_path, monkeypatch, capsys, legacy_flag):
    from pathlib import Path
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    import scribe
    orch = OrchestrationEngine()
    state = orch.start_notes_session("/scribe-notes A concise scalar model reference")
    plan, preferences = plan_and_preferences()
    state.collection_plan = plan
    state.resolved_preferences = preferences
    state.stage = "COLLECTION_PLAN_READY"
    orch.save_session_state(tmp_path, state)
    monkeypatch.setattr(sys, "argv", ["scribe.py", "notes", "generate", "--vault", str(tmp_path),
                                      "--session-id", state.request_id, *legacy_flag])
    assert scribe.main() == 1
    assert json.loads(capsys.readouterr().out)["status"] == "requires_teaching_contract"
    assert not list(tmp_path.rglob("*.md"))
