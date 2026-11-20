"""Advanced Knowledge Collection Intelligence & Lifecycle System (F02-F15).

Coordinates the 14 integrated collection capabilities through the shared
KnowledgeCollectionPlan (KCP) while reusing existing Scriptorium engines:
- E1 Orchestration (_interactive, orchestration)
- E3 Knowledge (ConceptIdentityRegistry, detect_semantic_changes, compute_change_impact)
- E4 Pedagogy (ExplanationBlueprint, compose_explanation_note)
- E5 Quality (validate_note_collection, review_explanatory_clarity)
- E6 Vault (build_obsidian_properties, incremental_update_note, safe_write_note, render_parent_moc)

EXPLICIT EXCLUSION: Feature 1 (Interactive Knowledge Diagnosis / pre-generation diagnostic quiz)
is intentionally NOT implemented.
"""
from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass, field
from datetime import date
import hashlib
import json
from pathlib import Path
import re
from typing import Any

import yaml

from scriptorium.engines._interactive import (
    NoteCollectionPlan,
    ResolvedNotePreferences,
    TopicNode,
    classify_topic_scope,
)
from scriptorium.engines.knowledge import (
    ConceptIdentityRegistry,
    compute_change_impact,
    detect_semantic_changes,
)
from scriptorium.models import content_hash, parse_note, slugify


# ---------------------------------------------------------------------------
# Explicit Exclusion Guard (Part 1.2)
# ---------------------------------------------------------------------------

INTERACTIVE_KNOWLEDGE_DIAGNOSIS_ENABLED: bool = False


# ---------------------------------------------------------------------------
# Part 5 — Unified Knowledge Collection Plan (KCP)
# ---------------------------------------------------------------------------

VALID_GENERATION_STATES: frozenset[str] = frozenset({
    "PLANNED",
    "READY",
    "GENERATING",
    "DRAFTED",
    "VALIDATING",
    "VALIDATED",
    "COMMITTED",
    "REUSED",
    "DEFERRED",
    "NEEDS_REVIEW",
    "FAILED",
    "CANCELLED",
})

VALID_REUSE_DECISIONS: frozenset[str] = frozenset({
    "reuse_unchanged",
    "reuse_with_link",
    "extend_existing",
    "update_existing",
    "create_distinct_variant",
    "create_new",
    "request_user_resolution",
})


@dataclass
class KnowledgeCollectionPlan:
    """Shared Knowledge Collection Plan (KCP) coordinating F02-F15 without duplicating engine state."""

    schema_version: str = "1.0"
    collection_id: str = ""
    topic: str = ""
    configuration: dict[str, Any] = field(default_factory=dict)
    scope: dict[str, Any] = field(default_factory=dict)
    plan: NoteCollectionPlan | None = None
    depth_allocation: dict[str, dict[str, Any]] = field(default_factory=dict)
    existing_note_reconciliation: dict[str, dict[str, Any]] = field(default_factory=dict)
    prerequisite_gaps: list[dict[str, Any]] = field(default_factory=list)
    scope_negotiation: dict[str, Any] = field(default_factory=dict)
    granularity_decisions: list[dict[str, Any]] = field(default_factory=list)
    granularity_revision_count: int = 0
    learning_paths: dict[str, Any] = field(default_factory=dict)
    terminology_registry: dict[str, Any] = field(default_factory=dict)
    synthesis_notes: list[dict[str, Any]] = field(default_factory=list)
    progressive_disclosure_policy: dict[str, Any] = field(default_factory=dict)
    competencies: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    assessment_plan: dict[str, Any] = field(default_factory=dict)
    generation: dict[str, Any] = field(default_factory=lambda: {
        "batches": [],
        "checkpoints": [],
        "note_states": {},
        "status": "PLANNED",
    })
    revisions: dict[str, Any] = field(default_factory=lambda: {
        "current_revision": 0,
        "history": [],
        "impact_queue": [],
    })
    refinement_log: list[dict[str, Any]] = field(default_factory=list)
    validation: dict[str, Any] = field(default_factory=lambda: {"status": "pending"})
    diagnostic_quiz_enabled: bool = False  # Strictly False per Part 1.2

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["diagnostic_quiz_enabled"] = False
        return data


# ---------------------------------------------------------------------------
# F02 — Collection-Level Adaptive Depth Allocation
# ---------------------------------------------------------------------------

_HIGH_COMPLEXITY_HINTS = re.compile(
    r"\b(?:gradient\s+descent|backpropagation|attention|transformer|regression|regularization|"
    r"optimization|svd|eigen|bayes|theorem|proof|dynamic\s+programming|dijkstra|binary\s+search|"
    r"pca|loss\s+function|virtual\s+memory|scheduling|deadlock|maxwell|biot[\s–-]savart)\b",
    re.I,
)
_ORIENTATION_HINTS = re.compile(
    r"\b(?:what\s+is|introduction|overview|terminology|glossary|history\s+of|types\s+of|missing\s+values)\b",
    re.I,
)


def allocate_collection_depth(
    plan: NoteCollectionPlan,
    preferences: ResolvedNotePreferences,
    *,
    budget_notes: int | None = None,
    user_priorities: list[str] | None = None,
) -> dict[str, Any]:
    """F02: Distribute collection-level instructional emphasis across concepts by complexity & centrality."""
    node_map = {n.concept_id: n for n in plan.nodes}
    # Count downstream dependents for each concept_id
    dependents_count: dict[str, int] = {n.concept_id: 0 for n in plan.nodes}
    for n in plan.nodes:
        for pid in n.prerequisite_ids:
            if pid in dependents_count:
                dependents_count[pid] += 1

    priority_terms = {p.strip().lower() for p in (user_priorities or []) if p.strip()}
    allocations: dict[str, dict[str, Any]] = {}
    deferred_optional: list[str] = []
    warnings: list[str] = []

    req_depth = (preferences.depth or "standard").lower()
    is_concise = req_depth == "concise" or preferences.master == "M3"
    is_exhaustive = req_depth == "exhaustive"

    child_nodes = [n for n in plan.nodes if n.note_role in {"child", "single"}]
    if budget_notes is not None and len(child_nodes) > budget_notes:
        warnings.append(
            f"Requested {len(child_nodes)} content notes exceeds practical single-pass budget ({budget_notes}); "
            "high-centrality concepts retain priority while optional expansion is flagged for deferral."
        )

    scored: list[tuple[int, TopicNode]] = []
    for node in child_nodes:
        score = 1
        reasons: list[str] = []
        dep_cnt = dependents_count.get(node.concept_id, 0)
        if dep_cnt >= 2:
            score += 2
            reasons.append("high_dependency_centrality")
        elif dep_cnt == 1:
            score += 1
            reasons.append("prerequisite_for_downstream_concept")

        if _HIGH_COMPLEXITY_HINTS.search(node.title):
            score += 2
            reasons.append("significant_conceptual_or_mathematical_complexity")
        if _ORIENTATION_HINTS.search(node.title):
            score -= 1
            reasons.append("introductory_orientation_scope")
        if node.title.lower() in priority_terms or any(pt in node.title.lower() for pt in priority_terms):
            score += 3
            reasons.append("explicit_user_priority")
        if preferences.source_policy == "strict":
            reasons.append("bounded_by_strict_source_coverage")
        if not reasons:
            reasons.append("core_collection_concept")

        if is_concise:
            level = "standard" if score >= 3 else "orientation"
        elif is_exhaustive:
            level = "exhaustive" if score >= 3 else ("deep" if score >= 2 else "detailed")
        elif req_depth == "comprehensive":
            level = "deep" if score >= 3 else ("detailed" if score >= 2 else ("standard" if score >= 1 else "orientation"))
        else:
            level = "detailed" if score >= 3 else ("standard" if score >= 1 else "orientation")

        math_emp = "deep" if ("mathematics" in preferences.emphasis or level in {"deep", "exhaustive"}) and _HIGH_COMPLEXITY_HINTS.search(node.title) else ("standard" if level != "orientation" else "minimal")
        code_emp = "detailed" if ("code" in preferences.emphasis or preferences.master == "M5") else "optional"

        allocations[node.concept_id] = {
            "concept_id": node.concept_id,
            "title": node.title,
            "priority": "high" if score >= 3 else ("medium" if score >= 1 else "low"),
            "allocation": level,
            "score": score,
            "reasons": reasons,
            "emphasis": {
                "derivation": math_emp,
                "numerical_examples": "detailed" if level in {"deep", "exhaustive"} else "standard",
                "implementation": code_emp,
            },
            "expose_scores_in_note": False,
        }
        scored.append((score, node))

    if budget_notes is not None and len(scored) > budget_notes:
        # Defer lowest-priority optional nodes rather than silently gutting core concepts
        ordered_low_first = sorted(scored, key=lambda pair: (pair[0], pair[1].title))
        excess = len(scored) - budget_notes
        for _, node in ordered_low_first[:excess]:
            if allocations[node.concept_id]["priority"] == "low":
                allocations[node.concept_id]["deferred_optional_expansion"] = True
                deferred_optional.append(node.concept_id)

    return {
        "requested_depth": req_depth,
        "budget_notes": budget_notes,
        "allocations": allocations,
        "deferred_optional": deferred_optional,
        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# F03 — Smart Existing-Note Reuse
# ---------------------------------------------------------------------------

def _norm_title(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(text or "").strip().lower()).strip()


def reconcile_existing_vault_notes(
    vault_root: Path,
    plan: NoteCollectionPlan,
    preferences: ResolvedNotePreferences,
    *,
    concept_registry: ConceptIdentityRegistry | None = None,
    readonly_paths: set[str] | None = None,
) -> dict[str, Any]:
    """F03: Discover existing vault notes, evaluate quality & compatibility, and assign reuse decisions."""
    vault_root = Path(vault_root)
    readonly_set = {p.replace("\\", "/").lower() for p in (readonly_paths or set())}

    # Scan vault notes once
    vault_index: list[dict[str, Any]] = []
    if vault_root.is_dir():
        for md in sorted(vault_root.rglob("*.md")):
            if any(part.startswith(".") for part in md.relative_to(vault_root).parts):
                continue
            rel = md.relative_to(vault_root).as_posix()
            try:
                raw = md.read_text(encoding="utf-8-sig")
                parsed = parse_note(raw)
                meta = parsed.metadata
                words = len(re.findall(r"\b\w+\b", parsed.body))
                aliases = [str(a) for a in (meta.get("aliases") or []) if str(a).strip()]
                cids = [str(c) for c in (meta.get("concept_ids") or []) if str(c).strip()]
                vault_index.append({
                    "path": rel,
                    "stem": md.stem,
                    "title": str(meta.get("topic") or parsed.title or md.stem),
                    "aliases": aliases,
                    "concept_ids": cids,
                    "domain": str(meta.get("domain") or ""),
                    "master_topic": str(meta.get("master_topic") or ""),
                    "note_type": str(meta.get("note_type") or ""),
                    "source_mode": str(meta.get("source_mode") or ""),
                    "difficulty": str(meta.get("difficulty") or ""),
                    "word_count": words,
                    "section_count": len(parsed.sections),
                    "readonly": rel.lower() in readonly_set,
                })
            except Exception:
                continue

    decisions: dict[str, dict[str, Any]] = {}
    reused_paths: list[str] = []
    conflicts: list[dict[str, Any]] = []

    req_note_type = {
        "M1": "deep-notes",
        "M2": "study-notes",
        "M3": "quick-reference",
        "M4": "worked-solutions",
        "M5": "implementation-guide",
        "M6": "assessment",
        "M7": "synthesis-revision",
    }.get(preferences.master, "deep-notes")

    min_words_for_depth = {"concise": 25, "standard": 50, "comprehensive": 90, "exhaustive": 130}.get(preferences.depth, 50)

    for node in plan.nodes:
        if node.note_role in {"root_index", "group_index"}:
            continue
        target_norm = _norm_title(node.title)
        match = None
        match_basis = ""

        # 1. Canonical concept_id match
        for item in vault_index:
            if node.concept_id in item["concept_ids"]:
                match, match_basis = item, "canonical_concept_id"
                break
        # 2. Exact title / stem match (respecting domain compatibility if both present)
        if match is None:
            for item in vault_index:
                if _norm_title(item["title"]) == target_norm or _norm_title(item["stem"]) == target_norm:
                    match, match_basis = item, "exact_title"
                    break
        # 3. Alias match
        if match is None:
            for item in vault_index:
                if any(_norm_title(a) == target_norm for a in item["aliases"]):
                    match, match_basis = item, "alias"
                    break
        # 4. Semantic token overlap (>= 0.75 Jaccard on >= 2 tokens)
        if match is None:
            t_tokens = {w for w in target_norm.split() if len(w) >= 3}
            if len(t_tokens) >= 2:
                for item in vault_index:
                    i_tokens = {w for w in _norm_title(item["title"]).split() if len(w) >= 3}
                    if i_tokens and len(t_tokens & i_tokens) / len(t_tokens | i_tokens) >= 0.75:
                        match, match_basis = item, "semantic_overlap"
                        break

        if match is None:
            decisions[node.concept_id] = {
                "concept_id": node.concept_id,
                "title": node.title,
                "decision": "create_new",
                "matched_path": None,
                "match_basis": None,
                "quality_gaps": [],
                "reason": "No matching canonical note exists in vault.",
            }
            continue

        # Evaluate quality & compatibility
        gaps: list[str] = []
        if match["word_count"] < min_words_for_depth:
            gaps.append(f"insufficient_depth ({match['word_count']} words < {min_words_for_depth} target)")
        if match["section_count"] < 2:
            gaps.append("minimal_structure (< 2 sections)")
        if preferences.source_policy == "strict" and match["source_mode"] and match["source_mode"] != "strict":
            gaps.append("source_policy_mismatch (existing note is not strict source-only)")

        # Distinct artifact variant check (e.g., deep-notes exists, user requests quick-reference/formula sheet)
        if match["note_type"] and req_note_type != match["note_type"] and preferences.master in {"M3", "M4", "M6"}:
            decision = "create_distinct_variant"
            reason = f"Existing canonical '{match['note_type']}' note retained; creating distinct '{req_note_type}' companion."
        elif match["readonly"] and gaps:
            decision = "request_user_resolution"
            reason = f"Existing note '{match['path']}' is read-only/externally owned and has quality gaps: {', '.join(gaps)}."
            conflicts.append({"concept_id": node.concept_id, "path": match["path"], "gaps": gaps})
        elif preferences.source_policy == "strict" and any("source_policy_mismatch" in g for g in gaps):
            decision = "request_user_resolution"
            reason = f"Existing note '{match['path']}' has incompatible source_mode under strict source-only policy."
            conflicts.append({"concept_id": node.concept_id, "path": match["path"], "gaps": gaps})
        elif not gaps:
            decision = "reuse_with_link" if match["path"].lower() != node.proposed_path.lower() else "reuse_unchanged"
            reason = f"Existing note '{match['path']}' ({match_basis}) satisfies depth and quality requirements."
            reused_paths.append(match["path"])
        else:
            decision = "extend_existing" if match["word_count"] >= 20 else "update_existing"
            reason = f"Existing note '{match['path']}' matched via {match_basis} but needs enrichment: {', '.join(gaps)}."

        decisions[node.concept_id] = {
            "concept_id": node.concept_id,
            "title": node.title,
            "decision": decision,
            "matched_path": match["path"],
            "match_basis": match_basis,
            "quality_gaps": gaps,
            "readonly": match["readonly"],
            "reason": reason,
        }

    return {
        "vault_notes_scanned": len(vault_index),
        "decisions": decisions,
        "reused_count": sum(1 for d in decisions.values() if d["decision"] in {"reuse_unchanged", "reuse_with_link"}),
        "reused_paths": reused_paths,
        "conflicts": conflicts,
    }


# ---------------------------------------------------------------------------
# F04 — Knowledge Graph Gap Analysis (G1-G5)
# ---------------------------------------------------------------------------

_KNOWN_PREREQ_KNOWLEDGE: dict[str, list[str]] = {
    "backpropagation": ["Chain Rule", "Partial Derivatives", "Computational Graphs"],
    "gradient descent": ["Derivatives", "Loss Functions"],
    "stochastic gradient descent": ["Gradient Descent"],
    "adam": ["Gradient Descent", "Momentum"],
    "logistic regression": ["Linear Regression", "Probability Basics"],
    "self-attention": ["Matrix Multiplication", "Softmax Function"],
    "multi-head attention": ["Self-Attention"],
    "transformers": ["Self-Attention", "Positional Encoding"],
    "pca": ["Eigenvalues and Eigenvectors", "Covariance Matrix"],
    "binary search": ["Sorted Arrays"],
}


def analyze_prerequisite_gaps(
    plan: NoteCollectionPlan,
    preferences: ResolvedNotePreferences,
    *,
    existing_reconciliation: dict[str, Any] | None = None,
    known_concepts: list[str] | None = None,
    vault_titles: list[str] | None = None,
) -> dict[str, Any]:
    """F04: Detect G1-G5 prerequisite gaps using smallest-intervention resolution (NO diagnostic quizzes!)."""
    node_map = {n.concept_id: n for n in plan.nodes}
    planned_titles_norm = {_norm_title(n.title): n.concept_id for n in plan.nodes}
    order_pos = {cid: idx for idx, cid in enumerate(plan.learning_order)}

    # Combine user's self-reported known concepts from preferences + explicit param
    self_reported = list((preferences.prior_knowledge or {}).get("known_concepts") or [])
    known_norm = {_norm_title(k) for k in (*self_reported, *(known_concepts or [])) if str(k).strip()}
    vault_norm = {_norm_title(v) for v in (vault_titles or []) if str(v).strip()}
    reused_decisions = (existing_reconciliation or {}).get("decisions") or {}

    gaps: list[dict[str, Any]] = []
    user_level = str((preferences.prior_knowledge or {}).get("level") or "intermediate").lower()

    for node in plan.nodes:
        if node.note_role in {"root_index", "group_index"}:
            continue
        declared_prereqs = list(node.prerequisite_ids)
        # Check domain-known prerequisites if not already declared
        inferred = _KNOWN_PREREQ_KNOWLEDGE.get(node.title.strip().lower(), [])
        all_checks: list[tuple[str, str]] = [(p, "declared") for p in declared_prereqs]
        for inf in inferred:
            inf_norm = _norm_title(inf)
            if not any(_norm_title(node_map[p].title if p in node_map else p) == inf_norm for p in declared_prereqs):
                all_checks.append((inf, "inferred"))

        # G5: Excessive prerequisite expansion guard (> 5 declared prerequisites on one focused note)
        if len(declared_prereqs) > 5:
            gaps.append({
                "gap_type": "G5",
                "category": "excessive_prerequisite_expansion",
                "concept_id": node.concept_id,
                "target": node.title,
                "detail": f"Node '{node.title}' lists {len(declared_prereqs)} prerequisites; prune non-essential related topics.",
                "recommended_action": "prune_to_essential_prerequisites",
            })

        for prereq_ref, origin in all_checks:
            prereq_title = node_map[prereq_ref].title if prereq_ref in node_map else prereq_ref
            p_norm = _norm_title(prereq_title)

            # Skip if explicitly self-reported known by the user
            if p_norm in known_norm:
                continue

            # Resolve if present inside plan
            resolved_cid = prereq_ref if prereq_ref in node_map else planned_titles_norm.get(p_norm)
            if resolved_cid is not None:
                # G3: Ordering violation (prerequisite scheduled AFTER dependent in learning_order)
                if resolved_cid in order_pos and node.concept_id in order_pos:
                    if order_pos[resolved_cid] > order_pos[node.concept_id]:
                        gaps.append({
                            "gap_type": "G3",
                            "category": "prerequisite_ordering_violation",
                            "concept_id": node.concept_id,
                            "prerequisite": prereq_title,
                            "detail": f"Prerequisite '{prereq_title}' appears after '{node.title}' in learning_order.",
                            "recommended_action": "reorder_learning_path",
                        })
                # G2: Insufficient coverage on an existing/reused prerequisite
                dec = reused_decisions.get(resolved_cid)
                if dec and dec.get("quality_gaps"):
                    gaps.append({
                        "gap_type": "G2",
                        "category": "insufficient_prerequisite_coverage",
                        "concept_id": node.concept_id,
                        "prerequisite": prereq_title,
                        "detail": f"Prerequisite '{prereq_title}' has coverage gaps: {', '.join(dec['quality_gaps'])}.",
                        "recommended_action": "extend_prerequisite_or_add_bridge",
                    })
                continue

            # If it exists in vault already -> link cleanly (no missing gap!)
            if p_norm in vault_norm:
                continue

            # G4 vs G1: Declared broken concept_id reference vs missing prerequisite concept
            if origin == "declared" and "." in prereq_ref and prereq_ref not in node_map:
                gaps.append({
                    "gap_type": "G4",
                    "category": "broken_prerequisite_reference",
                    "concept_id": node.concept_id,
                    "prerequisite": prereq_ref,
                    "detail": f"Declared prerequisite concept_id '{prereq_ref}' does not exist in plan or vault.",
                    "recommended_action": "repair_or_remove_broken_reference",
                })
            else:
                if preferences.source_policy == "strict":
                    action = "flag_gap_or_source_compatible_bridge"
                elif user_level == "beginner":
                    action = "add_prerequisite_bridge_or_focused_note"
                else:
                    action = "add_concise_prerequisite_reminder"
                gaps.append({
                    "gap_type": "G1",
                    "category": "missing_prerequisite",
                    "concept_id": node.concept_id,
                    "prerequisite": prereq_title,
                    "detail": f"Prerequisite '{prereq_title}' for '{node.title}' is not covered in plan or vault.",
                    "recommended_action": action,
                    "respects_strict_source_policy": preferences.source_policy == "strict",
                })

    return {
        "gap_count": len(gaps),
        "has_blocking_gaps": any(g["gap_type"] in {"G3", "G4"} for g in gaps),
        "gaps": gaps,
        "used_diagnostic_quiz": False,
    }


# ---------------------------------------------------------------------------
# F05 — Intelligent Collection Size Negotiation
# ---------------------------------------------------------------------------

_EXTENSIVE_FIELD_RE = re.compile(
    r"\b(?:everything\s+about|complete\s+(?:artificial\s+intelligence|computer\s+science|mathematics)|"
    r"entire\s+(?:field|curriculum|computer\s+science)|exhaustive\s+detail)\b",
    re.I,
)


def negotiate_collection_scope(
    topic: str,
    raw_request: str,
    preferences: ResolvedNotePreferences,
    *,
    planned_note_count: int = 1,
    existing_reuse_count: int = 0,
    max_single_pass_notes: int = 16,
) -> dict[str, Any]:
    """F05: Evaluate scope realism and offer structured scope packages without false completeness claims."""
    scope_info = classify_topic_scope(topic, raw_request)
    tier = scope_info["level"]
    effective_new = max(0, planned_note_count - existing_reuse_count)
    is_extreme = bool(_EXTENSIVE_FIELD_RE.search(raw_request)) or tier == "S5"
    needs_negotiation = is_extreme or (tier == "S4" and preferences.depth == "exhaustive") or effective_new > max_single_pass_notes

    packages = [
        {
            "id": "foundations",
            "label": "A. Foundations",
            "estimated_notes": "6–10 notes",
            "description": f"Core intuition, terminology, and foundational mechanisms of {topic}.",
        },
        {
            "id": "core_curriculum",
            "label": "B. Core Curriculum",
            "estimated_notes": "12–18 notes",
            "description": f"Structured study hierarchy covering the primary sub-areas of {topic}.",
        },
        {
            "id": "specialized_track",
            "label": "C. Specialized Track",
            "estimated_notes": "10–16 notes",
            "description": f"Focused deep dive into one chosen sub-area of {topic}.",
        },
        {
            "id": "staged_extensive",
            "label": "D. Staged Extensive Collection",
            "estimated_notes": "20+ notes (multi-stage checkpoints)",
            "description": f"Generate {topic} across verified dependency-ordered stages with checkpoints.",
        },
        {
            "id": "custom_scope",
            "label": "E. Custom Scope",
            "estimated_notes": "User-selected",
            "description": "Explicitly select included and excluded subject areas.",
        },
    ]

    selected_scope = preferences.scope_boundary or ("core_curriculum" if tier in {"S3", "S4"} else "focused_topic")
    return {
        "topic": topic,
        "scope_tier": tier,
        "planned_note_count": planned_note_count,
        "existing_reuse_count": existing_reuse_count,
        "net_new_notes": effective_new,
        "needs_negotiation": needs_negotiation,
        "selected_scope": selected_scope,
        "exhaustive_completeness_claimed": False,
        "packages": packages if needs_negotiation else [],
        "disclosure": (
            f"'{topic}' ({tier}) is too broad for a single exhaustive pass; select a bounded scope package."
            if needs_negotiation
            else f"Scope for '{topic}' ({tier}, {effective_new} net new notes) is manageable in a single verified run."
        ),
    }


# ---------------------------------------------------------------------------
# F07 — Adaptive Note Granularity Revision (Split / Merge / Retain)
# ---------------------------------------------------------------------------

_SPLITTABLE_HINTS: dict[str, list[str]] = {
    "gradient descent variants": [
        "Batch Gradient Descent",
        "Stochastic Gradient Descent",
        "Mini-Batch Gradient Descent",
    ],
    "regularization techniques": [
        "L1 Regularization (Lasso)",
        "L2 Regularization (Ridge)",
        "Dropout Regularization",
    ],
    "classification metrics": [
        "Confusion Matrix and Precision-Recall",
        "ROC Curve and AUC",
    ],
}


def evaluate_note_granularity(
    plan: NoteCollectionPlan,
    preferences: ResolvedNotePreferences,
    *,
    committed_paths: set[str] | None = None,
    max_revisions: int = 2,
    current_revision_count: int = 0,
) -> dict[str, Any]:
    """F07: Evaluate planned notes for bounded split, merge, or retain decisions."""
    committed = {p.replace("\\", "/").lower() for p in (committed_paths or set())}
    decisions: list[dict[str, Any]] = []
    if current_revision_count >= max_revisions:
        return {
            "decisions": [],
            "revision_cap_reached": True,
            "reason": f"Bounded granularity revision limit ({max_revisions}) reached; retaining current boundaries.",
        }

    # Detect split candidates
    for node in plan.nodes:
        if node.note_role not in {"child", "single"}:
            continue
        key = node.title.strip().lower()
        is_committed = node.proposed_path.replace("\\", "/").lower() in committed
        if key in _SPLITTABLE_HINTS and preferences.depth in {"comprehensive", "exhaustive"}:
            decisions.append({
                "action": "split",
                "concept_id": node.concept_id,
                "title": node.title,
                "proposed_children": list(_SPLITTABLE_HINTS[key]),
                "requires_approval": is_committed,
                "reason": f"'{node.title}' encompasses multiple independently teachable methods at '{preferences.depth}' depth.",
            })
        else:
            decisions.append({
                "action": "retain",
                "concept_id": node.concept_id,
                "title": node.title,
                "requires_approval": False,
                "reason": "Coherent single-focus note boundary.",
            })

    # Detect overfragmented duplicate/near-duplicate sibling pairs for merge
    children = [n for n in plan.nodes if n.note_role == "child"]
    for i in range(len(children)):
        for j in range(i + 1, len(children)):
            a, b = children[i], children[j]
            if a.parent_id == b.parent_id:
                ta = set(_norm_title(a.title).split())
                tb = set(_norm_title(b.title).split())
                if ta and tb and len(ta & tb) / len(ta | tb) >= 0.8:
                    is_comm = (
                        a.proposed_path.replace("\\", "/").lower() in committed
                        or b.proposed_path.replace("\\", "/").lower() in committed
                    )
                    decisions.append({
                        "action": "merge",
                        "concept_ids": [a.concept_id, b.concept_id],
                        "titles": [a.title, b.title],
                        "requires_approval": is_comm,
                        "reason": f"High conceptual overlap between sibling notes '{a.title}' and '{b.title}'.",
                    })

    return {
        "decisions": decisions,
        "revision_cap_reached": False,
        "proposed_changes": [d for d in decisions if d["action"] in {"split", "merge"}],
    }


def apply_granularity_split(plan: NoteCollectionPlan, target_concept_id: str, child_titles: list[str]) -> NoteCollectionPlan:
    """Safely split a planned note into a parent group index + focused child notes preserving canonical IDs."""
    node_map = {n.concept_id: n for n in plan.nodes}
    if target_concept_id not in node_map:
        raise ValueError(f"Unknown concept_id to split: {target_concept_id}")
    target = node_map[target_concept_id]
    base_dir = Path(target.proposed_path).parent.as_posix()
    folder_name = re.sub(r'[<>:"/\\|?*]', "-", target.title).strip()
    new_dir = f"{base_dir}/{folder_name}" if base_dir and base_dir != "." else folder_name

    # Convert target into a group_index retaining its canonical concept_id!
    new_children: list[TopicNode] = []
    child_ids: list[str] = []
    for title in child_titles:
        cid = f"{target.concept_id}.{slugify(title).replace('-', '_')}"
        child_ids.append(cid)
        safe_fn = re.sub(r'[<>:"/\\|?*]', "-", title).strip()
        new_children.append(TopicNode(
            concept_id=cid,
            title=title,
            parent_id=target.concept_id,
            prerequisite_ids=list(target.prerequisite_ids),
            related_ids=list(target.related_ids),
            proposed_path=f"{new_dir}/{safe_fn}.md",
            note_role="child",
            template_plan=dict(target.template_plan),
            source_bindings=list(target.source_bindings),
        ))

    updated_target = TopicNode(
        concept_id=target.concept_id,
        title=target.title,
        parent_id=target.parent_id,
        child_ids=child_ids,
        prerequisite_ids=list(target.prerequisite_ids),
        related_ids=list(target.related_ids),
        proposed_path=f"{new_dir}/{folder_name}.md",
        note_role="group_index" if target.parent_id else "root_index",
        template_plan={"master": "M7", "note_type": "index", "depth": "standard"},
        source_bindings=list(target.source_bindings),
    )

    new_nodes: list[TopicNode] = []
    for n in plan.nodes:
        if n.concept_id == target_concept_id:
            new_nodes.append(updated_target)
            new_nodes.extend(new_children)
        else:
            new_nodes.append(n)

    child_only = [n.concept_id for n in new_nodes if n.note_role == "child"]
    groups = [n.concept_id for n in new_nodes if n.note_role == "group_index"]
    roots = [n.concept_id for n in new_nodes if n.note_role == "root_index"]
    return NoteCollectionPlan(
        collection_id=plan.collection_id,
        title=plan.title,
        root_topic_id=plan.root_topic_id,
        organization="hierarchical_collection",
        nodes=new_nodes,
        planned_paths=[n.proposed_path for n in new_nodes],
        learning_order=child_only,
        generation_order=[*child_only, *groups, *roots],
        scope_summary={**(plan.scope_summary or {}), "total_notes": len(new_nodes), "child_notes": len(child_only)},
    )


# ---------------------------------------------------------------------------
# F08 — Cross-Note Learning Path Generation
# ---------------------------------------------------------------------------

def generate_learning_paths(
    plan: NoteCollectionPlan,
    preferences: ResolvedNotePreferences,
    *,
    strategy: str = "auto",
    known_concepts: list[str] | None = None,
) -> dict[str, Any]:
    """F08: Build prerequisite-aware reading sequences distinct from folder hierarchy, handling cycles & known skips."""
    content_nodes = [n for n in plan.nodes if n.note_role in {"child", "single"}]
    node_map = {n.concept_id: n for n in content_nodes}

    eff_strategy = strategy
    if eff_strategy == "auto":
        if preferences.preserve_source_order:
            eff_strategy = "source_order"
        elif preferences.master == "M3" or preferences.depth == "concise":
            eff_strategy = "fast_revision"
        elif preferences.master == "M5":
            eff_strategy = "implementation_first"
        elif "mathematics" in preferences.emphasis or "proofs" in preferences.emphasis:
            eff_strategy = "math_first"
        else:
            eff_strategy = "beginner"

    self_reported = list((preferences.prior_knowledge or {}).get("known_concepts") or [])
    known_norm = {_norm_title(k) for k in (*self_reported, *(known_concepts or [])) if str(k).strip()}

    # If source_order strategy, honor exact planned learning_order
    cycles_detected: list[list[str]] = []
    if eff_strategy == "source_order":
        ordered_ids = [cid for cid in plan.learning_order if cid in node_map]
    else:
        # Kahn's topological sort over internal prerequisite edges with strategy-aware tie-breaking
        in_degree: dict[str, int] = {cid: 0 for cid in node_map}
        adj: dict[str, list[str]] = {cid: [] for cid in node_map}
        for cid, node in node_map.items():
            for pid in node.prerequisite_ids:
                if pid in node_map and pid != cid:
                    adj[pid].append(cid)
                    in_degree[cid] += 1

        def _tie_key(cid: str) -> tuple[int, int, str]:
            title = node_map[cid].title.lower()
            base_idx = plan.learning_order.index(cid) if cid in plan.learning_order else 999
            if eff_strategy == "math_first":
                boost = 0 if re.search(r"math|deriv|loss|gradient|prob|linear|matrix|equation", title) else 1
                return (boost, base_idx, title)
            if eff_strategy == "implementation_first":
                boost = 0 if re.search(r"code|implement|algorithm|data|python|c\+\+|search|sort", title) else 1
                return (boost, base_idx, title)
            return (0, base_idx, title)

        ready = sorted([cid for cid, deg in in_degree.items() if deg == 0], key=_tie_key)
        ordered_ids: list[str] = []
        while ready:
            cur = ready.pop(0)
            ordered_ids.append(cur)
            for nxt in adj[cur]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    ready.append(nxt)
            ready.sort(key=_tie_key)

        # Cycle detection & deterministic cycle-breaking fallback
        remaining = [cid for cid in node_map if cid not in ordered_ids]
        if remaining:
            cycles_detected.append(remaining)
            ordered_ids.extend(sorted(remaining, key=_tie_key))

    steps: list[dict[str, Any]] = []
    for idx, cid in enumerate(ordered_ids, 1):
        node = node_map[cid]
        is_known = _norm_title(node.title) in known_norm
        steps.append({
            "step": idx,
            "concept_id": cid,
            "title": node.title,
            "path": node.proposed_path,
            "prerequisite_ids": list(node.prerequisite_ids),
            "skippable_known_concept": is_known,
            "keep_prerequisite_link": True,
        })

    return {
        "strategy": eff_strategy,
        "steps": steps,
        "active_reading_order": [s["concept_id"] for s in steps if not s["skippable_known_concept"]],
        "full_prerequisite_order": ordered_ids,
        "cycles_detected": cycles_detected,
        "distinct_from_folder_hierarchy": True,
    }


# ---------------------------------------------------------------------------
# F09 — Collection-Wide Terminology & Notation Registry
# ---------------------------------------------------------------------------

class CollectionTerminologyRegistry:
    """F09: Scoped collection-wide terminology & symbol governance preserving source notation."""

    def __init__(self, concept_registry: ConceptIdentityRegistry | None = None) -> None:
        self.concept_registry = concept_registry or ConceptIdentityRegistry()
        self._entries: dict[str, dict[str, Any]] = {}
        # (scope, symbol) -> list of concept_ids
        self._symbol_scope: dict[tuple[str, str], list[str]] = {}

    def register_notation(
        self,
        *,
        concept_id: str,
        preferred_term: str,
        preferred_symbol: str,
        accepted_symbols: list[str] | None = None,
        scope: str = "general",
        units: str = "",
        source_specific_mappings: list[dict[str, str]] | None = None,
        definition: str = "",
    ) -> dict[str, Any]:
        entry = {
            "concept_id": concept_id,
            "preferred_term": preferred_term,
            "preferred_symbol": preferred_symbol,
            "accepted_symbols": list(dict.fromkeys([preferred_symbol, *(accepted_symbols or [])])),
            "scope": scope.strip().lower(),
            "units": units.strip(),
            "definition": definition.strip(),
            "source_specific_mappings": list(source_specific_mappings or []),
        }
        self._entries[concept_id] = entry
        key = (entry["scope"], preferred_symbol.strip())
        bucket = self._symbol_scope.setdefault(key, [])
        if concept_id not in bucket:
            bucket.append(concept_id)
        return entry

    def validate_consistency(self, note_usages: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        """Detect same-scope symbol collisions, unit mismatches, and unexplained notation shifts."""
        conflicts: list[dict[str, Any]] = []
        mappings_explained: list[str] = []

        # 1. Same-scope symbol collisions across distinct concepts
        for (scope, sym), cids in self._symbol_scope.items():
            if len(cids) > 1:
                conflicts.append({
                    "type": "same_scope_symbol_collision",
                    "scope": scope,
                    "symbol": sym,
                    "concept_ids": list(cids),
                    "detail": f"Symbol '{sym}' is assigned to multiple concepts {cids} inside the same scope '{scope}'.",
                })

        # 2. Check cross-note usages against registered notation & units
        for usage in note_usages or []:
            cid = str(usage.get("concept_id") or "")
            entry = self._entries.get(cid)
            if not entry:
                continue
            sym = str(usage.get("symbol") or "").strip()
            units = str(usage.get("units") or "").strip()
            source_explained = bool(usage.get("mapping_explained", False))
            preserve_source = bool(usage.get("source_specific", False))

            if sym and sym != entry["preferred_symbol"]:
                if sym in entry["accepted_symbols"]:
                    if source_explained or preserve_source:
                        mappings_explained.append(
                            f"Preserved source symbol '{sym}' for '{entry['preferred_term']}' (canonical: '{entry['preferred_symbol']}')."
                        )
                    else:
                        conflicts.append({
                            "type": "unexplained_symbol_alias",
                            "concept_id": cid,
                            "symbol": sym,
                            "preferred_symbol": entry["preferred_symbol"],
                            "detail": f"Note uses alias '{sym}' instead of '{entry['preferred_symbol']}' without explaining equivalence.",
                        })
                else:
                    conflicts.append({
                        "type": "incompatible_symbol",
                        "concept_id": cid,
                        "symbol": sym,
                        "preferred_symbol": entry["preferred_symbol"],
                        "detail": f"Unregistered symbol '{sym}' used for '{entry['preferred_term']}'.",
                    })

            if units and entry["units"] and units.lower() != entry["units"].lower():
                conflicts.append({
                    "type": "unit_inconsistency",
                    "concept_id": cid,
                    "expected_units": entry["units"],
                    "observed_units": units,
                    "detail": f"Unit mismatch for '{entry['preferred_term']}': expected '{entry['units']}', got '{units}'.",
                })

        return {
            "consistent": not conflicts,
            "registered_count": len(self._entries),
            "conflicts": conflicts,
            "mappings_explained": mappings_explained,
        }

    def to_dict(self) -> dict[str, Any]:
        return {"entries": dict(self._entries)}


# ---------------------------------------------------------------------------
# F10 — Intelligent Cross-Note Synthesis (Reuses M7)
# ---------------------------------------------------------------------------

_SYNTHESIS_CLUSTERS: tuple[tuple[str, set[str], list[str]], ...] = (
    (
        "How Backpropagation and Optimizers Work Together",
        {"backpropagation", "gradient descent", "sgd", "adam", "optimizers", "loss functions"},
        [
            "Forward pass maps inputs to predictions through parameterized layers.",
            "Loss function quantifies prediction error as a scalar objective.",
            "Backpropagation applies the chain rule to compute parameter gradients.",
            "The optimizer (Gradient Descent / SGD / Adam) converts gradients into bounded parameter updates.",
            "Iterative updates repeat across batches until validation performance stabilizes.",
        ],
    ),
    (
        "How Loss Functions, Gradient Descent, and Regularization Interact",
        {"loss functions", "gradient descent", "regularization", "overfitting and underfitting"},
        [
            "The loss function defines the empirical error surface over model parameters.",
            "Regularization adds a complexity penalty that reshapes the objective geometry.",
            "Gradient Descent minimizes the combined objective, trading training fit against generalization.",
        ],
    ),
)


def plan_and_render_synthesis_notes(
    plan: NoteCollectionPlan,
    preferences: ResolvedNotePreferences,
    *,
    domain: str = "Artificial Intelligence",
    master_topic: str | None = None,
) -> list[dict[str, Any]]:
    """F10: Identify high-value multi-concept interactions and render M7 synthesis notes without duplicating child bodies."""
    from scriptorium.engines.vault import build_obsidian_properties, render_note_with_properties

    title_map = {n.title.strip().lower(): n for n in plan.nodes if n.note_role in {"child", "single"}}
    syntheses: list[dict[str, Any]] = []
    root_folder = Path(plan.planned_paths[0]).parts[0] if plan.planned_paths else plan.title

    for synth_title, trigger_set, flow_steps in _SYNTHESIS_CLUSTERS:
        matched_nodes = [node for key, node in title_map.items() if key in trigger_set]
        if len(matched_nodes) >= 2:
            linked_titles = [n.title for n in matched_nodes]
            rel_path = f"{root_folder}/Synthesis/{synth_title}.md"
            props = build_obsidian_properties(
                topic=synth_title,
                note_type="synthesis-revision",
                domain=domain,
                master_topic=master_topic or plan.title,
                parent_topic=plan.title,
                collection_id=plan.collection_id,
                concept_ids=[f"{plan.collection_id}.synthesis.{slugify(synth_title).replace('-', '_')}"],
                related=linked_titles,
                source_mode=preferences.source_policy,
                difficulty=preferences.depth,
                template_id="M7",
                status="active",
                created=date.today(),
            )
            lines = [
                f"# {synth_title}",
                "",
                "## Integrated Conceptual Mechanism",
                "This synthesis note explains how the linked components operate as one unified pipeline without repeating full individual derivations.",
                "",
            ]
            for idx, step in enumerate(flow_steps, 1):
                lines.append(f"{idx}. {step}")
            lines.extend([
                "",
                "## Connected Canonical Notes",
                *[f"- [[{t}]] — canonical definition, equations, and worked examples." for t in linked_titles],
                "",
                "## Scope & Interpretation Note",
                (
                    "Strict source-only mode active: competing source interpretations remain separated rather than merged into unsupported claims."
                    if preferences.source_policy == "strict"
                    else "Follow each linked canonical note for full step-by-step derivations and applicability limits."
                ),
                "",
            ])
            content = render_note_with_properties(props, "\n".join(lines))
            syntheses.append({
                "title": synth_title,
                "master": "M7",
                "note_type": "synthesis-revision",
                "proposed_path": rel_path,
                "linked_concepts": [n.concept_id for n in matched_nodes],
                "linked_titles": linked_titles,
                "content": content,
            })

    return syntheses


# ---------------------------------------------------------------------------
# F11 — Progressive Disclosure Within Notes
# ---------------------------------------------------------------------------

PROGRESSIVE_DISCLOSURE_BY_MASTER: dict[str, dict[str, Any]] = {
    "M1": {"level": "strong", "layers": ["core_idea", "detailed_mechanism", "mathematical_reasoning", "worked_example", "advanced_considerations", "retrieval_summary"], "use_collapsible_advanced": True},
    "M2": {"level": "source_ordered", "layers": ["source_section_core", "local_mechanism", "source_examples", "summary"], "use_collapsible_advanced": False},
    "M3": {"level": "minimal", "layers": ["compact_reference", "applicability_caveats"], "use_collapsible_advanced": False},
    "M4": {"level": "problem_staged", "layers": ["strategy", "step_by_step_solution", "verification", "alternative_methods"], "use_collapsible_advanced": True},
    "M5": {"level": "implementation_staged", "layers": ["overview", "implementation", "execution_trace", "edge_cases_and_tests"], "use_collapsible_advanced": True},
    "M6": {"level": "answer_separated", "layers": ["questions", "hints", "solutions"], "use_collapsible_advanced": True},
    "M7": {"level": "synthesis_layered", "layers": ["core_synthesis", "cross_links", "deeper_connections"], "use_collapsible_advanced": True},
}


def apply_progressive_disclosure(
    note_text: str,
    *,
    master: str = "M1",
    topic: str = "",
    advanced_note: str | None = None,
) -> dict[str, Any]:
    """F11: Organize layered explanations in Obsidian-native Markdown without hiding essential definitions."""
    policy = PROGRESSIVE_DISCLOSURE_BY_MASTER.get(master, PROGRESSIVE_DISCLOSURE_BY_MASTER["M1"])
    parsed = parse_note(note_text)
    updated_text = note_text

    # Only add a collapsible Obsidian callout for genuinely optional advanced considerations (never hide core definitions!)
    if policy["use_collapsible_advanced"] and advanced_note and "> [!note]- Advanced Considerations" not in note_text:
        callout = f"\n> [!note]- Advanced Considerations ({topic or parsed.title or 'Optional Depth'})\n> {advanced_note.strip()}\n"
        updated_text = note_text.rstrip() + "\n" + callout

    return {
        "master": master,
        "policy": policy,
        "essential_content_visible": True,
        "obsidian_compatible": True,
        "content": updated_text,
    }


# ---------------------------------------------------------------------------
# F12 — Learning Outcomes & Competency Coverage
# ---------------------------------------------------------------------------

OUTCOME_CATEGORIES: frozenset[str] = frozenset({
    "recognition", "explanation", "discrimination", "calculation",
    "derivation", "application", "implementation", "debugging",
    "prediction", "evaluation", "transfer",
})


def define_learning_outcomes(node: TopicNode, preferences: ResolvedNotePreferences) -> list[dict[str, Any]]:
    """F12: Define concise, distinct learning outcomes aligned with the node's master & depth (no inflation)."""
    slug = slugify(node.title).replace("-", "_")
    master = (node.template_plan or {}).get("master") or preferences.master or "M1"
    outcomes: list[dict[str, Any]] = [
        {
            "id": f"{slug}.explain_mechanism",
            "category": "explanation",
            "action": "explain",
            "target": f"core mechanism and motivation of {node.title}",
            "expected_signals": ["mechanism", "motivation", "core", "idea", "why"],
        },
        {
            "id": f"{slug}.evaluate_conditions",
            "category": "evaluation",
            "action": "evaluate",
            "target": f"applicability conditions and limitations of {node.title}",
            "expected_signals": ["condition", "assumption", "limit", "fail", "valid"],
        },
    ]
    if master in {"M1", "M4"} and ("mathematics" in preferences.emphasis or _HIGH_COMPLEXITY_HINTS.search(node.title)):
        outcomes.append({
            "id": f"{slug}.calculate_or_derive",
            "category": "calculation",
            "action": "calculate",
            "target": f"concrete step-by-step updates or calculations for {node.title}",
            "expected_signals": ["step", "example", "iteration", "equation", "="],
        })
    if master == "M5" or "code" in preferences.emphasis:
        outcomes.append({
            "id": f"{slug}.implement_and_verify",
            "category": "implementation",
            "action": "implement",
            "target": f"correct implementation and edge-case verification for {node.title}",
            "expected_signals": ["```", "test", "edge", "invariant", "verify"],
        })
    return outcomes


def validate_competency_coverage(note_text: str, outcomes: list[dict[str, Any]]) -> dict[str, Any]:
    """F12: Check whether note content supports declared outcomes without claiming demonstrated learner mastery."""
    lowered = parse_note(note_text).body.lower()
    supported: list[str] = []
    unsupported: list[dict[str, Any]] = []
    for oc in outcomes:
        signals = [str(s).lower() for s in (oc.get("expected_signals") or [])]
        matched = [s for s in signals if s in lowered]
        if matched:
            supported.append(oc["id"])
        else:
            unsupported.append({
                "outcome_id": oc["id"],
                "category": oc.get("category"),
                "target": oc.get("target"),
                "missing_signals": signals,
            })
    return {
        "covered": not unsupported,
        "total_outcomes": len(outcomes),
        "supported_outcomes": supported,
        "unsupported_outcomes": unsupported,
        "claims_learner_mastery": False,  # Content coverage != learner mastery!
    }


# ---------------------------------------------------------------------------
# F13 — Collection-Wide Assessment Blueprint (Reuses M6, NO Pre-Gen Diagnostic)
# ---------------------------------------------------------------------------

def build_collection_assessment(
    plan: NoteCollectionPlan,
    preferences: ResolvedNotePreferences,
    competencies: dict[str, list[dict[str, Any]]],
    *,
    answer_mode: str = "hints_then_solutions",
    domain: str = "Artificial Intelligence",
) -> dict[str, Any]:
    """F13: Generate a competency-aligned M6 collection assessment across multiple skill types."""
    from scriptorium.engines.vault import build_obsidian_properties, render_note_with_properties

    child_nodes = [n for n in plan.nodes if n.note_role in {"child", "single"}]
    questions: list[dict[str, Any]] = []
    for idx, node in enumerate(child_nodes[:6], 1):
        oc_list = competencies.get(node.concept_id) or define_learning_outcomes(node, preferences)
        primary_oc = oc_list[0]
        if any(o["category"] == "implementation" for o in oc_list):
            q_type = "coding"
            prompt = f"Implement a minimal verified routine for **{node.title}** and state one boundary edge case it must guard against."
            hint = f"Identify the invariant preserved on each iteration of {node.title}."
            answer = f"Check termination, empty/boundary inputs, and the core invariant documented in [[{node.title}]]."
        elif any(o["category"] == "calculation" for o in oc_list):
            q_type = "calculation"
            prompt = f"Given a concrete small input, trace one full computational update step of **{node.title}** and verify the direction of change."
            hint = f"Substitute the exact symbol values defined in [[{node.title}]] before evaluating."
            answer = f"Compute the intermediate sensitivity/gradient term first, apply the update rule, and verify the bound from [[{node.title}]]."
        else:
            q_type = "conceptual"
            prompt = f"Explain the core mechanism of **{node.title}** and state one condition under which it breaks down."
            hint = f"Recall the central guiding question and applicability limits in [[{node.title}]]."
            answer = f"Refer to the mechanism and applicability boundaries in [[{node.title}]]."

        questions.append({
            "id": f"Q{idx}",
            "concept_id": node.concept_id,
            "title": node.title,
            "skill_type": q_type,
            "difficulty": "foundational" if idx <= 2 else ("intermediate" if idx <= 4 else "integrative"),
            "outcome_id": primary_oc["id"],
            "prompt": prompt,
            "hint": hint,
            "answer": answer,
        })

    # Add an integrative cross-topic question when >= 2 concepts exist
    if len(child_nodes) >= 2:
        a, b = child_nodes[0], child_nodes[-1]
        questions.append({
            "id": f"Q{len(questions) + 1}",
            "concept_id": f"{plan.collection_id}.integrative",
            "title": f"{a.title} + {b.title}",
            "skill_type": "integrative",
            "difficulty": "integrative",
            "outcome_id": f"{plan.collection_id}.cross_topic_transfer",
            "prompt": f"Compare how **[[{a.title}]]** and **[[{b.title}]]** connect inside {plan.title}, and diagnose what fails if the prerequisite condition between them is violated.",
            "hint": f"Trace how outputs from [[{a.title}]] feed into or constrain [[{b.title}]].",
            "answer": f"Explain the causal handoff between [[{a.title}]] and [[{b.title}]] and identify the specific violated assumption.",
        })

    # Render M6 Markdown note honoring answer_mode separation
    root_folder = Path(plan.planned_paths[0]).parts[0] if plan.planned_paths else plan.title
    assessment_title = f"{plan.title} — Collection Assessment"
    assessment_path = f"Practice Sets/{plan.title} - Collection Assessment.md"
    props = build_obsidian_properties(
        topic=assessment_title,
        note_type="assessment",
        domain=domain,
        master_topic=plan.title,
        parent_topic=plan.title,
        collection_id=plan.collection_id,
        related=[n.title for n in child_nodes[:6]],
        source_mode=preferences.source_policy,
        difficulty=preferences.depth,
        template_id="M6",
        status="active",
        created=date.today(),
    )
    lines = [f"# {assessment_title}", "", f"**Parent Collection:** [[{plan.title}]]", ""]
    lines.append("## Assessment Questions")
    for q in questions:
        lines.append(f"### {q['id']} — {q['title']} ({q['skill_type']}, {q['difficulty']})")
        lines.append(q["prompt"])
        if answer_mode == "hints_then_solutions":
            lines.append(f"\n> [!tip]- Hint ({q['id']})\n> {q['hint']}")
            lines.append(f"\n> [!note]- Answer Key ({q['id']})\n> {q['answer']}")
        elif answer_mode == "inline_answers" or answer_mode == "worked_solutions":
            lines.append(f"\n- **Answer ({q['id']}):** {q['answer']}")
        lines.append("")

    if answer_mode == "separate_key":
        lines.append("## Separate Answer Key")
        for q in questions:
            lines.append(f"- **{q['id']}**: {q['answer']}")
        lines.append("")

    content = render_note_with_properties(props, "\n".join(lines))
    return {
        "master": "M6",
        "note_type": "assessment",
        "answer_mode": answer_mode,
        "proposed_path": assessment_path,
        "skill_types_covered": sorted({q["skill_type"] for q in questions}),
        "questions": questions,
        "content": content,
        "is_pre_generation_diagnostic": False,  # Strictly NOT Feature 1!
    }


# ---------------------------------------------------------------------------
# F06 — Dependency-Aware Generation Checkpoints & Idempotent Resume
# ---------------------------------------------------------------------------

def generate_collection_with_checkpoints(
    vault_root: Path,
    kcp: KnowledgeCollectionPlan,
    preferences: ResolvedNotePreferences,
    *,
    batch_size: int = 5,
    fail_on_concept_id: str | None = None,
    resume: bool = True,
    source_facts_by_node: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    """F06: Execute dependency-ordered batches with SHA-256 checkpoints, honest partial reporting, and idempotent resume."""
    from scriptorium.engines.vault import (
        _compose_child_note,
        classify_knowledge_hierarchy,
        incremental_update_note,
        render_parent_moc,
        safe_write_note,
        validate_obsidian_properties,
    )

    assert kcp.plan is not None, "KnowledgeCollectionPlan.plan must be populated before generation."
    plan = kcp.plan
    vault_root = Path(vault_root)
    vault_root.mkdir(parents=True, exist_ok=True)
    node_map = {n.concept_id: n for n in plan.nodes}
    root_h = classify_knowledge_hierarchy(plan.title)
    root_domain = root_h["domain"]
    root_mt = root_h["master_topic"] if root_h["master_topic"] != "General Knowledge" else plan.title

    ckpt_dir = vault_root / ".scriptorium" / "collections"
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    ckpt_path = ckpt_dir / f"{plan.collection_id}.checkpoint.json"

    # Load and REVALIDATE existing checkpoint on resume (never blindly trust stale metadata!)
    committed_hashes: dict[str, str] = {}
    note_states: dict[str, str] = {n.concept_id: "PLANNED" for n in plan.nodes}
    if resume and ckpt_path.is_file():
        try:
            prev = json.loads(ckpt_path.read_text(encoding="utf-8"))
            for cid, info in (prev.get("committed") or {}).items():
                fpath = vault_root / info["path"]
                if fpath.is_file():
                    actual_hash = content_hash(fpath.read_text(encoding="utf-8-sig"))
                    if actual_hash == info.get("sha256"):
                        committed_hashes[cid] = actual_hash
                        note_states[cid] = "COMMITTED"
                    else:
                        note_states[cid] = "NEEDS_REVIEW"
                else:
                    note_states[cid] = "PLANNED"
        except Exception:
            # Corrupted checkpoint metadata -> safely rebuild from scratch without crashing silently
            committed_hashes = {}

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
            committed_records[cid] = {"path": node_map[cid].proposed_path, "sha256": digest, "validated": True}

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
            target_path = vault_root / node.proposed_path
            try:
                if fail_on_concept_id and cid == fail_on_concept_id:
                    raise RuntimeError(f"Injected failure on '{cid}' for checkpoint recovery test.")

                if node.note_role in {"root_index", "group_index"}:
                    content = render_parent_moc(
                        node, plan, node_map, preferences, domain=root_domain, master_topic=root_mt
                    )
                else:
                    facts = (source_facts_by_node or {}).get(cid)
                    content = _compose_child_note(
                        node, plan, node_map, preferences, domain=root_domain, master_topic=root_mt, source_facts=facts
                    )
                    # Apply F11 progressive disclosure if applicable
                    m_id = (node.template_plan or {}).get("master") or preferences.master
                    pd_res = apply_progressive_disclosure(content, master=m_id, topic=node.title)
                    content = pd_res["content"]

                note_states[cid] = "VALIDATING"
                errs = validate_obsidian_properties(content)
                if errs:
                    raise ValueError("; ".join(errs))
                note_states[cid] = "VALIDATED"

                # Safe non-destructive reconciliation if file exists
                if target_path.exists():
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

                safe_write_note(target_path, content, validate_properties=True)
                digest = content_hash(target_path.read_text(encoding="utf-8-sig"))
                committed_records[cid] = {"path": node.proposed_path, "sha256": digest, "validated": True}
                note_states[cid] = "COMMITTED"
            except Exception as exc:
                note_states[cid] = "FAILED"
                failed_nodes.append({"concept_id": cid, "title": node.title, "path": node.proposed_path, "error": str(exc)})

        # Save checkpoint atomically after every batch
        ckpt_payload = {
            "collection_id": plan.collection_id,
            "batch_completed": batch_idx,
            "total_batches": len(batches),
            "note_states": note_states,
            "committed": committed_records,
            "failed": failed_nodes,
            "pending": [cid for cid, st in note_states.items() if st in {"PLANNED", "READY", "DEFERRED", "FAILED"}],
            "complete": not failed_nodes and all(st in {"COMMITTED", "REUSED"} for st in note_states.values()),
        }
        ckpt_path.write_text(json.dumps(ckpt_payload, indent=2, ensure_ascii=False), encoding="utf-8")

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
    }
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")

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
        "reused_count": sum(1 for st in note_states.values() if st == "REUSED"),
        "skipped_already_committed": skipped_already_committed,
        "failed_count": len(failed_nodes),
        "failed_nodes": failed_nodes,
        "checkpoint_path": str(ckpt_path),
        "manifest_path": str(manifest_path),
        "note_states": note_states,
        "manifest": manifest,
    }


# ---------------------------------------------------------------------------
# F14 — Collection Versioning & Change-Impact Analysis
# ---------------------------------------------------------------------------

def analyze_collection_change_impact(
    plan: NoteCollectionPlan,
    changed_concept_id: str,
    old_text: str,
    new_text: str,
    *,
    manually_edited: set[str] | None = None,
    synthesis_notes: list[dict[str, Any]] | None = None,
    assessment_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """F14: Classify semantic changes and produce a targeted downstream review queue without cascading rebuilds."""
    sem = detect_semantic_changes(old_text, new_text)
    base_type = sem["change_type"]

    # Map fine-grained change type
    if base_type in {"none", "cosmetic"}:
        fine_type = "formatting"
    elif "evidence" in sem["categories"]:
        fine_type = "source_update"
    elif "semantic" in sem["categories"]:
        fine_type = "equation_correction" if ("$" in old_text or "$" in new_text) else "definition_change"
    elif "structural" in sem["categories"]:
        fine_type = "structural_split_merge"
    elif "implementation" in sem["categories"]:
        fine_type = "example_change"
    else:
        fine_type = "wording"

    # Build downstream dependency graph: prerequisite -> dependents + parent + synthesis + assessment
    dep_graph: dict[str, list[str]] = {}
    node_map = {n.concept_id: n for n in plan.nodes}
    for n in plan.nodes:
        for pid in n.prerequisite_ids:
            dep_graph.setdefault(pid, []).append(n.concept_id)
        for rid in n.related_ids:
            dep_graph.setdefault(rid, []).append(n.concept_id)
        if n.parent_id:
            dep_graph.setdefault(n.concept_id, []).append(n.parent_id)

    for synth in synthesis_notes or []:
        sid = f"synthesis:{synth['title']}"
        for cid in synth.get("linked_concepts") or []:
            dep_graph.setdefault(cid, []).append(sid)

    if assessment_plan:
        aid = f"assessment:{assessment_plan.get('proposed_path', 'collection')}"
        for q in assessment_plan.get("questions") or []:
            if q.get("concept_id"):
                dep_graph.setdefault(q["concept_id"], []).append(aid)

    # Formatting-only changes NEVER trigger downstream regeneration or review!
    if fine_type == "formatting":
        return {
            "changed_concept_id": changed_concept_id,
            "change_type": fine_type,
            "semantic_diff": sem,
            "requires_downstream_review": False,
            "review_queue": [],
            "manual_edit_conflicts": [],
        }

    impact = compute_change_impact([changed_concept_id], dep_graph, manually_edited=manually_edited)
    review_queue = [
        {
            "target_id": target_id,
            "title": node_map[target_id].title if target_id in node_map else target_id,
            "status": "needs_review",
            "manual_conflict": target_id in (manually_edited or set()),
            "reason": f"Depends on '{changed_concept_id}' which underwent '{fine_type}'.",
        }
        for target_id in impact["impacted"]
    ]

    return {
        "changed_concept_id": changed_concept_id,
        "change_type": fine_type,
        "semantic_diff": sem,
        "requires_downstream_review": bool(review_queue),
        "review_queue": review_queue,
        "manual_edit_conflicts": impact["manual_edit_conflicts"],
    }


# ---------------------------------------------------------------------------
# F15 — Post-Generation Personalization (Explicit Reader Feedback)
# ---------------------------------------------------------------------------

_FEEDBACK_PATTERNS: tuple[tuple[re.Pattern[str], str, str], ...] = (
    (re.compile(r"\b(?:assumes?\s+i\s+(?:already\s+)?know|missing\s+prerequisite|haven'?t\s+learned)\b", re.I), "missing_prerequisite", "insert_prerequisite_bridge"),
    (re.compile(r"\b(?:too\s+fast|too\s+difficult|too\s+hard|overwhelming|lost\s+me)\b", re.I), "too_difficult", "expand_intermediate_steps_and_simplify"),
    (re.compile(r"\b(?:too\s+shallow|too\s+brief|more\s+depth|needs?\s+more\s+detail)\b", re.I), "too_shallow", "deepen_mechanism_and_derivation"),
    (re.compile(r"\b(?:more\s+intuitive|intuition|don'?t\s+understand\s+why|confusing)\b", re.I), "confusing_explanation", "add_intuitive_motivation_and_walkthrough"),
    (re.compile(r"\b(?:unclear\s+formula|equation|symbol|notation)\b", re.I), "unclear_formula", "clarify_symbol_roles_and_equation_meaning"),
    (re.compile(r"\b(?:more\s+examples?|insufficient\s+examples?|numerical\s+example)\b", re.I), "insufficient_examples", "add_concrete_worked_example"),
    (re.compile(r"\b(?:code\s+trace|recursion\s+example|bug|wrong\s+output)\b", re.I), "incorrect_code_trace", "repair_state_trace_and_verify"),
    (re.compile(r"\b(?:wrong|incorrect|factual\s+error|mistake)\b", re.I), "factual_error", "verify_and_correct_claim"),
    (re.compile(r"\b(?:repetitive|repetition|repeats?\s+itself)\b", re.I), "excessive_repetition", "deduplicate_prose"),
)


def process_reader_feedback(
    vault_root: Path,
    plan: NoteCollectionPlan | None,
    feedback_text: str,
    *,
    target_note_path: Path | None = None,
    apply_approved: bool = False,
    source_policy: str = "adaptive",
) -> dict[str, Any]:
    """F15: Locate target note/section from explicit reader feedback, propose or safely apply a localized improvement."""
    from scriptorium.engines.vault import incremental_update_note, safe_write_note

    vault_root = Path(vault_root)
    fb = feedback_text.strip()
    fb_low = fb.lower()

    # 1. Classify feedback category
    fb_category = "confusing_explanation"
    repair_strategy = "add_intuitive_motivation_and_walkthrough"
    for pat, cat, strat in _FEEDBACK_PATTERNS:
        if pat.search(fb):
            fb_category, repair_strategy = cat, strat
            break

    # 2. Locate target note (explicit path, filename mention, or vault title match)
    candidates: list[Path] = []
    if target_note_path is not None:
        resolved = target_note_path if target_note_path.is_absolute() else (vault_root / target_note_path)
        if resolved.is_file():
            candidates = [resolved]
    else:
        for md in sorted(vault_root.rglob("*.md")):
            if any(part.startswith(".") for part in md.relative_to(vault_root).parts):
                continue
            stem_low = md.stem.lower()
            if md.name.lower() in fb_low or (len(stem_low) >= 4 and stem_low in fb_low):
                candidates.append(md)

    if not candidates:
        return {
            "status": "note_not_found",
            "feedback_category": fb_category,
            "applied": False,
            "message": "Could not identify which note your feedback refers to. Please specify the note title or path.",
            "claims_learner_mastery": False,
        }
    if len(candidates) > 1:
        return {
            "status": "ambiguous_note_reference",
            "feedback_category": fb_category,
            "candidates": [c.relative_to(vault_root).as_posix() for c in candidates],
            "applied": False,
            "message": "Multiple notes match your feedback; please specify which note to refine.",
            "claims_learner_mastery": False,
        }

    note_path = candidates[0]
    old_text = note_path.read_text(encoding="utf-8-sig")
    parsed = parse_note(old_text)

    # 3. Identify target section inside note
    target_section = None
    for sec in parsed.sections:
        if any(tok in fb_low for tok in _norm_title(sec.heading).split() if len(tok) >= 4):
            target_section = sec
            break
    if target_section is None and parsed.sections:
        target_section = parsed.sections[0]

    sec_heading = target_section.heading if target_section else "Motivation and Core Idea"
    old_sec_body = "\n".join(target_section.content.splitlines()[1:]).strip() if target_section else ""

    # 4. Build localized, source-safe improvement
    if source_policy == "strict":
        addition = (
            f"\n\n> [!info] Targeted Clarification ({fb_category.replace('_', ' ')})\n"
            "> Restating the existing supplied-source reasoning step by step without adding external facts: "
            "connect each intermediate step directly to the stated assumption and symbol definition above."
        )
    elif fb_category == "missing_prerequisite":
        addition = (
            "\n\n> [!tip] Prerequisite Bridge\n"
            "> Before reading this step, recall the prerequisite operation referenced above: "
            "verify input dimensions/domains first, then trace how each output element combines inputs linearly."
        )
    elif fb_category in {"confusing_explanation", "too_difficult", "unclear_formula"}:
        addition = (
            "\n\n> [!tip] Step-by-Step Intuition\n"
            "> Break the transition into two smaller moves: (1) evaluate the local sensitivity (rate of change) "
            "at the current point, and (2) move in the direction that strictly reduces error while verifying each intermediate value."
        )
    else:
        addition = (
            "\n\n> [!tip] Concrete Worked Check\n"
            "> Test the rule on a minimal numerical instance first, verify every intermediate quantity, "
            "and confirm the boundary condition holds before generalizing."
        )

    proposed_body = (old_sec_body + addition).strip()
    upd = incremental_update_note(
        old_text,
        section_updates={sec_heading: proposed_body},
        update_date=date.today(),
    )

    if not apply_approved:
        return {
            "status": "proposal_ready",
            "applied": False,
            "requires_approval": True,
            "target_note": note_path.relative_to(vault_root).as_posix(),
            "target_section": sec_heading,
            "feedback_category": fb_category,
            "repair_strategy": repair_strategy,
            "source_policy": source_policy,
            "proposed_addition": addition.strip(),
            "claims_learner_mastery": False,
        }

    safe_write_note(note_path, upd["content"], validate_properties=True)
    impact = None
    if plan is not None:
        rel_str = note_path.relative_to(vault_root).as_posix().lower()
        matched_node = next((n for n in plan.nodes if n.proposed_path.lower() == rel_str), None)
        if matched_node:
            impact = analyze_collection_change_impact(plan, matched_node.concept_id, old_text, upd["content"])

    return {
        "status": "applied",
        "applied": True,
        "target_note": note_path.relative_to(vault_root).as_posix(),
        "target_section": sec_heading,
        "feedback_category": fb_category,
        "repair_strategy": repair_strategy,
        "source_policy": source_policy,
        "modified_sections": upd["modified_sections"],
        "downstream_impact": impact,
        "claims_learner_mastery": False,
    }


# ---------------------------------------------------------------------------
# Unified KCP Builder (Coordinates F02-F13 before Generation)
# ---------------------------------------------------------------------------

def build_knowledge_collection_plan(
    vault_root: Path,
    plan: NoteCollectionPlan,
    preferences: ResolvedNotePreferences,
    *,
    raw_request: str = "",
    budget_notes: int | None = None,
    user_priorities: list[str] | None = None,
    known_concepts: list[str] | None = None,
    include_synthesis: bool = True,
    include_assessment: bool = False,
    answer_mode: str = "hints_then_solutions",
) -> KnowledgeCollectionPlan:
    """Build a coordinated KnowledgeCollectionPlan (KCP) linking F02-F13 cleanly."""
    from scriptorium.engines.vault import classify_knowledge_hierarchy

    vault_root = Path(vault_root)
    vault_titles = [
        p.stem for p in vault_root.rglob("*.md")
        if not any(part.startswith(".") for part in p.relative_to(vault_root).parts)
    ] if vault_root.is_dir() else []

    reuse = reconcile_existing_vault_notes(vault_root, plan, preferences)
    gaps = analyze_prerequisite_gaps(
        plan, preferences, existing_reconciliation=reuse, known_concepts=known_concepts, vault_titles=vault_titles
    )
    negotiation = negotiate_collection_scope(
        plan.title,
        raw_request or plan.title,
        preferences,
        planned_note_count=len(plan.nodes),
        existing_reuse_count=reuse["reused_count"],
    )
    depth_alloc = allocate_collection_depth(plan, preferences, budget_notes=budget_notes, user_priorities=user_priorities)
    granularity = evaluate_note_granularity(plan, preferences)
    learning_paths = generate_learning_paths(plan, preferences, known_concepts=known_concepts)

    # F12 competencies for all child/single notes
    competencies = {
        n.concept_id: define_learning_outcomes(n, preferences)
        for n in plan.nodes
        if n.note_role in {"child", "single"}
    }

    # F09 terminology registry baseline
    term_reg = CollectionTerminologyRegistry()
    hier = classify_knowledge_hierarchy(plan.title)
    if hier["domain"] == "Artificial Intelligence":
        term_reg.register_notation(
            concept_id="ml.optimization.loss",
            preferred_term="loss_function",
            preferred_symbol="J",
            accepted_symbols=["J", "L", "E"],
            scope="machine_learning",
        )
        term_reg.register_notation(
            concept_id="ml.optimization.learning_rate",
            preferred_term="learning_rate",
            preferred_symbol="α",
            accepted_symbols=["α", "η", "alpha", "eta"],
            scope="machine_learning",
        )

    # F10 synthesis notes & F13 assessment blueprint
    syntheses = plan_and_render_synthesis_notes(plan, preferences, domain=hier["domain"]) if include_synthesis else []
    assessment = (
        build_collection_assessment(plan, preferences, competencies, answer_mode=answer_mode, domain=hier["domain"])
        if include_assessment
        else {}
    )

    return KnowledgeCollectionPlan(
        schema_version="1.0",
        collection_id=plan.collection_id,
        topic=plan.title,
        configuration={
            "master": preferences.master,
            "variant": preferences.variant,
            "depth": preferences.depth,
            "organization": preferences.organization,
            "source_policy": preferences.source_policy,
            "preserve_source_order": preferences.preserve_source_order,
            "emphasis": list(preferences.emphasis),
        },
        scope={
            "selected_scope": negotiation["selected_scope"],
            "scope_tier": negotiation["scope_tier"],
            "exhaustive_completeness_claimed": False,
        },
        plan=plan,
        depth_allocation=depth_alloc,
        existing_note_reconciliation=reuse,
        prerequisite_gaps=gaps["gaps"],
        scope_negotiation=negotiation,
        granularity_decisions=granularity["decisions"],
        learning_paths=learning_paths,
        terminology_registry=term_reg.to_dict(),
        synthesis_notes=syntheses,
        progressive_disclosure_policy=PROGRESSIVE_DISCLOSURE_BY_MASTER.get(preferences.master, PROGRESSIVE_DISCLOSURE_BY_MASTER["M1"]),
        competencies=competencies,
        assessment_plan=assessment,
        diagnostic_quiz_enabled=False,
    )
