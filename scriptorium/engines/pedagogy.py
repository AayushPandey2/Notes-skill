"""Engine E4 — Pedagogical and Composition Engine for Scriptorium.

Consolidates:
- Contract v3 Adaptive Instructional Planner (_instructional)
- P01-P11 Pedagogical Intelligence Layer (_pedagogical_core)
- Isolated Legacy Compatibility Adapter (never silently invoked)
- Mechanism 7: Explanation Gap Detector
- Mechanism 8: Information Density Controller
- Mechanism 9: Example Selection Optimizer
- Mechanism 15: Knowledge Compression Engine
"""
from __future__ import annotations

import re
from typing import Any

from scriptorium.engines import _decision as decision_core
from scriptorium.engines import _instructional as instructional_core
from scriptorium.engines import _pedagogical_core as pedagogical_core
from scriptorium.models import parse_note

# Re-export core Contract v3 & P01-P11 helpers cleanly
from scriptorium.engines._instructional import (
    CONTRACT_VERSION,
    LEGACY_WARNING,
    adapt_legacy_contract,
    audit_modern_note,
    build_concept_dependency_graph,
    compose_concept_sequence,
    compose_document_outline,
    coverage_errors,
    from_legacy,
    normalize_plan,
    registry,
    resolve_instructional_contract,
)
from scriptorium.engines._pedagogical_core import (
    build_pedagogical_plan,
    validate_pedagogical_quality,
)
from scriptorium.engines._explanation import (
    BLUEPRINT_SCHEMA_VERSION,
    MASTER_EIS_ACTIVATION,
    ExplanationBlueprint,
    build_explanation_blueprint,
    build_retrieval_cues,
    compose_explanation_note,
    construct_explanatory_spine,
    plan_boundaries_and_contrasts,
    plan_central_question_and_anticipation,
    plan_mechanism_and_motivation,
    plan_variable_and_state_reasoning,
    resolve_eis_activation,
    validate_explanation_structure,
    verify_numerical_trace,
)

# ---------------------------------------------------------------------------
# Mechanism 7 — Explanation Gap Detector (Section 16)
# ---------------------------------------------------------------------------

_INLINE_SYM_RE = re.compile(r"\$([A-Za-z]|\\[a-zA-Z]+)(?:_\{?[\w]+\}?)?\$")
_CAPITALIZED_TERM_RE = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b")
_DERIV_STEP_RE = re.compile(r"(?:\\frac\{d|\\partial|d/d[a-z])\s*.*?(?:=|\to)\s*", re.I)


def detect_explanation_gaps(
    note_text: str,
    *,
    required_prerequisites: list[str] | None = None,
    defined_symbols: set[str] | None = None,
    reader_level: str = "beginner",
) -> dict[str, Any]:
    """Mechanism 7: Detect undefined terms, symbols used before introduction, and skipped derivation steps."""
    parsed = parse_note(note_text)
    body = parsed.body
    gaps: list[dict[str, Any]] = []
    known_symbols = {s.lstrip("\\") for s in (defined_symbols or set())}

    # 1. Symbols used before introduction (check if symbol appears in equation before a prose definition)
    lines = body.splitlines()
    for idx, line in enumerate(lines, 1):
        # Record definitions like "Let $\eta$ be...", "where $\alpha$ is...", "| $\theta$ | ... |"
        for def_m in re.finditer(r"(?:let|where|denotes?|represents?|is\s+the|\|\s*)\s*\$?(\\?[a-zA-Z]+)\$?", line, re.I):
            known_symbols.add(def_m.group(1).lstrip("\\"))
        for sym_m in _INLINE_SYM_RE.finditer(line):
            raw_sym = sym_m.group(1).lstrip("\\")
            if raw_sym in {"x", "y", "n", "i", "j", "k", "t", "f", "g"}:
                continue
            if raw_sym not in known_symbols and re.search(r"^\s*\$\$|=", line):
                gaps.append({
                    "type": "undefined_symbol",
                    "line": idx,
                    "symbol": sym_m.group(1),
                    "description": f"Symbol '{sym_m.group(1)}' is used in an expression before introduction.",
                    "repair_strategy": "definition",
                    "repair_hint": f"Introduce '{sym_m.group(1)}' with meaning and domain/units before line {idx}.",
                })
                known_symbols.add(raw_sym)

    # 2. Missing prerequisite concepts referenced or skipped in derivations
    lowered = body.lower()
    for prereq in required_prerequisites or []:
        if prereq.lower() not in lowered:
            gaps.append({
                "type": "hidden_prerequisite",
                "prerequisite": prereq,
                "description": f"Prerequisite '{prereq}' is needed for the explanation but is never introduced or bridged.",
                "repair_strategy": "prerequisite_bridge",
                "repair_hint": f"Add a brief 2-3 sentence prerequisite bridge for '{prereq}' immediately before use.",
            })

    # 3. Sudden nested/composite-function derivative leap without mentioning chain rule or intermediate step
    has_nested_deriv = bool(re.search(
        r"(?:d/dx|\\frac\{d\}\{dx\}|\\frac\{\\partial).*?(?:\([^\n)]*\([^\n)]*\)|(?:sin|cos|tan|exp|log|ln)\([^)]*(?:\^|\*|/|\+|-)[^)]*\))",
        body,
        re.I,
    ))
    has_chain_step = bool(re.search(r"\bchain\s+rule\b|inner\s+derivative|outer\s+derivative|du/dx|\\frac\{du\}\{dx\}", body, re.I))
    if has_nested_deriv and not has_chain_step and reader_level != "advanced":
        gaps.append({
            "type": "skipped_derivation_step",
            "description": "Derivation jumps directly from a composite/nested function to its derivative without showing the chain rule intermediate step.",
            "repair_strategy": "intermediate_equation",
            "repair_hint": "Insert the intermediate substitution u = g(x) and apply df/dx = (df/du)(du/dx).",
        })

    # 4. Missing assumptions check when theorem/bound/convergence is claimed
    if re.search(r"\b(?:converges|guarantees?\s+descent|optimal|bound)\b", body, re.I):
        if not re.search(r"\b(?:assuming|assumption|convex|smooth|lipschitz|differentiable|provided\s+that|when\s+0|condition)\b", body, re.I):
            gaps.append({
                "type": "missing_assumption",
                "description": "Convergence or optimality claim stated without explicit applicability assumptions.",
                "repair_strategy": "definition",
                "repair_hint": "State the explicit regularity assumptions (e.g., differentiability, L-smoothness, convexity).",
            })

    return {
        "has_gaps": bool(gaps),
        "gap_count": len(gaps),
        "reader_level": reader_level,
        "gaps": gaps,
    }


# ---------------------------------------------------------------------------
# Mechanism 8 — Information Density Controller (Section 17)
# ---------------------------------------------------------------------------

def analyze_information_density(
    note_text: str,
    *,
    reader_level: str = "beginner",
    preserve_exhaustive_depth: bool = True,
) -> dict[str, Any]:
    """Mechanism 8: Analyze per-section term density, symbol rate, derivation length, and example proximity."""
    parsed = parse_note(note_text)
    threshold_terms = 6 if reader_level == "beginner" else (10 if reader_level == "intermediate" else 14)
    section_reports: list[dict[str, Any]] = []
    overloaded_sections: list[dict[str, Any]] = []

    for sec in parsed.sections:
        content = sec.content
        words = len(re.findall(r"\b\w+\b", content))
        # Technical/bold/backticked/italicized newly introduced terms
        bold_terms = set(re.findall(r"\*\*([^*]{2,40})\*\*", content))
        code_terms = set(re.findall(r"`([^`]{2,40})`", content))
        long_tech_words = {
            w.lower() for w in re.findall(r"\b[a-zA-Z]{9,}\b", content)
            if w.lower() not in {"therefore", "something", "different", "important", "following", "understand", "explaining"}
        }
        new_term_count = len(bold_terms | code_terms) + max(0, len(long_tech_words) - 4)
        symbols = set(re.findall(r"\$(?:\\[a-zA-Z]+|[A-Za-z])(?:_\{?[\w]+\}?)?\$", content))
        display_eqs = len(re.findall(r"\$\$.*?\$\$", content, re.S))
        has_example = bool(re.search(r"\b(?:example|suppose|for\s+instance|take\s+\$?x|consider\s+a\s+concrete)\b", content, re.I))

        interventions: list[str] = []
        if new_term_count > threshold_terms:
            interventions.append("break_into_staged_subsections_and_define_terms_before_use")
        if len(symbols) > (5 if reader_level == "beginner" else 9):
            interventions.append("introduce_symbols_progressively_with_inline_glossary")
        if display_eqs >= 4 and not has_example:
            interventions.append("insert_concrete_numerical_example_between_derivation_steps")
        if words > 350 and not has_example and "summary" not in sec.slug:
            interventions.append("add_worked_anchor_or_summary_table")

        report = {
            "heading": sec.heading,
            "words": words,
            "estimated_new_terms": new_term_count,
            "unique_symbols": len(symbols),
            "display_equations": display_eqs,
            "has_example": has_example,
            "overloaded": bool(interventions),
            "interventions": interventions,
            "preserves_requested_depth": preserve_exhaustive_depth,
        }
        section_reports.append(report)
        if interventions:
            overloaded_sections.append(report)

    return {
        "reader_level": reader_level,
        "preserve_exhaustive_depth": preserve_exhaustive_depth,
        "needs_restructuring": bool(overloaded_sections),
        "overloaded_sections": overloaded_sections,
        "sections": section_reports,
    }


# ---------------------------------------------------------------------------
# Mechanism 9 — Example Selection Optimizer (Section 18)
# ---------------------------------------------------------------------------

EXAMPLE_ROLES = frozenset({
    "minimal",
    "worked",
    "representative",
    "boundary",
    "counterexample",
    "debugging",
    "transfer",
    "comparative",
})


def _token_set(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]{3,}", text.lower()) if w not in {"the", "and", "for", "with", "that", "this", "from", "into"}}


def optimize_examples(examples: list[dict[str, Any]]) -> dict[str, Any]:
    """Mechanism 9: Evaluate pedagogical role diversity and flag redundant near-duplicate examples without arbitrary quotas."""
    kept: list[dict[str, Any]] = []
    redundant: list[dict[str, Any]] = []
    warnings: list[str] = []

    seen_signatures: list[tuple[str, str, set[str], str]] = []
    for idx, ex in enumerate(examples):
        ex_id = str(ex.get("id") or f"ex_{idx + 1}")
        role = str(ex.get("role") or "worked").strip().lower()
        mechanism = str(ex.get("mechanism") or "core").strip().lower()
        text = str(ex.get("content") or ex.get("description") or "")
        tokens = _token_set(text)

        if role not in EXAMPLE_ROLES:
            warnings.append(f"Example '{ex_id}' uses non-standard role '{role}'; valid roles: {sorted(EXAMPLE_ROLES)}.")

        duplicate_of = None
        for prev_id, prev_role, prev_tokens, prev_mech in seen_signatures:
            if role == prev_role and mechanism == prev_mech:
                union = tokens | prev_tokens
                jaccard = (len(tokens & prev_tokens) / len(union)) if union else 1.0
                if jaccard >= 0.55:
                    duplicate_of = prev_id
                    break

        if duplicate_of is not None:
            redundant.append({
                "id": ex_id,
                "role": role,
                "duplicate_of": duplicate_of,
                "reason": f"Teaches the same '{role}' mechanism ('{mechanism}') as '{duplicate_of}' without adding a new boundary, failure mode, or transfer insight.",
            })
        else:
            seen_signatures.append((ex_id, role, tokens, mechanism))
            kept.append({**ex, "id": ex_id, "role": role})

    return {
        "kept": kept,
        "redundant": redundant,
        "has_redundancy": bool(redundant),
        "warnings": warnings,
        "role_coverage": sorted({e["role"] for e in kept}),
    }


# ---------------------------------------------------------------------------
# Mechanism 15 — Knowledge Compression Engine (Section 24)
# ---------------------------------------------------------------------------

def compress_knowledge(
    authoritative_note: str,
    *,
    target_product: str = "quick-reference",
    required_conditions: list[str] | None = None,
    source_link: str | None = None,
) -> dict[str, Any]:
    """Mechanism 15: Compress an authoritative note into a compact learning artifact while preserving definitions, formulas, and conditions."""
    parsed = parse_note(authoritative_note)
    title = parsed.title or parsed.metadata.get("topic") or "Concept"

    equations = re.findall(r"\$\$(.+?)\$\$", parsed.body, re.S)
    bullet_rules = [
        ln.strip() for ln in parsed.body.splitlines()
        if re.match(r"^\s*[-*]\s+\*\*", ln)
    ]
    conditions_found = [
        ln.strip() for ln in parsed.body.splitlines()
        if re.search(r"\b(?:when|assuming|condition|requires|valid\s+for|provided|trap|fails|caveat|limit)\b", ln, re.I)
        and not ln.strip().startswith("#")
    ]

    lines: list[str] = [f"# {title} — {target_product.replace('-', ' ').title()}", ""]
    if target_product == "flashcards":
        if equations:
            lines.extend([
                "### Card 1",
                f"- **Front**: State the governing equation for {title} and its applicability condition.",
                f"- **Back**: $${equations[0].strip()}$$ — " + (conditions_found[0] if conditions_found else "Verify domain assumptions."),
                "",
            ])
        for idx, b in enumerate(bullet_rules[:4], start=2):
            lines.extend([
                f"### Card {idx}",
                f"- **Front**: Explain the key rule for {title} (item {idx - 1}).",
                f"- **Back**: {b.lstrip('-* ').strip()}",
                "",
            ])
    else:
        if equations:
            lines.append("## Core Formulas & Conditions")
            lines.append("| Formula | Applicability Condition / Caveat |")
            lines.append("|---|---|")
            for idx, eq in enumerate(equations[:5]):
                cond = (
                    required_conditions[idx]
                    if required_conditions and idx < len(required_conditions)
                    else (conditions_found[idx] if idx < len(conditions_found) else "State domain assumptions before applying.")
                )
                eq_one_line = " ".join(eq.strip().splitlines()).replace("|", "\\|")
                cond_clean = cond.replace("|", "\\|")
                lines.append(f"| `${eq_one_line}$` | {cond_clean} |")
            lines.append("")

        lines.append("## Key Principles & Caveats")
        seen_lines: set[str] = set()
        for item in (*bullet_rules[:5], *conditions_found[:5]):
            clean_item = item if item.startswith("-") else f"- {item}"
            if clean_item not in seen_lines:
                seen_lines.add(clean_item)
                lines.append(clean_item)
        # Ensure all explicitly required conditions survive compression verbatim
        joined_so_far = "\n".join(lines).replace("$", "").lower()
        for cond in required_conditions or []:
            if cond.replace("$", "").lower() not in joined_so_far:
                lines.append(f"- **Condition**: {cond}")
        lines.append("")

    if source_link:
        lines.append(f"Full explanation: [[{source_link}]]")
        lines.append("")

    compressed_text = "\n".join(lines).strip() + "\n"
    validation = validate_compression(
        authoritative_note,
        compressed_text,
        required_conditions=required_conditions,
    )
    return {
        "target_product": target_product,
        "compressed_body": compressed_text,
        "validation": validation,
    }


def validate_compression(
    authoritative_note: str,
    compressed_note: str,
    *,
    required_conditions: list[str] | None = None,
) -> dict[str, Any]:
    """Verify compressed output preserves essential applicability conditions and introduces no distortions."""
    issues: list[str] = []
    auth_parsed = parse_note(authoritative_note)
    comp_lower = compressed_note.lower()

    # Check explicitly required conditions (ignoring inline $ delimiters)
    auth_plain = auth_parsed.body.replace("$", "")
    comp_plain = compressed_note.replace("$", "")
    for cond in required_conditions or []:
        if cond.replace("$", "").lower() not in comp_plain.lower():
            issues.append(f"Compression dropped required applicability condition: '{cond}'.")

    # Auto-detect key inequality/regularity conditions in authoritative note (ignoring inline $ delimiters)
    for pat, label in (
        (r"0\s*<\s*\\?(?:eta|alpha)\s*<\s*2/L", "step-size stability condition (0 < eta < 2/L)"),
        (r"\bL[- ]smooth\b", "L-smoothness assumption"),
        (r"\bconvex\b", "convexity assumption"),
        (r"\bdifferentiable\b", "differentiability assumption"),
    ):
        if re.search(pat, auth_plain, re.I) and not re.search(pat, comp_plain, re.I):
            issues.append(f"Compression dropped essential mathematical condition: {label}.")

    # Reject overgeneralized absolute claims if authoritative note had caveats
    if re.search(r"\b(?:fails|diverges|limitation|only\s+when|assuming)\b", auth_parsed.body, re.I):
        if re.search(r"\balways\s+(?:converges|works|holds|optimal)\b", compressed_note, re.I):
            issues.append("Compression overgeneralized a conditional result into an unconditional 'always' claim.")

    return {
        "valid": not issues,
        "issues": issues,
        "compression_ratio": round(len(compressed_note) / max(1, len(auth_parsed.body)), 3),
    }


class PedagogyEngine:
    def plan_composition(self, specification: dict[str, Any]) -> dict[str, Any]:
        from ._composition import build_composition
        return build_composition(specification)

    def render_table(self, specification: dict[str, Any]) -> str:
        from ._composition import render_table
        return render_table(specification)

    def select_visual(self, requirement: dict[str, Any], *, available: set[str]) -> dict[str, Any]:
        from ._composition import select_visual
        return select_visual(requirement, available=available)

    """Cohesive Engine E4 facade integrating Contract v3, P01-P11, gaps, density, examples, and compression."""

    def normalize_plan(self, raw_plan: dict[str, Any]) -> dict[str, Any]:
        return normalize_plan(raw_plan)

    def resolve_contract(self, request: str, topic: str, raw_plan: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        return resolve_instructional_contract(request, topic, raw_plan, **kwargs)

    def build_pedagogical_plan(self, instructional_plan: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        return build_pedagogical_plan(instructional_plan, **kwargs)

    def detect_gaps(self, note_text: str, **kwargs: Any) -> dict[str, Any]:
        return detect_explanation_gaps(note_text, **kwargs)

    def control_density(self, note_text: str, **kwargs: Any) -> dict[str, Any]:
        return analyze_information_density(note_text, **kwargs)

    def optimize_examples(self, examples: list[dict[str, Any]]) -> dict[str, Any]:
        return optimize_examples(examples)

    def compress(self, authoritative_note: str, **kwargs: Any) -> dict[str, Any]:
        return compress_knowledge(authoritative_note, **kwargs)

    def validate_compression(self, authoritative_note: str, compressed_note: str, **kwargs: Any) -> dict[str, Any]:
        return validate_compression(authoritative_note, compressed_note, **kwargs)

    # Explanation Intelligence System (EIS-01 through EIS-06)
    def build_explanation_blueprint(self, topic: str, **kwargs: Any) -> ExplanationBlueprint:
        return build_explanation_blueprint(topic, **kwargs)

    def compose_explanation(self, blueprint: ExplanationBlueprint, **kwargs: Any) -> str:
        return compose_explanation_note(blueprint, **kwargs)

    def validate_explanation(self, note_text: str, blueprint: ExplanationBlueprint) -> list[dict[str, Any]]:
        return validate_explanation_structure(note_text, blueprint)

    def verify_trace(self, trace: list[dict[str, Any]], *, rule: str = "quadratic_gd", alpha: float = 0.1) -> dict[str, Any]:
        return verify_numerical_trace(trace, rule=rule, alpha=alpha)

    # Hierarchical Topic Decomposition & Collection Planning
    def plan_collection(
        self,
        topic: str,
        preferences: Any,
        *,
        scope: dict[str, Any] | None = None,
        source_sections: list[dict[str, str]] | list[str] | None = None,
        existing_notes: list[str] | None = None,
    ):
        from scriptorium.engines._interactive import plan_note_collection
        normalized_sections: list[dict[str, str]] | None = None
        if source_sections is not None:
            normalized_sections = [
                {"title": s} if isinstance(s, str) else s for s in source_sections
            ]
        return plan_note_collection(
            topic,
            preferences,
            scope=scope,
            source_sections=normalized_sections,
        )

    def format_collection_preview(self, plan: Any, preferences: Any | None = None) -> str:
        from scriptorium.engines._interactive import ResolvedNotePreferences, format_collection_preview
        prefs = preferences or ResolvedNotePreferences(
            "Structured understanding", "M1", None, "standard", {}, plan.organization, [], "adaptive"
        )
        return format_collection_preview(plan, prefs)

    def modify_collection_plan(self, plan: Any, instruction: str):
        from scriptorium.engines._interactive import modify_collection_plan
        return modify_collection_plan(plan, instruction)

    # Collection Pedagogical Intelligence (F02, F07, F08, F10, F11, F12, F13)
    def allocate_depth(self, plan: Any, preferences: Any, **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._collection_intelligence import allocate_collection_depth
        return allocate_collection_depth(plan, preferences, **kwargs)

    def evaluate_granularity(self, plan: Any, preferences: Any, **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._collection_intelligence import evaluate_note_granularity
        return evaluate_note_granularity(plan, preferences, **kwargs)

    def split_note_in_plan(self, plan: Any, target_concept_id: str, child_titles: list[str]):
        from scriptorium.engines._collection_intelligence import apply_granularity_split
        return apply_granularity_split(plan, target_concept_id, child_titles)

    def generate_learning_paths(self, plan: Any, preferences: Any, **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._collection_intelligence import generate_learning_paths
        return generate_learning_paths(plan, preferences, **kwargs)

    def plan_synthesis_notes(self, plan: Any, preferences: Any, **kwargs: Any) -> list[dict[str, Any]]:
        from scriptorium.engines._collection_intelligence import plan_and_render_synthesis_notes
        return plan_and_render_synthesis_notes(plan, preferences, **kwargs)

    def apply_progressive_disclosure(self, note_text: str, **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._collection_intelligence import apply_progressive_disclosure
        return apply_progressive_disclosure(note_text, **kwargs)

    def define_learning_outcomes(self, node: Any, preferences: Any) -> list[dict[str, Any]]:
        from scriptorium.engines._collection_intelligence import define_learning_outcomes
        return define_learning_outcomes(node, preferences)

    def build_collection_assessment(self, plan: Any, preferences: Any, competencies: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._collection_intelligence import build_collection_assessment
        return build_collection_assessment(plan, preferences, competencies, **kwargs)
