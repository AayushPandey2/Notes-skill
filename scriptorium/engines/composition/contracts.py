"""Executable educational obligations shared by composition, KCP and publication.

Semantic review is a signed assertion about exact artifacts, never a proof inferred
from nonempty prose. Deterministic checks keep their narrower scope in the manifest.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
import time
from typing import Any

from scriptorium.models import content_hash, parse_note
from . import checks

STATES = frozenset({"planned", "ready", "generated", "verified", "blocked", "justifiably-omitted", "failed"})
DOMAINS = ("structural", "computational", "mathematical", "research", "visual", "educational")
PREREQUISITES = frozenset({"essential", "supporting", "optional", "covered", "assumed", "missing"})
ASSESSMENT_TYPES = frozenset({"conceptual", "mathematical", "numerical", "algorithmic", "implementation",
                              "comparison", "diagnosis", "experimental_design", "historical", "causal"})
CHECK_FIELDS = {
    "proofs": ("mathematical", "proof"), "claims": ("research", "claim"),
    "information_flows": ("computational", "flow"), "tensors": ("computational", "tensor"),
    "examples": ("computational", "example"), "implementations": ("computational", "implementation"),
    "numerical_tests": ("computational", "numerical"), "failures": ("educational", "failure"),
    "costs": ("computational", "cost"), "diagnostics": ("research", "diagnostics"),
    "gaps": ("educational", "gap"),
}
DEPTH_DELIVERABLES = {
    "conceptual": "motivate the problem; connect intuition, definitions and mechanism; bridge prerequisites before use; work an appropriate example with intermediate reasoning; interpret the result, assumptions, limits, relationships and likely misconception without repeated filler",
    "mathematical": "state assumptions and show intermediate derivation with boundary checks",
    "algorithmic": "trace actual algorithm state, invariants and termination",
    "implementation": "state backend, input/output contract, executable path and testing level",
    "research": "attach claim-level evidence with source scope, uncertainty and version",
    "visual": "review the learning difficulty and deliver a verified representation or justified omission",
    "analytical": "compare assumptions, alternatives, failure diagnostics and downstream effects",
}


def objective_kind(goal: str, explicit: str | None = None) -> str:
    allowed = {"historical", "algorithmic", "mathematical", "causal", "implementation", "reproduction", "synthesis", "conceptual", "visual"}
    if explicit is not None:
        if explicit not in allowed:
            raise ValueError("Unknown semantic objective kind")
        return explicit
    text = goal.casefold()
    if re.search(r"\b(history|historical|evolution|chronology|development over time)\b", text):
        return "historical"
    if re.search(r"\b(reproduce|replicate|reproduction)\b", text):
        return "reproduction"
    if re.search(r"\b(derive|prove|derivation|proof)\b", text):
        return "mathematical"
    if re.search(r"\b(implement|debug|code)\b", text):
        return "implementation"
    if re.search(r"\b(trace|execute|simulate)\b", text) and re.search(r"\b(state|states|iteration|algorithm|execution|loop|tokens?)\b", text):
        return "algorithmic"
    if re.search(r"\b(cause|causal|why)\b", text):
        return "causal"
    if re.search(r"\b(compare|synthesize|connect|analyze)\b", text):
        return "synthesis"
    if re.search(r"\b(visualize|plot|draw)\b", text):
        return "visual"
    return "conceptual"


def extend_plan(plan: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    """Extend the existing composition field in KCP; no parallel plan transport."""
    plan["version"] = 2
    plan["assessments"] = deepcopy(spec.get("assessments", []))
    plan["validation_policy"] = {"chapter_assessments": True, **spec.get("validation_policy", {})}
    # A comprehensive chapter always needs its educational assessment. Narrow
    # products already use their own M2-M7/single-note paths.
    if plan["validation_policy"]["chapter_assessments"] is not True:
        raise ValueError("Comprehensive chapters require objective-aligned assessment")
    obligations = []
    by_id = {c["id"]: c for c in plan["concepts"]}
    owners = {cid: chapter for chapter in plan["chapters"] for cid in chapter["concepts"]}

    def add(oid, cid, deliverable, verifier, domain, dependencies=(), record=None, severity="critical"):
        chapter = owners[cid]
        obligations.append({"id": oid, "concept": cid, "owner": chapter["id"], "chapter": chapter["path"],
                            "section": by_id[cid].get("section", by_id[cid]["title"]), "deliverable": deliverable,
                            "dependencies": list(dependencies), "verifier": verifier, "domain": domain,
                            "severity": severity, "status": "planned", "evidence": [], "record": record})

    for concept in plan["concepts"]:
        cid = concept["id"]
        concept["objective_ids"] = [f"{cid}:objective:{i}" for i in range(len(concept["objectives"]))]
        concept["objective_kinds"] = [objective_kind(g, concept.get("objective_kinds", {}).get(str(i)))
                                      for i, g in enumerate(concept["objectives"])]
        base = []
        for i, objective in enumerate(concept["objectives"]):
            oid = concept["objective_ids"][i]
            add(oid, cid, objective, "review", "educational")
            base.append(oid)
        for dim, level in concept["depth_allocation"]["levels"].items():
            if level:
                add(f"{cid}:depth:{dim}", cid, f"Level {level}: {DEPTH_DELIVERABLES[dim]}", "review",
                    {"mathematical": "mathematical", "research": "research", "visual": "visual"}.get(dim, "educational"), base)
        for capability in concept["capabilities"]:
            add(f"{cid}:capability:{capability}", cid, f"Deliver the active {capability} technical contributions", "review", "educational", base)
        for obligation in concept["research_obligations"]:
            add(obligation["id"], cid, obligation["requirement"], "research_record", "research", base, obligation)
        for field, (domain, verifier) in CHECK_FIELDS.items():
            for record in concept.get(field, []):
                if not record.get("id"):
                    raise ValueError(f"{field} records need stable IDs")
                add(record["id"], cid, record.get("claim", record.get("text", record.get("description", field))),
                    verifier, domain, record.get("dependencies", base), record)
        for index, term in enumerate(concept.get("terminology", [])):
            add(f"{cid}:term:{index}", cid, f"Define {term.get('term', 'term')} before use", "terminology", "educational", (), term)
        levels = concept["depth_allocation"]["levels"]
        if (levels["mathematical"] >= 3 or "S02" in concept["capabilities"]) and not concept.get("proofs"):
            add(f"{cid}:required-proof", cid, "Supply the consequential mathematical derivation contract", "missing", "mathematical", base)
        if (levels["implementation"] >= 3 or "S04" in concept["capabilities"]) and not concept.get("implementations"):
            add(f"{cid}:required-implementation", cid, "Supply implementation scope and actual execution evidence", "missing", "computational", base)
        if "S05" in concept["capabilities"] and not concept.get("information_flows"):
            add(f"{cid}:required-flow", cid, "Supply computational branch and information permissions", "missing", "computational", base)
        if concept.get("signals", {}).get("tensor_heavy") and not concept.get("tensors"):
            add(f"{cid}:required-tensors", cid, "Supply tensor, tokenizer, label-shift and readout contracts", "missing", "computational", base)
        if "S06" in concept["capabilities"] and not concept.get("claims"):
            add(f"{cid}:required-claims", cid, "Supply exact versioned claims from the analyzed source", "missing", "research", base)
        if "S09" in concept["capabilities"] and not concept.get("examples"):
            add(f"{cid}:required-examples", cid, "Classify the worked example and provide its actual provenance", "missing", "educational", base)
        if (levels["visual"] or "S12" in concept["capabilities"]):
            review = concept.get("visual_review", {})
            add(f"{cid}:visual-opportunity", cid, "Review visual learning difficulty and placement", "visual_review", "visual", base, review)
        for prereq in concept.get("prerequisite_records", []):
            if prereq["classification"] == "missing":
                add(f"{cid}:prerequisite:{prereq['id']}", cid, f"Bridge missing prerequisite {prereq['id']}", "gap", "educational", base, prereq)
    # Resolve assessment identity and ownership against the same canonical plan.
    # Otherwise a question assigned to an unknown chapter is silently ignored by
    # every chapter checker, despite remaining in the publication manifest.
    if not isinstance(plan["assessments"], list):
        raise ValueError("Assessments must be a list of question records")
    question_ids = set()
    chapter_objectives = {chapter["id"]: {oid for cid in chapter["concepts"] for oid in by_id[cid]["objective_ids"]}
                          for chapter in plan["chapters"]}
    for question in plan["assessments"]:
        if not isinstance(question, dict):
            raise ValueError("Assessment must be a question record")
        qid, owner = question.get("id"), question.get("chapter")
        if not isinstance(qid, str) or not qid.strip() or qid in question_ids:
            raise ValueError("Assessment IDs must be nonempty and globally unique")
        question_ids.add(qid)
        if not isinstance(owner, str) or owner not in chapter_objectives:
            raise ValueError(f"Assessment refers to an unknown chapter: {owner}")
        objectives = question.get("objectives")
        if (not isinstance(objectives, list) or not objectives
                or any(not isinstance(oid, str) or oid not in chapter_objectives[owner] for oid in objectives)):
            raise ValueError("Assessment objective must belong to its owning chapter")
        placement = question.get("placement", "chapter_end")
        if not isinstance(placement, str) or not placement.strip():
            raise ValueError("Assessment placement must name a milestone heading or chapter_end")
    for i, visual in enumerate(plan["visuals"]):
        visual.setdefault("id", f"{visual['concept']}:visual:{i}")
        add(visual["id"], visual["concept"], visual["objective"], "visual", "visual",
            visual.get("dependencies", by_id[visual["concept"]]["objective_ids"]), visual,
            "critical" if visual.get("required", True) else "warning")
    for chapter in plan["chapters"]:
        add(f"{chapter['id']}:assessment", chapter["concepts"][0], "Four to five diverse final questions, hints, solutions and objective coverage",
            "assessment", "educational", [oid for cid in chapter["concepts"] for oid in by_id[cid]["objective_ids"]], chapter)
    for obligation in obligations:
        if obligation["verifier"] == "review":
            obligation["dependencies"] += [o["id"] for o in obligations if o["concept"] == obligation["concept"]
                                            and o["verifier"] in {"proof", "flow", "tensor", "claim"}]
    ids = {o["id"] for o in obligations}
    if len(ids) != len(obligations):
        raise ValueError("Obligation IDs must be unique across the composition")
    for obligation in obligations:
        if set(obligation["dependencies"]) - ids:
            raise ValueError(f"Unknown obligation dependency: {obligation['id']}")
    # Objective reviews and proof records both depend on coverage, so avoid
    # introducing a review/proof dependency cycle: proofs stand on prerequisites.
    for obligation in obligations:
        if obligation["verifier"] != "review":
            obligation["dependencies"] = [d for d in obligation["dependencies"]
                                            if not (d in by_id[obligation["concept"]]["objective_ids"])]
    pending, done = list(obligations), set()
    while pending:
        ready = [o for o in pending if set(o["dependencies"]) <= done]
        if not ready:
            raise ValueError("Cyclic educational obligation dependencies")
        for obligation in ready:
            done.add(obligation["id"])
            pending.remove(obligation)
    plan["obligations"] = obligations
    return plan


def render_question(question: dict[str, Any]) -> str:
    if any(not question.get(k) for k in ("id", "question", "hint", "solution", "type", "objectives")):
        raise ValueError("Assessment needs question, hint, detailed solution, type and objectives")
    if any(not isinstance(question[k], str) or not question[k].strip()
           for k in ("id", "question", "hint", "solution", "type")):
        raise ValueError("Assessment question, hint and detailed solution must be nonempty text")
    def quote(text):
        return "\n".join("> " + line if line else ">" for line in text.splitlines())
    return (f"**Question ({question['id']}):** {question['question']}\n\n"
            f"> [!hint]- Show hint\n{quote(question['hint'])}\n\n"
            f"> [!answer]- Show detailed answer\n{quote(question['solution'])}")


def prepare_drafts(plan: dict[str, Any], drafts: dict[str, str]) -> dict[str, str]:
    """Insert declared tables and assessment at owned headings; never append to a missing draft."""
    from . import render_table
    result = dict(drafts)
    for chapter in plan["chapters"]:
        cid = chapter["id"]
        if not result.get(cid, "").strip():
            continue
        body = result[cid]
        for table in plan.get("tables", []):
            if table["concept"] in chapter["concepts"]:
                rendered = render_table(table)
                if rendered not in body:
                    body = insert_at_section(body, table["section"], rendered)
        questions = [q for q in plan["assessments"] if q.get("chapter") == cid]
        final = []
        for question in questions:
            text = render_question(question)
            if text in body:
                continue
            if question.get("placement", "chapter_end") == "chapter_end":
                final.append(text)
            else:
                body = insert_at_section(body, question["placement"], text)
        if final:
            body = body.rstrip() + "\n\n## Check your understanding\n\n" + "\n\n".join(final) + "\n"
        result[cid] = body
    return result


def insert_at_section(body: str, section: str, text: str) -> str:
    # Keep a contribution inside its owning section, before the next peer/parent.
    note = parse_note(body)
    lines = body.splitlines(keepends=True)
    fenced = {i + note.body_start_line for block in note.code_blocks
              for i in range(block["start_line"], block["end_line"] + 1)}
    headings, offset = [], 0
    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line.rstrip("\r\n"))
        if match and index not in fenced:
            headings.append((offset, len(match[1]), match[2]))
        offset += len(line)
    # A document title commonly repeats its first concept heading. Prefer the
    # substantive section; use the title itself only when no section matches.
    matches = [i for i, (_, level, title) in enumerate(headings) if title == section and level > 1]
    if not matches:
        matches = [i for i, (_, _, title) in enumerate(headings) if title == section]
    if len(matches) != 1:
        raise ValueError(f"missing contribution placement heading or ambiguous heading: {section}")
    owner = matches[0]
    end = next((offset for offset, level, _ in headings[owner + 1:] if level <= headings[owner][1]), len(body))
    return body[:end].rstrip() + "\n\n" + text + "\n\n" + body[end:]


def receipt_errors(receipt: Any, drafts: dict[str, str]) -> list[str]:
    if not isinstance(receipt, dict):
        return ["review must be structured artifact evidence; a nonempty string is insufficient"]
    fields = ("verifier", "method", "evidence", "limitations", "result")
    errors = [f"review missing {f}" for f in fields if not receipt.get(f)]
    if receipt.get("result") != "pass":
        errors.append("review did not pass")
    if not isinstance(receipt.get("evidence"), list):
        return errors + ["review evidence must bind exact chapter content"]
    for item in receipt["evidence"]:
        if not isinstance(item, dict):
            errors.append("review evidence items must identify a chapter, hash and excerpt")
            continue
        body = drafts.get(item.get("chapter", ""), "")
        if not body or item.get("hash") != content_hash(body) or not item.get("excerpt") or item["excerpt"] not in body:
            errors.append("stale or ungrounded review evidence")
    return errors


def _review_chapters(receipt: Any) -> set[str]:
    if not isinstance(receipt, dict) or not isinstance(receipt.get("evidence"), list):
        return set()
    return {item.get("chapter") for item in receipt["evidence"] if isinstance(item, dict)}


def check_assessment(plan: dict[str, Any], chapter: dict[str, Any], body: str) -> list[str]:
    questions = [q for q in plan["assessments"] if q.get("chapter") == chapter["id"]]
    final = [q for q in questions if q.get("placement", "chapter_end") == "chapter_end"]
    errors = []
    if not 4 <= len(final) <= 5:
        errors.append("comprehensive chapter needs four to five final questions")
    if len({q.get("type") for q in final}) < 3 or any(q.get("type") not in ASSESSMENT_TYPES for q in questions):
        errors.append("assessment lacks diversity across learning tasks")
    objectives = {oid for c in plan["concepts"] if c["id"] in chapter["concepts"] for oid in c["objective_ids"]}
    covered = {oid for q in questions for oid in q.get("objectives", [])}
    if objectives - covered or covered - objectives:
        errors.append("assessment objective coverage is missing or refers to another chapter")
    if len({q.get("id") for q in questions}) != len(questions):
        errors.append("assessment IDs must be unique")
    for question in questions:
        try:
            rendered = render_question(question)
            if rendered not in body:
                errors.append("independently folded hint/answer is absent from its chapter")
            placement = question.get("placement", "chapter_end")
            if placement != "chapter_end":
                sections = [s for s in parse_note(body).sections if s.heading == placement]
                if len(sections) != 1 or rendered not in sections[0].content:
                    errors.append("section check is absent from its declared milestone heading")
        except ValueError as exc:
            errors.append(str(exc))
    return errors


def _gap_errors(record: dict[str, Any], body: str) -> list[str]:
    errors = []
    if not record.get("resolved_excerpt") or record["resolved_excerpt"] not in body:
        errors.append("explanation gap lacks an actual prerequisite bridge or transition")
    if record.get("before"):
        if record["before"] not in body or body.find(record.get("resolved_excerpt", "")) >= body.find(record["before"]):
            errors.append("prerequisite bridge must precede the dependent equation or term")
    if not record.get("gap") and not record.get("classification"):
        errors.append("explanation gap needs a diagnosis")
    return errors


def _verify_obligation(obligation, plan, drafts, evidence, visuals, vault):
    verifier, record = obligation["verifier"], obligation.get("record") or {}
    body = drafts.get(obligation["owner"], "")
    if not body:
        return ["missing owning chapter"]
    if verifier == "review":
        return []
    if verifier == "missing":
        return [obligation["deliverable"]]
    if verifier == "research_record":
        from . import evidence_status
        return [] if evidence_status([record], evidence)["sufficient"] else ["insufficient ARRIE evidence"]
    if verifier == "proof":
        return checks.check_proof(record) + ([] if record.get("claim") in body else ["mathematical claim is absent from chapter"])
    if verifier == "claim":
        errors = checks.check_claim(record, source_policy=plan["source_policy"])
        if record.get("text") not in body:
            errors.append("exact claim is absent from chapter")
        source = record.get("source", {})
        if source.get("snapshot"):
            from . import contained
            try:
                path = contained(vault, source["snapshot"])
                raw = path.read_bytes()
                if content_hash(raw) != source.get("hash") or source.get("excerpt", "") not in raw.decode("utf-8-sig"):
                    errors.append("source snapshot/hash/excerpt does not support the provenance record")
            except (OSError, ValueError) as exc:
                errors.append(f"claim source snapshot unavailable: {exc}")
        return errors
    if verifier in {"flow", "tensor", "example", "numerical", "failure", "cost", "diagnostics"}:
        fn = {"flow": checks.check_flow, "tensor": checks.check_tensor, "example": checks.check_example,
              "numerical": checks.check_numerical, "failure": checks.check_failure,
              "cost": checks.check_cost, "diagnostics": checks.check_diagnostics}[verifier]
        issues = fn(record)
        excerpt = record.get("artifact_excerpt")
        if not excerpt or excerpt not in body:
            issues.append("technical contract lacks its actual educational artifact excerpt")
        if verifier == "example" and record.get("execution"):
            issues.extend(checks.check_execution_artifact(record["execution"], body))
        return issues
    if verifier == "implementation":
        return checks.check_implementation(record, body)
    if verifier == "gap":
        return _gap_errors(record, body)
    if verifier == "terminology":
        if not all(record.get(k) for k in ("term", "definition", "first_use")):
            return ["undefined term or notation lacks a definition/use contract"]
        if record["definition"] not in body or record["first_use"] not in body or body.find(record["definition"]) >= body.find(record["first_use"]):
            return ["undefined term or notation: prerequisite must precede the equation or first use"]
        return []
    if verifier == "assessment":
        return check_assessment(plan, record, body)
    if verifier == "visual_review":
        if not all(record.get(k) for k in ("objective", "difficulty", "representation", "placement", "validation")):
            return ["visual opportunity review is missing the learning difficulty or validation"]
        actual = [v for v in plan["visuals"] if v["concept"] == obligation["concept"]]
        if not actual and not record.get("omission_reason"):
            return ["visual depth allocated without a planned artifact or reasoned omission"]
        return []
    if verifier == "visual":
        result = visuals.get(obligation["id"], {})
        if result.get("status") == "unavailable" and result.get("unmet_visual_obligation"):
            return [f"unmet visual obligation: {result.get('failure_reason') or 'no permitted web image found'}"]
        if result.get("status") != "verified" or not result.get("attempted") or not result.get("hash"):
            reason = result.get("failure_reason")
            detail = f" ({reason})" if reason else ""
            return [f"required visual lacks executed renderer/acquisition and verified asset{detail}"]
        embed = result.get("embed", f"![[{result.get('path')}]]")
        if not isinstance(embed, str) or not embed.strip() or embed not in body:
            return ["verified visual is not embedded in its owning chapter"]
        if record.get("empirical"):
            claims = {c["id"]: c for concept in plan["concepts"] for c in concept.get("claims", [])}
            selected = [claims.get(cid, {}) for cid in record.get("verified_comparable_claims", [])]
            if not selected or any(c.get("classification") != "empirical_observation" or checks.check_claim(c, source_policy=plan["source_policy"]) for c in selected):
                return ["empirical chart requires actual verified empirical claims"]
            signatures = {json.dumps({k: c["empirical"].get(k) for k in ("dataset", "adaptation", "metric", "protocol", "units")}, sort_keys=True) for c in selected}
            if len(signatures) != 1:
                return ["empirical chart mixes incomparable datasets, regimes, metrics, protocols or units"]
            ys = [point[1] for series in record.get("data", {}).values() for point in series]
            if sorted(ys) != sorted(c["empirical"]["value"] for c in selected):
                return ["empirical chart values disagree with the cited measurements"]
        return []
    return [f"unknown obligation verifier: {verifier}"]


def validate_obligations(plan: dict[str, Any], drafts: dict[str, str], *, evidence: dict[str, Any],
                         reviews: dict[str, Any], visuals: dict[str, Any], vault: Path, cache=None) -> dict[str, Any]:
    started = time.perf_counter()
    obligations = deepcopy(plan["obligations"])
    errors, outcomes = [], {domain: {"status": "not_applicable", "obligations": []} for domain in DOMAINS}
    scope = content_hash(str(vault.resolve()))[:16]
    source_hashes = {}
    concepts = {c["id"]: c for c in plan["concepts"]}
    def dependency_concepts(cid):
        result = {cid}
        for parent in concepts[cid].get("prerequisites", []):
            result.update(dependency_concepts(parent))
        return result
    from . import contained
    for concept in plan["concepts"]:
        for claim in concept.get("claims", []):
            snapshot = claim.get("source", {}).get("snapshot")
            if snapshot:
                try:
                    source_hashes[snapshot] = content_hash(contained(vault, snapshot).read_bytes())
                except (OSError, ValueError):
                    source_hashes[snapshot] = None
    for name in plan["review_required"]:
        record = reviews.get(name)
        issues = receipt_errors(record, drafts)
        if isinstance(record, dict) and _review_chapters(record) != set(drafts):
            issues.append("collection review must cover every authored chapter")
        errors.extend(f"{name}: {issue}" for issue in issues)
    receipts = reviews.get("obligations", {})
    if not isinstance(receipts, dict):
        errors.append("obligation reviews must be an ID-to-receipt mapping")
        receipts = {}
    for obligation in obligations:
        domain = outcomes[obligation["domain"]]
        domain["obligations"].append(obligation["id"])
        receipt = receipts.get(obligation["id"])
        issues = receipt_errors(receipt, drafts)
        if isinstance(receipt, dict) and obligation["owner"] not in _review_chapters(receipt):
            issues.append("obligation review does not cover its owning chapter")
        key = None
        cached = False
        if cache is not None:
            related = dependency_concepts(obligation["concept"])
            related_sources = {claim["source"]["snapshot"] for cid in related for claim in concepts[cid].get("claims", [])
                               if claim.get("source", {}).get("snapshot")}
            related_chapters = {c["id"] for c in plan["chapters"] if related.intersection(c["concepts"])}
            related_visuals = {v["id"] for v in plan["visuals"] if v["concept"] in related}
            dependencies = {"version": plan["validator_version"], "obligation": obligation,
                            "drafts": {cid: drafts.get(cid) for cid in sorted(related_chapters)},
                            "concepts": [concepts[cid] for cid in sorted(related)],
                            "assessments": [q for q in plan["assessments"] if q.get("chapter") in related_chapters],
                            "evidence": {o["id"]: evidence.get(o["id"]) for o in obligations if o["concept"] in related},
                            "sources": {s: source_hashes[s] for s in related_sources},
                            "visuals": {vid: {k: visuals.get(vid, {}).get(k) for k in ("renderer", "input_hash", "hash", "status", "attempted")}
                                        for vid in sorted(related_visuals)}, "policy": plan["source_policy"]}
            key = cache.build_key("L9_validation_result", user_scope=scope, dependencies=dependencies)
            cached, check_errors = cache.get(key, expected_user_scope=scope)
        if not cached:
            try:
                check_errors = _verify_obligation(obligation, plan, drafts, evidence, visuals, vault)
            except (ValueError, TypeError, KeyError, ArithmeticError, AttributeError, IndexError) as exc:
                check_errors = [f"malformed obligation contract: {exc}"]
            if cache is not None:
                cache.put(key, check_errors, user_scope=scope)
        issues.extend(check_errors)
        omission = isinstance(receipt, dict) and receipt.get("status") == "justifiably-omitted"
        if omission and obligation["severity"] != "critical" and receipt.get("omission_reason") and not receipt_errors(receipt, drafts):
            obligation["status"] = "justifiably-omitted"
            obligation["evidence"] = receipt
            issues = []
        else:
            obligation["status"] = "failed" if check_errors else "generated" if issues else "verified"
            if not drafts.get(obligation["owner"]):
                obligation["status"] = "blocked"
        # Keep the receipt in one canonical registry instead of copying it twice
        # into every result and again into the publication manifest.
        receipt_reference = f"reviews.obligations.{obligation['id']}" if receipt else None
        obligation["evidence"] = [receipt_reference] if receipt_reference else []
        obligation["validation"] = {"verifier": f"KCP/{obligation['verifier']}", "method": "scoped deterministic checks plus artifact-bound review",
                                     "result": "fail" if issues else "pass", "evidence": receipt_reference,
                                     "limitations": "Checks validate explicit contracts; source entailment and open-ended teaching require review.",
                                     "errors": issues, "cached": cached}
        obligation["status_history"] = ["planned", "ready", "generated"] if drafts.get(obligation["owner"]) else ["planned"]
        if obligation["status"] != "generated":
            obligation["status_history"].append(obligation["status"])
        if issues:
            errors.extend(f"{obligation['id']}: {issue}" for issue in issues)
        obligation.pop("record", None)  # canonical record remains in plan.obligations
    by_id = {o["id"]: o for o in obligations}
    changed = True
    while changed:
        changed = False
        for obligation in obligations:
            failed = [d for d in obligation["dependencies"] if by_id[d]["status"] not in {"verified", "justifiably-omitted"}]
            if failed and obligation["status"] in {"verified", "justifiably-omitted"}:
                obligation["status"] = "blocked"
                obligation["status_history"].append("blocked")
                obligation["validation"]["result"] = "blocked"
                obligation["validation"]["errors"].append(f"unresolved dependencies: {failed}")
                errors.append(f"{obligation['id']}: unresolved dependencies {failed}")
                changed = True
    for domain in outcomes.values():
        if domain["obligations"]:
            domain["status"] = "pass" if all(by_id[oid]["status"] in {"verified", "justifiably-omitted"} for oid in domain["obligations"]) else "fail"
    return {"complete": not errors, "errors": errors, "obligations": obligations, "outcomes": outcomes,
            "disclosure": {"format": "Obsidian native independently folded callouts", "ui_tested": False,
                           "limitation": "Reading View, Live Preview, keyboard, mobile and themes require a live Obsidian environment."},
            "metrics": {"elapsed_seconds": time.perf_counter()-started, "obligations": len(obligations),
                        "cached_checks": sum(o["validation"]["cached"] for o in obligations), "model_calls": 0,
                        "model_tokens": None, "cache": dict(cache.stats) if cache else {}}}


DEPTH_COMPLETENESS_CHECKLIST = (
    ("problem_statement", "What problem does this solve?"),
    ("necessity", "Why is it necessary?"),
    ("prerequisites", "What prerequisites are required?"),
    ("intuition", "What is the intuition?"),
    ("formal_definition", "What is the formal definition?"),
    ("mechanism", "How does the mechanism work?"),
    ("intermediate_steps", "What happens at each intermediate step?"),
    ("mathematics", "What mathematics is involved, when relevant?"),
    ("symbol_definitions", "What do the symbols represent?"),
    ("demonstration", "How can the concept be demonstrated?"),
    ("worked_example", "What is a complete worked example?"),
    ("visuals", "What visual representations help explain it?"),
    ("visual_interpretation", "How should those visuals be interpreted?"),
    ("assumptions", "What assumptions are involved?"),
    ("failure_modes", "When does the approach fail?"),
    ("misconceptions", "What common misconceptions arise?"),
    ("adjacent_connections", "How does it relate to adjacent concepts?"),
    ("advanced_details", "What advanced details are necessary?"),
    ("assessment", "How can understanding be assessed?"),
)


def evaluate_chapter_depth_contract(
    plan: dict[str, Any],
    chapter: dict[str, Any],
    body: str,
) -> dict[str, Any]:
    """Evaluate applicable educational obligations without imposing mechanical word quotas."""
    concepts = [c for c in plan.get("concepts", []) if c["id"] in chapter.get("concepts", [])]
    applicable: list[str] = ["problem_statement", "intuition", "mechanism", "worked_example", "assumptions", "assessment"]
    if any(c.get("prerequisite_records") for c in concepts):
        applicable.append("prerequisites")
    if any(c.get("depth_allocation", {}).get("levels", {}).get("mathematical", 0) >= 2 for c in concepts):
        applicable.extend(["formal_definition", "intermediate_steps", "mathematics", "symbol_definitions"])
    if any(c.get("depth_allocation", {}).get("levels", {}).get("visual", 0) >= 1 for c in concepts) or any(
        v.get("concept") in chapter.get("concepts", []) for v in plan.get("visuals", [])
    ):
        applicable.extend(["visuals", "visual_interpretation"])
    if any(c.get("depth_allocation", {}).get("levels", {}).get("analytical", 0) >= 2 or c.get("failures") for c in concepts):
        applicable.extend(["failure_modes", "misconceptions", "adjacent_connections"])
    if any(c.get("depth_allocation", {}).get("levels", {}).get("research", 0) >= 3 for c in concepts):
        applicable.append("advanced_details")
    applicable = list(dict.fromkeys(applicable))

    note = parse_note(body)
    nonempty_paragraphs = [p for p in re.split(r"\n\s*\n", note.body) if p.strip() and not p.strip().startswith("#")]
    h2_count = sum(1 for s in note.sections if s.level == 2)
    word_count = len(re.findall(r"\b\w+\b", note.body))
    concept_count = max(1, len(concepts))
    overcompressed = concept_count >= 3 and word_count < concept_count * 90
    shallow = (len(nonempty_paragraphs) < 2 and h2_count < 2) or overcompressed
    recommendation = (
        f"Split or expand overcompressed concepts ({concept_count} concepts in {word_count} words); "
        "ensure intuition, math deconstruction, and worked examples per major concept."
        if overcompressed
        else ""
    )
    return {
        "chapter_id": chapter.get("id"),
        "applicable_obligations": applicable,
        "section_count": h2_count,
        "paragraph_count": len(nonempty_paragraphs),
        "word_count": word_count,
        "concept_count": concept_count,
        "overcompressed": overcompressed,
        "structurally_shallow": shallow,
        "recommendation": recommendation,
        "checklist_size": len(DEPTH_COMPLETENESS_CHECKLIST),
    }


def repair_plan(plan: dict[str, Any], failed: list[str]) -> dict[str, Any]:
    """Dependency closure ordered with critical proof/flow fixes before expansion."""
    by_id = {o["id"]: o for o in plan["obligations"]}
    if set(failed) - set(by_id):
        raise ValueError("Unknown repair obligation")
    affected = set(failed)
    concepts = {by_id[oid]["concept"] for oid in failed}
    changed = True
    while changed:
        changed = False
        for concept in plan["concepts"]:
            if set(concept.get("prerequisites", [])).intersection(concepts) and concept["id"] not in concepts:
                concepts.add(concept["id"])
                changed = True
        for obligation in by_id.values():
            if (set(obligation["dependencies"]).intersection(affected) or obligation["concept"] in concepts) and obligation["id"] not in affected:
                affected.add(obligation["id"])
                changed = True
    ordered = sorted(affected, key=lambda oid: (by_id[oid]["verifier"] not in {"proof", "flow", "tensor"}, by_id[oid]["chapter"], oid))
    return {"obligations": ordered, "sections": sorted({(by_id[oid]["owner"], by_id[oid]["section"]) for oid in affected}),
            "chapters": sorted({by_id[oid]["owner"] for oid in affected}),
            "assets": [v["id"] for v in plan["visuals"] if v["concept"] in concepts],
            "preserve": [c["id"] for c in plan["chapters"] if not concepts.intersection(c["concepts"])]}
