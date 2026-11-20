"""Deterministic SVG figures for E4; all numbers come from supplied data.

Uses standard-library XML. Mermaid is emitted natively by the MOC renderer;
external figures and conceptual image generation remain host tool adapters.
"""
from __future__ import annotations

import math
import xml.etree.ElementTree as ET

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
