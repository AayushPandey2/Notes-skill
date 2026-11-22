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
from urllib.parse import unquote, urlsplit

from scriptorium.models import REPO_ROOT, content_hash, dump_frontmatter, parse_note, slugify

DIMENSIONS = ("conceptual", "mathematical", "algorithmic", "implementation", "research", "visual", "analytical")
LEVELS = {"omitted": 0, "orientation": 1, "working": 2, "advanced": 3, "comprehensive": 4, "research": 5}
FIVE_KEYS = {"id", "aliases", "topic", "tags", "nexttopics"}
PROFILE = "comprehensive_multifile"


def capabilities() -> dict[str, Any]:
    from .._instructional import registry
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
        from .contracts import objective_kind
        mappings = {"explain": ("conceptual", 2), "derive": ("mathematical", 3),
                    "prove": ("mathematical", 5),
                    "implement": ("implementation", 3), "compare": ("analytical", 3),
                    "analyze": ("analytical", 3), "visualize": ("visual", 2)}
        verb = goal.split()[0].lower()
        if verb in mappings:
            dim, minimum = mappings[verb]
            depth[dim] = max(depth[dim], minimum)
            reasons[dim].append(f"learning objective: {goal}")
        kind = objective_kind(goal, concept.get("objective_kinds", {}).get(str(concept["objectives"].index(goal))))
        semantic_depth = {"historical": ("conceptual", 2), "algorithmic": ("algorithmic", 3),
                          "mathematical": ("mathematical", 3), "implementation": ("implementation", 3),
                          "reproduction": ("research", 4)}
        if kind in semantic_depth:
            dim, minimum = semantic_depth[kind]
            depth[dim] = max(depth[dim], minimum)
            reasons[dim].append(f"semantic objective ({kind}): {goal}")
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
    if not isinstance(spec, dict):
        raise ValueError("Composition specification must be a JSON object")
    topic = str(spec.get("topic", "")).strip()
    if not topic:
        raise ValueError("A topic is required")
    policy = spec.get("source_policy", "adaptive")
    if policy not in {"strict", "source_first", "adaptive"}:
        raise ValueError("Invalid source policy")
    chapters = deepcopy(spec.get("chapters", []))
    concepts = deepcopy(spec.get("concepts", []))
    if not isinstance(concepts, list) or any(not isinstance(c, dict) or not isinstance(c.get("id"), str) or not c["id"].strip() for c in concepts):
        raise ValueError("Concepts must be records with nonempty string IDs")
    for concept in concepts:
        for field in ("title", "section"):
            value = concept.get(field, concept.get("title"))
            if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
                raise ValueError(f"Concept needs a nonempty single-line {field}")
        objectives = concept.get("objectives")
        if not isinstance(objectives, list) or not objectives or any(not isinstance(o, str) or not o.strip() for o in objectives):
            raise ValueError("Concept objectives must be a nonempty list of nonempty strings")
        if not isinstance(concept.get("prerequisites", []), list):
            raise ValueError("Concept prerequisites must be a list")
    notation = spec.get("notation", {})
    if not isinstance(notation, dict) or any(not isinstance(symbol, str) or not symbol.strip() or not isinstance(meaning, str) or not meaning.strip() for symbol, meaning in notation.items()):
        raise ValueError("notation must map nonempty symbols to nonempty definitions")
    if "chapters" not in spec:
        from .planning import plan_chapters
        allocation = plan_chapters(concepts, known_prerequisites=spec.get("known_prerequisites", []))
        chapters = allocation["chapters"]
        rationale = allocation["rationale"]
    else:
        rationale = {"method": "explicit author allocation", "reason": spec.get("chapter_rationale", "Author-supplied grouping; review workload and continuity before publication"),
                     "chapter_count": len(chapters) if isinstance(chapters, list) else 0}
    if not isinstance(chapters, list) or not 5 <= len(chapters) <= 10:
        raise ValueError("Comprehensive output requires 5–10 substantive chapters plus a separate MOC")
    if any(not isinstance(c, dict) or not isinstance(c.get("id"), str) or not c["id"].strip() for c in chapters):
        raise ValueError("Chapters must be records with nonempty string IDs")
    ids = [c["id"] for c in concepts]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError("Concept identities must be nonempty and unique")
    chapter_ids = [c["id"] for c in chapters]
    if len(set(chapter_ids)) != len(chapters):
        raise ValueError("Chapter identities must be unique")
    order: dict[str, int] = {}
    seen: set[str] = set()
    publishing = spec.get("publishing") or {}
    folder, moc_path, chapter_prefix = resolve_collection_layout(
        topic,
        collection_layout=publishing.get("collection_layout", "topic_folder_under_vault"),
        create_category_folders=bool(publishing.get("create_category_folders", False)),
        category_folder=publishing.get("category_folder"),
        vault_root=spec.get("vault_root"),
    )
    for i, chapter in enumerate(chapters, 1):
        title = safe_title(chapter["title"])
        if chapter_prefix:
            chapter["path"] = f"{chapter_prefix} - {i:02d} - {title}.md"
        else:
            chapter["path"] = f"{folder}/{i:02d} - {title}.md"
        if not isinstance(chapter.get("concepts"), list) or not chapter["concepts"] or any(not isinstance(cid, str) for cid in chapter["concepts"]):
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
        from .contracts import PREREQUISITES
        records = []
        for dependency in concept.get("prerequisites", []):
            record = deepcopy(dependency) if isinstance(dependency, dict) else {
                "id": dependency, "classification": "covered" if dependency in ordered else "assumed"}
            if record.get("classification") not in PREREQUISITES or not record.get("id"):
                raise ValueError("Invalid classified prerequisite")
            records.append(record)
        concept["prerequisite_records"] = records
        concept["prerequisites"] = [r["id"] for r in records if r["id"] in ordered]
        for record in records:
            dep = record["id"]
            if record["classification"] in {"missing", "optional"} and dep not in ordered:
                continue
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
        from .._instructional import STAGE_ORDER
        concept["sequence"] = [{"stage": s, **contributions[s]} for s in STAGE_ORDER if s in contributions]
        concept["research_obligations"] = [
            {"id": f"{cid}:{cap}:{i}", "concept": cid, "capability": cap,
             "requirement": requirement, "source_policy": policy, "status": "planned", "exact_evidence": True,
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
    visuals = []
    for visual in spec.get("visuals", []):
        if visual.get("kind") == "hybrid":
            if not visual.get("parts") or not visual.get("objective"):
                raise ValueError("Hybrid representation needs a shared objective and complementary parts")
            for i, part in enumerate(visual["parts"]):
                if part.get("kind") == "hybrid":
                    raise ValueError("Nested hybrid specifications are unnecessary; list complementary representations")
                visuals.append({"concept": visual["concept"], "section": visual["section"],
                                "id": f"{visual.get('id', visual['concept']+':hybrid')}:{i}",
                                "hybrid_objective": visual["objective"], **deepcopy(part)})
        else:
            visuals.append(deepcopy(visual))
    for visual in visuals:
        if visual.get("concept") not in ordered or not visual.get("section"):
            raise ValueError("Visual requires concept ownership and a planned section")
        select_visual(visual, available=set(spec.get("available_renderers", [])))
    from .contracts import extend_plan
    validator_files = [*Path(__file__).parent.glob("*.py"),
                       Path(__file__).parents[1]/"quality.py", Path(__file__).parents[1]/"_instructional.py",
                       Path(__file__).parents[1]/"vault.py",
                       REPO_ROOT/"references/workflows/notes-creation/instructional-registry.json"]
    validator_version = content_hash("".join(content_hash(p.read_text(encoding="utf-8")) for p in sorted(validator_files)))
    from ..vault import classify_knowledge_hierarchy
    classification = spec.get("classification", {})
    if not isinstance(classification, dict):
        raise ValueError("classification must be an object with optional subject/domain/subdomain")
    if any(not isinstance(value, str) or not value.strip() for value in classification.values()):
        raise ValueError("classification values must be nonempty strings")
    hierarchy = classify_knowledge_hierarchy(topic, content=" ".join(c["title"] for c in concepts),
        explicit_domain=classification.get("domain"), explicit_master_topic=classification.get("subject"),
        explicit_subdomain=classification.get("subdomain"))
    plan_payload: dict[str, Any] = {
        "version": 2,
        "validator_version": validator_version,
        "output_profile": PROFILE,
        "topic": topic,
        "source_policy": policy,
        "classification": hierarchy,
        "chapter_rationale": rationale,
        "folder": folder,
        "moc_path": moc_path,
        "chapters": chapters,
        "concepts": list(ordered.values()),
        "notation": deepcopy(spec.get("notation", {})),
        "visuals": visuals,
        "tables": deepcopy(spec.get("tables", [])),
        "spec_hash": content_hash(json.dumps(spec, sort_keys=True)),
        "review_required": ["factual_accuracy", "derivation_correctness", "reader_simulation", "cross_chapter_coherence"],
    }
    for key in ("web_image_first", "collection_slug", "organize_by_collection", "embed_style", "learner_level", "enforce_bvia_walkthrough"):
        if key in spec and spec[key] is not None:
            plan_payload[key] = spec[key]
    if plan_payload.get("organize_by_collection") and not plan_payload.get("collection_slug"):
        plan_payload["collection_slug"] = slugify(topic)
    plan = extend_plan(plan_payload, spec)
    from . import bvia, lavia
    plan["visual_coverage"] = lavia.plan_visual_coverage(plan)
    if plan.get("learner_level") and plan.get("visuals"):
        plan["progressive_visual_order"] = [v["id"] for v in bvia.plan_progressive_visuals(plan["visuals"])]
    return plan


def resolve_collection_layout(
    topic: str,
    *,
    collection_layout: str = "topic_folder_under_vault",
    create_category_folders: bool = False,
    category_folder: str | None = None,
    vault_root: str | Path | None = None,
) -> tuple[str, str, str | None]:
    """Resolve vault-relative collection folder and MOC path without automatic category dirs.

    Returns `(folder, moc_path, flat_prefix)`.
    """
    topic_name = safe_title(topic)
    if collection_layout == "flat_root":
        return "", f"{topic_name} - 00 - Map of Contents.md", topic_name
    if collection_layout != "topic_folder_under_vault":
        raise ValueError(f"Unsupported collection_layout: {collection_layout}")

    if create_category_folders and category_folder:
        cat_name = safe_title(category_folder)
        if vault_root and Path(vault_root).name.casefold() == cat_name.casefold():
            folder = topic_name
        else:
            folder = f"{cat_name}/{topic_name}"
    else:
        folder = topic_name
    return folder, f"{folder}/00 - Map of Contents.md", None


def safe_title(title: str) -> str:
    if not isinstance(title, str) or not title.strip() or re.search(r'[<>:"/\\|?*\x00-\x1f]', title) or title.strip() in {".", ".."}:
        raise ValueError(f"Unsafe title: {title!r}")
    clean = title.strip().rstrip(". ")
    if not clean or re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", clean, re.I):
        raise ValueError("Reserved filename")
    return clean


def to_collection_plan(composition: dict[str, Any]):
    """Use the existing NoteCollectionPlan transport and KCP lifecycle."""
    from .._interactive import NoteCollectionPlan, TopicNode
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
        if obligation.get("exact_evidence"):
            valid = valid and all(record.get(k) for k in ("claim", "classification", "version", "verification_method", "limits"))
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
    "failure": ["symptom", "latent_property", "candidate_cause", "diagnostic", "evidence_status", "remediation"],
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
    from .renderers import select_representation
    return select_representation(requirement, available=available)


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
    lines += ["```", "", "| Concept | Canonical chapter | Prerequisites |", "|---|---|---|"]
    owners = {cid: chapter for chapter in plan["chapters"] for cid in chapter["concepts"]}
    titles_by_id = {c["id"]: c["title"] for c in plan["concepts"]}
    for concept in plan["concepts"]:
        chapter = owners[concept["id"]]
        prereq_labels = [
            titles_by_id[r["id"]] if r["id"] in titles_by_id else r["id"].replace("_", " ")
            for r in concept.get("prerequisite_records", [])
        ]
        prerequisites = ", ".join(prereq_labels) or "none"
        lines.append(f"| {concept['title']} | [[{Path(chapter['path']).stem}#{concept.get('section', chapter['title'])}|{chapter['title']}]] | {prerequisites} |")
    return "\n".join([*lines, ""])


def five_key_note(plan: dict[str, Any], identifier: str, title: str, body: str, next_title: str | None) -> str:
    from ..vault import classify_knowledge_hierarchy, generate_tags
    hierarchy = plan.get("classification") or classify_knowledge_hierarchy(plan["topic"], content=body)
    chapter = next((c for c in plan["chapters"] if c["id"] == identifier), None)
    concepts = [c for c in plan["concepts"] if chapter and c["id"] in chapter["concepts"]]
    primary = concepts[0]["title"] if concepts else plan["topic"]
    tags = generate_tags(topic=primary, domain=hierarchy["domain"], master_topic=hierarchy["master_topic"],
                         subdomain=hierarchy.get("subdomain", ""), note_type="deep-notes",
                         secondary_concepts=[c["title"] for c in concepts[1:]])
    tags = [t for t in tags if not t.startswith("type/")] + ["type/full-notes"]
    return dump_frontmatter({"id": identifier, "aliases": [title], "topic": plan["topic"],
                             "tags": tags,
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
    from ..vault import validate_semantic_tags
    errors.extend(validate_semantic_tags(note.metadata.get("tags")))
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
    prose_no_inline = re.sub(r"`[^`\n]*`", "", prose)
    has_tab_in_math = any("\t" in m.group(1) for m in re.finditer(r"\$\$(.*?)\$\$", prose_no_inline, re.S))
    if not has_tab_in_math:
        prose_no_display = re.sub(r"\$\$.*?\$\$", "", prose_no_inline, flags=re.S)
        has_tab_in_math = any(
            "\t" in m.group(1)
            for m in re.finditer(r"(?<!\\)\$(?!\$)([^$\n]+?)(?<!\\)\$", prose_no_display)
        )
    if has_tab_in_math:
        errors.append("raw TAB character inside LaTeX math span")
    nonempty_prose = [line.strip() for line in prose_lines if line.strip()]
    for prev_line, next_line in zip(nonempty_prose, nonempty_prose[1:]):
        m1 = re.match(r"^#\s+(.+?)\s*$", prev_line)
        m2 = re.match(r"^##\s+(.+?)\s*$", next_line)
        if m1 and m2 and m1.group(1).strip().casefold() == m2.group(1).strip().casefold():
            errors.append(f"duplicate immediate H1/H2 heading: {m1.group(1).strip()}")
            break
    if re.search(
        r"\b[a-z][a-z0-9_-]*(?:\.[a-z0-9_-]+)+\s*\((?:covered|assumed|missing|essential|supporting|optional)\)"
        r"|\b[a-z]+\d+\s*\((?:covered|assumed|missing|essential|supporting|optional)\)",
        prose_no_inline,
        re.I,
    ):
        errors.append("leaked internal concept/prerequisite ID")
    if re.search(r"^\s*\*Key mathematical claim:\*", prose_no_inline, re.M):
        errors.append("leaked internal claim stub '*Key mathematical claim:*'")
    for section in required_sections or []:
        if section not in [s.heading.lstrip("# ") for s in note.sections]:
            errors.append(f"missing planned section: {section}")
    return errors


def contained(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Path escapes vault")
    return path


def wikilink_errors(vault: Path, documents: dict[str, str]) -> list[str]:
    """Resolve collection paths and heading/block anchors against the actual artifacts."""
    errors = []
    aliases = {alias: path for path in documents for alias in (Path(path).stem, path.removesuffix(".md"), path)}
    for relative, text in documents.items():
        # The shared parser excludes fenced code; an example of a link is not a link obligation.
        for link in parse_note(text).wikilinks:
            if link.split("#", 1)[0].split(".")[-1] in {"svg", "png", "jpg", "pdf", "webp"}:
                continue
            name, _, anchor = link.partition("#")
            destination = aliases.get(name, relative if not name else None)
            if destination is not None:
                target_text = documents[destination]
            else:
                path = contained(vault, name if name.endswith(".md") else name+".md")
                if not path.is_file():
                    errors.append(f"unresolved wikilink: {link}")
                    continue
                target_text = path.read_text(encoding="utf-8-sig")
            if anchor:
                target_note = parse_note(target_text)
                headings = {s.heading for s in target_note.sections} | {target_note.title}
                found = bool(re.search(r"\^"+re.escape(anchor[1:])+r"\s*$", target_text, re.M)) if anchor.startswith("^") else anchor in headings
                if not found:
                    errors.append(f"unresolved wikilink anchor: {link}")
    return errors


def markdown_image_targets(prose: str) -> list[tuple[str, str]]:
    """Read balanced/escaped alt labels and direct or reference image targets."""
    references = {}
    for match in re.finditer(r"^ {0,3}\[([^\]\n]+)\]:\s*(?:<([^>\n]+)>|(\S+))", prose, re.M):
        references[" ".join(match[1].split()).casefold()] = match[2] or match[3]
    images, cursor = [], 0
    while (start := prose.find("![", cursor)) >= 0:
        if prose.startswith("![[", start):
            cursor = start + 3  # Native wiki embeds are checked separately.
            continue
        if start and prose[start - 1] == "\\":
            cursor = start + 2
            continue
        index, depth = start + 2, 1
        while index < len(prose) and depth:
            if prose[index] == "\\":
                index += 2
                continue
            if prose[index] == "[": depth += 1
            if prose[index] == "]": depth -= 1
            index += 1
        if depth:
            raise ValueError("unclosed Markdown image label")
        label, after = prose[start + 2:index - 1], index
        if index < len(prose) and prose[index] == "(":
            index += 1
            begin, nesting = index, 1
            while index < len(prose) and nesting:
                if prose[index] == "\\":
                    index += 2
                    continue
                if prose[index] == "(": nesting += 1
                if prose[index] == ")": nesting -= 1
                index += 1
            if nesting:
                raise ValueError("unclosed Markdown image target")
            value = prose[begin:index - 1].strip()
            target = value[1:value.index(">")] if value.startswith("<") and ">" in value else value.split(maxsplit=1)[0] if value else ""
        else:
            if index < len(prose) and prose[index] == "[":
                end = prose.find("]", index + 1)
                if end < 0:
                    raise ValueError("unclosed Markdown image reference")
                reference, index = prose[index + 1:end] or label, end + 1
            else:
                reference = label
            target = references.get(" ".join(reference.split()).casefold(), "")
            if not target:
                raise ValueError("unresolved Markdown image reference")
        images.append((prose[start:index], re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])", r"\1", target)))
        cursor = max(index, after)
    return images


def inspect_assets(vault: Path, documents: dict[str, str], renderers: dict[str, Any]) -> tuple[list[str], dict[str, str]]:
    """Check actual image targets and hash every renderer artifact and media receipt.

    Remote URLs require the acquisition pipeline's verified snapshot. Validation
    never issues an incidental network request for images found in a note.
    """
    errors, hashes = [], {}
    for result in renderers.values():
        if result.get("status") != "verified":
            continue
        for key in ("path", "media_receipt"):
            relative = result.get(key)
            if not relative:
                continue
            path = contained(vault, relative)
            if not path.is_file():
                errors.append(f"missing renderer artifact: {relative}")
            else:
                hashes[relative] = content_hash(path.read_bytes())
                if key == "path" and hashes[relative] != result.get("hash"):
                    errors.append(f"renderer artifact hash mismatch: {relative}")
    for relative, text in documents.items():
        note = parse_note(text)
        lines = note.body.splitlines()
        for block in note.code_blocks:
            for i in range(block["start_line"], min(len(lines), block["end_line"] + 1)):
                lines[i] = ""
        prose = "\n".join(lines)
        for asset in re.findall(r"!\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", prose):
            path = contained(vault, asset)
            if not path.is_file():
                errors.append(f"missing asset: {asset}")
            else:
                hashes[asset] = content_hash(path.read_bytes())
        try:
            image_targets = markdown_image_targets(prose)
        except ValueError as exc:
            errors.append(str(exc))
            image_targets = []
        for markup, target in image_targets:
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                accepted = parts.scheme == "https" and any(
                    r.get("status") == "verified" and r.get("renderer") == "external"
                    and r.get("embed") in prose and markup in r.get("embed", "")
                    for r in renderers.values()
                )
                if not accepted:
                    errors.append(f"unverified remote image: {target}")
                continue
            name = unquote(parts.path)
            if not name:
                errors.append("empty image target")
                continue
            candidate = (Path(relative).parent / name).as_posix()
            path = contained(vault, candidate)
            if not path.is_file():
                errors.append(f"missing Markdown image asset: {target}")
            else:
                hashes[path.relative_to(vault.resolve()).as_posix()] = content_hash(path.read_bytes())
        for match in re.finditer(r"(?<!!)\[[^\]\n]+\]\(\s*(<[^>\n]+>|[^\s)]+)(?:\s+[^)]*)?\)", prose):
            target = match.group(1).strip("<>")
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            path = contained(vault, (Path(relative).parent / unquote(parts.path)).as_posix())
            if not path.is_file() and path.as_posix() not in {(vault / name).resolve().as_posix() for name in documents}:
                errors.append(f"missing Markdown link target: {target}")
    return errors, hashes


def _validate_local_first_visuals(
    vault: Path,
    plan: dict[str, Any],
    drafts: dict[str, str],
    renderers: dict[str, Any],
    *,
    require_manifest_file: bool = False,
) -> tuple[dict[str, Any], list[str]]:
    from . import bvia, lavia
    manifest = lavia.build_asset_manifest(plan, renderers, collection_slug=plan.get("collection_slug"))
    errors: list[str] = []
    if plan.get("web_image_first") or plan.get("organize_by_collection"):
        lavia_check = lavia.validate_collection_visuals(vault, plan, drafts, manifest)
        errors.extend(lavia_check["errors"])
        for cid, body in drafts.items():
            note = parse_note(body)
            lines = note.body.splitlines()
            for block in note.code_blocks:
                for idx in range(block["start_line"], min(len(lines), block["end_line"] + 1)):
                    lines[idx] = ""
            prose = "\n".join(lines)
            for target in re.findall(r"!\[\[([^\]|#]+)", prose):
                if target.strip().startswith(("http://", "https://")):
                    msg = f"{cid}: remote image URL embed forbidden ({target.strip()})"
                    if msg not in errors:
                        errors.append(msg)
            try:
                for _, target in markdown_image_targets(prose):
                    if target.strip().startswith(("http://", "https://")):
                        msg = f"{cid}: remote image URL embed forbidden ({target.strip()})"
                        if msg not in errors:
                            errors.append(msg)
            except ValueError:
                pass
        if require_manifest_file and (plan.get("organize_by_collection") or plan.get("collection_slug")):
            slug = slugify(plan.get("collection_slug") or plan["topic"])
            rel = f"assets/scriptorium/{slug}/manifest.json"
            if not contained(vault, rel).is_file():
                errors.append(f"missing LAVIA asset manifest: {rel}")
    if plan.get("enforce_bvia_walkthrough") or any(v.get("require_walkthrough") for v in plan.get("visuals", [])):
        owners = {cid: ch["id"] for ch in plan.get("chapters", []) for cid in ch.get("concepts", [])}
        for visual in plan.get("visuals", []):
            if not (plan.get("enforce_bvia_walkthrough") or visual.get("require_walkthrough")):
                continue
            chid = owners.get(visual.get("concept", ""), "")
            check = bvia.validate_explain_show_decode_connect(
                drafts.get(chid, ""),
                visual,
                terminology_registry=plan.get("notation"),
            )
            if not check["passed"]:
                errors.extend(f"{visual['id']}: {e}" for e in check["errors"])
    return manifest, errors


PUBLICATION_READINESS_STATES = (
    "complete",
    "complete_with_justified_omissions",
    "draft",
    "partial",
    "blocked",
    "failed",
)


def _derive_readiness_state(
    *,
    errors: list[str],
    validation: dict[str, Any],
    visual_results: dict[str, Any],
    written_paths: list[str],
) -> str:
    obligations = validation.get("obligations", [])
    has_omissions = any(o.get("status") == "justifiably-omitted" for o in obligations)
    has_unmet_visual = any(v.get("unmet_visual_obligation") for v in visual_results.values())
    if not errors:
        return "complete_with_justified_omissions" if has_omissions else "complete"
    if has_unmet_visual or any(o.get("status") == "blocked" for o in obligations):
        return "partial" if written_paths else "blocked"
    return "draft" if written_paths else "failed"


def publish_composition(vault: Path, plan: dict[str, Any], drafts: dict[str, str], *,
                        evidence: dict[str, Any], reviews: dict[str, Any],
                        expected_hashes: dict[str, str] | None = None,
                        allow_draft: bool = False) -> dict[str, Any]:
    """Preflight whole collection; checkpoint individual atomic writes using E6.

    No overwrite without a matching expected digest. Human/model review is explicit
    evidence, not a deterministic quality score. Internal state stays outside topics.
    """
    from ..vault import safe_write_note
    from .contracts import validate_obligations
    from .._token_optimizer import MultiLevelCache
    from . import lavia
    if not all(isinstance(value, dict) for value in (plan, drafts, evidence, reviews)) or any(not isinstance(body, str) for body in drafts.values()):
        raise ValueError("Plan, drafts, evidence and reviews must be JSON objects; draft bodies must be strings")
    plan = deepcopy(plan)
    if plan.get("version") != 2 or not plan.get("obligations"):
        return {"complete": False, "errors": ["rebuild the composition with executable obligations"], "written_paths": []}
    drafts, visual_results = prepare_composition(vault, plan, drafts)
    cache = MultiLevelCache(disk_dir=contained(vault, ".scriptorium/cache/composition"))
    validation = validate_obligations(plan, drafts, evidence=evidence, reviews=reviews,
                                      visuals=visual_results, vault=vault, cache=cache)
    obligations = [o for c in plan["concepts"] for o in c["research_obligations"]]
    status = evidence_status(obligations, evidence)
    errors = [*validation["errors"], *[f"pending evidence: {oid}" for oid in status["pending"]]]
    semantic_error_count = len(errors)
    documents = {}
    for i, chapter in enumerate(plan["chapters"]):
        body = drafts.get(chapter["id"], "")
        if not body.strip():
            errors.append(f"missing authored chapter: {chapter['id']}")
        next_title = Path(plan["chapters"][i + 1]["path"]).stem if i + 1 < len(plan["chapters"]) else None
        text = five_key_note(plan, chapter["id"], chapter["title"], body, next_title)
        sections = list(dict.fromkeys([*chapter.get("sections", []), *[c.get("section", c["title"]) for c in plan["concepts"] if c["id"] in chapter["concepts"]]]))
        errors.extend(f"{chapter['id']}: {e}" for e in validate_chapter(text, required_sections=sections))
        documents[chapter["path"]] = text
    documents[plan["moc_path"]] = five_key_note(plan, f"{slugify(plan['topic'])}.moc", "Map of Contents", render_moc(plan), Path(plan["chapters"][0]["path"]).stem)
    errors.extend(wikilink_errors(vault, documents))
    asset_errors, asset_hashes = inspect_assets(vault, documents, visual_results)
    errors.extend(asset_errors)
    visual_manifest, lavia_errors = _validate_local_first_visuals(vault, plan, drafts, visual_results)
    errors.extend(lavia_errors)
    current_hashes = {}
    for relative, text in documents.items():
        target = contained(vault, relative)
        current_hashes[relative] = content_hash(target.read_text(encoding="utf-8-sig")) if target.exists() else None
        if target.exists() and target.read_text(encoding="utf-8-sig") != text and (expected_hashes or {}).get(relative) != current_hashes[relative]:
            errors.append(f"existing chapter needs expected digest: {relative}")
    if errors:
        validation["outcomes"]["structural"] = {"status": "fail" if len(errors) > semantic_error_count else "pass",
                                                   "method": "YAML, sections, fences, links, assets and expected digests"}
        readiness = _derive_readiness_state(errors=errors, validation=validation, visual_results=visual_results, written_paths=[])
        report = {"complete": False, "readiness_state": readiness, "errors": errors, "written_paths": [], "validation": validation, "renderers": visual_results,
                  "manifest": visual_manifest, "reviews": reviews, "evidence": evidence}
        report_path = contained(vault, f".scriptorium/validation/col-{slugify(plan['topic'])}.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        safe_write_note(report_path, json.dumps(report, indent=2, ensure_ascii=False), validate_properties=False)
        if not allow_draft:
            return report
        # Explicit draft policy: persist authored Markdown chapters while honestly reporting non-complete readiness.
        draft_written: list[str] = []
        for relative, text in documents.items():
            target = contained(vault, relative)
            result = safe_write_note(target, text, expected_digest=current_hashes[relative], validate_properties=False)
            if result["written"]:
                draft_written.append(relative)
        report["written_paths"] = draft_written
        report["readiness_state"] = _derive_readiness_state(errors=errors, validation=validation, visual_results=visual_results, written_paths=draft_written)
        return report
    state_path = contained(vault, f".scriptorium/collections/col-{slugify(plan['topic'])}.json")
    state = {"composition": plan, "spec_hash": plan["spec_hash"], "evidence": evidence, "reviews": reviews,
             "checkpoints": {}, "asset_hashes": asset_hashes, "complete": False, "errors": [],
             "validation": validation, "renderers": visual_results, "manifest": visual_manifest}
    state["validation"]["outcomes"]["structural"] = {"status": "pass", "method": "YAML, sections, fences, links, assets and expected digests"}
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
    if plan.get("organize_by_collection") or plan.get("collection_slug"):
        lavia.save_asset_manifest(vault, visual_manifest)
    readiness = _derive_readiness_state(errors=[], validation=validation, visual_results=visual_results, written_paths=written)
    state["complete"] = True
    state["readiness_state"] = readiness
    checkpoint()
    return {**state, "written_paths": written}


def prepare_composition(vault: Path, plan: dict[str, Any], drafts: dict[str, str], *, execute: bool = True) -> tuple[dict, dict]:
    """Prepare the actual artifact before review; returned bodies are the receipt subjects."""
    from .contracts import prepare_drafts
    from .visuals import render_visuals
    from . import lavia
    bodies = prepare_drafts(plan, drafts)
    bodies, results = render_visuals(vault, plan, bodies, execute=execute)
    manifest = lavia.build_asset_manifest(plan, results, collection_slug=plan.get("collection_slug"))
    if execute:
        from ..vault import safe_write_note
        path = contained(vault, f".scriptorium/renderers/col-{slugify(plan['topic'])}.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        safe_write_note(
            path,
            json.dumps({"spec_hash": plan["spec_hash"], "renderers": results, "manifest": manifest}, indent=2),
            validate_properties=False,
        )
        if plan.get("organize_by_collection") or plan.get("collection_slug"):
            lavia.save_asset_manifest(vault, manifest)
    return {cid: body.strip() + "\n" for cid, body in bodies.items()}, results


def compile_context(plan: dict[str, Any], concept_ids: list[str]) -> dict[str, Any]:
    """Use E1's existing selective loader and compiler for just the active concept closure."""
    from .._token_optimizer import select_context_bundle, compile_execution_prompt, estimate_tokens
    concepts = {c["id"]: c for c in plan["concepts"]}
    if not concept_ids or set(concept_ids) - set(concepts):
        raise ValueError("Context needs known concept IDs")
    selected, prerequisites = set(concept_ids), set()
    def visit(cid):
        for dep in concepts[cid]["prerequisites"]:
            if dep not in prerequisites:
                prerequisites.add(dep)
                visit(dep)
    for cid in concept_ids:
        visit(cid)
    active = [concepts[cid] for cid in concept_ids]
    types = {"conceptual"}
    for concept in active:
        for cap in concept["capabilities"]:
            types.add({
                "S02": "mathematical",
                "S03": "computational",
                "S04": "computational",
                "S05": "computational",
                "S06": "empirical",
                "S07": "scientific",
                "S11": "historical",
                "S16": "scientific",
            }.get(cap, "conceptual"))
    bundle = select_context_bundle(master="M1", knowledge_types=sorted(types), source_policy=plan["source_policy"],
                                   has_source=any(c.get("claims") for c in active),
                                   math_depth=max(c["depth_allocation"]["levels"]["mathematical"] for c in active),
                                   code_depth=max(c["depth_allocation"]["levels"]["implementation"] for c in active))
    contract = "references/workflows/notes-creation/composition-contract.md"
    raw = (REPO_ROOT / contract).read_text(encoding="utf-8")
    bundle["loaded_docs"].append({"role": "profile:composition (overrides legacy layout/Properties)", "path": contract,
                                   "content": raw, "tokens": estimate_tokens(raw)})
    integrity_path = "references/contracts/composition-integrity.md"
    integrity = (REPO_ROOT/integrity_path).read_text(encoding="utf-8")
    needed = {"Authoring and publication", "Shared obligations and reviews", "Pedagogy, objectives and prerequisites",
              "Claims and research", "Assessments", "Repair and optimization"}
    if any(c["depth_allocation"]["levels"]["mathematical"] or set(c["capabilities"])-{"S01", "S11", "S14", "S15"} for c in active):
        needed.add("Mathematical and technical records")
    if any(c["depth_allocation"]["levels"]["visual"] or "S12" in c["capabilities"] for c in active) or any(v["concept"] in selected for v in plan["visuals"]):
        needed.add("Visuals")
        representation_path = "references/workflows/notes-creation/representations.md"
        representation = (REPO_ROOT / representation_path).read_text(encoding="utf-8")
        bundle["loaded_docs"].append({"role": "policy:active representations", "path": representation_path,
                                     "content": representation, "tokens": estimate_tokens(representation)})
    parts = re.split(r"(?=^## )", integrity, flags=re.M)
    selected_integrity = "\n".join(part for part in parts if not part.startswith("## ") or part.splitlines()[0][3:] in needed)
    bundle["loaded_docs"].append({"role": "policy:integrity (active sections)", "path": integrity_path,
                                   "content": selected_integrity, "tokens": estimate_tokens(selected_integrity)})
    selected_caps = {cap for c in active for cap in c["capabilities"]}
    specs = capabilities()
    context = {"concepts": active, "capabilities": {cap: specs[cap] for cap in sorted(selected_caps)},
               "prerequisite_summaries": [{"id": cid, "title": concepts[cid]["title"], "owner": concepts[cid]["chapter"]} for cid in sorted(prerequisites-selected)],
               "notation": plan["notation"], "obligations": [o for o in plan["obligations"] if o["concept"] in selected]}
    result = compile_execution_prompt(bundle, preferences_ir={"master": "M1", "output_profile": PROFILE, "source_policy": plan["source_policy"]},
                                      knowledge_context=context, validation_contracts=["five_key_profile", "executable_obligations", "claim_provenance",
                                                                                     "artifact_bound_review", "independent_disclosure", "critical_obligation_gate"])
    return {**result, "selected_concepts": concept_ids, "loaded_files": [d["path"] for d in bundle["loaded_docs"]],
            "capability_count": len(selected_caps), "context_file_reads": bundle["context_file_reads"]+3, "actual_model_tokens": None}


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
    documents = {}
    for relative in paths:
        path = contained(vault, relative)
        if not path.is_file():
            errors.append(f"missing chapter: {relative}")
            continue
        text = path.read_text(encoding="utf-8-sig")
        documents[relative] = text
        errors.extend(f"{relative}: {e}" for e in validate_chapter(text))
        checkpoint = state.get("checkpoints", {}).get(relative, {})
        if content_hash(text) != checkpoint.get("hash"):
            errors.append(f"chapter changed since review: {relative}")
        for asset in re.findall(r"!\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", text):
            if not contained(vault, asset).is_file():
                errors.append(f"missing asset: {asset}")
            elif content_hash(contained(vault, asset).read_bytes()) != state.get("asset_hashes", {}).get(asset):
                errors.append(f"asset changed since review: {asset}")
    errors.extend(wikilink_errors(vault, documents))
    asset_errors, asset_hashes = inspect_assets(vault, documents, state.get("renderers", {}))
    errors.extend(asset_errors)
    for relative, expected in state.get("asset_hashes", {}).items():
        path = contained(vault, relative)
        if not path.is_file() or content_hash(path.read_bytes()) != expected:
            errors.append(f"asset changed since review: {relative}")
    folder = contained(vault, plan["folder"])
    if plan["folder"] and folder.is_dir() and {p.name for p in folder.iterdir()} != {Path(p).name for p in paths}:
        errors.append(f"topic folder must contain only the {len(paths)} planned Markdown files")
    obligations = [o for c in plan["concepts"] for o in c["research_obligations"]]
    if not evidence_status(obligations, state.get("evidence", {}))["sufficient"]:
        errors.append("evidence is no longer sufficient")
    if plan.get("version") != 2 or not plan.get("obligations"):
        errors.append("legacy composition lacks executable obligations; rebuild and review")
        return {"valid": False, "errors": errors}
    drafts = {c["id"]: parse_note(contained(vault, c["path"]).read_text(encoding="utf-8-sig")).body.strip()+"\n"
              for c in plan["chapters"] if contained(vault, c["path"]).is_file()}
    from .contracts import validate_obligations
    from .visuals import render_visuals
    _, renderers = render_visuals(vault, plan, drafts, execute=False)
    # A valid asset alone cannot retroactively establish that its renderer ran.
    for oid, result in renderers.items():
        recorded = state.get("renderers", {}).get(oid, {})
        if not recorded.get("attempted") or recorded.get("status") != "verified" or recorded.get("hash") != result.get("hash"):
            result["status"] = "failed"
            result["failure_reason"] = "missing persisted renderer execution result"
    visual_manifest, lavia_errors = _validate_local_first_visuals(
        vault, plan, drafts, renderers, require_manifest_file=True,
    )
    errors.extend(lavia_errors)
    validation = validate_obligations(plan, drafts, evidence=state.get("evidence", {}), reviews=state.get("reviews", {}),
                                      visuals=renderers, vault=vault)
    structural_valid = not errors
    errors.extend(validation["errors"])
    validation["outcomes"]["structural"] = {"status": "pass" if structural_valid else "fail", "method": "published file, link and hash checks"}
    return {"valid": not errors, "errors": errors, "validation": validation, "manifest": visual_manifest,
            "review_scope": "scoped computations and artifact-bound recorded semantic review; no universal proof or source-entailment certification"}
