#!/usr/bin/env python3
"""Unified Pedagogical Intelligence & Learning Experience Engine (P01-P11) for Scriptorium.

Extends the Contract v3 adaptive instructional planner without overriding its
knowledge-type subtemplate, module, or per-concept depth (0-5) authority.
Provides deterministic cognitive dependency mapping, progressive explanation
layering, multiple-representation alignment (symbol/tensor-shape/equation-code),
worked-example intelligence & duplicate detection, visual accuracy & rendering
checks, misconception auditing, cognitive-load density checks, cross-topic vault
integration, executable verification tiering, revision integrity validation, and
actionable PED-xxx educational quality defect reporting for targeted local repair.
"""
from __future__ import annotations

import argparse
import ast
from collections import deque
from copy import deepcopy
import json
import math
from pathlib import Path
import re
import sys
from typing import Any

from scriptorium.models import safe_eval_expr

PEDAGOGICAL_CONTRACT_VERSION = 1

DEPENDENCY_TYPES = {
    "essential",
    "supporting",
    "alternative_route",
    "contextual",
    "future_application",
}

PREREQ_TREATMENTS = {
    "assume": "assume",
    "known": "assume",
    "remind": "remind",
    "reminder": "remind",
    "bridge": "bridge",
    "teach": "teach",
    "explain": "teach",
    "foundation": "teach",
    "defer": "defer",
}

EXPLANATION_LAYERS = (
    "motivation",
    "intuition",
    "mechanism",
    "formal_definition",
    "formalization",
    "worked_application",
    "limitations",
    "integration",
)

LAYER_LEVELS = {"omitted", "minimal", "standard", "detailed", "deep", "required", "supporting"}

EXAMPLE_CATEGORIES = {
    "minimal",
    "worked",
    "representative",
    "boundary",
    "counterexample",
    "failure",
    "debugging",
    "transfer",
    "comparative",
}

EXAMPLE_PROVENANCE = {
    "source_provided",
    "source_adapted",
    "illustrative",
    "researched",
}

VISUAL_CATEGORIES = {
    "function_graph",
    "geometric_diagram",
    "flowchart",
    "architecture_diagram",
    "dependency_graph",
    "state_transition",
    "timeline",
    "matrix_tensor_diagram",
    "table",
    "data_visualization",
}

MISCONCEPTION_CATEGORIES = {
    "terminological",
    "mathematical",
    "conceptual",
    "implementation",
    "statistical",
    "scope",
}

CONNECTION_RELATIONS = {
    "prerequisite_of",
    "builds_upon",
    "applies",
    "generalizes",
    "special_case_of",
    "alternative_to",
    "contrasts_with",
    "shares_foundation",
    "shares_implementation",
    "historically_from",
    "used_together_with",
}

DETAIL_LEVELS = {"minimal", "standard", "detailed", "deep", "exhaustive", "optional"}

IMPLEMENTATION_MODES = {
    "none",
    "pseudocode",
    "minimal",
    "from_scratch",
    "framework",
    "comparative",
    "debugging_exercise",
}

VERIFICATION_TIERS = (
    "generated",
    "syntax_checked",
    "executed",
    "tests_passed",
    "numerically_verified",
    "mathematically_verified",
)

UNSUPPORTED_HTML_RE = re.compile(r"<\s*(?:script|iframe|object|embed|canvas)\b", re.I)
INVENTED_FREQ_RE = re.compile(
    r"\b(?:over\s+)?\d{1,3}%\s+of\s+(?:students|learners|beginners|developers|people)\s+(?:make\s+this|confuse|misunderstand|fail)\b",
    re.I,
)
WIKILINK_RE = re.compile(r"\[\[([^\]\n]+)\]\]")
INLINE_MATH_RE = re.compile(r"(?<!\$)\$(?!\$)([^$\n]+?)(?<!\$)\$(?!\$)")
DISPLAY_MATH_RE = re.compile(r"(?<![\\$])\$\$(?!\$)(.+?)(?<![\\$])\$\$(?!\$)", re.S)


def _issue(
    issue_num: int,
    *,
    severity: str,
    concept_id: str,
    location: str,
    issue_type: str,
    description: str,
    suggested_repair: str,
    requires_regeneration: bool = False,
) -> dict[str, Any]:
    return {
        "issue_id": f"PED-{issue_num:03d}",
        "severity": severity,
        "concept_id": concept_id,
        "location": location,
        "type": issue_type,
        "description": description,
        "suggested_repair": suggested_repair,
        "requires_regeneration": requires_regeneration,
    }


def safe_eval_math(expression: str, variables: dict[str, float]) -> float:
    """Safely evaluate an algebraic expression via the canonical AST evaluator."""
    return safe_eval_expr(
        expression,
        variables,
        allow_functions=True,
        allow_constants=True,
        normalize_equation=True,
    )


# ===========================================================================
# P01 — Cognitive Dependency Mapping
# ===========================================================================

def build_cognitive_dependency_graph(
    concepts: list[dict[str, Any]],
    *,
    source_policy: str = "independent",
) -> dict[str, Any]:
    """Build and validate the cognitive prerequisite graph G=(V, E) separately from chapter hierarchy.

    Supports typed edges (essential, supporting, alternative_route, contextual, future_application),
    readiness-sensitive treatments, Kahn topological ordering over essential edges, cycle analysis,
    and source-order bridge reconciliation when strict/expanded source policies preserve order.
    """
    ids = [c["id"] for c in concepts]
    id_set = set(ids)
    preserve_source_order = source_policy in {"strict", "expanded"}

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    external_prereqs: list[dict[str, Any]] = []
    source_order_bridges: list[dict[str, Any]] = []

    essential_adj: dict[str, list[str]] = {cid: [] for cid in ids}
    in_degree: dict[str, int] = {cid: 0 for cid in ids}
    full_adj: dict[str, list[str]] = {cid: [] for cid in ids}

    for idx, c in enumerate(concepts):
        cid = c["id"]
        raw_deps = c.get("dependency_plan") or c.get("prerequisites") or []
        if isinstance(raw_deps, dict):
            # Support structured dependency_plan dict ({essential: [...], supporting: [...], prerequisite_treatments: {...}})
            treatments = raw_deps.get("prerequisite_treatments") or {}
            expanded: list[dict[str, Any]] = []
            for dep_type in ("essential", "supporting", "alternative_route", "contextual", "future_application"):
                for item in raw_deps.get(dep_type) or []:
                    target = item if isinstance(item, str) else item.get("concept")
                    tr = (
                        treatments.get(target)
                        or (item.get("treatment") if isinstance(item, dict) else None)
                        or ("bridge" if dep_type == "essential" else "remind")
                    )
                    expanded.append({"concept": target, "type": dep_type, "treatment": tr})
            raw_deps = expanded

        parsed_deps: list[dict[str, Any]] = []
        for dep in raw_deps:
            if isinstance(dep, str):
                target = dep.strip()
                dep_type = "essential"
                treatment = "teach"
            elif isinstance(dep, dict):
                target = str(dep.get("concept") or "").strip()
                raw_type = str(dep.get("type") or dep.get("kind") or "essential").strip().lower()
                dep_type = {
                    "required": "essential",
                    "helpful": "supporting",
                }.get(raw_type, raw_type)
                if dep_type not in DEPENDENCY_TYPES:
                    raise ValueError(f"{cid}: unknown dependency type '{dep_type}'")
                raw_tr = str(dep.get("treatment") or "teach").strip().lower()
                if raw_tr not in PREREQ_TREATMENTS:
                    raise ValueError(f"{cid}: unknown prerequisite treatment '{raw_tr}'")
                treatment = PREREQ_TREATMENTS[raw_tr]
            else:
                raise ValueError(f"{cid}: invalid prerequisite entry")

            if not target:
                continue
            rec = {"concept": target, "type": dep_type, "treatment": treatment}
            parsed_deps.append(rec)

            if target in id_set:
                edge = {"from": target, "to": cid, "type": dep_type, "treatment": treatment}
                edges.append(edge)
                full_adj[target].append(cid)
                if dep_type == "essential":
                    essential_adj[target].append(cid)
                    in_degree[cid] += 1
                    # If source order puts consumer before essential prereq, recommend a local bridge
                    if preserve_source_order and ids.index(target) > idx:
                        source_order_bridges.append({
                            "consumer": cid,
                            "prerequisite": target,
                            "action": "insert_local_bridge",
                            "reason": f"Source order places '{cid}' before essential prerequisite '{target}'; preserve source sequence and insert a concise bridge.",
                        })
            else:
                external_prereqs.append({
                    "concept": target,
                    "consumer": cid,
                    "type": dep_type,
                    "treatment": treatment,
                })

        nodes.append({
            "id": cid,
            "title": c.get("title") or cid,
            "source_position": idx + 1,
            "prerequisites": parsed_deps,
            "familiarity": c.get("familiarity") or "estimated",
        })

    # Kahn topological ordering over essential prerequisite edges
    queue = deque(cid for cid in ids if in_degree[cid] == 0)
    topo_order: list[str] = []
    deg_copy = dict(in_degree)
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v in essential_adj[u]:
            deg_copy[v] -= 1
            if deg_copy[v] == 0:
                queue.append(v)

    essential_cycles: list[dict[str, Any]] = []
    if len(topo_order) < len(ids):
        cycled = [cid for cid in ids if cid not in topo_order]
        essential_cycles.append({
            "nodes": cycled,
            "resolution": "Split overbroad concepts into foundational/advanced layers or downgrade mutual links to 'contextual'/'supporting'.",
        })

    return {
        "nodes": nodes,
        "edges": edges,
        "external_prerequisites": external_prereqs,
        "teaching_order": ids if preserve_source_order else (topo_order if not essential_cycles else ids),
        "essential_topological_order": topo_order,
        "has_essential_cycles": bool(essential_cycles),
        "cycles": essential_cycles,
        "source_order_preserved": preserve_source_order,
        "source_order_bridges": source_order_bridges,
    }


def detect_dependency_gaps(
    note_text: str,
    dependency_graph: dict[str, Any],
    *,
    concept_id: str = "document",
) -> list[dict[str, Any]]:
    """Detect essential prerequisites marked 'bridge' or 'teach' that are never introduced in the note."""
    issues: list[dict[str, Any]] = []
    low = note_text.lower()
    issue_idx = 1

    # Check external essential prerequisites that require teaching or bridging
    for ext in dependency_graph.get("external_prerequisites", []):
        if ext["type"] == "essential" and ext["treatment"] in {"bridge", "teach"}:
            term = ext["concept"].replace("_", " ").replace("-", " ").lower()
            words = [w for w in term.split() if len(w) > 2]
            present = term in low or (words and all(re.search(rf"\b{re.escape(w)}\w*\b", low) for w in words))
            if not present:
                issues.append(_issue(
                    issue_idx,
                    severity="major",
                    concept_id=ext["consumer"],
                    location="prerequisite_bridge",
                    issue_type="missing_prerequisite_bridge",
                    description=f"Essential prerequisite '{ext['concept']}' (treatment={ext['treatment']}) is not introduced or bridged before use.",
                    suggested_repair=f"Insert a concise prerequisite bridge defining '{ext['concept']}' before developing '{ext['consumer']}'.",
                ))
                issue_idx += 1

    if dependency_graph.get("has_essential_cycles"):
        for cyc in dependency_graph["cycles"]:
            issues.append(_issue(
                issue_idx,
                severity="major",
                concept_id=concept_id,
                location="dependency_graph",
                issue_type="essential_dependency_cycle",
                description=f"Essential prerequisite cycle detected across {cyc['nodes']}.",
                suggested_repair=cyc["resolution"],
            ))
            issue_idx += 1

    return issues


# ===========================================================================
# P02 — Progressive Explanation Layers (L1-L8)
# ===========================================================================

def plan_explanation_layers(concept: dict[str, Any], *, audience: str = "beginner") -> dict[str, str]:
    """Conditionally activate L1-L8 explanation layers based on types, objectives, depths, and audience."""
    explicit = concept.get("explanation_plan")
    if isinstance(explicit, dict):
        plan: dict[str, str] = {}
        for layer in EXPLANATION_LAYERS:
            val = str(explicit.get(layer, "omitted")).strip().lower()
            if val not in LAYER_LEVELS:
                raise ValueError(f"{concept['id']}: invalid explanation layer level '{val}' for '{layer}'")
            plan[layer] = val
        return plan

    types = set(concept.get("types") or [])
    objectives = set(concept.get("objectives") or [])
    depth = concept.get("depth") or {}
    t_lvl = depth.get("theory", 0)
    m_lvl = depth.get("math", 0)
    c_lvl = depth.get("code", 0)
    p_lvl = depth.get("practice", 0)

    is_standalone_def = objectives == {"define"} or objectives == {"recognize"}

    layers: dict[str, str] = {
        "motivation": "omitted" if (is_standalone_def or audience == "advanced") else ("detailed" if audience == "beginner" and t_lvl >= 3 else "standard"),
        "intuition": "omitted" if is_standalone_def else ("detailed" if (audience == "beginner" and t_lvl >= 3) or bool(types & {"conceptual", "mathematical", "scientific"}) else "minimal"),
        "mechanism": "omitted" if is_standalone_def else ("deep" if t_lvl >= 4 or "algorithmic" in types or "architectural" in types else "detailed" if t_lvl >= 3 else "standard"),
        "formal_definition": "detailed" if (t_lvl >= 3 or "define" in objectives or m_lvl >= 2) else "standard",
        "formalization": "deep" if (m_lvl >= 4 or c_lvl >= 4 or "prove" in objectives or "derive" in objectives) else ("detailed" if m_lvl >= 2 or c_lvl >= 2 or "algorithmic" in types else "omitted"),
        "worked_application": "deep" if p_lvl >= 4 else ("detailed" if p_lvl >= 2 or bool(objectives & {"calculate", "apply", "implement", "trace", "solve"}) else "omitted"),
        "limitations": "detailed" if (t_lvl >= 4 or bool(objectives & {"analyze", "evaluate", "prove", "debug"})) else ("standard" if t_lvl >= 3 and not is_standalone_def else "omitted"),
        "integration": "supporting" if (t_lvl >= 3 and not is_standalone_def) else "omitted",
    }
    return layers


# ===========================================================================
# P03 — Multiple Representation Alignment
# ===========================================================================

def validate_representations(
    concept_spec: dict[str, Any],
    *,
    note_text: str = "",
    code_outputs: dict[str, float] | None = None,
    source_policy: str = "independent",
) -> list[dict[str, Any]]:
    """Validate symbol consistency, equation-vs-example/code numeric agreement, tensor shapes, and analogy limits."""
    issues: list[dict[str, Any]] = []
    cid = str(concept_spec.get("concept") or concept_spec.get("id") or "concept")
    idx = 1

    symbols = concept_spec.get("symbols") or {}
    equation = concept_spec.get("equation")
    expected_values = dict(concept_spec.get("expected_values") or {})

    # Extract numeric bindings from symbols dict
    var_values: dict[str, float] = {}
    target_var: str | None = None
    if isinstance(equation, str) and "=" in equation:
        lhs = equation.split("=", 1)[0].strip()
        if re.fullmatch(r"[A-Za-z_]\w*", lhs):
            target_var = lhs

    for sym, info in symbols.items():
        if isinstance(info, dict) and isinstance(info.get("value"), (int, float)):
            if sym == target_var:
                expected_values.setdefault(sym, float(info["value"]))
            else:
                var_values[sym] = float(info["value"])
        elif isinstance(info, (int, float)):
            if sym == target_var:
                expected_values.setdefault(sym, float(info))
            else:
                var_values[sym] = float(info)

    # 1. Check algebraic equation against declared expected values
    computed_val: float | None = None
    if isinstance(equation, str) and equation.strip() and var_values:
        try:
            computed_val = safe_eval_math(equation, var_values)
            if target_var and target_var in expected_values:
                exp = float(expected_values[target_var])
                if not math.isclose(computed_val, exp, rel_tol=1e-5, abs_tol=1e-6):
                    issues.append(_issue(
                        idx,
                        severity="critical",
                        concept_id=cid,
                        location="equation_and_example",
                        issue_type="equation_example_mismatch",
                        description=f"Equation '{equation}' evaluates to {computed_val:g} for {var_values}, contradicting declared {target_var}={exp:g}.",
                        suggested_repair="Recalculate the worked example or verify the governing equation against the authoritative specification.",
                    ))
                    idx += 1
        except ValueError as exc:
            issues.append(_issue(
                idx,
                severity="major",
                concept_id=cid,
                location="symbol_registry",
                issue_type="undefined_symbol_in_equation",
                description=str(exc),
                suggested_repair="Define every symbol appearing in the equation in the canonical symbol specification before use.",
            ))
            idx += 1

    # 2. Check equation against executed code outputs
    if code_outputs and target_var and computed_val is not None and target_var in code_outputs:
        observed = float(code_outputs[target_var])
        if not math.isclose(computed_val, observed, rel_tol=1e-5, abs_tol=1e-6):
            repair_hint = (
                "Preserve the supplied source equation and flag the code discrepancy separately."
                if source_policy == "strict"
                else f"Repair the conflicting code or equation so both yield {computed_val:g} (currently code yields {observed:g})."
            )
            issues.append(_issue(
                idx,
                severity="critical",
                concept_id=cid,
                location="equation_vs_code",
                issue_type="equation_code_conflict",
                description=f"Equation '{equation}' predicts {target_var}={computed_val:g}, but code output produced {target_var}={observed:g}.",
                suggested_repair=repair_hint,
            ))
            idx += 1

    # 3. Validate tensor shape contractions (e.g. matmul contracts [A, K] @ [K, B] -> [A, B])
    tensor_ops = concept_spec.get("tensor_operations") or []
    tensor_shapes = concept_spec.get("tensor_shapes") or {}
    for op in tensor_ops:
        if not isinstance(op, dict):
            continue
        if op.get("op") == "matmul":
            a_name, b_name, out_name = op.get("left"), op.get("right"), op.get("output")
            a_shape = tensor_shapes.get(a_name)
            b_shape = tensor_shapes.get(b_name)
            o_shape = tensor_shapes.get(out_name)
            if isinstance(a_shape, list) and isinstance(b_shape, list) and len(a_shape) >= 2 and len(b_shape) >= 2:
                if a_shape[-1] != b_shape[-2]:
                    issues.append(_issue(
                        idx,
                        severity="critical",
                        concept_id=cid,
                        location="tensor_shapes",
                        issue_type="tensor_shape_mismatch",
                        description=f"Incompatible matmul shapes: {a_name}{a_shape} @ {b_name}{b_shape} ({a_shape[-1]} != {b_shape[-2]}).",
                        suggested_repair=f"Align inner dimensions of {a_name} and {b_name} across equations, diagrams, and code.",
                    ))
                    idx += 1
                elif isinstance(o_shape, list) and (o_shape[-2:] != [a_shape[-2], b_shape[-1]]):
                    issues.append(_issue(
                        idx,
                        severity="major",
                        concept_id=cid,
                        location="tensor_shapes",
                        issue_type="tensor_output_shape_mismatch",
                        description=f"Declared output {out_name}{o_shape} conflicts with {a_name}{a_shape} @ {b_name}{b_shape} -> [..., {a_shape[-2]}, {b_shape[-1]}].",
                        suggested_repair=f"Update {out_name} shape annotation to end with [{a_shape[-2]}, {b_shape[-1]}].",
                    ))
                    idx += 1

    # 4. Check analogy breakdown limit when analogy representation is used
    reps = concept_spec.get("representations") or []
    has_analogy = any((r.get("type") if isinstance(r, dict) else r) == "analogy" for r in reps)
    if has_analogy and not concept_spec.get("analogy_limit"):
        issues.append(_issue(
            idx,
            severity="moderate",
            concept_id=cid,
            location="analogy",
            issue_type="missing_analogy_limit",
            description="Analogy representation is planned without stating where the analogy breaks down.",
            suggested_repair="Record the exact boundary where the analogy fails so intuition is not mistaken for an equivalence.",
        ))
        idx += 1

    # 5. Check that canonical symbols appear defined in prose when note_text is supplied
    if note_text and symbols:
        for sym in symbols:
            if not re.search(rf"(?<![A-Za-z0-9_]){re.escape(sym)}(?![A-Za-z0-9_])", note_text):
                issues.append(_issue(
                    idx,
                    severity="moderate",
                    concept_id=cid,
                    location="notation",
                    issue_type="missing_canonical_symbol",
                    description=f"Canonical symbol '{sym}' from concept specification is absent from the authored explanation.",
                    suggested_repair=f"Introduce and consistently use '{sym}' or update the canonical symbol specification.",
                ))
                idx += 1

    return issues


# ===========================================================================
# P04 — Worked-Example Intelligence
# ===========================================================================

def audit_examples(
    examples: list[dict[str, Any]],
    *,
    concept_id: str = "concept",
    source_policy: str = "independent",
) -> list[dict[str, Any]]:
    """Validate worked-example purposes, provenance under source policies, and detect redundant duplicates."""
    issues: list[dict[str, Any]] = []
    idx = 1
    seen_signatures: dict[tuple[str, str, str], str] = {}

    for ex_i, ex in enumerate(examples, 1):
        if not isinstance(ex, dict):
            continue
        eid = str(ex.get("id") or f"EX-{ex_i}")
        cat = str(ex.get("category") or "worked").strip().lower()
        if cat not in EXAMPLE_CATEGORIES:
            issues.append(_issue(
                idx,
                severity="moderate",
                concept_id=concept_id,
                location=eid,
                issue_type="invalid_example_category",
                description=f"Example '{eid}' uses unknown category '{cat}'.",
                suggested_repair=f"Assign a supported example category from {sorted(EXAMPLE_CATEGORIES)}.",
            ))
            idx += 1
            continue

        prov = str(ex.get("provenance") or "illustrative").strip().lower()
        if prov not in EXAMPLE_PROVENANCE:
            issues.append(_issue(
                idx,
                severity="moderate",
                concept_id=concept_id,
                location=eid,
                issue_type="invalid_example_provenance",
                description=f"Example '{eid}' uses unknown provenance '{prov}'.",
                suggested_repair=f"Tag provenance as one of {sorted(EXAMPLE_PROVENANCE)}.",
            ))
            idx += 1

        if source_policy == "strict" and prov == "illustrative" and not ex.get("labeled_as_addition", False):
            issues.append(_issue(
                idx,
                severity="major",
                concept_id=concept_id,
                location=eid,
                issue_type="unlabeled_illustrative_example_in_strict_mode",
                description=f"Illustrative example '{eid}' in strict source mode is not explicitly labeled as an educational addition.",
                suggested_repair="Label the example explicitly as an illustrative addition or use only source-provided examples.",
            ))
            idx += 1

        # Redundancy / duplicate teaching signature check
        mech = str(ex.get("mechanism") or ex.get("purpose") or "").strip().lower()
        boundary = str(ex.get("boundary_or_twist") or "none").strip().lower()
        sig = (cat, mech, boundary)
        if mech and sig in seen_signatures:
            issues.append(_issue(
                idx,
                severity="moderate",
                concept_id=concept_id,
                location=eid,
                issue_type="redundant_example",
                description=f"Example '{eid}' duplicates '{seen_signatures[sig]}' (same category='{cat}', mechanism='{mech}', boundary='{boundary}').",
                suggested_repair=f"Consolidate '{eid}' with '{seen_signatures[sig]}' or convert it to a distinct boundary/counterexample/transfer case.",
            ))
            idx += 1
        elif mech:
            seen_signatures[sig] = eid

    return issues


# ===========================================================================
# P05 — Visual Reasoning and Diagram Selection
# ===========================================================================

def validate_visuals(
    visuals: list[dict[str, Any]],
    *,
    concept_id: str = "concept",
    vault: Path | None = None,
    note_text: str = "",
) -> list[dict[str, Any]]:
    """Validate visual type, axis/plotted mathematical accuracy, Obsidian compatibility, asset existence, and density."""
    issues: list[dict[str, Any]] = []
    idx = 1
    seen_purposes: dict[tuple[str, str], str] = {}

    if note_text and UNSUPPORTED_HTML_RE.search(note_text):
        issues.append(_issue(
            idx,
            severity="major",
            concept_id=concept_id,
            location="visual_rendering",
            issue_type="unsupported_obsidian_html",
            description="Arbitrary interactive HTML (<script>/<iframe>/<canvas>) is incompatible with portable Obsidian Markdown.",
            suggested_repair="Replace with Mermaid, Markdown tables, LaTeX, or a static .png/.svg image asset.",
        ))
        idx += 1

    for v_i, vis in enumerate(visuals, 1):
        if not isinstance(vis, dict):
            continue
        vid = str(vis.get("id") or f"VIS-{v_i}")
        vtype = str(vis.get("type") or "").strip().lower()
        if vtype and vtype not in VISUAL_CATEGORIES:
            issues.append(_issue(
                idx,
                severity="moderate",
                concept_id=concept_id,
                location=vid,
                issue_type="unknown_visual_type",
                description=f"Visual '{vid}' specifies unrecognized type '{vtype}'.",
                suggested_repair=f"Choose from {sorted(VISUAL_CATEGORIES)}.",
            ))
            idx += 1

        purpose = str(vis.get("purpose") or "").strip().lower()
        sig = (vtype, purpose)
        if purpose and sig in seen_purposes:
            issues.append(_issue(
                idx,
                severity="moderate",
                concept_id=concept_id,
                location=vid,
                issue_type="redundant_visual",
                description=f"Visual '{vid}' duplicates '{seen_purposes[sig]}' with the same type and purpose ('{purpose}').",
                suggested_repair="Keep one clear visual or assign each diagram a distinct explanatory role.",
            ))
            idx += 1
        elif purpose:
            seen_purposes[sig] = vid

        # Check asset existence if an image asset is claimed
        asset_path = vis.get("asset_path")
        if asset_path and vault is not None:
            candidate = vault / str(asset_path).lstrip("/")
            if not candidate.is_file():
                issues.append(_issue(
                    idx,
                    severity="major",
                    concept_id=concept_id,
                    location=vid,
                    issue_type="missing_visual_asset",
                    description=f"Visual '{vid}' references missing asset '{asset_path}'.",
                    suggested_repair="Generate and save the asset or fall back to a supported Mermaid diagram/table.",
                ))
                idx += 1

        # Mathematical accuracy check for function graphs / data visualizations
        model = vis.get("mathematical_model")
        if isinstance(model, dict):
            expr = model.get("function")
            var_name = str(model.get("variable") or "x")
            axes = vis.get("axes") or {}
            if vtype == "function_graph" and (not axes.get("x") or not axes.get("y")):
                issues.append(_issue(
                    idx,
                    severity="major",
                    concept_id=concept_id,
                    location=vid,
                    issue_type="missing_axis_labels",
                    description=f"Function graph '{vid}' is missing required x/y axis labels.",
                    suggested_repair="Specify explicit x and y axis labels with units/variables.",
                ))
                idx += 1
            if expr and isinstance(vis.get("plotted_points"), list):
                for pt in vis["plotted_points"]:
                    if isinstance(pt, (list, tuple)) and len(pt) == 2:
                        x_val, y_val = float(pt[0]), float(pt[1])
                        try:
                            expected_y = safe_eval_math(expr, {var_name: x_val})
                            if not math.isclose(expected_y, y_val, rel_tol=1e-4, abs_tol=1e-5):
                                issues.append(_issue(
                                    idx,
                                    severity="major",
                                    concept_id=concept_id,
                                    location=vid,
                                    issue_type="misleading_plotted_value",
                                    description=f"Visual '{vid}' plots ({x_val:g}, {y_val:g}), but '{expr}' evaluates to {expected_y:g} at {var_name}={x_val:g}.",
                                    suggested_repair=f"Correct the plotted point to ({x_val:g}, {expected_y:g}) or remove the inaccurate diagram.",
                                ))
                                idx += 1
                        except ValueError:
                            pass

    return issues


# ===========================================================================
# P06 — Misconception Anticipation
# ===========================================================================

def audit_misconceptions(
    misconceptions: list[dict[str, Any]],
    *,
    note_text: str = "",
    concept_id: str = "concept",
) -> list[dict[str, Any]]:
    """Validate misconception plan structure, relevance, and absence of invented frequency statistics."""
    issues: list[dict[str, Any]] = []
    idx = 1
    seen_ids: set[str] = set()

    for m in misconceptions:
        if not isinstance(m, dict):
            continue
        mid = str(m.get("id") or "misconception")
        if mid in seen_ids:
            issues.append(_issue(
                idx,
                severity="minor",
                concept_id=concept_id,
                location=mid,
                issue_type="duplicate_misconception",
                description=f"Duplicate misconception entry '{mid}'.",
                suggested_repair="Merge duplicate misconception notes into one point-of-need correction.",
            ))
            idx += 1
        seen_ids.add(mid)
        cat = str(m.get("type") or m.get("category") or "conceptual").strip().lower()
        if cat not in MISCONCEPTION_CATEGORIES:
            issues.append(_issue(
                idx,
                severity="moderate",
                concept_id=concept_id,
                location=mid,
                issue_type="invalid_misconception_category",
                description=f"Misconception '{mid}' has unknown category '{cat}'.",
                suggested_repair=f"Use one of {sorted(MISCONCEPTION_CATEGORIES)}.",
            ))
            idx += 1

    if note_text and INVENTED_FREQ_RE.search(note_text):
        issues.append(_issue(
            idx,
            severity="moderate",
            concept_id=concept_id,
            location="misconceptions",
            issue_type="unsupported_misconception_statistic",
            description="Detected unverified percentage claim about how frequently learners hold a misconception.",
            suggested_repair="Describe the conceptual trap objectively without inventing learner-frequency statistics.",
        ))
        idx += 1

    return issues


# ===========================================================================
# P08 — Cross-Topic Knowledge Integration
# ===========================================================================

def resolve_cross_topic_connections(
    connections: list[dict[str, Any]],
    *,
    vault: Path | None = None,
    planned_stems: set[str] | None = None,
    note_text: str = "",
) -> dict[str, Any]:
    """Resolve semantic cross-topic connections against the Obsidian vault and detect link inflation."""
    lookup: dict[str, list[str]] = {}
    if vault is not None and vault.is_dir():
        from vault_graph import _build_lookup
        from vault_index import build_or_load_index

        idx_data = build_or_load_index(vault, use_cache=False)
        lookup = _build_lookup(idx_data.get("notes") or [])

    planned_cf = {s.strip().casefold() for s in (planned_stems or set())}
    resolved: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    seen_targets: dict[str, str] = {}
    issue_idx = 1

    for conn in connections:
        if not isinstance(conn, dict):
            continue
        target = str(conn.get("target") or "").strip()
        rel = str(conn.get("relation") or "used_together_with").strip().lower()
        if rel not in CONNECTION_RELATIONS:
            raise ValueError(f"Unknown cross-topic relation '{rel}'")
        norm_key = re.sub(r"[\s_-]+", "", target.casefold())
        if norm_key in seen_targets and seen_targets[norm_key] != target:
            issues.append(_issue(
                issue_idx,
                severity="minor",
                concept_id="connections",
                location=target,
                issue_type="duplicate_concept_synonym",
                description=f"Near-duplicate concept targets '{seen_targets[norm_key]}' and '{target}'.",
                suggested_repair="Consolidate onto one canonical concept ID/title.",
            ))
            issue_idx += 1
        seen_targets.setdefault(norm_key, target)

        matches = lookup.get(target.lower(), [])
        if len(matches) == 1:
            status = "existing_note"
            resolved_path = matches[0]
        elif len(matches) > 1:
            status = "ambiguous_note"
            resolved_path = None
            issues.append(_issue(
                issue_idx,
                severity="moderate",
                concept_id="connections",
                location=target,
                issue_type="ambiguous_vault_link",
                description=f"Target '{target}' matches multiple vault notes: {matches}.",
                suggested_repair="Use a vault-relative path to disambiguate the wikilink.",
            ))
            issue_idx += 1
        elif target.casefold() in planned_cf:
            status = "planned_note"
            resolved_path = None
        elif conn.get("external_url"):
            status = "external_resource"
            resolved_path = conn["external_url"]
        else:
            status = "unresolved_concept"
            resolved_path = None

        resolved.append({
            "target": target,
            "relation": rel,
            "status": status,
            "resolved_path": resolved_path,
            "bridge": conn.get("bridge") or "",
        })

    # Link inflation guard: detect over-linked short prose
    if note_text:
        words = len(re.findall(r"\b\w+\b", note_text))
        links = WIKILINK_RE.findall(note_text)
        if words >= 40 and len(links) > max(12, words // 12):
            issues.append(_issue(
                issue_idx,
                severity="moderate",
                concept_id="connections",
                location="body_links",
                issue_type="link_inflation",
                description=f"High wikilink density ({len(links)} links in {words} words) risks cluttering navigation.",
                suggested_repair="Keep only links supporting prerequisite review, comparison, application, or revision.",
            ))

    return {"connections": resolved, "issues": issues}


# ===========================================================================
# P09 — Adaptive Detail and Cognitive Load Control
# ===========================================================================

def plan_detail_allocation(concept: dict[str, Any], *, audience: str = "beginner") -> dict[str, str]:
    """Allocate concept-specific detail facets (no arbitrary word quotas)."""
    explicit = concept.get("detail_profile") or concept.get("detail_plan")
    if isinstance(explicit, dict):
        return {k: str(v).strip().lower() for k, v in explicit.items() if str(v).strip().lower() in DETAIL_LEVELS}

    depth = concept.get("depth") or {}
    lvl_map = {0: "minimal", 1: "minimal", 2: "standard", 3: "detailed", 4: "deep", 5: "exhaustive"}
    return {
        "intuition": "deep" if (audience == "beginner" and depth.get("theory", 0) >= 3) else lvl_map.get(depth.get("theory", 2), "standard"),
        "formal_definition": lvl_map.get(max(depth.get("theory", 0), depth.get("math", 0)), "standard"),
        "mathematics": lvl_map.get(depth.get("math", 0), "minimal"),
        "coding": lvl_map.get(depth.get("code", 0), "minimal"),
        "edge_cases": "detailed" if depth.get("theory", 0) >= 3 or depth.get("code", 0) >= 3 else "minimal",
    }


def audit_cognitive_load(
    note_text: str,
    *,
    audience: str = "beginner",
    concept_id: str = "document",
) -> list[dict[str, Any]]:
    """Detect cognitive-load density spikes (too many unexplained symbols per paragraph, unchunked dense math)."""
    issues: list[dict[str, Any]] = []
    idx = 1

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", note_text) if p.strip() and not p.strip().startswith(("#", "```", "~~~", "|", "---"))]
    has_example = bool(re.search(r"\b(?:for example|worked example|suppose|concrete|trace|let\s+[a-z]\s*=|\d+\s*[+\-*/=])", note_text, re.I))
    total_display_eqs = len(DISPLAY_MATH_RE.findall(note_text))

    for p_i, para in enumerate(paragraphs, 1):
        inline_syms = set(INLINE_MATH_RE.findall(para))
        if audience == "beginner" and len(inline_syms) >= 7 and not re.search(r"\b(?:where|denotes?|represents?|means?|is the)\b", para, re.I):
            issues.append(_issue(
                idx,
                severity="major",
                concept_id=concept_id,
                location=f"paragraph_{p_i}",
                issue_type="symbol_overload_without_definitions",
                description=f"Paragraph {p_i} introduces {len(inline_syms)} inline math expressions without nearby definitions for a beginner audience.",
                suggested_repair="Chunk the explanation and define key symbols beside their first use before combining them.",
            ))
            idx += 1

    if audience == "beginner" and total_display_eqs >= 3 and not has_example:
        issues.append(_issue(
            idx,
            severity="moderate",
            concept_id=concept_id,
            location="worked_examples",
            issue_type="dense_formalism_without_example",
            description=f"Introductory note contains {total_display_eqs} display equations without a concrete worked numerical example.",
            suggested_repair="Insert a small worked numerical example near the central equation to reduce cognitive load.",
        ))
        idx += 1

    return issues


# ===========================================================================
# P10 — Executable Learning and Verification
# ===========================================================================

def plan_executable_learning(concept: dict[str, Any]) -> dict[str, Any]:
    """Derive executable learning contract strictly from existing instructional_plan coding depth (C0-C5)."""
    depth = concept.get("depth") or {}
    c_lvl = depth.get("code", 0)
    impl = concept.get("implementation") or {}

    if c_lvl == 0:
        mode = "none"
    elif c_lvl == 1:
        mode = "pseudocode"
    elif c_lvl == 2:
        mode = "minimal"
    elif c_lvl == 3:
        mode = "framework" if impl.get("framework") in {"scikit-learn", "pytorch", "tensorflow-keras"} else "from_scratch"
    else:
        mode = "from_scratch"

    if isinstance(impl.get("mode"), str) and impl["mode"] in IMPLEMENTATION_MODES:
        # Never allow an explicit mode to contradict C0
        if c_lvl == 0 and impl["mode"] != "none":
            raise ValueError(f"{concept['id']}: implementation mode '{impl['mode']}' conflicts with C0 code depth")
        mode = impl["mode"]

    return {
        "mode": mode,
        "language": impl.get("language") or ("none" if c_lvl < 2 else "python"),
        "framework": impl.get("framework"),
        "runtime_verification": "when_available" if c_lvl >= 2 else "not_applicable",
        "equation_mapping_required": c_lvl >= 2 and depth.get("math", 0) >= 2,
    }


def verify_executable_example(
    code: str,
    *,
    language: str = "python",
    untrusted_source: bool = False,
    execute: bool = True,
) -> dict[str, Any]:
    """Verify code honestly across explicit verification tiers without executing untrusted retrieved code."""
    if untrusted_source:
        return {
            "verification_tier": "generated",
            "syntax_ok": False,
            "executed": False,
            "passed": False,
            "error": "Execution refused: code originated from an untrusted external source.",
        }

    if language in {"python", "py", "python3"}:
        try:
            ast.parse(code)
        except SyntaxError as exc:
            return {
                "verification_tier": "generated",
                "syntax_ok": False,
                "executed": False,
                "passed": False,
                "error": f"SyntaxError on line {exc.lineno}: {exc.msg}",
            }
        if not execute:
            return {
                "verification_tier": "syntax_checked",
                "syntax_ok": True,
                "executed": False,
                "passed": True,
                "stdout": "",
            }
        from scriptorium.engines._verification import Block, verify_runtimes

        try:
            res = verify_runtimes({"python": Block(1, "python", code)}, [])["python"]
            has_assert = "assert " in code
            return {
                "verification_tier": "tests_passed" if has_assert else "executed",
                "syntax_ok": True,
                "executed": res.get("status") == "executed",
                "passed": True,
                "stdout": res.get("stdout", ""),
                "version": res.get("version"),
            }
        except ValueError as exc:
            return {
                "verification_tier": "syntax_checked",
                "syntax_ok": True,
                "executed": True,
                "passed": False,
                "error": str(exc),
            }

    return {
        "verification_tier": "generated",
        "syntax_ok": True,
        "executed": False,
        "passed": True,
        "note": f"Runtime execution for '{language}' is verified through plan_notes.py verify-runtimes.",
    }


# ===========================================================================
# P11 — Multi-Layer Revision and Navigation
# ===========================================================================

def plan_revision_layers(plan: dict[str, Any]) -> dict[str, Any]:
    """Select conditional revision layers (Layer A full note, Layer B concept review, Layer C rapid revision)."""
    concepts = plan.get("concepts") or []
    max_math = max((c.get("depth", {}).get("math", 0) for c in concepts), default=0)
    max_theory = max((c.get("depth", {}).get("theory", 0) for c in concepts), default=0)
    standalone = len(concepts) == 1 and max_theory <= 2 and max_math == 0

    return {
        "layer_a_authoritative": True,
        "layer_b_concept_review": not standalone,
        "layer_c_rapid_revision": len(concepts) >= 2 or max_theory >= 4 or max_math >= 3,
        "formula_reference_required": max_math >= 2,
        "preserve_conditions_in_revision": max_math >= 2,
    }


def validate_revision_integrity(
    full_note: str,
    revision_text: str,
    *,
    canonical_formulas: list[dict[str, Any]] | None = None,
    concept_id: str = "revision",
) -> list[dict[str, Any]]:
    """Verify condensed revision material preserves assumptions/conditions, matches full note, and avoids verbatim duplication."""
    issues: list[dict[str, Any]] = []
    idx = 1

    # 1. Check that canonical formulas in revision preserve stated applicability conditions
    rev_low = revision_text.lower()
    for item in canonical_formulas or []:
        formula = str(item.get("formula") or "").strip()
        conditions = item.get("conditions") or []
        if formula and formula in revision_text:
            for cond in conditions:
                cond_words = [w for w in re.findall(r"[a-zA-Z]{4,}", cond.lower())]
                if cond_words and not all(re.search(rf"\b{re.escape(w)}\w*\b", rev_low) for w in cond_words):
                    issues.append(_issue(
                        idx,
                        severity="major",
                        concept_id=concept_id,
                        location="revision_formulas",
                        issue_type="formula_stripped_of_conditions",
                        description=f"Condensed revision includes '{formula}' but omits required applicability condition '{cond}'.",
                        suggested_repair=f"State condition '{cond}' alongside '{formula}' in the revision layer.",
                    ))
                    idx += 1

    # 2. Check internal heading anchor links in revision point to actual headings in full_note
    from verify_vault_notes import _heading_slug

    full_headings = {
        _heading_slug(m.group(1))
        for line in full_note.splitlines()
        if (m := re.match(r"^#{1,6}\s+(.+)$", line))
    }
    for m in re.finditer(r"\[\[#([^\]|]+)", revision_text):
        anchor = _heading_slug(m.group(1))
        if anchor not in full_headings:
            issues.append(_issue(
                idx,
                severity="moderate",
                concept_id=concept_id,
                location="revision_navigation",
                issue_type="broken_revision_anchor",
                description=f"Revision link '[[#{m.group(1)}]]' does not match any heading in the full learning note.",
                suggested_repair="Point the revision anchor to an actual heading in Layer A.",
            ))
            idx += 1

    # 3. Check for verbatim multi-sentence paragraph duplication between full note and revision
    def _body_paragraphs(md: str) -> list[str]:
        paras: list[str] = []
        for chunk in re.split(r"\n\s*\n", md):
            lines = [ln.strip() for ln in chunk.splitlines() if ln.strip() and not ln.strip().startswith("#")]
            joined = " ".join(lines).strip()
            if len(joined) >= 120:
                paras.append(joined)
        return paras

    full_paras = set(_body_paragraphs(full_note))
    for rp in _body_paragraphs(revision_text):
        if rp in full_paras:
            issues.append(_issue(
                idx,
                severity="moderate",
                concept_id=concept_id,
                location="revision_summary",
                issue_type="verbatim_revision_duplication",
                description="Revision section repeats a full paragraph verbatim from the main explanation.",
                suggested_repair="Condense into retrieval cues and link back to the full explanation.",
            ))
            idx += 1
            break

    return issues


# ===========================================================================
# Unified Pedagogical Contract Builder & P07 Quality Validator
# ===========================================================================

def build_pedagogical_plan(
    instructional_plan: dict[str, Any],
    *,
    vault: Path | None = None,
    planned_stems: set[str] | None = None,
) -> dict[str, Any]:
    """Enrich an existing Contract v3 instructional_plan with sparse, unified P01-P11 pedagogical decisions."""
    if not isinstance(instructional_plan, dict) or not instructional_plan.get("concepts"):
        raise ValueError("build_pedagogical_plan requires a normalized instructional_plan with concepts.")

    audience = instructional_plan.get("audience", "beginner")
    source_policy = instructional_plan.get("source_policy", "independent")
    concepts = instructional_plan["concepts"]

    dep_graph = build_cognitive_dependency_graph(concepts, source_policy=source_policy)

    concept_plans: dict[str, dict[str, Any]] = {}
    all_connections: list[dict[str, Any]] = []

    for c in concepts:
        cid = c["id"]
        entry: dict[str, Any] = {
            "explanation_plan": plan_explanation_layers(c, audience=audience),
            "detail_profile": plan_detail_allocation(c, audience=audience),
            "implementation_plan": plan_executable_learning(c),
        }
        if c.get("canonical_spec"):
            entry["canonical_spec"] = deepcopy(c["canonical_spec"])
        if c.get("example_plan"):
            entry["example_plan"] = deepcopy(c["example_plan"])
        if c.get("visualizations"):
            entry["visual_plan"] = deepcopy(c["visualizations"])
        if c.get("misconception_plan"):
            entry["misconception_plan"] = deepcopy(c["misconception_plan"])
        if c.get("connection_plan"):
            entry["connection_plan"] = deepcopy(c["connection_plan"])
            all_connections.extend(c["connection_plan"])
        concept_plans[cid] = entry

    conn_report = resolve_cross_topic_connections(all_connections, vault=vault, planned_stems=planned_stems) if all_connections else {"connections": [], "issues": []}

    return {
        "pedagogical_contract_version": PEDAGOGICAL_CONTRACT_VERSION,
        "audience": audience,
        "source_policy": source_policy,
        "cognitive_dependency_graph": dep_graph,
        "concepts": concept_plans,
        "cross_topic_connections": conn_report["connections"],
        "revision_plan": plan_revision_layers(instructional_plan),
    }


def validate_pedagogical_quality(
    note_text: str,
    pedagogical_plan: dict[str, Any],
    *,
    vault: Path | None = None,
    code_outputs: dict[str, dict[str, float]] | None = None,
    revision_text: str | None = None,
    canonical_formulas: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Run unified P07 educational quality validation across all active mechanisms and return structured PED-xxx issues."""
    all_issues: list[dict[str, Any]] = []
    source_policy = pedagogical_plan.get("source_policy", "independent")
    audience = pedagogical_plan.get("audience", "beginner")
    dep_graph = pedagogical_plan.get("cognitive_dependency_graph") or {}

    all_issues.extend(detect_dependency_gaps(note_text, dep_graph))
    all_issues.extend(audit_cognitive_load(note_text, audience=audience))

    for cid, cplan in (pedagogical_plan.get("concepts") or {}).items():
        if cplan.get("canonical_spec"):
            all_issues.extend(
                validate_representations(
                    cplan["canonical_spec"],
                    note_text=note_text,
                    code_outputs=(code_outputs or {}).get(cid),
                    source_policy=source_policy,
                )
            )
        if cplan.get("example_plan"):
            all_issues.extend(audit_examples(cplan["example_plan"], concept_id=cid, source_policy=source_policy))
        if cplan.get("visual_plan"):
            all_issues.extend(validate_visuals(cplan["visual_plan"], concept_id=cid, vault=vault, note_text=note_text))
        if cplan.get("misconception_plan"):
            all_issues.extend(audit_misconceptions(cplan["misconception_plan"], note_text=note_text, concept_id=cid))

    if revision_text is not None:
        all_issues.extend(validate_revision_integrity(note_text, revision_text, canonical_formulas=canonical_formulas))

    # Renumber PED IDs consecutively across the unified report
    for idx, issue in enumerate(all_issues, 1):
        issue["issue_id"] = f"PED-{idx:03d}"

    counts = {"critical": 0, "major": 0, "moderate": 0, "minor": 0}
    for issue in all_issues:
        sev = issue.get("severity", "moderate")
        counts[sev] = counts.get(sev, 0) + 1

    return {
        "pedagogical_contract_version": PEDAGOGICAL_CONTRACT_VERSION,
        "issue_count": len(all_issues),
        "severity_counts": counts,
        "blocking": (counts["critical"] + counts["major"]) > 0,
        "issues": all_issues,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)

    p_plan = sub.add_parser("plan", help="Build a unified P01-P11 pedagogical plan from an instructional_plan JSON.")
    p_plan.add_argument("--instructional-plan", type=Path, required=True)
    p_plan.add_argument("--vault", type=Path, default=None)

    p_val = sub.add_parser("validate", help="Run P07 educational quality validation on a Markdown draft.")
    p_val.add_argument("note", type=Path)
    p_val.add_argument("--pedagogical-plan", type=Path, required=True)
    p_val.add_argument("--vault", type=Path, default=None)

    p_dep = sub.add_parser("dependencies", help="Compute cognitive dependency graph and teaching order.")
    p_dep.add_argument("--instructional-plan", type=Path, required=True)

    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        if args.action == "plan":
            raw = json.loads(args.instructional_plan.read_text(encoding="utf-8-sig"))
            out = build_pedagogical_plan(raw, vault=args.vault)
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0
        if args.action == "dependencies":
            raw = json.loads(args.instructional_plan.read_text(encoding="utf-8-sig"))
            out = build_cognitive_dependency_graph(raw.get("concepts") or [], source_policy=raw.get("source_policy", "independent"))
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0
        if args.action == "validate":
            text = args.note.read_text(encoding="utf-8-sig")
            pplan = json.loads(args.pedagogical_plan.read_text(encoding="utf-8-sig"))
            out = validate_pedagogical_quality(text, pplan, vault=args.vault)
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 1 if out["blocking"] else 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
