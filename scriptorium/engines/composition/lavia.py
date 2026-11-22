"""LAVIA — Local Asset and Visual Intelligence Architecture inside UMRIA.

Coordinates concept-level visual coverage planning, acquisition strategy selection,
canonical asset manifests, SHA-256 deduplication, offline/Obsidian validation,
and targeted dependency-aware visual repair.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import posixpath
import re
from typing import Any

from scriptorium.models import content_hash, slugify

LIFECYCLE_STATES = (
    "planned",
    "source_identified",
    "source_verified",
    "acquired",
    "file_validated",
    "semantically_verified",
    "embedded",
    "publication_verified",
    "failed",
    "blocked",
)

COVERAGE_CATEGORIES = (
    "overall_structure",
    "component_structure",
    "information_flow",
    "mathematical_behavior",
    "step_by_step_execution",
    "numerical_results",
    "comparisons",
    "failure_conditions",
)

STRATEGY_MAP = {
    "external": "retrieve_figure",
    "imagegen": "conceptual_illustration",
}


def select_acquisition_strategy(visual: dict[str, Any], *, host_imagegen_available: bool = False) -> str:
    """Choose Strategy A (retrieve), Strategy B (deterministic), or Strategy C (illustration)."""
    renderer = visual.get("renderer")
    if not renderer:
        from .renderers import KINDS
        kind = visual.get("kind", "")
        renderer = KINDS.get(kind, ("svg",))[0]
    strategy = STRATEGY_MAP.get(renderer, "deterministic_render")
    if strategy == "conceptual_illustration":
        if visual.get("empirical") or visual.get("equation") or visual.get("data"):
            raise ValueError("Artistic illustration cannot represent exact numerical evidence")
        if not (host_imagegen_available or visual.get("generated_image") or visual.get("local_fallback")):
            return "deterministic_render"
    return strategy


def _concept_categories(concept: dict[str, Any]) -> list[str]:
    levels = concept.get("depth_allocation", {}).get("levels", concept.get("depth", {}))
    categories: list[str] = []
    if levels.get("conceptual", 0) >= 2:
        categories.extend(["overall_structure", "component_structure"])
    if levels.get("mathematical", 0) >= 2 or concept.get("proofs"):
        categories.extend(["mathematical_behavior", "numerical_results"])
    if levels.get("algorithmic", 0) >= 2 or concept.get("information_flows") or concept.get("tensors"):
        categories.extend(["information_flow", "step_by_step_execution"])
    if levels.get("analytical", 0) >= 2:
        categories.append("comparisons")
    if concept.get("failures") or levels.get("research", 0) >= 3:
        categories.append("failure_conditions")
    return list(dict.fromkeys(categories or ["overall_structure"]))


def plan_visual_coverage(plan: dict[str, Any]) -> dict[str, Any]:
    """Evaluate per-chapter educational visual opportunities without decorative quotas."""
    concepts_by_id = {c["id"]: c for c in plan.get("concepts", [])}
    existing_by_concept: dict[str, list[dict[str, Any]]] = {}
    for visual in plan.get("visuals", []):
        existing_by_concept.setdefault(visual.get("concept", ""), []).append(visual)

    chapters_report: list[dict[str, Any]] = []
    for chapter in plan.get("chapters", []):
        cids = chapter.get("concepts", [])
        chapter_concepts = [concepts_by_id[cid] for cid in cids if cid in concepts_by_id]
        needed_categories: list[str] = []
        for concept in chapter_concepts:
            for cat in _concept_categories(concept):
                if cat not in needed_categories:
                    needed_categories.append(cat)

        planned_visuals = [v for cid in cids for v in existing_by_concept.get(cid, [])]
        covered_categories = {
            v.get("coverage_category")
            for v in planned_visuals
            if v.get("coverage_category") in COVERAGE_CATEGORIES
        }
        missing_categories = [c for c in needed_categories if c not in covered_categories]

        math_heavy = any(
            c.get("depth_allocation", {}).get("levels", c.get("depth", {})).get("mathematical", 0) >= 3
            for c in chapter_concepts
        )
        arch_heavy = any(
            c.get("information_flows") or c.get("tensors") or len(cids) >= 3
            for c in chapter_concepts
        )
        recommended_range = (4, 8) if arch_heavy else ((2, 5) if math_heavy or len(cids) >= 2 else (1, 3))
        chapters_report.append({
            "chapter_id": chapter.get("id"),
            "title": chapter.get("title"),
            "concept_count": len(cids),
            "planned_visual_count": len(planned_visuals),
            "recommended_range": list(recommended_range),
            "needed_categories": needed_categories,
            "missing_categories": missing_categories,
            "coverage_ratio": round(
                len(covered_categories) / max(len(needed_categories), 1), 3
            ),
        })
    return {
        "chapters": chapters_report,
        "total_planned_visuals": len(plan.get("visuals", [])),
        "total_missing_categories": sum(len(c["missing_categories"]) for c in chapters_report),
    }


def _lifecycle_from_result(result: dict[str, Any]) -> str:
    status = result.get("status", "planned")
    if status == "verified":
        return "embedded" if result.get("embed") else "file_validated"
    if status == "unavailable":
        return "blocked"
    if status == "failed":
        return "failed"
    return "planned"


def build_asset_manifest(
    plan: dict[str, Any],
    results: dict[str, dict[str, Any]],
    *,
    collection_slug: str | None = None,
) -> dict[str, Any]:
    """Build a canonical LAVIA asset manifest with deduplication and provenance."""
    slug = slugify(collection_slug or plan.get("collection_slug") or plan.get("topic") or "collection")
    chapter_for_concept = {
        cid: ch["id"]
        for ch in plan.get("chapters", [])
        for cid in ch.get("concepts", [])
    }
    visuals_by_id = {v["id"]: v for v in plan.get("visuals", [])}
    seen_hashes: dict[str, str] = {}
    entries: list[dict[str, Any]] = []
    deduplicated_count = 0

    for vid, result in results.items():
        visual = visuals_by_id.get(vid, {})
        cid = visual.get("concept", "")
        digest = result.get("hash")
        canonical_path = result.get("path")
        duplicate_of = None
        if digest and canonical_path:
            if digest in seen_hashes:
                duplicate_of = seen_hashes[digest]
                deduplicated_count += 1
            else:
                seen_hashes[digest] = vid

        provenance = result.get("provenance") or {}
        renderer = result.get("renderer", "svg")
        method = "external_download" if renderer == "external" else "deterministic_render"
        lifecycle = _lifecycle_from_result(result)
        suffix = Path(canonical_path).suffix.lstrip(".") if canonical_path else ""
        entries.append({
            "asset_id": vid,
            "concept_id": cid,
            "chapter_id": chapter_for_concept.get(cid, ""),
            "lifecycle_state": lifecycle,
            "duplicate_of": duplicate_of,
            "dependencies": list(visual.get("dependencies", [cid] if cid else [])),
            "acquisition": {
                "method": method,
                "strategy": select_acquisition_strategy(visual) if visual else "deterministic_render",
                "original_source": provenance.get("source") or visual.get("source"),
                "downloaded_from": provenance.get("final_url") or provenance.get("url") or visual.get("url"),
                "license": provenance.get("rights") or visual.get("rights"),
                "renderer": renderer,
                "input_hash": result.get("input_hash"),
            },
            "storage": {
                "relative_path": canonical_path,
                "format": suffix,
                "content_hash": digest,
                "cached": bool(result.get("cached")),
            },
            "verification": {
                "image_integrity": "passed" if result.get("status") == "verified" else "failed",
                "semantic_accuracy": "pending_editorial_review" if result.get("status") == "verified" else "unverified",
                "attribution": "passed" if (renderer != "external" or provenance.get("rights")) else "failed",
                "embed_resolution": "pending",
                "offline_available": bool(canonical_path and not str(canonical_path).startswith("https:")),
            },
            "publication": {
                "status": result.get("status", "planned"),
                "alt_text": visual.get("alt") or visual.get("objective", ""),
                "embed": result.get("embed"),
                "failure_reason": result.get("failure_reason"),
            },
        })

    return {
        "schema_version": "lavia-manifest/v1",
        "collection_slug": slug,
        "assets": entries,
        "summary": {
            "total": len(entries),
            "verified": sum(1 for e in entries if e["publication"]["status"] == "verified"),
            "failed": sum(1 for e in entries if e["lifecycle_state"] == "failed"),
            "blocked": sum(1 for e in entries if e["lifecycle_state"] == "blocked"),
            "deduplicated": deduplicated_count,
        },
    }


def save_asset_manifest(vault: Path, manifest: dict[str, Any]) -> Path:
    from . import contained
    from ..vault import safe_write_note

    slug = slugify(manifest.get("collection_slug") or "collection")
    rel = f"assets/scriptorium/{slug}/manifest.json"
    path = contained(vault, rel)
    safe_write_note(path, json.dumps(manifest, indent=2, sort_keys=True) + "\n", validate_properties=False)
    return path


def _extract_local_embeds(markdown: str) -> list[str]:
    wiki = re.findall(r"!\[\[([^\]|#]+)", markdown)
    md = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", markdown)
    return wiki + md


def validate_collection_visuals(
    vault: Path,
    plan: dict[str, Any],
    bodies: dict[str, str],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    """Verify offline availability, local embed resolution, integrity, and completion gate."""
    from . import contained
    from .media import SUPPORTED_MIMES, validate_image_bytes

    errors: list[str] = []
    chapters_by_id = {c["id"]: c for c in plan.get("chapters", [])}
    mime_by_ext = {f".{ext}": mime for mime, ext in SUPPORTED_MIMES.items()}

    for entry in manifest.get("assets", []):
        aid = entry["asset_id"]
        rel = entry["storage"].get("relative_path")
        expected_hash = entry["storage"].get("content_hash")
        pub_status = entry["publication"].get("status")
        if pub_status != "verified":
            errors.append(f"{aid}: visual obligation not verified ({pub_status})")
            continue
        if not rel or str(rel).startswith(("http://", "https://")):
            errors.append(f"{aid}: non-local asset path forbidden in local-first mode")
            continue
        path = contained(vault, rel)
        if not path.is_file():
            errors.append(f"{aid}: missing local asset {rel}")
            continue
        raw = path.read_bytes()
        if expected_hash and content_hash(raw) != expected_hash:
            errors.append(f"{aid}: SHA-256 mismatch on {rel}")
            continue
        if path.suffix.lower() in mime_by_ext:
            try:
                validate_image_bytes(raw, mime_by_ext[path.suffix.lower()])
            except ValueError as exc:
                errors.append(f"{aid}: invalid image bytes ({exc})")
                continue

        chid = entry.get("chapter_id")
        body = bodies.get(chid, "")
        embeds = _extract_local_embeds(body)
        chapter_path = chapters_by_id.get(chid, {}).get("path", "note.md")
        rel_from_note = posixpath.relpath(rel, posixpath.dirname(chapter_path) or ".")
        if rel not in embeds and rel_from_note not in embeds:
            errors.append(f"{aid}: missing local embed in chapter {chid}")
            continue
        for target in embeds:
            if target.startswith(("http://", "https://")):
                errors.append(f"{chid}: remote image URL embed forbidden ({target})")
        entry["verification"]["embed_resolution"] = "passed"
        entry["lifecycle_state"] = "publication_verified"

    return {
        "passed": not errors,
        "errors": errors,
        "offline_ready": not errors,
        "verified_assets": sum(1 for e in manifest.get("assets", []) if e["lifecycle_state"] == "publication_verified"),
    }


def repair_visual_assets(
    vault: Path,
    plan: dict[str, Any],
    bodies: dict[str, str],
    manifest: dict[str, Any],
    *,
    changed_dependencies: set[str] | None = None,
    execute: bool = True,
) -> dict[str, Any]:
    """Targeted recovery: repair only missing, corrupted, or dependency-impacted visuals."""
    from . import contained
    from .visuals import render_visuals

    impacted_ids: list[str] = []
    for entry in manifest.get("assets", []):
        aid = entry["asset_id"]
        rel = entry["storage"].get("relative_path")
        expected_hash = entry["storage"].get("content_hash")
        deps = set(entry.get("dependencies", []))
        dep_hit = bool(changed_dependencies and (deps & changed_dependencies))
        missing_or_corrupt = False
        if not rel:
            missing_or_corrupt = True
        else:
            path = contained(vault, rel)
            if not path.is_file() or (expected_hash and content_hash(path.read_bytes()) != expected_hash):
                missing_or_corrupt = True
        if dep_hit or missing_or_corrupt or entry["publication"].get("status") != "verified":
            impacted_ids.append(aid)

    if not impacted_ids:
        return {"repaired_ids": [], "bodies": dict(bodies), "manifest": deepcopy(manifest)}

    sub_plan = dict(plan)
    sub_plan["visuals"] = [v for v in plan.get("visuals", []) if v["id"] in set(impacted_ids)]
    new_bodies, new_results = render_visuals(vault, sub_plan, bodies, execute=execute)
    updated_manifest = deepcopy(manifest)
    repaired_manifest = build_asset_manifest(
        sub_plan, new_results, collection_slug=manifest.get("collection_slug")
    )
    by_id = {e["asset_id"]: e for e in repaired_manifest["assets"]}
    for i, entry in enumerate(updated_manifest.get("assets", [])):
        if entry["asset_id"] in by_id:
            updated_manifest["assets"][i] = by_id[entry["asset_id"]]
    return {
        "repaired_ids": impacted_ids,
        "bodies": new_bodies,
        "manifest": updated_manifest,
    }
