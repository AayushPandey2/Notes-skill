"""Shared data models, error taxonomy, YAML/frontmatter parsing, and caching for Scriptorium."""
from __future__ import annotations

import ast
from dataclasses import dataclass, field
from functools import lru_cache
import hashlib
import math
import operator
import os
from pathlib import Path
import re
from typing import Any, Callable

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


def is_within_vault(vault_root: Path, target: Path) -> bool:
    """Verify target resolves strictly inside vault_root (no symlink or traversal escape)."""
    try:
        real_root = os.path.realpath(vault_root)
        real_target = os.path.realpath(target)
        return os.path.commonpath([real_root, real_target]) == real_root
    except ValueError:
        return False


def contained_path(root: Path, relative: str | Path) -> Path:
    """Resolve ``relative`` inside ``root`` and reject path traversal outside ``root``."""
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not is_within_vault(root, path):
        raise ValueError(f"Path escapes vault: {relative}")
    return path


def split_frontmatter_lines(lines: list[str]) -> tuple[list[str], int] | tuple[None, int]:
    """Return ``(yaml_lines, body_start_idx)`` if ``lines`` starts with YAML frontmatter."""
    if not lines or lines[0].strip() != "---":
        return None, 0
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[1:idx], idx + 1
    return None, 0


def heading_slug(heading: str) -> str:
    """Normalize a Markdown heading string into a GitHub/Obsidian anchor slug."""
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading.strip())
    cleaned = cleaned.replace("`", "").replace("*", "").replace("~", "").lower()
    cleaned = re.sub(r"[^\w\s-]", "", cleaned, flags=re.UNICODE)
    return re.sub(r"\s+", "-", cleaned.strip())


def format_wikilink(value: str) -> str:
    """Wrap a note name as ``[[value]]`` unless it is already bracketed."""
    s = value.strip()
    if s.startswith("[[") and s.endswith("]]"):
        return s
    return f"[[{s}]]"


_SAFE_BINOPS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}
_SAFE_UNARYOPS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}
_SAFE_MATH_FUNCS: dict[str, Callable[..., float]] = {
    "abs": abs,
    "sqrt": math.sqrt,
    "exp": math.exp,
    "log": math.log,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "max": max,
    "min": min,
}


def safe_eval_expr(
    expression: str,
    variables: dict[str, float] | None = None,
    *,
    allow_functions: bool = False,
    allow_constants: bool = False,
    normalize_equation: bool = False,
) -> float:
    """Safely evaluate a pure mathematical expression via Python AST (never raw eval())."""
    env = variables or {}
    cleaned = expression.strip()
    if normalize_equation:
        cleaned = cleaned.replace("^", "**")
        if "=" in cleaned:
            _, cleaned = cleaned.split("=", 1)
            cleaned = cleaned.strip()
    tree = ast.parse(cleaned, mode="eval")

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Name):
            if node.id in env:
                return float(env[node.id])
            if allow_constants and node.id == "pi":
                return math.pi
            if allow_constants and node.id == "e":
                return math.e
            raise ValueError(f"Unknown variable '{node.id}' in expression '{expression}'.")
        if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_BINOPS:
            return float(_SAFE_BINOPS[type(node.op)](_eval(node.left), _eval(node.right)))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _SAFE_UNARYOPS:
            return float(_SAFE_UNARYOPS[type(node.op)](_eval(node.operand)))
        if allow_functions and isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in _SAFE_MATH_FUNCS:
            return float(_SAFE_MATH_FUNCS[node.func.id](*[_eval(a) for a in node.args]))
        raise ValueError(f"Unsupported arithmetic construct in expression: {expression!r}")

    return _eval(tree)


# ---------------------------------------------------------------------------
# Replacement Architecture Typed Content Records (Shared Pipeline Contracts)
# ---------------------------------------------------------------------------

@dataclass
class ConceptPlanRecord:
    """Typed concept specification shared across intake, planning, authoring, and validation."""
    concept_id: str
    canonical_name: str
    learning_objective: str
    prerequisites: list[str] = field(default_factory=list)
    selected_depth: int = 3
    definitions: dict[str, str] = field(default_factory=dict)
    notation: dict[str, dict[str, Any]] = field(default_factory=dict)
    evidence_refs: list[str] = field(default_factory=list)
    formula_requirements: list[str] = field(default_factory=list)
    visual_requirements: list[str] = field(default_factory=list)
    assessment_requirements: list[str] = field(default_factory=list)


@dataclass
class FormulaTeachingRecord:
    """Owned atomic formula + folded walkthrough contract."""
    formula_id: str
    expression: str
    concept_owner: str
    purpose: str
    plain_reading: str
    symbols: list[dict[str, Any]] = field(default_factory=list)
    shapes_units_domains: list[str] = field(default_factory=list)
    operation_sequence: list[str] = field(default_factory=list)
    derivation_reasoning: str = ""
    numerical_example: dict[str, Any] = field(default_factory=dict)
    interpretation: str = ""
    assumptions: list[str] = field(default_factory=list)
    misconceptions: list[str] = field(default_factory=list)
    validation_status: str = "pending"
    placement: str = "prose"  # prose | worked_example | assessment | appendix | table | source


@dataclass
class AssetRecord:
    """Verified external raster image or local media asset record."""
    asset_id: str
    asset_type: str  # raster_web | video_frame | mermaid | table | interactive
    concept_owner: str
    instructional_role: str
    source_page_url: str = ""
    acquisition_url: str = ""
    local_path: str = ""
    sha256: str = ""
    width: int | None = None
    height: int | None = None
    detected_format: str = ""
    attribution: str = ""
    rights: str = ""
    inspection_status: str = "uninspected"
    verification_status: str = "pending"  # verified | failed | unmet_visual_obligation | pending
    failure_reason: str = ""


@dataclass
class VideoEvidenceRecord:
    """Video transcript, frame sequence, and explicit access-mode contract."""
    video_id: str
    source_access_mode: str  # full_multimodal | transcript_plus_frames | transcript_only | media_only | metadata_only
    source_url: str = ""
    transcript_intervals: list[dict[str, Any]] = field(default_factory=list)
    acquisition_method: str = ""
    frame_records: list[dict[str, Any]] = field(default_factory=list)
    concept_alignment: list[dict[str, Any]] = field(default_factory=list)
    confidence: str = "medium"
    uncertainty_notes: list[str] = field(default_factory=list)
    provenance_separation: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class PublicationQualityStatus:
    """Unified structural + semantic + safety verification summary."""
    passed: bool
    structural_checks: dict[str, Any] = field(default_factory=dict)
    semantic_checks: dict[str, Any] = field(default_factory=dict)
    partial_visual_coverage: bool = False
    partial_video_coverage: bool = False
    protected_hashes_verified: bool = True
    warnings: list[str] = field(default_factory=list)


@dataclass
class DisplayMathBlock:
    """Parsed Markdown display-math block and its immediately attached folded explanation."""
    index: int
    expression: str
    start_line: int
    end_line: int
    quote_depth: int = 0
    in_list: bool = False
    in_callout: bool = False
    callout_type: str | None = None
    has_following_fold: bool = False
    fold_header: str = ""
    fold_start_line: int | None = None
    fold_end_line: int | None = None
    fold_body: str = ""
    nested_inside_formula_fold: bool = False


_FENCE_LINE_RE = re.compile(r"^\s*(```+|~~~+)(.*)$")
_CALLOUT_HEADER_RE = re.compile(r"^\[!([A-Za-z0-9_-]+)\]([+-])?\s*(.*)$")


def _strip_quote_prefix(line: str) -> tuple[int, str]:
    depth = 0
    rest = line.lstrip()
    while rest.startswith(">"):
        depth += 1
        rest = rest[1:]
        if rest.startswith(" "):
            rest = rest[1:]
        rest = rest.lstrip() if rest.startswith(">") else rest
    return depth, rest


def _unescaped_dd_positions(line: str) -> list[int]:
    """Return column offsets of unescaped '$$' outside inline backtick code spans."""
    positions: list[int] = []
    i = 0
    n = len(line)
    in_tick = 0
    while i < n:
        ch = line[i]
        if ch == "\\" and in_tick == 0:
            i += 2
            continue
        if ch == "`":
            run = 1
            while i + run < n and line[i + run] == "`":
                run += 1
            if in_tick == 0:
                in_tick = run
            elif run == in_tick:
                in_tick = 0
            i += run
            continue
        if in_tick == 0 and ch == "$" and i + 1 < n and line[i + 1] == "$":
            positions.append(i)
            i += 2
            continue
        i += 1
    return positions


def scan_display_math_blocks(text: str) -> list[DisplayMathBlock]:
    """Scan Markdown note text for display $$...$$ blocks and attached folded explanations.

    Ignores YAML frontmatter, fenced code blocks, inline code spans, HTML comments,
    and escaped \\$ / currency symbols; handles blockquotes, callouts, and list items.
    """
    raw_lines = text.splitlines()
    fm_lines, start_idx = split_frontmatter_lines(raw_lines)
    if fm_lines is None:
        start_idx = 0

    blocks: list[DisplayMathBlock] = []
    fence_marker: str | None = None
    in_html_comment = False
    open_math: dict[str, Any] | None = None
    callout_stack: list[tuple[int, str, bool]] = []  # (depth, ctype, is_formula_fold)

    idx = start_idx
    while idx < len(raw_lines):
        lineno = idx + 1
        raw_line = raw_lines[idx]
        qdepth, stripped = _strip_quote_prefix(raw_line)
        while callout_stack and (qdepth < callout_stack[-1][0] or (qdepth == 0 and not raw_line.strip().startswith(">"))):
            callout_stack.pop()

        if in_html_comment:
            if "-->" in stripped:
                in_html_comment = False
            idx += 1
            continue
        if stripped.lstrip().startswith("<!--") and "-->" not in stripped:
            in_html_comment = True
            idx += 1
            continue
        stripped_no_comment = re.sub(r"<!--.*?-->", "", stripped)

        fm = _FENCE_LINE_RE.match(stripped_no_comment)
        if fence_marker is not None:
            if fm and fm.group(1)[0] == fence_marker[0] and len(fm.group(1)) >= len(fence_marker) and not fm.group(2).strip():
                fence_marker = None
            idx += 1
            continue
        if fm:
            fence_marker = fm.group(1)
            idx += 1
            continue

        cm = _CALLOUT_HEADER_RE.match(stripped_no_comment.strip()) if qdepth > 0 else None
        if cm:
            ctype = cm.group(1).lower()
            title_low = cm.group(3).strip().lower()
            is_formula_fold = (ctype == "example" and (
                "understand this formula" in title_low or "formula step by step" in title_low or "step-by-step" in title_low or "equation walkthrough" in title_low
            ))
            callout_stack.append((qdepth, ctype, is_formula_fold))
            idx += 1
            continue

        dd_pos = _unescaped_dd_positions(stripped_no_comment)
        if open_math is not None:
            if dd_pos:
                tail = stripped_no_comment[:dd_pos[0]]
                open_math["parts"].append(tail)
                blocks.append(DisplayMathBlock(
                    index=len(blocks) + 1,
                    expression="\n".join(open_math["parts"]).strip(),
                    start_line=open_math["start_line"],
                    end_line=lineno,
                    quote_depth=open_math["qdepth"],
                    in_list=open_math["in_list"],
                    in_callout=open_math["in_callout"],
                    callout_type=open_math["callout_type"],
                    nested_inside_formula_fold=open_math["nested_fold"],
                ))
                open_math = None
            else:
                open_math["parts"].append(stripped_no_comment)
        elif dd_pos:
            in_list = bool(re.match(r"^\s*(?:[-*+]|\d+\.)\s+", stripped_no_comment))
            active_ctype = callout_stack[-1][1] if callout_stack else None
            nested_fold = any(item[2] for item in callout_stack)
            if len(dd_pos) >= 2:
                expr = stripped_no_comment[dd_pos[0] + 2:dd_pos[1]].strip()
                blocks.append(DisplayMathBlock(
                    index=len(blocks) + 1,
                    expression=expr,
                    start_line=lineno,
                    end_line=lineno,
                    quote_depth=qdepth,
                    in_list=in_list,
                    in_callout=bool(callout_stack),
                    callout_type=active_ctype,
                    nested_inside_formula_fold=nested_fold,
                ))
            else:
                head = stripped_no_comment[dd_pos[0] + 2:]
                open_math = {
                    "parts": [head],
                    "start_line": lineno,
                    "qdepth": qdepth,
                    "in_list": in_list,
                    "in_callout": bool(callout_stack),
                    "callout_type": active_ctype,
                    "nested_fold": nested_fold,
                }
        idx += 1

    # Attach immediately following collapsed formula explanation callouts
    for blk in blocks:
        scan_i = blk.end_line  # 0-based index of line immediately after end_line
        while scan_i < len(raw_lines):
            q, s = _strip_quote_prefix(raw_lines[scan_i])
            if s.strip() == "" and q <= blk.quote_depth:
                scan_i += 1
                continue
            break
        if scan_i < len(raw_lines):
            q, s = _strip_quote_prefix(raw_lines[scan_i])
            cm = _CALLOUT_HEADER_RE.match(s.strip())
            if q > 0 and cm and cm.group(2) == "-" and cm.group(1).lower() in {"example", "note", "tip"}:
                fold_lines: list[str] = []
                f_end = scan_i + 1
                j = scan_i + 1
                while j < len(raw_lines):
                    fq, fs = _strip_quote_prefix(raw_lines[j])
                    if fq < q or (fq == 0 and raw_lines[j].strip() != ""):
                        break
                    if fq == 0 and raw_lines[j].strip() == "":
                        break
                    fold_lines.append(fs)
                    f_end = j + 1
                    j += 1
                blk.has_following_fold = True
                blk.fold_header = s.strip()
                blk.fold_start_line = scan_i + 1
                blk.fold_end_line = f_end
                blk.fold_body = "\n".join(fold_lines).strip()

    return blocks
