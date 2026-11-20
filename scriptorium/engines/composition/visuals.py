"""Deterministic SVG figures for E4; all numbers come from supplied data.

Uses standard-library XML. Mermaid is emitted natively by the MOC renderer;
external figures and conceptual image generation remain host tool adapters.
"""
from __future__ import annotations

import math
import json
from pathlib import Path
import time
import xml.etree.ElementTree as ET

from scriptorium.models import content_hash

NS = "http://www.w3.org/2000/svg"


def scientific_svg(series: dict[str, list[tuple[float, float]]], *, title: str, xlabel: str, ylabel: str) -> str:
    if not series or any(len(points) < 2 for points in series.values()):
        raise ValueError("Each series requires at least two points")
    points = [p for values in series.values() for p in values]
    if any(not math.isfinite(v) for p in points for v in p):
        raise ValueError("Scientific plot contains nonfinite data")
    xmin, xmax = min(x for x, _ in points), max(x for x, _ in points)
    ymin, ymax = min(y for _, y in points), max(y for _, y in points)
    if xmin == xmax or ymin == ymax:
        raise ValueError("Plot needs nonzero axis ranges")
    svg = ET.Element("svg", xmlns=NS, viewBox="0 0 720 440", role="img")
    ET.SubElement(svg, "title").text = title
    ET.SubElement(svg, "rect", x="0", y="0", width="720", height="440", fill="white")
    def label(x, y, text):
        ET.SubElement(svg, "text", x=str(x), y=str(y), fill="#172033", **{"font-size": "14"}).text = text
    label(70, 24, title)
    ET.SubElement(svg, "path", d="M70 50 V360 H680", fill="none", stroke="#172033")
    label(300, 428, xlabel)
    label(5, 44, ylabel)
    for i in range(6):
        x = xmin + (xmax - xmin) * i / 5
        y = ymin + (ymax - ymin) * i / 5
        label(70 + i * 122, 385, f"{x:.3g}")
        label(5, 360 - i * 62, f"{y:.3g}")
    colors = ["#245ac6", "#b93b26", "#08795c", "#7434aa"]
    for i, (name, values) in enumerate(series.items()):
        coords = " ".join(f"{70+(x-xmin)/(xmax-xmin)*610:.4f},{360-(y-ymin)/(ymax-ymin)*310:.4f}" for x, y in values)
        ET.SubElement(svg, "polyline", points=coords, fill="none", stroke=colors[i % len(colors)], **{"stroke-width": "2"})
        label(90 + i * 150, 405, name)
    return ET.tostring(svg, encoding="unicode")


def architecture_svg(components: list[dict[str, str]]) -> str:
    if not components or any(not c.get("label") or not c.get("shape") for c in components):
        raise ValueError("Each component requires a label and tensor shape or interface")
    width = 220 * len(components)
    svg = ET.Element("svg", xmlns=NS, viewBox=f"0 0 {width} 160", role="img")
    ET.SubElement(svg, "title").text = "Ordered architecture and interfaces"
    for i, component in enumerate(components):
        x = i * 220 + 10
        ET.SubElement(svg, "rect", x=str(x), y="30", width="180", height="90", rx="8", fill="#eef3ff", stroke="#245ac6")
        for y, field in ((60, "label"), (90, "shape")):
            ET.SubElement(svg, "text", x=str(x + 8), y=str(y), **{"font-size": "13"}).text = component[field]
        if i + 1 < len(components):
            ET.SubElement(svg, "path", d=f"M{x+180} 75 h35 l-6 -5 m6 5 l-6 5", fill="none", stroke="#172033")
    return ET.tostring(svg, encoding="unicode")


def validate_svg(text: str) -> list[str]:
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return [f"Invalid XML: {exc}"]
    errors = []
    if root.tag != f"{{{NS}}}svg" or not root.get("viewBox"):
        errors.append("SVG needs namespace and viewBox")
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] in {"script", "foreignObject"}:
            errors.append("Unsupported active SVG content")
        if any(k.lower().startswith("on") or k.endswith("href") for k in element.attrib):
            errors.append("Unsupported SVG event or external resource")
    return errors


def mask_svg(mask: list[list[bool]], segments: list[dict]) -> str:
    """Show the same boolean matrix used by the information-flow verifier."""
    size = len(mask)
    if not size or any(len(row) != size for row in mask):
        raise ValueError("Mask heatmap requires a nonempty square token context")
    svg = ET.Element("svg", xmlns=NS, viewBox=f"0 0 {size*28+180} {size*28+120}", role="img")
    ET.SubElement(svg, "title").text = "Attention permissions: rows=query, columns=key; blue=allowed"
    ET.SubElement(svg, "rect", width="100%", height="100%", fill="white")
    for i, row in enumerate(mask):
        for j, allowed in enumerate(row):
            ET.SubElement(svg, "rect", x=str(100+j*28), y=str(60+i*28), width="27", height="27",
                          fill="#245ac6" if allowed else "#eeeeee")
    tokens = [f"{s['id']}:{i}" for s in segments for i in range(s["length"])]
    for i, label in enumerate(tokens):
        ET.SubElement(svg, "text", x="4", y=str(78+i*28), **{"font-size": "10"}).text = f"q {label}"
        ET.SubElement(svg, "text", x=str(100+i*28), y="45", **{"font-size": "9"}).text = f"k{i}"
    ET.SubElement(svg, "text", x="10", y=str(size*28+95), **{"font-size": "11"}).text = "Blue: allowed. Gray: forbidden. Keys use global zero-based positions."
    return ET.tostring(svg, encoding="unicode")


def flow_svg(flow: dict) -> str:
    from .checks import check_flow
    errors = check_flow(flow)
    if errors:
        raise ValueError("; ".join(errors))
    branches = flow["branches"]
    svg = ET.Element("svg", xmlns=NS, viewBox=f"0 0 900 {80+len(branches)*120}", role="img")
    ET.SubElement(svg, "title").text = "Validated computational branches and actual input/output paths"
    ET.SubElement(svg, "rect", width="100%", height="100%", fill="white")
    for i, branch in enumerate(branches):
        y = 55 + i*120
        for x, text in ((10, ", ".join(branch["inputs"])), (300, branch["id"]), (600, ", ".join(branch["outputs"]))):
            ET.SubElement(svg, "rect", x=str(x), y=str(y), width="260", height="55", fill="#eef3ff", stroke="#245ac6")
            ET.SubElement(svg, "text", x=str(x+8), y=str(y+30), **{"font-size": "12"}).text = text
        for x in (270, 560):
            ET.SubElement(svg, "path", d=f"M{x} {y+27} h29 l-6 -5 m6 5 l-6 5", fill="none", stroke="#172033")
        ET.SubElement(svg, "text", x="300", y=str(y+76), **{"font-size": "11"}).text = (
            f"readout={branch['readout']}; gradient={branch['gradient_owner']}; forbidden={','.join(branch['forbidden'])}")
    return ET.tostring(svg, encoding="unicode")


def render_visuals(vault: Path, plan: dict, drafts: dict[str, str], *, execute: bool = True) -> tuple[dict, dict]:
    """Persist every attempt, even failures. Cache immutable SVGs by specification and renderer code."""
    from . import contained, select_visual
    from .contracts import insert_at_section
    from .checks import arithmetic, attention_mask, check_flow
    from ..vault import safe_write_note
    bodies, results = dict(drafts), {}
    render_version = content_hash(Path(__file__).read_bytes())
    for visual in plan["visuals"]:
        started = time.perf_counter()
        selected = select_visual(visual, available={"scientific", "svg", "mask"})
        renderer = selected["renderer"]
        fallback = visual.get("fallback")
        if renderer == "mermaid" and fallback == "svg" and visual.get("flow"):
            renderer = "svg"
        digest = content_hash(json.dumps({"spec": visual, "renderer": renderer, "version": render_version}, sort_keys=True))
        relative = f"assets/scriptorium/{digest}.svg"
        path = contained(vault, relative)
        status = {"renderer": renderer, "selected_renderer": selected["renderer"], "available": renderer in {"scientific", "svg", "mask"},
                  "attempted": False, "status": "planned", "input_hash": digest, "path": relative, "hash": None,
                  "failure_reason": None, "fallback": fallback, "renderer_version": render_version, "cached": False}
        chapter = next(c for c in plan["chapters"] if visual["concept"] in c["concepts"])
        try:
            if not status["available"]:
                raise ValueError("Renderer requires a host execution adapter; selection is not execution")
            status["attempted"] = True
            if renderer == "scientific":
                if not all(visual.get(k) for k in ("xlabel", "ylabel", "units", "interpretation")):
                    raise ValueError("Scientific plot requires axis labels, units and interpretation")
                series = visual.get("data")
                if series is None and visual.get("equation") and visual.get("x_values"):
                    series = {visual.get("label", visual["equation"]): [(x, arithmetic(visual["equation"], {"x": x, **visual.get("parameters", {})}))
                                                                       for x in visual["x_values"]]}
                if not isinstance(series, dict):
                    raise ValueError("Scientific plot needs reproducible named series")
                if visual.get("equation"):
                    for points in series.values():
                        for x, y in points:
                            if not math.isclose(y, arithmetic(visual["equation"], {"x": x, **visual.get("parameters", {})}), rel_tol=1e-9, abs_tol=1e-12):
                                raise ValueError("Scientific series disagrees with the claimed equation")
                if visual.get("empirical") and not visual.get("verified_comparable_claims"):
                    raise ValueError("Empirical chart requires verified comparable claim IDs")
                if visual.get("error_bars"):
                    raise ValueError("This deterministic renderer does not support error bars; select a capable scientific backend")
                svg = scientific_svg(series, title=visual["objective"], xlabel=visual["xlabel"], ylabel=visual["ylabel"])
            elif renderer == "mask":
                flow = visual["flow"]
                if check_flow(flow):
                    raise ValueError("Mask diagram contradicts the information-flow contract")
                mask = flow["mask"]
                svg = mask_svg(attention_mask(mask["segments"], mask["permissions"], causal=mask["causal"]), mask["segments"])
            else:
                if not visual.get("flow"):
                    raise ValueError("Architecture SVG requires a validated information-flow contract")
                svg = flow_svg(visual["flow"])
            issues = validate_svg(svg)
            if issues:
                raise ValueError("; ".join(issues))
            if execute:
                if path.exists():
                    if path.read_text(encoding="utf-8") != svg:
                        raise ValueError("Content-addressed visual was altered; repair the asset before reusing it")
                    status["cached"] = True
                else:
                    safe_write_note(path, svg, validate_properties=False)
            elif not path.is_file() or path.read_text(encoding="utf-8") != svg:
                raise ValueError("Rendered asset is missing or changed")
            status.update(status="verified", hash=content_hash(svg), validation={
                "method": "regenerate from numerical inputs or verified flow/mask and compare exact SVG",
                "result": "pass", "limits": "Visual semantics are checked against supplied contracts; browser/theme rendering is untested."})
            embed = f"![[{relative}]]"
            if embed not in bodies.get(chapter["id"], ""):
                bodies[chapter["id"]] = insert_at_section(bodies.get(chapter["id"], ""), visual["section"],
                                                         embed + "\n\n" + visual.get("interpretation", visual["objective"]))
        except (ValueError, KeyError, TypeError, OSError, ArithmeticError) as exc:
            status.update(status="failed" if status["available"] else "unavailable", failure_reason=str(exc))
        status["elapsed_seconds"] = time.perf_counter()-started
        results[visual["id"]] = status
    return bodies, results
