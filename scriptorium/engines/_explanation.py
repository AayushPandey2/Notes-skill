"""Explanation Intelligence System (EIS-01 through EIS-06) inside Tutor / Pedagogy.

Provides one unified, source-policy-aware, domain-independent ExplanationBlueprint
and coordinated explanation-design mechanisms:
  - EIS-01: Explanatory Spine Construction & Transition Validation
  - EIS-02: Central Question Reconstruction & Selective Question Anticipation
  - EIS-03: Causal Mechanism & Mathematical Derivation Motivation
  - EIS-04: Applicability Boundary & Conceptual Contrast Engineering
  - EIS-05: Variable Roles, Invariants, and Algorithm State Narration
  - EIS-06: Retrieval Cue Engineering & Reconstruction-Based Summaries
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import re
from typing import Any, Callable

from scriptorium.engines.vault import build_obsidian_properties, render_note_with_properties
from scriptorium.layout import canonical_note_type
from scriptorium.models import parse_note, slugify

BLUEPRINT_SCHEMA_VERSION = "1.0"

MASTER_EIS_ACTIVATION: dict[str, dict[str, str]] = {
    "M1": {
        "eis_01_spine": "deep",
        "eis_02_questions": "deep",
        "eis_03_motivation": "deep",
        "eis_04_boundaries": "deep",
        "eis_05_state": "contextual",
        "eis_06_retrieval": "standard",
        "eis_07_reader_review": "deep",
    },
    "M2": {
        "eis_01_spine": "standard",
        "eis_02_questions": "standard",
        "eis_03_motivation": "standard",
        "eis_04_boundaries": "standard",
        "eis_05_state": "contextual",
        "eis_06_retrieval": "standard",
        "eis_07_reader_review": "standard",
    },
    "M3": {
        "eis_01_spine": "lightweight",
        "eis_02_questions": "lightweight",
        "eis_03_motivation": "disabled",
        "eis_04_boundaries": "standard",
        "eis_05_state": "lightweight",
        "eis_06_retrieval": "lightweight",
        "eis_07_reader_review": "standard",
    },
    "M4": {
        "eis_01_spine": "standard",
        "eis_02_questions": "lightweight",
        "eis_03_motivation": "deep",
        "eis_04_boundaries": "standard",
        "eis_05_state": "standard",
        "eis_06_retrieval": "standard",
        "eis_07_reader_review": "standard",
    },
    "M5": {
        "eis_01_spine": "standard",
        "eis_02_questions": "standard",
        "eis_03_motivation": "deep",
        "eis_04_boundaries": "deep",
        "eis_05_state": "deep",
        "eis_06_retrieval": "standard",
        "eis_07_reader_review": "standard",
    },
    "M6": {
        "eis_01_spine": "lightweight",
        "eis_02_questions": "standard",
        "eis_03_motivation": "disabled",
        "eis_04_boundaries": "standard",
        "eis_05_state": "disabled",
        "eis_06_retrieval": "lightweight",
        "eis_07_reader_review": "standard",
    },
    "M7": {
        "eis_01_spine": "standard",
        "eis_02_questions": "lightweight",
        "eis_03_motivation": "standard",
        "eis_04_boundaries": "standard",
        "eis_05_state": "contextual",
        "eis_06_retrieval": "deep",
        "eis_07_reader_review": "standard",
    },
}

DOMAIN_SPINE_TEMPLATES: dict[str, tuple[str, ...]] = {
    "mathematical": ("problem", "relevant_property", "transformation", "result", "conditions"),
    "computational": ("task", "constraint", "algorithmic_insight", "procedure", "output"),
    "scientific": ("phenomenon", "model_assumptions", "governing_principle", "prediction", "limitations"),
    "historical": ("historical_question", "context", "developments", "competing_interpretations", "consequences"),
    "conceptual": ("question", "definition", "distinction", "implication", "application"),
}

INTERNAL_BLUEPRINT_HEADINGS_RE = re.compile(
    r"^#{1,6}\s+(?:Central Question|Starting Problem|Necessary Insight|Explanatory Spine|"
    r"Anticipated Questions|Causal Mechanism|Reader Simulation|Cognitive Friction|EIS-\d+)\b",
    re.M | re.I,
)

# Structural/syntactic procedural cues only (zero topic-specific lessons)
PROCEDURAL_CONCEPT_KEYWORDS = re.compile(
    r"\b(?:algorithm|algorithms|search|sort|sorting|recursion|recursive|iteration|iterative|"
    r"loop|state\s+machine|protocol|traversal|solver|procedure|pipeline|scheduler|optimizer)\b",
    re.I,
)


@dataclass
class ExplanationBlueprint:
    """Unified, concept-aware, source-policy-aware explanation blueprint shared across EIS-01..EIS-07."""
    schema_version: str = BLUEPRINT_SCHEMA_VERSION
    concept_id: str = ""
    topic: str = ""
    domain: str = "conceptual"
    concept_type: str = "conceptual"
    context: dict[str, Any] = field(default_factory=dict)
    activation_levels: dict[str, str] = field(default_factory=dict)
    provenance_policy: dict[str, Any] = field(default_factory=dict)
    central_question: dict[str, Any] = field(default_factory=dict)
    explanatory_spine: dict[str, Any] = field(default_factory=dict)
    anticipated_questions: list[dict[str, Any]] = field(default_factory=list)
    mechanism: dict[str, Any] = field(default_factory=dict)
    mathematical_motivation: dict[str, Any] = field(default_factory=dict)
    boundaries: dict[str, Any] = field(default_factory=dict)
    contrasts: list[dict[str, str]] = field(default_factory=list)
    variable_roles: list[dict[str, Any]] = field(default_factory=list)
    execution_state: dict[str, Any] = field(default_factory=dict)
    retrieval: dict[str, Any] = field(default_factory=dict)
    reader_review: dict[str, Any] = field(default_factory=dict)
    conflict_resolutions: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _infer_concept_type(topic: str, explicit_type: str | None = None) -> str:
    """Infer structural pedagogical category from explicit type or generic structural keywords."""
    if explicit_type:
        low = explicit_type.strip().lower()
        if low in {"mathematical", "computational", "scientific", "historical", "conceptual", "definition", "algorithm"}:
            return low
    t = topic.lower()
    if PROCEDURAL_CONCEPT_KEYWORDS.search(t):
        return "algorithm"
    if re.search(r"\b(?:theorem|proof|lemma|equation|derivative|integral|inequality|identity|formula|calculus|algebra|geometry)\b", t):
        return "mathematical"
    if re.search(r"\b(?:experiment|phenomenon|law|reaction|cell|potential|thermodynamics|optics|biology|chemistry|physics|physiology)\b", t):
        return "scientific"
    if re.search(r"\b(?:history|historical|revolution|war|treaty|empire|dynasty|era|period|convention|system)\b", t):
        return "historical"
    return "conceptual"


def _domain_family(concept_type: str) -> str:
    return {
        "algorithm": "computational",
        "definition": "conceptual",
    }.get(concept_type, concept_type if concept_type in DOMAIN_SPINE_TEMPLATES else "conceptual")


def resolve_eis_activation(
    *,
    master: str = "M1",
    concept_type: str = "conceptual",
    complexity: str = "standard",
    source_mode: str = "adaptive",
    audience: str = "intermediate",
) -> dict[str, str]:
    """Resolve cost-aware adaptive activation levels (disabled/lightweight/standard/deep) for EIS-01..EIS-07."""
    base = dict(MASTER_EIS_ACTIVATION.get(master, MASTER_EIS_ACTIVATION["M1"]))

    is_procedural = concept_type in {"algorithm", "computational"}
    is_quantitative = concept_type in {"mathematical", "scientific"}
    if base["eis_05_state"] == "contextual":
        if is_procedural:
            base["eis_05_state"] = "deep"
        elif is_quantitative:
            base["eis_05_state"] = "standard"
        else:
            base["eis_05_state"] = "disabled"

    if complexity == "trivial" or concept_type == "definition":
        base["eis_01_spine"] = "lightweight"
        base["eis_02_questions"] = "lightweight"
        base["eis_03_motivation"] = "disabled"
        base["eis_05_state"] = "disabled"
        base["eis_06_retrieval"] = "lightweight"

    if concept_type in {"historical", "conceptual"} and base["eis_03_motivation"] == "deep":
        base["eis_03_motivation"] = "standard"

    if source_mode == "strict" and master == "M2":
        base["eis_01_spine"] = "standard"
    if audience == "advanced" and master == "M3":
        base["eis_02_questions"] = "disabled"

    return base


# ---------------------------------------------------------------------------
# EIS-01: Explanatory Spine Construction (Domain-Independent)
# ---------------------------------------------------------------------------

def construct_explanatory_spine(
    topic: str,
    *,
    concept_type: str = "conceptual",
    source_mode: str = "adaptive",
    preserve_source_order: bool = False,
    source_facts: list[str] | None = None,
    prerequisites: list[str] | None = None,
    activation: str = "standard",
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """EIS-01: Construct a dynamic, domain-independent reasoning spine from supplied context & facts."""
    family = _domain_family(concept_type)
    stages = list(DOMAIN_SPINE_TEMPLATES[family])
    provenance = "source_supported_inference" if source_mode == "strict" else "reasoned_exposition"
    rel_type = {
        "mathematical": "mathematical_consequence",
        "computational": "logical_implication",
        "scientific": "causal_mechanism",
        "historical": "historical_sequence",
        "conceptual": "conceptual_association",
    }[family]

    ctx_spine = (context or {}).get("spine") or {}
    spine = {
        "starting_problem": ctx_spine.get("starting_problem") or f"Identify the motivating problem or phenomenon addressed by {topic}.",
        "desired_outcome": ctx_spine.get("desired_outcome") or f"Establish a rigorous, verifiable understanding of {topic}.",
        "obstacle": ctx_spine.get("obstacle") or f"Surface intuition alone leaves the governing constraints and intermediate reasoning of {topic} unspecified.",
        "necessary_insight": ctx_spine.get("necessary_insight") or f"Formulate the central principle or invariant defining how {topic} works.",
        "mechanism": ctx_spine.get("mechanism") or f"Develop each intermediate transition connecting prerequisites to {topic} via {rel_type.replace('_', ' ')}.",
        "result": ctx_spine.get("result") or f"Establish the characteristic result or behavior of {topic}.",
        "implication": ctx_spine.get("implication") or f"Relate {topic} to adjacent concepts within verified applicability boundaries.",
        "required_insights": list(
            ctx_spine.get("required_insights")
            or [slugify(f)[:32].replace("-", "_") for f in (source_facts or [topic])[:5]]
        ),
        "relation_type": ctx_spine.get("relation_type") or rel_type,
        "domain_pattern": stages,
        "activation": activation,
        "preserve_source_order": preserve_source_order,
        "source_order_strategy": "local_transitions_only" if preserve_source_order else "dependency_aligned_spine",
        "prerequisites_honored": list(prerequisites or []),
        "provenance": "source_stated_explanation" if (source_mode == "strict" and source_facts) else provenance,
    }
    if source_facts:
        spine["source_sequence"] = list(source_facts)
    return spine


# ---------------------------------------------------------------------------
# EIS-02: Central Question Reconstruction & Question Anticipation
# ---------------------------------------------------------------------------

def plan_central_question_and_anticipation(
    topic: str,
    spine: dict[str, Any],
    *,
    master: str = "M1",
    concept_type: str = "conceptual",
    activation: str = "standard",
    context: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """EIS-02: Reconstruct the central guiding question and selective anticipated reader questions."""
    key = slugify(topic).replace("-", "_")
    ctx = context or {}
    q_text = ctx.get("central_question") or f"What core problem does {topic} address, how does its mechanism operate step by step, and under what conditions does it apply?"

    supplied_qs = ctx.get("anticipated_questions")
    if isinstance(supplied_qs, list) and supplied_qs:
        anticipated = [dict(q) for q in supplied_qs]
    else:
        anticipated = [
            {"question_id": "why_needed", "question": f"Why is {topic} necessary, and what limitation does it overcome?", "concept": key, "priority": 1, "stage": "core", "render": "implicit"},
            {"question_id": "how_works", "question": f"How does each intermediate step of {topic} connect input assumptions to the outcome?", "concept": "mechanism", "priority": 2, "stage": "core", "render": "implicit"},
            {"question_id": "when_valid", "question": f"Under what boundary conditions does {topic} hold or fail?", "concept": "boundaries", "priority": 3, "stage": "limitations", "render": "implicit"},
        ]

    if activation == "disabled":
        anticipated = []
    elif activation == "lightweight" or master == "M3" or concept_type == "definition":
        anticipated = anticipated[:1]

    central = {
        "question": q_text,
        "what_is_investigated": topic,
        "what_counts_as_answer": spine.get("result", ""),
        "resolved_by": spine.get("mechanism", ""),
        "explicit_in_prose": master in {"M1", "M2"} and activation in {"standard", "deep"},
        "activation": activation,
    }
    return central, anticipated


# ---------------------------------------------------------------------------
# EIS-03: Causal Mechanism & Mathematical Derivation Motivation
# ---------------------------------------------------------------------------

def plan_mechanism_and_motivation(
    topic: str,
    *,
    concept_type: str = "conceptual",
    source_mode: str = "adaptive",
    activation: str = "standard",
    context: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """EIS-03: Plan causal/logical mechanism separately from mathematical derivation motivation."""
    family = _domain_family(concept_type)
    causality_justified = family in {"scientific", "computational"}
    if activation == "disabled":
        return (
            {"applicable": False, "type": family, "causality_justified": causality_justified},
            {"enabled": False, "steps": []},
        )

    ctx = context or {}
    ctx_mech = ctx.get("mechanism") or {}
    ctx_motiv = ctx.get("mathematical_motivation") or {}
    is_math = family in {"mathematical", "scientific"} or bool(ctx_motiv.get("steps"))

    mech = {
        "applicable": ctx_mech.get("applicable", family != "historical"),
        "type": ctx_mech.get("type", family),
        "causality_justified": ctx_mech.get("causality_justified", causality_justified),
        "relation_basis": ctx_mech.get("relation_basis", "historical_evidence_and_interpretation" if family == "historical" else family),
        "inputs": list(ctx_mech.get("inputs") or []),
        "relevant_conditions": list(ctx_mech.get("relevant_conditions") or []),
        "operations": list(ctx_mech.get("operations") or []),
        "intermediate_states": list(ctx_mech.get("intermediate_states") or []),
        "outputs": list(ctx_mech.get("outputs") or []),
        "limiting_factors": list(
            ctx_mech.get("limiting_factors")
            or (["evidence uncertainty and competing scholarly interpretations"] if family == "historical" else [])
        ),
    }
    motiv = {
        "enabled": is_math and activation in {"standard", "deep"},
        "central_operation": ctx_motiv.get("central_operation", ""),
        "local_vs_global_note": ctx_motiv.get("local_vs_global_note", ""),
        "steps": [dict(s) for s in (ctx_motiv.get("steps") or [])],
        "source_policy_guard": (
            "Only derive steps supported by the supplied source; never import external theorems."
            if source_mode == "strict"
            else "standard"
        ),
    }
    return mech, motiv


# ---------------------------------------------------------------------------
# EIS-04: Applicability Boundaries & Conceptual Contrasts
# ---------------------------------------------------------------------------

def plan_boundaries_and_contrasts(
    topic: str,
    *,
    concept_type: str = "conceptual",
    complexity: str = "standard",
    activation: str = "standard",
    context: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """EIS-04: Specify applicability conditions, limits, and caller-supplied or derived contrasts."""
    if activation == "disabled":
        return {"enabled": False}, []

    ctx = context or {}
    ctx_b = ctx.get("boundaries") or {}
    if ctx_b:
        boundaries = {"enabled": True, **ctx_b}
    elif concept_type == "definition" or complexity == "trivial":
        boundaries = {
            "enabled": True,
            "minimal_caveats_only": True,
            "required_conditions": [],
            "invalid_generalizations": [],
        }
    else:
        boundaries = {
            "enabled": True,
            "domain_of_use": [topic],
            "required_conditions": [f"Verify stated assumptions before applying {topic}."],
            "known_limitations": [],
            "invalid_generalizations": [],
        }

    contrasts = [dict(c) for c in (ctx.get("contrasts") or [])]
    return boundaries, contrasts


# ---------------------------------------------------------------------------
# EIS-05: Variable Roles, Invariants & Algorithm State Narration
# ---------------------------------------------------------------------------

def plan_variable_and_state_reasoning(
    topic: str,
    *,
    concept_type: str = "conceptual",
    activation: str = "contextual",
    context: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """EIS-05: Classify operational variable roles, valid invariants, and verified traces.

    Never forces execution traces or invented invariants onto nonprocedural topics.
    """
    if activation == "disabled":
        return [], {"applicable": False, "invariant": {"applicable": False}}

    ctx = context or {}
    variables = [dict(v) for v in (ctx.get("variables") or [])]
    supplied_state = ctx.get("state_model")
    if isinstance(supplied_state, dict) and supplied_state:
        return variables, dict(supplied_state)

    is_procedural = concept_type in {"algorithm", "computational"} or bool(PROCEDURAL_CONCEPT_KEYWORDS.search(topic))
    if not is_procedural:
        return variables, {"applicable": False, "invariant": {"applicable": False}}

    return variables, {
        "applicable": True,
        "state_variables": [v.get("symbol", "") for v in variables if v.get("symbol")],
        "invariant": {"applicable": False},
        "example_trace": [],
    }


# ---------------------------------------------------------------------------
# EIS-06: Retrieval Cues & Reconstruction Summaries
# ---------------------------------------------------------------------------

def build_retrieval_cues(
    topic: str,
    spine: dict[str, Any],
    boundaries: dict[str, Any],
    *,
    master: str = "M1",
    activation: str = "standard",
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """EIS-06: Construct compact reasoning-preserving retrieval cues and reconstruction summaries."""
    key = slugify(topic).replace("-", "_")
    if activation == "disabled":
        return {"enabled": False, "cues": [], "reconstruction_chain": [], "summary": ""}

    ctx_ret = (context or {}).get("retrieval") or {}
    conds = list(ctx_ret.get("critical_conditions") or boundaries.get("required_conditions") or [])
    cues = list(ctx_ret.get("cues") or ["problem", "insight", "mechanism", "conditions"])
    chain = list(ctx_ret.get("reconstruction_chain") or ["identify_problem", "apply_insight", "execute_mechanism", "verify_conditions"])
    summary = str(
        ctx_ret.get("summary")
        or f"{spine.get('starting_problem', '')} {spine.get('necessary_insight', '')} {spine.get('mechanism', '')} {spine.get('result', '')}"
    ).strip()

    leak_protected = master == "M6"
    return {
        "enabled": True,
        "concept_id": key,
        "activation": activation,
        "internal_only": leak_protected,
        "cues": cues,
        "reconstruction_chain": chain,
        "critical_conditions": conds,
        "summary": "" if leak_protected else summary,
        "claims_measured_retention": False,
    }


# ---------------------------------------------------------------------------
# Unified Blueprint Builder & Natural-Prose Composition
# ---------------------------------------------------------------------------

def build_explanation_blueprint(
    topic: str,
    *,
    concept_id: str | None = None,
    master: str = "M1",
    concept_type: str | None = None,
    complexity: str = "standard",
    source_mode: str = "adaptive",
    preserve_source_order: bool = False,
    audience: str = "intermediate",
    source_facts: list[str] | None = None,
    prerequisites: list[str] | None = None,
    context: dict[str, Any] | None = None,
) -> ExplanationBlueprint:
    """Build one coordinated ExplanationBlueprint integrating EIS-01 through EIS-07."""
    ctype = _infer_concept_type(topic, concept_type)
    family = _domain_family(ctype)
    cid = concept_id or f"{family}.{slugify(topic).replace('-', '_')}"
    activations = resolve_eis_activation(
        master=master,
        concept_type=ctype,
        complexity=complexity,
        source_mode=source_mode,
        audience=audience,
    )

    conflicts: list[dict[str, str]] = []
    if prerequisites and preserve_source_order:
        conflicts.append({
            "conflict": "prerequisites_vs_source_order",
            "resolution": "Preserve major source sequence and place concise local prerequisite reminders before first use.",
        })
    if master == "M3" and activations["eis_02_questions"] in {"lightweight", "disabled"}:
        conflicts.append({
            "conflict": "question_anticipation_vs_cheat_sheet_density",
            "resolution": "Keep anticipated questions implicit so M3 remains compact and scannable.",
        })
    if source_mode == "strict":
        conflicts.append({
            "conflict": "derivation_motivation_vs_strict_source_policy",
            "resolution": "Restrict factual claims and derivations strictly to supplied source content; allow only editorial transitions.",
        })

    spine = construct_explanatory_spine(
        topic,
        concept_type=ctype,
        source_mode=source_mode,
        preserve_source_order=preserve_source_order,
        source_facts=source_facts,
        prerequisites=prerequisites,
        activation=activations["eis_01_spine"],
        context=context,
    )
    central_q, anticipated_qs = plan_central_question_and_anticipation(
        topic, spine, master=master, concept_type=ctype, activation=activations["eis_02_questions"], context=context
    )
    mechanism, math_motiv = plan_mechanism_and_motivation(
        topic, concept_type=ctype, source_mode=source_mode, activation=activations["eis_03_motivation"], context=context
    )
    boundaries, contrasts = plan_boundaries_and_contrasts(
        topic, concept_type=ctype, complexity=complexity, activation=activations["eis_04_boundaries"], context=context
    )
    var_roles, exec_state = plan_variable_and_state_reasoning(
        topic, concept_type=ctype, activation=activations["eis_05_state"], context=context
    )
    retrieval = build_retrieval_cues(
        topic, spine, boundaries, master=master, activation=activations["eis_06_retrieval"], context=context
    )

    return ExplanationBlueprint(
        concept_id=cid,
        topic=topic,
        domain=family,
        concept_type=ctype,
        context={
            "selected_master": master,
            "source_mode": source_mode,
            "preserve_source_order": preserve_source_order,
            "audience_depth": audience,
            "complexity": complexity,
        },
        activation_levels=activations,
        provenance_policy={
            "source_mode": source_mode,
            "external_facts_permitted": source_mode != "strict",
            "editorial_transitions_permitted": True,
        },
        central_question=central_q,
        explanatory_spine=spine,
        anticipated_questions=anticipated_qs,
        mechanism=mechanism,
        mathematical_motivation=math_motiv,
        boundaries=boundaries,
        contrasts=contrasts,
        variable_roles=var_roles,
        execution_state=exec_state,
        retrieval=retrieval,
        reader_review={
            "enabled": activations["eis_07_reader_review"] != "disabled",
            "simulated_reader": audience,
            "hypothetical_review": True,
        },
        conflict_resolutions=conflicts,
    )


def compose_explanation_note(
    blueprint: ExplanationBlueprint,
    *,
    source_facts: list[str] | None = None,
    domain_override: str | None = None,
    master_topic_override: str | None = None,
) -> str:
    """Compose a natural-prose Markdown note with mandatory Obsidian Properties from an ExplanationBlueprint.

    Never exposes internal blueprint role names as visible headings.
    """
    master = blueprint.context.get("selected_master", "M1")
    source_mode = blueprint.context.get("source_mode", "adaptive")
    preserve_order = bool(blueprint.context.get("preserve_source_order"))
    note_type = canonical_note_type({
        "M1": "deep-notes",
        "M2": "study-notes",
        "M3": "quick-reference",
        "M4": "worked-solutions",
        "M5": "implementation-guide",
        "M6": "assessment",
        "M7": "synthesis-revision",
    }.get(master, "deep-notes"))

    props = build_obsidian_properties(
        topic=blueprint.topic,
        note_type=note_type,
        domain=domain_override,
        master_topic=master_topic_override,
        concept_ids=[blueprint.concept_id],
        source_mode=source_mode,
    )

    spine = blueprint.explanatory_spine
    lines: list[str] = [f"# {blueprint.topic}", ""]

    if master == "M3":
        lines.append("## Core Reference")
        if blueprint.variable_roles:
            lines.append("| Symbol | Meaning | Operational Role |")
            lines.append("|---|---|---|")
            for vr in blueprint.variable_roles:
                lines.append(f"| `{vr['symbol']}` | {vr['meaning']} | {vr['effect']} |")
            lines.append("")
        conds = blueprint.boundaries.get("required_conditions") or []
        if conds:
            lines.append("## Applicability Conditions")
            for c in conds:
                lines.append(f"- {c}")
            lines.append("")
        if blueprint.contrasts:
            c0 = blueprint.contrasts[0]
            lines.append("## Key Distinction")
            lines.append(f"- **{c0['concept_a']} vs {c0['concept_b']}**: {c0['distinction']}")
            lines.append("")
        if blueprint.retrieval.get("cues"):
            lines.append("## Recall Cues")
            lines.append("- " + " → ".join(blueprint.retrieval["cues"]))
            lines.append("")
        return render_note_with_properties(props, "\n".join(lines))

    if preserve_order and source_facts:
        lines.append("## 1. Source Context & Overview")
        lines.append(
            "> [!info] Source & Scope Context\n"
            f"> - **Source Policy**: `{source_mode}` (preserves original sequence; no external facts added)"
        )
        lines.append("")
        lines.append("## 2. Sequential Development")
        for idx, fact in enumerate(source_facts, 1):
            rendered_fact = fact if idx == 1 else f"Building directly on the preceding point: {fact}"
            lines.append(f"### 2.{idx} Step {idx}")
            lines.append(rendered_fact)
            lines.append("")
        if blueprint.retrieval.get("summary") and source_mode != "strict":
            lines.append("## 3. Synthesis")
            lines.append(blueprint.retrieval["summary"])
            lines.append("")
        return render_note_with_properties(props, "\n".join(lines))

    lines.append("## Motivation and Core Idea")
    opening = f"{spine.get('starting_problem', '')} {spine.get('obstacle', '')}".strip()
    if blueprint.central_question.get("explicit_in_prose") and blueprint.central_question.get("question"):
        opening += f" This leads naturally to a guiding question: *{blueprint.central_question['question']}*"
    lines.append(opening)
    lines.append("")
    lines.append(f"{spine.get('necessary_insight', '')} {spine.get('mechanism', '')} {spine.get('result', '')}".strip())
    lines.append("")

    steps = blueprint.mathematical_motivation.get("steps") or []
    if steps:
        lines.append("## Mathematical Motivation")
        for st in steps:
            lines.append(
                f"To {st['goal'][0].lower() + st['goal'][1:]} apply `{st['operation'].replace('_', ' ')}` "
                f"using {st['mathematical_basis'].replace('_', ' ')}: `{st['result']}`. "
                f"{st['interpretation']} {st['next_purpose']}"
            )
            lines.append("")
        if blueprint.mathematical_motivation.get("local_vs_global_note"):
            lines.append(blueprint.mathematical_motivation["local_vs_global_note"])
            lines.append("")

    if blueprint.variable_roles:
        lines.append("## Roles of Key Quantities")
        lines.append("| Symbol | Meaning | Operational Role | Effect of Change |")
        lines.append("|---|---|---|---|")
        for vr in blueprint.variable_roles:
            lines.append(f"| `{vr['symbol']}` | {vr['meaning']} | {vr['role']} | {vr['effect']} |")
        lines.append("")

    exec_st = blueprint.execution_state
    if exec_st.get("applicable") and exec_st.get("example_trace"):
        lines.append("## Step-by-Step State Evolution")
        if exec_st.get("invariant", {}).get("applicable"):
            lines.append(f"**Preserved Invariant:** {exec_st['invariant']['statement']}")
            lines.append("")
        cols = list(exec_st["example_trace"][0].keys())
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("|" + "|".join("---" for _ in cols) + "|")
        for row in exec_st["example_trace"]:
            lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
        lines.append("")

    req_conds = blueprint.boundaries.get("required_conditions") or []
    lims = blueprint.boundaries.get("known_limitations") or []
    if (req_conds or lims or blueprint.contrasts) and not blueprint.boundaries.get("minimal_caveats_only"):
        lines.append("## Applicability Conditions and Distinctions")
        for c in req_conds:
            lines.append(f"- **Required condition:** {c}")
        for lim in lims:
            lines.append(f"- **Limitation:** {lim}")
        for con in blueprint.contrasts:
            lines.append(
                f"- **{con['concept_a']} vs. {con['concept_b']}:** {con['distinction']} "
                f"*(Example: {con['discriminating_example']})*"
            )
        lines.append("")

    if blueprint.retrieval.get("enabled") and blueprint.retrieval.get("summary") and not blueprint.retrieval.get("internal_only"):
        lines.append("## Reconstructing the Reasoning")
        lines.append("**Key cues:** " + " → ".join(blueprint.retrieval["cues"]))
        lines.append("")
        lines.append(blueprint.retrieval["summary"])
        lines.append("")

    return render_note_with_properties(props, "\n".join(lines))


# ---------------------------------------------------------------------------
# EIS-01..EIS-06 Deterministic Validators
# ---------------------------------------------------------------------------

def validate_explanation_structure(
    note_text: str,
    blueprint: ExplanationBlueprint,
) -> list[dict[str, Any]]:
    """Run deterministic EIS-01..EIS-06 structural & domain-correctness checks."""
    issues: list[dict[str, Any]] = []
    parsed = parse_note(note_text)
    body = parsed.body
    lowered = body.lower()

    if m := INTERNAL_BLUEPRINT_HEADINGS_RE.search(body):
        issues.append({
            "code": "EIS-COMP-001",
            "severity": "major",
            "concept_id": blueprint.concept_id,
            "location": "headings",
            "description": f"Internal blueprint heading exposed in final note: '{m.group(0)}'.",
            "recommended_repair": "replace_internal_heading_with_natural_prose_heading",
        })

    src_seq = blueprint.explanatory_spine.get("source_sequence") or []
    if blueprint.explanatory_spine.get("preserve_source_order") and len(src_seq) >= 2:
        positions = [lowered.find(s[:24].lower()) for s in src_seq if s.strip()]
        found_pos = [p for p in positions if p >= 0]
        if found_pos != sorted(found_pos):
            issues.append({
                "code": "EIS-SPINE-003",
                "severity": "critical",
                "concept_id": blueprint.concept_id,
                "location": "section_order",
                "description": "Strict source order was violated by reordering source sequence.",
                "recommended_repair": "restore_source_sequence_with_local_transitions",
            })

    if blueprint.explanatory_spine.get("relation_type") in {"conceptual_association", "historical_sequence"}:
        if re.search(r"\b(?:proves?\s+causation|directly\s+caused\s+by\s+correlation|inevitably\s+caused)\b", body, re.I):
            issues.append({
                "code": "EIS-SPINE-002",
                "severity": "major",
                "concept_id": blueprint.concept_id,
                "location": "transitions",
                "description": "Unsupported causal claim introduced on a non-causal or contested topic.",
                "recommended_repair": "replace_causal_claim_with_association_or_evidence_qualified_language",
            })

    q_headings = [s.heading for s in parsed.sections if s.heading.strip().endswith("?")]
    if len(q_headings) >= 4 and len(body.split()) < 220:
        issues.append({
            "code": "EIS-Q-002",
            "severity": "minor",
            "concept_id": blueprint.concept_id,
            "location": "headings",
            "description": f"Excessive FAQ-style question headings ({len(q_headings)}) in a short note.",
            "recommended_repair": "consolidate_questions_into_connected_prose",
        })

    if re.search(r"(?:^|[.!?]\s+)(?:Now\s+differentiate\s+both\s+sides|Substitute\s+the\s+values)\.", body, re.I):
        issues.append({
            "code": "EIS-MOTIV-001",
            "severity": "major",
            "concept_id": blueprint.concept_id,
            "location": "derivation",
            "description": "Unmotivated algebraic narration ('Now differentiate both sides' / 'Substitute the values') lacks purpose.",
            "recommended_repair": "state_operation_purpose_before_step",
        })
    if re.search(r"\balways\s+(?:converges\s+to|finds)\s+(?:the\s+)?global\s+minimum\b", body, re.I) and not re.search(r"\bconvex|smoothness|assump|provided|if\b", body, re.I):
        issues.append({
            "code": "EIS-MOTIV-002",
            "severity": "critical",
            "concept_id": blueprint.concept_id,
            "location": "guarantees",
            "description": "Claims universal global optimality without stating required hypotheses or conditions.",
            "recommended_repair": "qualify_optimality_with_explicit_assumptions",
        })
    if re.search(r"\(a\s*\+\s*b\)\^2\s*=\s*a\^2\s*\+\s*b\^2", body, re.I):
        issues.append({
            "code": "EIS-MOTIV-003",
            "severity": "critical",
            "concept_id": blueprint.concept_id,
            "location": "derivation",
            "description": "Invalid algebraic shortcut detected: (a + b)^2 != a^2 + b^2.",
            "recommended_repair": "correct_algebraic_identity",
        })

    if re.search(r"\balways\s+(?:finds|works|holds|succeeds)\b", body, re.I) and not re.search(
        r"\b(?:assume|assumption|precondition|condition|provided|sorted|ordered|monotonic|when|if|requires)\b", body, re.I
    ):
        issues.append({
            "code": "EIS-BOUND-001",
            "severity": "critical",
            "concept_id": blueprint.concept_id,
            "location": "applicability",
            "description": "Makes an unconditional universal claim ('always finds/works/holds') without stating required preconditions.",
            "recommended_repair": "state_explicit_preconditions_and_applicability_boundaries",
        })

    if not blueprint.execution_state.get("applicable"):
        if re.search(r"\bLoop\s+Invariant\b|\bIteration\s+\|\s+State\b", body, re.I):
            issues.append({
                "code": "EIS-STATE-003",
                "severity": "minor",
                "concept_id": blueprint.concept_id,
                "location": "state_trace",
                "description": "Forced procedural execution trace or loop invariant onto a nonprocedural concept.",
                "recommended_repair": "remove_artificial_procedural_trace",
            })

    recap_heads = [s.heading for s in parsed.sections if re.search(r"\b(?:summary|summaries|takeaways?|recap|key\s+points)\b", s.heading, re.I)]
    if len(recap_heads) >= 3:
        issues.append({
            "code": "EIS-RET-003",
            "severity": "minor",
            "concept_id": blueprint.concept_id,
            "location": "summaries",
            "description": f"Summary inflation detected ({len(recap_heads)} redundant recap sections: {recap_heads}).",
            "recommended_repair": "consolidate_into_single_reconstruction_summary",
        })

    return issues


def verify_numerical_trace(
    trace: list[dict[str, Any]],
    *,
    value_checks: dict[str, str] | None = None,
    recurrence_checks: dict[str, str] | None = None,
    monotonic_field: str | None = None,
    monotonic_direction: str = "nonincreasing",
    shrinking_bounds: tuple[str, str] | None = None,
    constants: dict[str, float] | None = None,
    step_validator: Callable[[int, dict[str, Any], dict[str, Any] | None], list[str]] | None = None,
) -> dict[str, Any]:
    """EIS-05: Deterministically verify arbitrary numerical/state traces using supplied equations & invariants.

    Domain-independent: validates caller-supplied formulas (`value_checks`), transition recurrences
    (`recurrence_checks` where `prev_<var>` references the previous row), monotonicity invariants,
    and interval-shrinking invariants via E5's safe AST arithmetic evaluator.
    """
    from scriptorium.engines.composition.checks import arithmetic

    errors: list[str] = []
    if not trace:
        return {"valid": False, "errors": ["Empty state trace."]}

    const_map = dict(constants or {})
    prev_val: float | None = None
    prev_span: int | None = None

    for idx, row in enumerate(trace):
        numeric_vars: dict[str, float] = {**const_map}
        for k, v in row.items():
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                numeric_vars[k] = float(v)
        if idx > 0:
            for k, v in trace[idx - 1].items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    numeric_vars[f"prev_{k}"] = float(v)

        for field_name, expr in (value_checks or {}).items():
            if field_name not in row:
                errors.append(f"Row {idx}: missing field '{field_name}'.")
                continue
            expected = round(arithmetic(expr, numeric_vars), 6)
            actual = float(row[field_name])
            if abs(actual - expected) > 1e-3:
                errors.append(f"Row {idx}: {field_name}={actual} disagrees with {expr}={expected}.")

        if idx > 0:
            for field_name, expr in (recurrence_checks or {}).items():
                if field_name not in row:
                    errors.append(f"Row {idx}: missing recurrence field '{field_name}'.")
                    continue
                expected = round(arithmetic(expr, numeric_vars), 6)
                actual = float(row[field_name])
                if abs(actual - expected) > 1e-3:
                    errors.append(f"Row {idx}: {field_name}={actual} disagrees with recurrence {expr}={expected}.")

        if monotonic_field and monotonic_field in row:
            cur_val = float(row[monotonic_field])
            if prev_val is not None:
                if monotonic_direction == "nonincreasing" and cur_val > prev_val + 1e-6:
                    errors.append(f"Row {idx}: monotonic nonincreasing invariant violated ({cur_val} > {prev_val}).")
                elif monotonic_direction == "nondecreasing" and cur_val < prev_val - 1e-6:
                    errors.append(f"Row {idx}: monotonic nondecreasing invariant violated ({cur_val} < {prev_val}).")
            prev_val = cur_val

        if shrinking_bounds:
            lo_k, hi_k = shrinking_bounds
            lo, hi = int(row[lo_k]), int(row[hi_k])
            if lo > hi:
                errors.append(f"Row {idx}: invalid interval [{lo}, {hi}].")
            span = hi - lo + 1
            if prev_span is not None and span >= prev_span:
                errors.append(f"Row {idx}: interval failed to shrink strictly ({span} >= {prev_span}).")
            prev_span = span

        if step_validator is not None:
            errors.extend(step_validator(idx, row, trace[idx - 1] if idx > 0 else None))

    return {"valid": not errors, "errors": errors}
