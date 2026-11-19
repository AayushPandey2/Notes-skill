"""Isolated compatibility adapter for legacy outlines and historical v1/v2 saved plans.

New adaptive deep-note generation must use scripts/instructional_plan.py directly
and must never silently fall back to this module.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from instructional_plan import normalize_plan, registry

LEGACY_WARNING = (
    "Adapted through legacy_contract_adapter from historical outline/plan fields; "
    "author a structured instructional_plan (contract_version 3) for new deep-note generation."
)


def from_legacy(item: dict[str, Any], contract: dict[str, Any] | None = None) -> dict[str, Any]:
    """Convert legacy outline fields (purpose, math_level 0-3, code_depth) into a minimal normalized plan.

    Strictly reserved for backward-compatible legacy plan adaptation.
    """
    contract = contract or {}
    purpose = str(item.get("purpose") or "explain").strip().lower()
    objective = {"reference": "recognize", "practice": "apply", "revise": "recognize", "definition": "define"}.get(
        purpose, purpose
    )
    reg = registry()
    if objective not in reg["objectives"]:
        objective = "explain"

    raw_level = item.get("math_level", contract.get("math_level", 0))
    level = raw_level if isinstance(raw_level, int) and 0 <= raw_level <= 3 else 0
    objectives = [objective]
    if level >= 2:
        objectives.append("prove" if level == 3 else "derive")

    code_depth = contract.get("code_depth", "none")
    req_lang = str(item.get("language") or contract.get("language") or "none").strip().lower()
    impl_stack = item.get("implementation_stack") or contract.get("implementation_stack") or []
    has_code = code_depth not in {"none", "pseudocode"} or bool(impl_stack) or req_lang not in {"", "none"}
    code = 3 if has_code else (1 if code_depth == "pseudocode" else 0)
    if code >= 2 and "implement" not in objectives:
        objectives.append("implement")

    types = ["mathematical"] if level else ["conceptual"]
    if code >= 2 and "programming" not in types:
        types.append("programming")

    math_depth = (0, 3, 4, 5)[level]
    if item.get("math_level") is None:
        math_depth = max(math_depth, *(reg["objectives"][o].get("math", 0) for o in objectives))

    visual_mod = contract.get("visual_modality", "none")
    visual_depth = 3 if visual_mod == "diagram-image" else 0
    visualizations = (
        [{"type": "geometric_diagram", "purpose": "Legacy spatial/diagram visual", "placement": "inline"}]
        if visual_depth
        else []
    )
    primary_tool = (impl_stack[0] if impl_stack else req_lang) if code >= 2 else "none"
    implementation = (
        {
            "required": True,
            "language": "python" if primary_tool in {"python-numpy", "scikit-learn", "pytorch", "tensorflow-keras"} else primary_tool,
            "framework": primary_tool,
            "approach": "from_scratch" if code >= 4 else "complete",
            "reason": "Adapted from legacy implementation fields.",
        }
        if code >= 2
        else {"required": False}
    )

    plan = normalize_plan(
        {
            "audience": "beginner",
            "source_policy": "independent",
            "concepts": [
                {
                    "id": "core",
                    "title": item.get("title") or "Core concept",
                    "types": types,
                    "objectives": list(dict.fromkeys(objectives)),
                    "depth": {"math": math_depth, "code": code, "visual": visual_depth},
                    "implementation": implementation,
                    "visualizations": visualizations,
                    "reason": LEGACY_WARNING,
                }
            ],
        }
    )
    plan["legacy_adapted"] = True
    plan["compatibility_warning"] = LEGACY_WARNING
    return plan


def adapt_legacy_contract(item: dict[str, Any], legacy_contract: dict[str, Any]) -> dict[str, Any]:
    """Wrap a legacy v1/v2 contract dict into a normalized compatibility contract."""
    adapted = deepcopy(legacy_contract)
    plan = from_legacy(item, adapted)
    depths = {key: max(c["depth"][key] for c in plan["concepts"]) for key in ("math", "code", "visual")}
    adapted.update(
        {
            "contract_version": 2,
            "legacy_adapted": True,
            "compatibility_warning": LEGACY_WARNING,
            "instructional_plan": plan,
            "math_level": (0, 0, 1, 1, 2, 3)[depths["math"]],
            "require_math_floor": False,
            "max_qa_items": None,
        }
    )
    return adapted
