"""Semantic representation registry: families share bounded, reusable backends.

Availability describes execution in this package, not installed host tools.
Native Mermaid is validated source; it is never reported as a rendered bitmap.
"""
from __future__ import annotations

from html import escape
import json
import math
import re
import textwrap
import xml.etree.ElementTree as ET

FAMILIES = {
    "R1": {"name": "mathematical-geometric", "backends": ["scientific", "coordinates", "svg", "table"]},
    "R2": {"name": "scientific-statistical", "backends": ["scientific", "coordinates", "table"]},
    "R3": {"name": "engineering-physical", "backends": ["graph", "scientific", "coordinates", "svg", "table"]},
    "R4": {"name": "ai-ml", "backends": ["svg", "mask", "graph", "scientific", "table"]},
    "R5": {"name": "computer-science", "backends": ["graph", "mermaid", "svg", "table", "interactive"]},
    "R6": {"name": "data-analytics", "backends": ["scientific", "table", "graph"]},
    "R7": {"name": "graphs-networks", "backends": ["graph", "mermaid", "table"]},
    "R8": {"name": "spatial-structural", "backends": ["coordinates", "graph", "table"]},
    "R9": {"name": "research-evidence", "backends": ["external", "scientific", "graph", "table"]},
    "R10": {"name": "interactive-simulation", "backends": ["interactive"]},
    "R11": {"name": "external-media", "backends": ["external", "imagegen"]},
    "R12": {"name": "structured-tables", "backends": ["table"]},
}
KINDS = {
    "equation": ("scientific", "R1"), "distribution": ("scientific", "R2"),
    "workflow": ("mermaid", "R5"), "dependency": ("mermaid", "R7"), "state": ("mermaid", "R5"),
    "tensor": ("svg", "R4"), "architecture": ("svg", "R5"), "mask": ("mask", "R4"),
    "source_figure": ("external", "R11"), "intuition": ("imagegen", "R11"), "hybrid": ("hybrid", "R7"),
    "geometry": ("coordinates", "R1"), "spatial": ("coordinates", "R8"),
    "signal": ("scientific", "R3"), "timeseries": ("scientific", "R6"),
    "network": ("graph", "R7"), "circuit": ("graph", "R3"), "algorithm": ("graph", "R5"),
    "chronology": ("graph", "R7"), "research": ("graph", "R9"),
    "interactive": ("interactive", "R10"), "table": ("table", "R12"),
}
BUILTIN_BACKENDS = frozenset({"scientific", "svg", "mask", "coordinates", "graph", "mermaid", "table", "interactive", "external"})
BACKENDS = {
    "scientific": {"inputs": ["named numeric series or safe equation/grid", "axis labels", "units"], "suffix": "svg", "verification": "finite data, equation agreement and exact SVG regeneration", "fallbacks": ["table"]},
    "svg": {"inputs": ["validated information flow or illustrative components"], "suffix": "svg", "verification": "flow contract or labeled interfaces; safe SVG regeneration", "fallbacks": ["table"]},
    "mask": {"inputs": ["flow mask segments and permissions"], "suffix": "svg", "verification": "same boolean permission matrix as flow validator", "fallbacks": ["table"]},
    "coordinates": {"inputs": ["labeled finite x/y nodes", "edges", "units"], "suffix": "svg", "verification": "equal axis scale and exact SVG regeneration", "fallbacks": ["table"]},
    "graph": {"inputs": ["bounded labeled nodes", "known directed edges"], "suffix": "svg", "verification": "topology ownership and exact safe SVG regeneration", "fallbacks": ["mermaid", "table"]},
    "mermaid": {"inputs": ["bounded labeled nodes", "known directed edges"], "suffix": "mmd", "verification": "safe generated source; host visual rendering pending", "fallbacks": ["svg with explicit flow", "graph"]},
    "table": {"inputs": ["typed columns and rows", "objective", "interpretation"], "suffix": "txt", "verification": "complete comparable cells and exact regeneration", "fallbacks": []},
    "interactive": {"inputs": ["2–200 labeled textual frames"], "suffix": "html", "verification": "fixed program, CSP, escaped data and exact regeneration; host execution pending", "fallbacks": ["table"]},
    "external": {"inputs": ["direct HTTPS PNG or explicit offline fallback", "source", "rights", "alt", "relevance"], "suffix": "png", "verification": "HTTPS acquisition receipt, bounded full supported PNG decode and snapshot hash", "fallbacks": ["explicit local PNG"]},
    "imagegen": {"inputs": ["illustrative prompt", "available host adapter"], "suffix": "png", "verification": "host execution and editorial inspection required", "fallbacks": ["graph", "table"]},
}
for _backend, _contract in BACKENDS.items():
    _contract.update(domains=[family["name"] for family in FAMILIES.values() if _backend in family["backends"]],
                     dependencies=["Python standard library"] if _backend != "imagegen" else ["host image-generation tool"],
                     failure="persist explicit failure; required artifact blocks completion",
                     fallback_policy="explicit semantic alternative only; never silently substitute")
NS = "http://www.w3.org/2000/svg"


def select_representation(requirement: dict, *, available: set[str]) -> dict:
    if not requirement.get("objective") or requirement.get("kind") not in KINDS:
        raise ValueError("Visual needs a learning objective and supported relationship")
    renderer, default_family = KINDS[requirement["kind"]]
    family = requirement.get("family", default_family)
    if family not in FAMILIES:
        family = next((k for k, value in FAMILIES.items() if value["name"] == family), family)
    if family not in FAMILIES or renderer != "hybrid" and renderer not in FAMILIES[family]["backends"]:
        raise ValueError("Representation family does not support the selected backend")
    if renderer == "scientific" and not (requirement.get("equation") or requirement.get("data")):
        raise ValueError("Scientific visual requires an equation or reproducible data")
    if renderer == "external" and not all(requirement.get(k) for k in ("source", "url", "rights")):
        raise ValueError("External figure needs source, URL, and usage rights")
    return {**requirement, "renderer": renderer, "family": family,
            "status": "planned" if renderer in available else "unavailable", "verification_required": True}


def _nodes(spec):
    nodes, edges = spec.get("nodes", []), spec.get("edges", [])
    if not isinstance(nodes,list) or not isinstance(edges,list) or not nodes or len(nodes) > 100 or len(edges) > 300:
        raise ValueError("Graph requires 1-100 nodes and at most 300 edges")
    if any(not isinstance(node,dict) for node in nodes):
        raise ValueError("Graph nodes must be semantic objects")
    ids = [node.get("id") for node in nodes]
    if any(not isinstance(i, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", i) for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("Graph node identifiers must be unique safe identifiers")
    if any(not isinstance(n.get("label"), str) or not n["label"].strip() or len(n["label"]) > 120 for n in nodes):
        raise ValueError("Graph nodes need bounded nonempty labels")
    if any(not isinstance(e, dict) or e.get("source") not in ids or e.get("target") not in ids for e in edges):
        raise ValueError("Graph edges must reference known nodes")
    if any(e["source"]==e["target"] for e in edges):
        raise ValueError("Self-loop diagrams require a loop-capable host adapter")
    return nodes, edges


def graph_svg(spec: dict) -> str:
    """Directed topology diagram; edge data are preserved, not a physical simulator."""
    nodes, edges = _nodes(spec)
    columns = min(4, len(nodes))
    height = 130 * math.ceil(len(nodes) / columns) + 40
    svg = ET.Element("svg", xmlns=NS, viewBox=f"0 0 {columns*230+40} {height}", role="img")
    ET.SubElement(svg, "title").text = spec["objective"]
    positions = {n["id"]: (30 + i % columns * 230, 30 + i // columns * 130) for i, n in enumerate(nodes)}
    for edge in edges:
        x1, y1 = positions[edge["source"]]
        x2, y2 = positions[edge["target"]]
        # Arrow tip points to the target center. Draw edges before opaque nodes.
        sx, sy, tx, ty = x1+90, y1+35, x2+90, y2+35
        ET.SubElement(svg, "line", x1=str(sx), y1=str(sy), x2=str(tx), y2=str(ty), stroke="#475569")
        angle = math.atan2(ty-sy, tx-sx)
        boundary = min(90/max(abs(math.cos(angle)),1e-12),35/max(abs(math.sin(angle)),1e-12))
        tipx, tipy = tx-(boundary+2)*math.cos(angle), ty-(boundary+2)*math.sin(angle)
        points = [(tipx, tipy), (tipx-10*math.cos(angle-.5), tipy-10*math.sin(angle-.5)),
                  (tipx-10*math.cos(angle+.5), tipy-10*math.sin(angle+.5))]
        ET.SubElement(svg, "polygon", points=" ".join(f"{x:.2f},{y:.2f}" for x,y in points), fill="#475569")
        if edge.get("label"):
            ET.SubElement(svg, "text", x=str((sx+tx)/2), y=str((sy+ty)/2-10), **{"font-size":"11"}).text = str(edge["label"])
    for node in nodes:
        x, y = positions[node["id"]]
        ET.SubElement(svg, "rect", x=str(x), y=str(y), width="180", height="70", rx="7", fill="#eef3ff", stroke="#245ac6")
        for line_index,line in enumerate(textwrap.wrap(node["label"],width=26)):
            ET.SubElement(svg, "text", x=str(x+8), y=str(y+14+12*line_index), **{"font-size":"12"}).text = line
    return ET.tostring(svg, encoding="unicode")


def coordinate_svg(spec: dict) -> str:
    points, edges = _nodes(spec)
    if not spec.get("units"):
        raise ValueError("Coordinate diagrams need explicit units")
    if any(type(n.get(k)) not in {int,float} or not math.isfinite(n[k]) for n in points for k in ("x","y")):
        raise ValueError("Coordinate nodes require finite x and y")
    xs, ys = [n["x"] for n in points], [n["y"] for n in points]
    # Same scale on both axes preserves angles and distances.
    extent = max(max(xs)-min(xs), max(ys)-min(ys), 1)
    coords = {n["id"]: (60+480*(n["x"]-min(xs))/extent, 560-480*(n["y"]-min(ys))/extent) for n in points}
    svg = ET.Element("svg", xmlns=NS, viewBox="0 0 640 620", role="img")
    ET.SubElement(svg,"title").text = spec["objective"]
    ET.SubElement(svg,"text", x="10", y="25").text = f"Equal axis scale; units: {spec['units']}"
    for e in edges:
        (x1,y1),(x2,y2) = coords[e["source"]],coords[e["target"]]
        ET.SubElement(svg,"line", x1=str(x1), y1=str(y1), x2=str(x2), y2=str(y2),stroke="#245ac6")
    for n in points:
        x,y = coords[n["id"]]
        ET.SubElement(svg,"circle",cx=str(x),cy=str(y),r="4",fill="#245ac6")
        ET.SubElement(svg,"text",x=str(x+7),y=str(y-7), **{"font-size":"12"}).text = f"{n['label']} ({n['x']}, {n['y']})"
    return ET.tostring(svg,encoding="unicode")


def mermaid_source(spec: dict) -> str:
    nodes, edges = _nodes(spec)
    def label(value):
        # Mermaid entity encoding prevents labels introducing directives or statements.
        return "".join(c if c.isalnum() or c in " .,()-_" else f"#{ord(c)};" for c in str(value))
    lines = ["flowchart TD"]
    lines.extend(f'  {n["id"]}["{label(n["label"])}"]' for n in nodes)
    lines.extend(f'  {e["source"]} -->|"{label(e.get("label", ""))}"| {e["target"]}' for e in edges)
    return "\n".join(lines)+"\n"


def interactive_html(spec: dict) -> str:
    """A constrained state-sequence viewer; never executes supplied JavaScript."""
    frames = spec.get("frames", [])
    if not isinstance(frames,list) or not 2 <= len(frames) <= 200:
        raise ValueError("Interactive sequence needs 2-200 supplied frames")
    if any(not isinstance(f,dict) or not isinstance(f.get("label"),str) or not isinstance(f.get("state"),str)
           or len(f["state"]) > 10000 for f in frames):
        raise ValueError("Frames require bounded textual label and state")
    data = json.dumps(frames, ensure_ascii=True).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    script = ("const frames="+data+";const slider=document.getElementById('step');"
              "function show(){const f=frames[Number(slider.value)];document.getElementById('label').textContent=f.label;"
              "document.getElementById('state').textContent=f.state;}slider.addEventListener('input',show);show();")
    import base64,hashlib
    digest = base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
    return ("<!doctype html><html><head><meta charset='utf-8'>"
            f'<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'sha256-{digest}\'; base-uri \'none\'">'
            f"<title>{escape(spec['objective'])}</title></head><body><h1>{escape(spec['objective'])}</h1>"
            f"<label>Step <input id='step' type='range' min='0' max='{len(frames)-1}' value='0'></label>"
            f"<h2 id='label'></h2><pre id='state'></pre><script>{script}</script></body></html>")
