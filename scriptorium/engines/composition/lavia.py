"""LAVIA — Local Asset and Visual Intelligence Architecture (A7 Assets).

Coordinates web-image-first visual research, candidate discovery (including live
open-educational API adapters), rights verification, canonical asset manifests,
SHA-256 deduplication, offline/Obsidian validation, and targeted visual repair.

Programmatic SVG diagram generation has been retired. When no suitable,
permitted external web image can be acquired, LAVIA records an explicit unmet
visual obligation instead of generating synthetic diagrams.
"""
from __future__ import annotations

from copy import deepcopy
from html import unescape
import json
from pathlib import Path
import posixpath
import re
from typing import Any, Callable
from urllib.parse import quote_plus, urlencode
import urllib.request

from scriptorium.models import content_hash, slugify

LIFECYCLE_STATES = (
    "planned",
    "source_identified",
    "source_verified",
    "acquired",
    "file_validated",
    "inspected",
    "semantically_verified",
    "embedded",
    "publication_verified",
    "failed",
    "blocked",
    "unmet_obligation",
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

SEARCH_STATUSES = ("FOUND", "NO_IMAGE_EXISTS", "SEARCH_UNAVAILABLE", "RIGHTS_REJECTED")

STRATEGY_MAP = {
    "external": "retrieve_figure",
    "mermaid": "native_mermaid",
    "table": "markdown_table",
    "interactive": "interactive_sequence",
}

_HTML_TAG_RE = re.compile(r"<[^>]+>")


def _clean_html_text(value: Any) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", unescape(_HTML_TAG_RE.sub(" ", str(value)))).strip()


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
    """Create a structured image-discovery request (Scriptorium)."""
    clean_queries = [q.strip() for q in queries if isinstance(q, str) and q.strip()]
    if not clean_queries:
        raise ValueError("Image research request requires at least one search query")
    return {
        "schema_version": "image-research-request/v2",
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


def generate_visual_search_queries(
    concept_title: str,
    objective: str = "",
    *,
    synonyms: list[str] | None = None,
    relationships: list[str] | None = None,
    learner_level: str = "beginner",
    diagram_type: str = "diagram",
    domain_context: str = "",
    max_queries: int = 5,
) -> list[str]:
    """Generate escalated, domain-neutral web image search queries cleanly bounded by budget."""
    clean_title = re.sub(r"\s+", " ", concept_title).strip()
    if not clean_title:
        raise ValueError("concept_title must be nonempty")
    level_hint = "simple overview" if learner_level == "beginner" else "technical"
    dtype = (diagram_type or "diagram").replace("_", " ").strip()
    candidates: list[str] = [
        f"{clean_title} {dtype}".strip(),
        f"{clean_title} {level_hint} {dtype}".strip(),
    ]
    if domain_context:
        candidates.append(f"{clean_title} {domain_context.strip()} {dtype}".strip())
    for syn in synonyms or []:
        if syn and syn.strip():
            candidates.append(f"{syn.strip()} {dtype}".strip())
    for rel in relationships or []:
        if rel and rel.strip():
            candidates.append(f"{clean_title} {rel.strip()}".strip())
    if objective:
        obj_words = [w for w in re.findall(r"[A-Za-z0-9-]+", objective) if len(w) > 3][:4]
        if obj_words:
            candidates.append(f"{clean_title} {' '.join(obj_words)}".strip())

    deduped: list[str] = []
    seen: set[str] = set()
    for q in candidates:
        key = q.casefold()
        if key not in seen:
            seen.add(key)
            deduped.append(q)
    return deduped[: max(1, max_queries)]


def _default_http_get_json(url: str, timeout: int = 8) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Scriptorium-Media/1.0 (https://github.com/AayushPandey2/Notes-skill)"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if getattr(resp, "status", 200) != 200:
            raise ValueError(f"Search endpoint returned HTTP {getattr(resp, 'status', 'unknown')}")
        return json.loads(resp.read().decode("utf-8"))


def search_web_images(
    queries: list[str] | dict[str, Any],
    *,
    sources: tuple[str, ...] = ("wikimedia_commons",),
    max_results_per_query: int = 5,
    min_width: int = 320,
    min_height: int = 180,
    timeout: int = 8,
    require_permissive_license: bool = True,
    http_get: Callable[[str, int], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Discover real candidate educational images via open web APIs (e.g., Wikimedia Commons).

    Evaluates resolution, MIME type, attribution, and licensing before returning ranked candidates.
    Supports dependency-injected ``http_get(url, timeout) -> dict`` for offline tests.
    """
    from .media import SUPPORTED_MIMES, verify_license_and_rights

    if isinstance(queries, dict):
        q_list = list(queries.get("search_queries") or [])
        min_res = queries.get("min_resolution") or {}
        min_width = int(min_res.get("width", min_width))
        min_height = int(min_res.get("height", min_height))
        exclude_urls = set(queries.get("exclude_urls") or [])
    else:
        q_list = [q.strip() for q in queries if isinstance(q, str) and q.strip()]
        exclude_urls = set()

    if not q_list:
        raise ValueError("Web image search requires at least one query")

    fetcher = http_get or _default_http_get_json
    candidates: list[dict[str, Any]] = []
    rejected: list[dict[str, str]] = []
    seen_urls: set[str] = set(exclude_urls)
    queries_attempted: list[str] = []
    search_errors: list[str] = []

    for query in q_list:
        queries_attempted.append(query)
        if "wikimedia_commons" in sources:
            params = urlencode({
                "action": "query",
                "generator": "search",
                "gsrnamespace": "6",
                "gsrsearch": query,
                "gsrlimit": str(max(1, min(20, max_results_per_query))),
                "prop": "imageinfo",
                "iiprop": "url|size|mime|extmetadata",
                "format": "json",
            })
            api_url = f"https://commons.wikimedia.org/w/api.php?{params}"
            try:
                payload = fetcher(api_url, timeout)
            except Exception as exc:
                search_errors.append(f"wikimedia_commons ({query}): {exc}")
                continue
            pages = (payload.get("query") or {}).get("pages") or {}
            for page in pages.values():
                infos = page.get("imageinfo") or []
                if not infos:
                    continue
                info = infos[0]
                img_url = str(info.get("url") or "").strip()
                if not img_url or not img_url.startswith("https://") or img_url in seen_urls:
                    continue
                mime = str(info.get("mime") or "").split(";", 1)[0].strip().lower()
                if mime not in SUPPORTED_MIMES:
                    rejected.append({"url": img_url, "reason": f"unsupported MIME {mime}"})
                    continue
                w = int(info.get("width") or 0)
                h = int(info.get("height") or 0)
                if w < min_width or h < min_height:
                    rejected.append({"url": img_url, "reason": f"insufficient resolution {w}x{h} (< {min_width}x{min_height})"})
                    continue
                ext = info.get("extmetadata") or {}
                rights = _clean_html_text(
                    (ext.get("LicenseShortName") or {}).get("value")
                    or (ext.get("License") or {}).get("value")
                    or ""
                )
                try:
                    verify_license_and_rights(rights, require_permissive=require_permissive_license)
                except ValueError as exc:
                    rejected.append({"url": img_url, "reason": f"rights check failed: {exc}"})
                    continue
                author = _clean_html_text((ext.get("Artist") or {}).get("value") or "Wikimedia Commons contributor")
                desc = _clean_html_text((ext.get("ImageDescription") or {}).get("value") or page.get("title", ""))
                source_url = str(info.get("descriptionurl") or f"https://commons.wikimedia.org/wiki/{quote_plus(page.get('title', 'Main_Page'))}")
                seen_urls.add(img_url)
                candidates.append({
                    "url": img_url,
                    "source": source_url,
                    "author": author,
                    "rights": rights,
                    "mime": mime,
                    "width": w,
                    "height": h,
                    "title": page.get("title", ""),
                    "alt": desc[:240] or page.get("title", "").replace("File:", ""),
                    "relevance_score": 15,
                    "query": query,
                    "discovery_source": "wikimedia_commons",
                })
        if len(candidates) >= max(3, max_results_per_query):
            break

    if candidates:
        status = "FOUND"
    elif search_errors and len(search_errors) == len(queries_attempted):
        status = "SEARCH_UNAVAILABLE"
    elif rejected and not search_errors:
        status = "RIGHTS_REJECTED"
    else:
        status = "NO_IMAGE_EXISTS"

    return {
        "search_status": status,
        "queries_attempted": queries_attempted,
        "candidates": candidates,
        "rejected": rejected,
        "errors": search_errors,
    }


def record_unmet_visual_obligation(
    visual: dict[str, Any],
    *,
    search_status: str,
    queries_attempted: list[str] | None = None,
    sources_considered: list[str] | None = None,
    rejection_reasons: list[str] | None = None,
    justification: str = "",
) -> dict[str, Any]:
    """Record an explicit unmet visual obligation when no permitted web image can be acquired.

    Programmatic SVG diagram generation is retired and NEVER permitted as a hidden fallback.
    """
    if search_status not in SEARCH_STATUSES:
        raise ValueError(f"Invalid search_status: {search_status}")
    if search_status == "FOUND":
        raise ValueError("Cannot record unmet visual obligation when search_status is FOUND")
    return {
        "permitted": False,
        "fallback_generation": "prohibited",
        "unmet_obligation": True,
        "requested_concept": visual.get("concept", ""),
        "search_status": search_status,
        "queries_attempted": list(queries_attempted or []),
        "sources_considered": list(sources_considered or []),
        "rejection_reasons": list(rejection_reasons or []),
        "reason": justification.strip() or f"Web image acquisition unresolved ({search_status}); programmatic SVG generation retired.",
    }


def resolve_visual_route(
    visual: dict[str, Any],
    *,
    asset_registry: dict[str, dict[str, Any]] | None = None,
    host_candidates: list[dict[str, Any]] | None = None,
    search_available: bool = True,
    auto_search: bool = False,
    http_get: Callable[[str, int], dict[str, Any]] | None = None,
    learner_level: str = "beginner",
    fallback_decision: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Strict Web-Image-First routing: Reuse -> Discover/Evaluate -> Download -> Unmet Obligation.

    Never falls back to programmatic SVG generation.
    """
    from .bvia import rank_image_candidates

    concept = visual.get("concept", "")
    # Route 1: Reuse verified local asset
    if asset_registry:
        reusable = asset_registry.get(visual.get("id", "")) or asset_registry.get(concept)
        if reusable and reusable.get("relative_path"):
            return {
                "route": "reuse_local_asset",
                "visual": {**visual, "local_fallback": reusable["relative_path"], "asset_policy": "offline_only"},
                "search_status": "FOUND",
            }

    # Route 2: Rank supplied host candidates or execute real web image discovery
    candidates = list(host_candidates or [])
    attempted = list((fallback_decision or {}).get("queries_attempted") or visual.get("search_queries") or [])
    rejection_reasons: list[str] = list((fallback_decision or {}).get("rejection_reasons") or [])
    derived_status = "NO_IMAGE_EXISTS" if search_available else "SEARCH_UNAVAILABLE"

    if not candidates and auto_search and search_available:
        queries = attempted or generate_visual_search_queries(
            visual.get("concept_title") or visual.get("objective") or concept or "diagram",
            visual.get("objective", ""),
            learner_level=learner_level,
            diagram_type=visual.get("kind", "diagram"),
        )
        search_res = search_web_images(queries, http_get=http_get)
        attempted = search_res["queries_attempted"]
        candidates = search_res["candidates"]
        rejection_reasons.extend(r["reason"] for r in search_res["rejected"])
        derived_status = search_res["search_status"]

    ranked = rank_image_candidates(candidates, learner_level=learner_level) if candidates else []
    for cand in ranked:
        if cand.get("url") and cand.get("source") and cand.get("rights"):
            resolved = {
                **visual,
                "kind": visual.get("kind") or "source_figure",
                "url": cand["url"],
                "source": cand["source"],
                "rights": cand["rights"],
                "alt": cand.get("alt") or visual.get("objective", ""),
                "relevance": cand.get("relevance") or visual.get("objective", ""),
                "accessibility": cand.get("accessibility"),
                "require_permissive_license": True,
                "candidate_count_evaluated": len(candidates),
            }
            return {"route": "external_image_download", "visual": resolved, "search_status": "FOUND"}

    # Fallback if host_candidates lacked accessibility fields for strict ranker but still had permissive url/source/rights
    for cand in candidates:
        if cand.get("url") and cand.get("source") and cand.get("rights") and cand.get("technical_accuracy") is not False:
            from .media import verify_license_and_rights
            try:
                verify_license_and_rights(cand["rights"], require_permissive=True)
            except ValueError as exc:
                rejection_reasons.append(str(exc))
                continue
            resolved = {
                **visual,
                "kind": visual.get("kind") or "source_figure",
                "url": cand["url"],
                "source": cand["source"],
                "rights": cand["rights"],
                "alt": cand.get("alt") or visual.get("objective", ""),
                "relevance": cand.get("relevance") or visual.get("objective", ""),
                "require_permissive_license": True,
                "candidate_count_evaluated": len(candidates),
            }
            return {"route": "external_image_download", "visual": resolved, "search_status": "FOUND"}

    # Route 3: Honest unmet visual obligation (NO SVG fallback!)
    dec = fallback_decision or {}
    unmet = record_unmet_visual_obligation(
        visual,
        search_status=dec.get("search_status", derived_status if derived_status != "FOUND" else "NO_IMAGE_EXISTS"),
        queries_attempted=attempted,
        sources_considered=dec.get("sources_considered", ["wikimedia_commons"]),
        rejection_reasons=rejection_reasons,
        justification=dec.get("justification", visual.get("fallback_justification", "")),
    )
    return {
        "route": "unmet_visual_obligation",
        "visual": {**visual, "unmet_obligation": unmet},
        "search_status": unmet["search_status"],
    }


def verify_visual_obligations(
    obligations: list[dict[str, Any]],
    bodies: dict[str, str],
    vault: Path,
) -> dict[str, Any]:
    """Checker verification: verify local embeds, provenance, explanation density, and unmet obligations."""
    from . import contained
    errors: list[str] = []
    for ob in obligations:
        oid = ob.get("obligation_id", "<unknown>")
        chid = ob.get("chapter_id", "")
        if ob.get("status") in {"unavailable", "unmet_obligation", "blocked"}:
            errors.append(f"{oid}: unmet visual obligation ({ob.get('failure_reason', 'no permitted image acquired')})")
            continue
        rel = ob.get("local_asset_path")
        if not rel or not contained(vault, rel).is_file():
            errors.append(f"{oid}: missing local asset {rel}")
            continue
        body = bodies.get(chid, "")
        if rel not in body:
            errors.append(f"{oid}: asset {rel} is not embedded in chapter {chid}")
            continue
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


def select_acquisition_strategy(visual: dict[str, Any]) -> str:
    """Choose retrieve_figure (external), native_mermaid, markdown_table, or interactive_sequence."""
    renderer = visual.get("renderer")
    if not renderer:
        from .renderers import KINDS
        kind = visual.get("kind", "")
        renderer = KINDS.get(kind, ("external",))[0]
    if renderer not in STRATEGY_MAP:
        raise ValueError(f"Unsupported visual strategy renderer '{renderer}'; programmatic SVG creation is retired.")
    return STRATEGY_MAP[renderer]


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
        if result.get("embed"):
            return "embedded"
        return "inspected" if (result.get("inspection") or {}).get("inspection_performed") else "file_validated"
    if status == "unavailable":
        return "unmet_obligation" if result.get("unmet_visual_obligation") else "blocked"
    if status == "failed":
        return "failed"
    return "planned"


def build_asset_manifest(
    plan: dict[str, Any],
    results: dict[str, dict[str, Any]],
    *,
    collection_slug: str | None = None,
) -> dict[str, Any]:
    """Build a canonical LAVIA asset manifest with deduplication, inspection, and provenance."""
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
        renderer = result.get("renderer", "external")
        method = "external_download" if renderer == "external" else f"native_{renderer}"
        lifecycle = _lifecycle_from_result(result)
        suffix = Path(canonical_path).suffix.lstrip(".") if canonical_path else ""
        try:
            strategy = select_acquisition_strategy({"renderer": renderer, **visual})
        except ValueError:
            strategy = "retired_svg_prohibited"

        inspection = result.get("inspection") or {}
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
            "inspection": {
                "performed": bool(inspection.get("inspection_performed")),
                "readable_for_embedding": inspection.get("readable_for_embedding"),
                "width": inspection.get("width"),
                "height": inspection.get("height"),
                "text_labels_extracted": inspection.get("text_labels_extracted", []),
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
                "unmet_obligation": bool(result.get("unmet_visual_obligation")),
            },
        })

    return {
        "schema_version": "lavia-manifest/v2",
        "collection_slug": slug,
        "assets": entries,
        "summary": {
            "total": len(entries),
            "verified": sum(1 for e in entries if e["publication"]["status"] == "verified"),
            "failed": sum(1 for e in entries if e["lifecycle_state"] == "failed"),
            "blocked": sum(1 for e in entries if e["lifecycle_state"] in {"blocked", "unmet_obligation"}),
            "unmet_obligations": sum(1 for e in entries if e["publication"]["unmet_obligation"]),
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
