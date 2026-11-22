"""Engine E3 — Knowledge Integrity Engine for Scriptorium.

Consolidates:
- Mechanism 5: Concept Identity Registry (canonical IDs, aliases, domain disambiguation, source notation)
- Mechanism 6: Coverage Ledger (source, objective, and master-aware coverage tracking)
- Mechanism 11: Source-to-Claim Traceability (claim registry, strict source-only enforcement)
- Mechanism 12: Uncertainty and Assumption Ledger (verified/supported/inferred/assumed/unverified)
- Mechanism 14: Multi-Artifact Consistency Engine (shared concept specs, notation, Properties sync)
- Mechanism 17: Semantic Change Detection & Change Impact Graph
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
import re
from typing import Any

from scriptorium.models import (
    ConceptIdentityError,
    MissingEvidenceError,
    parse_note,
    slugify,
)


# ---------------------------------------------------------------------------
# Mechanism 5 — Concept Identity Registry (Section 14)
# ---------------------------------------------------------------------------

@dataclass
class ConceptRecord:
    concept_id: str
    canonical_name: str
    domain: str
    master_topic: str
    subdomain: str = ""
    aliases: list[str] = field(default_factory=list)
    definition: str = ""
    symbols: dict[str, dict[str, Any]] = field(default_factory=dict)
    prerequisites: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    note_paths: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)


class ConceptIdentityRegistry:
    """Maintain canonical concept identities with domain-aware disambiguation and notation mapping."""

    def __init__(self) -> None:
        self._records: dict[str, ConceptRecord] = {}
        # Normalized alias/name -> list of concept_ids (supports homonyms across domains!)
        self._lookup: dict[str, list[str]] = {}

    @staticmethod
    def _norm(text: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", str(text or "").strip().lower()).strip()

    def register(self, record: ConceptRecord | dict[str, Any]) -> ConceptRecord:
        if isinstance(record, dict):
            cid = record.get("concept_id") or self.make_concept_id(
                record.get("domain", "general"),
                record.get("master_topic", "general"),
                record["canonical_name"],
            )
            rec = ConceptRecord(
                concept_id=cid,
                canonical_name=record["canonical_name"],
                domain=record.get("domain", "General"),
                master_topic=record.get("master_topic", "General"),
                subdomain=record.get("subdomain", ""),
                aliases=list(record.get("aliases") or []),
                definition=record.get("definition", ""),
                symbols=dict(record.get("symbols") or {}),
                prerequisites=list(record.get("prerequisites") or []),
                related=list(record.get("related") or []),
                note_paths=list(record.get("note_paths") or []),
                source_refs=list(record.get("source_refs") or []),
            )
        else:
            rec = record

        self._records[rec.concept_id] = rec
        for key in (rec.canonical_name, *rec.aliases, rec.concept_id):
            norm = self._norm(key)
            if norm:
                bucket = self._lookup.setdefault(norm, [])
                if rec.concept_id not in bucket:
                    bucket.append(rec.concept_id)
        return rec

    @staticmethod
    def make_concept_id(domain: str, master_topic: str, canonical_name: str) -> str:
        d = slugify(domain).replace("-", "_")
        m = slugify(master_topic).replace("-", "_")
        c = slugify(canonical_name).replace("-", "_")
        return f"{d}.{m}.{c}"

    def resolve(self, query: str, *, domain: str | None = None, master_topic: str | None = None) -> ConceptRecord | None:
        if query in self._records:
            return self._records[query]
        candidates = self._lookup.get(self._norm(query), [])
        if not candidates:
            return None
        if len(candidates) == 1:
            rec = self._records[candidates[0]]
            if domain and self._norm(rec.domain) != self._norm(domain):
                return None
            return rec

        # Domain/master_topic disambiguation (never force false equivalence across domains!)
        filtered = candidates
        if domain:
            by_dom = [cid for cid in filtered if self._norm(self._records[cid].domain) == self._norm(domain)]
            if by_dom:
                filtered = by_dom
        if master_topic and len(filtered) > 1:
            by_mt = [cid for cid in filtered if self._norm(self._records[cid].master_topic) == self._norm(master_topic)]
            if by_mt:
                filtered = by_mt
        if len(filtered) == 1:
            return self._records[filtered[0]]
        raise ConceptIdentityError(
            f"Ambiguous concept '{query}' matches multiple domains: {filtered}. Provide domain context."
        )

    def explain_symbol_equivalence(self, concept_id: str, source_symbol: str) -> dict[str, Any]:
        """Preserve source notation while documenting equivalence to canonical preferred symbol."""
        rec = self._records.get(concept_id)
        if not rec:
            raise ConceptIdentityError(f"Unknown concept_id: {concept_id}")
        sym_clean = source_symbol.strip().lstrip("\\")
        for role, spec in rec.symbols.items():
            preferred = str(spec.get("preferred", "")).strip().lstrip("\\")
            aliases = [str(a).strip().lstrip("\\") for a in (spec.get("aliases") or [])]
            if sym_clean == preferred:
                return {"role": role, "source_symbol": source_symbol, "preferred": preferred, "equivalent": True, "preserve_source_notation": True}
            if sym_clean in aliases:
                return {
                    "role": role,
                    "source_symbol": source_symbol,
                    "preferred": preferred,
                    "equivalent": True,
                    "preserve_source_notation": True,
                    "note": f"Source uses '{source_symbol}' for {role} (equivalent to canonical '{preferred}').",
                }
        return {"role": None, "source_symbol": source_symbol, "preferred": None, "equivalent": False, "preserve_source_notation": True}

    def all_records(self) -> list[ConceptRecord]:
        return list(self._records.values())


# ---------------------------------------------------------------------------
# Mechanism 6 — Coverage Ledger (Section 15)
# ---------------------------------------------------------------------------

VALID_COVERAGE_STATES = frozenset({"covered", "partial", "deferred", "missing", "not_applicable"})


def evaluate_coverage_ledger(
    required_concepts: list[dict[str, Any]],
    note_text: str,
    *,
    master: str = "M1",
    deferrals: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Mechanism 6: Track source, learning-objective, and master-aware concept coverage."""
    parsed = parse_note(note_text)
    lowered = parsed.body.lower()
    deferrals = deferrals or {}
    entries: list[dict[str, Any]] = []
    missing_essential: list[dict[str, Any]] = []

    for item in required_concepts:
        cid = str(item.get("concept") or item.get("id") or "")
        requirement = str(item.get("requirement", "essential"))
        keywords = [str(k).lower() for k in (item.get("keywords") or [cid.replace("_", " ")])]
        intended_section = str(item.get("intended_section", ""))

        if cid in deferrals:
            reason = str(deferrals[cid]).strip()
            if not reason:
                raise ValueError(f"Deferred concept '{cid}' requires a non-empty justification reason.")
            entries.append({"concept": cid, "requirement": requirement, "status": "deferred", "reason": reason})
            continue

        # Master-aware relaxation: M3 (quick-reference) does not require full proof/derivation subsections
        if master == "M3" and requirement == "derivation_detail":
            entries.append({"concept": cid, "requirement": requirement, "status": "not_applicable", "reason": "M3 quick-reference omits full derivations."})
            continue

        hits = [kw for kw in keywords if kw and kw in lowered]
        if len(hits) == len(keywords) and hits:
            status = "covered"
        elif hits:
            status = "partial"
        else:
            status = "missing"

        entry: dict[str, Any] = {
            "concept": cid,
            "requirement": requirement,
            "status": status,
            "matched_keywords": hits,
        }
        if status in {"missing", "partial"} and requirement == "essential":
            entry["repair_target"] = {
                "concept": cid,
                "intended_location": intended_section or "core_concepts",
                "action": "add_missing_explanation" if status == "missing" else "complete_partial_explanation",
            }
            missing_essential.append(entry)
        entries.append(entry)

    return {
        "master": master,
        "complete": not missing_essential,
        "coverage": entries,
        "missing_essential": missing_essential,
    }


# ---------------------------------------------------------------------------
# Mechanism 11 — Source-to-Claim Traceability (Section 20)
# ---------------------------------------------------------------------------

def audit_claim_traceability(
    claims: list[dict[str, Any]],
    *,
    verified_sources: dict[str, dict[str, Any]],
    source_policy: str = "adaptive",
) -> dict[str, Any]:
    """Mechanism 11: Validate claim -> evidence traceability without fake citations or strict-mode leakage."""
    findings: list[dict[str, Any]] = []
    registry_out: list[dict[str, Any]] = []

    for claim in claims:
        cid = str(claim.get("id") or "claim_unknown")
        origin = str(claim.get("origin") or "source_fact")
        evidence = list(claim.get("evidence") or [])
        statement = str(claim.get("statement") or "").strip()

        if source_policy == "strict" and origin in {"additional_research", "external"}:
            findings.append({
                "claim_id": cid,
                "severity": "critical",
                "issue": "strict_source_policy_violation",
                "detail": f"Claim '{cid}' imports external/additional research under strict source-only mode.",
            })

        if not evidence:
            if source_policy == "strict" or origin in {"source_fact", "independent_verification"}:
                findings.append({
                    "claim_id": cid,
                    "severity": "major",
                    "issue": "unsupported_claim",
                    "detail": f"Claim '{cid}' ('{statement[:60]}') has no supporting evidence locator.",
                })
                status = "unsupported"
            else:
                status = "inferred"
        else:
            valid_refs = 0
            for ev in evidence:
                sid = str(ev.get("source_id") or "")
                loc = str(ev.get("location") or "").strip()
                src = verified_sources.get(sid)
                if src is None:
                    findings.append({
                        "claim_id": cid,
                        "severity": "critical",
                        "issue": "fake_or_unknown_citation",
                        "detail": f"Claim '{cid}' cites unknown source_id '{sid}'.",
                    })
                elif not src.get("content_verified", False):
                    findings.append({
                        "claim_id": cid,
                        "severity": "major",
                        "issue": "unverified_source_content",
                        "detail": f"Claim '{cid}' cites source '{sid}' whose content was not inspected/verified.",
                    })
                elif source_policy == "strict" and src.get("role") == "external":
                    findings.append({
                        "claim_id": cid,
                        "severity": "critical",
                        "issue": "external_citation_in_strict_mode",
                        "detail": f"Claim '{cid}' cites external source '{sid}' under strict source-only mode.",
                    })
                elif not loc:
                    findings.append({
                        "claim_id": cid,
                        "severity": "moderate",
                        "issue": "missing_source_locator",
                        "detail": f"Claim '{cid}' cites '{sid}' without a section/page/timestamp locator.",
                    })
                else:
                    valid_refs += 1
            status = "supported" if valid_refs > 0 and not any(f["claim_id"] == cid for f in findings) else "unsupported"

        registry_out.append({
            "id": cid,
            "concept_id": claim.get("concept_id"),
            "statement": statement,
            "origin": origin,
            "evidence": evidence,
            "verification": {"status": status},
        })

    return {
        "valid": not findings,
        "source_policy": source_policy,
        "claims": registry_out,
        "findings": findings,
    }


# ---------------------------------------------------------------------------
# Mechanism 12 — Uncertainty & Assumption Ledger (Section 21)
# ---------------------------------------------------------------------------

CERTAINTY_LEVELS = frozenset({"verified", "supported", "inferred", "assumed", "unverified"})


class UncertaintyLedger:
    """Track explicit assumptions, inferred baselines, unverified claims, and execution limitations."""

    def __init__(self) -> None:
        self.assumptions: list[dict[str, Any]] = []
        self.verification_limitations: list[dict[str, Any]] = []

    def record_assumption(
        self,
        item_id: str,
        value: Any,
        *,
        basis: str = "inferred",
        certainty: str = "assumed",
        reader_visible: bool = False,
    ) -> dict[str, Any]:
        if certainty not in CERTAINTY_LEVELS:
            raise ValueError(f"Invalid certainty level '{certainty}'. Must be one of {sorted(CERTAINTY_LEVELS)}.")
        entry = {
            "id": item_id,
            "value": value,
            "basis": basis,
            "certainty": certainty,
            "reader_visible": reader_visible,
        }
        self.assumptions.append(entry)
        return entry

    def record_limitation(self, item: str, *, status: str = "not_executed", reason: str = "runtime_unavailable") -> dict[str, Any]:
        entry = {
            "item": item,
            "status": status,
            "reason": reason,
            "certainty": "unverified",
        }
        self.verification_limitations.append(entry)
        return entry

    def to_dict(self) -> dict[str, Any]:
        return {
            "assumptions": list(self.assumptions),
            "verification_limitations": list(self.verification_limitations),
            "reader_visible_disclosures": [a for a in self.assumptions if a["reader_visible"]],
        }


# ---------------------------------------------------------------------------
# Mechanism 14 — Multi-Artifact Consistency Engine (Section 23)
# ---------------------------------------------------------------------------

def check_multi_artifact_consistency(
    artifacts: list[dict[str, Any]],
    *,
    concept_registry: ConceptIdentityRegistry | None = None,
) -> dict[str, Any]:
    """Mechanism 14: Ensure related artifacts (e.g., deep-notes + quick-reference + flashcards) stay consistent.

    Each artifact dict accepts: {"note_text": str, "note_type": str (optional), "symbols": dict (optional),
    "conditions": list[str] (optional), "numeric_results": dict[str, float] (optional)}.
    """
    issues: list[dict[str, Any]] = []
    parsed_items = []
    for idx, art in enumerate(artifacts):
        p = parse_note(art["note_text"])
        meta = p.metadata
        parsed_items.append({
            "index": idx,
            "meta": meta,
            "body": p.body,
            "note_type": meta.get("note_type") or art.get("note_type") or "unknown",
            "symbols": art.get("symbols") or {},
            "conditions": [c.lower().strip() for c in (art.get("conditions") or [])],
            "numeric_results": art.get("numeric_results") or {},
        })

    if len(parsed_items) < 2:
        return {"consistent": True, "issues": [], "reconciliations": []}

    ref = parsed_items[0]
    ref_meta = ref["meta"]
    reconciliations: list[str] = []

    seen_note_types: set[str] = {ref["note_type"]}
    for item in parsed_items[1:]:
        meta = item["meta"]
        # 1. Shared Properties alignment (domain, master_topic, canonical topic)
        for field_name in ("domain", "master_topic", "topic"):
            if ref_meta.get(field_name) and meta.get(field_name):
                if str(ref_meta[field_name]).strip().lower() != str(meta[field_name]).strip().lower():
                    issues.append({
                        "type": "metadata_mismatch",
                        "field": field_name,
                        "detail": f"Artifact 0 has {field_name}='{ref_meta[field_name]}', artifact {item['index']} has '{meta[field_name]}'.",
                    })
        # 2. Distinct note_type across multi-artifact companion files
        if item["note_type"] in seen_note_types and item["note_type"] != "unknown":
            issues.append({
                "type": "duplicate_note_type",
                "detail": f"Companion artifact {item['index']} duplicates note_type '{item['note_type']}'.",
            })
        seen_note_types.add(item["note_type"])

        # 3. Notation equivalence check (e.g., alpha vs eta for learning_rate)
        for role, sym_a in ref["symbols"].items():
            sym_b = item["symbols"].get(role)
            if sym_b and sym_a != sym_b:
                explained = (
                    (sym_a in item["body"] and sym_b in item["body"])
                    or (sym_b in ref["body"] and sym_a in ref["body"])
                )
                if not explained:
                    issues.append({
                        "type": "unexplained_notation_divergence",
                        "role": role,
                        "detail": f"Artifact 0 uses '{sym_a}' for {role} while artifact {item['index']} uses '{sym_b}' without noting equivalence.",
                        "suggested_fix": f"State equivalence ({sym_b} = {sym_a}) or align notation across artifacts.",
                    })
                else:
                    reconciliations.append(f"Notation '{sym_a}' and '{sym_b}' for '{role}' explicitly reconciled.")

        # 4. Formula applicability conditions preserved in compressed companions
        plain_body = item["body"].replace("$", "").lower()
        for cond in ref["conditions"]:
            cond_plain = cond.replace("$", "").lower()
            if cond_plain and cond_plain not in plain_body and cond not in item["conditions"]:
                issues.append({
                    "type": "dropped_applicability_condition",
                    "detail": f"Artifact {item['index']} ({item['note_type']}) omitted condition '{cond}' present in authoritative note.",
                })

        # 5. Numerical example results agree
        for expr_key, val_a in ref["numeric_results"].items():
            if expr_key in item["numeric_results"]:
                val_b = item["numeric_results"][expr_key]
                if abs(float(val_a) - float(val_b)) > 1e-6:
                    issues.append({
                        "type": "numeric_contradiction",
                        "key": expr_key,
                        "detail": f"Artifact 0 computes {expr_key}={val_a}, artifact {item['index']} computes {val_b}.",
                    })

    return {
        "consistent": not issues,
        "issues": issues,
        "reconciliations": reconciliations,
    }


# ---------------------------------------------------------------------------
# Mechanism 17 — Semantic Change Detection & Impact Graph (Section 26)
# ---------------------------------------------------------------------------

def detect_semantic_changes(old_text: str, new_text: str) -> dict[str, Any]:
    """Mechanism 17: Classify changes between two versions of a note or source."""
    if old_text == new_text:
        return {"change_type": "none", "categories": [], "changed_sections": []}

    old_norm_ws = re.sub(r"\s+", " ", old_text).strip()
    new_norm_ws = re.sub(r"\s+", " ", new_text).strip()
    if old_norm_ws == new_norm_ws:
        return {"change_type": "cosmetic", "categories": ["cosmetic"], "changed_sections": []}

    old_p = parse_note(old_text)
    new_p = parse_note(new_text)

    categories: list[str] = []
    old_heads = [s.heading for s in old_p.sections]
    new_heads = [s.heading for s in new_p.sections]
    if old_heads != new_heads:
        categories.append("structural")

    old_code = [b["code"] for b in old_p.code_blocks]
    new_code = [b["code"] for b in new_p.code_blocks]
    if old_code != new_code:
        categories.append("implementation")

    old_math = re.findall(r"\$\$.*?\$\$|\$[^$\n]+\$", old_p.body, re.S)
    new_math = re.findall(r"\$\$.*?\$\$|\$[^$\n]+\$", new_p.body, re.S)
    old_urls = set(re.findall(r"https?://[^\s)\]]+", old_p.body))
    new_urls = set(re.findall(r"https?://[^\s)\]]+", new_p.body))

    if old_urls != new_urls:
        categories.append("evidence")

    # Detect semantic definition/formula/number shifts
    old_nums = re.findall(r"\b\d+(?:\.\d+)?\b", old_p.body)
    new_nums = re.findall(r"\b\d+(?:\.\d+)?\b", new_p.body)
    if old_math != new_math or old_nums != new_nums:
        categories.append("semantic")

    old_map = {s.slug: s.content for s in old_p.sections}
    new_map = {s.slug: s.content for s in new_p.sections}
    changed_sections = sorted(
        {slug for slug in set(old_map) | set(new_map) if old_map.get(slug) != new_map.get(slug)}
    )

    # Check if wording changed in definition/theorem/rule section
    if not categories:
        if any(re.search(r"defini|formula|theorem|rule|invariant|spec", s, re.I) for s in changed_sections):
            categories.append("semantic")
        else:
            categories.append("editorial")

    # Primary severity ordering
    for priority in ("semantic", "evidence", "implementation", "structural", "editorial", "cosmetic"):
        if priority in categories:
            primary = priority
            break
    else:
        primary = "editorial"

    return {
        "change_type": primary,
        "categories": categories,
        "changed_sections": changed_sections,
        "requires_downstream_check": primary in {"semantic", "evidence", "implementation"},
    }


def compute_change_impact(
    changed_nodes: list[str],
    dependency_graph: dict[str, list[str]],
    *,
    manually_edited: set[str] | None = None,
) -> dict[str, Any]:
    """Traverse concept/artifact dependency graph (node -> downstream dependents) without infinite loops."""
    manually_edited = manually_edited or set()
    visited: list[str] = []
    seen = set(changed_nodes)
    queue: deque[str] = deque(changed_nodes)

    while queue:
        node = queue.popleft()
        for dependent in dependency_graph.get(node, []):
            if dependent not in seen:
                seen.add(dependent)
                visited.append(dependent)
                queue.append(dependent)

    manual_conflicts = [n for n in visited if n in manually_edited]
    safe_to_update = [n for n in visited if n not in manually_edited]
    return {
        "roots": list(changed_nodes),
        "impacted": visited,
        "safe_to_update": safe_to_update,
        "manual_edit_conflicts": manual_conflicts,
    }


class KnowledgeEngine:
    """Cohesive Engine E3 facade for identity, coverage, claims, uncertainty, consistency, and semantic change."""

    def __init__(self) -> None:
        self.registry = ConceptIdentityRegistry()
        self.uncertainty = UncertaintyLedger()

    def register_concept(self, record: ConceptRecord | dict[str, Any]) -> ConceptRecord:
        return self.registry.register(record)

    def resolve_concept(self, query: str, *, domain: str | None = None, master_topic: str | None = None) -> ConceptRecord | None:
        return self.registry.resolve(query, domain=domain, master_topic=master_topic)

    def track_coverage(self, required_concepts: list[dict[str, Any]], note_text: str, *, master: str = "M1", deferrals: dict[str, str] | None = None) -> dict[str, Any]:
        return evaluate_coverage_ledger(required_concepts, note_text, master=master, deferrals=deferrals)

    def verify_claim_links(self, claims: list[dict[str, Any]], *, verified_sources: dict[str, dict[str, Any]], source_policy: str = "adaptive") -> dict[str, Any]:
        return audit_claim_traceability(claims, verified_sources=verified_sources, source_policy=source_policy)

    def check_multi_artifact(self, artifacts: list[dict[str, Any]]) -> dict[str, Any]:
        return check_multi_artifact_consistency(artifacts, concept_registry=self.registry)

    def detect_changes(self, old_text: str, new_text: str) -> dict[str, Any]:
        return detect_semantic_changes(old_text, new_text)

    def detect_impacted_concepts(self, changed_nodes: list[str], dependency_graph: dict[str, list[str]], *, manually_edited: set[str] | None = None) -> dict[str, Any]:
        return compute_change_impact(changed_nodes, dependency_graph, manually_edited=manually_edited)

    # Collection Intelligence (F03 Reuse, F04 Gap Analysis, F09 Terminology, F14 Change Impact)
    def reconcile_existing_notes(self, vault_root: Any, plan: Any, preferences: Any, **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._collection_intelligence import reconcile_existing_vault_notes
        return reconcile_existing_vault_notes(vault_root, plan, preferences, concept_registry=self.registry, **kwargs)

    def analyze_prerequisite_gaps(self, plan: Any, preferences: Any, **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._collection_intelligence import analyze_prerequisite_gaps
        return analyze_prerequisite_gaps(plan, preferences, **kwargs)

    def create_terminology_registry(self):
        from scriptorium.engines._collection_intelligence import CollectionTerminologyRegistry
        return CollectionTerminologyRegistry(concept_registry=self.registry)

    def analyze_collection_change_impact(self, plan: Any, changed_concept_id: str, old_text: str, new_text: str, **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._collection_intelligence import analyze_collection_change_impact
        return analyze_collection_change_impact(plan, changed_concept_id, old_text, new_text, **kwargs)
