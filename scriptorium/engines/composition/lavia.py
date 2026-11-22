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

SEARCH_STATUSES = ("FOUND", "NO_IMAGE_EXISTS", "SEARCH_UNAVAILABLE")

STRATEGY_MAP = {
    "external": "retrieve_figure",
    "imagegen": "conceptual_illustration",
}


def build_image_research_request(
    *,
    job_id: str,
    chapter_id: str,
    concept_id: str,
    objective: str,
    subject: str,
    queries: list[str],
    structural_relationships: list[str] | None = None,
    min_width: int = 400,
    min_height: int = 250,
    preferred_type: str = "diagram",
    license_policy: str = "permissive_required",
    desired_count: int = 1,
    exclude_urls: list[str] | None = None,
) -> dict[str, Any]:
    """Create a structured ResearchFlow image-discovery request (Scriptorium 9.2)."""
    clean_queries = [q.strip() for q in queries if isinstance(q, str) and q.strip()]
    if not clean_queries:
        raise ValueError("Image research request requires at least one search query")
    return {
        "schema_version": "image-research-request/v1",
        "job_id": job_id,
        "chapter_id": chapter_id,
        "concept_id": concept_id,
        "educational_objective": objective,
        "image_subject": subject,
        "structural_relationships": list(structural_relationships or []),
        "search_queries": clean_queries,
        "min_resolution": {"width": min_width, "height": min_height},
        "preferred_visual_type": preferred_type,
        "license_policy": license_policy,
        "desired_count": max(1, desired_count),
        "exclude_urls": list(exclude_urls or []),
    }


def evaluate_svg_fallback_gate(
    visual: dict[str, Any],
    *,
    search_status: str,
    queries_attempted: list[str] | None = None,
    sources_considered: list[str] | None = None,
    rejection_reasons: list[str] | None = None,
    justification: str = "",
) -> dict[str, Any]:
    """Enforce the SVG fallback gate before allowing native SVG generation."""
    if search_status not in SEARCH_STATUSES:
        raise ValueError(f"Invalid search_status: {search_status}")
    if search_status == "FOUND":
        raise ValueError("SVG fallback forbidden when a suitable external image was found")
    # Custom numeric plots derived from chapter equations/data are an explicit justified exception.
    if visual.get("kind") in {"equation", "distribution", "timeseries", "signal"} and (
        visual.get("equation") or visual.get("data")
    ):
        return {
            "permitted": True,
            "reason": "custom_numeric_plot",
            "search_status": search_status,
            "justification": justification or "Deterministic plot matching chapter numerical equations/data",
        }
    if not justification.strip():
        raise ValueError("SVG fallback requires an explicit educational justification")
    if search_status == "NO_IMAGE_EXISTS" and not queries_attempted:
        raise ValueError("NO_IMAGE_EXISTS requires recorded search queries attempted")
    return {
        "permitted": True,
        "reason": "documented_fallback",
        "requested_concept": visual.get("concept", ""),
        "search_status": search_status,
        "queries_attempted": list(queries_attempted or []),
        "sources_considered": list(sources_considered or []),
        "rejection_reasons": list(rejection_reasons or []),
        "justification": justification.strip(),
    }


def resolve_visual_route(
    visual: dict[str, Any],
    *,
    asset_registry: dict[str, dict[str, Any]] | None = None,
    host_candidates: list[dict[str, Any]] | None = None,
    search_available: bool = True,
    fallback_decision: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Strict Web-Image-First routing: Reuse -> Discover/Download -> Documented Fallback."""
    concept = visual.get("concept", "")
    # Route 1: Reuse verified local asset
    if asset_registry:
        reusable = asset_registry.get(visual.get("id", "")) or asset_registry.get(concept)
        if reusable and reusable.get("relative_path"):
            return {"route": "reuse_local_asset", "visual": {**visual, "local_fallback": reusable["relative_path"], "asset_policy": "offline_only"}, "search_status": "FOUND"}

    # Route 2 & 3: Select permitted external candidate discovered by host
    for cand in host_candidates or []:
        if cand.get("url") and cand.get("source") and cand.get("rights"):
            resolved = {
                **visual,
                "kind": "source_figure",
                "url": cand["url"],
                "source": cand["source"],
                "rights": cand["rights"],
                "alt": cand.get("alt") or visual.get("objective", ""),
                "relevance": cand.get("relevance") or visual.get("objective", ""),
                "require_permissive_license": True,
            }
            return {"route": "external_image_download", "visual": resolved, "search_status": "FOUND"}

    # Route 4: Documented fallback only
    status = "NO_IMAGE_EXISTS" if search_available else "SEARCH_UNAVAILABLE"
    dec = fallback_decision or {}
    gate = evaluate_svg_fallback_gate(
        visual,
        search_status=dec.get("search_status", status),
        queries_attempted=dec.get("queries_attempted"),
        sources_considered=dec.get("sources_considered"),
        rejection_reasons=dec.get("rejection_reasons"),
        justification=dec.get("justification", visual.get("fallback_justification", "")),
    )
    return {"route": "documented_fallback", "visual": {**visual, "fallback_gate": gate}, "search_status": gate["search_status"]}


def verify_visual_obligations(
    obligations: list[dict[str, Any]],
    bodies: dict[str, str],
    vault: Path,
) -> dict[str, Any]:
    """ReviewEngine check: verify embeds, provenance, explanation density, and fallback gates."""
    from . import contained
    errors: list[str] = []
    for ob in obligations:
        oid = ob.get("obligation_id", "<unknown>")
        chid = ob.get("chapter_id", "")
        rel = ob.get("local_asset_path")
        if not rel or not contained(vault, rel).is_file():
            errors.append(f"{oid}: missing local asset {rel}")
            continue
        body = bodies.get(chid, "")
        if rel not in body:
            errors.append(f"{oid}: asset {rel} is not embedded in chapter {chid}")
            continue
        # Reject image-only chapters/sections with no accompanying explanatory prose
        non_embed_words = [
            w for line in body.splitlines()
            if not line.strip().startswith(("![", "#"))
            for w in line.split()
        ]
        if len(non_embed_words) < 15:
            errors.append(f"{oid}: chapter {chid} lacks sufficient explanatory prose around visual")
        if ob.get("acquisition_status") == "external_download" and not ob.get("provenance_record"):
            errors.append(f"{oid}: external image missing provenance/attribution record")
    return {"passed": not errors, "errors": errors, "checked": len(obligations)}


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
        try:
            strategy = select_acquisition_strategy(visual) if visual else "deterministic_render"
        except ValueError:
            strategy = "blocked_invalid_strategy"
        entries.append({
            "asset_id": vid,
            "concept_id": cid,
            "chapter_id": chapter_for_concept.get(cid, ""),
            "lifecycle_state": lifecycle,
            "duplicate_of": duplicate_of,
            "dependencies": list(visual.get("dependencies", [cid] if cid else [])),
            "acquisition": {
                "method": method,
                "strategy": strategy,
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


def _strip_fenced_code(markdown: str) -> str:
    lines: list[str] = []
    fence: tuple[str, int] | None = None
    for line in markdown.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if match:
            token, suffix = match.groups()
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1] and not suffix.strip():
                fence = None
        elif fence is None:
            lines.append(line)
    return "\n".join(lines)


def _extract_local_embeds(markdown: str) -> list[str]:
    prose = _strip_fenced_code(markdown)
    wiki = re.findall(r"!\[\[([^\]|#]+)", prose)
    md = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", prose)
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

    # Always scan all chapter bodies for leaked remote image URLs in local-first mode.
    for key, body in bodies.items():
        for target in _extract_local_embeds(body):
            if target.startswith(("http://", "https://")):
                errors.append(f"{key}: remote image URL embed forbidden ({target})")

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
        chapter_path = chapters_by_id.get(chid, {}).get("path", "note.md")
        body = bodies.get(chid) if chid in bodies else bodies.get(chapter_path, "")
        renderer = entry.get("acquisition", {}).get("renderer", "")
        expected_embed = (entry.get("publication", {}).get("embed") or "").strip()
        if renderer in {"mermaid", "table", "interactive"}:
            if not expected_embed or expected_embed not in body:
                errors.append(f"{aid}: missing embedded {renderer} visual in chapter {chid}")
                continue
        else:
            embeds = _extract_local_embeds(body)
            rel_from_note = posixpath.relpath(rel, posixpath.dirname(chapter_path) or ".")
            if rel not in embeds and rel_from_note not in embeds:
                errors.append(f"{aid}: missing local embed in chapter {chid}")
                continue
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
