"""Canonical collection generation, checkpointing and Obsidian publication."""
from __future__ import annotations
from copy import deepcopy
from datetime import date
import json
import re
from pathlib import Path
from typing import Any
import yaml
from scriptorium.models import content_hash, parse_note, slugify


def resolve_generated_links(content: str, nodes: dict[str, Any]) -> str:
    """Use real Obsidian file paths when a display title differs from its filename."""
    targets = {node.title: node.proposed_path.removesuffix(".md") for node in nodes.values()
               if Path(node.proposed_path).stem != node.title}
    fenced = False
    lines = []
    for line in content.splitlines():
        if re.match(r"^\s*(?:>\s*)*(?:```|~~~)", line):
            fenced = not fenced
        if not fenced:
            def replace(match):
                title, anchor, alias = match.groups()
                if title not in targets:
                    return match.group(0)
                return "[[" + targets[title] + (anchor or "") + (alias or "|" + title) + "]]"
            line = re.sub(r"(?<!!)\[\[([^\]|#]+)(#[^\]|]+)?(\|[^\]]+)?\]\]", replace, line)
        lines.append(line)
    return "\n".join(lines) + "\n"

def generate_collection_with_checkpoints(
    vault_root: Path,
    kcp: Any,
    preferences: Any,
    *,
    batch_size: int = 5,
    fail_on_concept_id: str | None = None,
    resume: bool = True,
    source_facts_by_node: dict[str, list[str]] | None = None,
    visual_specs: dict[str, list[dict[str, Any]]] | None = None,
    http_get: Any = None,
    overwrite_policy: str = "reconcile",
    created: Any = None,
    teaching_by_node: dict[str, dict] | None = None,
) -> dict[str, Any]:
    """F06: Execute dependency-ordered batches with SHA-256 checkpoints, honest partial reporting, and idempotent resume."""
    from scriptorium.engines.vault import (
        classify_knowledge_hierarchy,
        incremental_update_note,
        render_parent_moc,
        safe_write_note,
        validate_obsidian_properties,
    )

    from .writing import compose_chapter
    from .._collection_intelligence import apply_progressive_disclosure
    from scriptorium.models import contained_path

    assert kcp.plan is not None, "KnowledgeCollectionPlan.plan must be populated before generation."
    plan = kcp.plan
    vault_root = Path(vault_root)
    vault_root.mkdir(parents=True, exist_ok=True)
    node_map = {n.concept_id: n for n in plan.nodes}
    root_h = classify_knowledge_hierarchy(plan.title)
    root_domain = (plan.scope_summary or {}).get("domain", root_h["domain"])
    root_mt = root_h["master_topic"] if root_h["master_topic"] != "General Knowledge" else plan.title

    ckpt_dir = vault_root / ".scriptorium" / "collections"
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    ckpt_path = ckpt_dir / f"{plan.collection_id}.checkpoint.json"
    run_input_hash = content_hash(json.dumps({
        "plan": plan.to_dict(), "preferences": vars(preferences),
        "facts": source_facts_by_node, "visuals": visual_specs, "teaching": teaching_by_node,
    }, sort_keys=True, default=str))

    # Load and REVALIDATE existing checkpoint on resume (never blindly trust stale metadata!)
    committed_hashes: dict[str, str] = {}
    saved_records: dict[str, dict] = {}
    note_states: dict[str, str] = {n.concept_id: "PLANNED" for n in plan.nodes}
    if resume and ckpt_path.is_file():
        try:
            prev = json.loads(ckpt_path.read_text(encoding="utf-8"))
            if prev.get("input_hash") != run_input_hash:
                prev = {}
            for cid, info in (prev.get("committed") or {}).items():
                fpath = contained_path(vault_root, info["path"])
                if fpath.is_file():
                    actual_hash = content_hash(fpath.read_text(encoding="utf-8-sig"))
                    assets_valid = all(
                        contained_path(vault_root, asset["path"]).is_file()
                        and content_hash(contained_path(vault_root, asset["path"]).read_bytes()) == asset["hash"]
                        for asset in info.get("assets", [])
                    )
                    if actual_hash == info.get("sha256") and assets_valid:
                        committed_hashes[cid] = actual_hash
                        saved_records[cid] = info.get("record", {})
                        note_states[cid] = "COMMITTED"
                    else:
                        note_states[cid] = "NEEDS_REVIEW"
                else:
                    note_states[cid] = "PLANNED"
        except Exception:
            # Corrupted checkpoint metadata -> safely rebuild from scratch without crashing silently
            committed_hashes = {}
            saved_records = {}
            note_states = {n.concept_id: "PLANNED" for n in plan.nodes}

    # Respect F03 reuse_unchanged / reuse_with_link decisions
    reuse_map = (kcp.existing_note_reconciliation or {}).get("decisions") or {}
    for cid, dec in reuse_map.items():
        if dec.get("decision") in {"reuse_unchanged", "reuse_with_link"} and dec.get("matched_path"):
            if (vault_root / dec["matched_path"]).is_file():
                note_states[cid] = "REUSED"

    # Partition generation_order into dependency-aware batches (children first, then group/root indexes)
    children_order = [cid for cid in plan.generation_order if cid in node_map and node_map[cid].note_role in {"child", "single"}]
    index_order = [cid for cid in plan.generation_order if cid in node_map and node_map[cid].note_role in {"group_index", "root_index"}]
    batches: list[list[str]] = [
        children_order[i:i + max(1, batch_size)] for i in range(0, len(children_order), max(1, batch_size))
    ]
    if index_order:
        batches.append(index_order)

    committed_records: dict[str, dict[str, Any]] = {}
    for cid, digest in committed_hashes.items():
        if cid in node_map:
            record = saved_records.get(cid, {})
            committed_records[cid] = {"path": node_map[cid].proposed_path, "sha256": digest, "validated": True,
                "record": record, "assets": [{"path": value["path"], "hash": value["hash"]} for value in record.get("visuals", {}).values()]}

    records: list[dict[str, Any]] = [record for record in saved_records.values() if record]
    written_paths: list[str] = []
    failed_nodes: list[dict[str, Any]] = []
    skipped_already_committed = 0

    for batch_idx, batch in enumerate(batches, 1):
        # Do NOT falsely finalize parent index batch if any child failed!
        if batch == index_order and failed_nodes:
            for cid in batch:
                note_states[cid] = "DEFERRED"
            break

        for cid in batch:
            node = node_map[cid]
            if note_states.get(cid) in {"COMMITTED", "REUSED"}:
                skipped_already_committed += 1
                continue

            note_states[cid] = "GENERATING"
            target_path = contained_path(vault_root, node.proposed_path)
            visual_report = {}
            try:
                if fail_on_concept_id and cid == fail_on_concept_id:
                    raise RuntimeError(f"Injected failure on '{cid}' for checkpoint recovery test.")

                if node.note_role in {"root_index", "group_index"}:
                    content = render_parent_moc(
                        node, plan, node_map, preferences, domain=root_domain, master_topic=root_mt
                    )
                else:
                    teaching = dict((teaching_by_node or {}).get(cid) or (teaching_by_node or {}).get(node.title) or {})
                    facts = (source_facts_by_node or {}).get(cid) or teaching.get("source_facts")
                    walkthroughs_for_node: list[str] | None = None
                    node_visuals = (visual_specs or {}).get(cid) or (visual_specs or {}).get(node.title) or teaching.get("visual_specs")
                    requirements = teaching.get("visual_requirements") or (node.template_plan or {}).get("visual_requirements") or []
                    if not requirements:
                        requirements = [goal for goal in teaching.get("objectives", [])
                                        if re.match(r"(?i)^(?:visualize|draw|interpret (?:a |the )?(?:graph|diagram))\b", goal)]
                    if not node_visuals and requirements:
                        node_visuals = [{"id": f"{cid}-visual-{i}", "kind": "source_figure", "renderer": "external",
                                         "section": "Visual Explanation", "concept": cid, "concept_title": node.title,
                                         "objective": requirement if isinstance(requirement, str) else requirement["objective"],
                                         "research_required": True} for i, requirement in enumerate(requirements)]
                    if teaching.get("visual_required") and not node_visuals:
                        raise ValueError("Required visual learning obligation has no acquisition specification")
                    visual_report = {}
                    if node_visuals:
                        from scriptorium.engines.composition.visuals import acquire_node_visuals

                        walkthroughs_for_node, visual_report = acquire_node_visuals(
                            vault_root,
                            collection_title=plan.title,
                            concept_id=cid,
                            node_title=node.title,
                            proposed_path=node.proposed_path,
                            node_visuals=node_visuals,
                            learner_level=preferences.depth,
                            source_policy=preferences.source_policy,
                            image_http_get=http_get,
                        )
                        failed_visuals = [key for key, value in visual_report.items() if value.get("status") != "verified"]
                        if failed_visuals:
                            raise ValueError("Unfulfilled visual obligations: " + ", ".join(failed_visuals))
                        if teaching.get("require_complete") and any(not value.get("inspection", {}).get("semantic_findings") for value in visual_report.values()):
                            raise ValueError("Hash-bound semantic image inspection must precede complete educational composition")
                        teaching["assets"] = [{"path": value["path"], "hash": value["hash"]} for value in visual_report.values()]
                        teaching["inspections"] = [value["inspection"] for value in visual_report.values() if value.get("inspection")]
                    composition_report = {}
                    content = compose_chapter(
                        node,
                        plan,
                        node_map,
                        preferences,
                        domain=root_domain,
                        master_topic=root_mt,
                        source_facts=facts,
                        teaching_extensions=teaching,
                        execution_report=composition_report,
                        created=created,
                        visual_walkthroughs=walkthroughs_for_node or None,
                    )
                    # Apply F11 progressive disclosure if applicable
                    m_id = (node.template_plan or {}).get("master") or preferences.master
                    pd_res = apply_progressive_disclosure(content, master=m_id, topic=node.title)
                    content = pd_res["content"]

                note_states[cid] = "VALIDATING"
                content = resolve_generated_links(content, node_map)
                errs = validate_obsidian_properties(content)
                if errs:
                    raise ValueError("; ".join(errs))
                note_states[cid] = "VALIDATED"

                # Safe non-destructive reconciliation if file exists
                expected_digest = content_hash(target_path.read_bytes().decode("utf-8-sig")) if target_path.exists() else None
                if target_path.exists() and overwrite_policy == "reconcile":
                    existing_text = target_path.read_text(encoding="utf-8-sig")
                    gp = parse_note(content)
                    sec_map = {s.heading: "\n".join(s.content.splitlines()[1:]).strip() for s in gp.sections if s.level == 2}
                    upd = incremental_update_note(
                        existing_text,
                        append_sections=sec_map,
                        property_updates={"collection_id": plan.collection_id, "parent_topic": gp.metadata.get("parent_topic")},
                        update_date=date.today(),
                    )
                    content = upd["content"]

                from ..mathematics import validate_formula_folds
                formula_gate = validate_formula_folds(content)
                if not formula_gate["passed"]:
                    raise ValueError("Final publication formula gate failed")
                if node.note_role not in {"root_index", "group_index"} and composition_report.get("contract"):
                    from .writing import Composition, validate
                    final_review = validate(Composition(**composition_report["contract"]), parse_note(content).body)
                    composition_report["validation"] = final_review
                    if teaching.get("require_complete") and not final_review["complete"]:
                        raise ValueError("Final educational content does not fulfill its teaching contract")
                safe_write_note(target_path, content, validate_properties=True, expected_digest=expected_digest, vault_root=vault_root)
                written_paths.append(node.proposed_path)
                records.append({"concept_id": cid, "title": node.title, "role": node.note_role, "path": node.proposed_path, "status": "created", "word_count": len(content.split()), "composition": composition_report if node.note_role not in {"root_index", "group_index"} else {}, "visuals": visual_report if node.note_role not in {"root_index", "group_index"} else {}})
                digest = content_hash(target_path.read_text(encoding="utf-8-sig"))
                committed_records[cid] = {"path": node.proposed_path, "sha256": digest, "validated": True,
                    "record": records[-1], "assets": [{"path": value["path"], "hash": value["hash"]} for value in visual_report.values()]}
                note_states[cid] = "COMMITTED"
            except Exception as exc:
                note_states[cid] = "FAILED"
                failed_nodes.append({"concept_id": cid, "title": node.title, "path": node.proposed_path, "error": str(exc), "visuals": visual_report})

        # Save checkpoint atomically after every batch
        ckpt_payload = {
            "input_hash": run_input_hash,
            "collection_id": plan.collection_id,
            "batch_completed": batch_idx,
            "total_batches": len(batches),
            "note_states": note_states,
            "committed": committed_records,
            "failed": failed_nodes,
            "pending": [cid for cid, st in note_states.items() if st in {"PLANNED", "READY", "DEFERRED", "FAILED"}],
            "complete": not failed_nodes and all(st in {"COMMITTED", "REUSED"} for st in note_states.values()),
        }
        safe_write_note(ckpt_path, json.dumps(ckpt_payload, indent=2, ensure_ascii=False), validate_properties=False, vault_root=vault_root)

    # Persist synchronized manifest
    manifest_path = ckpt_dir / f"{plan.collection_id}.yaml"
    complete = not failed_nodes and all(st in {"COMMITTED", "REUSED"} for st in note_states.values())
    manifest = {
        "collection_id": plan.collection_id,
        "title": plan.title,
        "organization": plan.organization,
        "planned_count": len(plan.nodes),
        "completed_count": sum(1 for st in note_states.values() if st in {"COMMITTED", "REUSED"}),
        "failed_count": len(failed_nodes),
        "complete": complete,
        "checkpoint_path": str(ckpt_path),
        "note_states": note_states,
        "nodes": records,
        "planned_paths": list(plan.planned_paths),
        "content_state": "generated",
        "verified": False,
    }
    safe_write_note(manifest_path, yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), validate_properties=False, vault_root=vault_root)

    kcp.generation = {
        "batches": batches,
        "checkpoint_path": str(ckpt_path),
        "note_states": note_states,
        "status": "COMMITTED" if complete else "PARTIAL_FAILURE",
    }

    return {
        "collection_id": plan.collection_id,
        "complete": complete,
        "committed_count": len(committed_records),
        "completed_count": sum(1 for st in note_states.values() if st in {"COMMITTED", "REUSED"}),
        "planned_count": len(plan.nodes),
        "written_paths": written_paths,
        "records": records,
        "content_state": "generated",
        "verified": False,
        "reused_count": sum(1 for st in note_states.values() if st == "REUSED"),
        "skipped_already_committed": skipped_already_committed,
        "failed_count": len(failed_nodes),
        "failed_nodes": failed_nodes,
        "checkpoint_path": str(ckpt_path),
        "manifest_path": str(manifest_path),
        "note_states": note_states,
        "manifest": manifest,
    }




def publish_composition(vault: Path, plan: dict[str, Any], drafts: dict[str, str], *,
                        evidence: dict[str, Any], reviews: dict[str, Any],
                        expected_hashes: dict[str, str] | None = None,
                        allow_draft: bool = False) -> dict[str, Any]:
    """Preflight whole collection; checkpoint individual atomic writes using E6.

    No overwrite without a matching expected digest. Human/model review is explicit
    evidence, not a deterministic quality score. Internal state stays outside topics.
    """
    from ..vault import safe_write_note
    from . import (contained, evidence_status, five_key_note, validate_chapter, render_moc,
                   wikilink_errors, inspect_assets, _validate_local_first_visuals, _derive_readiness_state)
    from .contracts import validate_obligations
    from .._token_optimizer import MultiLevelCache
    from . import lavia
    if not all(isinstance(value, dict) for value in (plan, drafts, evidence, reviews)) or any(not isinstance(body, str) for body in drafts.values()):
        raise ValueError("Plan, drafts, evidence and reviews must be JSON objects; draft bodies must be strings")
    plan = deepcopy(plan)
    if plan.get("version") != 2 or not plan.get("obligations"):
        return {"complete": False, "errors": ["rebuild the composition with executable obligations"], "written_paths": []}
    drafts, visual_results = prepare_composition(vault, plan, drafts)
    cache = MultiLevelCache(disk_dir=contained(vault, ".scriptorium/cache/composition"))
    validation = validate_obligations(plan, drafts, evidence=evidence, reviews=reviews,
                                      visuals=visual_results, vault=vault, cache=cache)
    obligations = [o for c in plan["concepts"] for o in c["research_obligations"]]
    status = evidence_status(obligations, evidence)
    errors = [*validation["errors"], *[f"pending evidence: {oid}" for oid in status["pending"]]]
    semantic_error_count = len(errors)
    documents = {}
    for i, chapter in enumerate(plan["chapters"]):
        body = drafts.get(chapter["id"], "")
        if not body.strip():
            errors.append(f"missing authored chapter: {chapter['id']}")
        next_title = Path(plan["chapters"][i + 1]["path"]).stem if i + 1 < len(plan["chapters"]) else None
        text = five_key_note(plan, chapter["id"], chapter["title"], body, next_title)
        sections = list(dict.fromkeys([*chapter.get("sections", []), *[c.get("section", c["title"]) for c in plan["concepts"] if c["id"] in chapter["concepts"]]]))
        errors.extend(f"{chapter['id']}: {e}" for e in validate_chapter(text, required_sections=sections))
        documents[chapter["path"]] = text
    documents[plan["moc_path"]] = five_key_note(plan, f"{slugify(plan['topic'])}.moc", "Map of Contents", render_moc(plan), Path(plan["chapters"][0]["path"]).stem)
    errors.extend(wikilink_errors(vault, documents))
    asset_errors, asset_hashes = inspect_assets(vault, documents, visual_results)
    errors.extend(asset_errors)
    visual_manifest, lavia_errors = _validate_local_first_visuals(vault, plan, drafts, visual_results)
    errors.extend(lavia_errors)
    current_hashes = {}
    for relative, text in documents.items():
        target = contained(vault, relative)
        current_hashes[relative] = content_hash(target.read_text(encoding="utf-8-sig")) if target.exists() else None
        if target.exists() and target.read_text(encoding="utf-8-sig") != text and (expected_hashes or {}).get(relative) != current_hashes[relative]:
            errors.append(f"existing chapter needs expected digest: {relative}")
    if errors:
        validation["outcomes"]["structural"] = {"status": "fail" if len(errors) > semantic_error_count else "pass",
                                                   "method": "YAML, sections, fences, links, assets and expected digests"}
        readiness = _derive_readiness_state(errors=errors, validation=validation, visual_results=visual_results, written_paths=[])
        report = {"complete": False, "readiness_state": readiness, "errors": errors, "written_paths": [], "validation": validation, "renderers": visual_results,
                  "manifest": visual_manifest, "reviews": reviews, "evidence": evidence}
        report_path = contained(vault, f".scriptorium/validation/col-{slugify(plan['topic'])}.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        safe_write_note(report_path, json.dumps(report, indent=2, ensure_ascii=False), validate_properties=False)
        if not allow_draft:
            return report
        # Explicit draft policy: persist authored Markdown chapters while honestly reporting non-complete readiness.
        draft_written: list[str] = []
        for relative, text in documents.items():
            target = contained(vault, relative)
            result = safe_write_note(target, text, expected_digest=current_hashes[relative], validate_properties=False)
            if result["written"]:
                draft_written.append(relative)
        report["written_paths"] = draft_written
        report["readiness_state"] = _derive_readiness_state(errors=errors, validation=validation, visual_results=visual_results, written_paths=draft_written)
        return report
    state_path = contained(vault, f".scriptorium/collections/col-{slugify(plan['topic'])}.json")
    state = {"composition": plan, "spec_hash": plan["spec_hash"], "evidence": evidence, "reviews": reviews,
             "checkpoints": {}, "asset_hashes": asset_hashes, "complete": False, "errors": [],
             "validation": validation, "renderers": visual_results, "manifest": visual_manifest}
    state["validation"]["outcomes"]["structural"] = {"status": "pass", "method": "YAML, sections, fences, links, assets and expected digests"}
    state_path.parent.mkdir(parents=True, exist_ok=True)
    written = []
    def checkpoint() -> None:
        safe_write_note(state_path, json.dumps(state, indent=2, ensure_ascii=False), validate_properties=False)
    for relative, text in documents.items():
        try:
            result = safe_write_note(contained(vault, relative), text, expected_digest=current_hashes[relative], validate_properties=False)
            state["checkpoints"][relative] = {"hash": content_hash(text), "status": "COMMITTED"}
            if result["written"]:
                written.append(relative)
            checkpoint()
        except (OSError, ValueError) as exc:
            state["errors"].append(f"{relative}: {exc}")
            checkpoint()
            return {**state, "written_paths": written}
    if plan.get("organize_by_collection") or plan.get("collection_slug"):
        lavia.save_asset_manifest(vault, visual_manifest)
    readiness = _derive_readiness_state(errors=[], validation=validation, visual_results=visual_results, written_paths=written)
    state["complete"] = True
    state["readiness_state"] = readiness
    checkpoint()
    return {**state, "written_paths": written}


def prepare_composition(vault: Path, plan: dict[str, Any], drafts: dict[str, str], *, execute: bool = True) -> tuple[dict, dict]:
    """Prepare the actual artifact before review; returned bodies are the receipt subjects."""
    from . import contained
    from .contracts import prepare_drafts
    from .visuals import render_visuals
    from . import lavia
    bodies = prepare_drafts(plan, drafts)
    bodies, results = render_visuals(vault, plan, bodies, execute=execute)
    manifest = lavia.build_asset_manifest(plan, results, collection_slug=plan.get("collection_slug"))
    if execute:
        from ..vault import safe_write_note
        path = contained(vault, f".scriptorium/renderers/col-{slugify(plan['topic'])}.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        safe_write_note(
            path,
            json.dumps({"spec_hash": plan["spec_hash"], "renderers": results, "manifest": manifest}, indent=2),
            validate_properties=False,
        )
        if plan.get("organize_by_collection") or plan.get("collection_slug"):
            lavia.save_asset_manifest(vault, manifest)
    return {cid: body.strip() + "\n" for cid, body in bodies.items()}, results


