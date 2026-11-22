"""Engine E1 — Orchestration and Routing Engine for Scriptorium.

Consolidates:
- Seven-master (M1-M7) request routing & master registry validation
- Mechanism 1: Request Intent Normalization
- Mechanism 2: Constraint Precedence Engine
- Mechanism 3: Template Capability Matrix
- Mechanism 4: Instruction Authority Graph & Linting
- Mechanism 13: Adaptive Clarification Policy
- Mechanism 20: Observability and Decision Tracing
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlsplit

import yaml

from scriptorium.models import (
    REPO_ROOT,
    RoutingError,
    SourcePolicyConflictError,
    TemplateResolutionError,
    slugify,
)

ROOT = REPO_ROOT
CANONICAL_MASTER_IDS = ("M1", "M2", "M3", "M4", "M5", "M6", "M7")

URL_RE = re.compile(r"https?://[^\s<>\"]+", re.I)
PAPER_PATHS = {
    "arxiv.org": ("/abs/", "/pdf/", "/html/"),
    "doi.org": ("/10.",),
    "openreview.net": ("/forum", "/pdf"),
    "aclanthology.org": ("/",),
    "papers.nips.cc": ("/paper",),
    "proceedings.neurips.cc": ("/paper",),
    "openaccess.thecvf.com": ("/content",),
    "ieeexplore.ieee.org": ("/document/", "/abstract/document/", "/stamp/"),
    "dl.acm.org": ("/doi/",),
}

NEGATION_CLAUSES = (
    re.compile(
        r"\b(?:don't|do not|dont|never|not|no|avoid|skip|without|instead of|rather than)\s+"
        r"(?:make|create|write|give me|generate|produce|build|a|an|just|only|another|any)?\s*"
        r"(?:a|an|the)?\s*"
        r"(cheat[\s-]?sheet|formula[\s-]?sheet|quick[\s-]?reference|summary|summaries|"
        r"study[\s-]?guide|study[\s-]?notes|flashcards?|quiz|practice[\s-]?(?:test|set)|"
        r"mock[\s-]?exam|atomic[\s-]?note|worked[\s-]?solutions?|worked[\s-]?examples?|"
        r"examples?|coding[\s-]?tutorial|code|implementation|"
        r"comparison|concept[\s-]?map|deep[\s-]?notes?|essay)\b",
        re.I,
    ),
)

NEGATION_TO_MASTER = {
    "cheat": "M3",
    "formula": "M3",
    "quick": "M3",
    "atomic": "M3",
    "summary": "M7",
    "summaries": "M7",
    "comparison": "M7",
    "concept": "M7",
    "study": "M2",
    "flashcard": "M6",
    "quiz": "M6",
    "practice": "M6",
    "mock": "M6",
    "worked": "M4",
    "coding": "M5",
    "code": "M5",
    "implementation": "M5",
    "deep": "M1",
    "essay": "M1",
}

STRICT_SOURCE_PATTERNS = (
    re.compile(r"\busing only (?:its|the|this|these|my)\b", re.I),
    re.compile(r"\bonly (?:from|using) (?:the|this|my)\s+(?:lecture|pdf|slides|chapter|notes|source|text|paper|transcript|homework)\b", re.I),
    re.compile(r"\bno outside (?:sources|research|formulas|material)\b", re.I),
    re.compile(r"\bstrict(?:ly)? (?:source|faithful)\b", re.I),
    re.compile(r"\bsource[- ]only\b", re.I),
    re.compile(r"\bwithout skipping anything\b", re.I),
    re.compile(r"\bdo not add outside\b", re.I),
)

SOURCE_ORDER_PATTERNS = (
    re.compile(r"\b(?:in|preserving|keep(?:ing)?|follow(?:ing)?)\s+(?:its|the|exact)?\s*(?:lecture|chapter|source|slide|transcript|book|syllabus)?\s*order\b", re.I),
    re.compile(r"\b(?:this|my|the)\s+(?:lecture|transcript|slides|chapter|syllabus|textbook chapter|class notes|pdf)\b", re.I),
    re.compile(r"\bwithout skipping anything\b", re.I),
)

SEPARATE_MULTI_PATTERNS = (
    re.compile(
        r"\b(?:and|plus|,)\s+(?:also\s+)?(?:make|create|generate|write|produce|give me)?\s*"
        r"(?:a\s+|an\s+)?(?:separate|standalone|companion|dedicated)\s+"
        r"(cheat[\s-]?sheet|formula[\s-]?sheet|quick[\s-]?reference|syntax[\s-]?reference|"
        r"command[\s-]?reference|atomic[\s-]?note|practice[\s-]?(?:set|test)|quiz|flashcards?|"
        r"mock[\s-]?exam|worked[\s-]?(?:solutions?|examples?)|revision[\s-]?pack|concept[\s-]?map|"
        r"comparison|study[\s-]?notes?|deep[\s-]?notes?|implementation[\s-]?guide)\b",
        re.I,
    ),
    re.compile(
        r"\b(?:both|two separate|two standalone)\b.*?"
        r"(deep[\s-]?notes?|study[\s-]?notes?|cheat[\s-]?sheet|formula[\s-]?sheet|"
        r"practice[\s-]?(?:set|test)|flashcards?|worked[\s-]?solutions?|revision[\s-]?pack)\s+"
        r"and\s+(?:a\s+|an\s+)?(deep[\s-]?notes?|study[\s-]?notes?|cheat[\s-]?sheet|formula[\s-]?sheet|"
        r"practice[\s-]?(?:set|test)|flashcards?|worked[\s-]?solutions?|revision[\s-]?pack|mock[\s-]?exam)\b",
        re.I,
    ),
)

EMBEDDED_SECONDARY_PATTERNS = (
    (re.compile(r"\b(?:include|with|add|append|plus)\s+(?:a\s+)?(?:short|brief|quick|compact|mini|small)?\s*(?:formula\s+)?cheat[\s-]?sheet(?:\s+at the end)?\b", re.I), "formula_reference"),
    (re.compile(r"\b(?:include|with|add|append|plus)\s+(?:a\s+)?(?:short|brief|quick|compact)?\s*formula[\s-]?sheet(?:\s+at the end)?\b", re.I), "formula_reference"),
    (re.compile(r"\b(?:briefly\s+)?summari[sz]e the formulas?\s+(?:first|at the (?:top|start|end))\b", re.I), "formula_reference"),
    (re.compile(r"\b(?:include|with|add|append)\s+(?:a\s+few|\d+|some|quick|brief)?\s*(?:review|practice|self-check|recall)\s+questions?(?:\s+at the end)?\b", re.I), "active_recall"),
    (re.compile(r"\b(?:include|with|add)\s+(?:a\s+)?(?:brief|short)?\s*(?:complexity|mathematical)\s+(?:proof|derivation|explanation)\b", re.I), "mathematical_derivation"),
    (re.compile(r"\b(?:include|with|add)\s+(?:a\s+)?(?:brief|short)?\s*comparison\s+(?:table|section)\b", re.I), "comparisons"),
    (re.compile(r"\buseful for (?:fast|quick) revision\b|\bwith (?:a )?revision summary\b", re.I), "revision_summary"),
)

SUBTEMPLATE_SIGNALS: dict[str, tuple[re.Pattern[str], ...]] = {
    "mathematical": (
        re.compile(r"\b(?:theorem|proof|lemma|calculus|integral|integration|derivative|linear algebra|matrix|matrices|eigen|bayes|probability|stochastic|differential equation|optimization|gradient descent|sgd|rmsprop|adam|momentum|optimizer|backpropagation|entropy|thermodynamics|lagrangian|fourier|laplace|formula|equation|biot[\s–-]savart)\b", re.I),
    ),
    "computational": (
        re.compile(r"\b(?:python|numpy|pandas|pytorch|tensorflow|c\+\+|cpp|rust|java|javascript|typescript|sql|git|bash|cli|api|fastapi|rest|docker|kubernetes|algorithm|quicksort|mergesort|binary search|dijkstra|dynamic programming|binary tree|graph|transformer|neural network|cnn|vit|compiler|operating system|memory|cache|debug|implement|code|syntax)\b", re.I),
    ),
    "scientific": (
        re.compile(r"\b(?:physics|thermodynamics|electromagnetism|biot[\s–-]savart|magnetostatics|quantum|mechanics|chemistry|organic chemistry|reaction|molecule|biology|mitosis|meiosis|cellular respiration|genetics|dna|enzyme|neuroscience|ecology|geology|astronomy|photosynthesis|evolution|optics)\b", re.I),
    ),
    "historical": (
        re.compile(r"\b(?:history|historical|revolution|french revolution|world war|treaty|treaties|empire|dynasty|renaissance|cold war|industrial revolution|timeline|civil war|ancient|medieval|colonial)\b", re.I),
    ),
    "empirical": (
        re.compile(r"\b(?:paper|arxiv|ablation|benchmark|experiment|dataset|empirical|clinical trial|meta-analysis|p-value|regression study|survey data|evaluation metric|sota|baseline)\b", re.I),
    ),
    "conceptual": (
        re.compile(r"\b(?:economics|keynesian|monetarist|microeconomics|macroeconomics|philosophy|ethics|epistemology|law|constitutional|sociology|psychology|cognitive|framework|architecture|design pattern|management|strategy|governance|theory)\b", re.I),
    ),
}

ARTIFACT_PHRASE_MAP: tuple[tuple[re.Pattern[str], str, str | None], ...] = (
    (re.compile(r"formula[\s-]?sheet", re.I), "M3", "formula_sheet"),
    (re.compile(r"syntax[\s-]?reference|api[\s-]?(?:table|reference)", re.I), "M3", "syntax_reference"),
    (re.compile(r"command[\s-]?reference|cli[\s-]?reference", re.I), "M3", "command_reference"),
    (re.compile(r"atomic[\s-]?(?:note|card)", re.I), "M3", "atomic_card"),
    (re.compile(r"cheat[\s-]?sheet|quick[\s-]?reference", re.I), "M3", None),
    (re.compile(r"flashcards?", re.I), "M6", "flashcards"),
    (re.compile(r"mock[\s-]?exam|viva", re.I), "M6", "mock_exam"),
    (re.compile(r"practice[\s-]?(?:set|test)|quiz|assessment", re.I), "M6", None),
    (re.compile(r"worked[\s-]?(?:solutions?|examples?|problems?)", re.I), "M4", None),
    (re.compile(r"implementation[\s-]?guide", re.I), "M5", None),
    (re.compile(r"revision[\s-]?pack|exam[\s-]?revision", re.I), "M7", "revision_pack"),
    (re.compile(r"concept[\s-]?map", re.I), "M7", "concept_map"),
    (re.compile(r"paper[\s-]?breakdown", re.I), "M7", "paper_breakdown"),
    (re.compile(r"comparison", re.I), "M7", "comparison_guide"),
    (re.compile(r"study[\s-]?notes?", re.I), "M2", None),
    (re.compile(r"deep[\s-]?(?:learning[\s-]?)?notes?", re.I), "M1", None),
)

# ---------------------------------------------------------------------------
# Mechanism 2 — Constraint Precedence Hierarchy (Section 11)
# ---------------------------------------------------------------------------

CONSTRAINT_PRECEDENCE: tuple[str, ...] = (
    "runtime_safety",
    "explicit_user",
    "source_policy",
    "command_contract",
    "primary_master",
    "variant_specialization",
    "knowledge_type",
    "optional_module",
    "default_preference",
)

# ---------------------------------------------------------------------------
# Mechanism 3 — Template Capability Matrix (Section 12)
# ---------------------------------------------------------------------------

TEMPLATE_CAPABILITIES: dict[str, dict[str, str]] = {
    "M1": {
        "full_derivations": "supported",
        "compact_formulas": "optional",
        "code_implementation": "supported",
        "worked_problems": "supported",
        "visual_diagrams": "supported",
        "interactive_assessment": "optional",
        "source_order_preservation": "optional",
        "concept_maps": "optional",
        "revision_summaries": "supported",
    },
    "M2": {
        "full_derivations": "optional",
        "compact_formulas": "supported",
        "code_implementation": "optional",
        "worked_problems": "supported",
        "visual_diagrams": "supported",
        "interactive_assessment": "optional",
        "source_order_preservation": "required_for_variant",
        "concept_maps": "optional",
        "revision_summaries": "supported",
    },
    "M3": {
        "full_derivations": "incompatible_with_constraint",
        "compact_formulas": "required",
        "code_implementation": "optional",
        "worked_problems": "incompatible_with_constraint",
        "visual_diagrams": "optional",
        "interactive_assessment": "incompatible_with_constraint",
        "source_order_preservation": "optional",
        "concept_maps": "optional",
        "revision_summaries": "required",
    },
    "M4": {
        "full_derivations": "supported",
        "compact_formulas": "optional",
        "code_implementation": "optional",
        "worked_problems": "required",
        "visual_diagrams": "optional",
        "interactive_assessment": "incompatible_with_constraint",
        "source_order_preservation": "optional",
        "concept_maps": "optional",
        "revision_summaries": "optional",
    },
    "M5": {
        "full_derivations": "optional",
        "compact_formulas": "optional",
        "code_implementation": "required",
        "worked_problems": "supported",
        "visual_diagrams": "supported",
        "interactive_assessment": "optional",
        "source_order_preservation": "optional",
        "concept_maps": "optional",
        "revision_summaries": "optional",
    },
    "M6": {
        "full_derivations": "optional",
        "compact_formulas": "optional",
        "code_implementation": "optional",
        "worked_problems": "supported",
        "visual_diagrams": "optional",
        "interactive_assessment": "required",
        "source_order_preservation": "optional",
        "concept_maps": "optional",
        "revision_summaries": "optional",
    },
    "M7": {
        "full_derivations": "optional",
        "compact_formulas": "supported",
        "code_implementation": "optional",
        "worked_problems": "optional",
        "visual_diagrams": "supported",
        "interactive_assessment": "optional",
        "source_order_preservation": "optional",
        "concept_maps": "required_for_variant",
        "revision_summaries": "required",
    },
}

# ---------------------------------------------------------------------------
# Mechanism 4 — Instruction Authority Graph (Section 13)
# ---------------------------------------------------------------------------

AUTHORITY_GRAPH: dict[str, dict[str, Any]] = {
    "product_selection": {
        "owner": "orchestration_engine",
        "module": "scriptorium.engines.orchestration",
        "spec": "references/routing/master-registry.yaml",
    },
    "research_and_evidence": {
        "owner": "research_engine",
        "module": "scriptorium.engines.research",
        "spec": "references/workflows/research/research-policy-registry.json",
    },
    "concept_identity_and_traceability": {
        "owner": "knowledge_engine",
        "module": "scriptorium.engines.knowledge",
        "spec": "references/workflows/research/source-fidelity.md",
    },
    "instructional_depth_and_modules": {
        "owner": "pedagogy_engine",
        "module": "scriptorium.engines.pedagogy",
        "spec": "references/workflows/notes-creation/instructional-registry.json",
    },
    "output_composition_rules": {
        "owner": "master_template",
        "module": "scriptorium.layout",
        "spec": "references/templates/masters/README.md",
    },
    "note_metadata_and_lifecycle": {
        "owner": "vault_engine",
        "module": "scriptorium.engines.vault",
        "spec": "references/metadata/properties-policy.md",
    },
    "validation_and_repair": {
        "owner": "quality_engine",
        "module": "scriptorium.engines.quality",
        "spec": "references/workflows/validation/verification-checklist.md",
    },
}

SECRET_PATTERNS = (
    re.compile(r"(?:api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[\w\-/.+=]{8,}['\"]?", re.I),
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
)


def load_master_registry(root: Path = ROOT) -> dict[str, Any]:
    path = root / "references" / "routing" / "master-registry.yaml"
    return _parse_master_registry(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=4)
def _parse_master_registry(raw: str) -> dict[str, Any]:
    """Cache parsing by content, so edits cannot reuse a stale authority registry."""
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise TemplateResolutionError("Master registry must be a YAML mapping.")
    return data


def _resolve_artifact_phrase(phrase: str) -> tuple[str, str | None]:
    for pattern, master, variant in ARTIFACT_PHRASE_MAP:
        if pattern.search(phrase):
            return master, variant
    return "M1", None


def validate_registry(root: Path = ROOT, *, require_retired_legacy: bool = True) -> dict[str, Any]:
    """Validate master-registry.yaml integrity, file existence, and legacy retirement."""
    errors: list[str] = []
    registry_file = root / "references" / "routing" / "master-registry.yaml"
    if not registry_file.is_file():
        return {"valid": False, "errors": [f"Missing master registry: {registry_file}"]}
    reg = yaml.safe_load(registry_file.read_text(encoding="utf-8"))
    if not isinstance(reg, dict):
        return {"valid": False, "errors": ["master-registry.yaml must be a mapping."]}

    masters = reg.get("masters") or {}
    if tuple(masters.keys()) != CANONICAL_MASTER_IDS:
        errors.append(f"Expected masters {list(CANONICAL_MASTER_IDS)}, found {list(masters.keys())}.")

    seen_ids: set[str] = set()
    seen_routes: set[str] = set()
    for mid, spec in masters.items():
        if not isinstance(spec, dict):
            errors.append(f"{mid}: specification must be a mapping.")
            continue
        for key in ("id", "route", "name", "path", "primary_intent"):
            if not spec.get(key):
                errors.append(f"{mid}: missing required key '{key}'.")
        if spec.get("id") in seen_ids:
            errors.append(f"{mid}: duplicate master id '{spec.get('id')}'.")
        seen_ids.add(str(spec.get("id", "")))
        if spec.get("route") in seen_routes:
            errors.append(f"{mid}: duplicate master route '{spec.get('route')}'.")
        seen_routes.add(str(spec.get("route", "")))
        rel_path = str(spec.get("path", ""))
        if rel_path.startswith("templates/"):
            errors.append(f"{mid}: path '{rel_path}' still points to retired top-level templates/.")
        elif not (root / rel_path).is_file():
            errors.append(f"{mid}: master template file not found: {rel_path}")

    variants = reg.get("variants") or {}
    for vid, vspec in variants.items():
        parent = vspec.get("parent_master")
        if parent not in masters:
            errors.append(f"variant '{vid}': invalid parent_master '{parent}'.")
        rel_path = str(vspec.get("path", ""))
        if rel_path.startswith("templates/"):
            errors.append(f"variant '{vid}': path '{rel_path}' still points to retired top-level templates/.")
        elif not (root / rel_path).is_file():
            errors.append(f"variant '{vid}': file not found: {rel_path}")

    subtemplates = reg.get("subtemplates") or {}
    modules = reg.get("modules") or {}
    for sid, sspec in subtemplates.items():
        rel_path = str(sspec.get("path", ""))
        if not (root / rel_path).is_file():
            errors.append(f"subtemplate '{sid}': file not found: {rel_path}")
        for cm in sspec.get("compatible_masters") or []:
            if cm not in masters:
                errors.append(f"subtemplate '{sid}': invalid compatible_master '{cm}'.")
        for rm in sspec.get("required_modules") or []:
            if modules and rm not in modules:
                errors.append(f"subtemplate '{sid}': unregistered required_module '{rm}'.")

    for mod_id, mspec in modules.items():
        spec_path = str(mspec.get("spec", ""))
        if spec_path and not (root / spec_path).is_file():
            errors.append(f"module '{mod_id}': spec file not found: {spec_path}")
        for cm in mspec.get("compatible_masters") or []:
            if cm not in masters:
                errors.append(f"module '{mod_id}': invalid compatible_master '{cm}'.")
        for dep in mspec.get("depends_on") or []:
            if dep not in modules:
                errors.append(f"module '{mod_id}': unknown dependency '{dep}'.")
            elif dep == mod_id:
                errors.append(f"module '{mod_id}': self-dependency cycle.")

    for mid, spec in masters.items():
        for dm in spec.get("default_modules") or []:
            if modules and dm not in modules:
                errors.append(f"{mid}: default_module '{dm}' is not registered in modules.")

    commands = reg.get("command_mappings") or {}
    for cmd, cspec in commands.items():
        cmaster = cspec.get("master")
        cvariant = cspec.get("variant")
        if cmaster is not None and cmaster not in masters:
            errors.append(f"command '{cmd}': unknown master '{cmaster}'.")
        if cvariant is not None:
            if cvariant not in variants:
                errors.append(f"command '{cmd}': unknown variant '{cvariant}'.")
            elif cmaster and variants[cvariant].get("parent_master") != cmaster:
                errors.append(f"command '{cmd}': variant '{cvariant}' does not belong to {cmaster}.")

    retired_commands = reg.get("retired_commands") or {}
    for cmd, rspec in retired_commands.items():
        if cmd in commands:
            errors.append(f"retired_command '{cmd}' must not also appear in active command_mappings.")
        rmaster = rspec.get("equivalent_master")
        rvariant = rspec.get("equivalent_variant")
        if rmaster is not None and rmaster not in masters:
            errors.append(f"retired_command '{cmd}': unknown equivalent_master '{rmaster}'.")
        if rvariant is not None and rvariant not in variants:
            errors.append(f"retired_command '{cmd}': unknown equivalent_variant '{rvariant}'.")

    if require_retired_legacy and (root / "templates").exists():
        errors.append("Legacy top-level templates/ directory still exists; retire it into references/templates/.")

    return {
        "valid": not errors,
        "masters_count": len(masters),
        "variants_count": len(variants),
        "subtemplates_count": len(subtemplates),
        "modules_count": len(modules),
        "commands_count": len(commands),
        "retired_commands_count": len(retired_commands),
        "errors": errors,
    }


def master_to_compat_route(master: str | None, variant: str | None = None, *, root: Path = ROOT) -> str | None:
    if master is None:
        return None
    reg = load_master_registry(root)
    if variant and variant in (reg.get("variants") or {}):
        legacy = reg["variants"][variant].get("legacy_route")
        if legacy:
            return legacy
    spec = (reg.get("masters") or {}).get(master)
    if not spec:
        return None
    legacy_routes = spec.get("legacy_routes") or []
    return legacy_routes[0] if legacy_routes else spec["route"]


def route_to_master(route: str | None, *, root: Path = ROOT) -> tuple[str | None, str | None]:
    if not route:
        return None, None
    norm = route.strip().lower().replace("_", "-")
    reg = load_master_registry(root)
    if norm.upper() in (reg.get("masters") or {}):
        return norm.upper(), None
    for vid, vspec in (reg.get("variants") or {}).items():
        if norm in {vid.replace("_", "-"), vspec.get("legacy_route", "")}:
            return vspec["parent_master"], vid
    for mid, mspec in (reg.get("masters") or {}).items():
        candidates = {
            mspec["id"].replace("_", "-"),
            mspec["route"],
            *(r.lower() for r in (mspec.get("legacy_routes") or [])),
        }
        if norm in candidates:
            return mid, None
    return None, None


def detect_knowledge_types(text: str) -> list[str]:
    detected: list[str] = []
    for subtemplate, patterns in SUBTEMPLATE_SIGNALS.items():
        if any(p.search(text) for p in patterns):
            detected.append(subtemplate)
    return detected or ["conceptual"]


def _strip_negations(text: str) -> tuple[str, list[str], set[str]]:
    negated_phrases: list[str] = []
    negated_masters: set[str] = set()
    cleaned = text
    for pattern in NEGATION_CLAUSES:
        def _repl(match: re.Match[str]) -> str:
            phrase = match.group(1).strip().lower()
            negated_phrases.append(phrase)
            first_word = re.split(r"[\s-]+", phrase)[0]
            for prefix, master in NEGATION_TO_MASTER.items():
                if first_word.startswith(prefix):
                    negated_masters.add(master)
                    break
            return " "
        cleaned = pattern.sub(_repl, cleaned)
    return re.sub(r"\s+", " ", cleaned).strip(), negated_phrases, negated_masters


def _extract_embedded_secondary(text: str) -> tuple[str, list[str]]:
    secondary: list[str] = []
    cleaned = text
    for pattern, module_id in EMBEDDED_SECONDARY_PATTERNS:
        if pattern.search(cleaned):
            if module_id not in secondary:
                secondary.append(module_id)
            cleaned = pattern.sub(" ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip(), secondary


def _detect_source_policy(text: str, explicit_policy: str | None, has_source: bool) -> tuple[str, str, bool]:
    strict_hit = any(p.search(text) for p in STRICT_SOURCE_PATTERNS)
    order_hit = any(p.search(text) for p in SOURCE_ORDER_PATTERNS)
    if explicit_policy:
        pol = explicit_policy.strip().lower()
    elif strict_hit:
        pol = "strict"
    elif has_source or order_hit:
        pol = "source_first"
    else:
        pol = "adaptive"

    if pol == "strict":
        rmode = "R-S0"
    elif pol == "source_first":
        rmode = "R-S1"
    else:
        rmode = "R-I"
    return pol, rmode, order_hit


def _detect_explicit_template_override(payload: str, root: Path = ROOT) -> tuple[str | None, str | None, str | None]:
    reg = load_master_registry(root)
    tokens: list[str] = list(CANONICAL_MASTER_IDS)
    for mspec in (reg.get("masters") or {}).values():
        tokens.append(mspec["route"])
        tokens.append(mspec["id"])
        tokens.extend(mspec.get("legacy_routes") or [])
    for vid, vspec in (reg.get("variants") or {}).items():
        tokens.append(vid)
        tokens.append(vid.replace("_", "-"))
        if vspec.get("legacy_route"):
            tokens.append(vspec["legacy_route"])
    ordered = "|".join(re.escape(t) for t in sorted(set(tokens), key=len, reverse=True))
    quote = r"""[`"']?"""
    match = re.search(
        rf"\b(?:template|master)\s*[:=]\s*{quote}({ordered}){quote}(?![\w-])"
        rf"|\buse (?:the )?{quote}({ordered}){quote}\s+(?:template|master)\b",
        payload,
        re.I,
    )
    if not match:
        return None, None, None
    raw = (match.group(1) or match.group(2)).strip()
    master, variant = route_to_master(raw, root=root)
    return master, variant, raw


def _detect_separate_artifacts(cleaned: str) -> list[tuple[str, str | None]]:
    found: list[tuple[str, str | None]] = []
    both_match = SEPARATE_MULTI_PATTERNS[1].search(cleaned)
    if both_match:
        for grp in (both_match.group(1), both_match.group(2)):
            pair = _resolve_artifact_phrase(grp)
            if pair not in found:
                found.append(pair)
        return found
    for match in SEPARATE_MULTI_PATTERNS[0].finditer(cleaned):
        pair = _resolve_artifact_phrase(match.group(1))
        if pair not in found:
            found.append(pair)
    return found


def _classify_primary_intent(
    text: str,
    *,
    sources: list[str],
    standalone_url: bool,
    has_source: bool,
    source_order_hit: bool,
    negated_masters: set[str],
) -> tuple[str, str | None, str]:
    if standalone_url and sources:
        parsed = urlsplit(sources[0])
        host = (parsed.hostname or "").removeprefix("www.")
        prefixes = PAPER_PATHS.get(host, ())
        is_paper = parsed.path != "/" and parsed.path.startswith(prefixes)
        if is_paper and "M7" not in negated_masters:
            return "M7", "paper_breakdown", "standalone research paper URL"
        if "M7" not in negated_masters:
            return "M7", "quick_summary", "standalone external source URL"

    if "M3" not in negated_masters:
        if re.search(r"\bformula[\s-]?sheet\b|\bequation[\s-]?sheet\b", text, re.I):
            return "M3", "formula_sheet", "explicit formula sheet request"
        if re.search(r"\b(?:syntax|api)[\s-]?(?:reference|table|sheet|guide)\b|\blookup table\b", text, re.I):
            return "M3", "syntax_reference", "explicit syntax/API reference request"
        if re.search(r"\b(?:command|cli)[\s-]?(?:reference|cheat[\s-]?sheet|sheet|guide)\b", text, re.I):
            return "M3", "command_reference", "explicit CLI/command reference request"
        if re.search(r"\batomic[\s-]?(?:note|card)\b", text, re.I):
            return "M3", "atomic_card", "explicit atomic concept card request"
        if re.search(r"\bcheat[\s-]?sheet\b|\bquick[\s-]?reference\b|\bcrisp reference\b", text, re.I):
            if re.search(r"\b(?:formulas?|equations?)\b", text, re.I):
                return "M3", "formula_sheet", "explicit formula cheat sheet request"
            return "M3", None, "explicit cheat sheet / quick reference request"

    if "M6" not in negated_masters:
        if re.search(r"\bflashcards?\b|\banki\s+cards?\b", text, re.I):
            return "M6", "flashcards", "explicit flashcards request"
        if re.search(r"\bmock[\s-]?exam\b|\bviva\b|\boral[\s-]?exam\b|\bsample[\s-]?exam\b", text, re.I):
            return "M6", "mock_exam", "explicit mock exam / viva preparation request"
        if re.search(
            r"\b(?:practice[\s-]?(?:test|set|problems?|questions?|exercises?|assessment)|quiz|self-test|test myself|assess my|active[\s-]?recall|drill questions?|diagnostic questions?)\b",
            text,
            re.I,
        ):
            return "M6", None, "explicit practice or self-assessment request"

    # Explicit comprehensive/deep learning notes outrank embedded supporting phrases ("including worked examples and Python implementation")
    if "M1" not in negated_masters:
        if re.search(
            r"\b(?:comprehensive|deep(?:[\s-]learning)?|detailed|first[\s-]?principles)\s+(?:study\s+)?notes?\b",
            text,
            re.I,
        ):
            return "M1", None, "explicit comprehensive deep-learning notes request"

    if "M4" not in negated_masters:
        if re.search(
            r"\b(?:worked[\s-]?(?:solutions?|examples?|problems?)|step-by-step\s+solutions?|"
            r"solve\s+(?:these|the|my|\d+|a\s+set\s+of)?\s*(?:[\w-]+\s+){0,4}(?:problems?|exercises?|questions?|integrals?|equations?)|"
            r"walk\s+through\s+(?:solving|these\s+problems?)|show\s+(?:full\s+)?worked\s+(?:solutions?|examples?))\b",
            text,
            re.I,
        ):
            if not re.search(r"\bin\s+(?:c\+\+(?:20)?|cpp|python(?:3)?|rust|java|go|typescript|javascript)\b", text, re.I):
                return "M4", None, "explicit worked problem-solving request"

    if "M5" not in negated_masters:
        # "Make notes from scratch" and "teach/explain <X> from scratch" are M1/M2, NOT M5!
        is_notes_or_teach_from_scratch = bool(
            re.search(
                r"\b(?:make|write|create)\s+(?:deep\s+|study\s+)?notes\s+from\s+scratch\b"
                r"|\b(?:teach(?:\s+me)?|explain|learn|understand)\b[^.!?\n]*\bfrom\s+scratch\b",
                text,
                re.I,
            )
        ) and not bool(
            re.search(r"\b(?:implement|build|code|program|develop)\b", text, re.I)
        )
        if not is_notes_or_teach_from_scratch and re.search(
            r"\b(?:implement(?:ation)?(?:\s+guide)?|build\s+(?:a|an|the)\b|"
            r"(?:implement|build|code|program|develop|engineer)\b[^.!?\n]*\bfrom\s+scratch\b|"
            r"from\s+scratch\s+in\s+(?:c\+\+(?:20)?|cpp|python(?:3)?|numpy|pytorch|tensorflow|rust|java|go|typescript|javascript|c)\b|"
            r"debug(?:ging)?|troubleshoot(?:ing)?|deploy(?:ment)?\s+guide|code\s+walkthrough|"
            r"write\s+(?:a|an|the)?\s*(?:[\w-]+\s+){0,2}(?:script|service|api|pipeline|parser|classifier|solver|module)|"
            r"solve\b.*\bin\s+(?:c\+\+(?:20)?|cpp|python(?:3)?|rust|java|go|typescript|javascript)\b)\b",
            text,
            re.I,
        ):
            return "M5", None, "practical implementation, build, or debugging objective"

    if "M7" not in negated_masters:
        if re.search(r"\bcompare\b.+\b(?:vs\.?|versus|and|with|against)\b|\btrade-?offs?\s+between\b|\bvs\.?\b", text, re.I):
            return "M7", "comparison_guide", "comparative synthesis request"
        if re.search(r"\bpaper[\s-]?breakdown\b|\bbreak[\s-]?down\s+(?:this|the)\s+paper\b|\bdeconstruct\s+(?:this|the)\s+paper\b", text, re.I):
            return "M7", "paper_breakdown", "research paper breakdown request"
        if re.search(r"\bconcept[\s-]?map\b|\bknowledge[\s-]?map\b|\brelationship[\s-]?map\b", text, re.I):
            return "M7", "concept_map", "concept relationship map request"
        if re.search(r"\brevision[\s-]?(?:pack|guide|sheet)\b|\bexam[\s-]?(?:revision|review|prep\s+pack)\b|\bconsolidat(?:e|ion)\b|\bsynthesi[sz]e\b", text, re.I):
            return "M7", "revision_pack", "consolidation / exam revision pack request"
        if re.search(r"^\s*(?:please\s+)?summari[sz]e\b|\bquick[\s-]?summary\b|\bsummary\s+of\b", text, re.I):
            return "M7", "quick_summary", "source or topic summary request"

    if "M2" not in negated_masters:
        if re.search(r"\bstudy[\s-]?notes?\b|\bstudy[\s-]?guide\b|\bcourse[\s-]?notes?\b|\blecture[\s-]?notes?\b|\bchapter[\s-]?notes?\b|\bsyllabus[\s-]?notes?\b", text, re.I):
            variant = "lecture_order" if (source_order_hit or has_source) else None
            return "M2", variant, "structured study or course notes request"
        if (has_source or source_order_hit) and re.search(r"\b(?:make|take|create|write|turn|convert|give)\b.*\bnotes?\b", text, re.I):
            return "M2", "lecture_order", "source-preserving sequential study notes request"

    if "M3" not in negated_masters and re.search(r"\b(?:quick|brief|short)\b[^.!?\n]{0,100}\breminder\b", text, re.I):
        return "M3", None, "explicit brief reminder request"

    if "M1" not in negated_masters:
        if re.search(r"\b(?:deep(?:ly)?|first[\s-]?principles|detailed\s+explanations?|comprehensive|from\s+the\s+ground\s+up|master|understand\s+deeply|explain|teach\s+me|deep[\s-]?dive)\b", text, re.I):
            return "M1", None, "deep first-principles learning objective"
        return "M1", None, "default comprehensive learning master"

    return "M2", ("lecture_order" if source_order_hit else None), "fallback after M1 negation"


def _build_artifact_entry(
    master: str,
    variant: str | None,
    *,
    secondary_modules: list[str],
    knowledge_types: list[str],
    source_policy: str,
    research_mode: str,
    reason: str,
    root: Path = ROOT,
) -> dict[str, Any]:
    reg = load_master_registry(root)
    mspec = reg["masters"][master]
    vspec = (reg.get("variants") or {}).get(variant) if variant else None
    compat_route = master_to_compat_route(master, variant, root=root)
    return {
        "master": master,
        "master_id": mspec["id"],
        "master_route": mspec["route"],
        "master_name": mspec["name"],
        "template_path": vspec["path"] if vspec else mspec["path"],
        "master_path": mspec["path"],
        "variant": variant,
        "variant_path": vspec["path"] if vspec else None,
        "compat_route": compat_route,
        "knowledge_types": list(knowledge_types),
        "subtemplate_paths": [reg["subtemplates"][kt]["path"] for kt in knowledge_types if kt in reg["subtemplates"]],
        "default_modules": list(mspec.get("default_modules") or []),
        "secondary_modules": list(secondary_modules),
        "source_policy": source_policy,
        "research_mode": research_mode,
        "reason": reason,
    }


def route_request(
    request: str,
    *,
    source_policy: str | None = None,
    has_source: bool = False,
    existing_command: str | None = None,
    root: Path = ROOT,
) -> dict[str, Any]:
    raw = request.strip()
    if not raw:
        raise RoutingError("Provide a non-empty request to route.")

    reg = load_master_registry(root)
    cmd_map = reg.get("command_mappings") or {}
    retired_map = reg.get("retired_commands") or {}

    first, *rest = raw.split(maxsplit=1)
    parsed_cmd = first.lower().lstrip("/")
    is_retired_cmd = parsed_cmd in retired_map
    if existing_command:
        command = existing_command
    elif parsed_cmd in cmd_map:
        command = parsed_cmd
    elif is_retired_cmd:
        command = parsed_cmd
    else:
        command = None

    has_cmd_prefix = parsed_cmd in cmd_map or is_retired_cmd
    payload = rest[0] if (has_cmd_prefix and rest) else ("" if has_cmd_prefix else raw)

    migration_hint: str | None = None
    if command and command in retired_map:
        rspec = retired_map[command]
        migration_hint = str(
            rspec.get("migration_hint")
            or f"Command '/{command}' has been unified into '/scribe-notes'. Use '/scribe-notes <topic or request>' instead."
        )

    sources = [m.group().rstrip(".,;") for m in URL_RE.finditer(payload)]
    standalone_url = bool(URL_RE.fullmatch(payload.strip("<>"))) if payload else False
    effective_has_source = has_source or bool(sources)

    resolved_source_policy, research_mode, source_order_hit = _detect_source_policy(
        payload or raw, source_policy, effective_has_source
    )
    knowledge_types = detect_knowledge_types(payload or raw)
    cleaned_neg, negated_phrases, negated_masters = _strip_negations(payload or raw)
    cleaned_intent, secondary_modules = _extract_embedded_secondary(cleaned_neg)

    mode = "author"
    lock: str | None = None
    explicit_master, explicit_variant, explicit_raw = _detect_explicit_template_override(payload, root=root)

    # Non-note active commands (doubt, setfolder, quiz) and retired command compatibility
    if command and command in cmd_map and command != "scribe-notes":
        cspec = cmd_map[command]
        mode = cspec.get("mode", "author")
        cmaster = cspec.get("master")
        cvariant = cspec.get("variant")
        if command in {"scribe-doubt", "scribe-setfolder"}:
            return {
                "command": command,
                "mode": mode,
                "master": cmaster,
                "variant": cvariant,
                "compat_route": cspec.get("legacy_route"),
                "lock": None,
                "multi_artifact": False,
                "shared_context": False,
                "source_policy": resolved_source_policy,
                "research_mode": research_mode,
                "knowledge_types": knowledge_types,
                "artifacts": [],
                "routing_trace": {
                    "priority_level": 1,
                    "decision_basis": f"explicit command /{command}",
                    "negated_artifacts": negated_phrases,
                    "secondary_modules": secondary_modules,
                    "source_order_preserved": source_order_hit,
                },
            }
        if command == "scribe-quiz":
            lock = "command"
            primary_master, primary_variant = cmaster, cvariant
            reason = "explicit command /scribe-quiz"
            artifacts = [
                _build_artifact_entry(
                    primary_master,
                    primary_variant,
                    secondary_modules=secondary_modules,
                    knowledge_types=knowledge_types,
                    source_policy=resolved_source_policy,
                    research_mode=research_mode,
                    reason=reason,
                    root=root,
                )
            ]
            return {
                "command": command,
                "mode": mode,
                "master": primary_master,
                "variant": primary_variant,
                "compat_route": artifacts[0]["compat_route"],
                "lock": lock,
                "multi_artifact": False,
                "shared_context": False,
                "source_policy": resolved_source_policy,
                "research_mode": research_mode,
                "knowledge_types": knowledge_types,
                "artifacts": artifacts,
                "routing_trace": {
                    "priority_level": 1,
                    "decision_basis": reason,
                    "negated_artifacts": negated_phrases,
                    "secondary_modules": secondary_modules,
                    "source_order_preserved": source_order_hit,
                },
            }

    if command and command in retired_map:
        rspec = retired_map[command]
        rmaster = rspec.get("equivalent_master")
        rvariant = rspec.get("equivalent_variant")
        if command == "scribe-expand" or rmaster is None:
            return {
                "command": command,
                "retired_command": command,
                "migration_hint": migration_hint,
                "mode": "author",
                "master": None,
                "variant": None,
                "compat_route": None,
                "lock": None,
                "multi_artifact": False,
                "shared_context": False,
                "source_policy": resolved_source_policy,
                "research_mode": research_mode,
                "knowledge_types": knowledge_types,
                "artifacts": [],
                "routing_trace": {
                    "priority_level": 1,
                    "decision_basis": f"retired command /{command} -> /scribe-notes migration",
                    "negated_artifacts": negated_phrases,
                    "secondary_modules": secondary_modules,
                    "source_order_preserved": source_order_hit,
                },
            }
        if explicit_master:
            primary_master, primary_variant = explicit_master, explicit_variant
            lock = "explicit"
            reason = f"explicit template override '{explicit_raw}' via retired /{command}"
        elif standalone_url and command == "scribe-deepnotes":
            parsed = urlsplit(sources[0])
            host = (parsed.hostname or "").removeprefix("www.")
            is_paper = parsed.path != "/" and parsed.path.startswith(PAPER_PATHS.get(host, ()))
            lock = "source"
            primary_master = "M7"
            primary_variant = "paper_breakdown" if is_paper else "quick_summary"
            reason = "standalone source URL via retired /scribe-deepnotes"
        else:
            primary_master, primary_variant = rmaster, rvariant
            lock = "command" if command in {"scribe-dsa", "scribe-practice", "scribe-distill", "scribe-compare", "scribe-atomic-notes"} else None
            reason = f"retired command /{command} mapped to {primary_master} (prefer /scribe-notes)"
        artifacts = [
            _build_artifact_entry(
                primary_master,
                primary_variant,
                secondary_modules=secondary_modules,
                knowledge_types=knowledge_types,
                source_policy=resolved_source_policy,
                research_mode=research_mode,
                reason=reason,
                root=root,
            )
        ]
        return {
            "command": command,
            "retired_command": command,
            "migration_hint": migration_hint,
            "mode": "author",
            "master": primary_master,
            "variant": primary_variant,
            "compat_route": artifacts[0]["compat_route"],
            "lock": lock,
            "multi_artifact": False,
            "shared_context": False,
            "source_policy": resolved_source_policy,
            "research_mode": research_mode,
            "knowledge_types": knowledge_types,
            "artifacts": artifacts,
            "routing_trace": {
                "priority_level": 1 if lock == "command" else 2,
                "decision_basis": reason,
                "negated_artifacts": negated_phrases,
                "secondary_modules": secondary_modules,
                "source_order_preserved": source_order_hit or primary_variant == "lecture_order",
            },
        }

    # Universal /scribe-notes or natural-language author request: dynamic routing across ALL M1-M7
    effective_cmd = "scribe-notes" if command == "scribe-notes" else None

    if explicit_master:
        art = _build_artifact_entry(
            explicit_master,
            explicit_variant,
            secondary_modules=secondary_modules,
            knowledge_types=knowledge_types,
            source_policy=resolved_source_policy,
            research_mode=research_mode,
            reason=f"explicit template override '{explicit_raw}'",
            root=root,
        )
        return {
            "command": effective_cmd,
            "mode": "author",
            "master": explicit_master,
            "variant": explicit_variant,
            "compat_route": art["compat_route"],
            "lock": "explicit",
            "multi_artifact": False,
            "shared_context": False,
            "source_policy": resolved_source_policy,
            "research_mode": research_mode,
            "knowledge_types": knowledge_types,
            "artifacts": [art],
            "routing_trace": {
                "priority_level": 2,
                "decision_basis": art["reason"],
                "negated_artifacts": negated_phrases,
                "secondary_modules": secondary_modules,
                "source_order_preserved": source_order_hit or explicit_variant == "lecture_order",
            },
        }

    if effective_cmd == "scribe-notes" and not payload.strip():
        art = _build_artifact_entry(
            "M1",
            None,
            secondary_modules=[],
            knowledge_types=knowledge_types,
            source_policy=resolved_source_policy,
            research_mode=research_mode,
            reason="bare /scribe-notes awaiting topic specification",
            root=root,
        )
        return {
            "command": "scribe-notes",
            "mode": "author",
            "master": "M1",
            "variant": None,
            "compat_route": art["compat_route"],
            "lock": None,
            "multi_artifact": False,
            "shared_context": False,
            "source_policy": resolved_source_policy,
            "research_mode": research_mode,
            "knowledge_types": knowledge_types,
            "artifacts": [art],
            "routing_trace": {
                "priority_level": 5,
                "decision_basis": "bare /scribe-notes awaiting topic specification",
                "negated_artifacts": [],
                "secondary_modules": [],
                "source_order_preserved": False,
            },
        }

    extra_artifacts = _detect_separate_artifacts(cleaned_neg)
    primary_text = cleaned_intent
    for pat in SEPARATE_MULTI_PATTERNS:
        primary_text = pat.sub(" ", primary_text)
    primary_text = re.sub(r"\s+", " ", primary_text).strip()

    primary_master, primary_variant, primary_reason = _classify_primary_intent(
        primary_text or cleaned_intent,
        sources=sources,
        standalone_url=standalone_url,
        has_source=effective_has_source,
        source_order_hit=source_order_hit,
        negated_masters=negated_masters,
    )

    artifact_specs: list[tuple[str, str | None, str, list[str]]] = []
    if SEPARATE_MULTI_PATTERNS[1].search(cleaned_neg) and len(extra_artifacts) >= 2:
        for idx, (m, v) in enumerate(extra_artifacts):
            artifact_specs.append((m, v, "explicit multi-artifact request", secondary_modules if idx == 0 else []))
    else:
        artifact_specs.append((primary_master, primary_variant, primary_reason, secondary_modules))
        for m, v in extra_artifacts:
            if (m, v) != (primary_master, primary_variant):
                artifact_specs.append((m, v, "explicit separate companion artifact", []))

    artifacts = [
        _build_artifact_entry(
            m,
            v,
            secondary_modules=sec,
            knowledge_types=knowledge_types,
            source_policy=resolved_source_policy,
            research_mode=research_mode,
            reason=rsn,
            root=root,
        )
        for m, v, rsn, sec in artifact_specs
    ]

    multi = len(artifacts) > 1
    first_art = artifacts[0]
    inferred_lock = "source" if standalone_url else ("explicit" if first_art["master"] != "M1" else None)

    return {
        "command": effective_cmd,
        "mode": "author",
        "master": first_art["master"],
        "variant": first_art["variant"],
        "compat_route": first_art["compat_route"],
        "lock": inferred_lock,
        "multi_artifact": multi,
        "shared_context": multi,
        "source_policy": resolved_source_policy,
        "research_mode": research_mode,
        "knowledge_types": knowledge_types,
        "artifacts": artifacts,
        "routing_trace": {
            "priority_level": 2 if standalone_url else (3 if first_art["master"] != "M1" else 5),
            "decision_basis": first_art["reason"],
            "negated_artifacts": negated_phrases,
            "secondary_modules": secondary_modules,
            "source_order_preserved": source_order_hit or first_art["variant"] == "lecture_order",
            "artifact_count": len(artifacts),
        },
    }


# ---------------------------------------------------------------------------
# Mechanism 1 — Request Intent Normalization (Section 10)
# ---------------------------------------------------------------------------

def _extract_topic_phrase(raw: str, command: str | None) -> str:
    text = raw.strip()
    if command:
        parts = text.split(maxsplit=1)
        text = parts[1] if len(parts) > 1 else ""
    text = URL_RE.sub("", text).strip()
    # Strip trailing separate-artifact clause and exclusions
    text = re.split(r"\b(?:and\s+(?:also\s+)?(?:make|create|generate|include|a\s+separate|a\s+standalone)|but\s+|without\s+|using\s+only)\b", text, maxsplit=1, flags=re.I)[0]
    # Remove leading action/format verbs
    text = re.sub(
        r"^(?:please\s+)?(?:make|create|write|give\s+me|generate|explain|teach\s+me|build|implement|solve|compare|summari[sz]e|break\s+down)\s+"
        r"(?:me\s+)?(?:very\s+|detailed\s+|comprehensive\s+|deep\s+|structured\s+|quick\s+|compact\s+|source[- ]only\s+)*"
        r"(?:a\s+|an\s+|the\s+|these\s+\d*\s*)?"
        r"(?:deep[\s-]?learning[\s-]?notes?|study[\s-]?notes?|notes?|cheat[\s-]?sheet|formula[\s-]?sheet|"
        r"quick[\s-]?reference|syntax[\s-]?reference|command[\s-]?reference|atomic[\s-]?note|flashcards?|"
        r"practice[\s-]?(?:test|set|problems?)|mock[\s-]?exam|worked[\s-]?(?:solutions?|examples?)|"
        r"revision[\s-]?pack|concept[\s-]?map|paper[\s-]?breakdown|summary|implementation[\s-]?guide)?\s*"
        r"(?:on|about|for|of|from\s+scratch\s+(?:on|about|for|in)?)?\s*",
        "",
        text,
        flags=re.I,
    ).strip(" .,;:-")
    return text or raw.strip()


def normalize_request(
    request: str,
    *,
    source_policy: str | None = None,
    has_source: bool = False,
    root: Path = ROOT,
) -> dict[str, Any]:
    """Mechanism 1: Convert an unstructured user request into a normalized intent contract."""
    routed = route_request(request, source_policy=source_policy, has_source=has_source, root=root)
    raw = request.strip()
    cleaned_neg, negated_phrases, _ = _strip_negations(raw)

    # Detect requested depths
    math_depth = "deep" if re.search(r"\b(?:all the math|full derivations?|proof|rigorous math|all equations|all formulas)\b", cleaned_neg, re.I) else (
        "detailed" if re.search(r"\b(?:equations?|formulas?|math|derivations?)\b", cleaned_neg, re.I) else "standard"
    )
    conceptual_depth = "deep" if re.search(r"\b(?:very detailed|comprehensive|deep(?:ly)?|first[\s-]?principles|entire|exhaustive)\b", cleaned_neg, re.I) else "standard"
    code_depth = "none" if any("code" in n or "coding" in n for n in negated_phrases) else (
        "detailed" if re.search(r"\b(?:python|numpy|pytorch|c\+\+|cpp|rust|code|implement|script|fastapi)\b", cleaned_neg, re.I) else "minimal"
    )

    audience = "beginner" if re.search(r"\b(?:beginner|introductory|from scratch|simple|elI5)\b", raw, re.I) else (
        "advanced" if re.search(r"\b(?:advanced|graduate|research[- ]level|rigorous)\b", raw, re.I) else "intermediate"
    )

    required_elements: list[str] = []
    for pat, label in (
        (r"\b(?:worked\s+)?examples?\b", "worked_examples"),
        (r"\b(?:computational\s+graph|diagram|visual)\b", "visual_diagrams"),
        (r"\b(?:python|numpy|pytorch|code|implementation)\b", "code_implementation"),
        (r"\b(?:all\s+(?:the\s+)?(?:formulas?|equations?)|every\s+formula)\b", "all_source_formulas"),
        (r"\b(?:derivations?|proofs?)\b", "derivations"),
        (r"\b(?:fast|quick)\s+revision\b", "revision_summary"),
    ):
        if re.search(pat, cleaned_neg, re.I):
            required_elements.append(label)

    reg = load_master_registry(root)
    requested_outputs = [reg["masters"][a["master"]]["route"] for a in routed["artifacts"]]
    primary_master = routed["master"] or "M1"
    primary_goal = reg["masters"][primary_master]["primary_intent"] if primary_master in reg["masters"] else "comprehensive_learning"

    topic = _extract_topic_phrase(raw, routed.get("command"))
    ambiguity: list[str] = []
    if len(topic.split()) <= 1 and not routed.get("command") and routed["lock"] is None:
        ambiguity.append("broad_single_token_topic")
    if re.search(r"\b(?:this|the)\s+(?:lecture|pdf|chapter|paper|slides)\b", raw, re.I) and not (has_source or URL_RE.search(raw)):
        ambiguity.append("missing_referenced_source")

    return {
        "topic": topic,
        "primary_goal": primary_goal,
        "command": routed.get("command"),
        "requested_outputs": requested_outputs,
        "artifacts": routed["artifacts"],
        "artifact_relationship": {
            "separate_files": routed["multi_artifact"],
            "shared_context": routed["shared_context"],
            "artifact_count": len(routed["artifacts"]),
        },
        "depth": {
            "conceptual": conceptual_depth,
            "mathematical": math_depth,
            "coding": code_depth,
        },
        "audience": audience,
        "knowledge_types": routed["knowledge_types"],
        "constraints": {
            "source_policy": routed["source_policy"],
            "research_mode": routed["research_mode"],
            "preserve_source_order": bool(routed["routing_trace"].get("source_order_preserved")),
            "has_source": has_source or bool(URL_RE.search(raw)),
        },
        "required_elements": required_elements,
        "excluded_elements": negated_phrases,
        "secondary_modules": routed["routing_trace"].get("secondary_modules", []),
        "ambiguity": ambiguity,
        "routed": routed,
    }


# ---------------------------------------------------------------------------
# Mechanism 2 — Constraint Precedence Engine (Section 11)
# ---------------------------------------------------------------------------

def resolve_constraints(
    normalized_request: dict[str, Any],
    *,
    extra_constraints: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Mechanism 2: Resolve contradictions across safety, user, source policy, command, and template layers."""
    conflicts: list[dict[str, Any]] = []
    adaptations: list[str] = []
    req_elems = list(normalized_request.get("required_elements") or [])
    excl_elems = [e.lower() for e in (normalized_request.get("excluded_elements") or [])]
    constraints = normalized_request.get("constraints") or {}
    source_policy = constraints.get("source_policy", "adaptive")
    artifacts = normalized_request.get("artifacts") or []
    primary_master = artifacts[0]["master"] if artifacts else "M1"
    primary_variant = artifacts[0].get("variant") if artifacts else None

    # Conflict 1: Strict source-only policy vs request for exhaustive derivations/external expansion
    if source_policy == "strict" and "derivations" in req_elems:
        conflicts.append({
            "conflicting_requirements": ["source_policy: strict (R-S0)", "explicit_user: explain all derivations"],
            "prevailing_layer": "source_policy",
            "reason": "Strict source-only policy forbids importing external derivations; derivations must stay strictly within supplied source premises and steps.",
            "adapted": True,
            "satisfies_user_objective": True,
        })
        adaptations.append("restrict_derivations_to_source_premises")

    # Conflict 2: Concise formula sheet (M3) vs include every formula from chapter
    if primary_master == "M3" and "all_source_formulas" in req_elems:
        conflicts.append({
            "conflicting_requirements": ["explicit_user: include every formula from chapter", "primary_master(M3): compact length preference"],
            "prevailing_layer": "explicit_user",
            "reason": "Explicit user coverage requirement outranks M3 compact length preference; keep prose terse while preserving all required source formulas.",
            "adapted": True,
            "satisfies_user_objective": True,
        })
        adaptations.append("preserve_all_source_formulas_with_compact_prose")

    # Conflict 3: Explicit user exclusion of examples vs master default worked_examples
    if any("example" in ex for ex in excl_elems):
        conflicts.append({
            "conflicting_requirements": ["explicit_user: exclude examples", f"primary_master({primary_master}): default worked_examples"],
            "prevailing_layer": "explicit_user",
            "reason": "Explicit user exclusion removes optional worked examples while preserving definitions and applicability conditions.",
            "adapted": True,
            "satisfies_user_objective": True,
        })
        adaptations.append("omit_worked_examples_per_user_exclusion")

    # Conflict 4: Custom caller-supplied instruction conflicts (e.g. module vs master)
    rank = {name: idx for idx, name in enumerate(CONSTRAINT_PRECEDENCE)}
    for item in extra_constraints or []:
        layer_a = str(item.get("layer_a", "primary_master"))
        layer_b = str(item.get("layer_b", "optional_module"))
        if layer_a not in rank or layer_b not in rank:
            raise SourcePolicyConflictError(f"Unknown constraint layer: {layer_a!r} vs {layer_b!r}")
        winner = layer_a if rank[layer_a] <= rank[layer_b] else layer_b
        conflicts.append({
            "conflicting_requirements": [
                f"{layer_a}: {item.get('rule_a', '')}",
                f"{layer_b}: {item.get('rule_b', '')}",
            ],
            "prevailing_layer": winner,
            "reason": f"Layer '{winner}' has higher precedence than '{layer_b if winner == layer_a else layer_a}' in CONSTRAINT_PRECEDENCE.",
            "adapted": True,
            "satisfies_user_objective": True,
        })

    return {
        "precedence_order": list(CONSTRAINT_PRECEDENCE),
        "primary_master": primary_master,
        "primary_variant": primary_variant,
        "effective_source_policy": source_policy,
        "conflicts": conflicts,
        "adaptations": adaptations,
        "resolved": True,
    }


# ---------------------------------------------------------------------------
# Mechanism 3 — Template Capability Matrix Validation (Section 12)
# ---------------------------------------------------------------------------

def validate_template_capabilities(
    master: str,
    requested_capabilities: list[str],
    *,
    variant: str | None = None,
) -> dict[str, Any]:
    """Mechanism 3: Validate whether requested capabilities are supported by the selected master."""
    if master not in TEMPLATE_CAPABILITIES:
        raise TemplateResolutionError(f"Unknown master ID: {master}")
    cap_map = TEMPLATE_CAPABILITIES[master]
    incompatibilities: list[dict[str, str]] = []
    warnings: list[str] = []
    supported: list[str] = []

    for cap in requested_capabilities:
        state = cap_map.get(cap)
        if state is None:
            warnings.append(f"Capability '{cap}' is not registered in TEMPLATE_CAPABILITIES.")
            continue
        if state == "incompatible_with_constraint":
            incompatibilities.append({
                "capability": cap,
                "master": master,
                "state": state,
                "recommendation": f"Keep '{cap}' compact or route to a companion artifact rather than bloating {master}.",
            })
        elif state == "required_for_variant" and variant is None:
            warnings.append(f"Capability '{cap}' is specialized for a variant under {master}.")
            supported.append(cap)
        else:
            supported.append(cap)

    return {
        "master": master,
        "variant": variant,
        "valid": not incompatibilities,
        "supported": supported,
        "incompatibilities": incompatibilities,
        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# Mechanism 4 — Instruction Authority Linting (Section 13)
# ---------------------------------------------------------------------------

RETIRED_SCRIPT_NAMES = (
    "scripts/contracts.py",
    "scripts/decision_matrix.py",
    "scripts/instructional_plan.py",
    "scripts/legacy_contract_adapter.py",
    "scripts/note_layout.py",
    "scripts/note_verification.py",
    "scripts/pedagogical_engine.py",
    "scripts/research_cache.py",
    "scripts/research_engine.py",
    "scripts/routing_engine.py",
    "scripts/audit_repository.py",
)

BARE_RETIRED_SCRIPT_NAMES = (
    "decision_matrix.py",
    "instructional_plan.py",
    "legacy_contract_adapter.py",
    "note_layout.py",
    "note_verification.py",
    "pedagogical_engine.py",
    "research_cache.py",
    "research_engine.py",
    "routing_engine.py",
    "audit_repository.py",
)


def lint_instruction_authority(root: Path = ROOT) -> dict[str, Any]:
    """Mechanism 4: Verify single-owner authority, no retired references, and consistent master registry."""
    issues: list[dict[str, str]] = []

    # 1. Verify master registry itself
    reg_res = validate_registry(root, require_retired_legacy=True)
    for err in reg_res.get("errors", []):
        issues.append({"type": "registry_error", "file": "references/routing/master-registry.yaml", "detail": err})

    # 2. Verify all authority specs exist
    for decision, info in AUTHORITY_GRAPH.items():
        spec_path = root / info["spec"]
        if not spec_path.is_file():
            issues.append({
                "type": "missing_authority_spec",
                "file": info["spec"],
                "detail": f"Authority spec for '{decision}' ({info['owner']}) is missing.",
            })

    # 3. Scan active instruction Markdown files for references to retired templates or retired scripts
    active_md_roots = [
        root / "SKILL.md",
        root / "router.md",
        root / "README.md",
        *sorted((root / "shared").glob("*.md")),
        *sorted((root / "skills").glob("*/SKILL.md")),
        *sorted((root / "references" / "routing").glob("*.md")),
        *sorted((root / "references" / "workflows").rglob("*.md")),
        *sorted((root / "references" / "templates").rglob("*.md")),
        *(sorted((root / "references" / "architecture").glob("*.md")) if (root / "references" / "architecture").is_dir() else []),
        *(sorted((root / "references" / "metadata").glob("*.md")) if (root / "references" / "metadata").is_dir() else []),
        *(sorted((root / "references" / "contracts").glob("*.md")) if (root / "references" / "contracts").is_dir() else []),
    ]
    retired_tpl_re = re.compile(r"(?<![a-z/])templates/[a-z][a-z0-9_-]+\.md")
    bare_script_res = [
        (name, re.compile(rf"(?<![a-zA-Z0-9_/]){re.escape(name)}\b"))
        for name in BARE_RETIRED_SCRIPT_NAMES
    ]
    for path in active_md_roots:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8-sig")
        rel = path.relative_to(root).as_posix()
        if rel == "references/contracts/migration-notes.md":
            # In the historical migration log, ignore explicit retirement arrows (`templates/... -> references/templates/...`)
            # and "Removed ..." ledger lines while still catching active stale paths.
            for line in text.splitlines():
                if "->" in line or re.match(r"^\s*-\s*Removed\b", line):
                    continue
                if m := retired_tpl_re.search(line):
                    issues.append({"type": "retired_template_reference", "file": rel, "detail": m.group(0)})
                    break
        elif m := retired_tpl_re.search(text):
            issues.append({"type": "retired_template_reference", "file": rel, "detail": m.group(0)})
        flagged_scripts: set[str] = set()
        for retired_script in RETIRED_SCRIPT_NAMES:
            if retired_script in text:
                issues.append({"type": "retired_script_reference", "file": rel, "detail": retired_script})
                flagged_scripts.add(Path(retired_script).name)
        for bare_name, bare_re in bare_script_res:
            if bare_name not in flagged_scripts and bare_re.search(text):
                issues.append({"type": "retired_script_reference", "file": rel, "detail": bare_name})

    return {
        "valid": not issues,
        "authorities_checked": len(AUTHORITY_GRAPH),
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# Mechanism 13 — Adaptive Clarification Policy (Section 22)
# ---------------------------------------------------------------------------

def evaluate_clarification(
    normalized_request: dict[str, Any],
    *,
    destructive_action: bool = False,
    authorized: bool = False,
) -> dict[str, Any]:
    """Mechanism 13: Ask only when missing essential source, destructive action, or incompatible goals; otherwise proceed."""
    questions: list[str] = []
    assumptions: list[dict[str, str]] = []

    if destructive_action and not authorized:
        questions.append("This operation modifies or deletes existing files irreversibly. Please confirm before proceeding.")

    if "missing_referenced_source" in (normalized_request.get("ambiguity") or []):
        questions.append("You referenced a specific lecture/PDF/chapter source, but no file or URL was supplied. Please attach or link the source.")

    # Check mutually incompatible explicit requirements (e.g., strict source-only + invent external benchmark comparisons)
    constraints = normalized_request.get("constraints") or {}
    if constraints.get("source_policy") == "strict" and "external_research" in (normalized_request.get("required_elements") or []):
        questions.append("Your request asks for both strict source-only fidelity and external research. Which policy should prevail?")

    if questions:
        return {"action": "ask", "questions": questions, "assumptions": assumptions}

    # Proceed with safe documented defaults instead of annoying unnecessary questions
    primary_out = (normalized_request.get("requested_outputs") or ["deep-notes"])[0]
    assumptions.append({
        "id": "default_master_selection",
        "value": primary_out,
        "basis": "safe_default",
    })
    assumptions.append({
        "id": "audience_baseline",
        "value": normalized_request.get("audience", "intermediate"),
        "basis": "inferred",
    })
    return {"action": "proceed", "questions": [], "assumptions": assumptions}


# ---------------------------------------------------------------------------
# Mechanism 20 — Observability and Decision Tracing (Section 29)
# ---------------------------------------------------------------------------

def _scrub_sensitive(value: Any) -> Any:
    if isinstance(value, str):
        cleaned = value
        for pat in SECRET_PATTERNS:
            cleaned = pat.sub("[REDACTED]", cleaned)
        return cleaned
    if isinstance(value, dict):
        return {k: _scrub_sensitive(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_scrub_sensitive(v) for v in value]
    return value


def build_execution_trace(
    *,
    routed: dict[str, Any],
    metadata: dict[str, Any] | None = None,
    validation: dict[str, Any] | None = None,
    repair: dict[str, Any] | None = None,
    metrics: dict[str, Any] | None = None,
    changed_files: list[str] | None = None,
) -> dict[str, Any]:
    """Mechanism 20: Build a concise, secret-scrubbed execution trace kept separate from educational notes."""
    meta = metadata or {}
    tags = meta.get("tags") or []
    trace = {
        "route": {
            "master": routed.get("master"),
            "variant": routed.get("variant"),
            "reason": (routed.get("routing_trace") or {}).get("decision_basis", ""),
            "multi_artifact": bool(routed.get("multi_artifact")),
            "artifact_count": len(routed.get("artifacts") or []),
        },
        "source": {
            "mode": routed.get("source_policy", "adaptive"),
            "research_mode": routed.get("research_mode", "R-I"),
        },
        "metadata": {
            "topic": meta.get("topic"),
            "domain": meta.get("domain"),
            "master_topic": meta.get("master_topic"),
            "note_type": meta.get("note_type"),
            "tags_generated": len(tags) if isinstance(tags, list) else 0,
            "yaml_valid": bool(meta.get("topic") and meta.get("domain") and meta.get("master_topic") and meta.get("note_type")),
        },
        "validation": validation or {},
        "repair": repair or {"changes_applied": 0},
        "changed_files": list(changed_files or []),
        "metrics": metrics or {},
    }
    return _scrub_sensitive(trace)


def validate_master_output(note_text: str, master: str, *, variant: str | None = None) -> list[str]:
    """Product-specific validation ensuring each master output fulfills its contract."""
    errors: list[str] = []
    text = note_text.strip()
    if not text:
        return ["Output note is empty."]

    headings = re.findall(r"^##\s+(.+)$", text, re.M)
    words = len(re.findall(r"\b\w+\b", text))

    if master == "M1":
        if len(headings) < 3:
            errors.append("M1 (Deep Learning Notes) requires structured multi-section depth (>= 3 H2 sections).")
        if words < 120:
            errors.append(f"M1 (Deep Learning Notes) is too sparse ({words} words) for first-principles mastery.")
    elif master == "M2":
        if len(headings) < 2:
            errors.append("M2 (Structured Study Notes) requires at least 2 structured H2 sections.")
        if variant == "lecture_order" and not re.search(r"Source\s*&\s*Scope|Lecture|Chapter|Section", text, re.I):
            errors.append("M2 (lecture_order) must preserve source/lecture scope context.")
    elif master == "M3":
        paragraphs = [
            p.strip() for p in re.split(r"\n\s*\n", text)
            if p.strip() and not p.strip().startswith(("#", "|", "-", "*", ">", "```", "$$", "---"))
        ]
        long_prose = [p for p in paragraphs if len(re.findall(r"\b\w+\b", p)) > 75]
        if long_prose:
            errors.append("M3 (Quick Reference) contains essay-length prose paragraphs (> 75 words); keep scannable.")
        if not re.search(r"(?:^\||^[-*]\s|\$\$)", text, re.M):
            errors.append("M3 (Quick Reference) must include dense lookup tables, bullets, or equations.")
        if variant == "formula_sheet" and not re.search(r"\$|=", text):
            errors.append("M3 (formula_sheet) must include formulas/equations.")
    elif master == "M4":
        if not re.search(r"\b(?:Problem|Example|Exercise|Given)\b", text, re.I):
            errors.append("M4 (Worked Problems & Solutions) must state concrete problem(s).")
        if not re.search(r"\b(?:Step|Strategy|Method|Solution|Derivation)\b", text, re.I):
            errors.append("M4 (Worked Problems & Solutions) must show explicit method/step-by-step solution.")
        if not re.search(r"\b(?:Final Answer|Result|Check|Verify|Verification|Sanity)\b", text, re.I):
            errors.append("M4 (Worked Problems & Solutions) must include a final answer and verification check.")
    elif master == "M5":
        if "```" not in text:
            errors.append("M5 (Implementation & Technical Guide) must include executable fenced code block(s).")
        if not re.search(r"\b(?:Test|Verify|Output|Assert|Edge Case|Complexity|Invariant|Run)\b", text, re.I):
            errors.append("M5 (Implementation & Technical Guide) must include verification, testing, or edge-case checks.")
    elif master == "M6":
        if variant == "flashcards":
            if not re.search(r"\b(?:Front|Q:|Question|Card)\b", text, re.I) or not re.search(r"\b(?:Back|A:|Answer|Reveal)\b", text, re.I):
                errors.append("M6 (flashcards) must include front/question and back/answer pairs.")
        else:
            q_matches = re.findall(r"(?:^###\s+Q\d+|^\*\*Q\d+|^\d+\.\s+\*\*)", text, re.M)
            if not q_matches:
                errors.append("M6 (Practice & Assessment) must include numbered assessment questions.")
            if not re.search(r">\s*\[!(?:tip|hint)\]-|\b(?:Answer Key|Solution|Rubric)\b", text, re.I):
                errors.append("M6 (Practice & Assessment) must separate hints, solutions, or grading rubrics.")
    elif master == "M7":
        if variant == "comparison_guide" and "|" not in text:
            errors.append("M7 (comparison_guide) must include a structured comparison matrix table.")
        if variant == "concept_map" and "```mermaid" not in text:
            errors.append("M7 (concept_map) must include a Mermaid concept map diagram.")
        if not re.search(r"(?:^\||```mermaid|\b(?:Comparison|Synthesis|Decision|Takeaway|Lineage|Verdict|Summary|Revision)\b)", text, re.M | re.I):
            errors.append("M7 (Synthesis & Revision) must include synthesis, comparison, decision, or revision structures.")
    else:
        errors.append(f"Unknown master ID: {master}")

    return errors


class OrchestrationEngine:
    """Cohesive Engine E1 facade for normalization, constraints, routing, capabilities, authority, clarification, and tracing."""

    def __init__(self, root: Path = ROOT):
        self.root = root

    def normalize(self, request: str, *, source_policy: str | None = None, has_source: bool = False) -> dict[str, Any]:
        return normalize_request(request, source_policy=source_policy, has_source=has_source, root=self.root)

    def route(self, request: str, *, source_policy: str | None = None, has_source: bool = False, existing_command: str | None = None) -> dict[str, Any]:
        return route_request(request, source_policy=source_policy, has_source=has_source, existing_command=existing_command, root=self.root)

    def resolve_constraints(self, normalized: dict[str, Any], *, extra_constraints: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        return resolve_constraints(normalized, extra_constraints=extra_constraints)

    def check_capabilities(self, master: str, capabilities: list[str], *, variant: str | None = None) -> dict[str, Any]:
        return validate_template_capabilities(master, capabilities, variant=variant)

    def check_clarification(self, normalized: dict[str, Any], *, destructive_action: bool = False, authorized: bool = False) -> dict[str, Any]:
        return evaluate_clarification(normalized, destructive_action=destructive_action, authorized=authorized)

    def lint_authority(self) -> dict[str, Any]:
        return lint_instruction_authority(self.root)

    def validate_registry(self, *, require_retired_legacy: bool = True) -> dict[str, Any]:
        return validate_registry(self.root, require_retired_legacy=require_retired_legacy)

    def validate_output(self, note_text: str, master: str, *, variant: str | None = None) -> list[str]:
        return validate_master_output(note_text, master, variant=variant)

    def trace(self, **kwargs: Any) -> dict[str, Any]:
        return build_execution_trace(**kwargs)

    # Universal /scribe-notes interactive intelligence methods
    def classify_scope(self, topic: str | None, *, request: str = "", has_source: bool = False, source_sections: list[str] | None = None) -> dict[str, Any]:
        from scriptorium.engines._interactive import classify_topic_scope
        return classify_topic_scope(topic, request or (topic or ""), has_source=has_source, source_sections=source_sections)

    def analyze_universal_request(self, request: str, *, has_source: bool = False, source_sections: list[str] | None = None, existing_vault_notes: list[str] | None = None):
        from scriptorium.engines._interactive import analyze_universal_request
        return analyze_universal_request(
            request,
            has_source=has_source,
            source_sections=source_sections,
            existing_vault_notes=existing_vault_notes,
            root=self.root,
        )

    def start_notes_session(
        self,
        request: str,
        *,
        has_source: bool = False,
        source_sections: list[str] | None = None,
        existing_vault_notes: list[str] | None = None,
    ):
        from scriptorium.engines._interactive import start_notes_session
        return start_notes_session(
            request,
            has_source=has_source,
            source_sections=source_sections,
            existing_vault_notes=existing_vault_notes,
            root=self.root,
        )

    def format_configuration_prompt(self, state: Any) -> str:
        from scriptorium.engines._interactive import format_configuration_prompt
        return format_configuration_prompt(state)

    def respond_to_session(self, state: Any, user_reply: str, *, source_sections: list[dict[str, str]] | None = None):
        from scriptorium.engines._interactive import respond_to_session
        return respond_to_session(state, user_reply, source_sections=source_sections, root=self.root)

    def save_session_state(self, vault_root: Path, state: Any) -> Path:
        from scriptorium.engines._interactive import save_session_state
        return save_session_state(vault_root, state)

    def load_session_state(self, vault_root: Path, request_id: str):
        from scriptorium.engines._interactive import load_session_state
        return load_session_state(vault_root, request_id)

    # Collection Intelligence coordination (KCP & F05 Scope Negotiation)
    def build_kcp(self, vault_root: Path, plan: Any, preferences: Any, **kwargs: Any):
        from scriptorium.engines._collection_intelligence import build_knowledge_collection_plan
        return build_knowledge_collection_plan(vault_root, plan, preferences, **kwargs)

    def negotiate_scope(self, topic: str, raw_request: str, preferences: Any, **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._collection_intelligence import negotiate_collection_scope
        return negotiate_collection_scope(topic, raw_request, preferences, **kwargs)

    # Token Efficiency & Canonical Prompt Compilation (Opt A, B, F, M, N, R)
    def create_token_controller(self, *, cache_dir: Path | None = None):
        from scriptorium.engines._token_optimizer import TokenEfficiencyController
        return TokenEfficiencyController(self.root, cache_dir=cache_dir)

    def select_context(self, *, master: str, variant: str | None = None, knowledge_types: list[str] | None = None, **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._token_optimizer import select_context_bundle
        return select_context_bundle(master=master, variant=variant, knowledge_types=knowledge_types, root=self.root, **kwargs)

    def compile_prompt(self, bundle: dict[str, Any], *, preferences_ir: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._token_optimizer import compile_execution_prompt
        return compile_execution_prompt(bundle, preferences_ir=preferences_ir, **kwargs)

    def partition_collection_context(self, kcp: Any, target_concept_id: str) -> dict[str, Any]:
        from scriptorium.engines._token_optimizer import partition_collection_context
        return partition_collection_context(kcp, target_concept_id)

    def compact_working_state(self, state: Any, *, conversation_history: list[dict[str, str]] | None = None) -> dict[str, Any]:
        from scriptorium.engines._token_optimizer import compact_working_state
        return compact_working_state(state, conversation_history=conversation_history)
