"""Executable Canonical Architecture & Explicit Trigger Registry (T01-T16, A0-A11).

Programmatic SVG generation triggers are retired. T06-T09 implement the
Web-Image-First visual pipeline: discovery -> download -> inspection -> grounded prose.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from scriptorium.models import REPO_ROOT

CANONICAL_ARCHITECTURES: dict[str, dict[str, str]] = {
    "A0": {"name": "Director", "owner": "scriptorium/engines/orchestration.py", "responsibility": "Orchestration, triggers, state, and execution coordination"},
    "A1": {"name": "Map", "owner": "scriptorium/engines/knowledge.py", "responsibility": "Knowledge mapping, concepts, prerequisites, terminology, and nested tags"},
    "A2": {"name": "Tutor", "owner": "scriptorium/engines/pedagogy.py", "responsibility": "Pedagogy, intuition, detailed explanations, and beginner-to-advanced progression"},
    "A3": {"name": "Planner", "owner": "scriptorium/engines/composition/planning.py", "responsibility": "Chapter structure, depth allocation, and educational completion requirements"},
    "A4": {"name": "Researcher", "owner": "scriptorium/engines/research.py", "responsibility": "Research, sources, citations, evidence, and external figure discovery"},
    "A5": {"name": "Writer", "owner": "scriptorium/engines/pedagogy.py", "responsibility": "Educational composition, examples, equations, and image-grounded explanations"},
    "A6": {"name": "Visuals", "owner": "scriptorium/engines/composition/bvia.py", "responsibility": "Visual opportunity discovery, representation planning, accessibility evaluation, and external-image selection"},
    "A7": {"name": "Assets", "owner": "scriptorium/engines/composition/lavia.py", "responsibility": "Web-image downloading, validation, local storage, provenance, and reuse"},
    "A8": {"name": "Quiz", "owner": "scriptorium/engines/composition/contracts.py", "responsibility": "Knowledge checks, hints, detailed answers, and assessments"},
    "A9": {"name": "Checker", "owner": "scriptorium/engines/quality.py", "responsibility": "Educational, technical, research, visual, and publication validation"},
    "A10": {"name": "Vault", "owner": "scriptorium/engines/vault.py", "responsibility": "Obsidian publishing, file paths, YAML, wikilinks, and manifests"},
    "A11": {"name": "Speed", "owner": "scriptorium/engines/_token_optimizer.py", "responsibility": "Caching, selective loading, incremental work, and execution optimization"},
}

TRIGGER_REGISTRY: dict[str, dict[str, Any]] = {
    "T01": {
        "name": "Note Generation",
        "architectures": ["A0"],
        "activation_condition": "Any user note, summary, cheat sheet, worked solution, guide, or study request.",
        "semantic_intent": "Normalize request intent, enforce constraints, and route to M1-M7.",
        "dependencies": [],
        "required_inputs": ["request"],
        "outputs": ["routed", "constraints"],
        "verification": "Valid master M1-M7 selection and constraint precedence resolution.",
        "failure_handling": "Return explicit ambiguity/clarification prompt without mutating vault files.",
    },
    "T02": {
        "name": "Knowledge Mapping",
        "architectures": ["A1"],
        "activation_condition": "Concept decomposition, prerequisite graph construction, or vault tag classification needed.",
        "semantic_intent": "Build prerequisite DAG, check vault overlap, and govern terminology/tags.",
        "dependencies": ["T01"],
        "required_inputs": ["topic"],
        "outputs": ["hierarchy", "tags"],
        "verification": "Acyclic prerequisite graph and canonical hierarchical tags.",
        "failure_handling": "Raise ValueError on cycles or unresolved hard dependencies.",
    },
    "T03": {
        "name": "Beginner Foundations",
        "architectures": ["A2"],
        "activation_condition": "Learner lacks prerequisites or targets beginner-to-advanced comprehension.",
        "semantic_intent": "Build ExplanationBlueprint bridging intuition and prerequisites before formal depth.",
        "dependencies": ["T01", "T02"],
        "required_inputs": ["topic"],
        "outputs": ["blueprint"],
        "verification": "Prerequisite bridge ordering and absence of cognitive friction CF-01..CF-12.",
        "failure_handling": "Flag missing prerequisite gaps explicitly in validation report.",
    },
    "T04": {
        "name": "Depth Planning",
        "architectures": ["A3"],
        "activation_condition": "Comprehensive study material or multi-chapter M1 collection requested.",
        "semantic_intent": "Allocate concepts into 5-10 balanced chapters with explicit educational obligations.",
        "dependencies": ["T01", "T02"],
        "required_inputs": ["concepts"],
        "outputs": ["chapters", "rationale", "obligations"],
        "verification": "5-10 chapters, strict topological prerequisite order, non-empty chapter ownership.",
        "failure_handling": "Reject under-scoped comprehensive requests instead of padding thin chapters.",
    },
    "T05": {
        "name": "Research",
        "architectures": ["A4"],
        "activation_condition": "External factual, mathematical, API, or empirical evidence is required under source policy.",
        "semantic_intent": "Plan per-concept research questions and generate targeted discovery queries.",
        "dependencies": ["T01"],
        "required_inputs": ["topic", "instructional_plan"],
        "outputs": ["research_plan"],
        "verification": "Respect R-S0 strict source-only lock and separate further learning from citations.",
        "failure_handling": "Mark unverified external claims as pending/blocked when retrieval is prohibited.",
    },
    "T06": {
        "name": "Visual Research",
        "architectures": ["A4", "A6"],
        "activation_condition": "Visual learning opportunity identified (architecture, process, scientific figure, geometry).",
        "semantic_intent": "Discover external web image candidates via API/host search and rank for beginner accessibility.",
        "dependencies": ["T03"],
        "required_inputs": ["concept_title", "objective"],
        "outputs": ["search_status", "candidates"],
        "verification": "Permissive license check, minimum readability resolution, and candidate diversity.",
        "failure_handling": "Record explicit unmet visual obligation on NO_IMAGE_EXISTS or SEARCH_UNAVAILABLE; never generate SVGs.",
    },
    "T07": {
        "name": "Image Acquisition",
        "architectures": ["A7"],
        "activation_condition": "Permitted candidate URL or explicit offline fallback image selected.",
        "semantic_intent": "Download image bytes over pinned public HTTPS, validate format, compute SHA-256, and store under assets/scriptorium/<slug>/.",
        "dependencies": ["T06"],
        "required_inputs": ["vault", "visual"],
        "outputs": ["path", "hash", "provenance", "embed"],
        "verification": "Bounded image decoder (PNG/JPEG/WebP/sanitized SVG) and SHA-256 receipt.",
        "failure_handling": "Reject unsafe URLs, private DNS, corrupted bytes, or unclear rights.",
    },
    "T08": {
        "name": "Image Inspection",
        "architectures": ["A6", "A7"],
        "activation_condition": "Local image asset acquired and ready for visual grounding before composition.",
        "semantic_intent": "Inspect actual image pixels/metadata (dimensions, contrast, readable labels) before writing prose.",
        "dependencies": ["T07"],
        "required_inputs": ["source"],
        "outputs": ["inspection"],
        "verification": "inspection_performed=True and readable_for_embedding check; no invented labels.",
        "failure_handling": "Flag illegible resolution or mark label OCR unavailable honestly.",
    },
    "T09": {
        "name": "Image-Grounded Composition",
        "architectures": ["A5", "A6"],
        "activation_condition": "Conceptual explanation and inspected visual metadata are available for chapter prose.",
        "semantic_intent": "Compose Explain -> Show -> Decode -> Connect visual walkthroughs grounded in verified image details.",
        "dependencies": ["T08"],
        "required_inputs": ["visual", "embed"],
        "outputs": ["walkthrough"],
        "verification": "validate_image_grounded_explanation passes Explain before Show and Decode/Connect after.",
        "failure_handling": "Fail chapter completeness if images are dumped without explanation or cite unverified labels.",
    },
    "T10": {
        "name": "Mathematical Reasoning",
        "architectures": ["A2", "A9"],
        "activation_condition": "Derivations, equations, identities, or numerical claims are present.",
        "semantic_intent": "Verify algebraic identities, proof assumptions, and bounded arithmetic expressions.",
        "dependencies": ["T03"],
        "required_inputs": ["proof"],
        "outputs": ["errors"],
        "verification": "Exact polynomial normalization and assumption-scope checks.",
        "failure_handling": "Report counterexamples or unstated assumptions; never certify unverified numerical samples as universal proof.",
    },
    "T11": {
        "name": "Worked Examples",
        "architectures": ["A5", "A9"],
        "activation_condition": "Procedural/quantitative concepts require verified step-by-step worked demonstrations.",
        "semantic_intent": "Validate multi-step numerical/state traces against explicit recurrence and invariant contracts.",
        "dependencies": ["T10"],
        "required_inputs": ["trace"],
        "outputs": ["valid", "errors"],
        "verification": "Every intermediate row satisfies formula/recurrence and monotonicity/shrinking bounds.",
        "failure_handling": "Reject inconsistent trace steps with row-level diagnostic messages.",
    },
    "T12": {
        "name": "Assessment",
        "architectures": ["A8"],
        "activation_condition": "Chapter or milestone assessment generation or validation requested.",
        "semantic_intent": "Render/check 4-5 diverse objective-aligned questions with separately folded hints and detailed answers.",
        "dependencies": ["T04"],
        "required_inputs": ["plan", "chapter", "body"],
        "outputs": ["errors"],
        "verification": "Full chapter objective coverage, >=3 task types, independently folded hint/answer callouts.",
        "failure_handling": "Fail chapter assessment check until missing objectives or leaks are repaired.",
    },
    "T13": {
        "name": "Quality Verification",
        "architectures": ["A9"],
        "activation_condition": "Draft preparation, repository audit, or pre-publication validation.",
        "semantic_intent": "Verify educational depth obligations, visual coverage, local embeds, clarity, and source provenance.",
        "dependencies": ["T09", "T12"],
        "required_inputs": ["vault", "plan"],
        "outputs": ["valid", "errors"],
        "verification": "Zero broken wikilinks, zero remote image leaks, all critical obligations verified.",
        "failure_handling": "Block complete publication status; surface honest readiness state ('partial'/'blocked'/'draft').",
    },
    "T14": {
        "name": "Publication",
        "architectures": ["A10"],
        "activation_condition": "Verification gates pass (or explicit draft policy selected).",
        "semantic_intent": "Atomically write MOC, chapters, and LAVIA manifest under configured vault root without unwanted category folders.",
        "dependencies": ["T13"],
        "required_inputs": ["vault", "plan", "drafts", "evidence", "reviews"],
        "outputs": ["complete", "readiness_state", "written_paths"],
        "verification": "Content-hash checkpoints, protected path containment, post-write validation.",
        "failure_handling": "Abort overwrites without matching expected digests; report exact readiness state.",
    },
    "T15": {
        "name": "Targeted Repair",
        "architectures": ["A0", "A9"],
        "activation_condition": "Verification fails for specific obligations or visual assets.",
        "semantic_intent": "Compute minimal dependency closure across prerequisites/chapters/visuals and repair only affected spans.",
        "dependencies": ["T13"],
        "required_inputs": ["plan", "failed_obligations"],
        "outputs": ["obligations", "chapters", "assets"],
        "verification": "Unchanged chapters preserved byte-for-byte; repaired span passes validation.",
        "failure_handling": "Propagate downstream blocked status cleanly until critical root obligations pass.",
    },
    "T16": {
        "name": "Optimization",
        "architectures": ["A11"],
        "activation_condition": "Selective prompt context compilation, cache reuse, or single-pass source segmentation.",
        "semantic_intent": "Load only active master, variant, knowledge-type subtemplates, and concept slice to minimize context tokens.",
        "dependencies": ["T01"],
        "required_inputs": ["request"],
        "outputs": ["bundle", "compiled"],
        "verification": "Zero validation checks skipped across L1-L10 cache and selective loading.",
        "failure_handling": "Bypass stale cache keys when spec/validator hashes change.",
    },
}


def dispatch_trigger(
    trigger_id: str,
    payload: dict[str, Any] | None = None,
    *,
    root: Path = REPO_ROOT,
) -> dict[str, Any]:
    """Execute one explicit trigger contract (T01-T16) against real backing Scriptorium engines."""
    tid = trigger_id.strip().upper()
    if tid not in TRIGGER_REGISTRY:
        raise ValueError(f"Unknown trigger ID: {trigger_id}")
    data = dict(payload or {})
    meta = TRIGGER_REGISTRY[tid]

    if tid == "T01":
        from scriptorium.engines.orchestration import OrchestrationEngine
        result = OrchestrationEngine(root).route(
            data["request"],
            source_policy=data.get("source_policy"),
            has_source=bool(data.get("has_source")),
        )
    elif tid == "T02":
        from scriptorium.engines.vault import VaultEngine
        ve = VaultEngine()
        hierarchy = ve.classify_hierarchy(
            data["topic"],
            content=data.get("content", ""),
            domain=data.get("domain"),
            master_topic=data.get("master_topic"),
            subdomain=data.get("subdomain"),
        )
        tags = ve.generate_tags(
            topic=data["topic"],
            domain=hierarchy["domain"],
            master_topic=hierarchy["master_topic"],
            subdomain=hierarchy.get("subdomain", ""),
        )
        result = {"hierarchy": hierarchy, "tags": tags}
    elif tid == "T03":
        from scriptorium.engines.pedagogy import PedagogyEngine
        bp = PedagogyEngine().build_explanation_blueprint(
            data["topic"],
            master=data.get("master", "M1"),
            audience=data.get("audience", "beginner"),
            context=data.get("context"),
        )
        result = {"blueprint": bp.to_dict()}
    elif tid == "T04":
        from scriptorium.engines.composition.planning import plan_chapters
        result = plan_chapters(
            data["concepts"],
            known_prerequisites=data.get("known_prerequisites", ()),
        )
    elif tid == "T05":
        from scriptorium.engines.research import ResearchEngine
        result = ResearchEngine().plan(data["topic"], data["instructional_plan"])
    elif tid == "T06":
        from scriptorium.engines.composition import lavia
        queries = data.get("queries") or lavia.generate_visual_search_queries(
            data["concept_title"], data.get("objective", "")
        )
        result = lavia.search_web_images(queries, http_get=data.get("http_get"))
    elif tid == "T07":
        from scriptorium.engines.composition.media import media_artifact
        result = media_artifact(
            Path(data["vault"]),
            data["visual"],
            data.get("digest", "trigger-t07"),
            execute=bool(data.get("execute", True)),
        )
    elif tid == "T08":
        from scriptorium.engines.composition.media import inspect_image_content
        result = {"inspection": inspect_image_content(data["source"], mime=data.get("mime"))}
    elif tid == "T09":
        from scriptorium.engines.composition.bvia import compose_visual_walkthrough, validate_image_grounded_explanation
        walkthrough = compose_visual_walkthrough(
            data["visual"],
            embed=data["embed"],
            terminology_registry=data.get("terminology_registry"),
            inspection=data.get("inspection"),
        )
        validation = validate_image_grounded_explanation(
            walkthrough,
            data["visual"],
            inspection=data.get("inspection"),
            terminology_registry=data.get("terminology_registry"),
        )
        result = {"walkthrough": walkthrough, "validation": validation}
    elif tid == "T10":
        from scriptorium.engines.composition.checks import check_proof
        errors = check_proof(data["proof"])
        result = {"valid": not errors, "errors": errors}
    elif tid == "T11":
        from scriptorium.engines._explanation import verify_numerical_trace
        result = verify_numerical_trace(
            data["trace"],
            value_checks=data.get("value_checks"),
            recurrence_checks=data.get("recurrence_checks"),
            monotonic_field=data.get("monotonic_field"),
            shrinking_bounds=data.get("shrinking_bounds"),
            constants=data.get("constants"),
        )
    elif tid == "T12":
        from scriptorium.engines.composition.contracts import check_assessment
        errors = check_assessment(data["plan"], data["chapter"], data["body"])
        result = {"valid": not errors, "errors": errors}
    elif tid == "T13":
        from scriptorium.engines.quality import QualityEngine
        result = QualityEngine(root).validate_composition(Path(data["vault"]), data["plan"])
    elif tid == "T14":
        from scriptorium.engines.vault import VaultEngine
        result = VaultEngine().publish_composition(
            Path(data["vault"]),
            data["plan"],
            data["drafts"],
            evidence=data["evidence"],
            reviews=data["reviews"],
            allow_draft=bool(data.get("allow_draft", False)),
        )
    elif tid == "T15":
        from scriptorium.engines.composition.contracts import repair_plan
        result = repair_plan(data["plan"], data["failed_obligations"])
    elif tid == "T16":
        from scriptorium.engines._token_optimizer import TokenEfficiencyController
        ctrl = TokenEfficiencyController(root)
        result = ctrl.prepare_execution_context(
            data["request"],
            has_source=bool(data.get("has_source", False)),
        )
    else:
        raise ValueError(f"Trigger '{tid}' has no dispatcher")

    return {"trigger": tid, "name": meta["name"], "architectures": meta["architectures"], "result": result}
