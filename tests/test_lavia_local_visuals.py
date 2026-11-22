"""End-to-end tests for Scriptorium 5.1 LAVIA local-first visual architecture."""
from __future__ import annotations

import binascii
import os
import struct
import xml.etree.ElementTree as ET
import zlib

import pytest

from scriptorium.engines.composition import lavia, media
from scriptorium.engines.composition.visuals import (
    NS,
    architecture_svg,
    render_visuals,
    scientific_svg,
    validate_svg,
)


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
    assert lavia.select_acquisition_strategy({"kind": "equation"}) == "deterministic_render"
    assert lavia.select_acquisition_strategy({"kind": "intuition"}, host_imagegen_available=True) == "conceptual_illustration"
    with pytest.raises(ValueError, match="exact numerical evidence"):
        lavia.select_acquisition_strategy({"kind": "intuition", "equation": "x*2"}, host_imagegen_available=True)


def test_imagegen_host_artifact_and_deterministic_fallback(tmp_path):
    host_png = tmp_path / "host_generated.png"
    host_png.write_bytes(_png(12, 12))

    plan = {
        "topic": "Conceptual Intuition",
        "collection_slug": "conceptual-intuition",
        "organize_by_collection": True,
        "embed_style": "wikilink",
        "concepts": [{"id": "c1", "depth": {"conceptual": 3, "visual": 3}}],
        "chapters": [{"id": "ch1", "title": "Intuition", "path": "6 - Full Notes/Intuition/01 - Intuition.md", "concepts": ["c1"]}],
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
                "id": "fallback-illustration",
                "concept": "c1",
                "section": "Fallback Schematic",
                "objective": "Show conceptual fallback schematic",
                "kind": "intuition",
                "labels": ["Query", "Key", "Value"],
            },
        ],
    }
    drafts = {"ch1": "## Host Illustration\n\nText.\n\n## Fallback Schematic\n\nMore text.\n"}
    bodies, results = render_visuals(tmp_path, plan, drafts, execute=True)
    assert results["host-illustration"]["status"] == "verified"
    assert results["host-illustration"]["path"].endswith(".png")
    assert results["fallback-illustration"]["status"] == "verified"
    assert results["fallback-illustration"]["path"].endswith(".svg")
    assert results["fallback-illustration"]["fallback_used"] is True
    manifest = lavia.build_asset_manifest(plan, results)
    assert lavia.validate_collection_visuals(tmp_path, plan, bodies, manifest)["passed"] is True


def test_transformer_regression_local_first_pipeline_and_targeted_repair(tmp_path, monkeypatch):
    # Deterministic local socket mock by default; set SCRIPTORIUM_LIVE_NET=1 to hit live HTTPS.
    fallback_png = tmp_path / "reference_fallback.png"
    fallback_png.write_bytes(_png(16, 12))
    if not os.environ.get("SCRIPTORIUM_LIVE_NET"):
        live_png = _png(16, 12)
        monkeypatch.setattr(media, "_resolve_public", lambda host: ["93.184.216.34"])
        monkeypatch.setattr(
            media,
            "_request_once",
            lambda url, host, address: (200, {"content-type": "image/png"}, live_png),
        )
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
            {"id": "ch1", "title": "Foundations", "path": "6 - Full Notes/Transformer Architecture/01 - Foundations.md", "concepts": ["t.overview"]},
            {"id": "ch2", "title": "Positional Encoding", "path": "6 - Full Notes/Transformer Architecture/02 - Positional Encoding.md", "concepts": ["t.pos"]},
            {"id": "ch3", "title": "Causal Masking", "path": "6 - Full Notes/Transformer Architecture/03 - Causal Masking.md", "concepts": ["t.mask"]},
            {"id": "ch4", "title": "Multi-Head Attention", "path": "6 - Full Notes/Transformer Architecture/04 - Multi-Head Attention.md", "concepts": ["t.mha"]},
        ],
        "visuals": [
            {
                "id": "transformer-overview",
                "concept": "t.overview",
                "section": "Architecture",
                "objective": "Show end-to-end encoder-decoder blocks and tensor shapes",
                "kind": "architecture",
                "coverage_category": "overall_structure",
                "components": [
                    {"label": "Embeddings", "shape": "B, T, d_model"},
                    {"label": "Encoder Stack", "shape": "B, T, d_model"},
                    {"label": "Decoder Stack", "shape": "B, T, d_model"},
                ],
            },
            {
                "id": "positional-encoding-plot",
                "concept": "t.pos",
                "section": "Sinusoidal Encoding",
                "objective": "Plot positional scaling curve x / (1 + x * x)",
                "kind": "equation",
                "coverage_category": "mathematical_behavior",
                "equation": "x / (1 + x * x)",
                "x_values": [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
                "xlabel": "position",
                "ylabel": "encoding",
                "units": "dimensionless",
                "interpretation": "Bounded smooth curve across token positions.",
            },
            {
                "id": "encoder-decoder-flow",
                "concept": "t.mask",
                "section": "Causal Mask",
                "objective": "Show encoder-decoder cross-attention information flow",
                "kind": "network",
                "coverage_category": "information_flow",
                "nodes": [
                    {"id": "enc", "label": "Encoder Keys/Values"},
                    {"id": "dec", "label": "Decoder Masked Query"},
                    {"id": "cross", "label": "Cross-Attention"},
                ],
                "edges": [
                    {"source": "enc", "target": "cross", "label": "K, V"},
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

    bodies, results = render_visuals(tmp_path, plan, drafts, execute=True)
    assert all(r["status"] == "verified" for r in results.values()), {k: (v["status"], v["failure_reason"]) for k, v in results.items()}
    assert all(r["path"].startswith("assets/scriptorium/transformer-architecture/") for r in results.values())
    assert "![[assets/scriptorium/transformer-architecture/" in bodies["ch1"]
    assert "![[assets/scriptorium/transformer-architecture/" in bodies["ch4"]
    assert "https://www.python.org/static/community_logos/python-logo.png" not in bodies["ch4"]  # Local-first embed, not remote image URL

    manifest = lavia.build_asset_manifest(plan, results)
    manifest_path = lavia.save_asset_manifest(tmp_path, manifest)
    assert manifest_path.is_file()
    assert manifest["summary"]["verified"] == 4

    validation = lavia.validate_collection_visuals(tmp_path, plan, bodies, manifest)
    assert validation["passed"] is True, validation
    assert validation["offline_ready"] is True
    assert validation["verified_assets"] == 4

    # Simulate deleting one generated SVG asset and verify targeted repair restores only that asset
    broken_rel = results["positional-encoding-plot"]["path"]
    (tmp_path / broken_rel).unlink()
    broken_check = lavia.validate_collection_visuals(tmp_path, plan, bodies, manifest)
    assert broken_check["passed"] is False

    repaired = lavia.repair_visual_assets(tmp_path, plan, bodies, manifest, execute=True)
    assert repaired["repaired_ids"] == ["positional-encoding-plot"]
    assert (tmp_path / broken_rel).is_file()
    recheck = lavia.validate_collection_visuals(tmp_path, plan, repaired["bodies"], repaired["manifest"])
    assert recheck["passed"] is True, recheck


def test_web_image_first_policy_and_svg_fallback_gate(tmp_path):
    req = lavia.build_image_research_request(
        job_id="job-1",
        chapter_id="ch5",
        concept_id="t.encoder",
        objective="Illustrate encoder self-attention and residual FFN",
        subject="Transformer encoder block",
        queries=["Transformer encoder self-attention diagram", "Transformer encoder layer Creative Commons"],
    )
    assert req["schema_version"] == "image-research-request/v1"
    assert len(req["search_queries"]) == 2

    # Gate blocks undocumented SVG generation when web_image_first=True
    undocumented_plan = {
        "topic": "Gate Test",
        "web_image_first": True,
        "chapters": [{"id": "ch1", "concepts": ["c1"]}],
        "visuals": [{"id": "v1", "concept": "c1", "section": "Arch", "objective": "Show blocks", "kind": "architecture", "components": [{"label": "A", "shape": "B"}]}],
    }
    _, res = render_visuals(tmp_path, undocumented_plan, {"ch1": "## Arch\n\nSome text.\n"}, execute=True)
    assert res["v1"]["status"] == "failed"
    assert "fallback_gate" in res["v1"]["failure_reason"]

    # Route 4 with documented NO_IMAGE_EXISTS permits fallback cleanly
    routed = lavia.resolve_visual_route(
        undocumented_plan["visuals"][0],
        search_available=True,
        fallback_decision={
            "search_status": "NO_IMAGE_EXISTS",
            "queries_attempted": ["custom block diagram"],
            "justification": "No openly licensed diagram matches this exact toy block interface.",
        },
    )
    assert routed["route"] == "documented_fallback"
    documented_plan = {**undocumented_plan, "visuals": [routed["visual"]]}
    bodies, res2 = render_visuals(tmp_path, documented_plan, {"ch1": "## Arch\n\n" + ("Detailed explanation of blocks and tensor flow. " * 4) + "\n"}, execute=True)
    assert res2["v1"]["status"] == "verified"

    ob_check = lavia.verify_visual_obligations(
        [{"obligation_id": "ob1", "chapter_id": "ch1", "local_asset_path": res2["v1"]["path"], "acquisition_status": "documented_fallback"}],
        bodies,
        tmp_path,
    )
    assert ob_check["passed"] is True, ob_check


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


def test_architecture_svg_dynamic_box_widths_and_connectors():
    components = [
        {"label": "Input Embeddings", "shape": "B, T, d_model"},
        {"label": "Scaled Dot-Product + Mask", "shape": "B, h, T, T"},
        {"label": "Output", "shape": "B, T, d_model (projected)"},
    ]
    svg = architecture_svg(components)
    assert validate_svg(svg) == []
    root = ET.fromstring(svg)
    _, _, vb_w, _ = map(float, root.get("viewBox").split())
    rects = root.findall(f"{{{NS}}}rect")
    paths = root.findall(f"{{{NS}}}path")
    assert len(rects) == len(components)
    assert len(paths) == len(components) - 1

    expected_widths = [max(180, len(c["label"]) * 9 + 24, len(c["shape"]) * 9 + 24) for c in components]
    prev_right = 0.0
    for idx, (rect, exp_w) in enumerate(zip(rects, expected_widths)):
        rx = float(rect.get("x"))
        rw = float(rect.get("width"))
        assert rw == exp_w
        if idx == 1:
            assert rw >= len("Scaled Dot-Product + Mask") * 9 + 24 > 180
        if idx > 0:
            assert rx > prev_right
        prev_right = rx + rw
        if idx < len(paths):
            d_attr = paths[idx].get("d", "")
            assert d_attr.startswith(f"M{int(rx + rw)} ")
    assert prev_right < vb_w


def test_scientific_svg_ylabel_separation_and_colored_legend_swatches():
    series = {
        "Scaled Attention": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0)],
        "Unscaled Attention": [(0.0, 1.0), (1.0, 0.4), (2.0, 0.0)],
    }
    svg = scientific_svg(series, title="Attention Scaling", xlabel="position", ylabel="weight")
    assert validate_svg(svg) == []
    root = ET.fromstring(svg)

    texts = root.findall(f"{{{NS}}}text")
    ylabel_el = next(t for t in texts if t.text == "weight")
    top_tick_el = next(t for t in texts if t.text == "1")
    ylabel_x, ylabel_y = float(ylabel_el.get("x")), float(ylabel_el.get("y"))
    tick_x, tick_y = float(top_tick_el.get("x")), float(top_tick_el.get("y"))
    # ylabel must be well-separated from the top y-tick (no collision).
    assert abs(ylabel_x - tick_x) >= 30
    assert abs(ylabel_y - tick_y) >= 30

    polylines = root.findall(f"{{{NS}}}polyline")
    series_colors = [p.get("stroke") for p in polylines]
    assert len(series_colors) == 2 and len(set(series_colors)) == 2

    swatches = [ln for ln in root.findall(f"{{{NS}}}line") if ln.get("stroke") in series_colors]
    assert [ln.get("stroke") for ln in swatches] == series_colors

    for name, swatch in zip(series, swatches):
        legend_el = next(t for t in texts if t.text == name)
        assert float(swatch.get("x2")) < float(legend_el.get("x"))
        assert abs(float(swatch.get("y1")) - float(legend_el.get("y"))) <= 10
