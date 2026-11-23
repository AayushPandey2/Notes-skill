"""Prerequisite-safe chapter allocation driven by teaching obligations and coherence.

A chapter count is an outcome. No minimum quota or maximum chapter count pads or
truncates a subject. Explicitly coherent simple concepts may share a chapter;
complex mechanisms and derivations retain their own instructional space.
"""
from __future__ import annotations
from collections import Counter
import json
import re
from typing import Any, Iterable
from scriptorium.models import content_hash
from .learning import QUESTIONS


def validate_chapter_count(count: int) -> None:
    if type(count) is not int or count < 1:
        raise ValueError("Chapter count must be a positive integer")


def _inventory(concepts: list[dict[str, Any]], known: set[str]):
    from .contracts import PREREQUISITES

    if not isinstance(concepts, list) or not concepts:
        raise ValueError("At least one substantive concept is required")
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


def _safe_chapter_title(value: str) -> str:
    from . import safe_title

    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " - ", value)
    cleaned = re.sub(r"\s+", " ", cleaned).strip().rstrip(". ")[:90].rstrip()
    if not cleaned or re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", cleaned, re.I):
        cleaned = "Concept " + cleaned
    return safe_title(cleaned)


def _requirements(concept, prerequisite_depth: int = 0):
    from . import allocate_depth

    profile = concept.get("depth_profile", {})
    complexity = profile.get("complexity", concept.get("complexity", "standard"))
    goals = " ".join(concept["objectives"]).lower()
    requirements = list(QUESTIONS) if complexity != "trivial" else ["what"]
    if re.search(r"\b(?:derive|prove)\b", goals): requirements.append("derivation")
    if re.search(r"\b(?:calculate|compute|solve)\b", goals): requirements.append("numerical_walkthrough")
    if re.search(r"\b(?:implement|experiment|debug)\b", goals): requirements.append("practical_laboratory")
    if concept.get("visual_requirements") or concept.get("signals", {}).get("spatial"):
        requirements.append("visual_explanation")
    requirements += ["example:"+str(e.get("id", i)) for i,e in enumerate(concept.get("examples", []))]
    requirements += ["assessment:"+str(e.get("id", i)) for i,e in enumerate(concept.get("assessments", []))]
    standalone = complexity == "complex" or profile.get("internal_mechanisms", 1) > 1 or "derivation" in requirements
    depth_levels = allocate_depth(concept, source_policy="adaptive")["levels"]
    return {
        "requirements": requirements,
        "units": len(requirements),
        "prerequisite_depth": prerequisite_depth,
        "depth_levels": depth_levels,
        "complexity": complexity,
        "standalone": standalone,
        "reason": "Separate intermediate reasoning" if standalone else "Coherent concepts may share teaching context",
    }


def plan_chapters(concepts: list[dict[str, Any]], *, known_prerequisites: Iterable[str] = ()) -> dict[str, Any]:
    if isinstance(known_prerequisites, (str, bytes)):
        raise ValueError("known_prerequisites must contain concept IDs")
    try:
        known_list = list(known_prerequisites)
    except TypeError as exc:
        raise ValueError("known_prerequisites must contain concept IDs") from exc
    if any(not isinstance(cid, str) or not cid.strip() for cid in known_list):
        raise ValueError("known_prerequisites must contain nonempty concept IDs")
    records, parents, external = _inventory(concepts, set(known_list))
    ordered = _topological_order(records, parents)
    prereq_depths: dict[str, int] = {}
    for cid in ordered:
        prereq_depths[cid] = (1 + max(prereq_depths[p] for p in parents[cid])) if parents[cid] else 0
    estimates = {cid: _requirements(records[cid], prereq_depths[cid]) for cid in ordered}
    segments=[]
    for cid in ordered:
        current=records[cid]; previous=segments[-1][-1] if segments else None
        coherent = previous is not None and current.get("group") and current.get("group")==records[previous].get("group")
        shared_definition = previous is not None and estimates[cid]["complexity"]=="trivial" and estimates[previous]["complexity"]=="trivial" and parents[cid]==parents[previous]
        if (coherent or shared_definition) and not estimates[cid]["standalone"] and not any(estimates[x]["standalone"] for x in segments[-1]):
            segments[-1].append(cid)
        else:
            segments.append([cid])
    chapters=[];counts=Counter();used=set();group_owners={}
    for owned in segments:
        groups=list(dict.fromkeys(records[cid]["group"] for cid in owned if records[cid].get("group")))
        title=_safe_chapter_title(groups[0] if len(groups)==1 else records[owned[0]]["title"])
        base=title
        while title.casefold() in used:
            counts[base]+=1;title=f"{base} - Part {counts[base]+1}"
        used.add(title.casefold())
        identifier="chapter-"+content_hash(json.dumps(owned,ensure_ascii=False))[:12]
        obligations={cid:estimates[cid]["requirements"] for cid in owned}
        chapters.append({"id":identifier,"title":title,"concepts":owned,
                         "sections":list(dict.fromkeys(records[cid].get("section",records[cid]["title"]) for cid in owned)),
                         "teaching_obligations":obligations,
                         "estimate":{"units":sum(len(value) for value in obligations.values()),"concept_count":len(owned),"groups":groups}})
        for group in groups: group_owners.setdefault(group,[]).append(identifier)
    return {"chapters":chapters,"rationale":{
        "method":"prerequisite order, explicit coherence and instructional obligations; no chapter quota",
        "chapter_count":len(chapters),"concept_count":len(concepts),"bounds":[1,None],
        "topological_order":ordered,"external_prerequisites":external,"concept_estimates":estimates,
        "total_workload_units":sum(len(x["requirements"]) for x in estimates.values()),
        "workload_units_meaning":"number of explicit instructional obligations, not a quality or depth score",
        "split_groups":{g:owners for g,owners in group_owners.items() if len(owners)>1},
        "merged_groups":[],"overloaded_chapters":[],
        "scope_review_required":any(item["classification"]=="missing" for item in external),
        "limitations":"Topic coherence and semantic adequacy require author evidence; unrelated concepts are not merged by title keywords."}}
