"""Explanation Intelligence System (EIS-01 through EIS-06) inside Engine E4 (Pedagogy).

Provides one unified, source-policy-aware ExplanationBlueprint and coordinated
explanation-design mechanisms:
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
from typing import Any

from scriptorium.engines.vault import build_obsidian_properties, render_note_with_properties
from scriptorium.layout import canonical_note_type
from scriptorium.models import parse_note, slugify

BLUEPRINT_SCHEMA_VERSION = "1.0"

# Master-aware activation matrix (Section 12.3 — adaptive starting defaults, not rigid quotas)
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

# Built-in domain-grounded contrast library for high-risk conceptual distinctions (EIS-04)
KNOWN_CONTRASTS: dict[str, list[dict[str, str]]] = {
    "gradient_descent": [
        {
            "concept_a": "Parameter",
            "concept_b": "Hyperparameter",
            "distinction": "Parameters (e.g., weights) are updated during optimization from data; hyperparameters (e.g., learning rate) configure the optimization procedure itself.",
            "discriminating_feature": "updated_by_optimizer_vs_configured_externally",
            "discriminating_example": "Weight θ is learned via updates; learning rate α controls step scale.",
        },
        {
            "concept_a": "Local Minimum",
            "concept_b": "Global Minimum",
            "distinction": "A local minimum has no lower objective value in a small neighborhood; a global minimum is lowest across the entire feasible domain.",
            "discriminating_feature": "neighborhood_vs_domain_wide_optimality",
            "discriminating_example": "Nonconvex neural loss surfaces have many local minima and saddle points, whereas convex quadratics make every local minimum global.",
        },
    ],
    "binary_search": [
        {
            "concept_a": "Binary Search",
            "concept_b": "Linear Search",
            "distinction": "Binary search halves a sorted candidate interval per comparison in O(log n) time; linear search scans sequentially in O(n) time without requiring sorted input.",
            "discriminating_feature": "ordering_precondition_enabling_half_elimination",
            "discriminating_example": "On an unsorted array [7, 2, 9, 4], binary search can discard the half containing 4, while linear search still finds it.",
        },
    ],
    "backpropagation": [
        {
            "concept_a": "Backpropagation",
            "concept_b": "Gradient Descent",
            "distinction": "Backpropagation computes parameter gradients efficiently via reverse-mode differentiation; gradient descent uses those gradients to update parameters.",
            "discriminating_feature": "gradient_computation_vs_parameter_update",
            "discriminating_example": "You can pair backpropagation with SGD, Adam, or L-BFGS because backpropagation only supplies derivatives.",
        },
    ],
    "chain_rule": [
        {
            "concept_a": "Chain Rule",
            "concept_b": "Product Rule",
            "distinction": "The chain rule differentiates function composition f(g(x)); the product rule differentiates multiplication f(x)·g(x).",
            "discriminating_feature": "nested_composition_vs_pointwise_multiplication",
            "discriminating_example": "d/dx sin(x^2) uses the chain rule (2x cos(x^2)), whereas d/dx [x·sin(x)] uses the product rule.",
        },
    ],
    "biot_savart_law": [
        {
            "concept_a": "Biot–Savart Law",
            "concept_b": "Ampère's Law",
            "distinction": "Biot–Savart integrates magnetic field contributions directly from arbitrary steady current geometries; Ampère's Law simplifies field calculation only when high symmetry yields a constant field along an Amperian loop.",
            "discriminating_feature": "general_integration_vs_symmetry_exploiting_circulation",
            "discriminating_example": "Finite straight wire segments require Biot–Savart integration, whereas an infinite solenoid yields directly to Ampère's Law.",
        },
    ],
    "correlation_and_causation": [
        {
            "concept_a": "Correlation",
            "concept_b": "Causation",
            "distinction": "Correlation measures statistical co-variation between variables; causation means intervening on one variable changes the distribution of another.",
            "discriminating_feature": "observational_co_variation_vs_interventional_effect",
            "discriminating_example": "Ice cream sales and drownings correlate via seasonal temperature (a confounder), without either causing the other.",
        },
    ],
    "recursion": [
        {
            "concept_a": "Recursion",
            "concept_b": "Iteration",
            "distinction": "Recursion expresses computation through self-referential subproblem calls managed on a call stack; iteration repeats state transitions explicitly in a loop with constant stack overhead.",
            "discriminating_feature": "call_stack_self_reference_vs_explicit_loop_state",
            "discriminating_example": "Tree traversal maps naturally to recursion, whereas simple array summation uses O(1) extra space with iteration.",
        },
    ],
}

# Built-in domain-grounded variable roles & procedural traces for core concepts (EIS-05)
PROCEDURAL_CONCEPT_KEYWORDS = re.compile(
    r"\b(?:binary\s+search|gradient\s+descent|backpropagation|recursion|quicksort|mergesort|"
    r"insertion\s+sort|sorting|dynamic\s+programming|dijkstra|bfs|dfs|pointer|algorithm|loop|"
    r"state\s+machine|iteration|newton|optimizer)\b",
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
    if explicit_type:
        low = explicit_type.strip().lower()
        if low in {"mathematical", "computational", "scientific", "historical", "conceptual", "definition", "algorithm"}:
            return low
    t = topic.lower()
    if re.search(r"\b(?:binary search|quicksort|mergesort|sort|recursion|dijkstra|algorithm|dynamic programming|backpropagation|pointer)\b", t):
        return "algorithm"
    if re.search(r"\b(?:chain rule|derivative|integral|eigenvalue|pca|gradient descent|linear regression|theorem|matrix|calculus)\b", t):
        return "mathematical"
    if re.search(r"\b(?:biot|savart|capacitance|stefan|boltzmann|induction|thermodynamics|optics|physics|quantum|biology|chemistry)\b", t):
        return "scientific"
    if re.search(r"\b(?:revolution|war|treaty|empire|history|historical|dynasty)\b", t):
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

    # Resolve contextual EIS-05 (variable/state reasoning) based on concept type
    is_procedural = concept_type in {"algorithm", "computational"}
    is_quantitative = concept_type in {"mathematical", "scientific"}
    if base["eis_05_state"] == "contextual":
        if is_procedural:
            base["eis_05_state"] = "deep"
        elif is_quantitative:
            base["eis_05_state"] = "standard"
        else:
            base["eis_05_state"] = "disabled"

    # Trivial or pure-definition concepts avoid heavy over-scaffolding
    if complexity == "trivial" or concept_type == "definition":
        base["eis_01_spine"] = "lightweight"
        base["eis_02_questions"] = "lightweight"
        base["eis_03_motivation"] = "disabled"
        base["eis_05_state"] = "disabled"
        base["eis_06_retrieval"] = "lightweight"

    # Historical/conceptual non-math concepts disable mathematical derivation motivation
    if concept_type in {"historical", "conceptual"} and base["eis_03_motivation"] == "deep":
        base["eis_03_motivation"] = "standard"

    # Strict source-only still permits local transitions and clarity checks, never external fabrication
    if source_mode == "strict" and master == "M2":
        base["eis_01_spine"] = "standard"
    if audience == "advanced" and master == "M3":
        base["eis_02_questions"] = "disabled"

    return base


# ---------------------------------------------------------------------------
# EIS-01: Explanatory Spine Construction
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
) -> dict[str, Any]:
    """EIS-01: Construct a domain-adapted reasoning spine without inventing false causality."""
    family = _domain_family(concept_type)
    stages = list(DOMAIN_SPINE_TEMPLATES[family])
    key = slugify(topic).replace("-", "_")
    provenance = "source_supported_inference" if source_mode == "strict" else "general_mathematical_consequence"

    # Domain-grounded canonical reasoning threads for well-known benchmark concepts
    presets: dict[str, dict[str, Any]] = {
        "gradient_descent": {
            "starting_problem": "A parameterized model yields measurable prediction error (loss), and we must choose parameter changes that reduce it.",
            "desired_outcome": "Iteratively move parameters toward lower loss values.",
            "obstacle": "Directly solving ∇J(θ) = 0 in closed form is generally intractable for nonlinear or high-dimensional objectives.",
            "necessary_insight": "The gradient ∇J(θ) gives local sensitivity and points in the direction of steepest local increase under Euclidean geometry.",
            "mechanism": "Step opposite the gradient scaled by a learning rate α: θ_{t+1} = θ_t - α∇J(θ_t), then recompute the gradient.",
            "result": "A local first-order decrease in loss for sufficiently small positive step size when ∇J(θ_t) ≠ 0.",
            "implication": "Repeated updates converge to a stationary point (or global minimum under convexity and smoothness bounds).",
            "required_insights": ["loss_objective", "local_sensitivity", "descent_direction", "step_size", "iteration"],
            "relation_type": "mathematical_consequence",
        },
        "binary_search": {
            "starting_problem": "Locating a target value in a large array via linear scan inspects up to n elements.",
            "desired_outcome": "Determine whether the target exists (and its index) in O(log n) comparisons.",
            "obstacle": "Without structure, inspecting one element reveals nothing about unvisited elements.",
            "necessary_insight": "Sorted order lets a single midpoint comparison rule out half of all remaining candidates.",
            "mechanism": "Maintain bounds [low, high], compare target to arr[mid], discard the impossible half, and repeat until found or low > high.",
            "result": "Each step halves the search interval, finishing in at most floor(log2 n) + 1 comparisons.",
            "implication": "Demonstrates how a data invariant (sorted order) transforms linear search into logarithmic elimination.",
            "required_insights": ["linear_cost", "sorted_order_invariant", "midpoint_comparison", "half_elimination", "termination"],
            "relation_type": "logical_implication",
        },
        "backpropagation": {
            "starting_problem": "Training a multi-layer neural network requires partial derivatives of the final loss with respect to every weight.",
            "desired_outcome": "Compute all parameter gradients in one backward sweep proportional to a single forward pass.",
            "obstacle": "Computing finite differences or independent forward-mode derivatives per weight scales linearly with parameter count.",
            "necessary_insight": "A network is a composition of differentiable layers, so the chain rule lets upstream loss sensitivities be reused backward.",
            "mechanism": "Run a forward pass caching intermediate activations, compute loss sensitivity at the output, and propagate local gradients backward via reverse-mode differentiation.",
            "result": "Exact parameter gradients for all layers in O(forward pass) time.",
            "implication": "Enables scalable gradient-based optimization of deep architectures.",
            "required_insights": ["parameter_to_loss_dependency", "function_composition", "chain_rule", "activation_caching", "reverse_mode_reuse"],
            "relation_type": "mathematical_consequence",
        },
        "chain_rule": {
            "starting_problem": "Many functions are built by nesting one function inside another, f(g(x)), rather than adding or multiplying them.",
            "desired_outcome": "Find the instantaneous rate of change of the composite output with respect to x.",
            "obstacle": "Differentiating only the outer function ignores how fast its input u = g(x) changes with x.",
            "necessary_insight": "Small changes multiply sequentially: Δf ≈ f'(g(x))·Δg and Δg ≈ g'(x)·Δx.",
            "mechanism": "Multiply the outer derivative evaluated at the inner output by the inner derivative: d/dx f(g(x)) = f'(g(x))·g'(x).",
            "result": "Exact derivative of any differentiable composite function.",
            "implication": "Forms the analytical backbone of implicit differentiation and reverse-mode automatic differentiation.",
            "required_insights": ["nested_composition", "inner_sensitivity", "outer_sensitivity", "multiplicative_rate_composition"],
            "relation_type": "mathematical_consequence",
        },
        "biot_savart_law": {
            "starting_problem": "Moving electric charges (steady currents) create magnetic fields whose strength and direction vary in 3D space.",
            "desired_outcome": "Compute the magnetic field B at any observation point from an arbitrary steady current path.",
            "obstacle": "Extended wires have varying distances and orientations relative to the observation point.",
            "necessary_insight": "Superposition decomposes a steady current into infinitesimal vector elements I dℓ whose individual field contributions add linearly.",
            "mechanism": "Evaluate dB = (μ0 / 4π) (I dℓ × r̂) / r² for each element and integrate vectorially over the current distribution.",
            "result": "Exact magnetostatic field B(r) obeying the inverse-square decay and right-hand cross-product direction.",
            "implication": "Generalizes to loops, finite wires, and solenoids under steady-current (magnetostatic) assumptions.",
            "required_insights": ["steady_current_source", "infinitesimal_decomposition", "cross_product_direction", "inverse_square_law", "vector_superposition"],
            "relation_type": "causal_mechanism",
        },
        "correlation_and_causation": {
            "starting_problem": "Observed datasets frequently show two variables moving together, tempting analysts to infer cause and effect.",
            "desired_outcome": "Determine when observed association legitimately supports a causal claim.",
            "obstacle": "Confounding variables, reverse causality, and selection bias can produce strong correlation without any direct causal effect.",
            "necessary_insight": "Statistical association describes passive observation P(Y|X), whereas causation describes intervention P(Y|do(X)).",
            "mechanism": "Distinguish observational co-variation from interventional evidence using study design (randomization) or explicit causal identification assumptions.",
            "result": "Disciplined claims that state exact identification assumptions rather than equating correlation with causation.",
            "implication": "Prevents flawed policy, scientific, and engineering decisions based on spurious associations.",
            "required_insights": ["co_variation_measurement", "confounding_and_reverse_causality", "observation_vs_intervention", "identification_assumptions"],
            "relation_type": "conceptual_association",
        },
    }

    if key in presets:
        spine = dict(presets[key])
    else:
        rel_type = {
            "mathematical": "mathematical_consequence",
            "computational": "logical_implication",
            "scientific": "causal_mechanism",
            "historical": "historical_sequence",
            "conceptual": "conceptual_association",
        }[family]
        spine = {
            "starting_problem": f"Understand the core problem or question addressed by {topic}.",
            "desired_outcome": f"Establish a clear, accurate working understanding of {topic}.",
            "obstacle": f"Naive intuition alone does not specify the conditions or mechanism governing {topic}.",
            "necessary_insight": f"Identify the governing principle or defining distinction of {topic}.",
            "mechanism": f"Connect the key components of {topic} through {rel_type.replace('_', ' ')}.",
            "result": f"Derive or observe the characteristic outcome of {topic}.",
            "implication": f"Apply {topic} within its verified applicability boundaries.",
            "required_insights": [slugify(f)[:32].replace("-", "_") for f in (source_facts or [topic])[:5]],
            "relation_type": rel_type,
        }

    spine.update({
        "domain_pattern": stages,
        "activation": activation,
        "preserve_source_order": preserve_source_order,
        "source_order_strategy": "local_transitions_only" if preserve_source_order else "dependency_aligned_spine",
        "prerequisites_honored": list(prerequisites or []),
        "provenance": "source_stated_explanation" if (source_mode == "strict" and source_facts) else provenance,
    })
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
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """EIS-02: Reconstruct the central guiding question and rank selective anticipated reader questions."""
    key = slugify(topic).replace("-", "_")
    question_presets: dict[str, tuple[str, list[dict[str, Any]]]] = {
        "gradient_descent": (
            "How can we systematically update model parameters to reduce a loss function?",
            [
                {"question_id": "why_gradient", "question": "Why does the gradient tell us how to adjust parameters?", "concept": "loss_gradient", "priority": 1, "stage": "core", "render": "implicit"},
                {"question_id": "why_negative_direction", "question": "Why do we subtract rather than add the gradient?", "concept": "descent_direction", "priority": 2, "stage": "core", "render": "implicit"},
                {"question_id": "why_learning_rate", "question": "How large should each update step be?", "concept": "step_size", "priority": 3, "stage": "core", "render": "implicit"},
                {"question_id": "what_if_zero_gradient", "question": "What happens when the gradient is zero or the step size is too large?", "concept": "limitations", "priority": 4, "stage": "limitations", "render": "implicit"},
            ],
        ),
        "binary_search": (
            "How can sorted order let us locate an element without checking every position?",
            [
                {"question_id": "why_midpoint", "question": "Why compare against the middle element specifically?", "concept": "midpoint_comparison", "priority": 1, "stage": "core", "render": "implicit"},
                {"question_id": "why_terminates", "question": "Why is the algorithm guaranteed to terminate without skipping the target?", "concept": "interval_invariant", "priority": 2, "stage": "core", "render": "implicit"},
                {"question_id": "what_if_unsorted", "question": "What breaks if the input array is not sorted?", "concept": "precondition", "priority": 3, "stage": "limitations", "render": "implicit"},
            ],
        ),
        "backpropagation": (
            "How can a neural network efficiently compute how every parameter influences its final loss?",
            [
                {"question_id": "why_chain_rule", "question": "Why does the chain rule govern gradient flow across layers?", "concept": "chain_rule", "priority": 1, "stage": "core", "render": "implicit"},
                {"question_id": "why_reverse_mode", "question": "Why propagate derivatives backward instead of forward from each weight?", "concept": "reverse_mode_efficiency", "priority": 2, "stage": "core", "render": "implicit"},
                {"question_id": "what_must_be_cached", "question": "Why must forward activations be saved during training?", "concept": "activation_caching", "priority": 3, "stage": "core", "render": "implicit"},
            ],
        ),
        "chain_rule": (
            "How do we differentiate a function composed of other functions?",
            [
                {"question_id": "why_multiply_rates", "question": "Why do the outer and inner derivatives multiply rather than add?", "concept": "rate_composition", "priority": 1, "stage": "core", "render": "implicit"},
                {"question_id": "where_evaluated", "question": "Why is the outer derivative evaluated at g(x) rather than x?", "concept": "inner_evaluation", "priority": 2, "stage": "core", "render": "implicit"},
            ],
        ),
        "biot_savart_law": (
            "How can we calculate the magnetic field contribution produced by a small current element?",
            [
                {"question_id": "why_cross_product", "question": "Why does the field direction follow dℓ × r̂?", "concept": "field_direction", "priority": 1, "stage": "core", "render": "implicit"},
                {"question_id": "why_integrate", "question": "How do individual current-element contributions combine for a whole wire?", "concept": "superposition", "priority": 2, "stage": "core", "render": "implicit"},
            ],
        ),
        "correlation_and_causation": (
            "When does observing an association between two variables support a causal conclusion?",
            [
                {"question_id": "why_insufficient", "question": "Why can two variables correlate strongly without one causing the other?", "concept": "confounding", "priority": 1, "stage": "core", "render": "implicit"},
                {"question_id": "what_supports_causality", "question": "What evidence or assumptions are needed to justify a causal claim?", "concept": "causal_identification", "priority": 2, "stage": "core", "render": "implicit"},
            ],
        ),
    }

    if key in question_presets:
        q_text, anticipated = question_presets[key]
    else:
        q_text = f"What core problem does {topic} solve, and under what conditions does its mechanism work?"
        anticipated = [
            {"question_id": "why_needed", "question": f"Why is {topic} needed?", "concept": key, "priority": 1, "stage": "core", "render": "implicit"},
            {"question_id": "when_valid", "question": f"Under what conditions does {topic} apply?", "concept": "boundaries", "priority": 2, "stage": "limitations", "render": "implicit"},
        ]

    # Master-aware anti-question-explosion filtering (M3 cheat sheet & trivial defs keep minimal/implicit questions)
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
) -> tuple[dict[str, Any], dict[str, Any]]:
    """EIS-03: Plan causal/logical mechanism separately from mathematical derivation step motivation."""
    key = slugify(topic).replace("-", "_")
    family = _domain_family(concept_type)
    causality_justified = family in {"scientific", "computational"}

    if activation == "disabled":
        return (
            {"applicable": False, "type": family, "causality_justified": causality_justified},
            {"enabled": False, "steps": []},
        )

    mechanism_presets: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {
        "gradient_descent": (
            {
                "applicable": True,
                "type": "mathematical_optimization",
                "causality_justified": False,
                "relation_basis": "mathematical_dependence",
                "inputs": ["initial parameters θ_0", "differentiable loss J(θ)", "learning rate α > 0"],
                "relevant_conditions": ["differentiability", "L-smoothness for finite-step stability (0 < α < 2/L)"],
                "operations": ["evaluate gradient ∇J(θ_t)", "compute step Δθ = -α∇J(θ_t)", "update θ_{t+1} = θ_t + Δθ"],
                "intermediate_states": ["gradient vector at θ_t", "parameter shift Δθ"],
                "outputs": ["updated parameters θ_{t+1}", "new loss J(θ_{t+1})"],
                "limiting_factors": ["overshooting when α > 2/L", "saddle points and nonconvex local minima", "ill-conditioning"],
            },
            {
                "enabled": True,
                "central_operation": "first_order_taylor_descent_justification",
                "local_vs_global_note": "The first-order approximation justifies local descent direction for infinitesimal steps, not global convergence for arbitrary finite steps.",
                "steps": [
                    {
                        "goal": "Estimate how a small parameter shift Δθ changes the loss J(θ).",
                        "operation": "first_order_taylor_expansion",
                        "mathematical_basis": "differentiability",
                        "result": "J(θ + Δθ) ≈ J(θ) + ∇J(θ)^T Δθ",
                        "interpretation": "The inner product ∇J(θ)^T Δθ controls the first-order change in loss.",
                        "next_purpose": "Choose Δθ so that this inner product is negative.",
                        "assumptions": ["J is differentiable at θ", "||Δθ|| is sufficiently small"],
                    },
                    {
                        "goal": "Guarantee a nonpositive first-order loss change.",
                        "operation": "select_negative_gradient_step",
                        "mathematical_basis": "cauchy_schwarz_steepest_descent",
                        "result": "Δθ = -α∇J(θ) ⇒ J(θ + Δθ) ≈ J(θ) - α||∇J(θ)||²",
                        "interpretation": "For α > 0 and ∇J(θ) ≠ 0, -α||∇J(θ)||² < 0 gives local descent.",
                        "next_purpose": "Bound α using L-smoothness (0 < α < 2/L) to guarantee actual finite-step decrease.",
                        "assumptions": ["α > 0", "Euclidean norm geometry"],
                    },
                ],
            },
        ),
        "chain_rule": (
            {
                "applicable": True,
                "type": "mathematical_composition",
                "causality_justified": False,
                "relation_basis": "mathematical_dependence",
                "inputs": ["input x", "inner function g", "outer function f"],
                "relevant_conditions": ["g differentiable at x", "f differentiable at g(x)"],
                "operations": ["evaluate u = g(x)", "compute local sensitivity g'(x)", "multiply by f'(u)"],
                "intermediate_states": ["intermediate value u = g(x)"],
                "outputs": ["composite derivative f'(g(x))·g'(x)"],
                "limiting_factors": ["nondifferentiable corners such as |g(x)| at g(x)=0"],
            },
            {
                "enabled": True,
                "central_operation": "composite_rate_factorization",
                "steps": [
                    {
                        "goal": "Relate a small change in x to the induced change in inner output u = g(x).",
                        "operation": "introduce_intermediate_variable",
                        "mathematical_basis": "linear_approximation",
                        "result": "Δu ≈ g'(x)·Δx",
                        "interpretation": "g'(x) scales how strongly x moves the inner value u.",
                        "next_purpose": "Propagate Δu through the outer function f.",
                        "assumptions": ["g differentiable at x"],
                    },
                    {
                        "goal": "Combine inner and outer sensitivities to obtain Δf/Δx as Δx → 0.",
                        "operation": "compose_linear_maps",
                        "mathematical_basis": "limit_of_product",
                        "result": "d/dx f(g(x)) = f'(g(x))·g'(x)",
                        "interpretation": "Rates of change multiply along a chain of composed functions.",
                        "next_purpose": "Apply recursively to multi-layer compositions.",
                        "assumptions": ["f differentiable at g(x)"],
                    },
                ],
            },
        ),
        "biot_savart_law": (
            {
                "applicable": True,
                "type": "physical_field_generation",
                "causality_justified": True,
                "relation_basis": "physical_law",
                "inputs": ["steady current I", "current element dℓ", "displacement vector r"],
                "relevant_conditions": ["magnetostatics (steady current, negligible displacement current)"],
                "operations": ["compute cross product dℓ × r̂", "scale by μ0 I / (4π r²)", "integrate along wire"],
                "intermediate_states": ["infinitesimal field vector dB"],
                "outputs": ["net magnetic field vector B(r)"],
                "limiting_factors": ["breaks down for rapidly time-varying currents where Maxwell displacement current matters"],
            },
            {
                "enabled": True,
                "central_operation": "vector_superposition_integration",
                "steps": [
                    {
                        "goal": "Express the field from one infinitesimal current segment with direction perpendicular to both dℓ and r̂.",
                        "operation": "cross_product_formulation",
                        "mathematical_basis": "vector_calculus",
                        "result": "dB = (μ0 / 4π) (I dℓ × r̂) / r²",
                        "interpretation": "Magnitude scales with sin(θ)/r² and direction follows the right-hand rule.",
                        "next_purpose": "Integrate vectorially over the entire current path.",
                        "assumptions": ["steady current", "observation point not on the idealized filament (r > 0)"],
                    },
                ],
            },
        ),
    }

    if key in mechanism_presets:
        mech, motiv = mechanism_presets[key]
        if source_mode == "strict":
            motiv = {**motiv, "source_policy_guard": "Only derive steps supported by the supplied source; never import external theorems."}
        return mech, motiv

    is_math = family in {"mathematical", "scientific"}
    mech = {
        "applicable": family != "historical",
        "type": family,
        "causality_justified": causality_justified,
        "relation_basis": "historical_evidence_and_interpretation" if family == "historical" else family,
        "inputs": [],
        "relevant_conditions": [],
        "operations": [],
        "outputs": [],
        "limiting_factors": ["evidence uncertainty and competing scholarly interpretations"] if family == "historical" else [],
    }
    motiv = {
        "enabled": is_math and activation in {"standard", "deep"},
        "steps": [],
        "source_policy_guard": "strict_source_only" if source_mode == "strict" else "standard",
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
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """EIS-04: Specify applicability conditions, necessary vs sufficient distinctions, and high-value contrasts."""
    key = slugify(topic).replace("-", "_")
    if activation == "disabled":
        return {"enabled": False}, []

    boundary_presets: dict[str, dict[str, Any]] = {
        "gradient_descent": {
            "enabled": True,
            "domain_of_use": ["differentiable continuous optimization"],
            "required_conditions": ["differentiability (or a subgradient—a generalized slope—at nondifferentiable kinks)", "positive step size α > 0"],
            "sufficient_conditions": ["convexity + L-smoothness + 0 < α < 2/L for global convergence"],
            "guarantees": ["monotonic loss reduction under L-smoothness with 0 < α < 2/L"],
            "typical_behavior": ["linear convergence on strongly convex objectives; zig-zagging under ill-conditioning"],
            "known_limitations": ["stationary points (saddle points / local minima) on nonconvex losses", "divergence if α > 2/L"],
            "invalid_generalizations": ["Gradient descent always finds the global minimum."],
        },
        "binary_search": {
            "enabled": True,
            "domain_of_use": ["random-access ordered sequences or monotonic predicates"],
            "required_conditions": ["monotonic / sorted ordering matching the comparison operator"],
            "sufficient_conditions": ["sorted array with total order + correct midpoint and bound updates"],
            "guarantees": ["O(log n) worst-case comparisons; returns target index if present or not-found indicator"],
            "known_limitations": ["fails silently on unsorted arrays", "off-by-one infinite loops if bounds do not strictly shrink"],
            "invalid_generalizations": ["Binary search always finds an element in O(log n) time regardless of input order."],
        },
        "backpropagation": {
            "enabled": True,
            "domain_of_use": ["differentiable directed acyclic computation graphs"],
            "required_conditions": ["almost-everywhere differentiable operations (or defined subgradients like ReLU)"],
            "sufficient_conditions": ["acyclic forward graph with cached intermediates"],
            "guarantees": ["exact gradients (up to floating-point precision) in O(forward pass) time"],
            "known_limitations": ["memory overhead of caching activations", "vanishing/exploding gradients in deep chains"],
            "invalid_generalizations": ["Backpropagation itself updates weights (it computes gradients; the optimizer updates weights)."],
        },
        "chain_rule": {
            "enabled": True,
            "domain_of_use": ["differentiable composite functions"],
            "required_conditions": ["g differentiable at x", "f differentiable at g(x)"],
            "sufficient_conditions": ["both component functions differentiable at the relevant points"],
            "guarantees": ["(f ∘ g)'(x) = f'(g(x))·g'(x)"],
            "known_limitations": ["does not apply directly at points of nondifferentiability"],
            "invalid_generalizations": ["d/dx f(g(x)) = f'(g(x)) (omits inner derivative g'(x))."],
        },
        "biot_savart_law": {
            "enabled": True,
            "domain_of_use": ["magnetostatics (steady currents)"],
            "required_conditions": ["steady current (∂ρ/∂t = 0)", "observation point r > 0 outside idealized wire"],
            "sufficient_conditions": ["steady closed current distribution in linear homogeneous medium"],
            "guarantees": ["exact magnetostatic B field via line/volume integration"],
            "known_limitations": ["incomplete for rapidly changing electromagnetic fields where radiation/displacement current occurs"],
            "invalid_generalizations": ["Treating dB as a scalar without cross-product direction."],
        },
        "correlation_and_causation": {
            "enabled": True,
            "domain_of_use": ["statistical inference and empirical evaluation"],
            "required_conditions": ["explicit causal assumptions or randomized intervention to claim causation"],
            "known_limitations": ["confounding, reverse causality, collider bias"],
            "invalid_generalizations": [
                "Correlation proves causation.",
                "Observational data can never inform causal inference under any assumptions.",
            ],
        },
    }

    if key in boundary_presets:
        boundaries = dict(boundary_presets[key])
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

    contrasts = list(KNOWN_CONTRASTS.get(key, []))
    return boundaries, contrasts


# ---------------------------------------------------------------------------
# EIS-05: Variable Roles, Invariants & Algorithm State Narration
# ---------------------------------------------------------------------------

def plan_variable_and_state_reasoning(
    topic: str,
    *,
    concept_type: str = "conceptual",
    activation: str = "contextual",
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """EIS-05: Classify operational variable roles, valid invariants, and verified numerical/state traces.

    Never forces execution traces or invented invariants onto nonprocedural/conceptual/historical topics.
    """
    key = slugify(topic).replace("-", "_")
    if activation == "disabled":
        return [], {"applicable": False, "invariant": {"applicable": False}}

    if key == "gradient_descent":
        variables = [
            {"symbol": "θ", "meaning": "Model parameter", "role": "state_variable", "effect": "Moves opposite ∇J(θ) each iteration"},
            {"symbol": "α", "meaning": "Learning rate", "role": "hyperparameter", "effect": "Scales step size linearly: Δθ = -α∇J(θ)"},
            {"symbol": "∇J(θ)", "meaning": "Loss gradient", "role": "intermediate_result", "effect": "Specifies steepest local increase direction and slope magnitude"},
            {"symbol": "J(θ)", "meaning": "Objective loss", "role": "output", "effect": "Evaluates quality of current parameter state"},
        ]
        # Exact verified numerical trace for J(θ) = θ², J'(θ) = 2θ, α = 0.1, θ_0 = 4.0 -> θ_{t+1} = 0.8 θ_t
        trace = []
        theta = 4.0
        alpha = 0.1
        for step in range(4):
            loss = round(theta * theta, 4)
            grad = round(2.0 * theta, 4)
            trace.append({"iteration": step, "theta": round(theta, 4), "gradient": grad, "loss": loss})
            theta = theta - alpha * (2.0 * theta)
        state_model = {
            "applicable": True,
            "initial_state": {"theta": 4.0, "alpha": 0.1, "objective": "J(θ) = θ^2"},
            "state_variables": ["theta", "loss"],
            "transition_rule": "theta_{t+1} = theta_t - alpha * 2 * theta_t = 0.8 * theta_t",
            "termination_condition": "|gradient| < tol or step == max_steps",
            "invariant": {
                "applicable": True,
                "statement": "For convex L-smooth J(θ)=θ² (L=2) and 0 < α=0.1 < 2/L=1, J(θ_{t+1}) <= J(θ_t) monotonically at every step.",
            },
            "example_trace": trace,
        }
        return variables, state_model

    if key == "binary_search":
        variables = [
            {"symbol": "arr", "meaning": "Sorted input sequence", "role": "input", "effect": "Provides random-access ordered elements"},
            {"symbol": "target", "meaning": "Value being searched", "role": "input", "effect": "Compared against arr[mid] to pick half"},
            {"symbol": "low", "meaning": "Inclusive lower index", "role": "index", "effect": "Advances to mid + 1 when arr[mid] < target"},
            {"symbol": "high", "meaning": "Inclusive upper index", "role": "index", "effect": "Retreats to mid - 1 when arr[mid] > target"},
            {"symbol": "mid", "meaning": "Midpoint index", "role": "control_variable", "effect": "Partitions [low, high] into two halves"},
        ]
        arr = [2, 5, 8, 12, 16, 23, 38]
        target = 23
        low, high = 0, len(arr) - 1
        trace = []
        step = 0
        while low <= high:
            mid = low + (high - low) // 2
            val = arr[mid]
            if val == target:
                decision = "found"
                trace.append({"step": step, "low": low, "high": high, "mid": mid, "arr_mid": val, "decision": decision})
                break
            elif val < target:
                decision = "discard_left_half (low = mid + 1)"
                trace.append({"step": step, "low": low, "high": high, "mid": mid, "arr_mid": val, "decision": decision})
                low = mid + 1
            else:
                decision = "discard_right_half (high = mid - 1)"
                trace.append({"step": step, "low": low, "high": high, "mid": mid, "arr_mid": val, "decision": decision})
                high = mid - 1
            step += 1
        state_model = {
            "applicable": True,
            "initial_state": {"arr": arr, "target": target, "low": 0, "high": len(arr) - 1},
            "state_variables": ["low", "high", "mid"],
            "transition_rule": "Compare arr[mid] to target; shrink [low, high] strictly to [mid+1, high] or [low, mid-1].",
            "termination_condition": "arr[mid] == target or low > high",
            "invariant": {
                "applicable": True,
                "statement": "If target exists in sorted arr, its index lies within [low, high] before every iteration.",
            },
            "example_trace": trace,
        }
        return variables, state_model

    if key == "chain_rule":
        variables = [
            {"symbol": "x", "meaning": "Independent input", "role": "input", "effect": "Perturbation Δx drives inner change"},
            {"symbol": "u = g(x)", "meaning": "Intermediate inner output", "role": "intermediate_result", "effect": "Serves as input to outer function f"},
            {"symbol": "f(u)", "meaning": "Outer function output", "role": "output", "effect": "Changes at rate f'(g(x))·g'(x) with respect to x"},
        ]
        return variables, {"applicable": False, "invariant": {"applicable": False}}

    if key == "biot_savart_law":
        variables = [
            {"symbol": "I", "meaning": "Steady electric current (A)", "role": "input", "effect": "Scales magnetic field linearly"},
            {"symbol": "dℓ", "meaning": "Infinitesimal wire element vector (m)", "role": "input", "effect": "Sets current flow direction along path"},
            {"symbol": "r̂", "meaning": "Unit vector from element to field point", "role": "input", "effect": "Cross product dℓ × r̂ fixes field direction"},
            {"symbol": "r", "meaning": "Distance from element to observation point (m)", "role": "input", "effect": "Field decays as 1/r²"},
            {"symbol": "dB", "meaning": "Magnetic field contribution (T)", "role": "output", "effect": "Integrated over full wire for net B"},
        ]
        return variables, {"applicable": False, "invariant": {"applicable": False}}

    if key == "recursion":
        variables = [
            {"symbol": "n", "meaning": "Problem size parameter", "role": "state_variable", "effect": "Strictly decreases toward base case on each call"},
            {"symbol": "call_stack", "meaning": "Active suspended frames", "role": "state_variable", "effect": "Unwinds in LIFO order combining subproblem results"},
        ]
        state_model = {
            "applicable": True,
            "initial_state": {"call": "factorial(3)"},
            "state_variables": ["n", "call_stack"],
            "transition_rule": "Push smaller subproblem frame until base case n <= 1 returns 1, then unwind multiplying.",
            "termination_condition": "n <= 1 (base case reached)",
            "invariant": {
                "applicable": True,
                "statement": "Each recursive call strictly reduces non-negative integer n toward the base case.",
            },
            "example_trace": [
                {"phase": "call", "frame": "factorial(3)", "waiting_on": "3 * factorial(2)"},
                {"phase": "call", "frame": "factorial(2)", "waiting_on": "2 * factorial(1)"},
                {"phase": "base", "frame": "factorial(1)", "returns": 1},
                {"phase": "return", "frame": "factorial(2)", "returns": 2},
                {"phase": "return", "frame": "factorial(3)", "returns": 6},
            ],
        }
        return variables, state_model

    # Nonprocedural concepts explicitly disable execution trace and do not invent invariants
    is_procedural = concept_type in {"algorithm", "computational"} or bool(PROCEDURAL_CONCEPT_KEYWORDS.search(topic))
    if not is_procedural:
        return [], {"applicable": False, "invariant": {"applicable": False}}

    return [], {
        "applicable": True,
        "state_variables": [],
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
) -> dict[str, Any]:
    """EIS-06: Construct compact reasoning-preserving retrieval cues and reconstruction summaries."""
    key = slugify(topic).replace("-", "_")
    if activation == "disabled":
        return {"enabled": False, "cues": [], "reconstruction_chain": [], "summary": ""}

    presets: dict[str, dict[str, Any]] = {
        "gradient_descent": {
            "cues": ["objective", "direction", "magnitude", "iteration"],
            "reconstruction_chain": ["define_loss", "calculate_gradient", "select_negative_direction", "scale_step", "repeat_update"],
            "critical_conditions": ["differentiable objective", "0 < α < 2/L for L-smooth stability"],
            "summary": (
                "A loss function measures model error, and its gradient gives local sensitivity with respect to the parameters. "
                "Moving opposite the gradient provides a local descent direction, while the learning rate scales each step under smoothness limits (0 < α < 2/L). "
                "Repeating this update iteratively produces gradient descent."
            ),
        },
        "binary_search": {
            "cues": ["sorted_order", "middle", "compare", "eliminate", "repeat"],
            "reconstruction_chain": ["verify_sorted_order", "inspect_midpoint", "compare_target", "discard_impossible_half", "preserve_interval_invariant"],
            "critical_conditions": ["input sequence must be sorted"],
            "summary": (
                "Because the sequence is sorted, comparing the target to the midpoint rules out half of all remaining candidates. "
                "Shrinking the active interval [low, high] preserves the invariant that any matching index remains inside, guaranteeing O(log n) termination."
            ),
        },
        "backpropagation": {
            "cues": ["forward_values", "loss", "backward_derivatives", "parameter_gradients"],
            "reconstruction_chain": ["forward_pass_cache", "compute_output_loss", "apply_chain_rule_backward", "accumulate_parameter_gradients"],
            "critical_conditions": ["differentiable acyclic computation graph"],
            "summary": (
                "A forward pass computes and caches layer activations up to the scalar loss. "
                "Applying the chain rule in reverse reuses upstream derivatives to compute all parameter gradients in a single backward sweep."
            ),
        },
        "chain_rule": {
            "cues": ["nested_functions", "outer_derivative_at_inner", "multiply_inner_derivative"],
            "reconstruction_chain": ["identify_inner_u", "differentiate_outer_at_u", "multiply_by_inner_derivative"],
            "critical_conditions": ["g differentiable at x and f differentiable at g(x)"],
            "summary": (
                "When a function is nested as f(g(x)), a change in x shifts g(x) at rate g'(x), which shifts f at rate f'(g(x)). "
                "Multiplying those sensitivities gives d/dx f(g(x)) = f'(g(x))·g'(x) wherever both component derivatives exist."
            ),
        },
        "biot_savart_law": {
            "cues": ["steady_current", "element_cross_r_hat", "inverse_square", "vector_integral"],
            "reconstruction_chain": ["decompose_current_element", "apply_cross_product_direction", "scale_inverse_square", "integrate_superposition"],
            "critical_conditions": ["magnetostatic steady current, r > 0"],
            "summary": (
                "Break a steady current into infinitesimal vectors I dℓ, compute each perpendicular field contribution via dℓ × r̂ / r², "
                "and integrate vectorially over the wire under magnetostatic conditions."
            ),
        },
        "correlation_and_causation": {
            "cues": ["co_variation", "confounders", "intervention_vs_observation", "identification_assumptions"],
            "reconstruction_chain": ["measure_association", "check_confounders_and_reverse_causality", "require_interventional_or_identified_design"],
            "critical_conditions": ["association alone never proves causation without identification assumptions"],
            "summary": (
                "Correlation captures passive co-variation, which confounders or reverse causality can induce without any causal link. "
                "Establishing causation requires interventional evidence or explicit causal identification assumptions."
            ),
        },
    }

    if key in presets:
        rec = dict(presets[key])
    else:
        conds = list(boundaries.get("required_conditions") or [])
        rec = {
            "cues": ["problem", "insight", "mechanism", "conditions"],
            "reconstruction_chain": ["identify_problem", "apply_insight", "execute_mechanism", "verify_conditions"],
            "critical_conditions": conds,
            "summary": (
                f"{spine.get('starting_problem', '')} {spine.get('necessary_insight', '')} "
                f"{spine.get('mechanism', '')} {spine.get('result', '')}"
            ).strip(),
        }

    # M6 Assessment: keep retrieval cues internal for question design, do NOT leak answers into question-only artifacts
    leak_protected = master == "M6"
    return {
        "enabled": True,
        "concept_id": key,
        "activation": activation,
        "internal_only": leak_protected,
        "cues": rec["cues"],
        "reconstruction_chain": rec["reconstruction_chain"],
        "critical_conditions": rec["critical_conditions"],
        "summary": "" if leak_protected else rec["summary"],
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
    )
    central_q, anticipated_qs = plan_central_question_and_anticipation(
        topic, spine, master=master, concept_type=ctype, activation=activations["eis_02_questions"]
    )
    mechanism, math_motiv = plan_mechanism_and_motivation(
        topic, concept_type=ctype, source_mode=source_mode, activation=activations["eis_03_motivation"]
    )
    boundaries, contrasts = plan_boundaries_and_contrasts(
        topic, concept_type=ctype, complexity=complexity, activation=activations["eis_04_boundaries"]
    )
    var_roles, exec_state = plan_variable_and_state_reasoning(
        topic, concept_type=ctype, activation=activations["eis_05_state"]
    )
    retrieval = build_retrieval_cues(
        topic, spine, boundaries, master=master, activation=activations["eis_06_retrieval"]
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

    Never exposes internal blueprint role names (e.g., 'Explanatory Spine:', 'Reader Simulation') as headings.
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

    # M3 Quick Reference: dense, scannable, minimal prose
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

    # Strict source-order mode (M2 / source_only): preserve source fact sequence verbatim with concise transitions
    if preserve_order and source_facts:
        lines.append("## 1. Source Context & Overview")
        lines.append(
            "> [!info] Source & Scope Context\n"
            f"> - **Source Policy**: `{source_mode}` (preserves original sequence; no external facts added)"
        )
        lines.append("")
        lines.append("## 2. Sequential Development")
        for idx, fact in enumerate(source_facts, 1):
            if idx == 1:
                rendered_fact = fact
            else:
                # Preserve exact source text while keeping natural transition punctuation
                rendered_fact = f"Building directly on the preceding point: {fact}"
            lines.append(f"### 2.{idx} Step {idx}")
            lines.append(rendered_fact)
            lines.append("")
        if blueprint.retrieval.get("summary") and source_mode != "strict":
            lines.append("## 3. Synthesis")
            lines.append(blueprint.retrieval["summary"])
            lines.append("")
        return render_note_with_properties(props, "\n".join(lines))

    # Full natural-prose composition (M1, M2, M4, M5, M7)
    # 1. Problem motivation & guiding question woven naturally into prose
    lines.append("## Motivation and Core Idea")
    opening = f"{spine.get('starting_problem', '')} {spine.get('obstacle', '')}".strip()
    if blueprint.central_question.get("explicit_in_prose") and blueprint.central_question.get("question"):
        opening += f" This leads naturally to a guiding question: *{blueprint.central_question['question']}*"
    lines.append(opening)
    lines.append("")
    lines.append(f"{spine.get('necessary_insight', '')} {spine.get('mechanism', '')} {spine.get('result', '')}".strip())
    lines.append("")

    # 2. Mathematical derivation motivation (when enabled & populated)
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

    # 3. Variable roles & verified procedural state trace (when applicable)
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

    # 4. Applicability boundaries & discriminating contrasts
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

    # 5. Reconstruction-oriented summary (not for M6 question-only artifacts)
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

    # Composition hygiene: never expose internal planning labels as visible headings
    if m := INTERNAL_BLUEPRINT_HEADINGS_RE.search(body):
        issues.append({
            "code": "EIS-COMP-001",
            "severity": "major",
            "concept_id": blueprint.concept_id,
            "location": "headings",
            "description": f"Internal blueprint heading exposed in final note: '{m.group(0)}'.",
            "recommended_repair": "replace_internal_heading_with_natural_prose_heading",
        })

    # EIS-01: Source-order preservation check
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

    # EIS-01: False causality check on non-causal / correlation / historical domains
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

    # EIS-02: Anti-question-explosion check
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

    # EIS-03: Empty algebraic step narration & local-vs-global overclaim checks
    if re.search(r"(?:^|[.!?]\s+)(?:Now\s+differentiate\s+both\s+sides|Substitute\s+the\s+values)\.", body, re.I):
        issues.append({
            "code": "EIS-MOTIV-001",
            "severity": "major",
            "concept_id": blueprint.concept_id,
            "location": "derivation",
            "description": "Unmotivated algebraic narration ('Now differentiate both sides' / 'Substitute the values') lacks purpose.",
            "recommended_repair": "state_operation_purpose_before_step",
        })
    if re.search(r"\bgradient\s+descent\s+always\s+(?:converges\s+to|finds)\s+the\s+global\s+minimum\b", body, re.I):
        issues.append({
            "code": "EIS-MOTIV-002",
            "severity": "critical",
            "concept_id": blueprint.concept_id,
            "location": "guarantees",
            "description": "Confuses local descent argument with universal global minimum guarantee.",
            "recommended_repair": "qualify_global_optimality_with_convexity_and_smoothness",
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

    # EIS-04: Applicability boundary violation checks
    if "binary_search" in blueprint.concept_id or "binary search" in blueprint.topic.lower():
        if re.search(r"\bbinary\s+search\s+always\s+finds\b", body, re.I) and not re.search(r"\bsorted|ordered|monotonic\b", body, re.I):
            issues.append({
                "code": "EIS-BOUND-001",
                "severity": "critical",
                "concept_id": blueprint.concept_id,
                "location": "applicability",
                "description": "Claims binary search always finds elements without stating the sorted-input precondition.",
                "recommended_repair": "add_sorted_input_precondition",
            })

    # EIS-05: Reject forced execution trace / invented invariant on nonprocedural topics
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

    # EIS-06: Summary inflation check (multiple redundant recap headings)
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
    rule: str = "quadratic_gd",
    alpha: float = 0.1,
) -> dict[str, Any]:
    """EIS-05: Deterministically verify numerical state trace transitions and invariants."""
    errors: list[str] = []
    if not trace:
        return {"valid": False, "errors": ["Empty state trace."]}
    if rule == "quadratic_gd":
        prev_loss = None
        for idx, row in enumerate(trace):
            theta = float(row["theta"])
            loss = float(row["loss"])
            expected_loss = round(theta * theta, 4)
            if abs(loss - expected_loss) > 1e-3:
                errors.append(f"Row {idx}: loss={loss} disagrees with theta^2={expected_loss}.")
            if idx > 0:
                prev_theta = float(trace[idx - 1]["theta"])
                expected_theta = round(prev_theta - alpha * 2.0 * prev_theta, 4)
                if abs(theta - expected_theta) > 1e-3:
                    errors.append(f"Row {idx}: theta={theta} disagrees with recurrence {expected_theta}.")
            if prev_loss is not None and loss > prev_loss + 1e-6:
                errors.append(f"Row {idx}: monotonic descent invariant violated ({loss} > {prev_loss}).")
            prev_loss = loss
    elif rule == "binary_search":
        prev_span = None
        for idx, row in enumerate(trace):
            low, high, mid = int(row["low"]), int(row["high"]), int(row["mid"])
            if not (low <= mid <= high):
                errors.append(f"Row {idx}: midpoint {mid} outside [{low}, {high}].")
            span = high - low + 1
            if prev_span is not None and span >= prev_span:
                errors.append(f"Row {idx}: search interval failed to shrink strictly ({span} >= {prev_span}).")
            prev_span = span
    return {"valid": not errors, "errors": errors}
