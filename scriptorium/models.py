"""Shared data models, error taxonomy, YAML/frontmatter parsing, and caching for Scriptorium."""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
import hashlib
from pathlib import Path
import re
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

# Canonical Obsidian Properties contract (mandatory at top of every generated note).
REQUIRED_OBSIDIAN_PROPERTIES: tuple[str, ...] = (
    "topic",
    "tags",
    "master_topic",
    "domain",
    "note_type",
)

# Historical 5-key built-in note schema (supported for reading/validating legacy notes).
STRICT_KEYS: tuple[str, ...] = ("id", "aliases", "topic", "tags", "nexttopics")

# Supported optional Obsidian Properties (meaningful metadata preserved & validated).
OPTIONAL_OBSIDIAN_PROPERTIES: tuple[str, ...] = (
    "id",
    "aliases",
    "nexttopics",
    "subdomain",
    "concept_ids",
    "parent_topic",
    "collection_id",
    "prerequisites",
    "related",
    "source_mode",
    "source_refs",
    "difficulty",
    "status",
    "created",
    "updated",
    "template_id",
    "coverage_status",
)

ALL_MANAGED_PROPERTIES: frozenset[str] = frozenset(
    REQUIRED_OBSIDIAN_PROPERTIES + OPTIONAL_OBSIDIAN_PROPERTIES
)

CANONICAL_NOTE_TYPES: tuple[str, ...] = (
    "deep-notes",
    "study-notes",
    "quick-reference",
    "worked-solutions",
    "implementation-guide",
    "assessment",
    "synthesis-revision",
    "index",
)

# Single authoritative stack alias mapping (previously duplicated across decision_matrix & instructional_plan).
STACK_NAMES: dict[str, tuple[str, ...]] = {
    "python-numpy": ("numpy", "python + numpy"),
    "scikit-learn": ("sklearn", "python + scikit-learn"),
    "pytorch": ("torch", "python + pytorch"),
    "tensorflow-keras": ("tensorflow", "tf", "keras", "python + tensorflow"),
    "python": ("py", "python3"),
    "cpp": ("c++", "c++20"),
    "c": (),
    "rust": (),
    "sql": ("sqlite", "sqlite3"),
    "javascript": ("js",),
    "typescript": ("ts",),
    "java": (),
    "go": (),
    "csharp": ("c#",),
    "kotlin": (),
}
STACK_ALIASES: dict[str, str] = {
    alias: name for name, aliases in STACK_NAMES.items() for alias in (name, *aliases)
}


# ---------------------------------------------------------------------------
# Unified Error Taxonomy (Section 6.6)
# ---------------------------------------------------------------------------

class ScriptoriumError(ValueError):
    """Base error for Scriptorium engine operations."""
    category: str = "scriptorium_error"


class RoutingError(ScriptoriumError):
    category = "routing_error"


class TemplateResolutionError(ScriptoriumError):
    category = "template_resolution_error"


class SourcePolicyConflictError(ScriptoriumError):
    category = "source_policy_conflict"


class MetadataValidationError(ScriptoriumError):
    category = "metadata_validation_error"


class MissingEvidenceError(ScriptoriumError):
    category = "missing_source_evidence"


class ConceptIdentityError(ScriptoriumError):
    category = "concept_identity_conflict"


class CodeVerificationError(ScriptoriumError):
    category = "code_verification_failure"


class UnsafeUpdateConflictError(ScriptoriumError):
    category = "unsafe_update_conflict"


# ---------------------------------------------------------------------------
# Shared YAML / Frontmatter / Markdown Parsing (Single Implementation)
# ---------------------------------------------------------------------------

class UniqueMappingLoader(yaml.SafeLoader):
    """YAML SafeLoader that rejects duplicate mapping keys."""

    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        mapping = super().construct_mapping(node, deep)
        if len(mapping) != len(node.value):
            raise yaml.YAMLError("Duplicate YAML mapping key.")
        return mapping


def slugify(text: str) -> str:
    """Convert arbitrary text to a lowercase hyphenated slug."""
    s = re.sub(r"[^a-zA-Z0-9]+", "-", str(text or "").strip().lower()).strip("-")
    return s or "note"


def heading_slug(text: str) -> str:
    """Convert a Markdown heading to a GitHub/Obsidian-style anchor slug."""
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", str(text or "").strip())
    s = s.replace("`", "").replace("*", "").replace("~", "").lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def content_hash(text: str | bytes) -> str:
    data = text.encode("utf-8") if isinstance(text, str) else text
    return hashlib.sha256(data).hexdigest()


def normalize_stack(values: list[str]) -> list[str]:
    if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
        raise ValueError("implementation_stack must be a list of supported stack names.")
    try:
        return list(dict.fromkeys(STACK_ALIASES[value.strip().lower()] for value in values))
    except KeyError as exc:
        raise ValueError(f"Unsupported implementation stack: {exc.args[0]}") from exc


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str, int]:
    """Parse leading YAML frontmatter once. Returns (metadata_dict, raw_yaml, body_start_line_0idx)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise MetadataValidationError("Expected opening YAML frontmatter fence.")
    end = next((n for n in range(1, len(lines)) if lines[n].strip() == "---"), None)
    if end is None:
        raise MetadataValidationError("Expected closing YAML frontmatter fence.")
    raw = "\n".join(lines[1:end])
    metadata = yaml.load(raw, Loader=UniqueMappingLoader)
    if not isinstance(metadata, dict):
        raise MetadataValidationError("Frontmatter must be a YAML mapping.")
    return metadata, raw, end + 1


def has_frontmatter(text: str) -> bool:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    return any(line.strip() == "---" for line in lines[1:])


def dump_frontmatter(metadata: dict[str, Any]) -> str:
    """Serialize metadata cleanly to Obsidian-compatible YAML frontmatter."""
    # Ensure string values with YAML-special syntax are cleanly emitted via PyYAML safe_dump.
    dumped = yaml.safe_dump(
        metadata,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=1000,
    )
    return f"---\n{dumped}---"


@dataclass
class MarkdownSection:
    level: int
    heading: str
    slug: str
    start_line: int  # 0-based within body
    end_line: int    # exclusive, 0-based within body
    content: str


@dataclass
class ParsedNote:
    """Single-parse structured representation shared across engines (Section 6.1)."""
    raw_text: str
    content_digest: str
    metadata: dict[str, Any] = field(default_factory=dict)
    raw_frontmatter: str = ""
    body_start_line: int = 0
    body: str = ""
    title: str | None = None
    sections: list[MarkdownSection] = field(default_factory=list)
    code_blocks: list[dict[str, Any]] = field(default_factory=list)
    wikilinks: list[str] = field(default_factory=list)


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_FENCE_RE = re.compile(r"^([`~]{3,})(.*)$")
_WIKILINK_RE = re.compile(r"\[\[([^\]\n]+)\]\]")


def _extract_body_structure(body: str) -> tuple[str | None, list[MarkdownSection], list[dict[str, Any]], list[str]]:
    lines = body.splitlines()
    title: str | None = None
    heading_positions: list[tuple[int, int, str]] = []
    code_blocks: list[dict[str, Any]] = []
    wikilinks: list[str] = []

    fence_marker: str | None = None
    fence_lang = ""
    fence_start = 0
    fence_lines: list[str] = []

    for idx, line in enumerate(lines):
        m_fence = _FENCE_RE.match(line.strip())
        if fence_marker is not None:
            if m_fence and m_fence.group(1)[0] == fence_marker[0] and len(m_fence.group(1)) >= len(fence_marker) and not m_fence.group(2).strip():
                code_blocks.append({
                    "language": fence_lang,
                    "start_line": fence_start,
                    "end_line": idx,
                    "code": "\n".join(fence_lines),
                })
                fence_marker = None
                fence_lines = []
            else:
                fence_lines.append(line)
            continue

        if m_fence:
            fence_marker = m_fence.group(1)
            fence_lang = m_fence.group(2).strip().split(maxsplit=1)[0].lower() if m_fence.group(2).strip() else ""
            fence_start = idx
            fence_lines = []
            continue

        for wl in _WIKILINK_RE.finditer(line):
            wikilinks.append(wl.group(1).split("|", 1)[0].strip())

        m_head = _HEADING_RE.match(line)
        if m_head:
            lvl = len(m_head.group(1))
            text = m_head.group(2).strip()
            if lvl == 1 and title is None:
                title = text
            elif lvl >= 2:
                heading_positions.append((idx, lvl, text))

    sections: list[MarkdownSection] = []
    for pos_idx, (start, lvl, htext) in enumerate(heading_positions):
        end = len(lines)
        for next_start, next_lvl, _ in heading_positions[pos_idx + 1:]:
            if next_lvl <= lvl:
                end = next_start
                break
        sections.append(
            MarkdownSection(
                level=lvl,
                heading=htext,
                slug=slugify(htext),
                start_line=start,
                end_line=end,
                content="\n".join(lines[start:end]),
            )
        )
    return title, sections, code_blocks, wikilinks


@lru_cache(maxsize=256)
def _parse_note_cached(digest: str, text: str) -> ParsedNote:
    metadata: dict[str, Any] = {}
    raw_fm = ""
    body_start = 0
    if has_frontmatter(text):
        metadata, raw_fm, body_start = parse_frontmatter(text)
    lines = text.splitlines()
    body = "\n".join(lines[body_start:])
    title, sections, code_blocks, wikilinks = _extract_body_structure(body)
    return ParsedNote(
        raw_text=text,
        content_digest=digest,
        metadata=metadata,
        raw_frontmatter=raw_fm,
        body_start_line=body_start,
        body=body,
        title=title,
        sections=sections,
        code_blocks=code_blocks,
        wikilinks=wikilinks,
    )


def parse_note(text: str) -> ParsedNote:
    """Parse a Markdown note once (cached by SHA-256 content digest)."""
    return _parse_note_cached(content_hash(text), text)
