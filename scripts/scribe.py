#!/usr/bin/env python3
"""Unified thin CLI entry point delegating to Scriptorium's six cohesive engines."""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

from scriptorium.engines.orchestration import OrchestrationEngine
from scriptorium.engines.pedagogy import PedagogyEngine
from scriptorium.engines.quality import QualityEngine
from scriptorium.engines import research as research_mod
from scriptorium.engines import _pedagogical_core as ped_core_mod
from scriptorium.engines.vault import VaultEngine
from scriptorium.models import dump_frontmatter


def _resolve_compose_vault(explicit_vault: Path | None) -> Path | None:
    """Resolve explicit --vault, or honor configured vault + resolve_notes_folder()."""
    if explicit_vault is not None:
        return explicit_vault
    try:
        from vault_index import resolve_notes_folder, resolve_vault_root
        vault_root = resolve_vault_root(None)
        notes_folder = resolve_notes_folder(vault_root)
        if notes_folder:
            candidate = vault_root / notes_folder
            if candidate.is_dir():
                return candidate
        return vault_root
    except (ValueError, OSError):
        return None


def _composition_preferences(spec):
    from scriptorium.engines._interactive import ResolvedNotePreferences
    return ResolvedNotePreferences("Rigorous topic understanding", "M1", None, "comprehensive", {},
        "hierarchical_collection", [], spec.get("source_policy", "adaptive"))


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Fast passthrough for rich nested sub-CLIs
    args_list = list(sys.argv[1:] if argv is None else argv)
    if args_list and args_list[0] == "research":
        return research_mod.main(args_list[1:])
    if args_list and args_list[0] == "pedagogy":
        return ped_core_mod.main(args_list[1:])

    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_route = sub.add_parser("route", help="Normalize request, resolve constraints, and route to M1-M7.")
    p_route.add_argument("request")
    p_route.add_argument("--source-policy", choices=("strict", "source_first", "adaptive"))
    p_route.add_argument("--has-source", action="store_true")
    p_route.add_argument("--trace", action="store_true")

    p_props = sub.add_parser("properties", help="Generate Obsidian Properties YAML for a topic and note type.")
    p_props.add_argument("--topic", required=True)
    p_props.add_argument("--note-type", default="deep-notes")
    p_props.add_argument("--domain")
    p_props.add_argument("--master-topic")
    p_props.add_argument("--subdomain")
    p_props.add_argument("--format", choices=("yaml", "json"), default="yaml")

    p_update = sub.add_parser("update", help="Incrementally update sections or Properties in an existing note.")
    p_update.add_argument("file", type=Path)
    p_update.add_argument("--section", action="append", default=[], help="Heading=New body content")
    p_update.add_argument("--add-tag", action="append", default=[])
    p_update.add_argument("--dry-run", action="store_true")

    p_migrate = sub.add_parser("migrate", help="Ensure canonical Obsidian Properties on an existing note safely.")
    p_migrate.add_argument("file", type=Path)
    p_migrate.add_argument("--note-type", default="deep-notes")
    p_migrate.add_argument("--dry-run", action="store_true")

    p_validate = sub.add_parser("validate", help="Validate Properties and master-specific product contract.")
    p_validate.add_argument("file", type=Path)
    p_validate.add_argument("--master", choices=("M1", "M2", "M3", "M4", "M5", "M6", "M7"))
    p_validate.add_argument("--variant")

    p_explain = sub.add_parser("explain", help="Build an ExplanationBlueprint, compose prose with Properties, or review clarity (EIS-01..07).")
    p_explain.add_argument("--topic", required=True)
    p_explain.add_argument("--master", default="M1", choices=("M1", "M2", "M3", "M4", "M5", "M6", "M7"))
    p_explain.add_argument("--audience", default="intermediate", choices=("beginner", "intermediate", "advanced", "cross_domain_expert"))
    p_explain.add_argument("--source-mode", default="adaptive", choices=("adaptive", "source_first", "strict"))
    p_explain.add_argument("--preserve-source-order", action="store_true")
    p_explain.add_argument("--compose", action="store_true", help="Emit composed Markdown with Obsidian Properties.")
    p_explain.add_argument("--review", type=Path, help="Review an existing Markdown note for EIS & CF-01..CF-12 friction.")

    p_notes = sub.add_parser("notes", help="Universal /scribe-notes interactive session, collection planning, generation, and validation.")
    notes_sub = p_notes.add_subparsers(dest="notes_action", required=True)

    pn_comp = notes_sub.add_parser("compose", help="Plan or publish a comprehensive collection with 5–10 chapters and a MOC.")
    pn_comp.add_argument("--spec", type=Path, required=True, help="JSON topic, concepts, optional 5–10 chapters, classification, notation, and obligations.")
    pn_comp.add_argument("--vault", type=Path)
    pn_comp.add_argument("--drafts", type=Path, help="JSON mapping chapter IDs to authored Markdown bodies.")
    pn_comp.add_argument("--evidence", type=Path, help="JSON evidence records keyed by obligation ID.")
    pn_comp.add_argument("--reviews", type=Path, help="JSON review names mapped to review evidence.")
    pn_comp.add_argument("--expected-hashes", type=Path, help="JSON expected hashes for reviewed chapter replacements.")
    pn_comp.add_argument("--publish", action="store_true")
    pn_comp.add_argument("--prepare", action="store_true", help="Render assets and insert planned tables/questions; output chapter bodies to review.")
    pn_comp.add_argument("--repair", action="append", default=[], help="Failed obligation ID for a dependency-aware repair plan; repeat as needed.")
    pn_comp.add_argument("--repair-visuals", action="store_true", help="Repair only missing, corrupted, or dependency-impacted LAVIA visual assets.")
    pn_comp.add_argument("--context", action="append", default=[], help="Compile selective authoring context for a concept ID; repeat as needed.")
    pn_comp.add_argument("--validate", action="store_true", help="Validate a previously published composition without writing.")

    pn_start = notes_sub.add_parser("start", help="Start an interactive /scribe-notes session with inferred recommendations & questions.")
    pn_start.add_argument("request", nargs="?", default="/scribe-notes", help="User request or topic.")
    pn_start.add_argument("--vault", type=Path, help="Optional vault root to persist session state.")
    pn_start.add_argument("--has-source", action="store_true")
    pn_start.add_argument("--source-section", action="append", default=[])
    pn_start.add_argument("--json", action="store_true", dest="as_json")

    pn_resp = notes_sub.add_parser("respond", help="Respond to an active /scribe-notes configuration or plan-approval session.")
    pn_resp.add_argument("--vault", type=Path, required=True)
    pn_resp.add_argument("--session-id", required=True)
    pn_resp.add_argument("--reply", required=True)
    pn_resp.add_argument("--json", action="store_true", dest="as_json")

    pn_gen = notes_sub.add_parser("generate", help="Generate and validate notes for an approved /scribe-notes session.")
    pn_gen.add_argument("--vault", type=Path, required=True)
    pn_gen.add_argument("--session-id", required=True)
    pn_gen.add_argument("--checkpoints", action="store_true", help="Use dependency-aware checkpointed batch generation (F06).")
    pn_gen.add_argument("--synthesis", action="store_true", help="Generate M7 cross-note synthesis notes when warranted (F10).")
    pn_gen.add_argument("--assessment", action="store_true", help="Generate M6 competency-aligned collection assessment (F13).")
    pn_gen.add_argument("--validate", action="store_true", help="Run collection-wide quality validation after generation.")
    pn_gen.add_argument("--legacy-layout", action="store_true", help="Retain nested concept files for an existing legacy collection.")

    pn_val = notes_sub.add_parser("validate", help="Run collection-wide validation for a generated /scribe-notes session.")
    pn_val.add_argument("--vault", type=Path, required=True)
    pn_val.add_argument("--session-id", required=True)

    pn_ref = notes_sub.add_parser("refine", help="Process explicit post-generation reader feedback on an existing note (F15).")
    pn_ref.add_argument("--vault", type=Path, required=True)
    pn_ref.add_argument("--feedback", required=True)
    pn_ref.add_argument("--note", type=Path, help="Optional explicit note path.")
    pn_ref.add_argument("--session-id", help="Optional collection session ID for downstream impact analysis (F14).")
    pn_ref.add_argument("--apply", action="store_true", help="Apply approved localized improvement safely.")
    pn_ref.add_argument("--source-policy", choices=("strict", "source_first", "adaptive"), default="adaptive")

    p_opt = sub.add_parser("optimize", help="Run selective prompt compilation or 12-workload token-efficiency benchmarks.")
    p_opt.add_argument("--benchmark", action="store_true", help="Run 12-workload baseline vs. optimized token benchmark.")
    p_opt.add_argument("--compile", dest="compile_request", help="Compile minimal verified prompt bundle for a request.")
    p_opt.add_argument("--has-source", action="store_true")

    sub.add_parser("evaluate", help="Run the golden evaluation harness across all masters and lifecycle tasks.")
    p_audit = sub.add_parser("audit", help="Run consolidated repository link/CLI/syntax audit and instruction authority lint.")
    p_audit.add_argument("--inventory", action="store_true", help="Include per-file purpose, dependencies, size, estimated context cost and preservation decisions.")
    sub.add_parser("validate-registry", help="Validate references/routing/master-registry.yaml.")

    args = parser.parse_args(args_list)
    orch = OrchestrationEngine(REPO_ROOT)
    vault = VaultEngine()
    quality = QualityEngine(REPO_ROOT)

    if args.command == "route":
        norm = orch.normalize(args.request, source_policy=args.source_policy, has_source=args.has_source)
        constraints = orch.resolve_constraints(norm)
        clarification = orch.check_clarification(norm)
        payload = {
            "normalized": {k: v for k, v in norm.items() if k != "routed"},
            "routed": norm["routed"],
            "constraints": constraints,
            "clarification": clarification,
        }
        if args.trace:
            payload["execution_trace"] = orch.trace(routed=norm["routed"])
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    if args.command == "properties":
        props = vault.build_properties(
            topic=args.topic,
            note_type=args.note_type,
            domain=args.domain,
            master_topic=args.master_topic,
            subdomain=args.subdomain,
        )
        if args.format == "json":
            print(json.dumps(props, indent=2, ensure_ascii=False))
        else:
            print(dump_frontmatter(props))
        return 0

    if args.command == "update":
        text = args.file.read_text(encoding="utf-8-sig")
        sec_updates = {}
        for item in args.section:
            if "=" not in item:
                parser.error("--section requires 'Heading=Body'")
            h, b = item.split("=", 1)
            sec_updates[h.strip()] = b.strip()
        res = vault.update_note(
            text,
            section_updates=sec_updates or None,
            add_tags=args.add_tag or None,
            update_date=date.today(),
        )
        if not args.dry_run and res["changed"]:
            vault.write_note(args.file, res["content"])
        print(json.dumps({
            "file": str(args.file),
            "changed": res["changed"],
            "dry_run": args.dry_run,
            "modified_sections": res["modified_sections"],
            "preserved_custom_properties": res["preserved_custom_properties"],
        }, indent=2, ensure_ascii=False))
        return 0

    if args.command == "migrate":
        text = args.file.read_text(encoding="utf-8-sig")
        migrated = vault.ensure_properties(text, note_type=args.note_type, created=date.today())
        changed = migrated != text
        if not args.dry_run and changed:
            vault.write_note(args.file, migrated)
        print(json.dumps({"file": str(args.file), "changed": changed, "dry_run": args.dry_run}, indent=2))
        return 0

    if args.command == "validate":
        text = args.file.read_text(encoding="utf-8-sig")
        prop_errs = quality.validate_properties(text)
        master_errs = quality.validate_master(text, args.master, variant=args.variant) if args.master else []
        all_errs = prop_errs + master_errs
        print(json.dumps({"valid": not all_errs, "properties_errors": prop_errs, "master_errors": master_errs}, indent=2))
        return 0 if not all_errs else 1

    if args.command == "explain":
        ped = PedagogyEngine()
        bp = ped.build_explanation_blueprint(
            args.topic,
            master=args.master,
            audience=args.audience,
            source_mode=args.source_mode,
            preserve_source_order=args.preserve_source_order,
        )
        if args.review:
            text = args.review.read_text(encoding="utf-8-sig")
            report = quality.review_explanatory_clarity(text, bp, learner_profile=args.audience, source_mode=args.source_mode)
            print(json.dumps(report, indent=2, ensure_ascii=False))
            return 0 if report["passed"] else 1
        if args.compose:
            print(ped.compose_explanation(bp), end="")
            return 0
        print(json.dumps(bp.to_dict(), indent=2, ensure_ascii=False))
        return 0

    if args.command == "notes":
        if args.notes_action == "compose":
            try:
                ped = PedagogyEngine()
                spec = json.loads(args.spec.read_text(encoding="utf-8-sig"))
                composition = ped.plan_composition(spec)
                if sum(bool(x) for x in (args.prepare, args.publish, args.validate, args.repair, args.repair_visuals, args.context)) > 1:
                    raise ValueError("Choose one of --prepare, --publish, --validate, --context, --repair or --repair-visuals")
                if args.context:
                    from scriptorium.engines.composition import compile_context
                    print(json.dumps(compile_context(composition, args.context), indent=2, ensure_ascii=False))
                    return 0
                if args.repair:
                    from scriptorium.engines.composition.contracts import repair_plan
                    print(json.dumps(repair_plan(composition, args.repair), indent=2, ensure_ascii=False))
                    return 0
                if args.repair_visuals:
                    vault_dir = _resolve_compose_vault(args.vault)
                    if not vault_dir:
                        raise ValueError("Visual repair requires --vault")
                    from scriptorium.engines.composition import contained, lavia
                    from scriptorium.models import parse_note, slugify
                    slug = slugify(composition.get("collection_slug") or composition["topic"])
                    manifest_path = contained(vault_dir, f"assets/scriptorium/{slug}/manifest.json")
                    if manifest_path.is_file():
                        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
                    else:
                        state_path = contained(vault_dir, f".scriptorium/collections/col-{slugify(composition['topic'])}.json")
                        if not state_path.is_file():
                            raise ValueError(f"No LAVIA manifest or collection state found for '{composition['topic']}'")
                        state = json.loads(state_path.read_text(encoding="utf-8-sig"))
                        manifest = state.get("manifest") or lavia.build_asset_manifest(
                            composition, state.get("renderers", {}), collection_slug=composition.get("collection_slug")
                        )
                    if args.drafts:
                        bodies = json.loads(args.drafts.read_text(encoding="utf-8-sig"))
                    else:
                        bodies = {
                            c["id"]: parse_note(contained(vault_dir, c["path"]).read_text(encoding="utf-8-sig")).body.strip() + "\n"
                            for c in composition["chapters"]
                            if contained(vault_dir, c["path"]).is_file()
                        }
                    repaired = lavia.repair_visual_assets(vault_dir, composition, bodies, manifest, execute=True)
                    if composition.get("organize_by_collection") or composition.get("collection_slug") or manifest_path.is_file():
                        lavia.save_asset_manifest(vault_dir, repaired["manifest"])
                    print(json.dumps({"repaired_ids": repaired["repaired_ids"], "manifest": repaired["manifest"]}, indent=2, ensure_ascii=False))
                    return 0
                if args.prepare:
                    vault_dir = _resolve_compose_vault(args.vault)
                    if not vault_dir or not args.drafts:
                        raise ValueError("Preparation requires --vault and --drafts")
                    from scriptorium.engines._composition import prepare_composition
                    from scriptorium.engines.composition import lavia
                    bodies, renderers = prepare_composition(vault_dir, composition, json.loads(args.drafts.read_text(encoding="utf-8-sig")))
                    manifest = lavia.build_asset_manifest(composition, renderers, collection_slug=composition.get("collection_slug"))
                    print(json.dumps({"drafts": bodies, "renderers": renderers, "manifest": manifest, "obligations": composition["obligations"]}, indent=2, ensure_ascii=False))
                    return 0 if all(r["status"] == "verified" for r in renderers.values()) else 1
                if args.validate and not args.publish:
                    vault_dir = _resolve_compose_vault(args.vault)
                    if not vault_dir:
                        raise ValueError("Validation requires --vault")
                    from scriptorium.engines._composition import validate_published_composition
                    result = validate_published_composition(vault_dir, composition)
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                    return 0 if result["valid"] else 1
                if not args.publish:
                    print(json.dumps(composition, indent=2, ensure_ascii=False))
                    return 0
                vault_dir = _resolve_compose_vault(args.vault)
                if not all((vault_dir, args.drafts, args.evidence, args.reviews)):
                    raise ValueError("Publication requires --vault, --drafts, --evidence, and --reviews")
                def read_json(path):
                    return json.loads(path.read_text(encoding="utf-8-sig"))
                from scriptorium.engines._composition import to_collection_plan
                plan = to_collection_plan(composition)
                kcp = orch.build_kcp(vault_dir, plan, _composition_preferences(spec), include_synthesis=False)
                result = vault.publish_composition(vault_dir, kcp.composition, read_json(args.drafts),
                    evidence=read_json(args.evidence), reviews=read_json(args.reviews),
                    expected_hashes=read_json(args.expected_hashes) if args.expected_hashes else None)
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return 0 if result["complete"] else 1
            except (ValueError, OSError, KeyError) as exc:
                print(json.dumps({"complete": False, "error": str(exc)}, ensure_ascii=False))
                return 1
        if args.notes_action == "start":
            existing_topics: list[str] = []
            if args.vault and args.vault.is_dir():
                existing_topics = [p.stem for p in args.vault.rglob("*.md") if ".scriptorium" not in p.parts]
            state = orch.start_notes_session(
                args.request,
                has_source=args.has_source,
                source_sections=args.source_section or None,
                existing_vault_notes=existing_topics or None,
            )
            saved_path = str(orch.save_session_state(args.vault, state)) if args.vault else None
            prompt_text = orch.format_configuration_prompt(state)
            if args.as_json:
                print(json.dumps({
                    "session_id": state.request_id,
                    "stage": state.stage,
                    "saved_path": saved_path,
                    "prompt": prompt_text,
                    "state": state.to_dict(),
                }, indent=2, ensure_ascii=False))
            else:
                print(prompt_text)
                if saved_path:
                    print(f"\n[session_id={state.request_id}]")
            return 0

        if args.notes_action == "respond":
            state = orch.load_session_state(args.vault, args.session_id)
            res = orch.respond_to_session(state, args.reply)
            orch.save_session_state(args.vault, res["state"])
            if args.as_json:
                print(json.dumps({
                    "session_id": res["state"].request_id,
                    "stage": res["stage"],
                    "ready_to_generate": res["ready_to_generate"],
                    "message": res["message"],
                }, indent=2, ensure_ascii=False))
            else:
                print(res["message"])
            return 0

        if args.notes_action == "generate":
            state = orch.load_session_state(args.vault, args.session_id)
            if state.stage != "COLLECTION_PLAN_READY" or not state.collection_plan or not state.resolved_preferences:
                print(json.dumps({
                    "error": f"Session '{args.session_id}' is in stage '{state.stage}'; approve configuration/plan before generating.",
                }, indent=2))
                return 1
            if state.resolved_preferences.master == "M1" and state.collection_plan.organization == "hierarchical_collection" and not args.legacy_layout:
                print(json.dumps({"complete": False, "status": "requires_composition_spec",
                    "message": "Full-topic notes use 5–10 authored chapters and a MOC. Use notes compose --spec with concepts and optional chapter allocation; --legacy-layout retains an existing nested collection."}, indent=2))
                return 1
            if args.checkpoints:
                kcp = orch.build_kcp(
                    args.vault,
                    state.collection_plan,
                    state.resolved_preferences,
                    raw_request=state.original_intent.raw_request,
                    include_synthesis=args.synthesis,
                    include_assessment=args.assessment,
                )
                gen = vault.generate_with_checkpoints(args.vault, kcp, state.resolved_preferences)
                if args.synthesis and kcp.synthesis_notes:
                    for syn in kcp.synthesis_notes:
                        vault.write_note(args.vault / syn["proposed_path"], syn["content"])
                if args.assessment and kcp.assessment_plan:
                    vault.write_note(args.vault / kcp.assessment_plan["proposed_path"], kcp.assessment_plan["content"])
            else:
                gen = vault.generate_collection(args.vault, state.collection_plan, state.resolved_preferences)
            state.stage = "COMPLETED" if gen["complete"] else "PARTIAL_FAILURE"
            orch.save_session_state(args.vault, state)
            payload: dict = {"generation": gen}
            if args.validate:
                val = quality.validate_collection(args.vault, state.collection_plan, manifest=gen["manifest"])
                payload["validation"] = val
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            ok = gen["complete"] and (not args.validate or payload["validation"]["valid"])
            return 0 if ok else 1

        if args.notes_action == "validate":
            state = orch.load_session_state(args.vault, args.session_id)
            if not state.collection_plan:
                print(json.dumps({"valid": False, "error": "No collection plan recorded in session."}, indent=2))
                return 1
            val = quality.validate_collection(args.vault, state.collection_plan)
            print(json.dumps(val, indent=2, ensure_ascii=False))
            return 0 if val["valid"] else 1

        if args.notes_action == "refine":
            plan = orch.load_session_state(args.vault, args.session_id).collection_plan if args.session_id else None
            res = quality.process_feedback(
                args.vault,
                plan,
                args.feedback,
                target_note_path=args.note,
                apply_approved=args.apply,
                source_policy=args.source_policy,
            )
            print(json.dumps(res, indent=2, ensure_ascii=False))
            return 0 if res.get("status") in {"proposal_ready", "applied"} else 1

    if args.command == "optimize":
        ctrl = orch.create_token_controller()
        if args.compile_request:
            res = ctrl.prepare_execution_context(args.compile_request, has_source=args.has_source)
            print(json.dumps({
                "master": res["bundle"]["master"],
                "variant": res["bundle"]["variant"],
                "loaded_files": res["bundle"]["loaded_files"],
                "active_modules": res["bundle"]["active_modules"],
                "tokens": res["compiled"]["tokens"],
                "verified": res["compiled"]["verified"],
                "verification_errors": res["compiled"]["verification_errors"],
            }, indent=2, ensure_ascii=False))
            return 0 if res["compiled"]["verified"] else 1
        report = ctrl.run_benchmarks()
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["all_compilations_verified"] else 1

    if args.command == "evaluate":
        report = quality.run_golden_evaluations()
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["all_passed"] else 1

    if args.command == "audit":
        repo_audit = quality.audit_repo(include_inventory=args.inventory)
        auth_audit = quality.lint_authority()
        reg_audit = orch.validate_registry()
        ok = (not repo_audit["errors"]) and auth_audit["valid"] and reg_audit["valid"]
        print(json.dumps({
            "valid": ok,
            "repository_audit": repo_audit,
            "authority_audit": auth_audit,
            "registry_audit": reg_audit,
        }, indent=2, ensure_ascii=False))
        return 0 if ok else 1

    if args.command == "validate-registry":
        res = orch.validate_registry()
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0 if res["valid"] else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
