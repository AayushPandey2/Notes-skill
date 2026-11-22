"""Semantic representation registry: web-image-first external acquisition plus native Mermaid, tables, and constrained interactive frames.

Programmatic SVG diagram generation has been retired. Visual educational diagrams
and figures must be discovered via web image research, evaluated for accessibility
and licensing, downloaded locally, inspected, and explained in prose.
"""
from __future__ import annotations

from html import escape
import json
import re
from typing import Any

FAMILIES = {
    "R1": {"name": "mathematical-geometric", "backends": ["external", "table"]},
    "R2": {"name": "scientific-statistical", "backends": ["external", "table"]},
    "R3": {"name": "engineering-physical", "backends": ["external", "mermaid", "table"]},
    "R4": {"name": "ai-ml", "backends": ["external", "mermaid", "table"]},
    "R5": {"name": "computer-science", "backends": ["external", "mermaid", "table", "interactive"]},
    "R6": {"name": "data-analytics", "backends": ["external", "table"]},
    "R7": {"name": "graphs-networks", "backends": ["external", "mermaid", "table"]},
    "R8": {"name": "spatial-structural", "backends": ["external", "table"]},
    "R9": {"name": "research-evidence", "backends": ["external", "table"]},
    "R10": {"name": "interactive-simulation", "backends": ["interactive"]},
    "R11": {"name": "external-media", "backends": ["external"]},
    "R12": {"name": "structured-tables", "backends": ["table"]},
}

KINDS = {
    "equation": ("external", "R1"),
    "distribution": ("external", "R2"),
    "workflow": ("mermaid", "R5"),
    "dependency": ("mermaid", "R7"),
    "state": ("mermaid", "R5"),
    "tensor": ("external", "R4"),
    "architecture": ("external", "R5"),
    "mask": ("external", "R4"),
    "source_figure": ("external", "R11"),
    "intuition": ("external", "R11"),
    "hybrid": ("hybrid", "R7"),
    "geometry": ("external", "R1"),
    "spatial": ("external", "R8"),
    "signal": ("external", "R3"),
    "timeseries": ("external", "R6"),
    "network": ("external", "R7"),
    "circuit": ("external", "R3"),
    "algorithm": ("external", "R5"),
    "chronology": ("external", "R7"),
    "research": ("external", "R9"),
    "interactive": ("interactive", "R10"),
    "table": ("table", "R12"),
}

RETIRED_SVG_BACKENDS = frozenset({"svg", "mask", "coordinates", "graph", "scientific", "imagegen"})
BUILTIN_BACKENDS = frozenset({"external", "mermaid", "table", "interactive"})

BACKENDS = {
    "external": {
        "inputs": ["web image search queries or verified direct HTTPS image URL / local asset", "source", "rights", "alt", "relevance"],
        "suffix": "png",
        "verification": "web image discovery, permissive rights check, bounded decode/inspection, local asset snapshot hash",
        "fallbacks": ["explicit unmet visual obligation notice"],
    },
    "mermaid": {
        "inputs": ["bounded labeled nodes", "known directed edges"],
        "suffix": "mmd",
        "verification": "safe generated Mermaid flowchart syntax; Obsidian client rendering separate",
        "fallbacks": ["table"],
    },
    "table": {
        "inputs": ["typed columns and rows", "objective", "interpretation"],
        "suffix": "txt",
        "verification": "complete comparable cells and exact regeneration",
        "fallbacks": [],
    },
    "interactive": {
        "inputs": ["2–200 labeled textual frames"],
        "suffix": "html",
        "verification": "fixed program, CSP, escaped data and exact regeneration; host execution pending",
        "fallbacks": ["table"],
    },
}

for _backend, _contract in BACKENDS.items():
    _contract.update(
        domains=[family["name"] for family in FAMILIES.values() if _backend in family["backends"]],
        dependencies=["Python standard library"],
        failure="persist explicit failure or unmet visual obligation; never silently generate programmatic SVG",
        fallback_policy="explicit semantic alternative only (never programmatic diagram drawing)",
    )


def select_representation(requirement: dict[str, Any], *, available: set[str]) -> dict[str, Any]:
    """Select an active non-SVG representation backend for a visual requirement."""
    explicit_renderer = requirement.get("renderer")
    if explicit_renderer in RETIRED_SVG_BACKENDS:
        raise ValueError(
            f"Programmatic image generation backend '{explicit_renderer}' has been removed; "
            "use web image discovery ('external'), 'mermaid', or 'table'."
        )
    if not requirement.get("objective") or requirement.get("kind") not in KINDS:
        raise ValueError("Visual needs a learning objective and supported relationship")

    renderer, default_family = KINDS[requirement["kind"]]
    if explicit_renderer and explicit_renderer in BUILTIN_BACKENDS:
        renderer = explicit_renderer
    family = requirement.get("family", default_family)
    if family not in FAMILIES:
        family = next((k for k, value in FAMILIES.items() if value["name"] == family), family)
    if family not in FAMILIES or (renderer != "hybrid" and renderer not in FAMILIES[family]["backends"]):
        raise ValueError("Representation family does not support the selected backend")

    if renderer == "external":
        has_supplied = all(requirement.get(k) for k in ("source", "url", "rights"))
        has_search_intent = bool(requirement.get("search_queries") or requirement.get("research_required") or requirement.get("local_fallback"))
        if requirement["kind"] == "source_figure" and not (has_supplied or has_search_intent):
            raise ValueError("Source figure needs source, URL, and usage rights, or search_queries for web image discovery")

    return {
        **requirement,
        "renderer": renderer,
        "family": family,
        "status": "planned" if renderer in available else "unavailable",
        "verification_required": True,
    }


def _nodes(spec: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    nodes, edges = spec.get("nodes", []), spec.get("edges", [])
    if not isinstance(nodes, list) or not isinstance(edges, list) or not nodes or len(nodes) > 100 or len(edges) > 300:
        raise ValueError("Graph requires 1-100 nodes and at most 300 edges")
    if any(not isinstance(node, dict) for node in nodes):
        raise ValueError("Graph nodes must be semantic objects")
    ids = [node.get("id") for node in nodes]
    if any(not isinstance(i, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", i) for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("Graph node identifiers must be unique safe identifiers")
    if any(not isinstance(n.get("label"), str) or not n["label"].strip() or len(n["label"]) > 120 for n in nodes):
        raise ValueError("Graph nodes need bounded nonempty labels")
    if any(not isinstance(e, dict) or e.get("source") not in ids or e.get("target") not in ids for e in edges):
        raise ValueError("Graph edges must reference known nodes")
    if any(e["source"] == e["target"] for e in edges):
        raise ValueError("Self-loop diagrams require a loop-capable host adapter")
    return nodes, edges


def mermaid_source(spec: dict[str, Any]) -> str:
    """Emit sanitized native Mermaid flowchart source for Obsidian."""
    nodes, edges = _nodes(spec)

    def label(value: Any) -> str:
        # Mermaid entity encoding prevents labels introducing directives or statements.
        return "".join(c if c.isalnum() or c in " .,()-_" else f"#{ord(c)};" for c in str(value))

    lines = ["flowchart TD"]
    lines.extend(f'  {n["id"]}["{label(n["label"])}"]' for n in nodes)
    lines.extend(f'  {e["source"]} -->|"{label(e.get("label", ""))}"| {e["target"]}' for e in edges)
    return "\n".join(lines) + "\n"


def interactive_html(spec: dict[str, Any]) -> str:
    """A constrained textual state-sequence viewer; never executes supplied JavaScript."""
    frames = spec.get("frames", [])
    if not isinstance(frames, list) or not 2 <= len(frames) <= 200:
        raise ValueError("Interactive sequence needs 2-200 supplied frames")
    if any(
        not isinstance(f, dict)
        or not isinstance(f.get("label"), str)
        or not isinstance(f.get("state"), str)
        or len(f["state"]) > 10000
        for f in frames
    ):
        raise ValueError("Frames require bounded textual label and state")
    data = json.dumps(frames, ensure_ascii=True).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    script = (
        "const frames=" + data + ";const slider=document.getElementById('step');"
        "function show(){const f=frames[Number(slider.value)];document.getElementById('label').textContent=f.label;"
        "document.getElementById('state').textContent=f.state;}slider.addEventListener('input',show);show();"
    )
    import base64
    import hashlib

    digest = base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f'<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'sha256-{digest}\'; base-uri \'none\'">'
        f"<title>{escape(spec['objective'])}</title></head><body><h1>{escape(spec['objective'])}</h1>"
        f"<label>Step <input id='step' type='range' min='0' max='{len(frames)-1}' value='0'></label>"
        f"<h2 id='label'></h2><pre id='state'></pre><script>{script}</script></body></html>"
    )
