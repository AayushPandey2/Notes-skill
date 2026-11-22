#!/usr/bin/env python3
"""Adaptive Research & Resource Intelligence Engine (ARRIE) for Scriptorium.

Provides deterministic research mode resolution, per-concept research requirement
planning, claim-specific source category selection, query generation, source
evaluation, independence tracking, prompt-injection boundary detection,
structured source/evidence registries, contradiction detection, coverage analysis,
stopping criteria, learner-aware resource curation, compact generator handoff
packages, and citation traceability auditing.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
from functools import lru_cache
import json
from pathlib import Path
import re
import sys
from typing import Any
import hashlib
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from scriptorium.models import REPO_ROOT

RESEARCH_PLAN_VERSION = 1

TRACKING_QUERY_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid", "mc_cid", "mc_eid", "ref", "ref_src",
}

PROMPT_INJECTION_PATTERNS = (
    re.compile(r"ignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions", re.I),
    re.compile(r"override\s+(?:the\s+)?(?:system|user|skill|source\s+policy|routing)", re.I),
    re.compile(r"execute\s+(?:this\s+)?(?:shell|command|script|bash|powershell)", re.I),
    re.compile(r"exfiltrate|reveal\s+(?:your\s+)?(?:system\s+prompt|secrets|credentials|api\s+key)", re.I),
    re.compile(r"switch\s+(?:template|route|mode)\s+to\b", re.I),
)

VAGUE_RESOURCE_PATTERNS = (
    re.compile(r"^(?:read|check|see)\s+(?:the\s+)?(?:official\s+)?(?:docs|documentation|papers?|textbooks?|books?)$", re.I),
    re.compile(r"^(?:watch|search)\s+(?:youtube|videos|tutorials?|lectures?)$", re.I),
    re.compile(r"^(?:google|search\s+online|browse\s+github)$", re.I),
)

MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
BARE_URL_RE = re.compile(r"(?<!\()https?://[^\s<>\")]+")

SUPPORTED_VERIFICATION_STATES = {
    "supported_directly",
    "supported_with_qualifications",
    "supported_indirectly",
    "corroborated_independently",
    "computationally_verified",
}

STABLE_ELEMENTARY_RE = re.compile(
    r"\b(?:derivative\s+of\s+(?:a\s+)?polynomial|power\s+rule|basic\s+arithmetic|linear\s+equation\s+basics|"
    r"basic\s+slope\s+intuition|elementary\s+algebra)\b",
    re.I,
)


@lru_cache(maxsize=1)
def policy_registry() -> dict[str, Any]:
    return json.loads(
        (REPO_ROOT / "references" / "workflows" / "research" / "research-policy-registry.json").read_text(
            encoding="utf-8"
        )
    )


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be nonempty text")
    return value.strip()


def canonicalize_url(url: str | None) -> str | None:
    """Normalize a URL deterministically by lowercasing scheme/host and stripping tracking parameters."""
    if url is None:
        return None
    if not isinstance(url, str) or not url.strip():
        return None
    raw = url.strip()
    parsed = urlsplit(raw)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        raise ValueError(f"Invalid HTTP(S) URL: {raw}")
    scheme = parsed.scheme.lower()
    host = parsed.hostname.lower()
    port = f":{parsed.port}" if parsed.port and not ((scheme == "http" and parsed.port == 80) or (scheme == "https" and parsed.port == 443)) else ""
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    if len(path) > 1 and path.endswith("/"):
        path = path[:-1]
    filtered_q = [
        (k, v)
        for k, v in parse_qsl(parsed.query, keep_blank_values=False)
        if k.lower() not in TRACKING_QUERY_PARAMS
    ]
    query = urlencode(sorted(filtered_q))
    return urlunsplit((scheme, f"{host}{port}", path, query, parsed.fragment))


def is_bare_root_url(url: str | None) -> bool:
    if not url or not isinstance(url, str):
        return False
    parsed = urlsplit(url.strip())
    return parsed.scheme.lower() in {"http", "https"} and parsed.path in ("", "/") and not parsed.query


def detect_prompt_injection(text: str) -> list[str]:
    """Identify untrusted instruction-like prompt-injection phrases inside retrieved source text."""
    if not isinstance(text, str) or not text:
        return []
    hits: list[str] = []
    for pat in PROMPT_INJECTION_PATTERNS:
        for match in pat.finditer(text):
            snippet = match.group(0).strip()
            if snippet not in hits:
                hits.append(snippet)
    return hits


def sanitize_untrusted_text(text: str) -> dict[str, Any]:
    """Treat retrieved source text strictly as data; flag and neutralize injection directives."""
    hits = detect_prompt_injection(text)
    cleaned_lines: list[str] = []
    for line in (text or "").splitlines():
        if any(pat.search(line) for pat in PROMPT_INJECTION_PATTERNS):
            cleaned_lines.append("[UNTRUSTED_DIRECTIVE_STRIPPED]")
        else:
            cleaned_lines.append(line)
    return {
        "text": "\n".join(cleaned_lines),
        "injection_detected": bool(hits),
        "flagged_patterns": hits,
    }


def resolve_research_mode(
    request: str = "",
    *,
    source_policy: str | None = None,
    has_supplied_sources: bool = False,
    explicit_mode: str | None = None,
) -> dict[str, Any]:
    """Resolve the active ARRIE research mode (`R-S0` through `R-R`) with strict precedence."""
    modes = policy_registry()["modes"]
    mode_aliases = {spec["name"]: code for code, spec in modes.items()}
    req_low = (request or "").lower()

    if explicit_mode:
        code = explicit_mode if explicit_mode in modes else mode_aliases.get(explicit_mode.strip().lower())
        if not code:
            raise ValueError(f"Unknown research mode: {explicit_mode}")
        return {"mode": code, **modes[code]}

    # Strict source-only explicit user request takes top precedence over everything
    if re.search(r"\b(?:only\s+from\s+(?:this|the)\s+(?:source|textbook|pdf|document|notes)|strict(?:ly)?\s+source[- ]only|no\s+external\s+(?:research|browsing|sources))\b", req_low):
        return {"mode": "R-S0", **modes["R-S0"]}

    if source_policy == "strict":
        if re.search(r"\bverify|fact[- ]?check|check\s+against\b", req_low):
            return {"mode": "R-S1", **modes["R-S1"]}
        return {"mode": "R-S0", **modes["R-S0"]}

    if source_policy == "expanded":
        return {"mode": "R-S2", **modes["R-S2"]}

    if re.search(r"\b(?:literature\s+review|systematic\s+review|state\s+of\s+the\s+art\s+survey)\b", req_low):
        return {"mode": "R-L", **modes["R-L"]}

    if re.search(r"\b(?:recommend|best|free)\b.*\b(?:resources?|textbooks?|courses?|tutorials?|reading\s+list)\b", req_low):
        return {"mode": "R-R", **modes["R-R"]}

    if source_policy == "comparative" or re.search(r"\b(?:compare|versus|vs\.?|trade[- ]?offs?)\b", req_low):
        return {"mode": "R-C", **modes["R-C"]}

    if has_supplied_sources:
        return {"mode": "R-S2", **modes["R-S2"]}

    return {"mode": "R-I", **modes["R-I"]}


def _infer_concept_evidence_needs(
    concept: dict[str, Any],
    *,
    topic: str,
    request: str,
    mode_code: str,
    source_policy: str,
    sources_by_concept: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Derive concept-specific research questions and independent R0-R5 depth from objectives and types."""
    reg = policy_registry()
    cid = concept["id"]
    title = concept["title"]
    types = set(concept.get("types") or [])
    objectives = set(concept.get("objectives") or [])
    depth = concept.get("depth") or {}
    context = f"{topic} {title} {request}"
    supplied = sources_by_concept.get(cid, [])

    # Strict source-only mode (R-S0): never schedule external browsing
    if mode_code == "R-S0":
        return [
            {
                "concept_id": cid,
                "question": f"Verify exact definitions, assumptions, and claims for '{title}' within the supplied source.",
                "evidence_type": "no_external_research",
                "research_depth": 0,
                "preferred_source_types": ["local_user_source"],
                "freshness_required": False,
                "priority": "high" if supplied else "medium",
                "completion_criteria": "All required elements in supplied source inventory are inspected and faithfully attributed.",
            }
        ]

    # Stable elementary math / no-research-needed check -> R0
    if (
        STABLE_ELEMENTARY_RE.search(context)
        and mode_code not in {"R-L", "R-C", "R-R"}
        and "prove" not in objectives
        and "programming" not in types
        and not re.search(r"\b(?:version|api|recent|latest|202\d|benchmark|paper|theorem)\b", context, re.I)
    ):
        return [
            {
                "concept_id": cid,
                "question": f"Confirm internal mathematical consistency for '{title}' without unnecessary external retrieval.",
                "evidence_type": "no_external_research",
                "research_depth": 0,
                "preferred_source_types": ["local_user_source"],
                "freshness_required": False,
                "priority": "low",
                "completion_criteria": "Verified via self-contained mathematical reasoning or local check.",
            }
        ]

    needs: list[dict[str, Any]] = []

    def add_need(
        evidence_type: str,
        question: str,
        *,
        r_depth: int | None = None,
        priority: str = "high",
        freshness: bool = False,
        criteria: str = "",
    ) -> None:
        spec = reg["evidence_types"][evidence_type]
        eff_depth = spec["default_depth"] if r_depth is None else max(0, min(5, r_depth))
        if mode_code == "R-L":
            eff_depth = max(eff_depth, 5)
        elif mode_code == "R-C" and evidence_type in {"empirical_result", "software_architecture", "conceptual_expansion"}:
            eff_depth = max(eff_depth, 4)
        needs.append({
            "concept_id": cid,
            "question": question,
            "evidence_type": evidence_type,
            "research_depth": eff_depth,
            "preferred_source_types": list(spec["source_preferences"]),
            "freshness_required": freshness or spec["freshness_days"] <= 180,
            "priority": priority,
            "completion_criteria": criteria or f"Verify {', '.join(spec['evidence_requirements'])} from authoritative source(s).",
        })

    if mode_code == "R-R":
        add_need(
            "learning_resource",
            f"Identify verified, level-appropriate learning resources for '{title}' ({topic}).",
            r_depth=2,
            priority="high",
            criteria="Verified accessible resources matched to learner level, prerequisites, and cost constraint.",
        )
        return needs

    if mode_code == "R-L":
        add_need(
            "literature_synthesis",
            f"Synthesize primary literature, competing findings, and open questions for '{title}' ({topic}).",
            r_depth=5,
            priority="high",
        )
        return needs

    # Mathematical proof / theorem verification
    if "prove" in objectives or depth.get("math", 0) >= 5 or re.search(r"\b(?:theorem|convergence|lemma|proof)\b", context, re.I):
        add_need(
            "mathematical_proof",
            f"Verify exact theorem statement, hypotheses, assumptions, and proof conditions for '{title}'.",
            r_depth=3 if "prove" in objectives else 2,
            priority="high",
        )
    elif "derive" in objectives or "calculate" in objectives or "mathematical" in types or depth.get("math", 0) >= 2:
        add_need(
            "mathematical_definition",
            f"Verify formal mathematical definition, notation, and domain conditions for '{title}'.",
            r_depth=2,
            priority="high",
        )

    # Programming API & version-sensitive implementation evidence
    if "programming" in types or bool(objectives & {"implement", "debug"}) or depth.get("code", 0) >= 2:
        impl = concept.get("implementation") or {}
        tool = impl.get("framework") or impl.get("language") or "target runtime"
        is_versioned = bool(re.search(r"\b(?:numpy|pytorch|torch|tensorflow|keras|scikit-learn|pandas|api|version|deprecat|v\d)\b", context, re.I))
        add_need(
            "programming_api",
            f"Verify current official API signatures, version constraints, and behavior in {tool} for '{title}'.",
            r_depth=2 if not is_versioned else 3,
            priority="high",
            freshness=True,
        )

    # Architectural / original formulation evidence
    if "architectural" in types:
        add_need(
            "software_architecture" if not re.search(r"\b(?:transformer|attention|resnet|cnn|rnn|mlp|neural)\b", context, re.I) else "empirical_result",
            f"Verify original architecture specification, component interfaces, and tensor/data-flow contracts for '{title}'.",
            r_depth=2,
            priority="high",
        )

    # Historical claims & chronology
    if "historical" in types:
        add_need(
            "historical_claim",
            f"Verify chronology, primary publications/records, and scholarly attributions for '{title}'.",
            r_depth=2,
            priority="high",
        )

    # Scientific / empirical / research claims
    if "scientific" in types:
        add_need(
            "scientific_measurement",
            f"Verify experimental conditions, units, error bounds, and applicability regime for '{title}'.",
            r_depth=2,
            priority="high",
        )
    if "research" in types or "comparative" in types or mode_code == "R-C":
        add_need(
            "empirical_result",
            f"Verify methodology, datasets, metrics, and competing findings for '{title}'.",
            r_depth=4 if mode_code == "R-C" else 3,
            priority="high",
        )

    # Fallback conceptual / factual need if nothing specific triggered
    if not needs:
        if source_policy == "expanded" and supplied:
            add_need(
                "conceptual_expansion",
                f"Check whether supplemental intuition or prerequisite clarification is needed for '{title}' without altering source claims.",
                r_depth=1,
                priority="medium",
            )
        else:
            add_need(
                "factual_verification" if depth.get("theory", 0) <= 2 else "conceptual_expansion",
                f"Verify core definition, distinctions, and boundary conditions for '{title}'.",
                r_depth=1 if depth.get("theory", 0) <= 2 else 2,
                priority="medium",
            )

    return needs


def generate_search_queries(question_record: dict[str, Any], *, topic: str = "", max_queries: int = 3) -> list[dict[str, str]]:
    """Construct targeted, claim-specific search queries for one research question (never static site lists)."""
    r_depth = int(question_record.get("research_depth", 0))
    if r_depth == 0:
        return []

    etype = question_record.get("evidence_type", "factual_verification")
    q_text = question_record.get("question", "")
    concept = question_record.get("concept_title") or question_record.get("concept_id", "")
    anchor = f"{topic} {concept}".strip() if topic and topic.lower() not in concept.lower() else (concept or topic or q_text)

    queries: list[dict[str, str]] = []

    def add_q(qtype: str, query: str) -> None:
        cleaned = re.sub(r"\s+", " ", query).strip()
        if cleaned and all(existing["query"].lower() != cleaned.lower() for existing in queries):
            queries.append({"query_type": qtype, "query": cleaned})

    if etype == "mathematical_proof":
        add_q("primary_source", f"{anchor} original paper theorem proof")
        add_q("mathematical", f"{anchor} assumptions hypotheses proof conditions textbook")
        add_q("verification", f"{anchor} counterexample failure conditions")
    elif etype == "mathematical_definition":
        add_q("definition", f"{anchor} formal mathematical definition notation")
        add_q("mathematical", f"{anchor} derivation domain conditions")
    elif etype == "programming_api":
        add_q("implementation", f"{anchor} official documentation API reference")
        add_q("freshness", f"{anchor} release notes deprecation migration guide")
    elif etype == "empirical_result":
        add_q("primary_source", f"{anchor} original paper benchmark dataset methodology")
        add_q("comparison", f"{anchor} empirical comparison ablation limitations")
    elif etype == "historical_claim":
        add_q("primary_source", f"{anchor} original publication archive primary source chronology")
        add_q("verification", f"{anchor} scholarly history attribution")
    elif etype == "scientific_measurement":
        add_q("primary_source", f"{anchor} experimental measurement units uncertainty conditions")
        add_q("mathematical", f"{anchor} physical law validity regime assumptions")
    elif etype == "clinical_health":
        add_q("primary_source", f"{anchor} clinical guideline systematic review peer reviewed")
        add_q("freshness", f"{anchor} current safety contraindications update")
    elif etype == "economic_data":
        add_q("primary_source", f"{anchor} official statistical agency data definition methodology")
        add_q("freshness", f"{anchor} latest revision date units")
    elif etype == "legal_regulation":
        add_q("primary_source", f"{anchor} official statute regulation effective date jurisdiction")
    elif etype == "security_advisory":
        add_q("primary_source", f"{anchor} official security advisory affected versions remediation")
        add_q("freshness", f"{anchor} latest vulnerability update")
    elif etype == "software_architecture":
        add_q("primary_source", f"{anchor} official design specification architecture documentation")
        add_q("comparison", f"{anchor} architecture tradeoffs bottlenecks")
    elif etype == "literature_synthesis":
        add_q("discovery", f"{anchor} systematic survey review primary papers")
        add_q("comparison", f"{anchor} conflicting findings methodological differences")
        add_q("verification", f"{anchor} open questions limitations")
    elif etype == "learning_resource":
        add_q("resource_discovery", f"{anchor} university course open textbook lecture notes official tutorial")
        add_q("resource_discovery", f"{anchor} interactive visualization practice exercises")
    else:
        add_q("discovery", f"{anchor} authoritative definition mechanism")
        add_q("verification", f"{anchor} limitations boundary conditions")

    return queries[:max(1, max_queries)]


def normalize_research_plan(raw_plan: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize a structured ARRIE research plan."""
    if not isinstance(raw_plan, dict):
        raise ValueError("research_plan must be an object")
    reg = policy_registry()
    plan = deepcopy(raw_plan)
    topic = _text(plan.get("topic"), "research_plan topic")
    mode_info = resolve_research_mode(explicit_mode=plan.get("mode") or "R-I")
    mode_code = mode_info["mode"]
    plan["mode"] = mode_code
    plan["mode_name"] = mode_info["name"]
    plan["source_policy"] = mode_info["source_policy"]
    plan["allow_external_browsing"] = mode_info["allow_external_browsing"]
    plan["research_plan_version"] = RESEARCH_PLAN_VERSION
    plan["overall_objective"] = _text(plan.get("overall_objective") or f"Evidence-grounded understanding of {topic}", "overall_objective")

    raw_questions = plan.get("research_questions")
    if not isinstance(raw_questions, list):
        raise ValueError("research_questions must be a list")

    seen_ids: set[str] = set()
    normalized_questions: list[dict[str, Any]] = []
    for idx, q in enumerate(raw_questions, 1):
        if not isinstance(q, dict):
            raise ValueError("Each research question must be an object")
        qid = _text(q.get("id") or f"RQ-{idx:03d}", "research question id")
        if qid in seen_ids:
            raise ValueError(f"Duplicate research question ID: {qid}")
        seen_ids.add(qid)
        concept_id = _text(q.get("concept_id"), f"{qid} concept_id")
        question_text = _text(q.get("question"), f"{qid} question")
        etype = q.get("evidence_type") or "factual_verification"
        if etype not in reg["evidence_types"]:
            raise ValueError(f"{qid}: unknown evidence_type '{etype}'")
        r_depth = q.get("research_depth", reg["evidence_types"][etype]["default_depth"])
        if type(r_depth) is not int or r_depth not in range(6):
            raise ValueError(f"{qid}: research_depth must be an integer 0 through 5")
        if not mode_info["allow_external_browsing"] and r_depth > 0:
            raise ValueError(f"{qid}: mode {mode_code} ({mode_info['name']}) forbids external retrieval (research_depth must be 0)")
        pref_types = q.get("preferred_source_types") or list(reg["evidence_types"][etype]["source_preferences"])
        if not isinstance(pref_types, list) or not pref_types:
            raise ValueError(f"{qid}: preferred_source_types must be a nonempty list")
        priority = q.get("priority") or "medium"
        if priority not in {"high", "medium", "low"}:
            raise ValueError(f"{qid}: priority must be high, medium, or low")
        status = q.get("status") or "pending"
        if status not in {"pending", "in_progress", "answered", "partially_answered", "unresolved", "skipped_r0"}:
            raise ValueError(f"{qid}: invalid status '{status}'")
        if r_depth == 0 and status == "pending":
            status = "skipped_r0"

        entry = {
            "id": qid,
            "concept_id": concept_id,
            "concept_title": q.get("concept_title") or concept_id,
            "question": question_text,
            "evidence_type": etype,
            "research_depth": r_depth,
            "research_depth_code": f"R{r_depth}",
            "preferred_source_types": list(dict.fromkeys(pref_types)),
            "freshness_required": bool(q.get("freshness_required", reg["evidence_types"][etype]["freshness_days"] <= 180)),
            "priority": priority,
            "status": status,
            "completion_criteria": _text(
                q.get("completion_criteria") or f"Verify {', '.join(reg['evidence_types'][etype]['evidence_requirements'])}.",
                f"{qid} completion_criteria",
            ),
        }
        entry["queries"] = q.get("queries") if isinstance(q.get("queries"), list) else generate_search_queries(entry, topic=topic)
        normalized_questions.append(entry)

    plan["research_questions"] = normalized_questions
    plan["soft_query_budget"] = sum(
        reg["research_depths"][str(q["research_depth"])]["soft_query_budget"] for q in normalized_questions
    )
    return plan


def plan_research(
    topic: str,
    instructional_plan: dict[str, Any],
    *,
    request: str = "",
    explicit_mode: str | None = None,
    explicit_questions: list[dict[str, Any]] | None = None,
    offline: bool = False,
) -> dict[str, Any]:
    """Build a concept-specific ARRIE research plan from an existing adaptive instructional plan."""
    if not isinstance(instructional_plan, dict) or not instructional_plan.get("concepts"):
        raise ValueError("plan_research requires an instructional_plan with nonempty concepts.")

    source_policy = instructional_plan.get("source_policy", "independent")
    sources = instructional_plan.get("sources") or []
    mode_info = resolve_research_mode(
        request,
        source_policy=source_policy,
        has_supplied_sources=bool(sources),
        explicit_mode=explicit_mode,
    )
    mode_code = mode_info["mode"]

    sources_by_concept: dict[str, list[dict[str, Any]]] = {}
    for src in sources:
        if isinstance(src, dict):
            for cid in src.get("concepts") or []:
                sources_by_concept.setdefault(cid, []).append(src)

    if explicit_questions is not None:
        raw_questions = deepcopy(explicit_questions)
    else:
        raw_questions = []
        q_counter = 1
        for concept in instructional_plan["concepts"]:
            inferred = _infer_concept_evidence_needs(
                concept,
                topic=topic,
                request=request,
                mode_code=mode_code,
                source_policy=source_policy,
                sources_by_concept=sources_by_concept,
            )
            for item in inferred:
                item["id"] = f"RQ-{q_counter:03d}"
                item["concept_title"] = concept["title"]
                if offline and item["research_depth"] > 0:
                    item["offline_restricted"] = True
                raw_questions.append(item)
                q_counter += 1

    plan = normalize_research_plan({
        "topic": topic,
        "mode": mode_code,
        "overall_objective": f"Evidence-grounded support for {topic} ({instructional_plan.get('audience', 'beginner')} audience)",
        "offline": bool(offline),
        "research_questions": raw_questions,
    })
    plan["offline"] = bool(offline)
    plan["active_adapters"] = [
        name
        for name, spec in policy_registry()["provider_adapters"].items()
        if (not offline or spec["offline_capable"]) and (mode_info["allow_external_browsing"] or spec["offline_capable"])
    ]
    return plan


def evaluate_source(
    source: dict[str, Any],
    evidence_type: str,
    *,
    required_version: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Evaluate a candidate source relative to a specific evidence type (never universal site rankings)."""
    reg = policy_registry()
    if evidence_type not in reg["evidence_types"]:
        raise ValueError(f"Unknown evidence_type: {evidence_type}")
    spec = reg["evidence_types"][evidence_type]
    prefs = spec["source_preferences"]
    stype = source.get("source_type") or "general_web"
    role = reg["source_roles"].get(stype, "tertiary")

    reasons: list[str] = []
    warnings: list[str] = []
    fatal: list[str] = []

    url = source.get("canonical_url")
    if url and is_bare_root_url(url):
        fatal.append("bare root-domain URL is not a verifiable evidence locator")

    if not source.get("content_verified", False):
        fatal.append("source content was not inspected (search snippet or metadata only)")

    if source.get("access_status") in {"unavailable", "paywalled_uninspected"}:
        fatal.append(f"source access_status is {source.get('access_status')}")

    if source.get("is_preprint") or stype == "preprint":
        warnings.append("preprint: not automatically peer-reviewed; disclose publication status")

    if evidence_type == "programming_api" and required_version:
        src_ver = source.get("version")
        if not src_ver:
            warnings.append(f"missing API version metadata (required {required_version})")
        elif str(src_ver).strip().lower() != str(required_version).strip().lower():
            fatal.append(f"outdated/mismatched version ({src_ver} != {required_version})")

    if evidence_type == "empirical_result" and not source.get("has_methodology", True):
        fatal.append("empirical claim lacks stated dataset/methodology")

    # Authority score heuristic relative to claim type
    if stype in prefs:
        rank_idx = prefs.index(stype)
        authority_score = max(0.55, 1.0 - 0.1 * rank_idx)
        reasons.append(f"{stype} matches preferred authority rank #{rank_idx + 1} for {evidence_type}")
    elif role == "primary":
        authority_score = 0.7
        reasons.append(f"primary source ({stype}) outside default preference list")
    elif role == "secondary":
        authority_score = 0.5
        reasons.append(f"secondary source ({stype}) useful for context")
    else:
        authority_score = 0.25
        warnings.append(f"tertiary source ({stype}) is weak primary authority for {evidence_type}")

    if spec.get("primary_required") and role == "tertiary":
        fatal.append(f"tertiary source ({stype}) cannot alone establish primary-required claim ({evidence_type})")

    # Freshness check when publication/update date exists
    date_str = source.get("last_updated") or source.get("publication_date")
    if date_str and isinstance(date_str, str):
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            now_dt = now or datetime.now(timezone.utc)
            if now_dt.tzinfo is None:
                now_dt = now_dt.replace(tzinfo=timezone.utc)
            age_days = (now_dt - dt).total_seconds() / 86400.0
            if age_days > spec["freshness_days"]:
                warnings.append(f"source age ({int(age_days)}d) exceeds freshness window ({spec['freshness_days']}d) for {evidence_type}")
        except ValueError:
            warnings.append("unparseable publication/update date")

    accepted = not fatal
    return {
        "source_id": source.get("source_id"),
        "evidence_type": evidence_type,
        "source_role": role,
        "accepted": accepted,
        "authority_score": round(authority_score, 2) if accepted else 0.0,
        "reasons": reasons,
        "warnings": warnings,
        "rejection_reasons": fatal,
    }


def check_source_independence(sources: list[dict[str, Any]]) -> dict[str, Any]:
    """Group sources by underlying origin so derivative summaries of one paper never count as independent corroboration."""
    clusters: dict[str, list[str]] = {}
    derivative_map: dict[str, str] = {}

    for src in sources:
        sid = src["source_id"]
        origin = (
            src.get("origin_source_id")
            or src.get("cites_origin")
            or src.get("identifiers", {}).get("doi")
            or src.get("canonical_url")
            or sid
        )
        origin_key = str(origin).strip().lower()
        clusters.setdefault(origin_key, []).append(sid)
        if src.get("origin_source_id") or src.get("cites_origin"):
            derivative_map[sid] = str(src.get("origin_source_id") or src.get("cites_origin"))

    independent_count = len(clusters)
    return {
        "total_sources": len(sources),
        "independent_origin_count": independent_count,
        "origin_clusters": clusters,
        "derivative_sources": derivative_map,
        "has_independent_corroboration": independent_count >= 2,
    }


def normalize_evidence_registry(
    raw_registry: dict[str, Any],
    *,
    research_plan: dict[str, Any] | None = None,
    mode: str | None = None,
) -> dict[str, Any]:
    """Validate and normalize Source Records (`SRC-*`) and Evidence Records (`EV-*`) with strict provenance rules."""
    if not isinstance(raw_registry, dict):
        raise ValueError("evidence_registry must be an object")
    reg = policy_registry()
    valid_states = set(reg["verification_states"])
    valid_source_types = set(reg["source_roles"])
    mode_code = mode or (research_plan or {}).get("mode") or "R-I"
    mode_spec = reg["modes"][mode_code]

    sources_in = raw_registry.get("sources") or []
    evidence_in = raw_registry.get("evidence") or []
    if not isinstance(sources_in, list) or not isinstance(evidence_in, list):
        raise ValueError("evidence_registry requires 'sources' and 'evidence' lists")

    rq_ids = {q["id"] for q in (research_plan or {}).get("research_questions", [])}

    sources_by_id: dict[str, dict[str, Any]] = {}
    url_to_id: dict[str, str] = {}
    normalized_sources: list[dict[str, Any]] = []
    injection_warnings: list[dict[str, Any]] = []

    for src in sources_in:
        if not isinstance(src, dict):
            raise ValueError("Each source record must be an object")
        sid = _text(src.get("source_id"), "source_id")
        if sid in sources_by_id:
            raise ValueError(f"Duplicate source_id: {sid}")
        title = _text(src.get("title"), f"{sid} title")
        stype = src.get("source_type") or "general_web"
        if stype not in valid_source_types:
            raise ValueError(f"{sid}: unknown source_type '{stype}'")
        if not mode_spec["allow_external_browsing"] and stype != "local_user_source":
            raise ValueError(f"{sid}: mode {mode_code} ({mode_spec['name']}) forbids external source_type '{stype}'")

        raw_url = src.get("canonical_url")
        canon_url = canonicalize_url(raw_url) if raw_url else None
        if canon_url and is_bare_root_url(canon_url):
            raise ValueError(f"{sid}: bare root-domain URL '{canon_url}' is forbidden as a source citation")
        if canon_url and canon_url in url_to_id:
            raise ValueError(f"{sid}: duplicate canonical_url already registered under {url_to_id[canon_url]}")
        if canon_url:
            url_to_id[canon_url] = sid

        excerpt = src.get("excerpt") or ""
        sanitized = sanitize_untrusted_text(excerpt)
        if sanitized["injection_detected"]:
            injection_warnings.append({
                "source_id": sid,
                "flagged_patterns": sanitized["flagged_patterns"],
            })

        access_status = src.get("access_status") or "not_checked"
        if access_status not in {"full", "partial", "metadata_only", "unavailable", "not_checked", "paywalled_uninspected"}:
            raise ValueError(f"{sid}: invalid access_status '{access_status}'")
        content_verified = bool(src.get("content_verified", False))
        if content_verified and access_status in {"unavailable", "not_checked", "metadata_only", "paywalled_uninspected"}:
            raise ValueError(f"{sid}: content_verified cannot be True when access_status is '{access_status}'")

        entry = {
            "source_id": sid,
            "title": title,
            "source_type": stype,
            "source_role": reg["source_roles"][stype],
            "publisher": src.get("publisher"),
            "canonical_url": canon_url,
            "publication_date": src.get("publication_date"),
            "last_updated": src.get("last_updated"),
            "accessed_at": src.get("accessed_at"),
            "version": src.get("version"),
            "identifiers": deepcopy(src.get("identifiers") or {}),
            "access_status": access_status,
            "content_verified": content_verified,
            "is_preprint": bool(src.get("is_preprint", stype == "preprint")),
            "has_methodology": bool(src.get("has_methodology", True)),
            "origin_source_id": src.get("origin_source_id"),
            "cites_origin": src.get("cites_origin"),
            "research_questions": list(dict.fromkeys(src.get("research_questions") or [])),
            "excerpt": sanitized["text"],
            "injection_detected": sanitized["injection_detected"],
            "private": bool(src.get("private", stype == "local_user_source")),
        }
        sources_by_id[sid] = entry
        normalized_sources.append(entry)

    seen_ev: set[str] = set()
    normalized_evidence: list[dict[str, Any]] = []
    for ev in evidence_in:
        if not isinstance(ev, dict):
            raise ValueError("Each evidence record must be an object")
        eid = _text(ev.get("evidence_id"), "evidence_id")
        if eid in seen_ev:
            raise ValueError(f"Duplicate evidence_id: {eid}")
        seen_ev.add(eid)
        rq_id = _text(ev.get("research_question_id"), f"{eid} research_question_id")
        if rq_ids and rq_id not in rq_ids:
            raise ValueError(f"{eid}: unknown research_question_id '{rq_id}'")
        concept_id = _text(ev.get("concept_id"), f"{eid} concept_id")
        claim = _text(ev.get("claim"), f"{eid} claim")
        status = ev.get("support_status") or "not_verified"
        if status not in valid_states:
            raise ValueError(f"{eid}: invalid support_status '{status}'")

        sids = list(dict.fromkeys(ev.get("source_ids") or []))
        for sid in sids:
            if sid not in sources_by_id:
                raise ValueError(f"{eid}: references unknown source_id '{sid}'")

        locations = list(ev.get("source_locations") or [])

        # Strict provenance enforcement: never claim verified support without inspected content
        if status in {"supported_directly", "supported_with_qualifications", "supported_indirectly", "corroborated_independently"}:
            if not sids:
                raise ValueError(f"{eid}: status '{status}' requires at least one verified source_id")
            inspected = [sources_by_id[s] for s in sids if sources_by_id[s]["content_verified"]]
            if not inspected:
                raise ValueError(f"{eid}: cannot mark '{status}' when no linked source has content_verified=True")
            if status == "corroborated_independently":
                indep = check_source_independence(inspected)
                if not indep["has_independent_corroboration"]:
                    raise ValueError(
                        f"{eid}: 'corroborated_independently' requires at least 2 independent origin sources "
                        f"(found {indep['independent_origin_count']} independent origin cluster)"
                    )

        normalized_evidence.append({
            "evidence_id": eid,
            "research_question_id": rq_id,
            "concept_id": concept_id,
            "claim": claim,
            "source_ids": sids,
            "source_locations": locations,
            "support_status": status,
            "evidence_origin": ev.get("evidence_origin") or (
                "supplied_source" if sids and all(sources_by_id[s]["source_type"] == "local_user_source" for s in sids)
                else "computational_check" if status == "computationally_verified"
                else "external_research" if sids
                else "unverified"
            ),
            "qualifications": list(ev.get("qualifications") or []),
            "assumptions": list(ev.get("assumptions") or []),
            "contradictions": list(ev.get("contradictions") or []),
            "remaining_questions": list(ev.get("remaining_questions") or []),
            "methodology": ev.get("methodology"),
            "dataset_or_sample": ev.get("dataset_or_sample"),
            "version": ev.get("version"),
        })

    independence = check_source_independence(normalized_sources)
    return {
        "mode": mode_code,
        "sources": normalized_sources,
        "evidence": normalized_evidence,
        "independence": independence,
        "injection_warnings": injection_warnings,
    }


def detect_contradictions(evidence_registry: dict[str, Any]) -> list[dict[str, Any]]:
    """Detect explicit or structural contradictions across evidence records without silently merging them."""
    evidence = evidence_registry.get("evidence") or []
    sources_by_id = {s["source_id"]: s for s in (evidence_registry.get("sources") or [])}
    findings: list[dict[str, Any]] = []

    by_rq: dict[str, list[dict[str, Any]]] = {}
    for ev in evidence:
        by_rq.setdefault(ev["research_question_id"], []).append(ev)
        if ev["support_status"] == "contradicted" or ev.get("contradictions"):
            findings.append({
                "research_question_id": ev["research_question_id"],
                "concept_id": ev["concept_id"],
                "evidence_ids": [ev["evidence_id"]],
                "claim": ev["claim"],
                "contradiction_notes": list(ev.get("contradictions") or ["Marked contradicted"]),
                "resolution_required": "Compare wording, definitions, assumptions, dataset/methodology, and versions; preserve disagreement without inventing consensus.",
            })

    # Detect incompatible dataset/methodology or conflicting claims under the same research question
    for rq_id, items in by_rq.items():
        if len(items) < 2:
            continue
        supplied = [e for e in items if e.get("evidence_origin") == "supplied_source"]
        external = [e for e in items if e.get("evidence_origin") == "external_research"]
        if supplied and external and any(e["support_status"] == "contradicted" or e.get("contradictions") for e in items):
            findings.append({
                "research_question_id": rq_id,
                "concept_id": items[0]["concept_id"],
                "evidence_ids": [e["evidence_id"] for e in items],
                "claim": "Supplied source vs. external verification discrepancy",
                "contradiction_notes": [
                    "Preserve supplied source statement faithfully and label external discrepancy separately."
                ],
                "source_types": [
                    sources_by_id[s]["source_type"]
                    for e in items for s in e["source_ids"] if s in sources_by_id
                ],
                "resolution_required": "Preserve supplied source fidelity; report external discrepancy separately.",
            })

    return findings


def analyze_research_coverage(
    research_plan: dict[str, Any],
    evidence_registry: dict[str, Any],
    *,
    source_inventory: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Evaluate per-concept and per-question research coverage and pinpoint unresolved gaps."""
    questions = research_plan.get("research_questions") or []
    evidence = evidence_registry.get("evidence") or []
    ev_by_rq: dict[str, list[dict[str, Any]]] = {}
    for ev in evidence:
        ev_by_rq.setdefault(ev["research_question_id"], []).append(ev)

    question_status: dict[str, dict[str, Any]] = {}
    concept_buckets: dict[str, list[str]] = {}
    gaps: list[dict[str, Any]] = []

    for q in questions:
        qid = q["id"]
        cid = q["concept_id"]
        r_depth = q["research_depth"]
        evs = ev_by_rq.get(qid, [])

        if r_depth == 0:
            state = "not_applicable" if not evs else "complete"
        elif not evs:
            state = "missing"
            gaps.append({
                "research_question_id": qid,
                "concept_id": cid,
                "priority": q["priority"],
                "reason": "No evidence records collected for required research question.",
            })
        else:
            statuses = {e["support_status"] for e in evs}
            if statuses & {"contradicted"}:
                state = "partial"
                gaps.append({
                    "research_question_id": qid,
                    "concept_id": cid,
                    "priority": q["priority"],
                    "reason": "Contradictory evidence requires qualification and methodology comparison.",
                })
            elif statuses <= {"supported_directly", "corroborated_independently", "computationally_verified"}:
                state = "complete"
            elif statuses <= SUPPORTED_VERIFICATION_STATES:
                state = "sufficient_with_qualifications"
            elif statuses & SUPPORTED_VERIFICATION_STATES:
                state = "partial"
                gaps.append({
                    "research_question_id": qid,
                    "concept_id": cid,
                    "priority": q["priority"],
                    "reason": "Some claims remain unresolved or source_unavailable.",
                })
            else:
                state = "missing"
                gaps.append({
                    "research_question_id": qid,
                    "concept_id": cid,
                    "priority": q["priority"],
                    "reason": f"Claims have unverified status: {sorted(statuses)}.",
                })

        question_status[qid] = {"concept_id": cid, "priority": q["priority"], "coverage": state, "evidence_count": len(evs)}
        concept_buckets.setdefault(cid, []).append(state)

    concept_coverage: dict[str, str] = {}
    for cid, states in concept_buckets.items():
        if all(s == "not_applicable" for s in states):
            concept_coverage[cid] = "not_applicable"
        elif "missing" in states:
            concept_coverage[cid] = "missing" if all(s in {"missing", "not_applicable"} for s in states) else "partial"
        elif "partial" in states:
            concept_coverage[cid] = "partial"
        elif "sufficient_with_qualifications" in states:
            concept_coverage[cid] = "sufficient_with_qualifications"
        else:
            concept_coverage[cid] = "complete"

    # Check source-inventory obligations if provided
    uncovered_inventory: list[str] = []
    if source_inventory:
        referenced_locs = " ".join(
            loc.lower() for ev in evidence for loc in (ev.get("source_locations") or [])
        )
        for elem in source_inventory:
            if elem.get("required") and elem.get("access") != "full":
                uncovered_inventory.append(elem["id"])
            elif elem.get("required") and elem["id"].lower() not in referenced_locs and not evidence:
                uncovered_inventory.append(elem["id"])

    return {
        "concept_coverage": concept_coverage,
        "question_coverage": question_status,
        "gaps": gaps,
        "uncovered_inventory_ids": uncovered_inventory,
        "contradictions": detect_contradictions(evidence_registry),
        "all_high_priority_covered": not any(g["priority"] == "high" for g in gaps) and not uncovered_inventory,
    }


def should_stop_research(
    research_plan: dict[str, Any],
    evidence_registry: dict[str, Any],
    *,
    queries_used: int = 0,
    offline: bool = False,
    budget_exhausted: bool = False,
    marginal_gain_low: bool = False,
) -> dict[str, Any]:
    """Evidence-sufficiency stopping decision (never based purely on a source-count quota)."""
    coverage = analyze_research_coverage(research_plan, evidence_registry)
    mode_code = research_plan.get("mode", "R-I")

    if mode_code == "R-S0":
        return {"stop": True, "reason": "Strict source-only mode (R-S0) prohibits external retrieval.", "coverage": coverage}

    if offline:
        return {
            "stop": True,
            "reason": "Offline environment: stopping external retrieval and disclosing remaining gaps.",
            "coverage": coverage,
        }

    high_gaps = [g for g in coverage["gaps"] if g["priority"] == "high"]
    if not high_gaps and not coverage["uncovered_inventory_ids"]:
        if not coverage["gaps"] or marginal_gain_low:
            return {
                "stop": True,
                "reason": "All high-priority research questions and source obligations are sufficiently covered.",
                "coverage": coverage,
            }

    soft_budget = research_plan.get("soft_query_budget", 0)
    if budget_exhausted or (soft_budget > 0 and queries_used >= soft_budget and marginal_gain_low):
        return {
            "stop": True,
            "reason": "Soft research budget reached with low marginal information gain; report remaining gaps honestly.",
            "coverage": coverage,
        }

    return {
        "stop": False,
        "reason": f"{len(high_gaps)} high-priority question(s) and {len(coverage['gaps'])} total gap(s) remain unresolved.",
        "coverage": coverage,
    }


def curate_learning_resources(
    candidates: list[dict[str, Any]],
    *,
    audience: str = "beginner",
    objectives: list[str] | None = None,
    free_only: bool = False,
    extensive: bool = False,
    max_items: int = 5,
) -> dict[str, Any]:
    """Curate level-aware, accessibility-verified, progression-ordered further-learning resources.

    Strictly separate from factual research citations. Rejects vague advice, unverified links,
    and mismatched access/cost claims.
    """
    if audience not in {"beginner", "intermediate", "advanced"}:
        raise ValueError("audience must be beginner, intermediate, or advanced")
    stages = policy_registry()["progression_stages"]
    stage_rank = {stage: idx for idx, stage in enumerate(stages)}
    objectives_set = set(objectives or [])

    accepted: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    paywalled_alternatives: list[dict[str, Any]] = []

    for cand in candidates:
        if not isinstance(cand, dict):
            continue
        title = str(cand.get("title") or "").strip()
        if not title or any(pat.fullmatch(title) for pat in VAGUE_RESOURCE_PATTERNS):
            excluded.append({"title": title or "<empty>", "reason": "vague or non-specific recommendation"})
            continue
        if not cand.get("verified", False):
            excluded.append({"title": title, "reason": "resource existence or access not verified"})
            continue

        url = cand.get("canonical_url")
        if url:
            try:
                canon = canonicalize_url(url)
            except ValueError:
                excluded.append({"title": title, "reason": "invalid URL"})
                continue
            if is_bare_root_url(canon):
                excluded.append({"title": title, "reason": "bare root-domain URL lacks specificity"})
                continue
        else:
            canon = None

        cost = str(cand.get("cost") or "unknown").strip().lower()
        if free_only and cost != "free":
            if cost in {"paid", "freemium", "institutional"}:
                paywalled_alternatives.append({
                    "title": title,
                    "author_or_institution": cand.get("author_or_institution"),
                    "canonical_url": canon,
                    "cost": cost,
                    "note": "Excluded from free list because access is not free.",
                })
            else:
                excluded.append({"title": title, "reason": f"access cost '{cost}' not verified as free"})
            continue

        levels = cand.get("learner_levels") or ([cand["learner_level"]] if cand.get("learner_level") else ["beginner"])
        if audience not in levels:
            excluded.append({"title": title, "reason": f"level mismatch (targets {levels}, reader is {audience})"})
            continue

        stage = cand.get("progression_stage") or (
            "advanced_theory" if audience == "advanced" else "conceptual_foundation"
        )
        if stage not in stage_rank:
            stage = "conceptual_foundation"

        why = str(cand.get("why_useful") or "").strip()
        if not why:
            excluded.append({"title": title, "reason": "missing why_useful pedagogical justification"})
            continue

        obj_overlap = len(objectives_set & set(cand.get("objectives") or []))
        accepted.append({
            "title": title,
            "resource_type": cand.get("resource_type") or "textbook",
            "author_or_institution": cand.get("author_or_institution") or "[UNVERIFIED]",
            "canonical_url": canon,
            "section_or_chapter": cand.get("section_or_chapter"),
            "learner_level": audience,
            "prerequisites": list(cand.get("prerequisites") or []),
            "cost": cost,
            "progression_stage": stage,
            "priority": cand.get("priority") or "essential",
            "why_useful": why,
            "_score": (stage_rank[stage], 0 if (cand.get("priority") == "essential") else 1, -obj_overlap, title.lower()),
        })

    accepted.sort(key=lambda item: item["_score"])
    limit = len(accepted) if extensive else max(1, max_items)
    selected = []
    for item in accepted[:limit]:
        clean = {k: v for k, v in item.items() if k != "_score"}
        selected.append(clean)

    return {
        "audience": audience,
        "free_only": free_only,
        "recommended": selected,
        "paywalled_alternatives": paywalled_alternatives,
        "excluded": excluded,
    }


def build_research_package(
    research_plan: dict[str, Any],
    evidence_registry: dict[str, Any],
    *,
    learning_resources: dict[str, Any] | None = None,
    offline: bool = False,
) -> dict[str, Any]:
    """Assemble a compact, per-concept evidence handoff package for the adaptive instructional planner.

    Avoids passing full scraped webpages into generation passes.
    """
    sources_by_id = {s["source_id"]: s for s in (evidence_registry.get("sources") or [])}
    coverage = analyze_research_coverage(research_plan, evidence_registry)
    per_concept: dict[str, dict[str, Any]] = {}

    for q in research_plan.get("research_questions", []):
        cid = q["concept_id"]
        per_concept.setdefault(cid, {
            "concept_id": cid,
            "research_questions": [],
            "verified_claims": [],
            "qualifications": [],
            "assumptions": [],
            "contradictions": [],
            "citations": [],
            "implementation_versions": [],
            "unresolved_gaps": [],
        })
        per_concept[cid]["research_questions"].append({
            "id": q["id"],
            "question": q["question"],
            "evidence_type": q["evidence_type"],
            "research_depth": q["research_depth"],
        })

    for ev in evidence_registry.get("evidence", []):
        cid = ev["concept_id"]
        bucket = per_concept.setdefault(cid, {
            "concept_id": cid,
            "research_questions": [],
            "verified_claims": [],
            "qualifications": [],
            "assumptions": [],
            "contradictions": [],
            "citations": [],
            "implementation_versions": [],
            "unresolved_gaps": [],
        })
        claim_entry = {
            "evidence_id": ev["evidence_id"],
            "research_question_id": ev["research_question_id"],
            "claim": ev["claim"],
            "support_status": ev["support_status"],
            "evidence_origin": ev.get("evidence_origin"),
            "source_ids": ev["source_ids"],
            "source_locations": ev["source_locations"],
        }
        if ev["support_status"] in SUPPORTED_VERIFICATION_STATES:
            bucket["verified_claims"].append(claim_entry)
        else:
            bucket["unresolved_gaps"].append(claim_entry)

        for qual in ev.get("qualifications") or []:
            if qual not in bucket["qualifications"]:
                bucket["qualifications"].append(qual)
        for asm in ev.get("assumptions") or []:
            if asm not in bucket["assumptions"]:
                bucket["assumptions"].append(asm)
        for con in ev.get("contradictions") or []:
            if con not in bucket["contradictions"]:
                bucket["contradictions"].append(con)
        if ev.get("version") and ev["version"] not in bucket["implementation_versions"]:
            bucket["implementation_versions"].append(ev["version"])

        for sid in ev["source_ids"]:
            src = sources_by_id.get(sid)
            if src and all(c["source_id"] != sid for c in bucket["citations"]):
                bucket["citations"].append({
                    "source_id": sid,
                    "title": src["title"],
                    "source_type": src["source_type"],
                    "source_role": src["source_role"],
                    "canonical_url": src["canonical_url"],
                    "version": src["version"],
                    "is_preprint": src["is_preprint"],
                })

    for gap in coverage["gaps"]:
        cid = gap["concept_id"]
        if cid in per_concept:
            per_concept[cid]["unresolved_gaps"].append(gap)

    return {
        "research_plan_version": RESEARCH_PLAN_VERSION,
        "mode": research_plan.get("mode", "R-I"),
        "source_policy": research_plan.get("source_policy", "independent"),
        "offline": bool(offline or research_plan.get("offline", False)),
        "concepts": per_concept,
        "coverage_summary": coverage,
        "learning_resources": learning_resources or {"recommended": [], "paywalled_alternatives": []},
        "metrics": {
            "question_count": len(research_plan.get("research_questions", [])),
            "planned_query_count": sum(len(q.get("queries") or []) for q in research_plan.get("research_questions", [])),
            "retrieved_source_count": len(evidence_registry.get("sources", [])),
            "verified_claim_count": sum(1 for e in evidence_registry.get("evidence", []) if e["support_status"] in SUPPORTED_VERIFICATION_STATES),
            "unresolved_claim_count": sum(1 for e in evidence_registry.get("evidence", []) if e["support_status"] not in SUPPORTED_VERIFICATION_STATES),
            "independent_origin_count": evidence_registry.get("independence", {}).get("independent_origin_count", 0),
        },
    }


def validate_note_citations(
    note_text: str,
    evidence_registry: dict[str, Any],
    *,
    mode: str = "R-I",
    learning_resources: dict[str, Any] | None = None,
) -> list[tuple[int, str]]:
    """Audit citations in an authored note against verified records in the ARRIE evidence registry."""
    findings: list[tuple[int, str]] = []
    sources = evidence_registry.get("sources") or []
    verified_urls = {
        canonicalize_url(s["canonical_url"])
        for s in sources
        if s.get("canonical_url") and s.get("content_verified")
    }
    resource_urls = {
        canonicalize_url(r["canonical_url"])
        for r in (learning_resources or {}).get("recommended", [])
        if r.get("canonical_url")
    }
    allowed_urls = verified_urls | resource_urls
    all_source_urls = {canonicalize_url(s["canonical_url"]): s for s in sources if s.get("canonical_url")}

    in_fence = False
    for line_no, line in enumerate(note_text.splitlines(), 1):
        if re.match(r"^\s*(`{3,}|~{3,})", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        urls_in_line: list[str] = [m.group(2) for m in MARKDOWN_LINK_RE.finditer(line)]
        for raw_url in urls_in_line:
            if is_bare_root_url(raw_url):
                findings.append((line_no, f"Bare root-domain citation '{raw_url}' is forbidden."))
                continue
            try:
                canon = canonicalize_url(raw_url)
            except ValueError:
                findings.append((line_no, f"Malformed citation URL '{raw_url}'."))
                continue
            if mode == "R-S0" and canon not in verified_urls:
                findings.append((line_no, f"External citation '{raw_url}' violates strict source-only mode (R-S0)."))
            elif canon in all_source_urls and not all_source_urls[canon].get("content_verified"):
                findings.append((line_no, f"Citation '{raw_url}' points to an uninspected source (content_verified=False)."))
            elif allowed_urls and canon not in allowed_urls:
                findings.append((line_no, f"Unregistered citation '{raw_url}' does not match any verified source or curated resource in the evidence registry."))

    # Flag any unresolved contradiction or missing evidence that was omitted without disclosure
    for src in sources:
        if src.get("injection_detected"):
            for pat in PROMPT_INJECTION_PATTERNS:
                if pat.search(note_text):
                    findings.append((1, f"Untrusted prompt-injection text from {src['source_id']} leaked into the authored note."))
                    break

    return findings


def render_bibliography(evidence_registry: dict[str, Any]) -> list[str]:
    """Render clean Markdown reference bullets exclusively from verified source records."""
    lines: list[str] = []
    for src in evidence_registry.get("sources") or []:
        if not src.get("content_verified"):
            continue
        parts = [f"**{src['title']}**"]
        if src.get("publisher"):
            parts.append(str(src["publisher"]))
        if src.get("version"):
            parts.append(f"v{src['version']}")
        if src.get("publication_date"):
            parts.append(str(src["publication_date"]))
        if src.get("is_preprint"):
            parts.append("(preprint)")
        label = " — ".join(parts)
        if src.get("canonical_url"):
            lines.append(f"- `{src['source_id']}`: [{label}]({src['canonical_url']})")
        else:
            lines.append(f"- `{src['source_id']}`: {label}")
    return lines



# ---------------------------------------------------------------------------
# Integrated Research Cache (consolidated from research_cache.py)
# ---------------------------------------------------------------------------

DEFAULT_CACHE_DIR = Path.home() / ".cache" / "scriptorium" / "research"


def _policy_registry() -> dict[str, Any]:
    return policy_registry()


def _norm_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def cache_key(
    *,
    question: str,
    mode: str,
    source_policy: str,
    evidence_type: str,
    version: str | None = None,
    jurisdiction: str | None = None,
    language: str = "en",
    provider: str = "any",
    source_id: str | None = None,
) -> str:
    """Compute a deterministic cache key incorporating evidence freshness & provenance axes."""
    payload = {
        "question": _norm_text(question),
        "mode": mode,
        "source_policy": source_policy,
        "evidence_type": evidence_type,
        "version": _norm_text(version),
        "jurisdiction": _norm_text(jurisdiction),
        "language": _norm_text(language) or "en",
        "provider": _norm_text(provider) or "any",
        "source_id": _norm_text(source_id),
    }
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:32]


def freshness_window_days(evidence_type: str) -> int:
    """Return configured freshness TTL in days for an evidence category."""
    reg = _policy_registry()
    spec = reg.get("evidence_types", {}).get(evidence_type)
    if spec and isinstance(spec.get("freshness_days"), int):
        return spec["freshness_days"]
    return 180


def is_cache_entry_fresh(
    entry: dict[str, Any],
    *,
    evidence_type: str,
    now: datetime | None = None,
    required_version: str | None = None,
    force_refresh: bool = False,
) -> tuple[bool, str]:
    """Check whether a cached research entry is still valid under freshness, provenance, and version rules."""
    if force_refresh:
        return False, "explicit refresh requested"
    if not isinstance(entry, dict):
        return False, "malformed cache entry"
    if entry.get("invalidated"):
        return False, entry.get("invalidation_reason") or "entry invalidated"
    if entry.get("contradicted"):
        return False, "previously accepted claim was contradicted"
    if not entry.get("content_verified", False):
        return False, "missing verified provenance"

    cached_version = entry.get("version")
    if required_version and cached_version and _norm_text(required_version) != _norm_text(cached_version):
        return False, f"version changed ({cached_version} -> {required_version})"
    if required_version and not cached_version:
        return False, "cached entry lacks required version metadata"

    stored_at_raw = entry.get("cached_at")
    if not isinstance(stored_at_raw, str):
        return False, "missing cached_at timestamp"
    try:
        stored_at = datetime.fromisoformat(stored_at_raw.replace("Z", "+00:00"))
    except ValueError:
        return False, "invalid cached_at timestamp"
    if stored_at.tzinfo is None:
        stored_at = stored_at.replace(tzinfo=timezone.utc)
    now_dt = now or datetime.now(timezone.utc)
    if now_dt.tzinfo is None:
        now_dt = now_dt.replace(tzinfo=timezone.utc)

    ttl_days = freshness_window_days(evidence_type)
    age_days = (now_dt - stored_at).total_seconds() / 86400.0
    if age_days > ttl_days:
        return False, f"stale entry ({age_days:.1f}d > {ttl_days}d TTL for {evidence_type})"
    return True, "fresh"


class ResearchCache:
    """File-backed research cache with privacy and source-policy containment."""

    def __init__(self, cache_dir: Path | None = None) -> None:
        self.cache_dir = Path(cache_dir) if cache_dir is not None else DEFAULT_CACHE_DIR

    def _entry_path(self, key: str) -> Path:
        if not re.fullmatch(r"[0-9a-f]{32}", key):
            raise ValueError("Invalid cache key")
        return self.cache_dir / f"{key}.json"

    def put(
        self,
        key: str,
        payload: dict[str, Any],
        *,
        mode: str = "R-I",
        private: bool = False,
        source_type: str = "",
        now: datetime | None = None,
    ) -> bool:
        """Persist a verified public research entry. Refuses private or strict-source-only data."""
        if private or mode == "R-S0" or source_type == "local_user_source":
            return False
        if not payload.get("content_verified", False):
            return False
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        now_dt = now or datetime.now(timezone.utc)
        if now_dt.tzinfo is None:
            now_dt = now_dt.replace(tzinfo=timezone.utc)
        record = {
            **payload,
            "cache_key": key,
            "cached_at": now_dt.isoformat(),
            "invalidated": False,
        }
        self._entry_path(key).write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
        return True

    def get(
        self,
        key: str,
        *,
        evidence_type: str,
        now: datetime | None = None,
        required_version: str | None = None,
        force_refresh: bool = False,
    ) -> tuple[dict[str, Any] | None, str]:
        """Retrieve a cache entry only if it satisfies freshness, version, and provenance checks."""
        path = self._entry_path(key)
        if not path.is_file():
            return None, "cache miss"
        try:
            entry = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None, "corrupt cache entry"
        ok, reason = is_cache_entry_fresh(
            entry,
            evidence_type=evidence_type,
            now=now,
            required_version=required_version,
            force_refresh=force_refresh,
        )
        return (entry, "cache hit") if ok else (None, reason)

    def invalidate(self, key: str, reason: str = "manual invalidation") -> bool:
        """Mark an existing cache entry invalid so future lookups reverify."""
        path = self._entry_path(key)
        if not path.is_file():
            return False
        try:
            entry = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            path.unlink(missing_ok=True)
            return True
        entry["invalidated"] = True
        entry["invalidation_reason"] = reason
        path.write_text(json.dumps(entry, indent=2, ensure_ascii=False), encoding="utf-8")
        return True

# ---------------------------------------------------------------------------
# Engine E2 Cohesive Facade
# ---------------------------------------------------------------------------

class ResearchEngine:
    """Cohesive Engine E2 facade for ARRIE research planning, evidence verification, curation, caching, and citation audit."""

    def __init__(self, cache_dir: Path | None = None):
        self.cache = ResearchCache(cache_dir=cache_dir)

    def composition_evidence_status(self, composition: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
        from ._composition import evidence_status
        obligations = [o for c in composition["concepts"] for o in c["research_obligations"]]
        return evidence_status(obligations, evidence)

    def plan(self, topic: str, instructional_plan: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        return plan_research(topic, instructional_plan, **kwargs)

    def normalize_registry(self, registry: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        return normalize_evidence_registry(registry, **kwargs)

    def audit_citations(self, note_text: str, evidence_registry: dict[str, Any], **kwargs: Any) -> list[tuple[int, str]]:
        return validate_note_citations(note_text, evidence_registry, **kwargs)

    def package(self, research_plan: dict[str, Any], evidence_registry: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        return build_research_package(research_plan, evidence_registry, **kwargs)

    def curate_resources(
        self,
        topic_or_resources: str | list[dict[str, Any]],
        resources: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if isinstance(topic_or_resources, list) and resources is None:
            candidates = topic_or_resources
        else:
            candidates = list(resources or [])
        return curate_learning_resources(candidates, **kwargs)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)

    p_plan = sub.add_parser("plan", help="Generate a concept-specific ARRIE research plan from an instructional plan JSON.")
    p_plan.add_argument("--topic", required=True)
    p_plan.add_argument("--instructional-plan", type=Path, required=True)
    p_plan.add_argument("--request", default="")
    p_plan.add_argument("--mode", default=None)
    p_plan.add_argument("--offline", action="store_true")

    p_val = sub.add_parser("validate-registry", help="Validate an ARRIE source/evidence registry JSON.")
    p_val.add_argument("registry", type=Path)
    p_val.add_argument("--plan", type=Path, default=None)

    p_cov = sub.add_parser("coverage", help="Analyze research coverage and stopping criteria.")
    p_cov.add_argument("--plan", type=Path, required=True)
    p_cov.add_argument("--registry", type=Path, required=True)
    p_cov.add_argument("--offline", action="store_true")

    p_pkg = sub.add_parser("package", help="Build a compact generator handoff package from plan + evidence registry.")
    p_pkg.add_argument("--plan", type=Path, required=True)
    p_pkg.add_argument("--registry", type=Path, required=True)
    p_pkg.add_argument("--resources", type=Path, default=None)

    p_cur = sub.add_parser("curate", help="Curate learner-aware further-learning resources.")
    p_cur.add_argument("candidates", type=Path)
    p_cur.add_argument("--audience", choices=("beginner", "intermediate", "advanced"), default="beginner")
    p_cur.add_argument("--free-only", action="store_true")
    p_cur.add_argument("--extensive", action="store_true")

    p_aud = sub.add_parser("audit-citations", help="Audit note citations against an evidence registry.")
    p_aud.add_argument("note", type=Path)
    p_aud.add_argument("--registry", type=Path, required=True)
    p_aud.add_argument("--mode", default="R-I")

    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        if args.action == "plan":
            ip = json.loads(args.instructional_plan.read_text(encoding="utf-8-sig"))
            out = plan_research(args.topic, ip, request=args.request, explicit_mode=args.mode, offline=args.offline)
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0
        if args.action == "validate-registry":
            raw_reg = json.loads(args.registry.read_text(encoding="utf-8-sig"))
            rplan = json.loads(args.plan.read_text(encoding="utf-8-sig")) if args.plan else None
            out = normalize_evidence_registry(raw_reg, research_plan=rplan)
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0
        if args.action == "coverage":
            rplan = normalize_research_plan(json.loads(args.plan.read_text(encoding="utf-8-sig")))
            ereg = normalize_evidence_registry(json.loads(args.registry.read_text(encoding="utf-8-sig")), research_plan=rplan)
            out = should_stop_research(rplan, ereg, offline=args.offline)
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0
        if args.action == "package":
            rplan = normalize_research_plan(json.loads(args.plan.read_text(encoding="utf-8-sig")))
            ereg = normalize_evidence_registry(json.loads(args.registry.read_text(encoding="utf-8-sig")), research_plan=rplan)
            res = json.loads(args.resources.read_text(encoding="utf-8-sig")) if args.resources else None
            out = build_research_package(rplan, ereg, learning_resources=res)
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0
        if args.action == "curate":
            cands = json.loads(args.candidates.read_text(encoding="utf-8-sig"))
            out = curate_learning_resources(cands, audience=args.audience, free_only=args.free_only, extensive=args.extensive)
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0
        if args.action == "audit-citations":
            text = args.note.read_text(encoding="utf-8-sig")
            ereg = normalize_evidence_registry(json.loads(args.registry.read_text(encoding="utf-8-sig")), mode=args.mode)
            findings = validate_note_citations(text, ereg, mode=args.mode)
            print(json.dumps({"errors": len(findings), "findings": [{"line": l, "message": m} for l, m in findings]}, indent=2))
            return 1 if findings else 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
