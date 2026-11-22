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


def render_visuals(
    vault: Path,
    plan: dict[str, Any],
    drafts: dict[str, str],
    *,
    execute: bool = True,
    http_get: Callable[[str, int], dict[str, Any]] | None = None,
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

    for visual in plan.get("visuals", []):
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

                # When URL is not yet supplied and live/adapter search is requested, discover via LAVIA + BVIA
                if not media_spec.get("url") and media_spec.get("asset_policy") != "offline_only":
                    routed = lavia.resolve_visual_route(
                        media_spec,
                        host_candidates=media_spec.get("candidates"),
                        search_available=execute and bool(media_spec.get("search_queries") or plan.get("auto_web_image_search") or http_get),
                        auto_search=execute and bool(media_spec.get("search_queries") or plan.get("auto_web_image_search") or http_get),
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

                acquired = media.media_artifact(vault, media_spec, digest, execute=execute)
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
                    if media_spec.get("explain") or media_spec.get("decode_components") or plan.get("enforce_bvia_walkthrough")
                    else embed + "\n\n" + visual.get("interpretation", visual["objective"])
                )
                if embed not in bodies.get(chapter["id"], ""):
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
