"""Universal /scribe-notes Interactive Configuration, Scope Detection, and Hierarchical Collection Planner.

Owned by Engine E1 (Orchestration) and Engine E4 (Pedagogy).
Reuses existing M1-M7 routing, ExplanationBlueprint (EIS-01..07), KnowledgeEngine, and VaultEngine.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
import re
from typing import Any

from scriptorium.engines.orchestration import (
    OrchestrationEngine,
    URL_RE,
    normalize_request,
    route_request,
)
from scriptorium.models import REPO_ROOT, slugify

RETIRED_NOTE_COMMANDS: dict[str, str] = {
    "scribe-deepnotes": "deep learning notes (M1)",
    "scribe-distill": "quick-reference cheat sheet (M3)",
    "scribe-atomic-notes": "atomic concept card (M3/atomic_card)",
    "scribe-compare": "comparison guide (M7/comparison_guide)",
    "scribe-dsa": "algorithm implementation guide (M5)",
    "scribe-practice": "active-recall practice set (M6)",
    "scribe-ingest": "source-faithful study notes (M2/lecture_order)",
    "scribe-expand": "incremental note expansion under /scribe-notes",
}

PRESERVED_NON_NOTE_COMMANDS: frozenset[str] = frozenset({
    "scribe-doubt",
    "scribe-quiz",
    "scribe-setfolder",
})

ACTIVE_PUBLIC_COMMANDS: frozenset[str] = frozenset({"scribe-notes"}) | PRESERVED_NON_NOTE_COMMANDS

MASTER_READABLE_NAMES: dict[str, str] = {
    "M1": "Deep Learning Notes",
    "M2": "Structured Study Notes",
    "M3": "Quick Reference / Cheat Sheet",
    "M4": "Worked Problems / Solutions",
    "M5": "Implementation / Technical Guide",
    "M6": "Practice / Assessment",
    "M7": "Synthesis / Revision",
}


# ---------------------------------------------------------------------------
# Part 27 — Shared Dataclass Contracts
# ---------------------------------------------------------------------------

@dataclass
class NoteRequestIntent:
    raw_request: str
    topic: str | None
    requested_artifact: str | None = None
    explicit_constraints: dict[str, Any] = field(default_factory=dict)
    source_bindings: list[dict[str, Any]] = field(default_factory=list)
    inferred_scope: str | None = None
    update_existing: bool = False
    migration_hint: str | None = None


@dataclass
class NoteConfigurationRecommendation:
    recommended_master: str
    recommended_variant: str | None
    recommended_depth: str
    recommended_organization: str
    recommended_learning_objective: str
    confidence: str = "high"
    rationale: list[str] = field(default_factory=list)
    alternative_master: str | None = None


@dataclass
class ResolvedNotePreferences:
    learning_objective: str
    master: str
    variant: str | None
    depth: str
    prior_knowledge: dict[str, Any]
    organization: str
    emphasis: list[str]
    source_policy: str
    preserve_source_order: bool = False
    language: str | None = None
    scope_boundary: str = "focused_curriculum"
    custom_constraints: dict[str, Any] = field(default_factory=dict)


@dataclass
class TopicNode:
    concept_id: str
    title: str
    parent_id: str | None
    child_ids: list[str] = field(default_factory=list)
    prerequisite_ids: list[str] = field(default_factory=list)
    related_ids: list[str] = field(default_factory=list)
    proposed_path: str = ""
    note_role: str = "child"  # root_index | group_index | child | single
    template_plan: dict[str, Any] = field(default_factory=dict)
    source_bindings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class NoteCollectionPlan:
    collection_id: str
    title: str
    root_topic_id: str
    organization: str  # single_note | hierarchical_collection
    nodes: list[TopicNode] = field(default_factory=list)
    planned_paths: list[str] = field(default_factory=list)
    learning_order: list[str] = field(default_factory=list)
    generation_order: list[str] = field(default_factory=list)
    scope_summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class NoteInteractionState:
    request_id: str
    stage: str
    original_intent: NoteRequestIntent
    recommendation: NoteConfigurationRecommendation
    questions_asked: list[dict[str, Any]] = field(default_factory=list)
    resolved_preferences: ResolvedNotePreferences | None = None
    collection_plan: NoteCollectionPlan | None = None
    question_trace: list[dict[str, Any]] = field(default_factory=list)
    persistence_mode: str = "in_memory_or_vault_session"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Part 12 — Intelligent Topic Scope Detection (S0 - S5)
# ---------------------------------------------------------------------------

_S5_PATTERNS = re.compile(
    r"\b(?:complete\s+artificial\s+intelligence|full\s+computer\s+science\s+curriculum|"
    r"comprehensive\s+mathematics\s+knowledge\s+base|entire\s+computer\s+science|"
    r"complete\s+ai\s+curriculum)\b",
    re.I,
)
_S4_TOPICS = {
    "machine learning", "deep learning", "calculus", "linear algebra",
    "data structures and algorithms", "operating systems", "computer networks",
    "electromagnetism", "organic chemistry", "world history", "quantum mechanics",
    "databases", "compilers", "statistics", "probability and statistics",
}
_S3_TOPICS = {
    "supervised learning", "unsupervised learning", "reinforcement learning",
    "neural networks", "transformers", "transformer architecture", "data preprocessing",
    "computer vision", "natural language processing", "graph algorithms",
    "dynamic programming", "sorting algorithms", "thermodynamics", "wave optics",
}
_S2_PATTERNS = re.compile(
    r"\b(?:variants|algorithms|methods|metrics|techniques|models|architectures|optimizers|"
    r"adam,\s*sgd|sgd,\s*adam|feature\s+scaling\s+methods|classification\s+metrics|"
    r"normalization\s+methods|loss\s+functions)\b",
    re.I,
)
_S0_PATTERNS = re.compile(
    r"^\s*(?:what\s+is\s+(?:a|an|the)?\s*|define\s+|definition\s+of\s+)|\batomic\s+(?:note|card)\b",
    re.I,
)


def classify_topic_scope(
    topic: str | None,
    raw_request: str,
    *,
    has_source: bool = False,
    source_sections: list[str] | None = None,
) -> dict[str, Any]:
    """Classify request scope across S0 (atomic) to S5 (extensive domain)."""
    if not topic or not topic.strip():
        return {
            "level": "unknown",
            "category": "missing_topic",
            "breadth": "unknown",
            "recommended_structure": "undetermined",
            "rationale": "No topic provided yet.",
        }

    t_low = topic.strip().lower()
    r_low = raw_request.strip().lower()

    if _S5_PATTERNS.search(r_low) or _S5_PATTERNS.search(t_low):
        return {
            "level": "S5",
            "category": "extensive_domain",
            "breadth": "very_high",
            "dependency_complexity": "very_high",
            "recommended_structure": "hierarchical_collection",
            "requires_scope_boundary": True,
            "rationale": "Extensive multi-course domain requiring explicit scope boundaries and staged hierarchical generation.",
        }

    if t_low in _S4_TOPICS or re.search(r"\b(?:complete\s+obsidian\s+knowledge\s+base|from\s+beginner\s+to\s+advanced|from\s+scratch)\b", r_low) and any(k in t_low for k in _S4_TOPICS | _S3_TOPICS):
        lvl = "S4" if t_low in _S4_TOPICS else "S3"
        cat = "broad_domain" if lvl == "S4" else "major_subject_area"
        return {
            "level": lvl,
            "category": cat,
            "breadth": "high",
            "dependency_complexity": "high",
            "recommended_structure": "hierarchical_collection",
            "requires_scope_boundary": lvl == "S4",
            "rationale": f"'{topic}' spans multiple independently teachable subtopics better organized as a linked hierarchy.",
        }

    if t_low in _S3_TOPICS or any(t_low == s or t_low.endswith(f" {s}") for s in _S3_TOPICS):
        return {
            "level": "S3",
            "category": "major_subject_area",
            "breadth": "high",
            "dependency_complexity": "medium_high",
            "recommended_structure": "hierarchical_collection",
            "requires_scope_boundary": False,
            "rationale": f"'{topic}' is a major subject area with a parent index and distinct child concepts.",
        }

    if source_sections and len(source_sections) >= 3:
        return {
            "level": "S3",
            "category": "chapter_or_multi_section_source",
            "breadth": "medium_high",
            "dependency_complexity": "medium",
            "recommended_structure": "hierarchical_collection",
            "requires_scope_boundary": False,
            "rationale": f"Supplied source spans {len(source_sections)} distinct sections.",
        }

    if _S2_PATTERNS.search(t_low) or _S2_PATTERNS.search(r_low) or len(re.findall(r"\b(?:adam|sgd|momentum|rmsprop|adagrad)\b", r_low)) >= 3:
        return {
            "level": "S2",
            "category": "multi_concept_topic",
            "breadth": "medium",
            "dependency_complexity": "medium",
            "recommended_structure": "single_or_small_collection",
            "requires_scope_boundary": False,
            "rationale": f"'{topic}' groups several closely related methods that can live in one detailed note or a small linked set.",
        }

    if _S0_PATTERNS.search(r_low) or len(t_low.split()) <= 2 and t_low in {"label", "capacitance", "learning rate", "scalar", "epoch", "bias"}:
        return {
            "level": "S0",
            "category": "atomic_concept",
            "breadth": "low",
            "dependency_complexity": "low",
            "recommended_structure": "single_note",
            "requires_scope_boundary": False,
            "rationale": f"'{topic}' is an atomic concept best captured in one focused note.",
        }

    return {
        "level": "S1",
        "category": "focused_topic",
        "breadth": "low_medium",
        "dependency_complexity": "medium",
        "recommended_structure": "single_note",
        "requires_scope_boundary": False,
        "rationale": f"'{topic}' is a focused standalone topic suited to one cohesive note unless expanded.",
    }


# ---------------------------------------------------------------------------
# Request Parsing & Template Recommendation (Parts 4, 11)
# ---------------------------------------------------------------------------

def _detect_known_preferences(raw: str) -> dict[str, Any]:
    """Extract explicit preferences already stated in the user's request so we never ask redundantly."""
    known: dict[str, Any] = {}
    low = raw.lower()

    # Audience / prior knowledge
    if re.search(r"\b(?:complete\s+beginner|beginner|completely\s+new|no\s+prior\s+knowledge)\b", low):
        known["prior_knowledge"] = {"level": "beginner", "known_concepts": [], "unknown_concepts": []}
    elif re.search(r"\b(?:beginner\s+to\s+advanced)\b", low):
        known["prior_knowledge"] = {"level": "beginner_to_advanced", "known_concepts": [], "unknown_concepts": []}
    elif re.search(r"\bintermediate\b", low):
        known["prior_knowledge"] = {"level": "intermediate", "known_concepts": [], "unknown_concepts": []}
    elif re.search(r"\badvanced\b", low):
        known["prior_knowledge"] = {"level": "advanced", "known_concepts": [], "unknown_concepts": []}

    # Named prior knowledge ("I already know X, Y, but not Z")
    m_know = re.search(r"\b(?:i\s+)?already\s+know\s+([^.;]+?)(?:\s*,?\s*but\s+(?:i\s+)?(?:don'?t|do\s+not)\s+understand\s+([^.;]+))?(?:[.!]|$)", raw, re.I)
    if m_know:
        known_list = [c.strip(" .") for c in re.split(r",|\band\b", m_know.group(1)) if c.strip(" .")]
        unknown_list = [c.strip(" .") for c in re.split(r",|\band\b", m_know.group(2) or "") if c.strip(" .")]
        known.setdefault("prior_knowledge", {"level": "intermediate", "known_concepts": [], "unknown_concepts": []})
        known["prior_knowledge"]["known_concepts"] = known_list
        known["prior_knowledge"]["unknown_concepts"] = unknown_list

    # Language
    m_lang = re.search(r"\b(?:in|with|using)\s+(python|c\+\+|cpp|rust|java|go|typescript|javascript|sql|c)\b(?!\s+and\s+d)", low)
    if m_lang:
        lang = m_lang.group(1)
        known["language"] = "cpp" if lang in {"c++", "cpp"} else lang

    # Depth
    if re.search(r"\b(?:exhaustive|encyclopedic)\b", low):
        known["depth"] = "exhaustive"
    elif re.search(r"\b(?:comprehensive|very\s+detailed|in\s+depth|deeply|deep(?:\s+(?:learning|beginner|intermediate|advanced|guide|notes?)))\b", low):
        known["depth"] = "comprehensive"
    elif re.search(r"\b(?:concise|brief|compact|quick|short|one-page)\b", low):
        known["depth"] = "concise"

    # Organization
    if re.search(r"\b(?:one\s+(?:complete\s+|single\s+)?note|single[\s-]+file|single[\s-]+note|all\s+in\s+one)\b", low):
        known["organization"] = "single_note"
    elif re.search(r"\b(?:multiple\s+(?:linked\s+)?(?:notes|files)|separate\s+(?:linked\s+)?(?:notes|files)|knowledge\s+base|hierarchical\s+collection|split\s+(?:the\s+topic\s+)?into)\b", low):
        known["organization"] = "hierarchical_collection"

    # Emphasis
    emphasis: list[str] = []
    for pat, label in (
        (r"\bintuition\b", "intuition"),
        (r"\b(?:derivations?|mathematical\s+derivations?|formulas?|math)\b", "mathematics"),
        (r"\bproofs?\b", "proofs"),
        (r"\b(?:worked\s+)?examples?\b", "examples"),
        (r"\b(?:code|python|c\+\+|rust|java|implementation|c\s+code)\b", "code"),
        (r"\b(?:execution\s+traces?|traces?|dry\s+run)\b", "traces"),
        (r"\b(?:diagrams?|visuals?)\b", "visuals"),
        (r"\b(?:active\s+recall|exercises?|practice\s+questions?)\b", "active_recall"),
    ):
        if re.search(pat, low):
            emphasis.append(label)
    if emphasis:
        known["emphasis"] = emphasis

    # Table / comparison explicit presentation
    if re.search(r"\bcomparison\s+table\b|\bin\s+a\s+table\b", low):
        known["table_format"] = True

    # Source-only / source-order explicit constraints
    if re.search(r"\b(?:source[- ]only|using\s+only|no\s+outside)\b", low):
        known["source_policy"] = "strict"
    if re.search(r"\b(?:original\s+order|lecture\s+order|exact\s+order|in\s+the\s+original\s+order)\b", low):
        known["preserve_source_order"] = True

    # Learning objective
    if re.search(r"\bexam\b|\bmidterm\b|\bfinals?\b", low):
        known["learning_objective"] = "exam_preparation"
    elif re.search(r"\binterview\b", low):
        known["learning_objective"] = "interview_preparation"
    elif re.search(r"\bcompare\b|\bvs\.?\b", low):
        known["learning_objective"] = "compare_alternatives"
    elif re.search(r"\bsolve\b", low):
        known["learning_objective"] = "solve_problems"
    elif re.search(r"\bimplement|build\b", low):
        known["learning_objective"] = "practical_implementation"
    elif re.search(r"\bcheat\s?sheet|quick\s+revision|formula\s+sheet\b", low):
        known["learning_objective"] = "quick_revision"

    return known


def analyze_universal_request(
    raw_request: str,
    *,
    has_source: bool = False,
    source_sections: list[str] | None = None,
    existing_vault_notes: list[str] | None = None,
    root: Path = REPO_ROOT,
) -> tuple[NoteRequestIntent, NoteConfigurationRecommendation, dict[str, Any]]:
    """Parse any /scribe-notes request, infer scope, and produce provisional template recommendations."""
    raw = raw_request.strip()
    first, *rest = raw.split(maxsplit=1) if raw else ("", [])
    cmd_token = first.lower().lstrip("/") if first.startswith("/") or first.lower().startswith("scribe-") else ""

    migration_hint: str | None = None
    payload = raw
    if cmd_token == "scribe-notes":
        payload = rest[0].strip() if rest else ""
    elif cmd_token in RETIRED_NOTE_COMMANDS:
        migration_hint = f"Command '/{cmd_token}' has been consolidated into '/scribe-notes' ({RETIRED_NOTE_COMMANDS[cmd_token]})."
        payload = rest[0].strip() if rest else ""

    # Empty /scribe-notes invocation -> request topic first!
    if not payload:
        intent = NoteRequestIntent(
            raw_request=raw,
            topic=None,
            requested_artifact=None,
            explicit_constraints={},
            source_bindings=[],
            inferred_scope="missing_topic",
            migration_hint=migration_hint,
        )
        rec = NoteConfigurationRecommendation(
            recommended_master="M1",
            recommended_variant=None,
            recommended_depth="standard",
            recommended_organization="single_note",
            recommended_learning_objective="conceptual_mastery",
            confidence="low",
            rationale=["Topic is required before selecting format and scope."],
        )
        return intent, rec, {"level": "unknown", "category": "missing_topic"}

    # Detect update/expand existing note intent
    update_existing = bool(re.search(r"\b(?:expand|update|extend)\s+(?:my\s+)?(?:existing\s+)?", payload, re.I)) or cmd_token == "scribe-expand"
    explicit = _detect_known_preferences(payload)
    sources = [{"url": m.group().rstrip(".,;")} for m in URL_RE.finditer(payload)]
    has_src = has_source or bool(sources) or bool(re.search(r"\b(?:this|my|the)\s+(?:pdf|chapter|lecture|transcript|slides|paper)\b", payload, re.I))

    # Reuse existing OrchestrationEngine normalizer & router (no keyword-only replacement!)
    norm = normalize_request(payload, source_policy=explicit.get("source_policy"), has_source=has_src, root=root)
    routed = norm["routed"]
    topic = norm["topic"]
    if update_existing:
        topic = re.sub(r"^(?:expand|update|extend)\s+(?:my\s+)?(?:existing\s+)?", "", topic, flags=re.I)
        topic = re.sub(r"\s+notes?$", "", topic, flags=re.I).strip() or norm["topic"]

    # Map retired command intent if payload lacked explicit format words
    rec_master = routed["master"] or "M1"
    rec_variant = routed["variant"]
    if cmd_token == "scribe-distill" and rec_master == "M1":
        rec_master, rec_variant = "M3", None
    elif cmd_token == "scribe-atomic-notes" and rec_master == "M1":
        rec_master, rec_variant = "M3", "atomic_card"
    elif cmd_token == "scribe-compare" and rec_master == "M1":
        rec_master, rec_variant = "M7", "comparison_guide"
    elif cmd_token == "scribe-dsa" and rec_master == "M1":
        rec_master, rec_variant = "M5", None
    elif cmd_token == "scribe-practice" and rec_master == "M1":
        rec_master, rec_variant = "M6", None
    elif cmd_token == "scribe-ingest" and rec_master == "M1":
        rec_master, rec_variant = "M2", "lecture_order"

    # Comparison table specialization (Section 11.4: variant, NOT an eighth master!)
    if explicit.get("table_format") and rec_master in {"M7", "M3", "M1"}:
        if explicit.get("depth") == "concise":
            rec_master, rec_variant = "M3", "compact_comparison"
        else:
            rec_master, rec_variant = "M7", "comparison_table"

    # Deep multi-method comparison with formulas & code (Scenario E)
    if re.search(r"\bcompare\b", payload, re.I) and ("code" in explicit.get("emphasis", []) or "mathematics" in explicit.get("emphasis", [])):
        rec_master, rec_variant = "M7", "comparison_guide"

    # Implementation-oriented explanation with explicit language & traces (Section 9.2 / Scenario)
    if explicit.get("language") and ("code" in explicit.get("emphasis", []) or "traces" in explicit.get("emphasis", [])):
        if rec_master == "M1" and not re.search(r"\bcompare\b", payload, re.I):
            rec_master = "M5"

    # Source-ordered PDF/chapter requests default to M2/lecture_order
    if explicit.get("preserve_source_order") and rec_master == "M1":
        rec_master, rec_variant = "M2", "lecture_order"

    scope = classify_topic_scope(topic, payload, has_source=has_src, source_sections=source_sections)

    # Organization recommendation
    if explicit.get("organization"):
        rec_org = explicit["organization"]
    elif rec_master in {"M3", "M4", "M6"} and scope["level"] in {"S0", "S1", "S2"}:
        rec_org = "single_note"
    elif scope["recommended_structure"] == "hierarchical_collection":
        rec_org = "hierarchical_collection"
    elif scope["level"] == "S2" and explicit.get("depth") in {"comprehensive", "exhaustive"}:
        rec_org = "hierarchical_collection"
    else:
        rec_org = "single_note"

    # Depth recommendation
    rec_depth = explicit.get("depth") or (
        "concise" if rec_master == "M3" else ("comprehensive" if scope["level"] in {"S3", "S4", "S5"} or rec_master == "M1" else "standard")
    )

    rec_obj = explicit.get("learning_objective") or {
        "M1": "conceptual_mastery",
        "M2": "structured_study",
        "M3": "quick_revision",
        "M4": "solve_problems",
        "M5": "practical_implementation",
        "M6": "self_assessment",
        "M7": "compare_alternatives" if rec_variant and "comparison" in rec_variant else "synthesis_and_revision",
    }.get(rec_master, "conceptual_mastery")

    alt_master = "M1" if rec_master == "M5" else ("M5" if rec_master == "M1" and explicit.get("language") else None)
    rationale = [
        f"Scope '{scope['level']}' ({scope['category']}): {scope['rationale']}",
        f"Selected {rec_master} ({MASTER_READABLE_NAMES[rec_master]})" + (f" with variant '{rec_variant}'" if rec_variant else "") + ".",
    ]
    if existing_vault_notes:
        explicit["existing_vault_matches"] = list(existing_vault_notes)

    all_bindings = list(sources)
    if source_sections:
        for idx, sec in enumerate(source_sections, 1):
            all_bindings.append({"section": str(sec), "order": idx})

    intent = NoteRequestIntent(
        raw_request=raw,
        topic=topic,
        requested_artifact=rec_variant or rec_master,
        explicit_constraints=explicit,
        source_bindings=all_bindings,
        inferred_scope=scope["level"],
        update_existing=update_existing,
        migration_hint=migration_hint,
    )
    recommendation = NoteConfigurationRecommendation(
        recommended_master=rec_master,
        recommended_variant=rec_variant,
        recommended_depth=rec_depth,
        recommended_organization=rec_org,
        recommended_learning_objective=rec_obj,
        confidence="medium" if alt_master else "high",
        rationale=rationale,
        alternative_master=alt_master,
    )
    return intent, recommendation, scope


# ---------------------------------------------------------------------------
# Parts 6-10 — Adaptive Interactive Configuration Gate & State Machine
# ---------------------------------------------------------------------------

def _build_adaptive_questions(
    intent: NoteRequestIntent,
    rec: NoteConfigurationRecommendation,
    scope: dict[str, Any],
) -> list[dict[str, Any]]:
    """Select only materially unresolved questions (typically 2-6 compact questions, zero redundancy)."""
    if intent.topic is None:
        return [{
            "id": "topic",
            "prompt": "What topic, question, or source would you like notes on?",
            "reason": "Topic is missing from bare /scribe-notes invocation.",
            "default": None,
        }]

    known = intent.explicit_constraints
    questions: list[dict[str, Any]] = []

    if "learning_objective" not in known and rec.recommended_master not in {"M3", "M4"}:
        questions.append({
            "id": "learning_objective",
            "prompt": "Purpose: (A) Understand from scratch, (B) Exam prep, (C) Interviews, (D) Practical implementation, (E) Research/reference",
            "reason": "Learning objective shapes examples, order, and rigor.",
            "default": rec.recommended_learning_objective,
        })

    if not known.get("table_format") and rec.recommended_master in {"M1", "M2", "M5", "M7"} and not re.search(r"\b(?:cheat[\s-]?sheet|formula[\s-]?sheet|worked\s+solutions?|compare|practice\s+test|flashcards?)\b", intent.raw_request, re.I):
        questions.append({
            "id": "master",
            "prompt": f"Notes format: (A) Use recommended ({MASTER_READABLE_NAMES[rec.recommended_master]}), (B) Deep notes, (C) Study notes, (D) Cheat sheet, (E) Worked solutions, (F) Implementation guide, (G) Practice set, (H) Synthesis/comparison",
            "reason": "Allow user to confirm or override provisional template recommendation.",
            "default": rec.recommended_master,
        })

    if "depth" not in known:
        questions.append({
            "id": "depth",
            "prompt": f"Depth: (A) Concise, (B) Standard, (C) Comprehensive, (D) Exhaustive (recommended: {rec.recommended_depth})",
            "reason": "Controls concept detail allocation without replacing per-concept depth planning.",
            "default": rec.recommended_depth,
        })

    if "prior_knowledge" not in known:
        questions.append({
            "id": "prior_knowledge",
            "prompt": "Current knowledge: (A) Completely new, (B) Know the basics, (C) Intermediate, (D) Advanced — or name what you already know",
            "reason": "Calibrates prerequisite bridges and assumed baseline.",
            "default": "intermediate",
        })

    if "organization" not in known and scope["level"] not in {"S0"}:
        questions.append({
            "id": "organization",
            "prompt": f"Organization: (A) Automatic — {rec.recommended_organization.replace('_', ' ')} (recommended), (B) One complete note, (C) Multiple linked notes",
            "reason": "Determines single-note vs hierarchical Obsidian collection.",
            "default": rec.recommended_organization,
        })

    if "emphasis" not in known and rec.recommended_master in {"M1", "M2", "M5", "M7"}:
        questions.append({
            "id": "emphasis",
            "prompt": "Special emphasis (optional): intuition, math/derivations, proofs, worked examples, code, traces, diagrams, or active recall",
            "reason": "Activates relevant adaptive modules.",
            "default": [],
        })

    # Context-sensitive optional questions (Part 8 — asked ONLY when relevant!)
    if (intent.source_bindings or re.search(r"\b(?:pdf|chapter|lecture|transcript)\b", intent.raw_request, re.I)) and "source_policy" not in known:
        questions.append({
            "id": "source_policy",
            "prompt": "Source handling: strictly follow provided source only, verify it, or supplement with external references?",
            "reason": "Source provided without explicit source-only/expanded policy.",
            "default": "source_first",
        })
    if scope.get("requires_scope_boundary"):
        questions.append({
            "id": "scope_boundary",
            "prompt": "Scope boundary: (A) Foundational curriculum (recommended), (B) Complete topic survey, (C) Focused subset",
            "reason": "Broad domain requires explicit scope boundary.",
            "default": "foundational_curriculum",
        })
    if known.get("existing_vault_matches") and not intent.update_existing:
        questions.append({
            "id": "existing_notes",
            "prompt": f"Existing notes found ({', '.join(known['existing_vault_matches'][:3])}): extend them incrementally or create a separate collection?",
            "reason": "Avoid overwriting or duplicating existing vault notes.",
            "default": "extend_existing",
        })

    return questions[:6]


def start_notes_session(
    raw_request: str,
    *,
    has_source: bool = False,
    source_sections: list[str] | None = None,
    existing_vault_notes: list[str] | None = None,
    root: Path = REPO_ROOT,
) -> NoteInteractionState:
    """Entry point for /scribe-notes: analyzes request and ALWAYS stops at configuration before generating."""
    intent, rec, scope = analyze_universal_request(
        raw_request,
        has_source=has_source,
        source_sections=source_sections,
        existing_vault_notes=existing_vault_notes,
        root=root,
    )
    req_id = "req-" + hashlib.sha256(f"{raw_request.strip()}".encode("utf-8")).hexdigest()[:12]
    questions = _build_adaptive_questions(intent, rec, scope)
    stage = "AWAITING_TOPIC" if intent.topic is None else "AWAITING_CONFIGURATION"
    trace = [
        {"question_id": q["id"], "reason": q["reason"], "default": q["default"]}
        for q in questions
    ]
    return NoteInteractionState(
        request_id=req_id,
        stage=stage,
        original_intent=intent,
        recommendation=rec,
        questions_asked=questions,
        question_trace=trace,
    )


def format_configuration_prompt(state: NoteInteractionState) -> str:
    """Render a clean, plain-text conversational configuration message (no GUI required)."""
    lines: list[str] = []
    if state.original_intent.migration_hint:
        lines.append(f"Note: {state.original_intent.migration_hint}")
        lines.append("")

    if state.stage == "AWAITING_TOPIC":
        lines.append("What topic, question, or source would you like me to create notes for?")
        return "\n".join(lines)

    rec = state.recommendation
    topic = state.original_intent.topic
    lines.append(f"Topic detected: **{topic}** (scope: `{state.original_intent.inferred_scope}`)")
    lines.append("")
    lines.append("Recommended setup:")
    lines.append(f"- Format: {MASTER_READABLE_NAMES[rec.recommended_master]}" + (f" ({rec.recommended_variant.replace('_', ' ')})" if rec.recommended_variant else ""))
    lines.append(f"- Depth: {rec.recommended_depth.title()}")
    lines.append(f"- Organization: {rec.recommended_organization.replace('_', ' ').title()}")
    if rec.alternative_master:
        lines.append(f"- Alternative: {MASTER_READABLE_NAMES[rec.alternative_master]}")
    lines.append("")
    lines.append("Before I generate the notes, confirm or adjust your preferences:")
    for idx, q in enumerate(state.questions_asked, 1):
        lines.append(f"{idx}. {q['prompt']}")
    lines.append("")
    lines.append('Reply naturally with your choices, or say "use your recommendations" to proceed.')
    return "\n".join(lines)


def _parse_user_preferences(
    reply: str,
    state: NoteInteractionState,
) -> ResolvedNotePreferences:
    """Parse free-text, numbered/lettered, partial, or default-acceptance replies without losing prior constraints."""
    rec = state.recommendation
    known = state.original_intent.explicit_constraints
    prev = state.resolved_preferences
    low = reply.strip().lower()

    accept_defaults = bool(re.search(
        r"\b(?:use\s+(?:your\s+)?recommendations?|default\s+settings?|defaults?|surprise\s+me|proceed|looks?\s+good|go\s+ahead|yes)\b",
        low,
    ))

    # Start from previous resolved prefs (for corrections) or recommendations + explicit initial constraints
    master = prev.master if prev else rec.recommended_master
    variant = prev.variant if prev else rec.recommended_variant
    depth = prev.depth if prev else known.get("depth", rec.recommended_depth)
    organization = prev.organization if prev else known.get("organization", rec.recommended_organization)
    objective = prev.learning_objective if prev else known.get("learning_objective", rec.recommended_learning_objective)
    prior_knowledge = dict(prev.prior_knowledge) if prev else dict(known.get("prior_knowledge") or {"level": "intermediate", "known_concepts": [], "unknown_concepts": []})
    emphasis = list(prev.emphasis) if prev else list(known.get("emphasis") or [])
    source_policy = prev.source_policy if prev else known.get("source_policy", "adaptive")
    preserve_order = prev.preserve_source_order if prev else bool(known.get("preserve_source_order", False))
    language = prev.language if prev else known.get("language")
    scope_boundary = prev.scope_boundary if prev else "foundational_curriculum"

    if not accept_defaults:
        # Parse numbered/lettered shorthand like "1B, 2D, 3A" mapped to actual asked questions
        for num_str, letter in re.findall(r"\b(\d)\s*([A-Ha-h])\b", reply):
            q_idx = int(num_str) - 1
            if 0 <= q_idx < len(state.questions_asked):
                qid = state.questions_asked[q_idx]["id"]
                ch = letter.upper()
                if qid == "learning_objective":
                    objective = {"A": "understand_from_scratch", "B": "exam_preparation", "C": "interview_preparation", "D": "practical_implementation", "E": "research_reference"}.get(ch, objective)
                elif qid == "master":
                    mapped = {"B": "M1", "C": "M2", "D": "M3", "E": "M4", "F": "M5", "G": "M6", "H": "M7"}.get(ch)
                    if mapped:
                        master, variant = mapped, None
                elif qid == "depth":
                    depth = {"A": "concise", "B": "standard", "C": "comprehensive", "D": "exhaustive"}.get(ch, depth)
                elif qid == "prior_knowledge":
                    prior_knowledge["level"] = {"A": "beginner", "B": "basic", "C": "intermediate", "D": "advanced"}.get(ch, prior_knowledge["level"])
                elif qid == "organization":
                    organization = {"A": rec.recommended_organization, "B": "single_note", "C": "hierarchical_collection"}.get(ch, organization)
                elif qid == "scope_boundary":
                    scope_boundary = {"A": "foundational_curriculum", "B": "complete_survey", "C": "focused_subset"}.get(ch, scope_boundary)

        # Free-text preference extraction
        parsed_free = _detect_known_preferences(reply)
        if "depth" in parsed_free:
            depth = parsed_free["depth"]
        elif re.search(r"\bstandard\b", low):
            depth = "standard"
        if "organization" in parsed_free:
            organization = parsed_free["organization"]
        if "prior_knowledge" in parsed_free:
            prior_knowledge.update({k: v for k, v in parsed_free["prior_knowledge"].items() if v})
        if "language" in parsed_free:
            language = parsed_free["language"]
        if "emphasis" in parsed_free:
            for item in parsed_free["emphasis"]:
                if item not in emphasis:
                    emphasis.append(item)
        if "source_policy" in parsed_free:
            source_policy = parsed_free["source_policy"]
        if "preserve_source_order" in parsed_free:
            preserve_order = True
        if "learning_objective" in parsed_free:
            objective = parsed_free["learning_objective"]

        # Explicit master override in free text
        if re.search(r"\bcheat\s?sheet|quick\s+reference\b", low):
            master, variant = "M3", None
        elif re.search(r"\bworked\s+solutions?\b", low):
            master, variant = "M4", None
        elif re.search(r"\bimplementation\s+guide|technical\s+guide\b", low):
            master, variant = "M5", None
        elif re.search(r"\bpractice\s+(?:set|questions?)|assessment|flashcards?\b", low):
            master, variant = "M6", ("flashcards" if "flashcard" in low else None)
        elif re.search(r"\bcomparison\s+table\b", low):
            master, variant = "M7", "comparison_table"
        elif re.search(r"\bdeep\s+(?:learning\s+)?notes?|deep\s+explanations?\b", low):
            master, variant = "M1", None
        elif re.search(r"\bstructured\s+study\s+notes?\b", low):
            master, variant = "M2", None

    return ResolvedNotePreferences(
        learning_objective=objective,
        master=master,
        variant=variant,
        depth=depth,
        prior_knowledge=prior_knowledge,
        organization=organization,
        emphasis=emphasis,
        source_policy=source_policy,
        preserve_source_order=preserve_order,
        language=language,
        scope_boundary=scope_boundary,
        custom_constraints=dict(known),
    )


# ---------------------------------------------------------------------------
# Parts 13-18 & 22 — Hierarchical Topic Decomposition & Collection Preview
# ---------------------------------------------------------------------------

# Domain-grounded hierarchical blueprints (separate topic hierarchy, prerequisites, and related links!)
COLLECTION_CURRICULA: dict[str, dict[str, Any]] = {
    "machine_learning": {
        "title": "Machine Learning",
        "groups": [
            ("Foundations", [
                ("What is Machine Learning", "M1", [], ["Types of Machine Learning"]),
                ("Types of Machine Learning", "M1", ["What is Machine Learning"], ["Supervised Learning"]),
                ("Features and Labels", "M1", ["What is Machine Learning"], ["Data Preparation"]),
            ]),
            ("Supervised Learning", [
                ("Linear Regression", "M1", ["Features and Labels"], ["Loss Functions", "Gradient Descent"]),
                ("Logistic Regression", "M1", ["Linear Regression"], ["Classification Metrics"]),
            ]),
            ("Data Preparation", [
                ("Missing Values", "M2", ["Features and Labels"], ["Feature Scaling"]),
                ("Feature Scaling", "M1", ["Features and Labels"], ["Gradient Descent"]),
            ]),
            ("Optimization", [
                ("Loss Functions", "M1", ["Linear Regression"], ["Gradient Descent"]),
                ("Gradient Descent", "M1", ["Loss Functions"], ["Feature Scaling", "Regularization"]),
                ("Regularization", "M1", ["Loss Functions", "Gradient Descent"], ["Overfitting and Underfitting"]),
            ]),
            ("Evaluation", [
                ("Overfitting and Underfitting", "M1", ["Linear Regression"], ["Regularization"]),
                ("Classification Metrics", "M7", ["Logistic Regression"], ["Overfitting and Underfitting"]),
            ]),
        ],
        "external_prerequisites": ["Derivatives", "Linear Algebra Basics", "Introductory Probability"],
    },
    "supervised_learning": {
        "title": "Supervised Learning",
        "groups": [
            ("Core Formulation", [
                ("Features, Targets, and Hypothesis Spaces", "M1", [], ["Loss Functions"]),
                ("Loss Functions", "M1", ["Features, Targets, and Hypothesis Spaces"], ["Gradient Descent"]),
            ]),
            ("Models", [
                ("Linear Regression", "M1", ["Loss Functions"], ["Gradient Descent"]),
                ("Logistic Regression", "M1", ["Linear Regression"], ["Decision Trees"]),
                ("Decision Trees", "M1", ["Features, Targets, and Hypothesis Spaces"], ["Logistic Regression"]),
            ]),
            ("Generalization", [
                ("Bias-Variance Tradeoff", "M1", ["Linear Regression"], ["Regularization"]),
                ("Regularization", "M1", ["Loss Functions", "Bias-Variance Tradeoff"], ["Linear Regression"]),
            ]),
        ],
        "external_prerequisites": ["Basic Calculus", "Probability Distributions"],
    },
    "transformers": {
        "title": "Transformers",
        "groups": [
            ("Representations", [
                ("Tokenization and Embeddings", "M1", [], ["Positional Encoding"]),
                ("Positional Encoding", "M1", ["Tokenization and Embeddings"], ["Scaled Dot-Product Attention"]),
            ]),
            ("Attention Mechanisms", [
                ("Scaled Dot-Product Attention", "M1", ["Positional Encoding"], ["Multi-Head Attention"]),
                ("Multi-Head Attention", "M1", ["Scaled Dot-Product Attention"], ["Encoder and Decoder Blocks"]),
            ]),
            ("Architecture and Training", [
                ("Encoder and Decoder Blocks", "M1", ["Multi-Head Attention"], ["Backpropagation"]),
                ("Training and Autoregressive Inference", "M5", ["Encoder and Decoder Blocks"], ["Scaled Dot-Product Attention"]),
            ]),
        ],
        "external_prerequisites": ["Matrix Multiplication", "Softmax", "Backpropagation"],
    },
    "optimization_algorithms": {
        "title": "Optimization Algorithms",
        "groups": [
            ("First-Order Foundations", [
                ("Gradient Descent", "M1", [], ["Stochastic Gradient Descent", "Momentum"]),
                ("Stochastic Gradient Descent", "M1", ["Gradient Descent"], ["Momentum"]),
                ("Momentum", "M1", ["Gradient Descent"], ["RMSProp", "Adam"]),
            ]),
            ("Adaptive Methods", [
                ("RMSProp", "M1", ["Gradient Descent"], ["Adam"]),
                ("Adam", "M1", ["Momentum", "RMSProp"], ["Optimizer Comparison"]),
                ("Optimizer Comparison", "M7", ["Gradient Descent", "Momentum", "RMSProp", "Adam"], []),
            ]),
        ],
        "external_prerequisites": ["Multivariable Derivatives", "Gradients"],
    },
}


def _safe_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", name.strip()).strip(" .")
    return cleaned or "Untitled"


def plan_note_collection(
    topic: str,
    preferences: ResolvedNotePreferences,
    *,
    scope: dict[str, Any] | None = None,
    source_sections: list[dict[str, str]] | None = None,
) -> NoteCollectionPlan:
    """Plan either a single note or a hierarchical multi-note collection with separate hierarchy & prerequisite graphs."""
    clean_topic = topic.strip()
    cid_root = f"topic.{slugify(clean_topic).replace('-', '_')}"
    root_folder = _safe_filename(clean_topic)
    coll_id = f"col-{slugify(clean_topic)}"

    # Explicit single-note preference always respected (Section 13.5)
    if preferences.organization == "single_note":
        node = TopicNode(
            concept_id=cid_root,
            title=clean_topic,
            parent_id=None,
            proposed_path=f"{root_folder}.md",
            note_role="single",
            template_plan={
                "master": preferences.master,
                "variant": preferences.variant,
                "depth": preferences.depth,
                "language": preferences.language,
                "emphasis": list(preferences.emphasis),
            },
            source_bindings=list(source_sections or []),
        )
        return NoteCollectionPlan(
            collection_id=coll_id,
            title=clean_topic,
            root_topic_id=cid_root,
            organization="single_note",
            nodes=[node],
            planned_paths=[node.proposed_path],
            learning_order=[cid_root],
            generation_order=[cid_root],
            scope_summary={
                "root_indexes": 0,
                "topic_groups": 0,
                "child_notes": 1,
                "exhaustive_domain_claim": False,
                "scope_boundary": preferences.scope_boundary,
            },
        )

    nodes: list[TopicNode] = []
    root_path = f"{root_folder}/{root_folder}.md"

    # Case 1: Source-faithful section decomposition (Part 22 — never invents extra topics in strict mode!)
    if source_sections:
        root_node = TopicNode(
            concept_id=cid_root,
            title=clean_topic,
            parent_id=None,
            proposed_path=root_path,
            note_role="root_index",
            template_plan={"master": "M7", "note_type": "index", "depth": "standard"},
        )
        child_ids: list[str] = []
        prev_cid: str | None = None
        for idx, sec in enumerate(source_sections, 1):
            sec_title = str(sec.get("title") or f"Section {idx}").strip()
            sec_id = f"{cid_root}.s{idx}_{slugify(sec_title).replace('-', '_')}"
            sec_path = f"{root_folder}/{idx:02d} - {_safe_filename(sec_title)}.md"
            child_ids.append(sec_id)
            nodes.append(TopicNode(
                concept_id=sec_id,
                title=sec_title,
                parent_id=cid_root,
                prerequisite_ids=[prev_cid] if prev_cid else [],
                proposed_path=sec_path,
                note_role="child",
                template_plan={
                    "master": preferences.master,
                    "variant": "lecture_order" if preferences.preserve_source_order else preferences.variant,
                    "depth": preferences.depth,
                    "source_policy": preferences.source_policy,
                    "preserve_source_order": preferences.preserve_source_order,
                },
                source_bindings=[sec],
            ))
            prev_cid = sec_id
        root_node.child_ids = child_ids
        all_nodes = [root_node, *nodes]
        return NoteCollectionPlan(
            collection_id=coll_id,
            title=clean_topic,
            root_topic_id=cid_root,
            organization="hierarchical_collection",
            nodes=all_nodes,
            planned_paths=[n.proposed_path for n in all_nodes],
            learning_order=child_ids,
            generation_order=[*child_ids, cid_root],
            scope_summary={
                "root_indexes": 1,
                "topic_groups": 0,
                "child_notes": len(child_ids),
                "source_sections_mapped": len(source_sections),
                "source_order_preserved": preferences.preserve_source_order,
                "exhaustive_domain_claim": False,
            },
        )

    # Case 2: Hierarchical domain decomposition (preset curricula or adaptive generic decomposition)
    key = slugify(clean_topic).replace("-", "_")
    curriculum = COLLECTION_CURRICULA.get(key)
    if curriculum is None:
        # Check partial match (e.g., "optimization algorithms used in machine learning")
        if "optimization" in key and "algorithm" in key:
            curriculum = COLLECTION_CURRICULA["optimization_algorithms"]
        elif "transformer" in key:
            curriculum = COLLECTION_CURRICULA["transformers"]
        elif "supervised" in key and "learning" in key:
            curriculum = COLLECTION_CURRICULA["supervised_learning"]
        elif "machine_learning" in key:
            curriculum = COLLECTION_CURRICULA["machine_learning"]
        else:
            # Adaptive non-fragmented 3-group decomposition for any broad topic
            curriculum = {
                "title": clean_topic,
                "groups": [
                    ("Foundations", [
                        (f"{clean_topic} Fundamentals", preferences.master, [], []),
                        (f"Core Principles of {clean_topic}", preferences.master, [f"{clean_topic} Fundamentals"], []),
                    ]),
                    ("Core Mechanisms", [
                        (f"Methods and Techniques in {clean_topic}", preferences.master, [f"Core Principles of {clean_topic}"], []),
                        (f"Worked Examples in {clean_topic}", "M4", [f"Methods and Techniques in {clean_topic}"], []),
                    ]),
                    ("Synthesis and Practice", [
                        (f"{clean_topic} Summary and Comparisons", "M7", [f"Methods and Techniques in {clean_topic}"], []),
                    ]),
                ],
                "external_prerequisites": [],
            }

    # Pre-assign canonical concept_ids for every child title (zero duplicate canonical concepts!)
    title_to_cid: dict[str, str] = {}
    for group_name, items in curriculum["groups"]:
        g_slug = slugify(group_name).replace("-", "_")
        for item_title, _, _, _ in items:
            if item_title not in title_to_cid:
                title_to_cid[item_title] = f"{slugify(clean_topic).replace('-', '_')}.{g_slug}.{slugify(item_title).replace('-', '_')}"

    root_node = TopicNode(
        concept_id=cid_root,
        title=curriculum["title"],
        parent_id=None,
        prerequisite_ids=list(curriculum.get("external_prerequisites") or []),
        proposed_path=root_path,
        note_role="root_index",
        template_plan={"master": "M7", "note_type": "index", "depth": "standard"},
    )
    group_nodes: list[TopicNode] = []
    child_nodes: list[TopicNode] = []
    seen_paths: set[str] = {root_path.casefold()}

    for group_name, items in curriculum["groups"]:
        g_id = f"{cid_root}.{slugify(group_name).replace('-', '_')}"
        g_folder = _safe_filename(group_name)
        g_child_ids: list[str] = []

        for item_title, item_master, prereq_titles, rel_titles in items:
            c_id = title_to_cid[item_title]
            c_path = f"{root_folder}/{g_folder}/{_safe_filename(item_title)}.md"
            if c_path.casefold() in seen_paths:
                continue
            seen_paths.add(c_path.casefold())
            g_child_ids.append(c_id)
            eff_master = preferences.master if preferences.master in {"M2", "M3", "M6"} else item_master
            child_nodes.append(TopicNode(
                concept_id=c_id,
                title=item_title,
                parent_id=g_id,
                prerequisite_ids=[title_to_cid.get(p, p) for p in prereq_titles],
                related_ids=[title_to_cid.get(r, r) for r in rel_titles],
                proposed_path=c_path,
                note_role="child",
                template_plan={
                    "master": eff_master,
                    "variant": preferences.variant if eff_master == preferences.master else None,
                    "depth": preferences.depth,
                    "language": preferences.language,
                    "emphasis": list(preferences.emphasis),
                    "source_policy": preferences.source_policy,
                },
            ))

        group_nodes.append(TopicNode(
            concept_id=g_id,
            title=group_name,
            parent_id=cid_root,
            child_ids=g_child_ids,
            proposed_path=f"{root_folder}/{g_folder}/{g_folder}.md",
            note_role="group_index",
            template_plan={"master": "M7", "note_type": "index", "depth": "concise"},
        ))
        root_node.child_ids.append(g_id)

    all_nodes = [root_node, *group_nodes, *child_nodes]
    learning_order = [n.concept_id for n in child_nodes]
    generation_order = [*learning_order, *[g.concept_id for g in group_nodes], cid_root]

    return NoteCollectionPlan(
        collection_id=coll_id,
        title=curriculum["title"],
        root_topic_id=cid_root,
        organization="hierarchical_collection",
        nodes=all_nodes,
        planned_paths=[n.proposed_path for n in all_nodes],
        learning_order=learning_order,
        generation_order=generation_order,
        scope_summary={
            "scope_tier": classify_topic_scope(clean_topic, clean_topic)["level"],
            "root_indexes": 1,
            "topic_groups": len(group_nodes),
            "child_notes": len(child_nodes),
            "total_notes": len(all_nodes),
            "exhaustive_domain_claim": False,
            "scope_boundary": preferences.scope_boundary,
            "external_prerequisites": list(curriculum.get("external_prerequisites") or []),
        },
    )


def format_collection_preview(plan: NoteCollectionPlan, preferences: ResolvedNotePreferences) -> str:
    """Render an honest, exact-count collection outline preview for user approval/modification."""
    lines = [
        f"Proposed collection: **{plan.title}**",
        f"- Organization: {plan.organization.replace('_', ' ').title()}",
        f"- Depth: {preferences.depth.title()} | Level: {preferences.prior_knowledge.get('level', 'intermediate')}",
        "",
        "Planned structure:",
    ]
    node_map = {n.concept_id: n for n in plan.nodes}
    groups = [n for n in plan.nodes if n.note_role == "group_index"]
    if groups:
        for idx, g in enumerate(groups, 1):
            lines.append(f"{idx}. **{g.title}**")
            for cid in g.child_ids:
                child = node_map.get(cid)
                if child:
                    lines.append(f"   - {child.title} (`{child.template_plan.get('master', 'M1')}`)")
    else:
        for idx, n in enumerate([x for x in plan.nodes if x.note_role == "child"], 1):
            lines.append(f"{idx}. {n.title} (`{n.template_plan.get('master', 'M1')}`)")
    s = plan.scope_summary
    lines.extend([
        "",
        f"Estimated files: {s.get('root_indexes', 0)} root index, {s.get('topic_groups', 0)} topic group index(es), {s.get('child_notes', 0)} child notes.",
        f"Note: This is a scoped collection ({s.get('scope_boundary', 'foundational')}), not an exhaustive claim over the entire field.",
        "Proceed, remove/add sections, or restrict to one section?",
    ])
    return "\n".join(lines)


def modify_collection_plan(plan: NoteCollectionPlan, instruction: str) -> NoteCollectionPlan:
    """Apply user outline revisions ('Remove X', 'Generate only Y', 'Add Z') without restarting planning."""
    low = instruction.strip().lower()
    node_map = {n.concept_id: n for n in plan.nodes}
    root = node_map[plan.root_topic_id]

    # 1. "Generate only <group> section"
    m_only = re.search(r"\b(?:only|just)\s+(?:the\s+)?([\w\s-]+?)(?:\s+section|\s+group|\s+part)?$", low)
    if m_only:
        target = m_only.group(1).strip()
        keep_groups = [n for n in plan.nodes if n.note_role == "group_index" and target in n.title.lower()]
        if keep_groups:
            keep_gids = {g.concept_id for g in keep_groups}
            keep_cids = {cid for g in keep_groups for cid in g.child_ids}
            root.child_ids = [g.concept_id for g in keep_groups]
            new_nodes = [root, *keep_groups, *[n for n in plan.nodes if n.concept_id in keep_cids]]
            return _rebuild_plan_stats(plan, new_nodes)

    # 2. "Remove <topic or group>"
    m_rem = re.search(r"\b(?:remove|drop|skip|exclude)\s+(?:the\s+)?([\w\s-]+?)(?:\s+section|\s+group)?$", low)
    if m_rem:
        target = m_rem.group(1).strip()
        drop_ids: set[str] = set()
        for n in plan.nodes:
            if n.concept_id != plan.root_topic_id and target in n.title.lower():
                drop_ids.add(n.concept_id)
                drop_ids.update(n.child_ids)
        if drop_ids:
            new_nodes = []
            for n in plan.nodes:
                if n.concept_id in drop_ids:
                    continue
                n.child_ids = [c for c in n.child_ids if c not in drop_ids]
                n.prerequisite_ids = [p for p in n.prerequisite_ids if p not in drop_ids]
                n.related_ids = [r for r in n.related_ids if r not in drop_ids]
                new_nodes.append(n)
            return _rebuild_plan_stats(plan, new_nodes)

    # 3. "Add <topic>"
    m_add = re.search(r"\badd\s+(?:a\s+note\s+(?:on|for)\s+)?([\w\s-]+?)$", instruction.strip(), re.I)
    if m_add:
        new_title = m_add.group(1).strip(" .")
        new_cid = f"{plan.root_topic_id}.{slugify(new_title).replace('-', '_')}"
        groups = [n for n in plan.nodes if n.note_role == "group_index"]
        parent = groups[-1] if groups else root
        folder = Path(parent.proposed_path).parent.as_posix()
        new_node = TopicNode(
            concept_id=new_cid,
            title=new_title,
            parent_id=parent.concept_id,
            proposed_path=f"{folder}/{_safe_filename(new_title)}.md",
            note_role="child",
            template_plan={"master": "M1", "depth": "standard"},
        )
        parent.child_ids.append(new_cid)
        return _rebuild_plan_stats(plan, [*plan.nodes, new_node])

    return plan


def _rebuild_plan_stats(plan: NoteCollectionPlan, nodes: list[TopicNode]) -> NoteCollectionPlan:
    groups = [n for n in nodes if n.note_role == "group_index"]
    children = [n for n in nodes if n.note_role == "child"]
    learning = [n.concept_id for n in children]
    gen = [*learning, *[g.concept_id for g in groups], plan.root_topic_id]
    return NoteCollectionPlan(
        collection_id=plan.collection_id,
        title=plan.title,
        root_topic_id=plan.root_topic_id,
        organization=plan.organization,
        nodes=nodes,
        planned_paths=[n.proposed_path for n in nodes],
        learning_order=learning,
        generation_order=gen,
        scope_summary={
            **plan.scope_summary,
            "root_indexes": 1 if any(n.note_role == "root_index" for n in nodes) else 0,
            "topic_groups": len(groups),
            "child_notes": len(children),
            "total_notes": len(nodes),
        },
    )


def respond_to_session(
    state: NoteInteractionState,
    user_reply: str,
    *,
    source_sections: list[dict[str, str]] | None = None,
    root: Path = REPO_ROOT,
) -> dict[str, Any]:
    """Advance the multi-turn interactive state machine without requiring the user to repeat /scribe-notes."""
    reply = user_reply.strip()
    low = reply.lower()

    # Cancellation / start over (Section 10.5)
    if re.fullmatch(r"(?:cancel|stop|abort|never\s*mind|start\s+over)\.?", low):
        state.stage = "CANCELLED"
        return {
            "stage": state.stage,
            "message": "Cancelled the pending /scribe-notes request. Start a new request whenever ready.",
            "ready_to_generate": False,
            "state": state,
        }

    # New /scribe-notes invocation replaces pending session cleanly (Section 10.4)
    if reply.lower().startswith("/scribe-notes"):
        new_state = start_notes_session(reply, root=root)
        return {
            "stage": new_state.stage,
            "message": format_configuration_prompt(new_state),
            "ready_to_generate": False,
            "state": new_state,
        }

    # Stage 1: Supplying missing topic after bare /scribe-notes
    if state.stage == "AWAITING_TOPIC":
        new_state = start_notes_session(f"/scribe-notes {reply}", root=root)
        new_state.request_id = state.request_id
        return {
            "stage": new_state.stage,
            "message": format_configuration_prompt(new_state),
            "ready_to_generate": False,
            "state": new_state,
        }

    # Stage 2: Configuration resolution (or mid-flow preference correction!)
    if state.stage == "AWAITING_CONFIGURATION":
        prefs = _parse_user_preferences(reply, state)
        state.resolved_preferences = prefs
        state.stage = "CONFIGURATION_RESOLVED"
        eff_sections = source_sections
        if not eff_sections:
            bound_secs = [
                {"title": str(b["section"]), "source": str(b.get("source", "supplied_source"))}
                for b in (state.original_intent.source_bindings or [])
                if isinstance(b, dict) and b.get("section")
            ]
            if bound_secs:
                eff_sections = bound_secs
        plan = plan_note_collection(
            state.original_intent.topic or "Untitled",
            prefs,
            source_sections=eff_sections,
        )
        state.collection_plan = plan
        # Substantial collections (>= 4 notes) pause for user preview/approval (Part 18)
        if plan.organization == "hierarchical_collection" and len(plan.nodes) >= 4:
            state.stage = "AWAITING_PLAN_APPROVAL"
            return {
                "stage": state.stage,
                "message": format_collection_preview(plan, prefs),
                "ready_to_generate": False,
                "state": state,
            }
        state.stage = "COLLECTION_PLAN_READY"
        return {
            "stage": state.stage,
            "message": f"Configuration confirmed ({MASTER_READABLE_NAMES[prefs.master]}, {prefs.depth}, {plan.organization.replace('_', ' ')}). Ready to generate {len(plan.nodes)} note(s).",
            "ready_to_generate": True,
            "state": state,
        }

    # Stage 3: Collection preview approval, outline revision, or preference correction
    if state.stage == "AWAITING_PLAN_APPROVAL" and state.collection_plan and state.resolved_preferences:
        if re.search(r"\b(?:proceed|approve|looks?\s+good|yes|generate|go\s+ahead|confirm)\b", low):
            state.stage = "COLLECTION_PLAN_READY"
            return {
                "stage": state.stage,
                "message": f"Plan approved. Ready to generate {len(state.collection_plan.nodes)} note(s).",
                "ready_to_generate": True,
                "state": state,
            }
        if re.search(r"\bactually\b|\bchange\s+to\b|\bmake\s+(?:them|it)\b", low):
            state.resolved_preferences = _parse_user_preferences(reply, state)
            return {
                "stage": state.stage,
                "message": "Updated preferences.\n\n" + format_collection_preview(state.collection_plan, state.resolved_preferences),
                "ready_to_generate": False,
                "state": state,
            }
        updated_plan = modify_collection_plan(state.collection_plan, reply)
        state.collection_plan = updated_plan
        return {
            "stage": state.stage,
            "message": "Updated collection outline:\n\n" + format_collection_preview(updated_plan, state.resolved_preferences),
            "ready_to_generate": False,
            "state": state,
        }

    return {"stage": state.stage, "message": f"Session is in stage '{state.stage}'.", "ready_to_generate": state.stage == "COLLECTION_PLAN_READY", "state": state}


def save_session_state(vault: Path, state: NoteInteractionState) -> Path:
    """Persist a pending session state safely inside <vault>/.scriptorium/sessions/."""
    sessions_dir = Path(vault) / ".scriptorium" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    path = sessions_dir / f"{state.request_id}.json"
    path.write_text(json.dumps(state.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_session_state(vault: Path, request_id: str) -> NoteInteractionState:
    """Load a persisted NoteInteractionState from <vault>/.scriptorium/sessions/<request_id>.json."""
    path = Path(vault) / ".scriptorium" / "sessions" / f"{request_id}.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    orig = NoteRequestIntent(**raw["original_intent"])
    rec = NoteConfigurationRecommendation(**raw["recommendation"])
    prefs = ResolvedNotePreferences(**raw["resolved_preferences"]) if raw.get("resolved_preferences") else None
    plan_raw = raw.get("collection_plan")
    plan = None
    if plan_raw:
        nodes = [TopicNode(**n) for n in plan_raw.get("nodes", [])]
        plan = NoteCollectionPlan(
            collection_id=plan_raw["collection_id"],
            title=plan_raw["title"],
            root_topic_id=plan_raw["root_topic_id"],
            organization=plan_raw["organization"],
            nodes=nodes,
            planned_paths=plan_raw.get("planned_paths", []),
            learning_order=plan_raw.get("learning_order", []),
            generation_order=plan_raw.get("generation_order", []),
            scope_summary=plan_raw.get("scope_summary", {}),
        )
    return NoteInteractionState(
        request_id=raw["request_id"],
        stage=raw["stage"],
        original_intent=orig,
        recommendation=rec,
        questions_asked=raw.get("questions_asked", []),
        resolved_preferences=prefs,
        collection_plan=plan,
        question_trace=raw.get("question_trace", []),
        persistence_mode=raw.get("persistence_mode", "in_memory_or_vault_session"),
    )
