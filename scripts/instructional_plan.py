"""Validate and normalize agent-authored instructional decisions; no model calls."""
from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import json
from pathlib import Path
import re

SOURCE_MODULES = {
    "equation": ("mathematics", "math", 2), "formula": ("mathematics", "math", 2),
    "derivation": ("derivation", "math", 4), "proof": ("proof", "math", 5),
    "figure": ("visualization", "visual", 2), "table": ("visualization", "visual", 2),
    "example": ("examples", "practice", 3), "exercise": ("assessment", "assessment", 3),
    "algorithm": ("algorithm", "theory", 3), "qualification": ("limitations", "theory", 2),
}


@lru_cache(maxsize=1)
def registry():
    return json.loads((Path(__file__).resolve().parent.parent /
                       "references/instructional-registry.json").read_text(encoding="utf-8"))


def _names(value, allowed, field):
    if not isinstance(value, list) or not value or any(not isinstance(v, str) or v not in allowed for v in value):
        raise ValueError(f"{field} must be a nonempty list drawn from {sorted(allowed)}")
    return list(dict.fromkeys(value))


def _text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be nonempty text")
    return value.strip()


def normalize_plan(raw):
    """Resolve objective floors, module dependencies and coverage assignments.

    Classification is supplied by the author from goals and inspected evidence.
    This function deliberately does not infer knowledge types from topic keywords.
    """
    if not isinstance(raw, dict):
        raise ValueError("instructional_plan must be an object")
    result = deepcopy(raw)
    reg = registry()
    audience = result.setdefault("audience", "beginner")
    if audience not in {"beginner", "intermediate", "advanced"}:
        raise ValueError("audience must be beginner, intermediate or advanced")
    policy = result.setdefault("source_policy", "independent")
    if policy not in {"independent", "strict", "expanded", "comparative"}:
        raise ValueError("Unknown source_policy")
    concepts = result.get("concepts")
    if not isinstance(concepts, list) or not concepts:
        raise ValueError("concepts must be a nonempty list")
    ids = []
    for c in concepts:
        if not isinstance(c, dict):
            raise ValueError("Each concept must be an object")
        ident = _text(c.get("id"), "concept id")
        if not re.fullmatch(r"[a-zA-Z0-9][\w-]*", ident) or ident in ids:
            raise ValueError("Concept IDs must be unique identifiers")
        ids.append(ident)
    seen = set()
    for c in concepts:
        _text(c.get("title"), "concept title")
        _text(c.get("reason"), "concept reason")
        c["types"] = _names(c.get("types"), reg["subtemplates"], "types")
        c["objectives"] = _names(c.get("objectives"), reg["objectives"], "objectives")
        prerequisites = c.setdefault("prerequisites", [])
        if not isinstance(prerequisites, list):
            raise ValueError("prerequisites must be a list")
        for dep in prerequisites:
            if not isinstance(dep, dict) or dep.get("treatment") not in {"known", "reminder", "explain", "foundation"}:
                raise ValueError("Each prerequisite needs a concept and treatment")
            target = _text(dep.get("concept"), "prerequisite concept")
            if target in ids and target not in seen:
                raise ValueError("Prerequisites must precede their consumers (cycle or forward dependency)")
        seen.add(c["id"])
        depth = dict.fromkeys(reg["dimensions"], 0)
        for objective in c["objectives"]:
            for dimension, floor in reg["objectives"][objective].items():
                depth[dimension] = max(depth[dimension], floor)
        # Types select explanatory capabilities, never domain-wide math/code ceilings.
        for kind, dimension, floor in (("algorithmic", "theory", 3), ("programming", "code", 2),
                                       ("historical", "theory", 2), ("comparative", "theory", 2),
                                       ("procedural", "practice", 3), ("scientific", "practice", 2),
                                       ("research", "practice", 2)):
            if kind in c["types"]:
                depth[dimension] = max(depth[dimension], floor)
        source_required = set()
        inventory = result.get("sources", [])
        if not isinstance(inventory, list):
            raise ValueError("sources must be a list")
        for source in inventory:
            if isinstance(source, dict) and source.get("required") and c["id"] in (source.get("concepts") or []):
                module, dimension, floor = SOURCE_MODULES.get(source.get("kind"), ("definitions", "theory", 2))
                source_required.add(module)
                depth[dimension] = max(depth[dimension], floor)
        overrides = c.get("depth", {})
        if not isinstance(overrides, dict):
            raise ValueError("depth must be an object")
        for dimension, value in overrides.items():
            if dimension not in depth or type(value) is not int or value not in range(6):
                raise ValueError("Depth dimensions must have integer levels 0 through 5")
            if value < depth[dimension]:
                raise ValueError(f"{c['id']}: {dimension} conflicts with a required objective/type")
            depth[dimension] = value
        c["depth"] = depth
        modules = {}
        for name, spec in reg["modules"].items():
            level = depth[spec["dimension"]]
            required = bool(name in source_required or set(spec["required_for"]) & set(c["objectives"]) or set(spec["types"]) & set(c["types"]))
            status = "required" if required else "supporting" if level and spec["supporting"] else "excluded"
            modules[name] = {"status": status, "depth": level if status != "excluded" else 0,
                             "reason": "objective/type requirement" if required else "supports selected dimension" if status == "supporting" else "no selected need"}
        custom = c.get("modules", {})
        if not isinstance(custom, dict):
            raise ValueError("modules must be an object")
        for name, choice in custom.items():
            if name not in modules or not isinstance(choice, dict):
                raise ValueError(f"Unknown or invalid module: {name}")
            _text(choice.get("reason"), "module override reason")
            status = choice.get("status")
            level = choice.get("depth")
            if status not in {"required", "supporting", "optional", "excluded"} or type(level) is not int or level not in range(6):
                raise ValueError("Module requires a valid status and depth 0 through 5")
            if (status == "excluded") != (level == 0):
                raise ValueError("Only excluded modules have zero depth")
            if level > depth[reg["modules"][name]["dimension"]]:
                raise ValueError("Module depth exceeds its concept dimension; update the profile")
            if modules[name]["status"] == "required" and (status != "required" or level < modules[name]["depth"]):
                raise ValueError("Cannot drop or lower a required module")
            if name == "derivation" and level and level < 4 or name == "proof" and level and level < 5:
                raise ValueError("Derivation needs M4 and proof needs M5")
            modules[name] = {"status": status, "depth": level, "reason": choice["reason"]}
        # Required module dependencies are promoted transitively.
        pending = [name for name, choice in modules.items() if choice["status"] in {"required", "supporting"}]
        visited = set()
        while pending:
            name = pending.pop()
            if name in visited:
                continue
            visited.add(name)
            for dep in reg["modules"][name]["depends"]:
                if dep in custom and modules[dep]["status"] in {"excluded", "optional"}:
                    raise ValueError(f"{name} depends on excluded/deferred module {dep}")
                if modules[dep]["status"] != "required":
                    modules[dep] = {"status": "required", "depth": max(2, depth[reg["modules"][dep]["dimension"]]),
                                    "reason": f"dependency of {name}"}
                    depth[reg["modules"][dep]["dimension"]] = modules[dep]["depth"]
                pending.append(dep)
        c["modules"] = modules
        c["sequence_candidates"] = {kind: reg["subtemplates"][kind] for kind in c["types"]}
        # This is a soft sizing heuristic, not a token counter or output cap.
        c["estimated_output_tokens"] = 180 + 90 * sum(depth.values()) + 120 * sum(
            dep["treatment"] in {"explain", "foundation"} for dep in prerequisites)
    sources = result.setdefault("sources", [])
    if not isinstance(sources, list):
        raise ValueError("sources must be a list")
    if policy != "independent" and not sources:
        raise ValueError("Source-grounded policy requires an element inventory")
    source_ids = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("Source elements must be objects")
        sid = _text(source.get("id"), "source element id")
        if sid in source_ids:
            raise ValueError("Duplicate source element ID")
        source_ids.add(sid)
        for key in ("location", "kind"):
            _text(source.get(key), f"source {key}")
        if source.get("access") not in {"full", "partial", "unavailable"} or type(source.get("required")) is not bool:
            raise ValueError("Source needs access and required boolean")
        if source["required"]:
            _names(source.get("concepts"), ids, "source concept assignments")
        else:
            _text(source.get("reason"), "source omission reason")
    result["version"] = 1
    result["estimated_output_tokens"] = sum(c["estimated_output_tokens"] for c in concepts)
    return result


def from_legacy(item, contract):
    """Adapt preserved outline fields without claiming a semantic classification."""
    purpose = item.get("purpose", "explain")
    objective = {"reference": "recognize", "practice": "apply"}.get(purpose, purpose)
    if objective not in registry()["objectives"]:
        objective = "explain"
    level = contract["math_level"]
    objectives = [objective]
    if level >= 2:
        objectives.append("prove" if level == 3 else "derive")
    code = 3 if contract["code_depth"] != "none" else 0
    if code and objective != "implement":
        objectives.append("implement")
    types = ["mathematical"] if level else ["conceptual"]
    if code:
        types.append("programming")
    math_depth = (0, 3, 4, 5)[level]
    if item.get("math_level") is None:
        math_depth = max(math_depth, *(registry()["objectives"][o].get("math", 0) for o in objectives))
    return normalize_plan({"audience": "beginner", "source_policy": "independent", "concepts": [{
        "id": "core", "title": item.get("title") or "Core concept", "types": types,
        "objectives": list(dict.fromkeys(objectives)), "depth": {"math": math_depth,
            "visual": 3 if contract["visual_modality"] == "diagram-image" else 0},
        "reason": "Adapted from legacy outline; author must refine types and prerequisites from goals and sources."}]})


def coverage_errors(plan, report, draft):
    """Check inventory receipts structurally; the author still verifies evidence."""
    sources = {s["id"]: s for s in plan.get("sources", [])}
    if not sources and report is None:
        return []
    elements = report.get("elements") if isinstance(report, dict) else None
    if not isinstance(elements, list):
        return ["Source coverage requires an elements report"]
    # Mask fenced code so a heading inside an example cannot pass as coverage.
    from note_verification import split_blocks
    _, prose = split_blocks(draft)
    from verify_vault_notes import _heading_slug
    anchors = {_heading_slug(m[1]) for line in prose if (m := re.match(r"^#{1,6}\s+(.+)$", line))}
    receipts = {}
    errors = []
    for receipt in elements:
        if not isinstance(receipt, dict) or not isinstance(receipt.get("id"), str):
            errors.append("Invalid source coverage receipt")
            continue
        sid = receipt["id"]
        if sid not in sources or sid in receipts:
            errors.append(f"Unknown or duplicate source receipt: {sid}")
        receipts[sid] = receipt
        if receipt.get("status") != "validated" or receipt.get("anchor") not in anchors or not isinstance(receipt.get("note"), str) or not receipt["note"].strip():
            errors.append(f"{sid}: coverage needs a validated receipt, actual anchor and check note")
    for sid, source in sources.items():
        if source["required"] and (source["access"] != "full" or sid not in receipts):
            errors.append(f"{sid}: required source element is inaccessible or not validated")
    if plan.get("source_policy") in {"strict", "expanded"}:
        positions = {_heading_slug(m[1]): i for i, line in enumerate(prose) if (m := re.match(r"^#{1,6}\s+(.+)$", line))}
        order = [positions[receipts[sid]["anchor"]] for sid, source in sources.items()
                 if source["required"] and sid in receipts and receipts[sid].get("anchor") in positions]
        if order != sorted(order):
            errors.append("Source order differs from the required inventory sequence")
    return errors
