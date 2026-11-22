"""Deterministic chapter allocation for the existing composition plan.

Workload units are transparent planning estimates, not measured reading time or
a claim that a chapter is pedagogically complete. Authored content and the
existing educational obligations still require separate review.
"""
from __future__ import annotations

from collections import Counter
import json
import math
import re
from typing import Any, Iterable

from scriptorium.models import content_hash


MIN_CHAPTERS = 5
MAX_CHAPTERS = 10
TARGET_WORKLOAD = 6.0
DEPTH_WEIGHTS = {
    "conceptual": 0.15,
    "mathematical": 0.30,
    "algorithmic": 0.25,
    "implementation": 0.40,
    "research": 0.35,
    "visual": 0.20,
    "analytical": 0.20,
}


def validate_chapter_count(count: int) -> None:
    if type(count) is not int or not MIN_CHAPTERS <= count <= MAX_CHAPTERS:
        raise ValueError("Comprehensive output requires 5–10 substantive chapters")


def _inventory(concepts: list[dict[str, Any]], known: set[str]):
    from .contracts import PREREQUISITES

    if not isinstance(concepts, list) or len(concepts) < MIN_CHAPTERS:
        raise ValueError("At least five substantive concepts are needed; narrow the output profile instead of padding")
    records: dict[str, dict[str, Any]] = {}
    for concept in concepts:
        if not isinstance(concept, dict):
            raise ValueError("Concept inventory must contain objects")
        cid = concept.get("id")
        if not isinstance(cid, str) or not cid.strip() or cid in records:
            raise ValueError("Concept identities must be nonempty and unique")
        for field in ("title", "section"):
            value = concept.get(field, concept.get("title"))
            if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
                raise ValueError(f"Concept {cid} needs a nonempty single-line {field}")
        objectives = concept.get("objectives")
        if not isinstance(objectives, list) or not objectives or any(
            not isinstance(goal, str) or not goal.strip() for goal in objectives
        ):
            raise ValueError(f"Concept {cid} needs substantive learning objectives")
        if concept.get("group") is not None and (
            not isinstance(concept["group"], str) or not concept["group"].strip()
        ):
            raise ValueError("A supplied concept group must be a nonempty string")
        records[cid] = concept

    parents: dict[str, list[str]] = {}
    external = []
    for cid, concept in records.items():
        requirements = concept.get("prerequisites", [])
        if not isinstance(requirements, list):
            raise ValueError("Concept prerequisites must be a list")
        parents[cid] = []
        for requirement in requirements:
            if isinstance(requirement, str):
                dependency, classification = requirement, "covered" if requirement in records else "assumed"
            elif isinstance(requirement, dict):
                dependency, classification = requirement.get("id"), requirement.get("classification")
            else:
                raise ValueError("Prerequisites need an ID or a classified record")
            if not isinstance(dependency, str) or not dependency.strip() or not isinstance(classification, str) or classification not in PREREQUISITES:
                raise ValueError("Invalid classified prerequisite")
            if dependency in records:
                if dependency not in parents[cid]:
                    parents[cid].append(dependency)
            elif dependency in known or classification in {"optional", "missing"}:
                external.append({"concept": cid, "id": dependency, "classification": classification,
                                 "known": dependency in known})
            else:
                raise ValueError(f"Unknown prerequisite: {dependency}")
    return records, parents, external


def _topological_order(records, parents):
    """Stable input-order ties, preferring the preceding group only when ready."""
    pending, ordered, done = list(records), [], set()
    while pending:
        ready = [cid for cid in pending if set(parents[cid]) <= done]
        if not ready:
            raise ValueError("Cyclic concept prerequisites")
        previous_group = records[ordered[-1]].get("group") if ordered else None
        selected = next((cid for cid in ready if previous_group and records[cid].get("group") == previous_group), ready[0])
        ordered.append(selected)
        done.add(selected)
        pending.remove(selected)
    return ordered


def _workload(concept: dict[str, Any], prerequisite_depth: int) -> dict[str, Any]:
    # Reuse the canonical depth semantics; do not maintain another objective parser.
    from . import allocate_depth

    levels = allocate_depth(concept, source_policy="adaptive")["levels"]
    for field in ("examples", "assessments"):
        if not isinstance(concept.get(field, []), list):
            raise ValueError(f"Concept {field} must be a list")
    components = {
        "concept": 1.0,
        "additional_objectives": 0.25 * (len(concept["objectives"]) - 1),
        "prerequisite_depth": 0.15 * min(prerequisite_depth, 6),
        "depth": sum(levels[name] * weight for name, weight in DEPTH_WEIGHTS.items()),
        "worked_examples": 0.25 * len(concept.get("examples", [])),
        "assessments": 0.15 * len(concept.get("assessments", [])),
    }
    return {"units": round(sum(components.values()), 4), "components": components,
            "depth_levels": levels, "prerequisite_depth": prerequisite_depth}


def _partition(ordered, records, estimates, count):
    """Balance contiguous topological segments while keeping supplied groups together.

    Dynamic programming globally considers splits and merges, rather than
    repeatedly applying local rules that can oscillate or lose ownership.
    """
    size = len(ordered)
    prefix = [0.0]
    for cid in ordered:
        prefix.append(prefix[-1] + estimates[cid]["units"])
    target = prefix[-1] / count
    # A segment's cost combines normalized workload variance and a modest
    # supplied-group boundary penalty. Dependencies are already topological.
    costs = [[math.inf] * (size + 1) for _ in range(count + 1)]
    cuts = [[None] * (size + 1) for _ in range(count + 1)]
    costs[0][0] = 0.0
    for parts in range(1, count + 1):
        for end in range(parts, size - (count - parts) + 1):
            for start in range(parts - 1, end):
                if not math.isfinite(costs[parts - 1][start]):
                    continue
                load = prefix[end] - prefix[start]
                boundary = bool(start and records[ordered[start]].get("group") and
                                records[ordered[start]].get("group") == records[ordered[start - 1]].get("group"))
                score = costs[parts - 1][start] + ((load - target) / target) ** 2 + 0.20 * boundary
                if score < costs[parts][end]:
                    costs[parts][end], cuts[parts][end] = score, start
    segments, end = [], size
    for parts in range(count, 0, -1):
        start = cuts[parts][end]
        if start is None:
            raise ValueError("Unable to allocate nonempty chapters")
        segments.append(ordered[start:end])
        end = start
    return list(reversed(segments)), target


def _safe_chapter_title(value: str) -> str:
    from . import safe_title

    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " - ", value)
    cleaned = re.sub(r"\s+", " ", cleaned).strip().rstrip(". ")[:90].rstrip()
    if not cleaned or re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", cleaned, re.I):
        cleaned = "Concept " + cleaned
    return safe_title(cleaned)


def plan_chapters(concepts: list[dict[str, Any]], *, known_prerequisites: Iterable[str] = ()) -> dict[str, Any]:
    """Allocate supplied concepts into five to ten chapters without inventing scope.

    ``group`` is an optional coherence hint, not permission to violate a
    prerequisite. Classified missing external prerequisites remain visible in
    the rationale for the existing obligation engine to resolve.
    """
    if isinstance(known_prerequisites, (str, bytes)):
        raise ValueError("known_prerequisites must be a collection of concept IDs")
    try:
        supplied_known = list(known_prerequisites)
    except TypeError as exc:
        raise ValueError("known_prerequisites must be a collection of concept IDs") from exc
    if any(not isinstance(cid, str) or not cid.strip() for cid in supplied_known):
        raise ValueError("known_prerequisites must contain nonempty concept IDs")
    known = set(supplied_known)
    records, parents, external = _inventory(concepts, known)
    ordered = _topological_order(records, parents)
    depths, estimates = {}, {}
    for cid in ordered:
        depths[cid] = max((depths[parent] + 1 for parent in parents[cid]), default=0)
        estimates[cid] = _workload(records[cid], depths[cid])
    total = sum(record["units"] for record in estimates.values())
    desired = math.ceil(total / TARGET_WORKLOAD)
    count = min(MAX_CHAPTERS, len(concepts), max(MIN_CHAPTERS, desired))
    validate_chapter_count(count)
    segments, balanced_target = _partition(ordered, records, estimates, count)
    chapters, title_counts, used_titles = [], Counter(), set()
    group_owners: dict[str, list[str]] = {}
    for owned in segments:
        groups = list(dict.fromkeys(records[cid]["group"] for cid in owned if records[cid].get("group")))
        shared_group = groups[0] if len(groups) == 1 and all(records[cid].get("group") == groups[0] for cid in owned) else None
        title = _safe_chapter_title(shared_group or records[owned[0]]["title"])
        base = title
        title_counts[base.casefold()] += 1
        if title.casefold() in used_titles:
            title = f"{base} - Part {title_counts[base.casefold()]}"
            while title.casefold() in used_titles:
                title_counts[base.casefold()] += 1
                title = f"{base} - Part {title_counts[base.casefold()]}"
        used_titles.add(title.casefold())
        # Membership-derived IDs survive a new earlier chapter when this
        # chapter's actual ownership remains unchanged.
        identifier = "chapter-" + content_hash(json.dumps(owned, ensure_ascii=False))[:12]
        load = round(sum(estimates[cid]["units"] for cid in owned), 4)
        chapters.append({"id": identifier, "title": title, "concepts": owned,
                         "sections": list(dict.fromkeys(records[cid].get("section", records[cid]["title"]) for cid in owned)),
                         "estimate": {"units": load, "concept_count": len(owned), "groups": groups}})
        for group in groups:
            group_owners.setdefault(group, []).append(identifier)
    return {"chapters": chapters, "rationale": {
        "method": "stable prerequisite order; workload-bounded count; balanced contiguous partition with group preference",
        "chapter_count": count, "concept_count": len(concepts), "bounds": [MIN_CHAPTERS, MAX_CHAPTERS],
        "target_workload_units": TARGET_WORKLOAD, "balanced_workload_units": round(balanced_target, 4),
        "total_workload_units": round(total, 4), "unbounded_recommendation": desired,
        "concept_estimates": estimates, "topological_order": ordered, "external_prerequisites": external,
        "split_groups": {group: owners for group, owners in group_owners.items() if len(owners) > 1},
        "merged_groups": [{"chapter": chapter["id"], "groups": chapter["estimate"]["groups"]}
                          for chapter in chapters if len(chapter["estimate"]["groups"]) > 1],
        "overloaded_chapters": [chapter["id"] for chapter in chapters
                                if chapter["estimate"]["units"] > max(TARGET_WORKLOAD, balanced_target) * 1.5],
        "scope_review_required": desired > MAX_CHAPTERS,
        "limitations": "Heuristic instructional workload, not measured time or educational certification. An indivisible heavy concept needs author review; no concepts or content are fabricated.",
    }}
