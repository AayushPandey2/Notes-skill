"""Comprehensive composition contracts, owned by E4; no retrieval or model calls.

Agent decisions are explicit inputs. Deterministic checks cannot certify pedagogy,
proofs, source truth, or scientific accuracy; review obligations remain visible.
"""
from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
import re
from typing import Any

from scriptorium.models import REPO_ROOT, content_hash, dump_frontmatter, parse_note, slugify

DIMENSIONS = ("conceptual", "mathematical", "algorithmic", "implementation", "research", "visual", "analytical")
LEVELS = {"omitted": 0, "orientation": 1, "working": 2, "advanced": 3, "comprehensive": 4, "research": 5}
FIVE_KEYS = {"id", "aliases", "topic", "tags", "nexttopics"}
PROFILE = "comprehensive_multifile"


def capabilities() -> dict[str, Any]:
    from ._instructional import registry
    data = registry()
    return {key: {**deepcopy(data["capability_contract"]), **deepcopy(spec),
                  "explanation_strategy": list(spec["stages"])} for key, spec in data["capabilities"].items()}


def resolve_capabilities(selected: list[str]) -> list[str]:
    """Stable dependency order; reject unknown capabilities and cycles."""
    specs = capabilities()
    result: list[str] = []
    active: set[str] = set()

    def visit(name: str) -> None:
        if name not in specs:
            raise ValueError(f"Unknown capability: {name}")
        if name in active:
            raise ValueError(f"Capability cycle: {name}")
        if name in result:
            return
        active.add(name)
        for dependency in specs[name]["dependencies"]:
            visit(dependency)
        active.remove(name)
        result.append(name)

    for name in selected:
        visit(name)
    return result


def allocate_depth(concept: dict[str, Any], *, source_policy: str) -> dict[str, Any]:
    """Independent ordinal obligations; inputs are reasoned decisions, not magic scores."""
    depth = {d: 0 for d in DIMENSIONS}
    reasons = {d: [] for d in DIMENSIONS}
    requested = concept.get("depth", {})
    if set(requested) - set(DIMENSIONS):
        raise ValueError("Unknown depth dimension")
    for dim, level in requested.items():
        value = LEVELS.get(level, level) if isinstance(level, str) else level
        if type(value) is not int or not 0 <= value <= 5:
            raise ValueError(f"Invalid depth for {dim}")
        depth[dim] = value
        reasons[dim].append("explicit concept requirement")
    for goal in concept.get("objectives", []):
        mappings = {"explain": ("conceptual", 2), "derive": ("mathematical", 3),
                    "prove": ("mathematical", 5), "trace": ("algorithmic", 3),
                    "implement": ("implementation", 3), "compare": ("analytical", 3),
                    "analyze": ("analytical", 3), "visualize": ("visual", 2)}
        verb = goal.split()[0].lower()
        if verb in mappings:
            dim, minimum = mappings[verb]
            depth[dim] = max(depth[dim], minimum)
            reasons[dim].append(f"learning objective: {goal}")
    signals = concept.get("signals", {})
    for flag, dim, minimum in (("difficult", "conceptual", 3), ("missing_prerequisite", "conceptual", 3),
                               ("conflicting_evidence", "research", 4), ("novel", "research", 3),
                               ("high_consequence", "research", 4), ("spatial", "visual", 2)):
        if signals.get(flag):
            depth[dim] = max(depth[dim], minimum)
            reasons[dim].append(flag)
    # Research effort is separate from permission to retrieve externally.
    return {"levels": depth, "reasons": reasons,
            "external_retrieval_permitted": source_policy != "strict",
            "unresolved": ["source gap: external retrieval prohibited"]
            if source_policy == "strict" and signals.get("source_gap") else []}


def build_composition(spec: dict[str, Any]) -> dict[str, Any]:
    """Validate one common concept/chapter/notation/evidence plan before authoring."""
    topic = str(spec.get("topic", "")).strip()
    if not topic:
        raise ValueError("A topic is required")
    policy = spec.get("source_policy", "adaptive")
    if policy not in {"strict", "source_first", "adaptive"}:
        raise ValueError("Invalid source policy")
    chapters = deepcopy(spec.get("chapters", []))
    concepts = deepcopy(spec.get("concepts", []))
    if len(chapters) != 5:
        raise ValueError("Comprehensive output requires five chapters; revise scope before exceeding it")
    ids = [c["id"] for c in concepts]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError("Concept identities must be nonempty and unique")
    chapter_ids = [c["id"] for c in chapters]
    if len(set(chapter_ids)) != 5:
        raise ValueError("Chapter identities must be unique")
    order: dict[str, int] = {}
    seen: set[str] = set()
    folder = f"6 - Full Notes/{safe_title(topic)}"
    for i, chapter in enumerate(chapters, 1):
        title = safe_title(chapter["title"])
        chapter["path"] = f"{folder}/{i:02d} - {title}.md"
        if not chapter.get("concepts"):
            raise ValueError("Each chapter needs owned concepts")
        for cid in chapter["concepts"]:
            if cid not in ids or cid in seen:
                raise ValueError(f"Unknown or multiply owned concept: {cid}")
            seen.add(cid)
            order[cid] = i
    if seen != set(ids):
        raise ValueError("Every concept needs exactly one chapter owner")
    processed: set[str] = set()
    ordered = {c["id"]: c for c in concepts}
    specs = capabilities()
    # Order within chapters is explicit, and prerequisites must be earlier.
    for cid in [cid for chapter in chapters for cid in chapter["concepts"]]:
        concept = ordered[cid]
        if not concept.get("objectives") or not concept.get("title"):
            raise ValueError(f"Concept needs a title and learning objectives: {cid}")
        for dep in concept.get("prerequisites", []):
            if dep not in processed and (dep in ordered or dep not in spec.get("known_prerequisites", [])):
                raise ValueError(f"Missing, cyclic, or forward prerequisite: {dep}")
        concept["chapter"] = order[cid]
        concept["depth_allocation"] = allocate_depth(concept, source_policy=policy)
        selected = resolve_capabilities(concept.get("capabilities", ["S01"]))
        concept["capabilities"] = selected
        # Each stage has one primary owner and all unique obligations survive.
        contributions: dict[str, dict[str, Any]] = {}
        for cap in selected:
            for stage in specs[cap]["stages"]:
                contribution = contributions.setdefault(stage, {"owner": cap, "contributors": [], "obligations": []})
                contribution["contributors"].append(cap)
                for obligation in specs[cap]["technical_obligations"]:
                    if obligation not in contribution["obligations"]:
                        contribution["obligations"].append(obligation)
        from ._instructional import STAGE_ORDER
        concept["sequence"] = [{"stage": s, **contributions[s]} for s in STAGE_ORDER if s in contributions]
        concept["research_obligations"] = [
            {"id": f"{cid}:{cap}:{i}", "concept": cid, "capability": cap,
             "requirement": requirement, "source_policy": policy, "status": "pending",
             "research_depth": concept["depth_allocation"]["levels"]["research"],
             "primary_required": cap == "S06", "freshness_required": cap == "S04"}
            for cap in selected for i, requirement in enumerate(specs[cap]["evidence_requirements"])
        ]
        processed.add(cid)
    for table in spec.get("tables", []):
        if table.get("concept") not in ordered or not table.get("section"):
            raise ValueError("Table requires concept ownership and a planned section")
        if "rows" in table:
            render_table(table)
    for visual in spec.get("visuals", []):
        if visual.get("concept") not in ordered or not visual.get("section"):
            raise ValueError("Visual requires concept ownership and a planned section")
        select_visual(visual, available=set(spec.get("available_renderers", [])))
    return {"version": 1, "output_profile": PROFILE, "topic": topic, "source_policy": policy,
            "folder": folder, "moc_path": f"{folder}/00 - Map of Contents.md",
            "chapters": chapters, "concepts": list(ordered.values()),
            "notation": deepcopy(spec.get("notation", {})),
            "visuals": deepcopy(spec.get("visuals", [])), "tables": deepcopy(spec.get("tables", [])),
            "spec_hash": content_hash(json.dumps(spec, sort_keys=True)),
            "review_required": ["factual_accuracy", "derivation_correctness", "reader_simulation", "cross_chapter_coherence"]}


def safe_title(title: str) -> str:
    if not isinstance(title, str) or not title.strip() or re.search(r'[<>:"/\\|?*\x00-\x1f]', title) or title.strip() in {".", ".."}:
        raise ValueError(f"Unsafe title: {title!r}")
    clean = title.strip().rstrip(". ")
    if not clean or re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", clean, re.I):
        raise ValueError("Reserved filename")
    return clean


def to_collection_plan(composition: dict[str, Any]):
    """Use the existing NoteCollectionPlan transport and KCP lifecycle."""
    from ._interactive import NoteCollectionPlan, TopicNode
    root = f"topic.{slugify(composition['topic'])}"
    nodes = [TopicNode(root, composition["topic"], None, proposed_path=composition["moc_path"], note_role="root_index")]
    for chapter in composition["chapters"]:
        nodes.append(TopicNode(chapter["id"], chapter["title"], root, proposed_path=chapter["path"],
                               note_role="child", template_plan={"master": "M1", "concepts": chapter["concepts"]}))
    nodes[0].child_ids = [n.concept_id for n in nodes[1:]]
    return NoteCollectionPlan(f"col-{slugify(composition['topic'])}", composition["topic"], root,
                              "hierarchical_collection", nodes, [n.proposed_path for n in nodes],
                              nodes[0].child_ids, [*nodes[0].child_ids, root],
                              {"output_profile": PROFILE, "composition": composition})


def evidence_status(obligations: list[dict[str, Any]], evidence: dict[str, Any]) -> dict[str, Any]:
    """Evidence assertions need a location, provenance, policy, and no open contradiction.

    Verification is supplied by ARRIE or a reviewer; this function never verifies URLs.
    """
    pending = []
    for obligation in obligations:
        record = evidence.get(obligation["id"], {})
        valid = (record.get("verified") is True and bool(record.get("source"))
                 and bool(record.get("location")) and not record.get("contradictions"))
        if obligation["source_policy"] == "strict":
            valid = valid and record.get("origin") == "supplied"
        if obligation.get("primary_required"):
            valid = valid and record.get("primary") is True
        if obligation.get("freshness_required"):
            valid = valid and bool(record.get("checked_at")) and bool(record.get("version"))
        if not valid:
            pending.append(obligation["id"])
    return {"sufficient": not pending, "pending": pending, "stop_retrieval": not pending,
            "escalate": [oid for oid in pending if evidence.get(oid, {}).get("contradictions")]}


TABLE_TYPES = {
    "definition": ["term", "meaning"], "variable": ["symbol", "meaning", "domain", "units"],
    "comparison": ["method", "criterion", "value", "conditions", "source"],
    "execution": ["step", "state", "output"], "complexity": ["method", "time", "space", "assumptions"],
    "experimental": ["method", "metric", "value", "units", "conditions", "source", "uncertainty"],
    "architecture": ["component", "input", "output", "operation"],
    "failure": ["symptom", "cause", "diagnosis", "correction"],
    "decision": ["constraint", "alternative", "tradeoff"], "evidence": ["claim", "source", "location"],
    "prerequisite": ["concept", "dependency", "knowledge"],
    "formula": ["formula", "symbols", "assumptions", "applicability"],
}


def render_table(table: dict[str, Any]) -> str:
    columns = TABLE_TYPES.get(table.get("type"))
    if not columns or not table.get("objective") or not table.get("interpretation"):
        raise ValueError("Table needs a supported type, learning objective, and prose interpretation")
    rows = table.get("rows", [])
    if not rows:
        raise ValueError("Table needs rows")
    for row in rows:
        for column in columns:
            value = row.get(column)
            if value is None or not str(value).strip():
                raise ValueError(f"Missing {column}; use an explained unavailable value")
            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError("Nonfinite table measurement")
            if str(value).lower() in {"fast", "slow", "good", "bad"} or "\n" in str(value) or "```" in str(value):
                raise ValueError("Unqualified or multiline table value")
    if table["type"] in {"comparison", "experimental"}:
        conditions = {str(r["conditions"]) for r in rows}
        metrics = {str(r.get("metric", r.get("criterion"))) for r in rows}
        units = {str(r.get("units")) for r in rows}
        if len(conditions) > 1 or len(metrics) > 1 or len(units) > 1:
            raise ValueError("Incomparable measurement conditions, metrics, or units")
    def cell(value: Any) -> str:
        return str(value).replace("|", "\\|")
    lines = [table["objective"], "", "| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    lines.extend("| " + " | ".join(cell(row[col]) for col in columns) + " |" for row in rows)
    return "\n".join([*lines, "", table["interpretation"]])


def select_visual(requirement: dict[str, Any], *, available: set[str]) -> dict[str, Any]:
    types = {"equation": "scientific", "distribution": "scientific", "workflow": "mermaid",
             "dependency": "mermaid", "state": "mermaid", "tensor": "svg", "architecture": "svg",
             "source_figure": "external", "intuition": "imagegen", "hybrid": "hybrid"}
    if not requirement.get("objective") or requirement.get("kind") not in types:
        raise ValueError("Visual needs a learning objective and supported relationship")
    renderer = types[requirement["kind"]]
    if renderer == "scientific" and not (requirement.get("equation") or requirement.get("data")):
        raise ValueError("Scientific visual requires an equation or reproducible data")
    if renderer == "external" and not all(requirement.get(k) for k in ("source", "url", "rights")):
        raise ValueError("External figure needs source, URL, and usage rights")
    return {**requirement, "renderer": renderer, "status": "planned" if renderer in available else "unavailable",
            "verification_required": True}


def render_moc(plan: dict[str, Any]) -> str:
    lines = [f"# {plan['topic']}", "", "## Learning path", ""]
    lines.extend(f"{i}. [[{Path(c['path']).stem}]]" for i, c in enumerate(plan["chapters"], 1))
    lines += ["", "## Concept prerequisites", "", "```mermaid", "flowchart TD"]
    ids = {c["id"]: f"n{i}" for i, c in enumerate(plan["concepts"])}
    for concept in plan["concepts"]:
        label = concept["title"].replace('"', "&quot;").replace("\n", " ").replace("<", "&lt;")
        lines.append(f'    {ids[concept["id"]]}["{label}"]')
        for dep in concept.get("prerequisites", []):
            if dep in ids:
                lines.append(f'    {ids[dep]} --> {ids[concept["id"]]}')
    return "\n".join([*lines, "```", ""])


def five_key_note(plan: dict[str, Any], identifier: str, title: str, body: str, next_title: str | None) -> str:
    return dump_frontmatter({"id": identifier, "aliases": [title], "topic": plan["topic"],
                             "tags": ["type/full-notes"],
                             "nexttopics": [f"[[{next_title}]]"] if next_title else []}) + "\n" + body.strip() + "\n"


def validate_chapter(text: str, *, required_sections: list[str] | None = None) -> list[str]:
    errors = []
    note = parse_note(text)
    if set(note.metadata) != FIVE_KEYS:
        errors.append("frontmatter must contain exactly the five profile keys")
    for key in ("id", "topic"):
        if not isinstance(note.metadata.get(key), str) or not note.metadata[key].strip():
            errors.append(f"invalid {key}")
    for key in ("aliases", "tags", "nexttopics"):
        value = note.metadata.get(key)
        if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
            errors.append(f"invalid {key}")
    if re.search(r"\b(?:TODO|TBD|FIXME)\b|<!--\s*(?:scaffold|temporary)|\[placeholder\]", text, re.I):
        errors.append("unfinished content")
    fence: tuple[str, int] | None = None
    prose_lines = []
    for line in note.body.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if match:
            token, suffix = match.groups()
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1] and not suffix.strip():
                fence = None
        elif fence is None:
            prose_lines.append(line)
    if fence:
        errors.append("unclosed code fence")
    prose = "\n".join(prose_lines)
    if prose.count("$$") % 2:
        errors.append("unclosed display mathematics")
    for section in required_sections or []:
        if section not in [s.heading.lstrip("# ") for s in note.sections]:
            errors.append(f"missing planned section: {section}")
    return errors


def contained(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Path escapes vault")
    return path


def publish_composition(vault: Path, plan: dict[str, Any], drafts: dict[str, str], *,
                        evidence: dict[str, Any], reviews: dict[str, str],
                        expected_hashes: dict[str, str] | None = None) -> dict[str, Any]:
    """Preflight whole collection; checkpoint individual atomic writes using E6.

    No overwrite without a matching expected digest. Human/model review is explicit
    evidence, not a deterministic quality score. Internal state stays outside topics.
    """
    from .vault import safe_write_note
    plan = deepcopy(plan)
    obligations = [o for c in plan["concepts"] for o in c["research_obligations"]]
    status = evidence_status(obligations, evidence)
    errors = [f"pending evidence: {oid}" for oid in status["pending"]]
    errors.extend(f"missing review: {r}" for r in plan["review_required"] if not reviews.get(r))
    documents = {}
    asset_hashes = {}
    for i, chapter in enumerate(plan["chapters"]):
        body = drafts.get(chapter["id"], "")
        if not body.strip():
            errors.append(f"missing authored chapter: {chapter['id']}")
        next_title = Path(plan["chapters"][i + 1]["path"]).stem if i + 1 < len(plan["chapters"]) else None
        text = five_key_note(plan, chapter["id"], chapter["title"], body, next_title)
        errors.extend(f"{chapter['id']}: {e}" for e in validate_chapter(text, required_sections=chapter.get("sections")))
        documents[chapter["path"]] = text
    documents[plan["moc_path"]] = five_key_note(plan, f"{slugify(plan['topic'])}.moc", "Map of Contents", render_moc(plan), Path(plan["chapters"][0]["path"]).stem)
    planned = {Path(p).stem for p in documents}
    current_hashes = {}
    for relative, text in documents.items():
        target = contained(vault, relative)
        current_hashes[relative] = content_hash(target.read_text(encoding="utf-8-sig")) if target.exists() else None
        if target.exists() and target.read_text(encoding="utf-8-sig") != text and (expected_hashes or {}).get(relative) != current_hashes[relative]:
            errors.append(f"existing chapter needs expected digest: {relative}")
        for target_link in re.findall(r"(?<!!)\[\[([^\]|#]+)(?:[^\]]*)\]\]", text):
            if target_link not in planned and not contained(vault, target_link + ".md").is_file():
                errors.append(f"unresolved wikilink: {target_link}")
        for asset in re.findall(r"!\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", text):
            if not contained(vault, asset).is_file():
                errors.append(f"missing asset: {asset}")
            else:
                asset_hashes[asset] = content_hash(contained(vault, asset).read_bytes())
    if errors:
        return {"complete": False, "errors": errors, "written_paths": []}
    state_path = contained(vault, f".scriptorium/collections/col-{slugify(plan['topic'])}.json")
    state = {"composition": plan, "spec_hash": plan["spec_hash"], "evidence": evidence, "reviews": reviews,
             "checkpoints": {}, "asset_hashes": asset_hashes, "complete": False, "errors": []}
    state_path.parent.mkdir(parents=True, exist_ok=True)
    written = []
    def checkpoint() -> None:
        safe_write_note(state_path, json.dumps(state, indent=2, ensure_ascii=False), validate_properties=False)
    for relative, text in documents.items():
        try:
            result = safe_write_note(contained(vault, relative), text, expected_digest=current_hashes[relative], validate_properties=False)
            state["checkpoints"][relative] = {"hash": content_hash(text), "status": "COMMITTED"}
            if result["written"]:
                written.append(relative)
            checkpoint()
        except (OSError, ValueError) as exc:
            state["errors"].append(f"{relative}: {exc}")
            checkpoint()
            return {**state, "written_paths": written}
    state["complete"] = True
    checkpoint()
    return {**state, "written_paths": written}


def inventory_migration(vault: Path, paths: list[str]) -> dict[str, Any]:
    """Non-destructive migration evidence. No claim that consolidation is lossless."""
    files = []
    for relative in paths:
        path = contained(vault, relative)
        text = path.read_text(encoding="utf-8-sig")
        files.append({"path": relative, "hash": content_hash(text), "content": text,
                      "links": re.findall(r"!?\[\[([^\]]+)\]\]", text),
                      "code_blocks": len(parse_note(text).code_blocks)})
    backlinks = {}
    stems = {Path(p).stem for p in paths}
    for path in vault.rglob("*.md"):
        if path.is_symlink() or not path.resolve().is_relative_to(vault.resolve()):
            continue
        matches = stems.intersection(re.findall(r"\[\[([^\]|#]+)", path.read_text(encoding="utf-8-sig")))
        if matches:
            backlinks[path.relative_to(vault).as_posix()] = sorted(matches)
    return {"files": files, "backlinks": backlinks, "deletion_permitted": False,
            "status": "inventory_only", "required_next": ["chapter_mapping", "backup", "coverage_review", "backlink_repair", "approval_to_remove_originals"]}


def validate_published_composition(vault: Path, plan: dict[str, Any]) -> dict[str, Any]:
    """Detect changed reviewed artifacts, missing files/assets, and dirty topic folders."""
    manifest = contained(vault, f".scriptorium/collections/col-{slugify(plan['topic'])}.json")
    if not manifest.is_file():
        return {"valid": False, "errors": ["missing composition manifest"]}
    state = json.loads(manifest.read_text(encoding="utf-8"))
    errors = []
    if state.get("spec_hash") != plan["spec_hash"]:
        errors.append("composition specification changed; dependent checks must rerun")
    if not state.get("complete"):
        errors.append("incomplete publication checkpoint")
    paths = [plan["moc_path"], *[c["path"] for c in plan["chapters"]]]
    names = {Path(p).stem for p in paths}
    for relative in paths:
        path = contained(vault, relative)
        if not path.is_file():
            errors.append(f"missing chapter: {relative}")
            continue
        text = path.read_text(encoding="utf-8-sig")
        errors.extend(f"{relative}: {e}" for e in validate_chapter(text))
        checkpoint = state.get("checkpoints", {}).get(relative, {})
        if content_hash(text) != checkpoint.get("hash"):
            errors.append(f"chapter changed since review: {relative}")
        for link in re.findall(r"(?<!!)\[\[([^\]|#]+)(?:[^\]]*)\]\]", text):
            if link not in names and not contained(vault, link + ".md").is_file():
                errors.append(f"unresolved wikilink: {link}")
        for asset in re.findall(r"!\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", text):
            if not contained(vault, asset).is_file():
                errors.append(f"missing asset: {asset}")
            elif content_hash(contained(vault, asset).read_bytes()) != state.get("asset_hashes", {}).get(asset):
                errors.append(f"asset changed since review: {asset}")
    folder = contained(vault, plan["folder"])
    if folder.is_dir() and {p.name for p in folder.iterdir()} != {Path(p).name for p in paths}:
        errors.append("topic folder must contain only the six planned Markdown files")
    obligations = [o for c in plan["concepts"] for o in c["research_obligations"]]
    if not evidence_status(obligations, state.get("evidence", {}))["sufficient"]:
        errors.append("evidence is no longer sufficient")
    return {"valid": not errors, "errors": errors, "review_scope": "structural and recorded evidence; semantic review is separate"}
