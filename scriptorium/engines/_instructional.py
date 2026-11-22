"""Validate, normalize, compose, and audit agent-authored instructional decisions; no model calls."""
from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlsplit

from scriptorium.models import REPO_ROOT, normalize_stack

CONTRACT_VERSION = 3

SOURCE_MODULES = {
    "equation": ("mathematics", "math", 2), "formula": ("mathematics", "math", 2),
    "derivation": ("derivation", "math", 4), "proof": ("proof", "math", 5),
    "figure": ("visualization", "visual", 2), "table": ("visualization", "visual", 2),
    "example": ("examples", "practice", 3), "exercise": ("assessment", "assessment", 3),
    "algorithm": ("algorithm", "theory", 3), "qualification": ("limitations", "theory", 2),
}

DIMENSION_ALIASES = {
    "math": "math",
    "mathematical": "math",
    "code": "code",
    "coding": "code",
    "visual": "visual",
    "theory": "theory",
    "conceptual": "theory",
    "theoretical": "theory",
    "algorithmic": "theory",
    "practice": "practice",
    "examples": "practice",
    "assessment": "assessment",
}


CODE_LANG_FENCES = {
    "python", "py", "python3", "cpp", "c++", "c", "rust", "java", "go",
    "javascript", "js", "typescript", "ts", "sql", "csharp", "c#", "kotlin", "bash", "sh",
}

# Canonical pedagogical stage mapping for composing multiple subtemplates into one deduplicated sequence.
STAGE_CANONICAL = {
    "need": ("motivation_and_problem", "motivation"),
    "problem": ("motivation_and_problem", "motivation"),
    "purpose": ("motivation_and_problem", "motivation"),
    "goal": ("motivation_and_problem", "motivation"),
    "question": ("motivation_and_problem", "motivation"),
    "phenomenon": ("motivation_and_problem", "motivation"),
    "context": ("historical_context", "history"),
    "background": ("motivation_and_problem", "motivation"),
    "decision": ("motivation_and_problem", "comparison"),
    "intuition": ("intuition_and_model", "intuition"),
    "principles": ("intuition_and_model", "intuition"),
    "hypothesis": ("intuition_and_model", "intuition"),
    "definition": ("definitions_and_setup", "definitions"),
    "notation": ("definitions_and_setup", "definitions"),
    "assumptions": ("definitions_and_setup", "definitions"),
    "inputs_outputs": ("definitions_and_setup", "definitions"),
    "requirements": ("definitions_and_setup", "definitions"),
    "preparation": ("definitions_and_setup", "applications"),
    "state": ("definitions_and_setup", "algorithm"),
    "invariant": ("definitions_and_setup", "algorithm"),
    "criteria": ("definitions_and_setup", "comparison"),
    "components": ("mechanism_and_structure", "visualization"),
    "interfaces": ("mechanism_and_structure", "definitions"),
    "data_flow": ("mechanism_and_structure", "visualization"),
    "shapes": ("mechanism_and_structure", "visualization"),
    "interactions": ("mechanism_and_structure", "definitions"),
    "mechanism": ("mechanism_and_structure", "definitions"),
    "behavior": ("mechanism_and_structure", "definitions"),
    "chronology": ("chronology_and_developments", "history"),
    "developments": ("chronology_and_developments", "history"),
    "causes": ("chronology_and_developments", "history"),
    "consequences": ("chronology_and_developments", "history"),
    "relation": ("mathematical_formulation", "mathematics"),
    "justification": ("derivation_and_proof", "derivation"),
    "calculation": ("worked_application", "mathematics"),
    "algorithm": ("algorithmic_procedure", "algorithm"),
    "steps": ("algorithmic_procedure", "algorithm"),
    "intermediate_states": ("worked_application", "applications"),
    "environment": ("implementation_and_code", "coding"),
    "implementation": ("implementation_and_code", "coding"),
    "method": ("experiment_and_evidence", "experiment"),
    "experiment": ("experiment_and_evidence", "experiment"),
    "measurement": ("experiment_and_evidence", "experiment"),
    "evidence": ("experiment_and_evidence", "history"),
    "results": ("experiment_and_evidence", "experiment"),
    "examples": ("worked_application", "examples"),
    "trace": ("worked_application", "tracing"),
    "distinctions": ("comparison_and_distinctions", "definitions"),
    "shared_properties": ("comparison_and_distinctions", "comparison"),
    "differences": ("comparison_and_distinctions", "comparison"),
    "tradeoffs": ("comparison_and_distinctions", "comparison"),
    "conditional_choice": ("comparison_and_distinctions", "comparison"),
    "interpretations": ("interpretation_and_verification", "history"),
    "interpretation": ("interpretation_and_verification", "definitions"),
    "correctness": ("interpretation_and_verification", "algorithm"),
    "cost": ("interpretation_and_verification", "algorithm"),
    "tests": ("interpretation_and_verification", "coding"),
    "verification": ("interpretation_and_verification", "applications"),
    "debugging": ("limitations_and_boundaries", "coding"),
    "troubleshooting": ("limitations_and_boundaries", "applications"),
    "validity": ("limitations_and_boundaries", "mathematics"),
    "limits": ("limitations_and_boundaries", "limitations"),
    "limitations": ("limitations_and_boundaries", "limitations"),
    "edge_cases": ("limitations_and_boundaries", "limitations"),
    "bottlenecks": ("limitations_and_boundaries", "limitations"),
    "error": ("limitations_and_boundaries", "experiment"),
    "open_questions": ("revision_and_consolidation", "revision"),
}

STAGE_ORDER = [
    "prerequisite_preparation",
    "motivation_and_problem",
    "historical_context",
    "intuition_and_model",
    "definitions_and_setup",
    "mechanism_and_structure",
    "chronology_and_developments",
    "mathematical_formulation",
    "derivation_and_proof",
    "algorithmic_procedure",
    "implementation_and_code",
    "experiment_and_evidence",
    "worked_application",
    "comparison_and_distinctions",
    "interpretation_and_verification",
    "limitations_and_boundaries",
    "assessment_and_practice",
    "revision_and_consolidation",
]


def registry() -> dict[str, Any]:
    return _parse_registry((REPO_ROOT / "references/workflows/notes-creation/instructional-registry.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=4)
def _parse_registry(raw: str) -> dict[str, Any]:
    return json.loads(raw)



def _names(value: Any, allowed: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not value or any(not isinstance(v, str) or v not in allowed for v in value):
        raise ValueError(f"{field} must be a nonempty list drawn from {sorted(allowed)}")
    return list(dict.fromkeys(value))


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be nonempty text")
    return value.strip()


def _normalize_prerequisites(c: dict[str, Any], ids: list[str], seen: set[str]) -> list[dict[str, str]]:
    """Normalize prerequisites, required_prerequisites, and helpful_prerequisites into structured dependency records."""
    raw_prereqs = c.get("prerequisites")
    if raw_prereqs is None:
        raw_prereqs = []
    if not isinstance(raw_prereqs, list):
        raise ValueError("prerequisites must be a list")

    normalized: list[dict[str, str]] = []
    seen_targets: set[str] = set()

    for dep in raw_prereqs:
        if isinstance(dep, str):
            target = _text(dep, "prerequisite concept")
            entry = {"concept": target, "treatment": "explain", "kind": "required"}
        elif isinstance(dep, dict):
            treatment = dep.get("treatment")
            if treatment not in {"known", "reminder", "explain", "foundation"}:
                raise ValueError("Each prerequisite needs a concept and treatment")
            target = _text(dep.get("concept"), "prerequisite concept")
            kind = str(dep.get("kind") or ("helpful" if treatment == "reminder" else "required"))
            entry = {"concept": target, "treatment": treatment, "kind": kind}
        else:
            raise ValueError("Each prerequisite needs a concept and treatment")
        if target in ids and target not in seen:
            raise ValueError(f"Prerequisites must precede their consumers (cycle or forward dependency on '{target}')")
        if target not in seen_targets:
            seen_targets.add(target)
            normalized.append(entry)

    for field, default_treatment, kind in (
        ("required_prerequisites", "explain", "required"),
        ("helpful_prerequisites", "reminder", "helpful"),
    ):
        extra = c.get(field, [])
        if not isinstance(extra, list):
            raise ValueError(f"{field} must be a list")
        for item in extra:
            if isinstance(item, str):
                target = _text(item, field)
                treatment = default_treatment
            elif isinstance(item, dict):
                target = _text(item.get("concept"), field)
                treatment = item.get("treatment", default_treatment)
                if treatment not in {"known", "reminder", "explain", "foundation"}:
                    raise ValueError(f"Invalid prerequisite treatment in {field}")
            else:
                raise ValueError(f"Invalid prerequisite entry in {field}")
            if target in ids and target not in seen:
                raise ValueError(f"Prerequisites must precede their consumers (cycle or forward dependency on '{target}')")
            if target not in seen_targets:
                seen_targets.add(target)
                normalized.append({"concept": target, "treatment": treatment, "kind": kind})

    related = c.setdefault("related_topics", [])
    if not isinstance(related, list) or any(not isinstance(r, str) or not r.strip() for r in related):
        raise ValueError("related_topics must be a list of nonempty strings")

    c["prerequisites"] = normalized
    c["required_prerequisites"] = [d["concept"] for d in normalized if d.get("kind") != "helpful"]
    c["helpful_prerequisites"] = [d["concept"] for d in normalized if d.get("kind") == "helpful"]
    return normalized


def _should_support_module(
    name: str,
    c: dict[str, Any],
    depth: dict[str, int],
    total_concepts: int,
) -> tuple[bool, str]:
    """Selective supporting-module activation: never activate every supporting module merely because depth > 0."""
    types = set(c["types"])
    objectives = set(c["objectives"])
    prereqs = c.get("prerequisites", [])

    if name == "motivation":
        if any(dep.get("treatment") in {"explain", "foundation"} for dep in prereqs):
            return True, "prepares foundational prerequisite motivation"
        if "need" in [step for t in c["types"] for step in registry()["subtemplates"].get(t, [])]:
            return True, "conceptual/problem motivation stage"
        return False, "no selected need"

    if name == "intuition":
        if depth["theory"] >= 2 and bool(types & {"conceptual", "mathematical", "scientific", "architectural"}):
            return True, "builds mental model for conceptual/formal structure"
        return False, "no selected need"

    if name == "definitions":
        if depth["theory"] >= 1 or depth["math"] >= 1 or depth["code"] >= 1:
            return True, "establishes terminology and symbol contracts at first use"
        return False, "no selected need"

    if name == "mathematics":
        if depth["math"] >= 1 and ("mathematical" in types or bool(objectives & {"calculate", "derive", "prove"})):
            return True, "supports selected mathematical relation"
        if depth["math"] >= 2:
            return True, "explicit quantitative depth profile"
        return False, "no selected need"

    if name == "visualization":
        visuals = c.get("visualizations") or []
        if visuals:
            return True, "explicit concept visualization planned"
        if "architectural" in types and depth["visual"] >= 2:
            return True, "architectural component and flow diagram"
        return False, "no specific visual relationship selected"

    if name == "coding":
        impl = c.get("implementation") or {}
        if impl.get("required") or (depth["code"] >= 2 and ("programming" in types or bool(objectives & {"implement", "debug"}))):
            return True, "executable implementation selected for concept"
        return False, "no executable implementation needed"

    if name == "examples":
        if depth["practice"] >= 2 and (
            bool(types & {"conceptual", "mathematical", "scientific", "programming", "algorithmic", "procedural"})
            or bool(objectives & {"explain", "calculate", "apply", "implement", "trace"})
        ):
            return True, "concrete worked case clarifies mechanism"
        return False, "no selected need"

    if name == "limitations":
        if depth["theory"] >= 3 and bool(types & {"mathematical", "algorithmic", "architectural", "scientific", "comparative", "procedural"}):
            return True, "documents assumptions and validity boundaries"
        return False, "no selected need"

    if name == "assessment":
        if depth["assessment"] >= 2:
            return True, "verifies observable concept objective"
        return False, "no selected need"

    if name == "revision":
        if total_concepts > 1 or depth["theory"] >= 4:
            return True, "consolidates retrieval cues across dependencies"
        return False, "no selected need"

    return False, "no selected need"


def compose_concept_sequence(concept: dict[str, Any], reg: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Compose one or more knowledge-type subtemplates into one deduplicated, ordered explanation sequence."""
    reg = reg or registry()
    modules = concept.get("modules", {})
    types = concept.get("types", [])
    prereqs = concept.get("prerequisites", [])

    stage_entries: dict[str, dict[str, Any]] = {}

    # 1. Prerequisite handling before main concept steps if needed
    active_prereqs = [p for p in prereqs if p.get("treatment") in {"reminder", "explain", "foundation"}]
    if active_prereqs:
        stage_entries["prerequisite_preparation"] = {
            "stage": "prerequisite_preparation",
            "module": "definitions",
            "source_steps": [f"prerequisite:{p['concept']}({p['treatment']})" for p in active_prereqs],
            "types": list(types),
        }

    # 2. Merge steps from all selected subtemplates without repeating introductions or definitions
    for kind in types:
        for raw_step in reg["subtemplates"].get(kind, []):
            canonical_stage, gov_module = STAGE_CANONICAL.get(raw_step, ("mechanism_and_structure", "definitions"))
            # adjust governing module for derivation vs proof
            if canonical_stage == "derivation_and_proof":
                if modules.get("proof", {}).get("status") in {"required", "supporting"}:
                    gov_module = "proof"
                elif modules.get("derivation", {}).get("status") in {"required", "supporting"}:
                    gov_module = "derivation"
                else:
                    gov_module = "mathematics"
            mod_state = modules.get(gov_module, {}).get("status", "excluded")
            # Prune stages whose governing module is excluded (unless it's a core definition/mechanism step with active theory)
            if mod_state == "excluded":
                if canonical_stage in {"definitions_and_setup", "mechanism_and_structure"} and concept["depth"].get("theory", 0) > 0:
                    gov_module = "definitions"
                else:
                    continue
            if canonical_stage not in stage_entries:
                stage_entries[canonical_stage] = {
                    "stage": canonical_stage,
                    "module": gov_module,
                    "source_steps": [raw_step],
                    "types": [kind],
                }
            else:
                if raw_step not in stage_entries[canonical_stage]["source_steps"]:
                    stage_entries[canonical_stage]["source_steps"].append(raw_step)
                if kind not in stage_entries[canonical_stage]["types"]:
                    stage_entries[canonical_stage]["types"].append(kind)

    # 3. Ensure explicitly required/supporting modules that were not part of the raw subtemplate list are represented once
    MODULE_TO_STAGE = {
        "motivation": "motivation_and_problem",
        "history": "historical_context",
        "intuition": "intuition_and_model",
        "definitions": "definitions_and_setup",
        "visualization": "mechanism_and_structure",
        "mathematics": "mathematical_formulation",
        "derivation": "derivation_and_proof",
        "proof": "derivation_and_proof",
        "algorithm": "algorithmic_procedure",
        "coding": "implementation_and_code",
        "experiment": "experiment_and_evidence",
        "examples": "worked_application",
        "tracing": "worked_application",
        "applications": "worked_application",
        "comparison": "comparison_and_distinctions",
        "limitations": "limitations_and_boundaries",
        "assessment": "assessment_and_practice",
        "revision": "revision_and_consolidation",
    }
    for mod_name, choice in modules.items():
        if choice.get("status") in {"required", "supporting"}:
            st = MODULE_TO_STAGE.get(mod_name)
            if st and st not in stage_entries:
                stage_entries[st] = {
                    "stage": st,
                    "module": mod_name,
                    "source_steps": [mod_name],
                    "types": list(types),
                }

    ordered = [stage_entries[st] for st in STAGE_ORDER if st in stage_entries]
    return ordered


def build_concept_dependency_graph(plan: dict[str, Any]) -> dict[str, Any]:
    """Validate and construct the prerequisite-aware concept dependency graph."""
    concepts = plan.get("concepts", [])
    ids = [c["id"] for c in concepts]
    id_set = set(ids)
    index_map = {cid: idx for idx, cid in enumerate(ids)}

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []
    external_prerequisites: list[dict[str, str]] = []

    adj: dict[str, list[str]] = {cid: [] for cid in ids}

    for idx, c in enumerate(concepts):
        cid = c["id"]
        nodes.append({
            "id": cid,
            "title": c["title"],
            "order": idx + 1,
            "types": c["types"],
            "required_prerequisites": c.get("required_prerequisites", []),
            "helpful_prerequisites": c.get("helpful_prerequisites", []),
            "related_topics": c.get("related_topics", []),
        })
        for dep in c.get("prerequisites", []):
            target = dep["concept"]
            treatment = dep["treatment"]
            kind = dep.get("kind", "required")
            if target in id_set:
                if index_map[target] >= idx:
                    raise ValueError(f"Prerequisites must precede their consumers (cycle or forward dependency: '{target}' -> '{cid}')")
                adj[target].append(cid)
                edges.append({
                    "from": target,
                    "to": cid,
                    "treatment": treatment,
                    "kind": kind,
                    "relation": "conceptual_prerequisite",
                })
            else:
                external_prerequisites.append({
                    "concept": target,
                    "consumer": cid,
                    "treatment": treatment,
                    "kind": kind,
                })

    return {
        "nodes": nodes,
        "edges": edges,
        "external_prerequisites": external_prerequisites,
        "sequential_order": ids,
    }


def compose_document_outline(plan: dict[str, Any], reg: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a unified, non-duplicative document composition plan across all concepts."""
    reg = reg or registry()
    concepts = plan.get("concepts", [])
    canonical_homes: dict[str, str] = {}
    concept_sections: list[dict[str, Any]] = []

    for idx, c in enumerate(concepts, 1):
        cid = c["id"]
        canonical_homes[f"concept:{cid}"] = cid
        for mod_name, choice in c.get("modules", {}).items():
            if choice.get("status") in {"required", "supporting"}:
                canonical_homes.setdefault(f"module:{mod_name}:{cid}", cid)
        sequence = c.get("composed_sequence") or compose_concept_sequence(c, reg)
        transition = (
            f"Builds on {', '.join(p['concept'] for p in c['prerequisites'])} to establish {c['title']}."
            if c.get("prerequisites")
            else f"Establishes the foundational model for {c['title']}."
        )
        concept_sections.append({
            "concept_id": cid,
            "title": c["title"],
            "order": idx,
            "dominant_subtemplate": c["types"][0],
            "merged_subtemplates": c["types"][1:],
            "transition": transition,
            "stages": [s["stage"] for s in sequence],
        })

    return {
        "master_template": "deepstudy-master",
        "concept_sections": concept_sections,
        "canonical_homes": canonical_homes,
        "deduplicated": True,
    }


def normalize_plan(raw: dict[str, Any]) -> dict[str, Any]:
    """Resolve objective floors, selective module activation, composed sequences, and coverage assignments.

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
    ids: list[str] = []
    for c in concepts:
        if not isinstance(c, dict):
            raise ValueError("Each concept must be an object")
        ident = _text(c.get("id"), "concept id")
        if not re.fullmatch(r"[a-zA-Z0-9][\w-]*", ident) or ident in ids:
            raise ValueError("Concept IDs must be unique identifiers")
        ids.append(ident)
    seen: set[str] = set()
    total_concepts = len(concepts)
    for c in concepts:
        _text(c.get("title"), "concept title")
        if "reason" in c or "justification" not in c:
            c["reason"] = _text(c.get("reason"), "concept reason")
        else:
            c["reason"] = _text(c.get("justification"), "concept reason")

        raw_types = c.get("types") or c.get("knowledge_types") or c.get("subtemplates")
        c["types"] = _names(raw_types, reg["subtemplates"], "types")
        c["knowledge_types"] = list(c["types"])
        c["subtemplates"] = list(c["types"])

        c["objectives"] = _names(c.get("objectives"), reg["objectives"], "objectives")
        prerequisites = _normalize_prerequisites(c, ids, seen)
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
        for raw_dim, value in overrides.items():
            dimension = DIMENSION_ALIASES.get(str(raw_dim).strip().lower())
            if dimension not in depth or type(value) is not int or value not in range(6):
                raise ValueError("Depth dimensions must have integer levels 0 through 5")
            if value < depth[dimension]:
                raise ValueError(f"{c['id']}: {dimension} conflicts with a required objective/type")
            depth[dimension] = value
        c["depth"] = depth

        # Normalize concept-level implementation & visualizations if provided
        raw_impl = c.get("implementation")
        if raw_impl is not None and not isinstance(raw_impl, dict):
            raise ValueError("concept implementation must be an object")
        if isinstance(raw_impl, dict):
            if raw_impl.get("required") and depth["code"] < 2:
                raise ValueError(f"{c['id']}: implementation.required=True conflicts with code depth {depth['code']} (< 2)")
            c["implementation"] = deepcopy(raw_impl)
        else:
            c["implementation"] = {
                "required": depth["code"] >= 2,
                "code_depth": (
                    "none" if depth["code"] == 0 else
                    "pseudocode" if depth["code"] == 1 else
                    "minimal" if depth["code"] == 2 else
                    "complete" if depth["code"] == 3 else
                    "from-scratch"
                ),
            }

        raw_vis = c.get("visualizations", [])
        if not isinstance(raw_vis, list) or any(not isinstance(v, dict) for v in raw_vis):
            raise ValueError("concept visualizations must be a list of objects")
        c["visualizations"] = deepcopy(raw_vis)

        modules: dict[str, dict[str, Any]] = {}
        for name, spec in reg["modules"].items():
            level = depth[spec["dimension"]]
            required = bool(
                name in source_required
                or set(spec["required_for"]) & set(c["objectives"])
                or set(spec["types"]) & set(c["types"])
            )
            if required:
                status = "required"
                reason = "source inventory requirement" if name in source_required else "objective/type requirement"
            elif level and spec["supporting"]:
                should_support, sup_reason = _should_support_module(name, c, depth, total_concepts)
                status = "supporting" if should_support else "excluded"
                reason = sup_reason
            else:
                status = "excluded"
                reason = "no selected need"
            modules[name] = {
                "status": status,
                "depth": level if status != "excluded" else 0,
                "reason": reason,
            }

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
                    modules[dep] = {
                        "status": "required",
                        "depth": max(2, depth[reg["modules"][dep]["dimension"]]),
                        "reason": f"dependency of {name}",
                    }
                    depth[reg["modules"][dep]["dimension"]] = modules[dep]["depth"]
                pending.append(dep)

        c["modules"] = modules
        c["sequence_candidates"] = {kind: reg["subtemplates"][kind] for kind in c["types"]}
        c["composed_sequence"] = compose_concept_sequence(c, reg)
        # Soft sizing heuristic, not a token counter or output cap.
        c["estimated_output_tokens"] = 180 + 90 * sum(depth.values()) + 120 * sum(
            dep["treatment"] in {"explain", "foundation"} for dep in prerequisites
        )

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

    result["dependency_graph"] = build_concept_dependency_graph(result)
    result["composed_outline"] = compose_document_outline(result, reg)
    result["version"] = CONTRACT_VERSION
    result["estimated_output_tokens"] = sum(c["estimated_output_tokens"] for c in concepts)
    return result


def resolve_instructional_contract(
    request: str,
    topic: str,
    raw_plan: dict[str, Any],
    *,
    item: dict[str, Any] | None = None,
    source_inventory: list[dict[str, Any]] | None = None,
    research_plan: dict[str, Any] | None = None,
    evidence_registry: dict[str, Any] | None = None,
    learning_resources: dict[str, Any] | None = None,
    pedagogical_plan: dict[str, Any] | None = None,
    vault: Path | None = None,
) -> dict[str, Any]:
    """Authoritative modern contract resolver for adaptive deep-study notes (Contract v3).

    Never calls from_legacy() or applies subject/domain math ceilings, topic-keyword
    multi-framework stacks, or regex visual modalities.
    Integrates optional ARRIE research plans, verified evidence packages, and
    curated learning resources while keeping the instructional planner authoritative
    for educational structure.
    """
    if not isinstance(raw_plan, dict):
        raise ValueError("New deep-note generation requires a structured instructional_plan object.")
    item = item or {}
    plan_input = deepcopy(raw_plan)
    if source_inventory is not None and "sources" not in plan_input:
        plan_input["sources"] = deepcopy(source_inventory)

    plan = normalize_plan(plan_input)
    concepts = plan["concepts"]
    depths = {dim: max(c["depth"][dim] for c in concepts) for dim in registry()["dimensions"]}
    concept_depths = {c["id"]: deepcopy(c["depth"]) for c in concepts}

    # Explicit stack from item or concept-level implementation specifications
    override = item.get("implementation_stack")
    if override is not None:
        override = normalize_stack(override)
    req_lang = str(item.get("language") or "none").strip().lower()

    concept_stacks: list[str] = []
    for c in concepts:
        impl = c.get("implementation") or {}
        chosen = impl.get("framework") or impl.get("language")
        if isinstance(chosen, str) and chosen.strip().lower() not in {"", "none"}:
            for s in normalize_stack([chosen]):
                if s not in concept_stacks:
                    concept_stacks.append(s)

    if depths["code"] < 2:
        if override:
            raise ValueError("Explicit implementation stack conflicts with a non-executable instructional profile")
        if concept_stacks:
            raise ValueError("Concept implementation language/framework conflicts with non-executable code depth (< 2)")
        code_depth = "pseudocode" if depths["code"] == 1 else "none"
        language = "none"
        implementation_stack: list[str] = []
        verify_stack = False
    else:
        if override is not None:
            selected = override
        elif concept_stacks:
            selected = concept_stacks
        elif req_lang not in {"", "none"}:
            selected = normalize_stack([req_lang])
        else:
            selected = ["python"]
        if not selected:
            raise ValueError("Executable code objective conflicts with an empty implementation stack")
        primary = selected[0]
        language = "python" if primary in {"python-numpy", "scikit-learn", "pytorch", "tensorflow-keras"} else primary
        code_depth = "from-scratch" if depths["code"] >= 4 else "illustrative"
        implementation_stack = selected
        verify_stack = True
        for c in concepts:
            if c["depth"]["code"] >= 2:
                c["implementation"] = {
                    "required": True,
                    "language": language,
                    "framework": primary,
                    "approach": "from-scratch" if c["depth"]["code"] >= 4 else "complete" if c["depth"]["code"] == 3 else "minimal",
                    "reason": c["implementation"].get("reason") or c["reason"],
                }

    visualizations = [
        {**v, "concept": v.get("concept") or c["id"]}
        for c in concepts
        for v in (c.get("visualizations") or [])
    ]
    visual_modality = "concept-specific" if (visualizations or depths["visual"] > 0) else "none"

    active_required = sorted({
        name
        for c in concepts
        for name, choice in c["modules"].items()
        if choice["status"] == "required"
    })
    active_supporting = sorted({
        name
        for c in concepts
        for name, choice in c["modules"].items()
        if choice["status"] == "supporting"
    })
    omitted_sections = ["code_verification"] if depths["code"] < 2 else []
    forbidden_patterns = [
        "legacy_section_comments",
        "bare_root_domain_citations",
        "obsolete_matrix_references",
        "authoring_gate_callouts",
        "decision_contract_comments",
    ]
    if depths["code"] < 2:
        forbidden_patterns.extend(["fenced_code_blocks", "execution_claims"])
    if all(c["depth"]["math"] == 0 for c in concepts):
        forbidden_patterns.append("display_math_in_all_m0_profile")

    # math_level is retained strictly as a read-only derived summary for CLI/practice consumers;
    # per-concept depths in concept_depths and instructional_plan are authoritative.
    derived_math_level = (0, 0, 1, 1, 2, 3)[depths["math"]]

    contract = {
        "contract_version": CONTRACT_VERSION,
        "route": "deepstudy-master",
        "template": "deepstudy-master",
        "audience": plan["audience"],
        "source_policy": plan["source_policy"],
        "instructional_plan": plan,
        "concept_depths": concept_depths,
        "dependency_graph": plan["dependency_graph"],
        "composed_outline": plan["composed_outline"],
        "domain": "adaptive",
        "subject_family": "adaptive",
        "math_level": derived_math_level,
        "require_math_floor": False,
        "code_depth": code_depth,
        "language": language,
        "implementation_stack": implementation_stack,
        "verify_stack": verify_stack,
        "visual_modality": visual_modality,
        "visualizations": visualizations,
        "max_qa_items": None,
        "required_sections": active_required,
        "supporting_sections": active_supporting,
        "omitted_sections": omitted_sections,
        "forbidden_patterns": forbidden_patterns,
    }

    # Optional ARRIE Research & Resource Intelligence integration (never overrides instructional structure)
    raw_rp = research_plan if research_plan is not None else item.get("research_plan")
    raw_er = evidence_registry if evidence_registry is not None else item.get("evidence_registry")
    raw_lr = learning_resources if learning_resources is not None else item.get("learning_resources")
    explicit_rmode = item.get("research_mode")
    if raw_rp is not None or raw_er is not None or raw_lr is not None or explicit_rmode is not None:
        from scriptorium.engines.research import (
            build_research_package,
            normalize_evidence_registry,
            normalize_research_plan,
            plan_research,
        )

        norm_rp = (
            normalize_research_plan(raw_rp)
            if raw_rp is not None
            else plan_research(topic, plan, request=request, explicit_mode=explicit_rmode)
        )
        norm_er = (
            normalize_evidence_registry(raw_er, research_plan=norm_rp, mode=norm_rp["mode"])
            if raw_er is not None
            else normalize_evidence_registry({"sources": [], "evidence": []}, research_plan=norm_rp, mode=norm_rp["mode"])
        )
        package = build_research_package(norm_rp, norm_er, learning_resources=raw_lr)
        contract["research_mode"] = norm_rp["mode"]
        contract["research_plan"] = norm_rp
        contract["evidence_registry"] = norm_er
        contract["research_package"] = package
        if raw_lr is not None:
            contract["learning_resources"] = raw_lr

    # Optional Pedagogical Intelligence Layer (P01-P11) — enriches Contract v3 without overriding instructional authority
    ped_keys = {"canonical_spec", "example_plan", "misconception_plan", "connection_plan", "explanation_plan", "detail_profile", "dependency_plan"}
    has_ped_hints = any(ped_keys & set(c.keys()) for c in concepts) or bool(item.get("include_pedagogical_plan"))
    raw_pp = pedagogical_plan if pedagogical_plan is not None else item.get("pedagogical_plan")
    if raw_pp is not None or has_ped_hints:
        from scriptorium.engines._pedagogical_core import build_pedagogical_plan

        contract["pedagogical_plan"] = (
            deepcopy(raw_pp)
            if isinstance(raw_pp, dict)
            else build_pedagogical_plan(plan, vault=vault)
        )

    return contract


def audit_modern_note(note_text: str, contract: dict[str, Any]) -> list[tuple[int, str]]:
    """Audit an authored deep-study note against its modern adaptive contract (v2/v3)."""
    from scriptorium.engines._verification import required_examples, split_blocks

    findings: list[tuple[int, str]] = []
    blocks, lines = split_blocks(note_text)
    plan = contract.get("instructional_plan") or {}
    concepts = plan.get("concepts") or []
    code_depth = contract.get("code_depth", "none")

    legacy_section_re = re.compile(r"<!--\s*SECTION:\s*S\d+[^>]*-->", re.I)
    obsolete_matrix_re = re.compile(r"(?:shared/notes?_decision_matrix\.md|templates/notes_decision_matrix\.md|\bDecision-matrix IDs:)", re.I)
    exec_claim_re = re.compile(
        r"\b(?:(?:was\s+)?(?:\*\*)?executed(?:\*\*)?\s+via|observed\s+execution\s+output|all\s+assertions\s+passed)\b",
        re.I,
    )
    markdown_link_re = re.compile(r"\[[^\]]+\]\((https?://[^)\s]+)\)")
    display_math_re = re.compile(r"(?<![\\$])\$\$(?!\$)(.+?)(?<![\\$])\$\$(?!\$)", re.S)

    for idx, line in enumerate(note_text.splitlines(), 1):
        if legacy_section_re.search(line):
            findings.append((idx, "Legacy <!-- SECTION: S* --> marker is forbidden; use adaptive headings."))
        if obsolete_matrix_re.search(line):
            findings.append((idx, "Obsolete decision-matrix reference is forbidden in authored notes."))

    max_code_depth = max((c.get("depth", {}).get("code", 0) for c in concepts), default=0 if code_depth == "none" else 3)
    enforce_no_code = (max_code_depth < 2 or code_depth in {"none", "pseudocode"}) and bool(contract.get("explicit_contract") or concepts)
    has_code_fence = any(block.lang in CODE_LANG_FENCES for block in blocks)
    for block in blocks:
        if enforce_no_code and block.lang in CODE_LANG_FENCES:
            findings.append((block.line, f"Executable '{block.lang}' code block conflicts with non-executable concept profile (C0/C1)."))

    if (contract.get("explicit_contract") or concepts) and concepts and all(c.get("depth", {}).get("math", 0) == 0 for c in concepts):
        visible = "\n".join(re.sub(r"`[^`]+`", "", line.lstrip("> ")) for line in lines)
        if display_math_re.search(visible):
            findings.append((1, "Display mathematics conflicts with the saved all-M0 instructional profile."))

    stack = contract.get("implementation_stack", [])
    if stack and contract.get("verify_stack", True):
        _, missing = required_examples(blocks, stack, minimum_lines=1)
        findings.extend(missing)
        if len(stack) > 1:
            if not any(re.match(r"^(?:\*\*)?Shared fixture(?:\*\*)?:(?:\*\*)?\s*\S", line, re.I) for line in lines):
                findings.append((1, "Multi-stack comparison requires documenting shared inputs and parameters in a Shared fixture: field."))
            header = next((idx for idx, line in enumerate(lines) if re.match(
                r"^\s*\|\s*(?:Framework|Language|Stack)\s*\|\s*Exposes\s*\|\s*Hides\s*\|\s*(?:Main\s+)?Pitfall\s*\|\s*$", line, re.I
            )), None)
            rows = {}
            if header is not None:
                for line in lines[header + 2:]:
                    if not line.lstrip().startswith("|"):
                        break
                    cells = [cell.strip().strip("`") for cell in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
                    if len(cells) == 4 and all(cells):
                        rows[cells[0].lower()] = cells[1:]
            if not set(stack) <= rows.keys():
                findings.append((1, "Multi-stack comparison requires a Framework or Language table with Exposes, Hides and Pitfall columns for each stack."))

    if code_depth in {"none", "pseudocode"} or not has_code_fence:
        for idx, line in enumerate(lines, 1):
            if exec_claim_re.search(line):
                findings.append((idx, "Execution claim is forbidden when code_depth is 'none'/'pseudocode' or no code block exists."))

    for idx, line in enumerate(lines, 1):
        for match in markdown_link_re.finditer(line):
            url = match.group(1)
            parsed = urlsplit(url)
            if parsed.path in ("", "/"):
                findings.append((idx, f"Bare root-domain citation '{url}' is not a specific source link."))

    if contract.get("evidence_registry"):
        from scriptorium.engines.research import validate_note_citations

        findings.extend(
            validate_note_citations(
                note_text,
                contract["evidence_registry"],
                mode=contract.get("research_mode", "R-I"),
                learning_resources=contract.get("learning_resources")
                or (contract.get("research_package") or {}).get("learning_resources"),
            )
        )

    if contract.get("pedagogical_plan"):
        from scriptorium.engines._pedagogical_core import validate_pedagogical_quality

        ped_report = validate_pedagogical_quality(note_text, contract["pedagogical_plan"])
        for issue in ped_report["issues"]:
            if issue["severity"] in {"critical", "major"}:
                findings.append((1, f"{issue['issue_id']} ({issue['severity']}): {issue['description']}"))

    return findings


def coverage_errors(plan: dict[str, Any], report: dict[str, Any] | None, draft: str) -> list[str]:
    """Check inventory receipts structurally; the author still verifies evidence."""
    sources = {s["id"]: s for s in plan.get("sources", [])}
    if not sources and report is None:
        return []
    elements = report.get("elements") if isinstance(report, dict) else None
    if not isinstance(elements, list):
        return ["Source coverage requires an elements report"]
    # Mask fenced code so a heading inside an example cannot pass as coverage.
    from scriptorium.engines._verification import split_blocks
    _, prose = split_blocks(draft)
    from scriptorium.models import heading_slug
    anchors = {heading_slug(m[1]) for line in prose if (m := re.match(r"^#{1,6}\s+(.+)$", line))}
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
        positions = {heading_slug(m[1]): i for i, line in enumerate(prose) if (m := re.match(r"^#{1,6}\s+(.+)$", line))}
        order = [positions[receipts[sid]["anchor"]] for sid, source in sources.items()
                 if source["required"] and sid in receipts and receipts[sid].get("anchor") in positions]
        if order != sorted(order):
            errors.append("Source order differs from the required inventory sequence")
    return errors


# ---------------------------------------------------------------------------
# Isolated Legacy Compatibility Adapter (never silently called)
# ---------------------------------------------------------------------------

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
