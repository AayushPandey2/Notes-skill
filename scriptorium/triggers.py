"""Executable Canonical Architecture & Explicit Trigger Registry (T01-T16, A0-A11).

Programmatic SVG generation triggers are retired. T06-T09 implement the
Web-Image-First visual pipeline: discovery -> download -> inspection -> grounded prose.
"""
from __future__ import annotations

import re
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


VIDEO_TRIGGERS: dict[str, dict[str, Any]] = {
    "VIDEO-01": {
        "name": "Video Access & Capability Probe",
        "architectures": ["A0", "A4"],
        "activation_condition": "Video URL, local media, transcript, or frame candidates supplied via /scribe-ytnotes or /scribe-ytlecture.",
        "semantic_intent": "Discover actual host media/transcription tool availability and classify explicit access_state.",
        "verification": "discover_video_capabilities + classify_access_state",
    },
    "VIDEO-02": {
        "name": "Meaning-Based Transcript Segmentation",
        "architectures": ["A1", "A4"],
        "activation_condition": "Timestamped transcript or subtitles available for video notes.",
        "semantic_intent": "Preserve equations/variables/Hinglish/uncertainty while segmenting on conceptual/demonstration shifts.",
        "verification": "segment_transcript bounds & timestamp alignment check",
    },
    "VIDEO-03": {
        "name": "Educational Frame Screening",
        "architectures": ["A6", "A7"],
        "activation_condition": "Candidate video frames provided or extracted from accessible video media.",
        "semantic_intent": "Reject blank/blur/duplicate shots while preserving intermediate derivation step frames and SHA-256 receipts.",
        "verification": "screen_frame_candidates pixel/delta/duration verification",
    },
    "VIDEO-04": {
        "name": "Source-Faithful Video Note Composition",
        "architectures": ["A5", "A9"],
        "activation_condition": "Video payload assembled for /scribe-notes unified pipeline.",
        "semantic_intent": "Align transcript segments, screened frames, and formula folds; emit access report if metadata_only.",
        "verification": "compose_video_study_payload access-state enforcement",
    },
}


MATH_TRIGGERS: dict[str, dict[str, Any]] = {
    "MATH-01": {
        "name": "New Symbol",
        "architectures": ["A2", "A5"],
        "activation_condition": "A significant new mathematical symbol, subscript, or operator appears.",
        "semantic_intent": "Require explicit symbol definition, object type, and role before or at first use.",
        "verification": "detect_explanation_gaps + verify_math_deconstruction symbol inventory",
    },
    "MATH-02": {
        "name": "Compact Equation",
        "architectures": ["A2", "A5"],
        "activation_condition": "Compact vector, dot-product, or summation notation compresses elementwise arithmetic.",
        "semantic_intent": "Expand compact expressions into explicit elementary terms.",
        "verification": "M07 expanded_form obligation in deconstruct_equation",
    },
    "MATH-03": {
        "name": "Matrix or Tensor",
        "architectures": ["A2", "A9"],
        "activation_condition": "Matrix multiplication, transpose, or tensor shape expressions appear.",
        "semantic_intent": "Verify operand shapes, transpose orientation, and output dimensionality deterministically.",
        "verification": "check_dimension_compatibility inner-dimension match",
    },
    "MATH-04": {
        "name": "Derivation",
        "architectures": ["A2", "A5", "A9"],
        "activation_condition": "Multi-step algebraic or calculus derivation appears.",
        "semantic_intent": "Require stated purpose and justified intermediate transformation steps.",
        "verification": "MATH-04 intermediate derivation continuity & proof-step check",
    },
    "MATH-05": {
        "name": "Numerical Example",
        "architectures": ["A2", "A5", "A9"],
        "activation_condition": "Quantitative formula benefits from concrete declared substitution for target learner level.",
        "semantic_intent": "Provide declared synthetic inputs, intermediate arithmetic, and context interpretation.",
        "verification": "build_worked_solution & verify_worked_calculation",
    },
    "MATH-06": {
        "name": "Optimization Objective",
        "architectures": ["A2", "A5"],
        "activation_condition": "Loss, objective, penalty, or constrained min/max formulation is introduced.",
        "semantic_intent": "Explain what is minimized or maximized, why each term exists, and parameter scaling assumptions.",
        "verification": "Objective purpose + assumption pairing in verify_math_deconstruction",
    },
    "MATH-07": {
        "name": "Derivative or Gradient",
        "architectures": ["A2", "A5", "A9"],
        "activation_condition": "Derivatives, gradients, or partial differentiation govern the mechanism.",
        "semantic_intent": "Explain directional meaning, intermediate chain-rule steps, and local vs global scope.",
        "verification": "Skipped composite derivative detector in detect_explanation_gaps",
    },
    "MATH-08": {
        "name": "Probability",
        "architectures": ["A2", "A9"],
        "activation_condition": "Probability distributions, expectations, variances, or conditioning notation appear.",
        "semantic_intent": "Define random variables, conditioning sets, independence, and distributional assumptions.",
        "verification": "Assumption & random-variable definition check",
    },
    "MATH-09": {
        "name": "Notation Ambiguity",
        "architectures": ["A1", "A2"],
        "activation_condition": "Symbols collide across conventions (e.g., transpose shapes, norm scaling, regularizer strength).",
        "semantic_intent": "Disambiguate the active convention and explain how it maps to alternate notations.",
        "verification": "CollectionTerminologyRegistry / misconception note check",
    },
    "MATH-10": {
        "name": "Numerical Verification",
        "architectures": ["A9"],
        "activation_condition": "Worked arithmetic, identities, shapes, or step traces can be checked deterministically.",
        "semantic_intent": "Run safe AST arithmetic, polynomial, or shape compatibility verifiers before emission.",
        "verification": "verify_worked_calculation / check_dimension_compatibility / arithmetic",
    },
}

TEACH_TRIGGERS: dict[str, dict[str, Any]] = {
    "TEACH-01": {
        "name": "Missing Prerequisite",
        "architectures": ["A1", "A2"],
        "activation_condition": "Reader lacks an essential foundation term or operation.",
        "semantic_intent": "Insert a concise local Foundation Bridge immediately before dependent notation.",
        "verification": "TEACH-01 / P01 prerequisite bridge verification",
    },
    "TEACH-02": {
        "name": "High Abstraction",
        "architectures": ["A2", "A5"],
        "activation_condition": "Abstract formalisms appear without an intuitive concrete anchor.",
        "semantic_intent": "Introduce a simpler concrete mental model and disclose where analogies break.",
        "verification": "CF-08 / intuition-before-formalism check",
    },
    "TEACH-03": {
        "name": "Multi-Stage Mechanism",
        "architectures": ["A2", "A5"],
        "activation_condition": "Process has sequential stages or interacting components.",
        "semantic_intent": "Decompose inputs, intermediate states, operations, and outputs step by step.",
        "verification": "Mechanism stage continuity check",
    },
    "TEACH-04": {
        "name": "Concept Comparison",
        "architectures": ["A2", "A5", "A9"],
        "activation_condition": "Alternative methods, models, or parameters are contrasted.",
        "semantic_intent": "Explain causal trade-offs and selection conditions before summarizing in a table.",
        "verification": "Causal comparison check before summary tables",
    },
    "TEACH-05": {
        "name": "Complex Visual",
        "architectures": ["A6", "A5"],
        "activation_condition": "External figure or diagram contains dense components, curves, or axes.",
        "semantic_intent": "Write a structured reading guide (what it represents, where to start, labels, interaction, takeaway).",
        "verification": "bvia.validate_image_grounded_explanation",
    },
    "TEACH-06": {
        "name": "Short Explanation",
        "architectures": ["A3", "A9"],
        "activation_condition": "Chapter or section covers multiple concepts superficially.",
        "semantic_intent": "Diagnose missing educational obligations rather than inflating prose via repetition.",
        "verification": "evaluate_chapter_depth_contract + anti-overcompression check",
    },
    "TEACH-07": {
        "name": "Abrupt Transition",
        "architectures": ["A5", "A9"],
        "activation_condition": "New topic, heading, or equation starts without connecting why it follows.",
        "semantic_intent": "Create an explanatory bridge motivating the next concept or limitation.",
        "verification": "CF-04 / MATH-DECON-01 abrupt drop detector",
    },
    "TEACH-08": {
        "name": "Common Misconception",
        "architectures": ["A2", "A5"],
        "activation_condition": "Beginner-prone confusion or invalid generalization arises around an operation.",
        "semantic_intent": "Place targeted misconception clarification beside the step where confusion occurs.",
        "verification": "EIS-04 / misconception placement audit",
    },
    "TEACH-09": {
        "name": "Practical Application",
        "architectures": ["A5", "A2"],
        "activation_condition": "Concept applies directly to real problem-solving or executable modeling tasks.",
        "semantic_intent": "Connect theory to a realistic applied scenario with When-to-Use / When-Not-to-Use boundaries.",
        "verification": "Application & boundary completeness check",
    },
    "TEACH-10": {
        "name": "Chapter Completion",
        "architectures": ["A3", "A9"],
        "activation_condition": "Chapter draft is evaluated before publication.",
        "semantic_intent": "Verify all 12 teaching quality dimensions and applicable 19-point depth obligations.",
        "verification": "evaluate_teaching_quality + evaluate_chapter_depth_contract",
    },
}


def detect_active_triggers(
    note_or_spec: str | dict[str, Any],
    *,
    learner_level: str = "beginner",
) -> dict[str, Any]:
    """Semantically detect which MATH-01..MATH-10 and TEACH-01..TEACH-10 triggers activate."""
    from scriptorium.engines.mathematics import detect_equation_features

    text = note_or_spec if isinstance(note_or_spec, str) else " ".join(
        str(v) for v in note_or_spec.values() if isinstance(v, (str, list, dict))
    )
    active_math: list[str] = []
    active_teach: list[str] = ["TEACH-10"]

    equations = re.findall(r"\$\$(.*?)\$\$", text, re.S) + re.findall(r"(?<!\$)\$(?!\$)([^$\n]+?)(?<!\$)\$(?!\$)", text)
    if equations:
        active_math.extend(["MATH-01", "MATH-05", "MATH-10"])
    for eq in equations:
        feat = detect_equation_features(eq, learner_level=learner_level)["features"]
        if feat["has_matrix_or_vector"] or feat["has_transpose"]:
            active_math.extend(["MATH-02", "MATH-03", "MATH-09"])
        if feat["has_summation"]:
            active_math.append("MATH-02")
        if feat["has_optimization"]:
            active_math.append("MATH-06")
        if feat["has_derivative"]:
            active_math.extend(["MATH-04", "MATH-07"])
        if feat["has_probability"]:
            active_math.append("MATH-08")

    low = text.lower()
    if isinstance(note_or_spec, dict) and note_or_spec.get("prerequisites"):
        active_teach.append("TEACH-01")
    if equations or len(text.split()) > 150:
        active_teach.extend(["TEACH-02", "TEACH-03"])
    if re.search(r"\b(?:vs\.?|versus|compare|comparison|alternative|ridge|lasso|trade-?off)\b", low) or "|" in text:
        active_teach.append("TEACH-04")
    if "![[" in text or (isinstance(note_or_spec, dict) and note_or_spec.get("visuals")):
        active_teach.append("TEACH-05")
    if len(text.split()) < 180:
        active_teach.append("TEACH-06")
    if re.search(r"(?:^|\n)#{1,6}\s+[^\n]+\n+\s*\$\$", text):
        active_teach.append("TEACH-07")
    if re.search(r"\b(?:mistake|trap|confusion|unlike|avoid|never|misconception)\b", low) or equations:
        active_teach.append("TEACH-08")
    if re.search(r"\b(?:use\s+when|avoid\s+when|application|practice|real-?world|workflow|when\s+not\s+to\s+use)\b", low):
        active_teach.append("TEACH-09")

    ordered_math = [k for k in MATH_TRIGGERS if k in set(active_math)]
    ordered_teach = [k for k in TEACH_TRIGGERS if k in set(active_teach)]
    return {"learner_level": learner_level, "math_triggers": ordered_math, "teach_triggers": ordered_teach}


def dispatch_trigger(
    trigger_id: str,
    payload: dict[str, Any] | None = None,
    *,
    root: Path = REPO_ROOT,
) -> dict[str, Any]:
    """Execute one explicit trigger contract (T01-T16, MATH-01..10, TEACH-01..10)."""
    tid = trigger_id.strip().upper()
    all_registries = {**TRIGGER_REGISTRY, **MATH_TRIGGERS, **TEACH_TRIGGERS, **VIDEO_TRIGGERS}
    if tid not in all_registries:
        raise ValueError(f"Unknown trigger ID: {trigger_id}")
    data = dict(payload or {})
    meta = all_registries[tid]

    if tid in VIDEO_TRIGGERS:
        from scriptorium.engines.composition import video as video_eng
        if tid == "VIDEO-01":
            result = {
                "capabilities": video_eng.discover_video_capabilities(),
                "access_state": video_eng.classify_access_state(
                    has_video_media=bool(data.get("has_video_media")),
                    has_frames=bool(data.get("frame_candidates")),
                    has_transcript=bool(data.get("transcript_entries")),
                    has_audio_track=bool(data.get("transcript_entries")),
                ),
            }
        elif tid == "VIDEO-02":
            result = {"segments": video_eng.segment_transcript(data.get("transcript_entries") or [], video_duration_seconds=data.get("video_duration_seconds"))}
        elif tid == "VIDEO-03":
            result = video_eng.screen_frame_candidates(
                data.get("frame_candidates") or [],
                vault=Path(data["vault"]) if data.get("vault") else None,
                video_duration_seconds=data.get("video_duration_seconds"),
            )
        else:
            result = video_eng.compose_video_study_payload(
                title=str(data["title"]),
                source_url=str(data.get("source_url") or ""),
                transcript_entries=data.get("transcript_entries"),
                frame_candidates=data.get("frame_candidates"),
                vault=Path(data["vault"]) if data.get("vault") else None,
                collection_slug=data.get("collection_slug"),
                video_duration_seconds=data.get("video_duration_seconds"),
                has_video_media=bool(data.get("has_video_media")),
            )
        return {"trigger": tid, "name": meta["name"], "architectures": meta["architectures"], "result": result}

    if tid in MATH_TRIGGERS:
        from scriptorium.engines import mathematics as math_eng
        level = str(data.get("learner_level", "beginner"))
        if tid == "MATH-03" and data.get("operands"):
            result = math_eng.check_dimension_compatibility(data["operands"], operation=str(data.get("operation", "matmul")))
        elif tid in {"MATH-05", "MATH-10"} and data.get("problem_spec"):
            result = math_eng.build_worked_solution(data["problem_spec"], learner_level=level)
        elif tid == "MATH-10" and data.get("steps"):
            result = math_eng.verify_worked_calculation(data["steps"], variables=data.get("variables"), expected_result=data.get("expected_result"))
        elif data.get("equation_spec"):
            result = math_eng.deconstruct_equation(data["equation_spec"], learner_level=level)
        elif data.get("note_text"):
            result = math_eng.verify_math_deconstruction(data["note_text"], equations=data.get("equations"), learner_level=level)
        elif data.get("equation"):
            result = math_eng.detect_equation_features(data["equation"], learner_level=level)
        else:
            result = {"trigger": tid, "contract": meta, "status": "ready_for_inputs"}
        return {"trigger": tid, "name": meta["name"], "architectures": meta["architectures"], "result": result}

    if tid in TEACH_TRIGGERS:
        from scriptorium.engines.quality import QualityEngine
        level = str(data.get("learner_level", "beginner"))
        note_text = str(data.get("note_text") or "")
        if tid == "TEACH-05" and data.get("visual"):
            from scriptorium.engines.composition.bvia import validate_image_grounded_explanation
            result = validate_image_grounded_explanation(note_text, data["visual"], inspection=data.get("inspection"))
        elif tid in {"TEACH-06", "TEACH-10"} and note_text:
            result = QualityEngine(root).evaluate_teaching(note_text, learner_level=level, concept_spec=data.get("concept_spec"), worked_examples=data.get("worked_examples"), visuals=data.get("visuals"))
        elif note_text:
            qe = QualityEngine(root)
            result = qe.review_explanatory_clarity(note_text, learner_profile=level)
        else:
            result = {"trigger": tid, "contract": meta, "detected": detect_active_triggers(data, learner_level=level)}
        return {"trigger": tid, "name": meta["name"], "architectures": meta["architectures"], "result": result}

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
