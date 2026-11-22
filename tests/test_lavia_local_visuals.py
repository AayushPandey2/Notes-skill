"""End-to-end tests for Scriptorium LAVIA Web-Image-First local-first visual architecture."""
from __future__ import annotations

import binascii
import os
import struct
import zlib

import pytest

from scriptorium.engines.composition import bvia, lavia, media, renderers, visuals
from scriptorium.engines.composition.visuals import render_visuals


def _png(width: int = 2, height: int = 2) -> bytes:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    raw = (b"\x00" + b"\x10\x40\x80" * width) * height
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


def _jpeg(width: int = 32, height: int = 24) -> bytes:
    sof0 = b"\xff\xc0\x00\x11\x08" + struct.pack(">HH", height, width) + b"\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01"
    sos = b"\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\x00"
    return b"\xff\xd8" + sof0 + sos + b"\xff\xd9"


def _webp_vp8l(width: int = 40, height: int = 20) -> bytes:
    bits = ((width - 1) & 0x3FFF) | (((height - 1) & 0x3FFF) << 14)
    payload = b"\x2f" + struct.pack("<I", bits)
    chunk = b"VP8L" + struct.pack("<I", len(payload)) + payload + (b"\x00" if len(payload) % 2 else b"")
    riff_body = b"WEBP" + chunk
    return b"RIFF" + struct.pack("<I", len(riff_body)) + riff_body


def test_multiformat_validation_and_svg_security():
    svg_ok = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50"><rect width="100" height="50" fill="white"/></svg>'
    assert media.validate_image_bytes(svg_ok, "image/svg+xml")["decoder"].startswith("bounded XML/SVG")
    assert media.validate_image_bytes(_png(), "image/png")["width"] == 2
    assert media.validate_image_bytes(_jpeg(64, 48), "image/jpeg")["width"] == 64
    assert media.validate_image_bytes(_webp_vp8l(40, 20), "image/webp")["width"] == 40

    bad_svg = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><script>alert(1)</script></svg>'
    with pytest.raises(ValueError, match="Unsupported active SVG"):
        media.validate_image_bytes(bad_svg, "image/svg+xml")

    with pytest.raises(ValueError, match="DOCTYPE"):
        media.validate_image_bytes(b'<!DOCTYPE svg><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"/>', "image/svg+xml")

    with pytest.raises(ValueError, match="Unsupported image MIME"):
        media.validate_image_bytes(b"GIF89a", "image/gif")


def test_license_verification_and_strategy_selection():
    assert media.verify_license_and_rights("CC-BY-4.0", require_permissive=True)["local_copy_permitted"] is True
    with pytest.raises(ValueError, match="prohibits or leaves unclear"):
        media.verify_license_and_rights("All Rights Reserved", require_permissive=True)

    assert lavia.select_acquisition_strategy({"kind": "source_figure"}) == "retrieve_figure"
    assert lavia.select_acquisition_strategy({"kind": "equation"}) == "retrieve_figure"
    assert lavia.select_acquisition_strategy({"kind": "workflow"}) == "native_mermaid"
    assert lavia.select_acquisition_strategy({"renderer": "table", "kind": "comparison"}) == "markdown_table"


def test_web_image_research_discovery_download_and_pil_inspection(tmp_path, monkeypatch):
    # Verify query escalation + search_web_images permissive rights filtering + PIL inspection + local embed
    host_png = tmp_path / "host_generated.png"
    host_png.write_bytes(_png(360, 220))
    retrieved_png = _png(640, 400)

    queries = lavia.generate_visual_search_queries(
        "Attention Mechanism",
        objective="Illustrate self-attention weight matrix",
        synonyms=["Scaled dot-product attention"],
    )
    assert len(queries) >= 3

    def fake_commons_get(url, timeout=8):
        return {
            "query": {
                "pages": {
                    "101": {
                        "title": "File:Restricted_Diagram.png",
                        "imageinfo": [{
                            "url": "https://upload.wikimedia.org/restricted.png",
                            "descriptionurl": "https://commons.wikimedia.org/wiki/File:Restricted_Diagram.png",
                            "mime": "image/png",
                            "width": 800,
                            "height": 600,
                            "extmetadata": {"LicenseShortName": {"value": "All Rights Reserved"}},
                        }],
                    },
                    "102": {
                        "title": "File:Permissive_Attention_Diagram.png",
                        "imageinfo": [{
                            "url": "https://upload.wikimedia.org/attention_ok.png",
                            "descriptionurl": "https://commons.wikimedia.org/wiki/File:Permissive_Attention_Diagram.png",
                            "mime": "image/png",
                            "width": 640,
                            "height": 400,
                            "extmetadata": {"LicenseShortName": {"value": "CC-BY-SA-4.0"}},
                        }],
                    },
                }
            }
        }

    search_out = lavia.search_web_images(
        queries,
        http_get=fake_commons_get,
    )
    assert search_out["search_status"] == "FOUND"
    assert search_out["candidates"][0]["url"] == "https://upload.wikimedia.org/attention_ok.png"
    assert search_out["candidates"][0]["rights"] == "CC-BY-SA-4.0"
    assert search_out["rejected"]
    assert all(r["url"] == "https://upload.wikimedia.org/restricted.png" for r in search_out["rejected"])

    monkeypatch.setattr(media, "_resolve_public", lambda host: ["93.184.216.34"])
    monkeypatch.setattr(media, "_request_once", lambda url, host, address: (200, {"content-type": "image/png"}, retrieved_png))

    plan = {
        "topic": "Conceptual Intuition",
        "collection_slug": "conceptual-intuition",
        "organize_by_collection": True,
        "embed_style": "wikilink",
        "concepts": [{"id": "c1", "depth": {"conceptual": 3, "visual": 3}}],
        "chapters": [{"id": "ch1", "title": "Intuition", "path": "Conceptual Intuition/01 - Intuition.md", "concepts": ["c1"]}],
        "visuals": [
            {
                "id": "host-illustration",
                "concept": "c1",
                "section": "Host Illustration",
                "objective": "Show host-generated conceptual diagram",
                "kind": "intuition",
                "generated_image": "host_generated.png",
                "alt": "Host conceptual illustration",
            },
            {
                "id": "discovered-attention-diagram",
                "concept": "c1",
                "section": "Discovered Schematic",
                "objective": "Illustrate attention connections using permissive web figure",
                "kind": "source_figure",
                "search_queries": ["attention diagram"],
                "alt": "Attention connection diagram from Wikimedia Commons",
            },
        ],
    }
    drafts = {"ch1": "## Host Illustration\n\nText.\n\n## Discovered Schematic\n\nMore text.\n"}
    bodies, results = render_visuals(tmp_path, plan, drafts, execute=True, http_get=fake_commons_get)
    assert results["host-illustration"]["status"] == "verified"
    assert results["discovered-attention-diagram"]["status"] == "verified"
    assert results["discovered-attention-diagram"]["path"].endswith(".png")
    assert results["discovered-attention-diagram"]["inspection"]["width"] == 640
    assert results["discovered-attention-diagram"]["inspection"]["text_ocr_available"] is False
    manifest = lavia.build_asset_manifest(plan, results)
    assert manifest["schema_version"] == "lavia-manifest/v2"
    assert lavia.validate_collection_visuals(tmp_path, plan, bodies, manifest)["passed"] is True


def test_transformer_regression_local_first_pipeline_and_targeted_repair(tmp_path, monkeypatch):
    # Web-Image-First local-first pipeline across 4 chapter visuals + targeted broken-asset repair.
    fallback_png = tmp_path / "reference_fallback.png"
    fallback_png.write_bytes(_png(420, 260))
    if not os.environ.get("SCRIPTORIUM_LIVE_NET"):
        live_png = _png(640, 380)
        monkeypatch.setattr(media, "_resolve_public", lambda host: ["93.184.216.34"])
        monkeypatch.setattr(
            media,
            "_request_once",
            lambda url, host, address: (200, {"content-type": "image/png"}, live_png),
        )
    def fake_search(url, timeout=8):
        return {
            "query": {
                "pages": {
                    "201": {
                        "title": "File:Transformer_Diagram.png",
                        "imageinfo": [{
                            "url": "https://upload.wikimedia.org/wikipedia/commons/transformer_diagram.png",
                            "descriptionurl": "https://commons.wikimedia.org/wiki/File:Transformer_Diagram.png",
                            "mime": "image/png",
                            "width": 640,
                            "height": 380,
                            "extmetadata": {"LicenseShortName": {"value": "CC-BY-4.0"}},
                        }],
                    }
                }
            }
        }
    plan = {
        "topic": "Transformer Architecture",
        "collection_slug": "transformer-architecture",
        "organize_by_collection": True,
        "embed_style": "wikilink",
        "source_policy": "adaptive",
        "concepts": [
            {"id": "t.overview", "depth": {"conceptual": 3, "visual": 3}},
            {"id": "t.pos", "depth": {"mathematical": 3, "visual": 3}},
            {"id": "t.mask", "depth": {"algorithmic": 3, "visual": 3}, "information_flows": [{"id": "causal"}]},
            {"id": "t.mha", "depth": {"conceptual": 3, "mathematical": 3, "visual": 3}},
        ],
        "chapters": [
            {"id": "ch1", "title": "Foundations", "path": "Transformer Architecture/01 - Foundations.md", "concepts": ["t.overview"]},
            {"id": "ch2", "title": "Positional Encoding", "path": "Transformer Architecture/02 - Positional Encoding.md", "concepts": ["t.pos"]},
            {"id": "ch3", "title": "Causal Masking", "path": "Transformer Architecture/03 - Causal Masking.md", "concepts": ["t.mask"]},
            {"id": "ch4", "title": "Multi-Head Attention", "path": "Transformer Architecture/04 - Multi-Head Attention.md", "concepts": ["t.mha"]},
        ],
        "visuals": [
            {
                "id": "transformer-overview",
                "concept": "t.overview",
                "section": "Architecture",
                "objective": "Show end-to-end encoder-decoder blocks from vetted web reference figure",
                "kind": "architecture",
                "coverage_category": "overall_structure",
                "search_queries": ["Transformer model architecture Vaswani diagram"],
                "local_fallback": "reference_fallback.png",
                "alt": "Transformer encoder-decoder architecture overview",
            },
            {
                "id": "positional-encoding-plot",
                "concept": "t.pos",
                "section": "Sinusoidal Encoding",
                "objective": "Show retrieved sinusoidal encoding pattern figure",
                "kind": "source_figure",
                "coverage_category": "mathematical_behavior",
                "search_queries": ["positional encoding transformer heatmap"],
                "url": "https://upload.wikimedia.org/wikipedia/commons/pos_enc.png",
                "source": "https://commons.wikimedia.org/wiki/File:Positional_Encoding.png",
                "rights": "CC-BY-4.0",
                "require_permissive_license": True,
                "local_fallback": "reference_fallback.png",
                "alt": "Sinusoidal positional encoding heatmap across dimensions",
                "relevance": "Shows periodicity across token positions.",
            },
            {
                "id": "encoder-decoder-flow",
                "concept": "t.mask",
                "section": "Causal Mask",
                "objective": "Show encoder-decoder cross-attention flow natively in Mermaid",
                "kind": "workflow",
                "coverage_category": "information_flow",
                "nodes": [
                    {"id": "enc", "label": "Encoder Keys and Values"},
                    {"id": "dec", "label": "Decoder Masked Query"},
                    {"id": "cross", "label": "Cross-Attention"},
                ],
                "edges": [
                    {"source": "enc", "target": "cross", "label": "K and V"},
                    {"source": "dec", "target": "cross", "label": "Q"},
                ],
            },
            {
                "id": "attention-reference-figure",
                "concept": "t.mha",
                "section": "Multi-Head Attention",
                "objective": "Show external reference figure persisted locally via HTTPS",
                "kind": "source_figure",
                "coverage_category": "component_structure",
                "url": "https://www.python.org/static/community_logos/python-logo.png",
                "source": "https://www.python.org/community/logos/",
                "rights": "PSF-Permissive / CC-BY-4.0",
                "require_permissive_license": True,
                "local_fallback": "reference_fallback.png",
                "alt": "Locally persisted reference PNG figure",
                "relevance": "Exercises HTTPS acquisition, scanline validation, and offline embedding.",
            },
        ],
    }

    coverage = lavia.plan_visual_coverage(plan)
    assert coverage["total_planned_visuals"] == 4
    assert len(coverage["chapters"]) == 4

    drafts = {
        "ch1": "## Architecture\n\nOverview text.\n",
        "ch2": "## Sinusoidal Encoding\n\nWave equations.\n",
        "ch3": "## Causal Mask\n\nMasking rules.\n",
        "ch4": "## Multi-Head Attention\n\nProjection details.\n",
    }

    bodies, results = render_visuals(tmp_path, plan, drafts, execute=True, http_get=fake_search)
    assert all(r["status"] == "verified" for r in results.values()), {k: (v["status"], v["failure_reason"]) for k, v in results.items()}
    assert all(r["path"].startswith("assets/scriptorium/transformer-architecture/") for r in results.values())
    assert "![[assets/scriptorium/transformer-architecture/" in bodies["ch1"]
    assert "![[assets/scriptorium/transformer-architecture/" in bodies["ch4"]
    assert "https://www.python.org/static/community_logos/python-logo.png" not in bodies["ch4"]

    manifest = lavia.build_asset_manifest(plan, results)
    manifest_path = lavia.save_asset_manifest(tmp_path, manifest)
    assert manifest_path.is_file()
    assert manifest["summary"]["verified"] == 4

    validation = lavia.validate_collection_visuals(tmp_path, plan, bodies, manifest)
    assert validation["passed"] is True, validation
    assert validation["offline_ready"] is True
    assert validation["verified_assets"] == 4

    # Simulate deleting one local PNG asset and verify targeted repair restores only that asset
    broken_rel = results["positional-encoding-plot"]["path"]
    (tmp_path / broken_rel).unlink()
    broken_check = lavia.validate_collection_visuals(tmp_path, plan, bodies, manifest)
    assert broken_check["passed"] is False

    repaired = lavia.repair_visual_assets(tmp_path, plan, bodies, manifest, execute=True)
    assert repaired["repaired_ids"] == ["positional-encoding-plot"]
    assert (tmp_path / broken_rel).is_file()
    recheck = lavia.validate_collection_visuals(tmp_path, plan, repaired["bodies"], repaired["manifest"])
    assert recheck["passed"] is True, recheck


def test_web_image_first_request_and_svg_generation_prohibited(tmp_path):
    req = lavia.build_image_research_request(
        job_id="job-1",
        chapter_id="ch5",
        concept_id="t.encoder",
        objective="Illustrate encoder self-attention and residual FFN",
        subject="Transformer encoder block",
        queries=["Transformer encoder self-attention diagram", "Transformer encoder layer Creative Commons"],
    )
    assert req["schema_version"] == "image-research-request/v2"
    assert len(req["search_queries"]) >= 2

    # Programmatic SVG generators must remain completely absent from codebase
    for retired in ("architecture_svg", "scientific_svg", "mask_svg", "flow_svg"):
        assert not hasattr(visuals, retired)
    for retired_r in ("graph_svg", "coordinate_svg"):
        assert not hasattr(renderers, retired_r)
    assert not hasattr(lavia, "evaluate_svg_fallback_gate")

    # Unresolved web search reports an honest unmet visual obligation instead of drawing fake SVG
    unresolved_plan = {
        "topic": "Honesty Test",
        "web_image_first": True,
        "chapters": [{"id": "ch1", "concepts": ["c1"]}],
        "visuals": [{
            "id": "v1",
            "concept": "c1",
            "section": "Arch",
            "objective": "Show schematic",
            "kind": "architecture",
            "search_queries": ["obscure synthetic diagram xyz"],
        }],
    }
    bodies, res = render_visuals(
        tmp_path,
        unresolved_plan,
        {"ch1": "## Arch\n\nSome text.\n"},
        execute=True,
        http_get=lambda url, timeout=8: {"query": {"pages": {}}},
    )
    assert res["v1"]["status"] == "unavailable"
    assert res["v1"]["unmet_visual_obligation"] is True
    assert "NO_IMAGE_EXISTS" in res["v1"]["failure_reason"]
    assert "<svg" not in bodies["ch1"].lower()

    routed = lavia.resolve_visual_route(
        unresolved_plan["visuals"][0],
        search_available=True,
        http_get=lambda url, timeout=8: {"query": {"pages": {}}},
    )
    assert routed["route"] == "unmet_visual_obligation"
    assert routed["search_status"] == "NO_IMAGE_EXISTS"
    assert routed["visual"]["unmet_obligation"]["unmet_obligation"] is True


@pytest.mark.parametrize(
    ("mime", "ext", "payload"),
    [
        (
            "image/svg+xml",
            "svg",
            b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 60"><rect width="120" height="60" fill="white"/></svg>',
        ),
        ("image/jpeg", "jpg", _jpeg(64, 48)),
        ("image/webp", "webp", _webp_vp8l(40, 20)),
    ],
)
def test_media_cache_hit_non_png(tmp_path, monkeypatch, mime, ext, payload):
    url = f"https://example.org/assets/diagram.{ext}"
    visual = {
        "id": f"fig-{ext}",
        "collection_slug": "cache-regression",
        "asset_name": f"diagram-{ext}",
        "url": url,
        "source": "https://example.org/paper",
        "rights": "CC-BY-4.0",
        "require_permissive_license": True,
        "alt": f"Cached {ext} figure",
        "relevance": f"Verifies cached {mime} round-trip without PNG decoder crash.",
        "asset_policy": "local_preferred",
        "embed_style": "wikilink",
    }
    digest = f"digest-{ext}-001"
    monkeypatch.setattr(
        media,
        "fetch_image",
        lambda u: (payload, {"url": u, "final_url": u, "mime": mime, "bytes": len(payload)}),
    )
    first = media.media_artifact(tmp_path, visual, digest, execute=True)
    assert first["cached"] is False
    assert first["path"].endswith(f".{ext}")
    assert (tmp_path / first["path"]).read_bytes() == payload

    # Cache hit on execute=False and rerun execute=True must validate without network calls.
    monkeypatch.setattr(media, "fetch_image", lambda *a, **k: pytest.fail("cache hit must not fetch network"))
    verified_offline = media.media_artifact(tmp_path, visual, digest, execute=False)
    assert verified_offline["cached"] is True
    assert verified_offline["path"] == first["path"]
    assert verified_offline["hash"] == first["hash"]
    assert verified_offline["validation"]["result"] == "pass"

    verified_rerun = media.media_artifact(tmp_path, visual, digest, execute=True)
    assert verified_rerun["cached"] is True
    assert verified_rerun["hash"] == first["hash"]

    # Tampering with the cached non-PNG snapshot must still be rejected.
    (tmp_path / first["path"]).write_bytes(b"corrupted-bytes")
    with pytest.raises(ValueError, match="changed since acquisition"):
        media.media_artifact(tmp_path, visual, digest, execute=False)


def test_pil_image_content_inspection_and_grounding_gate():
    # SVG metadata extraction & grounded visual walkthrough verification (no fabricated label assertions)
    svg_bytes = (
        b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400">'
        b'<rect width="800" height="400" fill="#ffffff"/>'
        b'<text x="40" y="60">Input Tokens</text>'
        b'<text x="320" y="60">Multi-Head Attention</text>'
        b'</svg>'
    )
    svg_info = media.inspect_image_content(svg_bytes, mime="image/svg+xml")
    assert svg_info["width"] == 800
    assert svg_info["text_ocr_available"] is True
    assert {"Input Tokens", "Multi-Head Attention"} <= set(svg_info["text_labels_extracted"])

    vis = {"objective": "Inspect attention pipeline", "alt": "Attention schematic"}
    walkthrough_md = bvia.compose_visual_walkthrough(
        vis,
        embed="![[assets/scriptorium/attention-diagram.png|640]]",
        inspection=svg_info,
    )
    assert "Input Tokens" in walkthrough_md and "Multi-Head Attention" in walkthrough_md

    ok_check = bvia.validate_image_grounded_explanation(
        walkthrough_md,
        vis,
        inspection=svg_info,
    )
    assert ok_check["passed"] is True
    assert ok_check["image_inspected"] is True

    low_res_info = {**svg_info, "readable_for_embedding": False}
    bad_check = bvia.validate_image_grounded_explanation(
        walkthrough_md,
        vis,
        inspection=low_res_info,
    )
    assert bad_check["passed"] is False

    # Raster PIL pixel inspection check
    png_info = media.inspect_image_content(_png(640, 400), mime="image/png")
    assert png_info["width"] == 640 and png_info["height"] == 400
    assert png_info["inspection_method"] == "PIL_pixel_statistics_and_dimension_analysis"
