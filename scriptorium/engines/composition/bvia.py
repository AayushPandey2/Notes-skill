"""BVIA — Beginner-First Visual Intelligence Architecture inside UMRIA.

Evaluates visual cognitive accessibility, ranks external image candidates with
hard accuracy/licensing constraints, orders progressive visual learning ladders
(Levels 0-6), and enforces Explain -> Show -> Decode -> Connect composition.
"""
from __future__ import annotations

import re
from typing import Any

ACCESSIBILITY_CLASSES = (
    "beginner_friendly",
    "guided_intermediate",
    "advanced_technical",
    "unsuitable",
)

PROGRESSION_LEVELS = {
    0: "orientation",
    1: "simple_conceptual",
    2: "component_identification",
    3: "step_by_step_mechanism",
    4: "technical_representation",
    5: "advanced_integrated_view",
    6: "analysis",
}


def evaluate_visual_accessibility(candidate: dict[str, Any]) -> dict[str, Any]:
    """Heuristically classify visual comprehension difficulty and readability."""
    if candidate.get("technical_accuracy") is False:
        return {
            "classification": "unsuitable",
            "reason": "Candidate fails mandatory technical accuracy check",
            "score": 0,
            "legible_at_embed_width": False,
        }
    if candidate.get("text_readability") == "illegible":
        return {
            "classification": "unsuitable",
            "reason": "Text is illegible at expected viewing width",
            "score": 0,
            "legible_at_embed_width": False,
        }

    width = int(candidate.get("width") or 800)
    height = int(candidate.get("height") or 500)
    embedded_width = int(candidate.get("embedded_width_px") or 600)
    legible = width >= 320 and height >= 180 and (embedded_width <= width * 1.5)
    if not legible:
        return {
            "classification": "unsuitable",
            "reason": f"Insufficient resolution ({width}x{height}) for embedded width {embedded_width}px",
            "score": 0,
            "legible_at_embed_width": False,
        }

    components = int(candidate.get("labeled_components") or 4)
    unexplained_abbr = int(candidate.get("unexplained_abbreviations") or 0)
    undefined_syms = int(candidate.get("undefined_symbols") or 0)
    prereq_burden = int(candidate.get("prerequisite_burden") or 0)
    arrow_penalty = {"low": 0, "medium": 2, "high": 5}.get(candidate.get("arrow_density", "low"), 2)
    clutter_penalty = {"low": 0, "medium": 2, "high": 5}.get(candidate.get("diagram_clutter", "low"), 2)

    burden = (
        max(0, components - 5)
        + unexplained_abbr * 2
        + undefined_syms * 2
        + prereq_burden
        + arrow_penalty
        + clutter_penalty
    )
    if burden <= 3:
        classification = "beginner_friendly"
    elif burden <= 8:
        classification = "guided_intermediate"
    else:
        classification = "advanced_technical"

    return {
        "classification": classification,
        "burden_score": burden,
        "legible_at_embed_width": True,
        "requires_walkthrough": classification != "beginner_friendly",
    }


def rank_image_candidates(
    candidates: list[dict[str, Any]],
    *,
    learner_level: str = "beginner",
    existing_roles: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Rank candidates with technical accuracy & licensing as hard constraints."""
    from .media import verify_license_and_rights

    seen_roles = set(existing_roles or ())
    accepted: list[dict[str, Any]] = []
    for cand in candidates:
        if cand.get("technical_accuracy") is False:
            continue
        rights = cand.get("rights", "")
        try:
            verify_license_and_rights(rights, require_permissive=True)
        except ValueError:
            continue
        access = evaluate_visual_accessibility(cand)
        if access["classification"] == "unsuitable":
            continue

        cls = access["classification"]
        if learner_level == "beginner":
            fit = {"beginner_friendly": 30, "guided_intermediate": 18, "advanced_technical": 5}[cls]
        elif learner_level == "intermediate":
            fit = {"guided_intermediate": 30, "beginner_friendly": 20, "advanced_technical": 15}[cls]
        else:
            fit = {"advanced_technical": 30, "guided_intermediate": 22, "beginner_friendly": 12}[cls]

        role = cand.get("educational_role", "")
        duplicate_penalty = -15 if role and role in seen_roles else 0
        relevance_bonus = int(cand.get("relevance_score", 10))
        total = fit + relevance_bonus + duplicate_penalty
        accepted.append({**cand, "accessibility": access, "rank_score": total})

    accepted.sort(key=lambda item: item["rank_score"], reverse=True)
    return accepted


def plan_progressive_visuals(visuals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Order visuals along the Levels 0-6 progressive learning ladder."""
    class_order = {"beginner_friendly": 0, "guided_intermediate": 1, "advanced_technical": 2, "unsuitable": 3}

    def key(v: dict[str, Any]) -> tuple[int, int]:
        level = int(v.get("progression_level", 2))
        cls = v.get("accessibility", {}).get("classification", "guided_intermediate")
        return (level, class_order.get(cls, 1))

    return sorted(visuals, key=key)


def compose_visual_walkthrough(
    visual: dict[str, Any],
    *,
    embed: str,
    terminology_registry: dict[str, str] | None = None,
    inspection: dict[str, Any] | None = None,
) -> str:
    """Assemble Explain -> Show -> Decode -> Connect prose grounded in inspected image content."""
    registry = terminology_registry or {}
    explain = visual.get("explain") or f"To understand {visual.get('objective', 'this mechanism')}, examine how the key parts interact in the figure below."
    verified_labels = list((inspection or {}).get("text_labels_extracted") or [])
    decode_items = list(visual.get("decode_components") or [])
    if not decode_items:
        if verified_labels:
            decode_items = [f"Inspect the verified figure labels visible in the diagram: {', '.join(verified_labels[:6])}."]
        else:
            decode_items = [
                f"Focus on the relationship described in the caption: {visual.get('alt') or visual.get('objective', 'core structural arrangement')}."
            ]
    abbrs = [a for a in visual.get("abbreviations", []) if a in registry]
    abbr_lines = [f"- **{a}:** {registry[a]}" for a in abbrs]
    connect = visual.get("connect") or "This visual structure connects directly to the analytical mechanism developed next."

    parts = [
        explain.strip(),
        "",
        embed.strip(),
        "",
        f"*Figure: {visual.get('alt') or visual.get('objective', 'Visual explanation')}.*",
        "",
        "**How to read this figure:**",
        *[f"- {item}" for item in decode_items],
    ]
    if abbr_lines:
        parts.extend(["", "**Symbols and abbreviations:**", *abbr_lines])
    parts.extend(["", connect.strip()])
    return "\n".join(parts)


def validate_image_grounded_explanation(
    markdown: str,
    visual: dict[str, Any],
    *,
    inspection: dict[str, Any] | None = None,
    terminology_registry: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Verify Explain -> Show -> Decode -> Connect and image-inspection grounding."""
    result = validate_explain_show_decode_connect(
        markdown, visual, terminology_registry=terminology_registry
    )
    errors = list(result["errors"])
    warnings: list[str] = []
    inspected = bool(inspection and inspection.get("inspection_performed"))
    if inspection and inspection.get("readable_for_embedding") is False:
        errors.append("Inspected image failed minimum resolution/contrast readability check")
    if not inspected and visual.get("decode_components"):
        warnings.append("Image decode components supplied without recorded local image inspection")
    return {
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "image_inspected": inspected,
    }


def validate_explain_show_decode_connect(
    markdown: str,
    visual: dict[str, Any],
    *,
    terminology_registry: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Verify Explain -> Show -> Decode -> Connect and abbreviation definitions."""
    errors: list[str] = []
    embed_match = re.search(r"(!\[\[[^\]]+\]\]|!\[[^\]]*\]\([^)]+\))", markdown)
    if not embed_match:
        return {"passed": False, "errors": ["Missing visual embed"]}

    before = markdown[:embed_match.start()].strip()
    after = markdown[embed_match.end():].strip()
    if len(before.split()) < 6:
        errors.append("Missing Explain introduction before figure")
    if len(after.split()) < 10:
        errors.append("Missing Decode/Connect walkthrough after figure")

    registry = terminology_registry or {}
    for abbr in visual.get("abbreviations", []):
        if abbr not in markdown and abbr not in registry:
            errors.append(f"Unexplained abbreviation in diagram: {abbr}")
        elif abbr in visual.get("abbreviations", []) and abbr in registry and abbr not in markdown:
            errors.append(f"Abbreviation {abbr} missing from chapter text")

    return {"passed": not errors, "errors": errors}


def build_visual_teaching_contract(
    *,
    visual_id: str,
    concept_id: str,
    learner_level: str = "beginner",
    purpose: str,
    prerequisite_concepts: list[str] | None = None,
    progression_level: int = 1,
    preferred_type: str = "architecture_diagram",
    required_labels: list[str] | None = None,
) -> dict[str, Any]:
    """Create a canonical BVIA + UMRIA + LAVIA visual teaching contract."""
    if progression_level not in PROGRESSION_LEVELS:
        raise ValueError(f"Invalid progression_level {progression_level}; expected 0..6")
    return {
        "visual_id": visual_id,
        "concept_id": concept_id,
        "educational": {
            "learner_level": learner_level,
            "purpose": purpose,
            "prerequisite_concepts": list(prerequisite_concepts or []),
            "progression_level": PROGRESSION_LEVELS[progression_level],
        },
        "representation": {
            "preferred_type": preferred_type,
            "acquisition_priority": "external_first",
            "required_labels": list(required_labels or []),
        },
        "selection": {
            "candidate_status": "pending",
            "accessibility_review": "required",
            "technical_review": "required",
        },
        "asset": {
            "acquisition_status": "pending",
            "local_path": None,
            "content_hash": None,
        },
        "publication": {
            "chapter_id": None,
            "section_id": None,
            "embed_status": "pending",
        },
    }
