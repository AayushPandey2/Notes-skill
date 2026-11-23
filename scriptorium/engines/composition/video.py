"""Unified Video Source Adapter for /scribe-ytnotes and /scribe-ytlecture -> /scribe-notes.

Discovers actual local tool availability honestly, tracks explicit source-access
states, normalizes timestamps, segments transcripts semantically, screens candidate
video frames for readability while preserving meaningful intermediate derivation
states, and feeds Scriptorium's shared Concept/Formula/Asset/Narrative records.
"""
from __future__ import annotations

from io import BytesIO
import importlib.util
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any
from urllib.parse import parse_qs, urlsplit, urlunsplit

from scriptorium.engines.composition.media import inspect_image_content
from scriptorium.models import (
    AssetRecord,
    ConceptPlanRecord,
    VideoEvidenceRecord,
    contained_path,
    slugify,
)

VIDEO_ACCESS_STATES: tuple[str, ...] = (
    "full_multimodal",
    "transcript_plus_frames",
    "transcript_only",
    "media_only",
    "metadata_only",
)

_FILLER_RE = re.compile(r"\b(?:uh+|um+|erm+|you know|like i said|sort of)\b", re.I)
_SHIFT_CUE_RE = re.compile(
    r"\b(?:now\s+let'?s|next(?:\s+step|\s+topic)?|moving\s+on|for\s+example|suppose\s+we|"
    r"let\s+us\s+derive|to\s+prove|finally|in\s+summary|ab\s+dekho|next\s+part)\b",
    re.I,
)
_UNCERTAIN_MARKER_RE = re.compile(r"\[(?:uncertain|inaudible|blurry|unverified|illegible)[^\]]*\]", re.I)


def discover_video_capabilities() -> dict[str, Any]:
    """Probe actual host tools and libraries; never claim availability unless observed."""
    cli_tools = {
        name: shutil.which(name)
        for name in ("ffmpeg", "ffprobe", "yt-dlp", "youtube-dl", "whisper")
    }
    py_mods = {
        mod: (importlib.util.find_spec(mod) is not None)
        for mod in ("PIL", "numpy", "cv2", "youtube_transcript_api")
    }
    return {
        "cli": {k: (v is not None) for k, v in cli_tools.items()},
        "cli_paths": cli_tools,
        "python": py_mods,
        "can_download_youtube": bool(cli_tools["yt-dlp"] or cli_tools["youtube-dl"]),
        "can_extract_local_frames": bool(cli_tools["ffmpeg"]),
        "can_transcribe_audio": bool(cli_tools["whisper"]),
        "can_inspect_raster_frames": bool(py_mods["PIL"]),
        "can_score_frame_deltas": bool(py_mods["PIL"] and py_mods["numpy"]),
    }


def extract_youtube_id(url: str) -> str | None:
    """Extract canonical YouTube video ID from standard, short, or shorts URLs."""
    parts = urlsplit((url or "").strip())
    host = (parts.hostname or "").lower().removeprefix("www.").removeprefix("m.")
    if host == "youtu.be":
        vid = parts.path.strip("/").split("/")[0]
        return vid or None
    if host in {"youtube.com", "youtube-nocookie.com"}:
        if parts.path == "/watch":
            return (parse_qs(parts.query).get("v") or [None])[0]
        m = re.match(r"^/(?:embed|shorts|live)/([A-Za-z0-9_-]{6,})", parts.path)
        if m:
            return m.group(1)
    return None


def parse_timestamp_seconds(raw: int | float | str) -> int:
    """Parse seconds or HH:MM:SS / MM:SS strings into non-negative integer seconds."""
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        if raw < 0:
            raise ValueError(f"Timestamp must be non-negative: {raw}")
        return int(round(raw))
    text = str(raw).strip()
    if text.isdigit():
        return int(text)
    parts = text.split(":")
    if len(parts) == 2 and all(p.isdigit() for p in parts):
        return int(parts[0]) * 60 + int(parts[1])
    if len(parts) == 3 and all(p.isdigit() for p in parts):
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    raise ValueError(f"Unrecognized video timestamp: {raw!r}")


def format_timestamp_link(source_url: str, seconds: int) -> str:
    """Format a deterministic [MM:SS](url?t=<seconds>s) markdown timestamp link."""
    if seconds < 0:
        raise ValueError("Timestamp seconds cannot be negative")
    mm, ss = divmod(seconds, 60)
    label = f"{mm:02d}:{ss:02d}"
    parts = urlsplit(source_url.strip())
    q = parse_qs(parts.query, keep_blank_values=True)
    vid = extract_youtube_id(source_url)
    query_pairs: list[str] = []
    if vid and parts.path == "/watch":
        query_pairs.append(f"v={vid}")
    else:
        for k, vals in q.items():
            if k != "t":
                query_pairs.extend(f"{k}={v}" for v in vals)
    query_pairs.append(f"t={seconds}s")
    clean_url = urlunsplit((parts.scheme or "https", parts.netloc, parts.path, "&".join(query_pairs), ""))
    return f"[{label}]({clean_url})"


def classify_access_state(
    *,
    has_video_media: bool = False,
    has_frames: bool = False,
    has_transcript: bool = False,
    has_audio_track: bool = False,
) -> str:
    """Classify source access explicitly; never pretend metadata or transcript-only is full multimodal."""
    if has_transcript and (has_video_media or has_frames):
        return "full_multimodal" if (has_video_media and has_audio_track) else "transcript_plus_frames"
    if has_transcript:
        return "transcript_only"
    if has_video_media or has_frames:
        return "media_only"
    return "metadata_only"


def clean_transcript_text(text: str) -> tuple[str, list[str]]:
    """Trim conversational filler carefully while preserving variables, numbers, Hinglish, and uncertainty."""
    uncertain = _UNCERTAIN_MARKER_RE.findall(text or "")
    cleaned = _FILLER_RE.sub("", text or "")
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned).strip()
    return cleaned, uncertain


def segment_transcript(
    entries: list[dict[str, Any]],
    *,
    video_duration_seconds: int | None = None,
    max_segment_seconds: int = 240,
) -> list[dict[str, Any]]:
    """Group transcript entries into meaning-based concept intervals (not fixed blind chunks)."""
    if not entries:
        return []

    normalized: list[dict[str, Any]] = []
    for entry in entries:
        start_s = parse_timestamp_seconds(entry.get("start", entry.get("timestamp", 0)))
        dur_s = parse_timestamp_seconds(entry.get("duration", 0)) if entry.get("duration") is not None else 0
        if video_duration_seconds is not None and start_s > video_duration_seconds:
            raise ValueError(f"Transcript timestamp {start_s}s exceeds video duration {video_duration_seconds}s")
        text, unc = clean_transcript_text(str(entry.get("text") or ""))
        if not text:
            continue
        normalized.append({
            "start_s": start_s,
            "end_s": start_s + max(1, dur_s),
            "text": text,
            "uncertain_markers": unc,
            "confidence": float(entry.get("confidence", 0.9 if not unc else 0.45)),
            "scene_change": bool(entry.get("scene_change", False)),
            "language": str(entry.get("language") or "en"),
        })

    if not normalized:
        return []

    segments: list[dict[str, Any]] = []
    current_items: list[dict[str, Any]] = [normalized[0]]

    for item in normalized[1:]:
        seg_elapsed = item["start_s"] - current_items[0]["start_s"]
        meaning_shift = bool(_SHIFT_CUE_RE.search(item["text"]))
        hard_scene = bool(item["scene_change"]) and seg_elapsed >= 20
        if meaning_shift or hard_scene or seg_elapsed >= max_segment_seconds:
            segments.append(_finalize_segment(len(segments) + 1, current_items))
            current_items = [item]
        else:
            current_items.append(item)

    segments.append(_finalize_segment(len(segments) + 1, current_items))
    return segments


def _finalize_segment(index: int, items: list[dict[str, Any]]) -> dict[str, Any]:
    text = " ".join(x["text"] for x in items)
    uncertain = [u for x in items for u in x["uncertain_markers"]]
    avg_conf = round(sum(x["confidence"] for x in items) / max(len(items), 1), 3)
    return {
        "segment_id": f"seg-{index:02d}",
        "start_s": items[0]["start_s"],
        "end_s": max(x["end_s"] for x in items),
        "text": text,
        "uncertain_markers": uncertain,
        "confidence": avg_conf,
        "languages": sorted({x["language"] for x in items}),
    }


def _score_frame_pixels(raw: bytes) -> dict[str, Any]:
    """Compute dimension, brightness, contrast, edge sharpness, and a compact downsampled array."""
    info = inspect_image_content(raw)
    sharpness = float(info.get("contrast_stddev") or 0.0)
    thumb_vec = None
    try:
        import numpy as np
        from PIL import Image

        with Image.open(BytesIO(raw)) as img:
            gray = img.convert("L")
            arr = np.asarray(gray, dtype=np.float32)
            dx = np.abs(np.diff(arr, axis=1)).mean() if arr.shape[1] > 1 else 0.0
            dy = np.abs(np.diff(arr, axis=0)).mean() if arr.shape[0] > 1 else 0.0
            sharpness = round(float(dx + dy) * 0.5, 3)
            small = gray.resize((64, 36))
            thumb_vec = np.asarray(small, dtype=np.float32)
    except Exception:
        pass
    return {**info, "sharpness_grad": sharpness, "_thumb": thumb_vec}


def extract_frames_with_ffmpeg(
    video_path: Path,
    output_dir: Path,
    *,
    timestamps: list[int] | None = None,
    fps: float = 0.5,
    max_frames: int = 24,
) -> dict[str, Any]:
    """Extract candidate PNG frames via local ffmpeg when available; report unavailability cleanly."""
    caps = discover_video_capabilities()
    if not caps["cli"]["ffmpeg"]:
        return {
            "status": "tool_unavailable",
            "tool": "ffmpeg",
            "frames": [],
            "reason": "ffmpeg binary was not found on PATH; cannot decode local video into candidate frames.",
        }
    if not Path(video_path).is_file():
        raise FileNotFoundError(f"Local video file does not exist: {video_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg_bin = caps["cli_paths"]["ffmpeg"]
    extracted: list[dict[str, Any]] = []

    if timestamps:
        for ts in timestamps[:max_frames]:
            out_file = output_dir / f"frame-{int(ts):05d}s.png"
            subprocess.run(
                [ffmpeg_bin, "-y", "-ss", str(int(ts)), "-i", str(video_path), "-frames:v", "1", str(out_file)],
                check=True,
                capture_output=True,
            )
            if out_file.is_file():
                extracted.append({"timestamp_s": int(ts), "path": str(out_file), "source_type": "ffmpeg_extracted"})
    else:
        pattern = str(output_dir / "frame-%04d.png")
        subprocess.run(
            [ffmpeg_bin, "-y", "-i", str(video_path), "-vf", f"fps={fps}", "-frames:v", str(max_frames), pattern],
            check=True,
            capture_output=True,
        )
        for idx, p in enumerate(sorted(output_dir.glob("frame-*.png"))):
            extracted.append({"timestamp_s": int(round(idx / max(fps, 1e-6))), "path": str(p), "source_type": "ffmpeg_extracted"})

    return {"status": "extracted", "tool": "ffmpeg", "frames": extracted}


def screen_frame_candidates(
    candidates: list[dict[str, Any]],
    *,
    vault: Path | None = None,
    collection_slug: str = "video-notes",
    video_duration_seconds: int | None = None,
    min_width: int = 320,
    min_height: int = 180,
    min_contrast: float = 5.0,
    min_sharpness: float = 1.0,
    dup_delta_threshold: float = 1.5,
    max_selected: int = 20,
) -> dict[str, Any]:
    """Evaluate candidate frames for readability and meaningful visual/derivation state changes."""
    selected: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    prev_thumb = None
    prev_hash = None

    ordered = sorted(candidates, key=lambda c: parse_timestamp_seconds(c.get("timestamp_s", c.get("timestamp", 0))))
    for item in ordered:
        ts = parse_timestamp_seconds(item.get("timestamp_s", item.get("timestamp", 0)))
        if video_duration_seconds is not None and ts > video_duration_seconds:
            rejected.append({"timestamp_s": ts, "reason": f"timestamp {ts}s exceeds video duration {video_duration_seconds}s"})
            continue

        raw_bytes: bytes | None = item.get("bytes")
        fpath = Path(item["path"]) if item.get("path") else None
        if raw_bytes is None and fpath is not None:
            if not fpath.is_file():
                rejected.append({"timestamp_s": ts, "path": str(fpath), "reason": "frame file does not exist"})
                continue
            raw_bytes = fpath.read_bytes()
        if not raw_bytes:
            rejected.append({"timestamp_s": ts, "reason": "empty frame payload"})
            continue

        try:
            scored = _score_frame_pixels(raw_bytes)
        except Exception as exc:
            rejected.append({"timestamp_s": ts, "reason": f"invalid raster image: {exc}"})
            continue

        w = int(scored.get("width") or 0)
        h = int(scored.get("height") or 0)
        contrast = float(scored.get("contrast_stddev") or 0.0)
        sharp = float(scored.get("sharpness_grad") or 0.0)
        if w < min_width or h < min_height:
            rejected.append({"timestamp_s": ts, "reason": f"low resolution {w}x{h} (< {min_width}x{min_height})"})
            continue
        if contrast < min_contrast or sharp < min_sharpness:
            rejected.append({"timestamp_s": ts, "reason": f"blurry or blank frame (contrast={contrast}, sharpness={sharp})"})
            continue
        if item.get("is_transition") or item.get("irrelevant_presenter_only"):
            rejected.append({"timestamp_s": ts, "reason": "transition or irrelevant presenter-only shot"})
            continue

        thumb = scored.pop("_thumb", None)
        fhash = scored["content_hash"]
        delta_score = 999.0
        if thumb is not None and prev_thumb is not None:
            try:
                import numpy as np
                delta_score = round(float(np.abs(thumb - prev_thumb).mean()), 3)
            except Exception:
                pass
        elif fhash == prev_hash:
            delta_score = 0.0

        is_dup = (fhash == prev_hash) or (delta_score < dup_delta_threshold and not item.get("intermediate_derivation_state"))
        if is_dup:
            rejected.append({"timestamp_s": ts, "reason": f"near-duplicate frame (delta={delta_score})"})
            continue

        local_rel = str(fpath) if fpath else ""
        if vault is not None:
            ext = "png" if scored["mime"] == "image/png" else ("jpg" if scored["mime"] == "image/jpeg" else "webp")
            local_rel = f"assets/scriptorium/{slugify(collection_slug)}/frame-{ts:05d}s-{fhash[:10]}.{ext}"
            dest = contained_path(vault, local_rel)
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                dest.write_bytes(raw_bytes)

        prev_thumb = thumb
        prev_hash = fhash
        selected.append({
            "timestamp_s": ts,
            "local_path": local_rel,
            "sha256": fhash,
            "mime": scored["mime"],
            "width": w,
            "height": h,
            "contrast_stddev": contrast,
            "sharpness_grad": sharp,
            "state_delta": delta_score,
            "intermediate_derivation_state": bool(item.get("intermediate_derivation_state")),
            "selection_reason": str(item.get("selection_reason") or ("intermediate derivation step" if item.get("intermediate_derivation_state") else "visual state change")),
            "visible_elements": list(item.get("visible_elements") or []),
            "ocr_uncertain": list(item.get("ocr_uncertain") or []),
            "confidence": float(item.get("confidence", 0.9 if not item.get("ocr_uncertain") else 0.5)),
            "source_type": str(item.get("source_type") or "supplied_frame"),
        })
        if len(selected) >= max_selected:
            break

    return {"selected": selected, "rejected": rejected}


def build_video_access_report(
    *,
    video_id: str,
    title: str,
    source_url: str,
    access_state: str,
    capabilities: dict[str, Any] | None = None,
    reason: str = "",
) -> dict[str, Any]:
    """Generate an honest metadata-only / partial-access report instead of fabricated lecture notes."""
    caps = capabilities or discover_video_capabilities()
    markdown = "\n".join([
        f"# Video Access Report: {title}",
        "",
        f"> [!warning] Access Limitation ({access_state})",
        f"> Complete lecture notes cannot be produced from `{access_state}` access alone.",
        f"> Source URL: {source_url}" if source_url else "> Source URL: not provided",
        f"> Reason: {reason or 'Neither transcript nor extractable video frames were accessible in the current environment.'}",
        "",
        "## Host Tool Availability (Observed)",
        f"- `yt-dlp`: `{caps['cli']['yt-dlp']}` | `ffmpeg`: `{caps['cli']['ffmpeg']}` | `whisper`: `{caps['cli']['whisper']}` | `PIL`: `{caps['python']['PIL']}`",
        "",
        "## Required Next Inputs to Generate Complete Notes",
        "- Supply a timestamped transcript/subtitles file (`.srt` / `.vtt` / timestamped text), or an accessible local video file / candidate frame images.",
    ]) + "\n"
    return {
        "video_id": video_id,
        "access_state": access_state,
        "complete_notes_permitted": False,
        "markdown": markdown,
        "capabilities": caps,
    }


def compose_video_study_payload(
    *,
    title: str,
    source_url: str = "",
    transcript_entries: list[dict[str, Any]] | None = None,
    frame_candidates: list[dict[str, Any]] | None = None,
    equations: list[dict[str, Any]] | None = None,
    vault: Path | None = None,
    collection_slug: str | None = None,
    video_duration_seconds: int | None = None,
    has_video_media: bool = False,
) -> dict[str, Any]:
    """Normalize transcript + frames into unified Scriptorium records & grounded Markdown."""
    caps = discover_video_capabilities()
    vid = extract_youtube_id(source_url) or slugify(title) or "video"
    cslug = slugify(collection_slug or title or vid)

    screened = (
        screen_frame_candidates(
            frame_candidates,
            vault=vault,
            collection_slug=cslug,
            video_duration_seconds=video_duration_seconds,
        )
        if frame_candidates else {"selected": [], "rejected": []}
    )
    selected_frames = screened["selected"]
    segments = (
        segment_transcript(transcript_entries, video_duration_seconds=video_duration_seconds)
        if transcript_entries else []
    )

    access_state = classify_access_state(
        has_video_media=has_video_media,
        has_frames=bool(selected_frames),
        has_transcript=bool(segments),
        has_audio_track=bool(segments),
    )

    if access_state == "metadata_only":
        report = build_video_access_report(
            video_id=vid,
            title=title,
            source_url=source_url,
            access_state=access_state,
            capabilities=caps,
        )
        record = VideoEvidenceRecord(
            video_id=vid,
            source_access_mode=access_state,
            source_url=source_url,
            acquisition_method="metadata_probe_only",
            confidence="low",
            uncertainty_notes=["Only metadata available; complete lecture notes blocked."],
        )
        return {
            "video_id": vid,
            "access_state": access_state,
            "record": record,
            "assets": [],
            "concepts": [],
            "report": report,
            "markdown": report["markdown"],
            "screened_frames": screened,
        }

    # Align selected frames to semantic transcript segments
    aligned: list[dict[str, Any]] = []
    if segments:
        for seg in segments:
            seg_frames = [
                f for f in selected_frames
                if seg["start_s"] <= f["timestamp_s"] <= seg["end_s"] + 5
            ]
            aligned.append({"segment": seg, "frames": seg_frames})
    else:
        for idx, frm in enumerate(selected_frames, 1):
            aligned.append({
                "segment": {"segment_id": f"frame-seg-{idx:02d}", "start_s": frm["timestamp_s"], "end_s": frm["timestamp_s"], "text": "", "uncertain_markers": [], "confidence": frm["confidence"], "languages": []},
                "frames": [frm],
            })

    assets: list[AssetRecord] = []
    for f in selected_frames:
        assets.append(AssetRecord(
            asset_id=f"frame-{f['timestamp_s']:05d}s",
            asset_type="video_frame",
            concept_owner=cslug,
            instructional_role=f["selection_reason"],
            source_page_url=source_url,
            acquisition_url=source_url,
            local_path=f["local_path"],
            sha256=f["sha256"],
            width=f["width"],
            height=f["height"],
            detected_format=f["mime"],
            attribution=f"{title} @ {f['timestamp_s']}s ({f['source_type']})",
            rights="source_educational_frame",
            inspection_status="inspected",
            verification_status="verified",
        ))

    uncertain_notes: list[str] = []
    for seg in segments:
        uncertain_notes.extend(seg["uncertain_markers"])
    for f in selected_frames:
        uncertain_notes.extend(f["ocr_uncertain"])
    if access_state == "transcript_only":
        uncertain_notes.append("Transcript-only mode: no video frames were inspected or embedded.")

    presenter_claims = [seg["text"] for seg in segments if seg["text"]]
    added_reconstruction = [
        f"Aligned {len(selected_frames)} verified frames across {len(segments)} meaning segments."
        if selected_frames else "No frames available; structured from transcript intervals only."
    ]

    record = VideoEvidenceRecord(
        video_id=vid,
        source_access_mode=access_state,
        source_url=source_url,
        transcript_intervals=segments,
        acquisition_method="supplied_or_extracted_adapter",
        frame_records=selected_frames,
        concept_alignment=[{"segment_id": a["segment"]["segment_id"], "frames": [f["local_path"] for f in a["frames"]]} for a in aligned],
        confidence="medium" if uncertain_notes or access_state == "transcript_only" else "high",
        uncertainty_notes=list(dict.fromkeys(uncertain_notes)),
        provenance_separation={
            "presenter_supported": presenter_claims,
            "explanatory_reconstruction": added_reconstruction,
        },
    )

    lines = [
        f"# {title}",
        "",
        "> [!info] Source & Access Context",
        f"> **Access Mode:** `{access_state}` | **Source:** {source_url or 'Local media/transcript'}",
    ]
    if access_state == "transcript_only":
        lines.append("> **Visual Limitation:** Produced strictly from transcript intervals; zero video frames were inspected or claimed.")
    if uncertain_notes:
        lines.append(f"> **Uncertain Regions Preserved:** {'; '.join(dict.fromkeys(uncertain_notes))}")
    lines.append("")

    for idx, bundle in enumerate(aligned, 1):
        seg = bundle["segment"]
        ts_link = format_timestamp_link(source_url, seg["start_s"]) if source_url else f"`{seg['start_s'] // 60:02d}:{seg['start_s'] % 60:02d}`"
        lines.append(f"## Concept Segment {idx} ({ts_link})")
        lines.append("")
        if seg["text"]:
            lines.append(f"**Presenter explanation ({ts_link}):** {seg['text']}")
            lines.append("")
        for frm in bundle["frames"]:
            lines.append(f"**What to look for ({frm['selection_reason']}):** Inspect the visual state captured at timestamp `{frm['timestamp_s']}s`.")
            lines.append("")
            lines.append(f"![[{frm['local_path']}]]")
            lines.append("")
            if frm["visible_elements"]:
                lines.append(f"*Visible details:* {'; '.join(frm['visible_elements'])}.")
            if frm["ocr_uncertain"]:
                lines.append(f"*Uncertain visual reading (preserved as uncertain):* {'; '.join(frm['ocr_uncertain'])}.")
            lines.append("")

    if equations:
        from scriptorium.engines import mathematics

        lines.append("## Key Equations and Step-by-Step Breakdown")
        lines.append("")
        for eq in equations:
            if not isinstance(eq, dict):
                continue
            spec = dict(eq)
            if not spec.get("equation") and spec.get("latex"):
                spec["equation"] = spec.pop("latex")
            if not spec.get("equation"):
                continue
            learner_lvl = str(spec.pop("learner_level", "beginner") or "beginner")
            rendered_eq = mathematics.render_formula_component(
                spec,
                learner_level=learner_lvl,
            )
            lines.append(rendered_eq["markdown"])
            lines.append("")

    concepts = [
        ConceptPlanRecord(
            concept_id=f"{cslug}-{bundle['segment']['segment_id']}",
            canonical_name=f"{title} — Segment {i}",
            learning_objective=f"Explain presenter segment {i} grounded in timestamp {bundle['segment']['start_s']}s.",
            evidence_refs=[source_url or vid],
            visual_requirements=[f["local_path"] for f in bundle["frames"]],
        )
        for i, bundle in enumerate(aligned, 1)
    ]

    return {
        "video_id": vid,
        "access_state": access_state,
        "record": record,
        "assets": assets,
        "concepts": concepts,
        "capabilities": caps,
        "screened_frames": screened,
        "markdown": "\n".join(lines).strip() + "\n",
    }
