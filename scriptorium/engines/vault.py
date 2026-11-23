"""Engine E6 — Vault and Notes Lifecycle Engine for Scriptorium.

Consolidates:
- Mandatory Obsidian Properties Builder & Validator (topic, tags, master_topic, domain, note_type + optional)
- Central Hierarchical Tag Taxonomy & Synonym Normalization
- Knowledge Hierarchy Classifier (Domain / Master Topic / Subdomain across all disciplines)
- Mechanism 16: Incremental Notes Update Engine (minimal section edits, custom metadata preservation, idempotence, safe atomic write & rollback)
"""
from __future__ import annotations

from datetime import date
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Callable

import yaml

from scriptorium.layout import canonical_note_type
from scriptorium.models import (
    ALL_MANAGED_PROPERTIES,
    CANONICAL_NOTE_TYPES,
    MetadataValidationError,
    REQUIRED_OBSIDIAN_PROPERTIES,
    UnsafeUpdateConflictError,
    dump_frontmatter,
    has_frontmatter,
    parse_frontmatter,
    parse_note,
    slugify,
)

# ---------------------------------------------------------------------------
# Tag Normalization & Synonym Canonicalization (Section 8.6)
# ---------------------------------------------------------------------------

TAG_SYNONYMS: dict[str, str] = {
    "ml": "machine-learning",
    "machinelearning": "machine-learning",
    "machine_learning": "machine-learning",
    "ai": "artificial-intelligence",
    "artificialintelligence": "artificial-intelligence",
    "artificial_intelligence": "artificial-intelligence",
    "dl": "deep-learning",
    "deeplearning": "deep-learning",
    "deep_learning": "deep-learning",
    "dsa": "data-structures-algorithms",
    "data-structures-and-algorithms": "data-structures-algorithms",
    "cs": "computer-science",
    "os": "operating-systems",
    "nlp": "natural-language-processing",
    "cv": "computer-vision",
    "gd": "gradient-descent",
    "sgd": "stochastic-gradient-descent",
    "py": "python",
    "python3": "python",
    "cpp": "c-plus-plus",
    "c++": "c-plus-plus",
    "js": "javascript",
    "ts": "typescript",
    "em": "electromagnetism",
    "ww2": "world-war-ii",
    "wwii": "world-war-ii",
}

MANAGED_TAG_PREFIXES: tuple[str, ...] = (
    "topic/",
    "subject/",
    "domain/",
    "master-topic/",
    "subdomain/",
    "concept/",
    "type/",
    "level/",
    "skill/",
)

# Ordered discipline taxonomy: (pattern, domain, master_topic, subdomain)
HIERARCHY_RULES: tuple[tuple[re.Pattern[str], str, str, str], ...] = (
    # Engineering classifications supplement the same shared taxonomy.
    (re.compile(r"\b(?:circuits?|electrical\s+engineering|thevenin|thévenin|kirchhoff|impedance|electronics)\b", re.I),
     "Engineering", "Electrical Engineering", "Circuit Analysis"),
    (re.compile(r"\b(?:control\s+systems?|feedback\s+control|transfer\s+functions?)\b", re.I),
     "Engineering", "Control Engineering", "Systems"),
    # Artificial Intelligence / Machine Learning
    (re.compile(r"\b(?:gradient\s+descent|stochastic\s+gradient|adam\s+optimizer|rmsprop|momentum|learning\s+rate|convex\s+optimization)\b", re.I),
     "Artificial Intelligence", "Machine Learning", "Optimization"),
    (re.compile(r"\b(?:backpropagation|transformer|self[- ]attention|attention\s+mechanism|neural\s+network|cnn|convolutional|vit|vision\s+transformer|rnn|lstm|residual\s+connection|vanishing\s+gradient|batch\s+norm|layer\s+norm|deep\s+learning|mlp|perceptron)\b", re.I),
     "Artificial Intelligence", "Machine Learning", "Deep Learning"),
    (re.compile(r"\b(?:machine\s+learning|supervised\s+learning|unsupervised|regression|classification|svm|random\s+forest|decision\s+tree|k[- ]means|pca|loss\s+function|overfitting|regularization|cross[- ]validation|scikit[- ]learn)\b", re.I),
     "Artificial Intelligence", "Machine Learning", "Foundations"),
    # Computer Science — Python / Data Processing / Web / Systems / DSA
    (re.compile(r"\b(?:pandas|polars|data\s+cleaning|dataframe|numpy|scipy|matplotlib)\b", re.I),
     "Computer Science", "Python Programming", "Data Processing"),
    (re.compile(r"\b(?:pytorch|tensorflow|keras)\b", re.I),
     "Artificial Intelligence", "Machine Learning", "Frameworks"),
    (re.compile(r"\b(?:binary\s+search|linear\s+search)\b", re.I),
     "Computer Science", "Data Structures and Algorithms", "Searching"),
    (re.compile(r"\b(?:quicksort|mergesort|heapsort|sorting\s+algorithm)\b", re.I),
     "Computer Science", "Data Structures and Algorithms", "Sorting"),
    (re.compile(r"\b(?:two\s+sum|dynamic\s+programming|dijkstra|bfs|dfs|binary\s+tree|red[- ]black\s+tree|trie|hash\s+table|linked\s+list|graph\s+algorithm|dsa|data\s+structures?|algorithms?|recursion|heap)\b", re.I),
     "Computer Science", "Data Structures and Algorithms", "Algorithms"),
    (re.compile(r"\b(?:operating\s+systems?|paging|virtual\s+memory|cpu\s+scheduling|deadlock|threads?|mutex|semaphore|process\s+scheduling|linux\s+kernel)\b", re.I),
     "Computer Science", "Operating Systems", "Systems"),
    (re.compile(r"\b(?:fastapi|rest\s+api|graphql|http|websocket|authentication|oauth|jwt|react|typescript|javascript|frontend|backend)\b", re.I),
     "Computer Science", "Software Engineering", "Web Development"),
    (re.compile(r"\b(?:git\b|docker|kubernetes|bash|shell|cli|linux\s+commands?|ci/cd)\b", re.I),
     "Computer Science", "Software Engineering", "Developer Tools"),
    (re.compile(r"\b(?:sql|postgresql|mysql|duckdb|database|b[- ]tree|acid|transaction\s+isolation|indexing|normalization\s+forms?|3nf)\b", re.I),
     "Computer Science", "Databases", "Relational Systems"),
    (re.compile(r"\b(?:python|c\+\+|rust|java|golang|compiler|programming)\b", re.I),
     "Computer Science", "Software Engineering", "Programming"),
    # Physics
    (re.compile(r"\b(?:biot[\s–-]savart|ampere|magnetostatics|magnetic\s+field|lorentz\s+force|faraday|maxwell|gauss(?:'s)?\s+law|electrostatics|electromagnetism|coulomb)\b", re.I),
     "Physics", "Electromagnetism", "Magnetostatics"),
    (re.compile(r"\b(?:thermodynamics|entropy|carnot|enthalpy|gibbs\s+free\s+energy|boltzmann|heat\s+engine|ideal\s+gas)\b", re.I),
     "Physics", "Thermodynamics", "Statistical Physics"),
    (re.compile(r"\b(?:wave\s+optics|huygens|snell|refraction|diffraction|interference|polarization|lenses?|mirrors?|optics)\b", re.I),
     "Physics", "Optics", "Wave Optics"),
    (re.compile(r"\b(?:quantum\s+mechanics|schr[oö]dinger|wavefunction|heisenberg|superposition|entanglement|compton|photoelectric)\b", re.I),
     "Physics", "Quantum Mechanics", "Foundations"),
    (re.compile(r"\b(?:kinematics|newton(?:'s)?\s+laws?|lagrangian|hamiltonian|classical\s+mechanics|relativity|physics)\b", re.I),
     "Physics", "Classical Mechanics", "Dynamics"),
    # Mathematics
    (re.compile(r"\b(?:calculus|integrals?|integration|derivatives?|chain\s+rule|taylor\s+series|limits?|multivariable|partial\s+derivatives?|differential\s+equations?)\b", re.I),
     "Mathematics", "Calculus", "Analysis"),
    (re.compile(r"\b(?:linear\s+algebra|matrix|matrices|eigenvalue|eigenvector|svd|singular\s+value|vector\s+space|determinant|orthogonality)\b", re.I),
     "Mathematics", "Linear Algebra", "Matrix Theory"),
    (re.compile(r"\b(?:bayes(?:'s?)?\s+theorem|probability|random\s+variable|markov\s+chain|gaussian|normal\s+distribution|central\s+limit|hypothesis\s+testing|statistics|stochastic)\b", re.I),
     "Mathematics", "Probability and Statistics", "Inference"),
    (re.compile(r"\b(?:real\s+analysis|topology|group\s+theory|number\s+theory|abstract\s+algebra|measure\s+theory|fourier|laplace|pure\s+math)\b", re.I),
     "Mathematics", "Pure Mathematics", "Analysis"),
    # Chemistry
    (re.compile(r"\b(?:organic\s+chemistry|alkane|alkene|sn1|sn2|stereochemistry|carbonyl|aromatic|synthesis\s+reaction)\b", re.I),
     "Chemistry", "Organic Chemistry", "Reactions"),
    (re.compile(r"\b(?:chemistry|stoichiometry|chemical\s+equilibrium|kinetics|acid[- ]base|electrochemistry|orbitals?|molecular\s+bonding)\b", re.I),
     "Chemistry", "General Chemistry", "Principles"),
    # Biology
    (re.compile(r"\b(?:cellular\s+respiration|glycolysis|krebs\s+cycle|atp|mitosis|meiosis|photosynthesis|organelle|cell\s+cycle)\b", re.I),
     "Biology", "Cell Biology", "Metabolism and Division"),
    (re.compile(r"\b(?:dna|rna|genetics|transcription|translation|crispr|enzyme|hardy[\s–-]weinberg|evolution|ecology|biology)\b", re.I),
     "Biology", "Molecular Biology and Genetics", "Genetics"),
    # History
    (re.compile(r"\b(?:french\s+revolution|industrial\s+revolution|world\s+war|treaty|treaties|cold\s+war|renaissance|roman\s+empire|ottoman|dynasty|colonial|civil\s+war|history|historical)\b", re.I),
     "History", "World History", "Modern History"),
    # Economics
    (re.compile(r"\b(?:microeconomics|supply\s+and\s+demand|elasticity|marginal\s+utility|monopoly|game\s+theory|nash\s+equilibrium)\b", re.I),
     "Economics", "Microeconomics", "Market Theory"),
    (re.compile(r"\b(?:keynesian|monetarist|macroeconomics|inflation|monetary\s+policy|fiscal\s+policy|gdp|economics)\b", re.I),
     "Economics", "Macroeconomics", "Economic Policy"),
    # Philosophy / Law / Humanities
    (re.compile(r"\b(?:philosophy|epistemology|ethics|kantian|utilitarianism|logic|metaphysics)\b", re.I),
     "Philosophy", "Philosophy", "Foundations"),
    (re.compile(r"\b(?:constitutional\s+law|contract\s+law|tort|jurisprudence|statute)\b", re.I),
     "Law", "Legal Studies", "Jurisprudence"),
)


def normalize_tag_segment(raw: str) -> str:
    """Normalize a single tag segment into lowercase kebab-case with synonym canonicalization."""
    cleaned = str(raw or "").strip().lstrip("#")
    if not cleaned:
        return ""
    slug = slugify(cleaned)
    return TAG_SYNONYMS.get(slug, TAG_SYNONYMS.get(cleaned.lower(), slug))


def validate_semantic_tags(tags: Any) -> list[str]:
    """Validate hierarchical classification, independent of a note's YAML profile.

    Unknown classifications stay explicitly general until an author supplies a
    parent/domain. This check validates syntax and coverage, not semantic truth.
    """
    if not isinstance(tags, list) or not tags:
        return ["semantic tags must be a nonempty list"]
    errors = []
    normalized = []
    for tag in tags:
        if not isinstance(tag, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9]+(?:-[a-z0-9]+)*)+", tag):
            errors.append(f"invalid normalized semantic tag: {tag!r}")
        else:
            normalized.append(normalize_tag(tag))
            if tag in {"domain/general", "subject/general", "subject/general-knowledge", "topic/note"}:
                errors.append("generic-only classification needs an explicit subject and domain")
    if len(normalized) != len(set(normalized)):
        errors.append("duplicate semantic tags")
    for prefix in ("topic/", "subject/", "domain/"):
        if not any(tag.startswith(prefix) for tag in normalized):
            errors.append(f"missing semantic classification: {prefix}")
    return errors


def normalize_tag(raw: str) -> str:
    """Normalize either a hierarchical tag ('domain/AI') or flat tag ('ML') into canonical Obsidian form."""
    cleaned = str(raw or "").strip().lstrip("#")
    if not cleaned:
        return ""
    if "/" in cleaned:
        parts = [p for p in cleaned.split("/") if p.strip()]
        prefix = slugify(parts[0])
        rest = "/".join(normalize_tag_segment(p) for p in parts[1:] if normalize_tag_segment(p))
        return f"{prefix}/{rest}" if rest else prefix
    return normalize_tag_segment(cleaned)


def classify_knowledge_hierarchy(
    topic: str,
    *,
    content: str = "",
    explicit_domain: str | None = None,
    explicit_master_topic: str | None = None,
    explicit_subdomain: str | None = None,
) -> dict[str, str]:
    """Infer consistent (domain, master_topic, subdomain) from topic and optional content.

    Respects explicit overrides and falls back cleanly to General without inventing fake hierarchies.
    """
    combined = f"{topic} {content[:600]}".strip()
    inferred_domain = "General"
    inferred_master = "General Knowledge"
    inferred_sub = ""

    for pattern, dom, mtopic, sub in HIERARCHY_RULES:
        if pattern.search(topic):
            inferred_domain, inferred_master, inferred_sub = dom, mtopic, sub
            break
    else:
        for pattern, dom, mtopic, sub in HIERARCHY_RULES:
            if pattern.search(combined):
                inferred_domain, inferred_master, inferred_sub = dom, mtopic, sub
                break

    domain = explicit_domain.strip() if (explicit_domain and explicit_domain.strip() and explicit_domain.strip().lower() != "general") else inferred_domain
    master_topic = explicit_master_topic.strip() if (explicit_master_topic and explicit_master_topic.strip() and explicit_master_topic.strip().lower() != "general") else inferred_master
    subdomain = explicit_subdomain.strip() if (explicit_subdomain and explicit_subdomain.strip()) else inferred_sub

    # Refine subdomain specifically when topic clearly names Magnetostatics vs Electrostatics
    if domain == "Physics" and master_topic == "Electromagnetism" and not explicit_subdomain:
        if re.search(r"\b(?:gauss|coulomb|electrostatic|electric\s+field)\b", topic, re.I):
            subdomain = "Electrostatics"
    if domain == "History" and not explicit_subdomain:
        if re.search(r"\b(?:roman|greek|ancient|mesopotamia)\b", topic, re.I):
            subdomain = "Ancient History"
        elif re.search(r"\b(?:french\s+revolution|world\s+war|treaty|cold\s+war)\b", topic, re.I):
            subdomain = "Modern History"

    return {
        "domain": domain,
        "master_topic": master_topic,
        "subdomain": subdomain,
    }


def generate_tags(
    *,
    topic: str,
    domain: str,
    master_topic: str,
    note_type: str,
    subdomain: str = "",
    secondary_concepts: list[str] | None = None,
    difficulty: str | None = None,
    max_secondary: int = 3,
) -> list[str]:
    """Generate concise, normalized hierarchical Obsidian tags without tag inflation."""
    tags: list[str] = []

    def _add(tag: str) -> None:
        norm = normalize_tag(tag)
        if norm and norm not in tags:
            tags.append(norm)

    _add(f"topic/{topic}")
    _add(f"subject/{master_topic}")
    _add(f"domain/{domain}")
    _add(f"master-topic/{master_topic}")
    if subdomain:
        _add(f"subdomain/{subdomain}")
    _add(f"concept/{topic}")
    for sec in (secondary_concepts or [])[:max_secondary]:
        sec_clean = str(sec).strip()
        if sec_clean and normalize_tag_segment(sec_clean) != normalize_tag_segment(topic):
            _add(f"concept/{sec_clean}")
    _add(f"type/{canonical_note_type(note_type)}")
    if difficulty and difficulty.strip().lower() in {"beginner", "intermediate", "advanced"}:
        _add(f"level/{difficulty.strip().lower()}")
    return tags


def build_obsidian_properties(
    *,
    topic: str,
    note_type: str,
    domain: str | None = None,
    master_topic: str | None = None,
    subdomain: str | None = None,
    content: str = "",
    secondary_concepts: list[str] | None = None,
    user_tags: list[str] | None = None,
    note_id: str | None = None,
    aliases: list[str] | None = None,
    nexttopics: list[str] | None = None,
    concept_ids: list[str] | None = None,
    parent_topic: str | None = None,
    collection_id: str | None = None,
    prerequisites: list[str] | None = None,
    related: list[str] | None = None,
    source_mode: str | None = None,
    source_refs: list[str] | None = None,
    difficulty: str | None = None,
    status: str | None = None,
    created: str | date | None = None,
    updated: str | date | None = None,
    template_id: str | None = None,
    coverage_status: str | None = None,
    custom_properties: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Construct an Obsidian-compatible Properties mapping with all required fields."""
    clean_topic = str(topic or "").strip()
    if not clean_topic:
        raise MetadataValidationError("Obsidian Properties require a non-empty 'topic'.")

    canon_type = canonical_note_type(note_type)
    hierarchy = classify_knowledge_hierarchy(
        clean_topic,
        content=content,
        explicit_domain=domain,
        explicit_master_topic=master_topic,
        explicit_subdomain=subdomain,
    )

    managed_tags = generate_tags(
        topic=clean_topic,
        domain=hierarchy["domain"],
        master_topic=hierarchy["master_topic"],
        note_type=canon_type,
        subdomain=hierarchy["subdomain"],
        secondary_concepts=secondary_concepts,
        difficulty=difficulty,
    )
    # Append preserved user-defined tags (deduplicated, stripped of '#')
    all_tags = list(managed_tags)
    for ut in user_tags or []:
        u = str(ut).strip().lstrip("#")
        if u and u not in all_tags and normalize_tag(u) not in all_tags:
            all_tags.append(u)

    props: dict[str, Any] = {
        "topic": clean_topic,
        "tags": all_tags,
        "master_topic": hierarchy["master_topic"],
        "domain": hierarchy["domain"],
        "note_type": canon_type,
    }
    if hierarchy["subdomain"]:
        props["subdomain"] = hierarchy["subdomain"]
    if note_id:
        props["id"] = str(note_id).strip()
    if aliases:
        clean_aliases = list(dict.fromkeys(str(a).strip() for a in aliases if str(a).strip()))
        if clean_aliases:
            props["aliases"] = clean_aliases
    if nexttopics is not None:
        props["nexttopics"] = [str(n).strip() for n in nexttopics if str(n).strip()]
    if concept_ids:
        props["concept_ids"] = list(dict.fromkeys(str(c).strip() for c in concept_ids if str(c).strip()))
    if parent_topic:
        props["parent_topic"] = str(parent_topic).strip()
    if collection_id:
        props["collection_id"] = str(collection_id).strip()
    if prerequisites:
        props["prerequisites"] = list(dict.fromkeys(str(p).strip() for p in prerequisites if str(p).strip()))
    if related:
        props["related"] = list(dict.fromkeys(str(r).strip() for r in related if str(r).strip()))
    if source_mode:
        props["source_mode"] = str(source_mode).strip()
    if source_refs:
        props["source_refs"] = list(dict.fromkeys(str(s).strip() for s in source_refs if str(s).strip()))
    if difficulty:
        props["difficulty"] = str(difficulty).strip().lower()
    if status:
        props["status"] = str(status).strip()
    if created:
        props["created"] = created.isoformat() if isinstance(created, date) else str(created).strip()
    if updated:
        props["updated"] = updated.isoformat() if isinstance(updated, date) else str(updated).strip()
    if template_id:
        props["template_id"] = str(template_id).strip()
    if coverage_status:
        props["coverage_status"] = str(coverage_status).strip()

    # Preserve unrelated custom user properties without clobbering managed keys
    for key, val in (custom_properties or {}).items():
        if key not in props:
            props[key] = val
    return props


def validate_obsidian_properties(
    note_text: str,
    *,
    expected_note_type: str | None = None,
    allow_custom_properties: bool = True,
) -> list[str]:
    """Validate that a Markdown note starts at line 1 with valid Obsidian Properties."""
    errors: list[str] = []
    lines = note_text.splitlines()
    if not lines:
        return ["Note is empty."]
    if lines[0].strip() != "---":
        return ["Obsidian Properties YAML frontmatter must begin on line 1 with '---'."]

    try:
        metadata, _, body_start = parse_frontmatter(note_text)
    except (MetadataValidationError, yaml.YAMLError) as exc:
        return [str(exc)]

    # Check for duplicate frontmatter blocks immediately following the first block
    rest_lines = [ln for ln in lines[body_start:] if ln.strip()]
    if rest_lines and rest_lines[0].strip() == "---":
        if any(ln.strip() == "---" for ln in rest_lines[1:25]):
            errors.append("Duplicate YAML frontmatter block detected.")

    for key in REQUIRED_OBSIDIAN_PROPERTIES:
        if key not in metadata:
            errors.append(f"Missing required Obsidian Property: '{key}'.")
        elif key == "tags":
            if not isinstance(metadata[key], list) or not metadata[key]:
                errors.append("'tags' property must be a non-empty YAML list.")
        elif not isinstance(metadata[key], str) or not metadata[key].strip():
            errors.append(f"Required Obsidian Property '{key}' must be non-empty text.")

    tags = metadata.get("tags")
    if isinstance(tags, list):
        for tag in tags:
            if not isinstance(tag, str) or not tag.strip():
                errors.append("All entries in 'tags' must be non-empty strings.")
            elif tag.strip().startswith("#"):
                errors.append(f"Tag '{tag}' must not contain a leading '#' prefix in YAML Properties.")
            elif not re.fullmatch(r"[\w/-]+", tag.strip()):
                errors.append(f"Tag '{tag}' contains invalid Obsidian tag characters.")

    nt = metadata.get("note_type")
    if isinstance(nt, str) and nt.strip():
        if nt.strip() not in CANONICAL_NOTE_TYPES:
            errors.append(f"Invalid note_type '{nt}'; expected one of {CANONICAL_NOTE_TYPES}.")
        elif expected_note_type and nt.strip() != canonical_note_type(expected_note_type):
            errors.append(f"note_type '{nt}' does not match expected '{canonical_note_type(expected_note_type)}'.")

    if not allow_custom_properties:
        for key in metadata:
            if key not in ALL_MANAGED_PROPERTIES:
                errors.append(f"Unauthorized frontmatter key: {key}")

    return errors


def render_note_with_properties(properties: dict[str, Any], body: str) -> str:
    """Emit a Markdown note starting at line 1 with valid Obsidian Properties followed by body."""
    fm = dump_frontmatter(properties)
    clean_body = body.strip("\r\n")
    return f"{fm}\n\n{clean_body}\n" if clean_body else f"{fm}\n"


def ensure_obsidian_properties(
    note_text: str,
    *,
    topic: str | None = None,
    note_type: str = "deep-notes",
    domain: str | None = None,
    master_topic: str | None = None,
    subdomain: str | None = None,
    created: str | date | None = None,
) -> str:
    """Ensure any Markdown note begins with valid Obsidian Properties while preserving custom fields & tags."""
    if has_frontmatter(note_text):
        existing, _, body_start = parse_frontmatter(note_text)
        body = "\n".join(note_text.splitlines()[body_start:]).lstrip("\r\n")
    else:
        existing = {}
        body = note_text.lstrip("\r\n")

    parsed_title = None
    for ln in body.splitlines():
        if ln.startswith("# "):
            parsed_title = ln[2:].strip()
            break

    eff_topic = topic or existing.get("topic") or parsed_title or "Untitled Topic"
    eff_type = canonical_note_type(existing.get("note_type") or note_type)
    eff_domain = domain or existing.get("domain")
    eff_master = master_topic or existing.get("master_topic")
    eff_sub = subdomain or existing.get("subdomain")
    existing_tags = existing.get("tags") if isinstance(existing.get("tags"), list) else []
    user_tags = [t for t in existing_tags if not any(str(t).startswith(p) for p in MANAGED_TAG_PREFIXES)]

    custom = {k: v for k, v in existing.items() if k not in ALL_MANAGED_PROPERTIES}
    props = build_obsidian_properties(
        topic=str(eff_topic),
        note_type=eff_type,
        domain=str(eff_domain) if eff_domain else None,
        master_topic=str(eff_master) if eff_master else None,
        subdomain=str(eff_sub) if eff_sub else None,
        content=body,
        user_tags=user_tags,
        note_id=existing.get("id"),
        aliases=existing.get("aliases"),
        nexttopics=existing.get("nexttopics"),
        concept_ids=existing.get("concept_ids"),
        parent_topic=existing.get("parent_topic"),
        collection_id=existing.get("collection_id"),
        prerequisites=existing.get("prerequisites"),
        related=existing.get("related"),
        source_mode=existing.get("source_mode"),
        source_refs=existing.get("source_refs"),
        difficulty=existing.get("difficulty"),
        status=existing.get("status"),
        created=existing.get("created") or created,
        updated=existing.get("updated"),
        template_id=existing.get("template_id"),
        coverage_status=existing.get("coverage_status"),
        custom_properties=custom,
    )
    return render_note_with_properties(props, body)


# ---------------------------------------------------------------------------
# Mechanism 16 — Incremental Notes Update Engine (Section 25)
# ---------------------------------------------------------------------------

def incremental_update_note(
    existing_text: str,
    *,
    section_updates: dict[str, str] | None = None,
    append_sections: dict[str, str] | None = None,
    property_updates: dict[str, Any] | None = None,
    add_tags: list[str] | None = None,
    update_date: str | date | None = None,
) -> dict[str, Any]:
    """Mechanism 16: Incrementally update sections and/or Properties without destroying unrelated content or custom metadata.

    Idempotent: re-applying identical updates produces zero diff and never duplicates frontmatter or sections.
    """
    parsed = parse_note(existing_text)
    existing_meta = dict(parsed.metadata)
    body_lines = parsed.body.splitlines()
    changed = False
    modified_sections: list[str] = []

    # 1. Apply targeted section replacements without touching unrelated sections
    if section_updates:
        for target_heading, new_section_body in section_updates.items():
            target_slug = slugify(target_heading)
            # Re-parse current body lines for exact indices on each edit
            cur_parsed = parse_note("\n".join(body_lines))
            match = next((s for s in cur_parsed.sections if s.slug == target_slug or s.heading.lower() == target_heading.lower()), None)
            if match is not None:
                heading_line = f"{'#' * match.level} {match.heading}"
                replacement = [heading_line, "", *new_section_body.strip().splitlines(), ""]
                existing_slice = body_lines[match.start_line:match.end_line]
                while existing_slice and not existing_slice[-1].strip():
                    existing_slice.pop()
                expected_norm = [heading_line, "", *new_section_body.strip().splitlines()]
                if existing_slice != expected_norm:
                    body_lines = body_lines[:match.start_line] + replacement + body_lines[match.end_line:]
                    changed = True
                    modified_sections.append(match.heading)
            else:
                # Section did not exist yet -> append cleanly
                if body_lines and body_lines[-1].strip():
                    body_lines.append("")
                body_lines.extend([f"## {target_heading}", "", *new_section_body.strip().splitlines(), ""])
                changed = True
                modified_sections.append(target_heading)

    # 2. Append new sections idempotently (skip if heading already exists)
    if append_sections:
        cur_parsed = parse_note("\n".join(body_lines))
        existing_slugs = {s.slug for s in cur_parsed.sections}
        for heading, sec_body in append_sections.items():
            if slugify(heading) not in existing_slugs:
                if body_lines and body_lines[-1].strip():
                    body_lines.append("")
                body_lines.extend([f"## {heading}", "", *sec_body.strip().splitlines(), ""])
                changed = True
                modified_sections.append(heading)

    new_body = "\n".join(body_lines).strip() + "\n"

    # 3. Merge Obsidian Properties while preserving custom fields, original created date, and user tags
    custom_props = {k: v for k, v in existing_meta.items() if k not in ALL_MANAGED_PROPERTIES}
    merged_inputs = dict(existing_meta)
    for k, v in (property_updates or {}).items():
        if k == "created" and existing_meta.get("created"):
            # Never overwrite an existing creation date silently
            continue
        if k not in ALL_MANAGED_PROPERTIES:
            custom_props[k] = v
        else:
            merged_inputs[k] = v

    existing_tags = existing_meta.get("tags") if isinstance(existing_meta.get("tags"), list) else []
    user_tags = [t for t in existing_tags if not any(str(t).startswith(p) for p in MANAGED_TAG_PREFIXES)]
    for t in add_tags or []:
        t_clean = str(t).strip().lstrip("#")
        if t_clean and t_clean not in user_tags:
            user_tags.append(t_clean)

    # Preserve created date; update `updated` only if body or meaningful metadata actually changed
    eff_created = existing_meta.get("created")
    eff_updated = existing_meta.get("updated")

    props = build_obsidian_properties(
        topic=str(merged_inputs.get("topic") or parsed.title or "Untitled Topic"),
        note_type=str(merged_inputs.get("note_type") or "deep-notes"),
        domain=merged_inputs.get("domain"),
        master_topic=merged_inputs.get("master_topic"),
        subdomain=merged_inputs.get("subdomain"),
        content=new_body,
        user_tags=user_tags,
        note_id=merged_inputs.get("id"),
        aliases=merged_inputs.get("aliases"),
        nexttopics=merged_inputs.get("nexttopics"),
        concept_ids=merged_inputs.get("concept_ids"),
        parent_topic=merged_inputs.get("parent_topic"),
        collection_id=merged_inputs.get("collection_id"),
        prerequisites=merged_inputs.get("prerequisites"),
        related=merged_inputs.get("related"),
        source_mode=merged_inputs.get("source_mode"),
        source_refs=merged_inputs.get("source_refs"),
        difficulty=merged_inputs.get("difficulty"),
        status=merged_inputs.get("status"),
        created=eff_created,
        updated=eff_updated,
        template_id=merged_inputs.get("template_id"),
        coverage_status=merged_inputs.get("coverage_status"),
        custom_properties=custom_props,
    )

    if props != existing_meta:
        changed = True
    if changed and update_date is not None:
        eff_updated = update_date.isoformat() if isinstance(update_date, date) else str(update_date)
        props = build_obsidian_properties(
            topic=str(merged_inputs.get("topic") or parsed.title or "Untitled Topic"),
            note_type=str(merged_inputs.get("note_type") or "deep-notes"),
            domain=merged_inputs.get("domain"),
            master_topic=merged_inputs.get("master_topic"),
            subdomain=merged_inputs.get("subdomain"),
            content=new_body,
            user_tags=user_tags,
            note_id=merged_inputs.get("id"),
            aliases=merged_inputs.get("aliases"),
            nexttopics=merged_inputs.get("nexttopics"),
            concept_ids=merged_inputs.get("concept_ids"),
            parent_topic=merged_inputs.get("parent_topic"),
            collection_id=merged_inputs.get("collection_id"),
            prerequisites=merged_inputs.get("prerequisites"),
            related=merged_inputs.get("related"),
            source_mode=merged_inputs.get("source_mode"),
            source_refs=merged_inputs.get("source_refs"),
            difficulty=merged_inputs.get("difficulty"),
            status=merged_inputs.get("status"),
            created=eff_created,
            updated=eff_updated,
            template_id=merged_inputs.get("template_id"),
            coverage_status=merged_inputs.get("coverage_status"),
            custom_properties=custom_props,
        )

    updated_text = render_note_with_properties(props, new_body)
    validation_errors = validate_obsidian_properties(updated_text, allow_custom_properties=True)
    if validation_errors:
        raise MetadataValidationError("; ".join(validation_errors))

    return {
        "changed": updated_text != existing_text,
        "modified_sections": modified_sections,
        "properties": props,
        "preserved_custom_properties": list(custom_props.keys()),
        "content": updated_text,
    }


def safe_write_note(
    path: Path,
    content: str,
    *,
    expected_digest: str | None = None,
    validate_properties: bool = True,
    vault_root: Path | None = None,
) -> dict[str, Any]:
    """Validate containment & Properties, detect concurrent manual-edit conflicts, and write atomically."""
    raw_path = Path(path)
    if ".." in raw_path.parts:
        raise ValueError(f"Path traversal ('..') is not allowed when writing notes: {path}")
    if vault_root is not None:
        from scriptorium.models import is_within_vault
        if not is_within_vault(vault_root, raw_path):
            raise ValueError(f"Destination path '{path}' escapes vault root '{vault_root}'.")
    if validate_properties:
        errs = validate_obsidian_properties(content, allow_custom_properties=True)
        if errs:
            raise MetadataValidationError("; ".join(errs))

    if path.exists():
        current_bytes = path.read_bytes()
        current_text = current_bytes.decode("utf-8-sig")
        if expected_digest is not None:
            from scriptorium.models import content_hash
            if content_hash(current_text) != expected_digest:
                raise UnsafeUpdateConflictError(
                    f"Target note '{path.name}' was modified externally since it was read; aborting unsafe overwrite."
                )
        if current_text == content:
            return {"written": False, "path": str(path), "reason": "no_changes"}

    path.parent.mkdir(parents=True, exist_ok=True)
    data = content.encode("utf-8")
    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".scribe-tmp-", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            tmp.write(data)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(tmp_path, path)
        tmp_path = None
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
    return {"written": True, "path": str(path)}


class VaultEngine:
    def publish_composition(self, vault_root: Path, composition: dict[str, Any], drafts: dict[str, str], **kwargs: Any) -> dict[str, Any]:
        from .composition import publish_composition
        return publish_composition(vault_root, composition, drafts, **kwargs)

    def inventory_migration(self, vault_root: Path, paths: list[str]) -> dict[str, Any]:
        from .composition import inventory_migration
        return inventory_migration(vault_root, paths)

    """Cohesive Engine E6 facade for Properties, Tag Taxonomy, Incremental Updates, and Safe Writes."""

    def classify_hierarchy(self, topic: str, *, content: str = "", domain: str | None = None, master_topic: str | None = None, subdomain: str | None = None) -> dict[str, str]:
        return classify_knowledge_hierarchy(
            topic, content=content, explicit_domain=domain, explicit_master_topic=master_topic, explicit_subdomain=subdomain
        )

    def generate_tags(self, **kwargs: Any) -> list[str]:
        return generate_tags(**kwargs)

    def build_properties(self, **kwargs: Any) -> dict[str, Any]:
        return build_obsidian_properties(**kwargs)

    def validate_properties(self, note_text: str, *, expected_note_type: str | None = None, allow_custom_properties: bool = True) -> list[str]:
        return validate_obsidian_properties(
            note_text, expected_note_type=expected_note_type, allow_custom_properties=allow_custom_properties
        )

    def render_note(self, properties: dict[str, Any], body: str) -> str:
        return render_note_with_properties(properties, body)

    def ensure_properties(self, note_text: str, **kwargs: Any) -> str:
        return ensure_obsidian_properties(note_text, **kwargs)

    def update_note(self, existing_text: str, **kwargs: Any) -> dict[str, Any]:
        return incremental_update_note(existing_text, **kwargs)

    def write_note(
        self,
        path: Path,
        content: str,
        *,
        expected_digest: str | None = None,
        validate_properties: bool = True,
        vault_root: Path | None = None,
    ) -> dict[str, Any]:
        return safe_write_note(
            path,
            content,
            expected_digest=expected_digest,
            validate_properties=validate_properties,
            vault_root=vault_root,
        )

    def render_parent_moc(self, node: Any, plan: Any, node_map: dict[str, Any], preferences: Any, **kwargs: Any) -> str:
        return render_parent_moc(node, plan, node_map, preferences, **kwargs)

    def generate_collection(self, vault_root: Path, plan: Any, preferences: Any, **kwargs: Any) -> dict[str, Any]:
        return generate_note_collection(vault_root, plan, preferences, **kwargs)

    def generate_with_checkpoints(self, vault_root: Path, kcp: Any, preferences: Any, **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._collection_intelligence import generate_collection_with_checkpoints
        return generate_collection_with_checkpoints(vault_root, kcp, preferences, **kwargs)


# ---------------------------------------------------------------------------
# Hierarchical Collection Generation, Parent MOCs, & Manifest Persistence
# ---------------------------------------------------------------------------

def _master_to_note_type(master: str, variant: str | None = None) -> str:
    if variant == "atomic_card":
        return "atomic"
    return {
        "M1": "deep-notes",
        "M2": "study-notes",
        "M3": "quick-reference",
        "M4": "worked-solutions",
        "M5": "implementation-guide",
        "M6": "assessment",
        "M7": "synthesis-revision",
    }.get(master, "deep-notes")


def render_parent_moc(
    node: Any,
    plan: Any,
    node_map: dict[str, Any],
    preferences: Any,
    *,
    domain: str | None = None,
    master_topic: str | None = None,
    created: str | date | None = None,
) -> str:
    """Render a meaningful Parent / Group Map of Content (note_type: index) without duplicating child derivations."""
    parent_node = node_map.get(node.parent_id) if node.parent_id else None
    child_nodes = [node_map[cid] for cid in node.child_ids if cid in node_map]
    prereq_titles = [node_map[pid].title if pid in node_map else pid for pid in node.prerequisite_ids]
    related_titles = [node_map[rid].title if rid in node_map else rid for rid in node.related_ids]

    props = build_obsidian_properties(
        topic=node.title,
        note_type="index",
        domain=domain,
        master_topic=master_topic or plan.title,
        parent_topic=parent_node.title if parent_node else None,
        collection_id=plan.collection_id,
        concept_ids=[node.concept_id],
        prerequisites=prereq_titles or None,
        related=related_titles or None,
        source_mode=preferences.source_policy,
        difficulty=preferences.depth,
        status="active",
        created=created or date.today(),
        template_id="index",
        coverage_status="generated",
    )

    lines: list[str] = [f"# {node.title}", ""]
    if parent_node:
        lines.append(f"**Parent Index:** [[{parent_node.title}]]")
        lines.append("")

    # High-level synthesis (does NOT duplicate child note explanations)
    if node.note_role == "root_index":
        lines.extend([
            "## Overview",
            (
                f"This Map of Content organizes **{node.title}** into focused, linked notes calibrated for "
                f"**{preferences.depth}** depth ({preferences.learning_objective.replace('_', ' ')}). "
                "Each child note handles its own mechanisms, derivations, and worked examples independently so this index stays scannable."
            ),
            "",
        ])
    else:
        lines.extend([
            "## Overview",
            (
                f"**{node.title}** is a core sub-area within [[{plan.title}]]. "
                "Use the linked child notes below for full explanations, equations, and concrete walkthroughs."
            ),
            "",
        ])

    # Grouped child map
    lines.append("## Knowledge Map")
    if child_nodes:
        for ch in child_nodes:
            ch_master = (ch.template_plan or {}).get("master", preferences.master)
            ch_role = "Sub-area Index" if ch.note_role == "group_index" else f"Note ({ch_master})"
            sub_preview = ""
            if ch.child_ids:
                sub_links = ", ".join(f"[[{node_map[gc].title}]]" for gc in ch.child_ids if gc in node_map)
                sub_preview = f" — includes {sub_links}"
            lines.append(f"- [[{ch.title}]] *({ch_role})*{sub_preview}")
    else:
        lines.append("- No direct child notes planned.")
    lines.append("")

    # Recommended Learning Path (ordered study progression, distinct from folder hierarchy)
    descendant_ids: set[str] = set()
    stack = list(node.child_ids)
    while stack:
        cid = stack.pop()
        if cid in descendant_ids or cid not in node_map:
            continue
        descendant_ids.add(cid)
        stack.extend(node_map[cid].child_ids)

    ordered_study = [
        node_map[cid] for cid in plan.learning_order
        if cid in descendant_ids and node_map[cid].note_role == "child"
    ]
    if ordered_study:
        lines.append("## Recommended Learning Path")
        for idx, item in enumerate(ordered_study, 1):
            prereq_hint = ""
            if item.prerequisite_ids:
                pnames = ", ".join(f"[[{node_map[p].title}]]" for p in item.prerequisite_ids if p in node_map)
                if pnames:
                    prereq_hint = f" *(after {pnames})*"
            lines.append(f"{idx}. [[{item.title}]]{prereq_hint}")
        lines.append("")

    # Separate Prerequisites & Related section
    if prereq_titles or related_titles:
        lines.append("## Prerequisites & Related Links")
        if prereq_titles:
            lines.append("- **Prerequisites:** " + ", ".join(f"[[{t}]]" for t in prereq_titles))
        if related_titles:
            lines.append("- **Related:** " + ", ".join(f"[[{t}]]" for t in related_titles))
        lines.append("")

    if node.note_role == "root_index":
        boundary = (plan.scope_summary or {}).get("scope_boundary", preferences.scope_boundary)
        lines.extend([
            "## Scope Boundary",
            (
                f"Scope tier: `{(plan.scope_summary or {}).get('scope_tier', 'S3')}` "
                f"(boundary: `{boundary}`, planned notes: `{len(plan.nodes)}`). "
                "Additional subtopics can be expanded incrementally via `/scribe-notes` without regenerating existing notes."
            ),
            "",
        ])

    return render_note_with_properties(props, "\n".join(lines).strip() + "\n")


def _compose_child_note(
    node: Any,
    plan: Any,
    node_map: dict[str, Any],
    preferences: Any,
    *,
    domain: str,
    master_topic: str,
    source_facts: list[str] | None = None,
    visual_walkthroughs: list[str] | None = None,
    teaching_extensions: dict[str, Any] | None = None,
    created: str | date | None = None,
) -> str:
    """Compose a full adaptive child or single note using EIS-01..EIS-07 + M1-M7 + Obsidian Properties."""
    from scriptorium.engines.pedagogy import build_explanation_blueprint, compose_explanation_note

    tpl = node.template_plan or {}
    master = str(tpl.get("master") or preferences.master or "M1")
    variant = tpl.get("variant") if "variant" in tpl else preferences.variant
    note_type = str(tpl.get("note_type") or _master_to_note_type(master, variant))

    parent_node = node_map.get(node.parent_id) if node.parent_id else None
    prereq_titles = [node_map[pid].title if pid in node_map else pid for pid in node.prerequisite_ids]
    related_titles = [node_map[rid].title if rid in node_map else rid for rid in node.related_ids]

    ctx = {
        **(teaching_extensions or {}),
        "transition": (
            (teaching_extensions or {}).get("transition")
            or f"With this foundation on {node.title} established, connect these assumptions to related topics"
            + (f" such as [[{related_titles[0]}]]" if related_titles else "")
            + "."
        ),
    }
    if visual_walkthroughs:
        ctx["visual_walkthroughs"] = list(visual_walkthroughs)

    bp = build_explanation_blueprint(
        node.title,
        master=master,
        audience=preferences.depth,
        source_mode=preferences.source_policy,
        preserve_source_order=preferences.preserve_source_order,
        source_facts=source_facts,
        prerequisites=prereq_titles,
        context=ctx,
    )
    composed = compose_explanation_note(
        bp,
        source_facts=source_facts,
        domain_override=domain,
        master_topic_override=master_topic,
    )
    parsed = parse_note(composed)
    body = parsed.body.strip()

    # Add master-specific structural reinforcement when variant/master expects explicit structures
    if master == "M5" and "```" not in body:
        lang = preferences.language or "python"
        body += (
            f"\n\n## Executable Implementation ({lang.title()})\n\n"
            f"```{lang}\n"
            f"# Reference implementation scaffold for {node.title}\n"
            f"def run_{slugify(node.title).replace('-', '_')}(data):\n"
            f"    \"\"\"Verify core invariants on a minimal concrete input.\"\"\"\n"
            f"    assert data is not None, 'Input must not be None'\n"
            f"    return data\n"
            f"```\n\n"
            f"- **Verification & Edge Cases**: Check empty input, boundary conditions, and invariant preservation before scaling.\n"
        )
    elif master == "M6" and not re.search(r"(?:^###\s+Q\d+|^\*\*Front)", body, re.M):
        if variant == "flashcards":
            body += (
                "\n\n## Active-Recall Flashcards\n\n"
                f"### Card 1\n- **Front**: What core problem does {node.title} solve, and under what assumptions?\n"
                f"- **Back**: {node.title} resolves its target state transition only when its stated domain assumptions hold.\n"
            )
        else:
            body += (
                "\n\n## Practice Questions\n\n"
                f"### Q1 — Core Mechanism\nExplain why {node.title} fails when its primary boundary condition is violated.\n\n"
                "> [!tip]- Answer Key\n"
                f"> Identify the governing variable in {node.title} and trace how violating the assumption breaks convergence or validity.\n"
            )
    elif master == "M7" and variant == "comparison_guide" and "|" not in body:
        body += (
            "\n\n## Why Options Differ & Comparison Matrix\n\n"
            f"Choosing between candidate mechanisms for {node.title} depends on their underlying constraints and failure boundaries, not surface syntax alone.\n\n"
            "| Dimension | Option A | Option B | Decision Rule |\n"
            "|---|---|---|---|\n"
            f"| Core Mechanism ({node.title}) | Primary formulation | Alternative formulation | Choose based on domain assumptions and compute budget |\n"
        )
    elif master == "M4" and not re.search(r"\bFinal Answer\b", body, re.I):
        body += (
            "\n\n## Worked Problem Verification\n\n"
            f"- **Problem**: Apply {node.title} to a concrete minimal instance.\n"
            "- **Step-by-Step Method**: Substitute the given quantities, track every intermediate value, and check units/signs.\n"
            "- **Final Answer & Verification**: Cross-check the result against the boundary behavior stated above.\n"
        )

    # Add non-duplicative Obsidian navigation block
    nav_lines: list[str] = []
    if parent_node:
        nav_lines.append(f"- **Parent:** [[{parent_node.title}]]")
    if prereq_titles:
        nav_lines.append("- **Prerequisites:** " + ", ".join(f"[[{t}]]" for t in prereq_titles))
    if related_titles:
        nav_lines.append("- **Related:** " + ", ".join(f"[[{t}]]" for t in related_titles))
    if node.source_bindings:
        bound = ", ".join(str(b.get("section") or b.get("source") or "") for b in node.source_bindings if b)
        if bound:
            nav_lines.append(f"- **Source Coverage:** {bound}")
    if nav_lines:
        body += "\n\n## Navigation\n" + "\n".join(nav_lines)

    props = build_obsidian_properties(
        topic=node.title,
        note_type=note_type,
        domain=domain,
        master_topic=master_topic,
        content=body,
        parent_topic=parent_node.title if parent_node else None,
        collection_id=plan.collection_id,
        concept_ids=[node.concept_id],
        prerequisites=prereq_titles or None,
        related=related_titles or None,
        source_mode=preferences.source_policy,
        source_refs=[str(b.get("section") or b.get("source")) for b in node.source_bindings if b] or None,
        difficulty=preferences.depth,
        status="active",
        created=created or date.today(),
        template_id=master,
        coverage_status="generated",
    )
    return render_note_with_properties(props, body + "\n")


def generate_note_collection(
    vault_root: Path,
    plan: Any,
    preferences: Any,
    *,
    source_facts_by_node: dict[str, list[str]] | None = None,
    visual_specs: dict[str, list[dict[str, Any]]] | None = None,
    http_get: Callable[[str], tuple[bytes, str]] | None = None,
    overwrite_policy: str = "reconcile",
    created: str | date | None = None,
) -> dict[str, Any]:
    """Generate a single note or hierarchical note collection safely with manifest tracking and incremental reconciliation."""
    vault_root = Path(vault_root)
    vault_root.mkdir(parents=True, exist_ok=True)
    node_map = {n.concept_id: n for n in plan.nodes}
    root_hierarchy = classify_knowledge_hierarchy(plan.title)
    root_domain = root_hierarchy["domain"]
    root_master_topic = root_hierarchy["master_topic"]
    if root_master_topic == "General Knowledge":
        root_master_topic = plan.title

    records: list[dict[str, Any]] = []
    written_paths: list[str] = []
    failed_nodes: list[dict[str, Any]] = []

    for cid in plan.generation_order:
        node = node_map.get(cid)
        if node is None:
            continue
        target_path = vault_root / node.proposed_path
        try:
            visual_report: dict[str, Any] | None = None
            walkthroughs_for_node: list[str] = []
            node_visuals = (visual_specs or {}).get(cid) or (visual_specs or {}).get(node.title)
            if node_visuals and node.note_role not in {"root_index", "group_index"}:
                from scriptorium.engines.composition.visuals import acquire_node_visuals

                walkthroughs_for_node, visual_report = acquire_node_visuals(
                    vault_root,
                    collection_title=plan.title,
                    concept_id=cid,
                    node_title=node.title,
                    proposed_path=node.proposed_path,
                    node_visuals=node_visuals,
                    learner_level=preferences.depth,
                    image_http_get=http_get,
                )

            if node.note_role in {"root_index", "group_index"}:
                generated_content = render_parent_moc(
                    node,
                    plan,
                    node_map,
                    preferences,
                    domain=root_domain,
                    master_topic=root_master_topic,
                    created=created,
                )
            else:
                node_facts = (source_facts_by_node or {}).get(cid) or (source_facts_by_node or {}).get(node.title)
                generated_content = _compose_child_note(
                    node,
                    plan,
                    node_map,
                    preferences,
                    domain=root_domain,
                    master_topic=root_master_topic,
                    source_facts=node_facts,
                    visual_walkthroughs=walkthroughs_for_node or None,
                    created=created,
                )

            action = "created"
            final_content = generated_content
            if target_path.exists() and overwrite_policy == "reconcile":
                existing_text = target_path.read_text(encoding="utf-8-sig")
                gen_parsed = parse_note(generated_content)
                sec_map = {
                    sec.heading: "\n".join(sec.content.splitlines()[1:]).strip()
                    for sec in gen_parsed.sections
                    if sec.level == 2
                }
                upd = incremental_update_note(
                    existing_text,
                    append_sections=sec_map,
                    property_updates={
                        "collection_id": plan.collection_id,
                        "parent_topic": gen_parsed.metadata.get("parent_topic"),
                        "prerequisites": gen_parsed.metadata.get("prerequisites"),
                        "related": gen_parsed.metadata.get("related"),
                    },
                    update_date=created or date.today(),
                )
                final_content = upd["content"]
                action = "updated" if upd["changed"] else "unchanged"

            write_res = safe_write_note(target_path, final_content, validate_properties=True)
            if not write_res["written"] and action == "created":
                action = "unchanged"
            written_paths.append(node.proposed_path)
            rec = {
                "concept_id": cid,
                "title": node.title,
                "role": node.note_role,
                "path": node.proposed_path,
                "status": action,
                "master": (node.template_plan or {}).get("master") or ("index" if "index" in node.note_role else preferences.master),
                "word_count": len(re.findall(r"\b\w+\b", parse_note(final_content).body)),
            }
            if visual_report is not None:
                rec["visual_report"] = visual_report
            records.append(rec)
        except Exception as exc:
            failed_nodes.append({"concept_id": cid, "title": node.title, "path": node.proposed_path, "error": str(exc)})
            records.append({
                "concept_id": cid,
                "title": node.title,
                "role": node.note_role,
                "path": node.proposed_path,
                "status": "failed",
                "error": str(exc),
            })

    # Persist Collection Manifest
    manifest_dir = vault_root / ".scriptorium" / "collections"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / f"{plan.collection_id}.yaml"
    completed_count = sum(1 for r in records if r["status"] in {"created", "updated", "unchanged"})
    manifest = {
        "collection_id": plan.collection_id,
        "content_state": "generated",
        "verified": False,
        "completion_scope": "file generation only; authored content and semantic review remain required",
        "title": plan.title,
        "organization": plan.organization,
        "domain": root_domain,
        "master_topic": root_master_topic,
        "planned_count": len(plan.nodes),
        "completed_count": completed_count,
        "failed_count": len(failed_nodes),
        "complete": completed_count == len(plan.nodes) and not failed_nodes,
        "planned_paths": list(plan.planned_paths),
        "nodes": records,
    }
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")

    return {
        "collection_id": plan.collection_id,
        "content_state": "generated",
        "verified": False,
        "manifest_path": str(manifest_path),
        "planned_count": len(plan.nodes),
        "completed_count": completed_count,
        "failed_count": len(failed_nodes),
        "complete": manifest["complete"],
        "written_paths": written_paths,
        "records": records,
        "failed_nodes": failed_nodes,
        "manifest": manifest,
    }
