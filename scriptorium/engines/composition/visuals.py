"""Visual acquisition and embedding executor (A6 Visuals / A7 Assets).

Programmatic SVG diagram generation has been retired. Educational visuals are
resolved strictly via Web Image Research -> Candidate Evaluation -> Permissive
Rights Verification -> Local Download -> Image Inspection -> Grounded Embedding,
or native Markdown Mermaid / structured tables / constrained interactive frames.
Unresolved visual requirements are recorded explicitly rather than synthesized.
"""
from __future__ import annotations

import json
from pathlib import Path
import posixpath
import time
from typing import Any, Callable

from scriptorium.models import content_hash, slugify


_KIND_ALIASES = {
    "external_image": "source_figure",
    "image": "source_figure",
    "diagram": "source_figure",
    "figure": "source_figure",
    "conceptual_overview": "intuition",
    "overview": "intuition",
}


def _normalize_visual_spec(raw_visual: dict[str, Any]) -> dict[str, Any]:
    """Normalize caller visual fields to canonical representation/media keys."""
    visual = dict(raw_visual)
    if visual.get("preferred_renderer") and not visual.get("renderer"):
        visual["renderer"] = visual["preferred_renderer"]
    raw_kind = str(visual.get("kind") or visual.get("type") or "source_figure").strip().lower()
    visual["kind"] = _KIND_ALIASES.get(raw_kind, raw_kind)
    if not visual.get("objective"):
        visual["objective"] = (
            visual.get("learning_objective")
            or visual.get("caption")
            or visual.get("alt_text")
            or f"Illustrate {visual.get('concept', 'concept')}"
        )
    if not visual.get("alt") and (visual.get("alt_text") or visual.get("caption")):
        visual["alt"] = visual.get("alt_text") or visual.get("caption")
    if not visual.get("relevance") and (visual.get("caption") or visual.get("objective")):
        visual["relevance"] = visual.get("caption") or visual.get("objective")
    if not visual.get("source") and visual.get("url"):
        visual["source"] = visual["url"]
    if not visual.get("rights") and visual.get("origin") == "supplied":
        visual["rights"] = "author-permitted"
    if visual.get("filename_stem") and not visual.get("asset_name"):
        visual["asset_name"] = visual["filename_stem"]
    return visual


def render_visuals(
    vault: Path,
    plan: dict[str, Any],
    drafts: dict[str, str],
    *,
    execute: bool = True,
    http_get: Callable[[str, int], dict[str, Any]] | None = None,
    image_http_get: Callable[[str, int], dict[str, Any]] | None = None,
) -> tuple[dict[str, str], dict[str, dict[str, Any]]]:
    """Execute verified visual acquisition/rendering backends; preserve unmet obligations."""
    from . import bvia, contained, lavia, media, renderers, select_visual
    from .contracts import insert_at_section
    from ..vault import safe_write_note

    bodies, results = dict(drafts), {}
    collection_slug = plan.get("collection_slug") or (
        slugify(plan["topic"]) if plan.get("organize_by_collection") and plan.get("topic") else None
    )
    embed_style = plan.get("embed_style", "wikilink" if collection_slug else None)
    render_version = content_hash(
        b"".join(Path(module.__file__).read_bytes() for module in (renderers, media, lavia))
        + Path(__file__).read_bytes()
    )

    for raw_visual in plan.get("visuals", []):
        visual = _normalize_visual_spec(raw_visual)
        started = time.perf_counter()
        status: dict[str, Any] = {
            "renderer": None,
            "selected_renderer": None,
            "family": None,
            "available": False,
            "attempted": False,
            "status": "planned",
            "input_hash": None,
            "path": None,
            "hash": None,
            "failure_reason": None,
            "fallback": None,
            "renderer_version": render_version,
            "cached": False,
            "embed": None,
            "unmet_visual_obligation": False,
        }
        try:
            chapter = next(c for c in plan["chapters"] if visual["concept"] in c["concepts"])
            selected = select_visual(visual, available=set(renderers.BUILTIN_BACKENDS))
            renderer = selected["renderer"]
            status["renderer"] = renderer
            status["selected_renderer"] = renderer
            status["family"] = selected.get("family")
            status["available"] = renderer in renderers.BUILTIN_BACKENDS

            digest = content_hash(
                json.dumps({"spec": visual, "renderer": renderer, "version": render_version}, sort_keys=True)
            )
            status["input_hash"] = digest
            suffix = renderers.BACKENDS[renderer]["suffix"]
            if collection_slug:
                relative = (
                    f"assets/scriptorium/{slugify(collection_slug)}/"
                    f"{slugify(visual.get('asset_name') or visual['id'])}-{digest[:12]}.{suffix}"
                )
            else:
                relative = f"assets/scriptorium/{digest}.{suffix}"
            status["path"] = relative
            path = contained(vault, relative)

            if not status["available"]:
                raise ValueError(f"Visual backend '{renderer}' is unavailable without an external adapter")

            status["attempted"] = True

            if renderer == "external":
                if (
                    plan.get("source_policy") == "strict"
                    and visual.get("asset_policy", "local_preferred") != "offline_only"
                    and visual.get("origin") != "supplied"
                ):
                    raise ValueError("Source-only policy permits remote acquisition only for explicitly supplied media")

                media_spec = dict(visual)
                if collection_slug and "collection_slug" not in media_spec:
                    media_spec["collection_slug"] = collection_slug
                if embed_style and "embed_style" not in media_spec:
                    media_spec["embed_style"] = embed_style

                # When URL is not yet supplied and live/adapter search is enabled, discover via LAVIA + BVIA
                if not media_spec.get("url") and media_spec.get("asset_policy") != "offline_only":
                    can_search = execute and bool(plan.get("auto_web_image_search", True))
                    routed = lavia.resolve_visual_route(
                        media_spec,
                        host_candidates=media_spec.get("candidates"),
                        search_available=can_search,
                        auto_search=can_search,
                        http_get=http_get,
                        learner_level=plan.get("learner_level", "beginner"),
                    )
                    if routed["route"] == "unmet_visual_obligation":
                        unmet = routed["visual"]["unmet_obligation"]
                        status.update(
                            status="unavailable",
                            path=None,
                            failure_reason=unmet["reason"],
                            unmet_visual_obligation=True,
                            unmet_details=unmet,
                        )
                        continue
                    media_spec = routed["visual"]

                acquired = media.media_artifact(vault, media_spec, digest, execute=execute, http_get=image_http_get)
                findings = media_spec.get("inspection_findings")
                if findings:
                    if findings.get("content_hash") != acquired["hash"]:
                        raise ValueError("Semantic inspection findings do not bind the downloaded image")
                    acquired["inspection"]["semantic_findings"] = findings
                    acquired["inspection"]["text_labels_extracted"] = list(findings.get("text_labels_extracted") or [])
                status.update(acquired)
                status["status"] = "verified"
                embed = status["embed"]
                if embed_style != "wikilink":
                    local_target = posixpath.relpath(status["path"], posixpath.dirname(chapter.get("path", "note.md")) or ".")
                    embed = embed.replace(f"]({status['path']})", f"]({local_target})")
                status["embed"] = embed
                walkthrough = (
                    bvia.compose_visual_walkthrough(
                        media_spec,
                        embed=embed,
                        terminology_registry=plan.get("notation"),
                        inspection=acquired.get("inspection"),
                    )
                    if media_spec.get("explain") or media_spec.get("decode_components") or plan.get("enforce_bvia_walkthrough", True)
                    else embed + "\n\n" + visual.get("interpretation", visual["objective"])
                )
                status["walkthrough"] = walkthrough
                if bodies.get(chapter["id"], "").strip() and embed not in bodies.get(chapter["id"], ""):
                    bodies[chapter["id"]] = insert_at_section(bodies.get(chapter["id"], ""), visual["section"], walkthrough)
                continue

            if renderer == "mermaid":
                artifact_text = renderers.mermaid_source(visual)
                embed = "```mermaid\n" + artifact_text.rstrip() + "\n```"
                val_method = "regenerate safe Mermaid source from bounded nodes/edges"
                val_limits = "Native Mermaid is validated textual source, not a raster bitmap; Obsidian rendering tested separately."
            elif renderer == "table":
                from . import render_table
                artifact_text = render_table(visual.get("table", visual))
                embed = artifact_text
                val_method = "regenerate typed Markdown table from exact rows/units"
                val_limits = "Tabular text rendering only."
            elif renderer == "interactive":
                artifact_text = renderers.interactive_html(visual)
                target = posixpath.relpath(relative, posixpath.dirname(chapter.get("path", "note.md")) or ".")
                embed = f"[Open interactive state sequence]({target})"
                val_method = "regenerate CSP-locked textual frame sequence HTML"
                val_limits = "Constrained standalone HTML viewer; browser appearance requires live viewer testing."
            else:
                raise ValueError(f"Unsupported backend '{renderer}'; programmatic SVG generation has been retired.")

            if execute:
                if path.exists():
                    if path.read_text(encoding="utf-8") != artifact_text:
                        raise ValueError("Content-addressed visual was altered; repair the asset before reusing it")
                    status["cached"] = True
                else:
                    safe_write_note(path, artifact_text, validate_properties=False)
            elif not path.is_file() or path.read_text(encoding="utf-8") != artifact_text:
                raise ValueError("Rendered asset is missing or changed")

            status.update(
                status="verified",
                hash=content_hash(artifact_text),
                embed=embed,
                validation={"method": val_method, "result": "pass", "limits": val_limits},
            )
            if embed not in bodies.get(chapter["id"], ""):
                bodies[chapter["id"]] = insert_at_section(
                    bodies.get(chapter["id"], ""),
                    visual["section"],
                    embed + "\n\n" + visual.get("interpretation", visual["objective"]),
                )
        except (ValueError, KeyError, TypeError, OSError, ArithmeticError) as exc:
            status.update(
                status="failed" if status["available"] else "unavailable",
                failure_reason=str(exc),
                unmet_visual_obligation=not status["available"],
            )
        finally:
            status["elapsed_seconds"] = time.perf_counter() - started
            results[visual["id"]] = status

    return bodies, results


def acquire_and_inspect_visuals(
    vault: Path,
    plan: dict[str, Any],
    *,
    execute: bool = True,
    http_get: Callable[[str, int], dict[str, Any]] | None = None,
    image_http_get: Callable[[str, int], dict[str, Any]] | None = None,
) -> tuple[dict[str, list[str]], dict[str, dict[str, Any]]]:
    """Acquire, validate, and inspect visuals BEFORE prose composition.

    Returns ``(walkthroughs_by_chapter, results)`` so the writer can compose
    explanations grounded in inspected image content rather than bolting
    images onto pre-written chapters.
    """
    _, results = render_visuals(vault, plan, {}, execute=execute, http_get=http_get, image_http_get=image_http_get)
    walkthroughs_by_chapter: dict[str, list[str]] = {}
    chapters = plan.get("chapters") or []
    for raw_visual in plan.get("visuals", []):
        vid = raw_visual.get("id")
        if not vid or vid not in results:
            continue
        res = results[vid]
        wt = res.get("walkthrough")
        if not wt:
            continue
        owner = next((c["id"] for c in chapters if raw_visual.get("concept") in c.get("concepts", [])), None)
        if owner:
            walkthroughs_by_chapter.setdefault(owner, []).append(wt)
    return walkthroughs_by_chapter, results


def acquire_node_visuals(
    vault_root: Path,
    *,
    collection_title: str,
    concept_id: str,
    node_title: str,
    proposed_path: str,
    node_visuals: list[dict[str, Any]],
    learner_level: str = "beginner",
    source_policy: str = "adaptive",
    http_get: Callable[[str, int], dict[str, Any]] | None = None,
    image_http_get: Callable[[str, int], dict[str, Any]] | None = None,
) -> tuple[list[str], dict[str, dict[str, Any]]]:
    """Acquire and inspect visuals for a single topic node before prose composition."""
    norm_visuals: list[dict[str, Any]] = []
    for idx_v, raw_v in enumerate(node_visuals, 1):
        v = dict(raw_v)
        v.setdefault("id", v.get("visual_id") or f"vis-{slugify(concept_id)}-{idx_v}")
        v.setdefault("concept", concept_id)
        v.setdefault("objective", v.get("learning_objective") or f"Visually illustrate {node_title}")
        norm_visuals.append(v)

    v_plan = {
        "source_policy": source_policy,
        "topic": collection_title,
        "collection_slug": slugify(collection_title),
        "organize_by_collection": True,
        "auto_web_image_search": True,
        "learner_level": learner_level,
        "chapters": [{"id": concept_id, "path": proposed_path, "concepts": [concept_id]}],
        "visuals": norm_visuals,
    }
    walkthroughs_by_ch, v_results = acquire_and_inspect_visuals(
        vault_root,
        v_plan,
        execute=True,
        http_get=http_get,
        image_http_get=image_http_get,
    )
    return walkthroughs_by_ch.get(concept_id, []), v_results
