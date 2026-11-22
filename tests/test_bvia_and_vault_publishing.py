"""Tests for Scriptorium 5.2 BVIA (Beginner-First Visual Intelligence) and vault-native publishing."""
from __future__ import annotations

from scriptorium.engines.composition import build_composition, bvia, lavia, resolve_collection_layout


def _minimal_spec(**extra):
    concepts = [
        {"id": f"c{i}", "title": f"Concept {i}", "section": "Core", "objectives": [f"Explain concept {i}"], "prerequisites": [] if i == 1 else [f"c{i-1}"]}
        for i in range(1, 6)
    ]
    chapters = [
        {"id": f"ch{i}", "title": f"Chapter {i}", "concepts": [f"c{i}"]}
        for i in range(1, 6)
    ]
    return {"topic": "Transformer Architecture", "concepts": concepts, "chapters": chapters, **extra}


def test_default_publishing_omits_category_folder_and_prevents_duplicates(tmp_path):
    plan = build_composition(_minimal_spec())
    assert plan["folder"] == "Transformer Architecture"
    assert plan["moc_path"] == "Transformer Architecture/00 - Map of Contents.md"
    assert plan["chapters"][0]["path"] == "Transformer Architecture/01 - Chapter 1.md"
    assert "6 - Full Notes" not in plan["folder"]

    # Explicit category folder works when requested, and guards against duplicate segments
    folder, moc, _ = resolve_collection_layout(
        "Transformer Architecture",
        create_category_folders=True,
        category_folder="6 - Full Notes",
        vault_root=tmp_path / "6 - Full Notes",
    )
    assert folder == "Transformer Architecture"
    assert moc == "Transformer Architecture/00 - Map of Contents.md"

    # Optional flat_root layout uses collision-safe topic prefix
    flat_plan = build_composition(_minimal_spec(publishing={"collection_layout": "flat_root"}))
    assert flat_plan["folder"] == ""
    assert flat_plan["moc_path"] == "Transformer Architecture - 00 - Map of Contents.md"
    assert flat_plan["chapters"][0]["path"] == "Transformer Architecture - 01 - Chapter 1.md"


def test_bvia_accessibility_ranking_and_accuracy_gate():
    inaccurate_simple = {
        "id": "bad",
        "url": "https://example.org/bad.png",
        "rights": "CC0",
        "technical_accuracy": False,
        "labeled_components": 2,
        "width": 800,
        "height": 600,
    }
    beginner = {
        "id": "beg",
        "url": "https://example.org/beg.png",
        "rights": "CC BY 4.0",
        "technical_accuracy": True,
        "labeled_components": 4,
        "unexplained_abbreviations": 0,
        "arrow_density": "low",
        "diagram_clutter": "low",
        "width": 1000,
        "height": 600,
        "educational_role": "overview",
    }
    advanced = {
        "id": "adv",
        "url": "https://example.org/adv.png",
        "rights": "CC BY 4.0",
        "technical_accuracy": True,
        "labeled_components": 16,
        "unexplained_abbreviations": 5,
        "arrow_density": "high",
        "diagram_clutter": "high",
        "width": 1400,
        "height": 1500,
        "educational_role": "full_research",
    }
    unlicensed = {**beginner, "id": "unlic", "rights": "All Rights Reserved"}

    assert bvia.evaluate_visual_accessibility(inaccurate_simple)["classification"] == "unsuitable"
    assert bvia.evaluate_visual_accessibility(beginner)["classification"] == "beginner_friendly"
    assert bvia.evaluate_visual_accessibility(advanced)["classification"] == "advanced_technical"

    ranked = bvia.rank_image_candidates(
        [inaccurate_simple, unlicensed, advanced, beginner],
        learner_level="beginner",
    )
    assert [c["id"] for c in ranked] == ["beg", "adv"]


def test_bvia_progressive_ladder_and_explain_show_decode_connect():
    v_adv = {"id": "v_adv", "progression_level": 5, "accessibility": {"classification": "advanced_technical"}}
    v_beg = {"id": "v_beg", "progression_level": 1, "accessibility": {"classification": "beginner_friendly"}}
    ordered = bvia.plan_progressive_visuals([v_adv, v_beg])
    assert [v["id"] for v in ordered] == ["v_beg", "v_adv"]

    registry = {"Q": "Query vector", "K": "Key vector", "V": "Value vector"}
    visual = {
        "objective": "how attention matches queries against keys",
        "alt": "Scaled dot-product attention diagram",
        "abbreviations": ["Q", "K", "V"],
        "decode_components": ["Project inputs into Q, K, V matrices.", "Apply softmax to scaled dot products."],
    }
    md = bvia.compose_visual_walkthrough(
        visual,
        embed="![[assets/scriptorium/transformer-architecture/scaled-dot-product-attention.png]]",
        terminology_registry=registry,
    )
    check = bvia.validate_explain_show_decode_connect(md, visual, terminology_registry=registry)
    assert check["passed"] is True, check

    contract = bvia.build_visual_teaching_contract(
        visual_id="transformer.encoder.overview",
        concept_id="transformer.encoder",
        purpose="explain_encoder_structure",
        prerequisite_concepts=["token_embeddings", "self_attention"],
        progression_level=2,
        required_labels=["input", "attention", "normalization", "feed_forward", "output"],
    )
    assert contract["representation"]["acquisition_priority"] == "external_first"
    assert contract["educational"]["progression_level"] == "component_identification"

    # Retrieval-first still takes priority over SVG generation
    routed = lavia.resolve_visual_route(
        {"id": "enc", "concept": "transformer.encoder", "objective": "Encoder architecture"},
        host_candidates=[{"url": "https://example.org/enc.png", "source": "https://example.org/page", "rights": "CC BY 4.0"}],
    )
    assert routed["route"] == "external_image_download"


def test_lavia_manifest_and_validation_handle_mermaid_and_block_remote_leaks(tmp_path):
    from scriptorium.engines.composition.visuals import render_visuals

    plan = {
        "topic": "Attention Flow",
        "collection_slug": "attention-flow",
        "organize_by_collection": True,
        "embed_style": "wikilink",
        "concepts": [{"id": "c1", "depth": {"conceptual": 2, "algorithmic": 2}}],
        "chapters": [{"id": "ch1", "title": "Flow", "path": "Attention Flow/01 - Flow.md", "concepts": ["c1"]}],
        "visuals": [
            {
                "id": "flow-mmd",
                "concept": "c1",
                "section": "Flow",
                "objective": "Show query-key-value flow",
                "kind": "workflow",
                "nodes": [{"id": "q", "label": "Query"}, {"id": "a", "label": "Attention"}],
                "edges": [{"source": "q", "target": "a", "label": "dot"}],
            }
        ],
    }
    bodies, results = render_visuals(tmp_path, plan, {"ch1": "## Flow\n\nDetailed walkthrough.\n"}, execute=True)
    assert results["flow-mmd"]["status"] == "verified"
    manifest = lavia.build_asset_manifest(plan, results)
    check = lavia.validate_collection_visuals(tmp_path, plan, bodies, manifest)
    assert check["passed"] is True, check

    leaked = {"ch1": bodies["ch1"] + "\n![leaked](https://cdn.example.org/hotlink.png)\n"}
    leaked_check = lavia.validate_collection_visuals(tmp_path, plan, leaked, manifest)
    assert leaked_check["passed"] is False
    assert any("remote image URL embed forbidden" in err for err in leaked_check["errors"])
