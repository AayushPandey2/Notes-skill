"""Comprehensive adversarial, structural, semantic, media, video, and protection tests for Part 2 replacement architecture."""
from __future__ import annotations

import hashlib
from io import BytesIO
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from scriptorium import (
    AssetRecord,
    ConceptPlanRecord,
    FormulaTeachingRecord,
    OrchestrationEngine,
    PublicationQualityStatus,
    QualityEngine,
    VaultEngine,
    VideoEvidenceRecord,
    scan_display_math_blocks,
)
from scriptorium.engines import mathematics as math_eng
from scriptorium.engines.composition import media, video
from scriptorium.models import contained_path
from validate_note import validate_text

PROTECTED_SL_DIR = Path(
    r"C:\Users\aayus\OneDrive\Desktop\Notes Vault\6 - Full Notes\6 - Full Notes\Supervised Learning"
)
PROTECTED_SL_HASHES = {
    "00 - Map of Contents.md": "42464CB1CF9CB365AC58503CDBF9092404CCD6729D8FF751880A1835D2195B43",
    "01 - Features, Targets, and Hypothesis Spaces.md": "80937A992356638539698B8A68341270F7055037F1D55DD66A1104AC88BF5C33",
    "02 - Loss Functions.md": "9E034FDF29E1B72BDCFBE3C103909C8545544EA4549F44157CFB25DC5BA17D26",
    "03 - Linear Regression.md": "BC2034F6659DC8E181C77D8A9B157D8C12B8F7304F6692B03FA3E7B3CD3142B0",
    "04 - Logistic Regression.md": "CBE571AF14B2095F6ED65D02F0CB081568B8769BAF075CB1F6D974CC4D2B04D6",
    "05 - Decision Trees.md": "895F4EDAA651A8619ECEC71FE2A3B933D9D7FA67AEFAE59760513D31C85EF348",
    "06 - Bias-Variance Tradeoff.md": "5AE1501E4B816A58E359F90C31B32BF8FF99D906641CA96C88B26CB18CA037F8",
    "07 - Regularization.md": "F299EB1569EA7D485E80AABEFF3CC8732AAE3F711CD3B8BE549E44187BDFA7E4",
}


def _make_png(width: int = 400, height: int = 240, label: str = "step", blank: bool = False, step: int = 1) -> bytes:
    img = Image.new("RGB", (width, height), (245, 248, 252) if step == 1 else (232, 242, 236))
    if not blank:
        draw = ImageDraw.Draw(img)
        draw.rectangle([20, 20, width - 20, height - 20], outline=(20, 40, 80), width=4)
        draw.line([(30, 80), (width - 30, 80)], fill=(180, 40, 40), width=3)
        if step >= 2:
            draw.rectangle([40, 120, width - 40, height - 40], fill=(40, 90, 150))
        draw.text((40, 40), label, fill=(10, 20, 40))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ---------------------------------------------------------------------------
# 1. Shared Content Records & Scanner Boundary Tests
# ---------------------------------------------------------------------------

def test_shared_typed_content_records_and_scanner_edges():
    c = ConceptPlanRecord(concept_id="c-1", canonical_name="Linear Prediction", learning_objective="Compute scalar y_hat")
    a = AssetRecord(asset_id="a-1", asset_type="raster_web", concept_owner="c-1", instructional_role="geometry")
    v = VideoEvidenceRecord(video_id="v-1", source_access_mode="transcript_only")
    q = PublicationQualityStatus(passed=True)
    assert c.selected_depth == 3 and a.verification_status == "pending" and v.source_access_mode == "transcript_only" and q.protected_hashes_verified

    # Code fences, escaped dollars, inline currency must NEVER be scanned as display math;
    # multiline aligned, list math, and assessment quote math MUST be scanned cleanly.
    comp = math_eng.render_formula_component({
        "equation": r"\hat{y} = w x + b",
        "purpose": "Predict y_hat from scalar x using slope w and bias b.",
        "pronunciation": "y-hat equals w x plus b.",
        "symbols": [
            {"symbol": r"\hat{y}", "meaning": "prediction"},
            {"symbol": "w", "meaning": "weight"},
            {"symbol": "x", "meaning": "feature"},
            {"symbol": "b", "meaning": "bias"},
        ],
        "numerical_example": {
            "inputs": {"w": 2, "x": 3, "b": 1},
            "steps": [{"label": "y_hat", "expr": "w * x + b", "result": 7}],
            "expected_result": 7,
            "interpretation": "Prediction equals 7.",
        },
        "placement": "assessment",
    }, quote_prefix="> ")

    md = (
        "---\ntopic: Currency Test\ntags: [test]\nmaster_topic: Test\ndomain: test\nnote_type: deep-notes\n---\n\n"
        "Price is $100 and \\$200 in prose, and code uses `$$not_math$$`:\n\n"
        "```bash\necho \"$$FAKE_MATH$$\"\n```\n\n"
        "In a list item:\n\n"
        f"- First rule:\n\n{comp['display_block'].replace('> ', '')}\n\n{comp['folded_callout'].replace('> >', '>')}\n\n"
        "Inside an assessment answer:\n\n"
        "> [!answer]- Detailed Assessment Answer\n>\n"
        + comp["markdown"].strip() + "\n"
    )
    blocks = scan_display_math_blocks(md)
    assert len(blocks) == 2
    assert all("FAKE_MATH" not in b.expression for b in blocks)
    assert blocks[0].has_following_fold is True
    assert blocks[1].in_callout is True and blocks[1].has_following_fold is True


# ---------------------------------------------------------------------------
# 2. Adversarial Formula-Fold & Math Validation Failures
# ---------------------------------------------------------------------------

def test_formula_fold_rejects_missing_generic_bundled_and_nested_folds():
    # Missing fold
    missing = "# Title\n\nIntro prose.\n\n$$\nz = wx + b\n$$\n"
    res_missing = math_eng.validate_formula_folds(missing)
    assert res_missing["passed"] is False
    assert any(i["code"] == "FORMULA-FOLD-MISSING" for i in res_missing["issues"])

    # Generic filler fold ("substitute the values", "this computes the result")
    generic = (
        "# Title\n\nIntro prose.\n\n$$\nz = w x + b\n$$\n\n"
        "> [!example]- Understand this formula step by step\n"
        "> Just substitute the values and this computes the result cleanly.\n"
    )
    res_generic = math_eng.validate_formula_folds(generic)
    assert res_generic["passed"] is False
    assert any(i["code"] == "FORMULA-FOLD-GENERIC" for i in res_generic["issues"])

    # Bundled multiple unrelated formulas
    bundled = (
        "# Title\n\nIntro.\n\n$$\na = 1 + 2\nb = 3 + 4\nc = 5 + 6\n$$\n\n"
        "> [!example]- Understand this formula step by step\n"
        "> Explains a, b, and c values here with plenty of words so length check passes.\n"
    )
    res_bundled = math_eng.validate_formula_folds(bundled)
    assert any(i["code"] == "FORMULA-BUNDLED" for i in res_bundled["issues"])

    # Recursively nested display $$ inside a formula fold
    nested = (
        "# Title\n\nIntro.\n\n$$\ny = w x\n$$\n\n"
        "> [!example]- Understand this formula step by step\n"
        "> Purpose: scale x by w using inner step:\n>\n"
        "> $$\n> 2 * 3 = 6\n> $$\n"
    )
    res_nested = math_eng.validate_formula_folds(nested)
    assert res_nested["passed"] is False
    assert any(i["code"] in {"FORMULA-FOLD-NESTED", "FORMULA-FOLD-NESTED-MATH"} for i in res_nested["issues"])

    # Wrong non-square dimensions and wrong arithmetic caught
    bad_dim = math_eng.check_dimension_compatibility(
        [{"name": "X", "shape": [3, 2]}, {"name": "w", "shape": [3, 1]}],
        operation="matmul",
    )
    assert bad_dim["valid"] is False
    bad_calc = math_eng.verify_worked_calculation(
        [{"label": "mul", "expr": "w * x", "result": 99}],
        variables={"w": 2, "x": 3},
        expected_result=6,
    )
    assert bad_calc["valid"] is False


# ---------------------------------------------------------------------------
# 3. Raster-Only Acquisition, SVG Rejection & Tamper Checks
# ---------------------------------------------------------------------------

def test_svg_downloads_rejected_and_invalid_image_or_hash_tampering_caught(tmp_path):
    svg_payload = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10"/></svg>'
    with pytest.raises(ValueError, match="SVG"):
        media.validate_image_bytes(svg_payload, "image/svg+xml")
    with pytest.raises(ValueError, match="SVG"):
        media.inspect_image_content(svg_payload, mime="image/svg+xml")
    with pytest.raises(ValueError, match="PNG"):
        media.validate_image_bytes(b"<html>not an image</html>", "image/png")

    # SVG fallback rejected even when offline
    fb_svg = tmp_path / "legacy.svg"
    fb_svg.write_bytes(svg_payload)
    with pytest.raises(ValueError, match="Unsupported fallback image extension"):
        media.media_artifact(
            tmp_path,
            {
                "id": "v1",
                "source": "https://example.org/p",
                "rights": "CC0",
                "alt": "desc",
                "relevance": "rel",
                "asset_policy": "offline_only",
                "local_fallback": "legacy.svg",
            },
            "dig-svg-reject",
            execute=True,
        )

    # Valid PNG stored, then tampered -> must fail verification
    valid_png = tmp_path / "ok.png"
    valid_png.write_bytes(_make_png())
    vis = {
        "id": "v2",
        "source": "https://example.org/p",
        "rights": "CC0",
        "alt": "diagram",
        "relevance": "visual explanation",
        "asset_policy": "offline_only",
        "local_fallback": "ok.png",
    }
    res = media.media_artifact(tmp_path, vis, "dig-ok-1", execute=True)
    assert Path(tmp_path / res["path"]).is_file()
    (tmp_path / res["path"]).write_bytes(b"tampered")
    with pytest.raises(ValueError, match="changed since acquisition"):
        media.media_artifact(tmp_path, vis, "dig-ok-1", execute=False)


# ---------------------------------------------------------------------------
# 4. Unified Video Adapter, Capabilities, Intermediate Frames & Access Limits
# ---------------------------------------------------------------------------

def test_video_adapter_capabilities_frames_timestamps_and_access_states(tmp_path):
    caps = video.discover_video_capabilities()
    # Never lie about unavailable CLI binaries; if ffmpeg absent, extract fails cleanly
    if not caps["cli"]["ffmpeg"]:
        ex = video.extract_frames_with_ffmpeg(tmp_path / "missing.mp4", tmp_path / "out")
        assert ex["status"] == "tool_unavailable"

    # Timestamp out of bounds rejected
    with pytest.raises(ValueError, match="exceeds video duration"):
        video.segment_transcript([{"start": 120, "text": "Late segment"}], video_duration_seconds=60)

    # Timestamp-label mismatch caught by validate_note
    bad_ts_note = (
        "---\nid: v-1\naliases: [Vid]\ntopic: Demo\ntags: [demo]\nnexttopics: []\n---\n\n"
        "# Vid\n\n## 1. Executive Summary\n\nSee [01:30](https://www.youtube.com/watch?v=abc&t=10s).\n"
    )
    findings = validate_text(bad_ts_note, route="summary")
    assert any("t=<seconds>s" in msg for _, msg in findings)

    # Intermediate derivation state preserved, blank frame rejected
    f_blank = _make_png(blank=True)
    f_step1 = _make_png(label="Step 1: r = y - w*x", step=1)
    f_step2 = _make_png(label="Step 2: dL/dw = -2x(y - w*x)", step=2)
    screened = video.screen_frame_candidates(
        [
            {"timestamp_s": 5, "bytes": f_blank},
            {"timestamp_s": 15, "bytes": f_step1, "intermediate_derivation_state": True},
            {"timestamp_s": 30, "bytes": f_step2},
        ],
        vault=tmp_path,
        video_duration_seconds=60,
    )
    assert len(screened["selected"]) == 2
    assert len(screened["rejected"]) == 1 and "blank" in screened["rejected"][0]["reason"]
    assert screened["selected"][0]["intermediate_derivation_state"] is True

    # Transcript-only & metadata-only enforcement + uncertain OCR preserved
    tx_only = video.compose_video_study_payload(
        title="Gradient Clipping",
        source_url="https://www.youtube.com/watch?v=clip1",
        transcript_entries=[{"start": 12, "text": "Clip norm g [uncertain: threshold tau unclear]."}],
        video_duration_seconds=60,
    )
    assert tx_only["access_state"] == "transcript_only"
    assert "no video frames were inspected" in tx_only["markdown"].lower()
    assert "[uncertain: threshold tau unclear]" in tx_only["markdown"]

    meta_only = video.compose_video_study_payload(
        title="Metadata Only Test",
        source_url="https://www.youtube.com/watch?v=meta1",
    )
    assert meta_only["access_state"] == "metadata_only"
    assert meta_only["report"]["complete_notes_permitted"] is False


# ---------------------------------------------------------------------------
# 5. Command Aliases, Containment & Protected Vault Original Hash Verification
# ---------------------------------------------------------------------------

def test_aliases_containment_and_protected_originals_unchanged(tmp_path):
    orch = OrchestrationEngine(ROOT)
    r_yt = orch.route("/scribe-ytnote https://www.youtube.com/watch?v=abc123")
    r_yt1 = orch.route("/scribe-ytnotes https://www.youtube.com/watch?v=abc123")
    r_yt2 = orch.route("/scribe-ytlecture https://www.youtube.com/watch?v=abc123")
    assert r_yt["command"] == "scribe-notes" and r_yt["video_adapter"] is True
    assert r_yt1["command"] == "scribe-notes" and r_yt1["video_adapter"] is True
    assert r_yt2["command"] == "scribe-notes" and r_yt2["video_adapter"] is True
    assert r_yt["master"] == r_yt1["master"] == r_yt2["master"] == "M2"

    r_legacy = orch.route("/scribe-deepnotes Linear Regression")
    assert r_legacy["master"] == "M1" and r_legacy["migration_hint"]

    v1 = orch.execute_trigger("VIDEO-01", {"transcript_entries": [{"start": 0, "text": "intro"}]})
    assert v1["result"]["access_state"] == "transcript_only"
    v4 = orch.execute_trigger("VIDEO-04", {"title": "Meta Probe", "source_url": "https://www.youtube.com/watch?v=meta2"})
    assert v4["result"]["access_state"] == "metadata_only"

    # Traversal outside vault rejected
    with pytest.raises(ValueError, match="escapes"):
        contained_path(tmp_path, "../../outside.md")
    with pytest.raises(ValueError, match="traversal"):
        VaultEngine().write_note(tmp_path / ".." / "escape.md", "bad", validate_properties=False)

    # Recheck protected original Supervised Learning chapters (read-only!)
    if not PROTECTED_SL_DIR.is_dir():
        pytest.skip("Original Supervised Learning folder not present on host")
    for fname, expected_sha in PROTECTED_SL_HASHES.items():
        actual_sha = hashlib.sha256((PROTECTED_SL_DIR / fname).read_bytes()).hexdigest().upper()
        assert actual_sha == expected_sha, f"Protected note modified: {fname}"
    # Verify original Ch3/Ch4 fail the new strict formula-fold gate without being modified
    ch3_text = (PROTECTED_SL_DIR / "03 - Linear Regression.md").read_text(encoding="utf-8-sig")
    ch3_folds = math_eng.validate_formula_folds(ch3_text)
    assert ch3_folds["passed"] is False and ch3_folds["display_count"] == 9 and ch3_folds["folded_count"] == 0
