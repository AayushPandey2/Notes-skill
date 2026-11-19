#!/usr/bin/env python3
"""Lint a built-in Scriptorium note; optionally resolve vault links."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, urlsplit

import json
import yaml

from note_layout import ADAPTIVE_ROUTES, BEHAVIOR_TABLE, DEEP_ROUTES, HINT, NARROW_RANGES, PRACTICE_RANGES, ROUTES, SOLUTION, SYMBOL_TABLE, matches_legacy_study, matches_layout, optional_headings, heading_key
from note_verification import FENCE, check_python, quoted_line as _strip_quotes, split_blocks
from vault_index import is_within_vault, resolve_vault_root
from verify_vault_notes import RAW_LATEX_IN_YAML_RE, UNRESOLVED_TPL_RE, _extract_anchors_and_blocks, _heading_slug, build_vault_index

from contracts import STRICT_KEYS as STRICT_KEYS
REQUIRED = set(STRICT_KEYS)
TOKEN = re.compile(r"(" + chr(96) + r"+|\$+)")
QUESTION = re.compile(r"^### Q(\d+)\. (\S.*)$")
WIKILINK = re.compile(r"\[\[([^\]\n]+)\]\]")
ASSET_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp", ".pdf"}
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
WORD = re.compile(r"[\w]+(?:[-'’][\w]+)*", re.UNICODE)
VIDEO_TIMESTAMP = re.compile(r"\[(\d{2,}):([0-5]\d)\]\((https?://[^\s)]+)\)")


class UniqueMappingLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        mapping = super().construct_mapping(node, deep)
        if len(mapping) != len(node.value):
            raise yaml.YAMLError("Duplicate YAML mapping key.")
        return mapping


def read_frontmatter(text: str) -> tuple[dict, str, int]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Expected opening YAML frontmatter fence.")
    end = next((n for n in range(1, len(lines)) if lines[n].strip() == "---"), None)
    if end is None:
        raise ValueError("Expected closing YAML frontmatter fence.")
    raw = "\n".join(lines[1:end])
    metadata = yaml.load(raw, Loader=UniqueMappingLoader)
    if not isinstance(metadata, dict):
        raise ValueError("Frontmatter must be a YAML mapping.")
    return metadata, raw, end + 1


def _escaped(text: str, position: int) -> bool:
    prefix = text[:position]
    return (len(prefix) - len(prefix.rstrip("\\"))) % 2 == 1


def _inline(line: str, lineno: int, math: int, report) -> tuple[str, int, int]:
    """Mask matched code spans and track delimiter width across display lines."""
    masked = line
    tokens = list(TOKEN.finditer(line))
    displays = 0
    i = 0
    while i < len(tokens):
        match = tokens[i]
        token = match[0]
        i += 1
        if _escaped(line, match.start()):
            continue
        if token.startswith(chr(96)):
            end = next((k for k in range(i, len(tokens)) if tokens[k][0] == token), None)
            if end is not None:
                if math:
                    report(lineno, "Inline code inside math.")
                stop = tokens[end].end()
                masked = masked[:match.start()] + " " * (stop - match.start()) + masked[stop:]
                i = end + 1
        elif len(token) > 2:
            report(lineno, "Use only $ and $$ as math delimiters.")
        elif not math:
            math = len(token)
            displays += math == 2
        elif math != len(token):
            report(lineno, "Mismatched math delimiter widths.")
        else:
            math = 0
    if math == 1:
        report(lineno, "Unclosed inline math.")
        math = 0
    return masked, math, displays


def _mermaid(lines: list[str], start: int, report, *, adaptive: bool = False) -> None:
    meaningful = [(start + i, line.strip()) for i, line in enumerate(lines, 1)
                  if line.strip() and not line.lstrip().startswith("%%")]
    if adaptive and any("$" in line for _, line in meaningful):
        report(start, "Use Unicode rather than raw math delimiters in Mermaid.")
    if adaptive and len(meaningful) >= 2 and meaningful[0][1] not in {"flowchart TD", "sequenceDiagram"}:
        # This lightweight linter cannot parse every Mermaid grammar. Allow the
        # selected visual form; rendering remains a separate authoring check.
        if not re.fullmatch(r"(?:stateDiagram(?:-v2)?|timeline|mindmap|gantt|classDiagram|erDiagram|"
                            r"(?:flowchart|graph)\s+(?:TD|TB|BT|LR|RL))", meaningful[0][1]):
            report(start, "Unrecognized Mermaid diagram type; check rendering with Mermaid.")
        return
    if len(meaningful) < 2 or meaningful[0][1] not in {"flowchart TD", "sequenceDiagram"}:
        report(start, "Expected a nonempty Mermaid flowchart TD or sequenceDiagram.")
        return
    flow = meaningful[0][1] == "flowchart TD"
    ident = r"[A-Za-z_][\w-]*"
    quote = r'"[^"\n]+"'
    label = rf'(?:\[\[?{quote}\]\]?|\(\(?{quote}\)\)?|\{{\{{?{quote}\}}\}}?|\[\({quote}\)\])'
    node = rf"{ident}(?:{label})?"
    edge = r'(?:-->|---|-.->|==>|--\s*"[^"]*"\s*-->)\s*(?:\|[^|]+\|\s*)?'
    statement = re.compile(rf"{node}(?:\s*{edge}\s*{node})*;?")
    sequence = re.compile(
        rf"(?:{ident}\s*(?:--?>>?|--?[x)])[-+]?\s*{ident}\s*:\s*\S.*"
        rf"|(?:participant|actor)\s+{ident}(?:\s+as\s+{quote})?"
        rf"|(?:loop|alt|else|opt|par|and|critical|option|break|rect)\s+\S.*|end"
        rf"|(?:activate|deactivate)\s+{ident}|[Nn]ote\s+(?:over|left of|right of)\s+{ident}(?:,{ident})?\s*:\s*\S.*)"
    )
    blocks = []
    for number, line in meaningful[1:]:
        if "$" in line:
            report(number, "Use Unicode rather than raw math delimiters in Mermaid.")
        if flow and line.startswith("subgraph "):
            if not re.fullmatch(rf'subgraph\s+(?:{quote}|{node})', line):
                report(number, "Malformed Mermaid subgraph or unquoted label.")
            blocks.append(line)
        elif not flow and re.match(r"^(?:loop|alt|opt|par|critical|rect|break)\s+", line):
            blocks.append(line)
        elif line == "end":
            if blocks:
                blocks.pop()
            else:
                report(number, "Unexpected Mermaid end.")
        elif not (statement if flow else sequence).fullmatch(line):
            report(number, "Malformed Mermaid statement or unquoted node label.")
    if blocks:
        report(start, "Unclosed Mermaid block.")


def _pipes(line: str) -> list[int]:
    return [i for i, char in enumerate(line) if char == "|" and not _escaped(line, i)]


def _table_cells(line: str) -> list[str]:
    positions = [-1, *_pipes(line), len(line)]
    cells = [line[a + 1:b].strip() for a, b in zip(positions, positions[1:])]
    if not cells[0]:
        cells = cells[1:]
    if cells and not cells[-1]:
        cells = cells[:-1]
    return cells


def _table_sizes(lines: list[tuple[int, str]], report) -> dict[str, int]:
    tables = {}
    i = 1
    while i < len(lines):
        number, line = lines[i]
        cells = _table_cells(line)
        if len(cells) < 1 or not _pipes(line) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            i += 1
            continue
        header_number, header = lines[i - 1]
        if header_number + 1 != number or not _pipes(header) or len(_table_cells(header)) != len(cells):
            report(number, "Table header and separator have different widths. Escape literal pipes.")
        i += 1
        count = 0
        while i < len(lines) and lines[i][0] == number + count + 1 and _pipes(lines[i][1]):
            row_number, row = lines[i]
            if len(_table_cells(row)) != len(cells):
                report(row_number, "Table row width differs from the header. Escape literal pipes.")
            count += 1
            i += 1
        tables[header.strip()] = count
    return tables


def _practice(lines: list[tuple[int, str]], narrow: bool, report) -> None:
    boundaries = [i for i, (_, line) in enumerate(lines) if line.startswith("## ") or QUESTION.fullmatch(line)]
    buckets = {1: [], 2: [], 3: []}
    tier = 0
    recognized = set()
    for pos, i in enumerate(boundaries):
        number, line = lines[i]
        if line.startswith("## "):
            tier += 1
            continue
        question = int(QUESTION.fullmatch(line)[1])
        if tier not in buckets:
            report(number, "Practice questions belong in Tiers 1–3.")
            continue
        buckets[tier].append(question)
        end = boundaries[pos + 1] if pos + 1 < len(boundaries) else len(lines)
        block = lines[i + 1:end]
        slots = [n for n, (_, row) in enumerate(block) if row.strip().startswith(("> [!hint]", "> [!tip]"))]
        recognized.update(block[n][0] for n in slots)
        if [block[n][1].strip() for n in slots] != [HINT, SOLUTION]:
            report(number, "Each practice question needs exactly one collapsed hint then one collapsed solution.")
            continue
        first, second = slots
        if second == 0 or block[second - 1][1].strip():
            report(block[second][0], "Separate the callouts with an unquoted blank line.")
        for start, stop in ((first, second), (second, len(block))):
            content = block[start + 1:stop]
            while content and not content[-1][1].strip():
                content.pop()
            if not any(row.strip() not in {"", ">"} for _, row in content):
                report(block[start][0], "Callout body is empty.")
            for row_number, row in content:
                if not row.lstrip().startswith(">"):
                    report(row_number, "Prefix each callout line, including interior blank lines, with >.")
    for number, line in lines:
        if line.strip().startswith(("> [!hint]", "> [!tip]")) and number not in recognized:
            report(number, "Practice callout is outside a question.")
    ordered = buckets[1] + buckets[2] + buckets[3]
    min_q, max_q = (10, 14) if narrow else (15, 20)
    if any(not buckets[t] for t in (1, 2, 3)):
        report(1, "Each of Tiers 1–3 must contain at least one question.")
    elif ordered != list(range(1, len(ordered) + 1)) or not (min_q <= len(ordered) <= max_q):
        report(1, f"Practice tiers must contain consecutive questions Q1–Q{len(ordered)} within {min_q}–{max_q} total questions.")


def _link_checks(text: str, visible: list[tuple[int, str]], metadata: dict, vault: Path, target: Path,
                 planned, index, report) -> None:
    index = index if index is not None else build_vault_index(vault)
    targets = {target, *planned, *index["anchors_by_file"]}
    anchors, blocks = _extract_anchors_and_blocks(text)
    note_id = metadata.get("id")
    if isinstance(note_id, str) and any(path != target for path in index["ids_to_files"].get(note_id, ())):
        report(1, f"Duplicate YAML id: {note_id}")
    for number, line in visible:
        for match in WIKILINK.finditer(line):
            ref = re.split(r"\\?\|", match[1], maxsplit=1)[0]
            name, _, anchor = ref.partition("#")
            if Path(name.strip()).suffix.lower() in ASSET_EXTS:
                asset = name.strip().lstrip("/")
                if not ((vault / asset).is_file() or any(vault.rglob(Path(asset).name))):
                    report(number, f"Unresolved asset embed: {name}")
                continue
            key = re.sub(r"\.md$", "", name.strip(), flags=re.I).replace("\\", "/").casefold()
            if not key:
                resolved = target
            else:
                candidates = [p for p in targets if p.relative_to(vault).with_suffix("").as_posix().casefold() == key]
                if not candidates:
                    candidates = [p for p in targets if p.stem.casefold() == key]
                if len(candidates) > 1:
                    report(number, f"Ambiguous wikilink: {name}. Use a vault-relative path.")
                    continue
                resolved = candidates[0] if candidates else (
                    index["aliases"].get(key) or index["titles"].get(key) or index["ids_map"].get(key)
                )
            if resolved is None:
                report(number, f"Unresolved wikilink: {name}")
            elif anchor:
                is_block = anchor.startswith("^")
                lookup = index["blocks_by_file" if is_block else "anchors_by_file"]
                known = (blocks if is_block else anchors) if resolved == target else lookup.get(resolved, set())
                raw = anchor.removeprefix("^").strip().lower()
                if raw not in known and (is_block or _heading_slug(raw) not in known):
                    report(number, f"Unresolved wikilink anchor: {ref}")


def _infer_route_and_level(clean: str, headings: list[str], route: str | None, math_level: int | None) -> tuple[str | None, int]:
    if math_level is not None:
        level = math_level
    elif "> [!abstract] Key Equations" not in clean:
        level = 0
    elif "### Mathematical Intuition" in clean or "### Boundary & Limit Analysis" in clean or "*Why this step holds:*" in clean:
        level = 2
    else:
        level = 1

    if route is not None:
        return route, level
    narrow = any("Q1–Q3" in h for h in headings)
    for cand in ROUTES:
        if cand in DEEP_ROUTES:
            continue
        if matches_layout(cand, level, headings, narrow=(cand == "practice" and narrow)):
            return cand, level
    if matches_legacy_study(headings):
        return "studynotes", level
    return None, level


def validate_text(text: str, *, vault: Path | None = None, target: Path | None = None,
                  planned=(), index=None, route: str | None = None, math_level: int | None = None,
                  decision_contract: dict | None = None) -> list[tuple[int, str]]:
    findings = []

    def report(number, message):
        findings.append((number, message))

    try:
        metadata, raw, start = read_frontmatter(text)
    except (ValueError, yaml.YAMLError) as exc:
        return [(1, str(exc))]
    keys = list(metadata.keys())
    missing = [key for key in STRICT_KEYS if key not in metadata]
    extra = [key for key in keys if key not in STRICT_KEYS]
    for key in missing:
        report(1, f"Missing frontmatter key: {key}")
    for key in extra:
        report(1, f"Unauthorized frontmatter key: {key}")
    if not missing and not extra and keys != list(STRICT_KEYS):
        report(1, "Frontmatter keys must be strictly ordered: id, aliases, topic, tags, nexttopics.")
    for key in ("id", "topic"):
        if not isinstance(metadata.get(key), str) or not metadata[key].strip():
            report(1, f"{key} must be nonempty text.")
    for key in ("aliases", "tags", "nexttopics"):
        if not isinstance(metadata.get(key), list):
            report(1, f"{key} must be a list.")
    aliases = metadata.get("aliases")
    if isinstance(aliases, list) and (not aliases or any(not isinstance(alias, str) or not alias.strip() for alias in aliases)):
        report(1, "Aliases must contain at least one nonempty string.")
    tags = metadata.get("tags")
    if route is None and isinstance(tags, list) and any(tag in DEEP_ROUTES for tag in tags if isinstance(tag, str)):
        route = "deepstudy-master"
    if isinstance(tags, list) and (not tags or any(not isinstance(tag, str) or
                                                 not re.fullmatch(r"[\w/-]+", tag) for tag in tags)):
        report(1, "Tags must contain valid Obsidian tags. Prefer kebab-case for new tags.")
    nexttopics = metadata.get("nexttopics")
    if isinstance(nexttopics, list) and any(not isinstance(item, str) or not item.strip() for item in nexttopics):
        report(1, "nexttopics must contain only nonempty strings.")
    if "$" in raw or RAW_LATEX_IN_YAML_RE.search(raw):
        report(1, "Raw LaTeX in frontmatter.")
    if route is not None and route not in ROUTES:
        report(1, f"Unknown built-in route: {route}")
        return findings
    levels = (0, 1, 2, 3) if route in DEEP_ROUTES else (0, 1, 2)
    if math_level is not None and (type(math_level) is not int or math_level not in levels):
        report(1, f"math_level must be one of {levels} for this route.")
        return findings
    if math_level is not None and (decision_contract or {}).get("domain") and math_level != decision_contract.get("math_level"):
        report(1, "math_level differs from the saved decision contract.")
        return findings

    body = "\n".join(text.splitlines()[start:])
    for line, message in check_python(split_blocks(body)[0]):
        report(start + line, message)
    if "[OPTIONAL]" in body:
        report(start + 1, "Remove optional authoring markers before emission.")
    if re.search(r"<!--\s*scaffold:", body) or UNRESOLVED_TPL_RE.search(body):
        report(start + 1, "Unresolved scaffold or template field.")
    if re.search(r"<!--\s*SECTION:\s*S\d+[^>]*-->", body, re.I):
        report(start + 1, "Legacy <!-- SECTION: S* --> marker is forbidden; remove all section comments and use domain-natural headings.")
    if re.search(r"<!--\s*(?:Gate:|decision-contract:)", body, re.I):
        report(start + 1, "Remove authoring gates and decision records from the finished note.")
    clean = HTML_COMMENT.sub(lambda m: "\n" * m[0].count("\n"), body)
    prose, visible, structure, wording = [], [], [], []
    math, displays, preview_displays = 0, 0, 0
    preview = False
    preview_count = 0
    fence = None
    widget_end = None
    for number, original in enumerate(clean.splitlines(), start + 1):
        depth, line = _strip_quotes(original)
        marker = FENCE.match(line)
        if fence:
            opened, quote_depth, lang, first, contents = fence
            if depth == quote_depth and marker and marker[1][0] == opened[0] and len(marker[1]) >= len(opened) and not marker[2].strip():
                if lang == "mermaid":
                    _mermaid(contents, first, report, adaptive=route in DEEP_ROUTES)
                if lang == "dataviewjs":
                    js = "\n".join(contents)
                    if (re.search(r'\btext:\s*["\']Mark Revisited["\']', js)
                            and re.search(r'\bcreateEl\(\s*["\']button["\']', js)
                            and "app.vault.modify" in js and "**Revisited** ::" in js):
                        widget_end = number
                fence = None
            else:
                contents.append(line)
                if lang != "dataviewjs":
                    wording.append(original)
            structure.append((number, original if depth else ""))
            continue
        if marker:
            if math:
                report(number, "Fenced code inside math.")
            info = marker[2].strip().lower().split(maxsplit=1)
            fence = (marker[1], depth, info[0] if info else "", number, [])
            structure.append((number, original if depth else ""))
            continue
        structure.append((number, original))
        if original == "> [!abstract] Key Equations":
            preview_count += 1
            preview = True
        elif depth == 0:
            preview = False
        masked, math, count = _inline(line, number, math, report)
        displays += count
        preview_displays += count if preview else 0
        visible.append((number, masked))
        prose.append((number, original))
        wording.append(original)
    if fence:
        report(fence[3], "Unclosed Markdown fence.")
    if math:
        report(start + 1, "Unclosed display math.")
    tables = _table_sizes([(n, _strip_quotes(row)[1]) for n, row in prose], report)
    headings = [row for _, row in prose if row.startswith("## ")]
    route, level = _infer_route_and_level(clean, headings, route, math_level)
    if route in {"summary", "studynotes"}:
        for number, row in visible:
            for match in VIDEO_TIMESTAMP.finditer(row):
                source = urlsplit(match[3])
                if (source.hostname or "").removeprefix("www.") in {"youtube.com", "youtu.be", "m.youtube.com"}:
                    seconds = int(match[1]) * 60 + int(match[2])
                    if parse_qs(source.query).get("t") != [f"{seconds}s"]:
                        report(number, "YouTube timestamp label must match the t=<seconds>s URL parameter.")
    legacy_study = route == "studynotes" and matches_legacy_study(headings) and not (decision_contract or {}).get("domain")
    if route in ADAPTIVE_ROUTES and not legacy_study:
        if route == "studynotes":
            if not matches_layout(route, level, headings):
                report(start + 1, "Study notes need the required sections in template order with consecutive numbering.")
            if not any(row.strip() == "> [!info] Source & Scope Context" for _, row in prose):
                report(start + 1, "Study notes need the Source & Scope Context callout.")
        if sum(row.startswith("# ") for _, row in prose) != 1:
            report(start + 1, "Expected exactly one H1 title.")
        if not any(row.strip() and not row.startswith("#") for _, row in prose):
            report(start + 1, "The note has no authored explanation.")
        for i, (line_no, row) in enumerate(prose):
            if re.match(r"^#{2,6} ", row):
                tail = [value for value in clean.splitlines()[line_no - start:] if value.strip()]
                # Nested sections are valid content; reject only an empty peer/ancestor section.
                next_heading = re.match(r"^(#{1,6}) ", tail[0]) if tail else None
                if not tail or (next_heading and len(next_heading[1]) <= len(row.split()[0])):
                    report(line_no, "Empty section heading.")
        if "Authoring gate" in clean or "**Decision-matrix IDs:**" in clean:
            report(start + 1, "Remove authoring gates from the finished note.")
        from decision_matrix import audit_note_against_contract, check_slug_and_forward_links, resolve_decisions
        if decision_contract is not None:
            contract = {**decision_contract, "explicit_contract": True}
            if "domain" not in contract:
                # Saved plans keep the publishing checks that existed when they were created.
                contract["math_level"] = None
                contract["verify_stack"] = False
        else:
            topic = str(metadata.get("topic") or "")
            title = aliases[0] if isinstance(aliases, list) and aliases else ""
            contract = resolve_decisions(
                "",
                {"title": title, "template": route,
                 "math_level": math_level},
                topic,
                tags=tags if isinstance(tags, list) else None,
            )
            if math_level is None:
                # The chosen level and any explicit override live in planning state.
                contract["math_level"] = None
            elif "clamped_from" in contract:
                report(start + 1, f"Requested math_level {math_level} exceeds the effective level {contract['math_level']} for {contract['domain']}.")
        for c_line, c_msg in audit_note_against_contract(body, contract):
            report(start + c_line, c_msg)
        existing_stems = None
        if vault is not None:
            idx_data = index if index is not None else build_vault_index(vault)
            existing_stems = {p.stem.casefold() for p in idx_data["anchors_by_file"]} | {Path(p).stem.casefold() for p in planned}
        for s_line, s_msg in check_slug_and_forward_links(
            body,
            metadata=metadata,
            target_filename=target.name if target else None,
            existing_stems=existing_stems,
        ):
            report(start + s_line, s_msg)
        if vault is not None and target is not None:
            yaml_links = [(n, row) for n, row in enumerate(raw.splitlines(), 2)]
            _link_checks(text, yaml_links + visible, metadata, vault, target, planned, index, report)
        return findings
    if route is None:
        report(start + 1, "Section headings or ordering do not match any built-in template.")
        return findings
    optional = set(optional_headings(route))
    for pos, (n, row) in enumerate(prose):
        if row.startswith("## ") and heading_key(row) in optional:
            end = next((j for j in range(pos+1, len(prose)) if prose[j][1].startswith("## ")), len(prose))
            contents = "\n".join(value for _, value in prose[pos+1:end])
            for field in ("Context", "Analysis", "Check"):
                if not re.search(rf"\*\*{field}:\*\*\s*\S", contents):
                    report(n, f"Optional module needs a nonempty {field} field.")
    narrow = route == "practice" and any("Q1–Q3" in h for h in headings)
    if not legacy_study and not matches_layout(route, level, headings, narrow=narrow):
        report(start + 1, "Section headings or ordering differ from the selected template.")
    if sum(row.startswith("# ") for _, row in prose) != 1:
        report(start + 1, "Expected exactly one H1 title.")
    if route in {"api-table", "cheat-sheet", "summary"} and level >= 2:
        from decision_matrix import classify_domain
        title = aliases[0] if isinstance(aliases, list) and aliases else ""
        domain = (decision_contract or {}).get("domain") or classify_domain(str(metadata.get("topic") or ""), str(title))
        if domain != "pure-mathematics":
            report(start + 1, f"{route} accepts at most math_level 1 outside pure mathematics.")
    if decision_contract and decision_contract.get("verify_stack"):
        from decision_matrix import audit_note_against_contract

        for line, message in audit_note_against_contract(body, decision_contract):
            report(start + line, message)
    if route != "practice":
        if level == 0:
            if displays or preview_count:
                report(start + 1, "math_level 0 omits formal display equations and equation callouts.")
        else:
            if preview_count != 1 or not 1 <= preview_displays <= 3 or displays <= preview_displays:
                report(start + 1, "Include 1–3 Key Equations and a governing display equation in the body.")
            if not tables.get(SYMBOL_TABLE[0]):
                report(start + 1, "Missing Complete Symbol Anatomy table.")
            if tables.get(BEHAVIOR_TABLE[0]) != 4:
                report(start + 1, "Input-to-Output Behavior table must have four data rows.")
        if level == 2:
            for required in ("Mathematical Intuition", "Boundary & Limit Analysis", "Overgeneralization Counterexample"):
                if not any(row == f"### {required}" for _, row in prose):
                    report(start + 1, f"Missing level 2 section: {required}")
            if "*Why this step holds:*" not in clean:
                report(start + 1, "Missing zero-skip derivation justification.")

    if route == "practice":
        _practice(structure, narrow, report)
    if route != "practice":
        if not any(re.match(r"^\*\*Confusion\*\*\s*::\s*(?!None\s*$)\S", row, re.I) for _, row in prose):
            report(start + 1, "Missing specific **Confusion** :: field.")
        for field in ("What I learned", "Atomize", "Connection"):
            if not any(re.match(rf"^- \*\*{field}\*\*:\s*\S", row) for _, row in prose):
                report(start + 1, f"Missing reflection field: {field}")
        if widget_end is None or any(row.strip() for n, row in prose if n > widget_end):
            report(start + 1, "Missing trailing DataviewJS Mark Revisited widget.")
    if route in {"cheat-sheet", "atomic"}:
        words = sum(len(WORD.findall(row)) for row in wording)
        limit = 350 if route == "cheat-sheet" else 149
        if words > limit:
            report(start + 1, f"Body has {words} words; maximum is {limit}.")
        if route == "cheat-sheet":
            bullet = None
            for n, row in prose + [(0, "")]:
                _, row = _strip_quotes(row)
                match = re.match(r"^\s*(?:[-*+]|\d+[.)])\s+(.+)", row)
                if match or not row.strip() or not row[:1].isspace():
                    if bullet and bullet[1] > 20:
                        report(bullet[0], "Cheat-sheet bullet exceeds 20 words.")
                    bullet = (n, len(WORD.findall(match[1]))) if match else None
                elif bullet:
                    bullet = (bullet[0], bullet[1] + len(WORD.findall(row)))
    if vault is not None and target is not None:
        yaml_links = [(n, row) for n, row in enumerate(raw.splitlines(), 2)]
        _link_checks(text, yaml_links + visible, metadata, vault, target, planned, index, report)
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("note", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--vault", help="Resolve wikilinks in this vault.")
    parser.add_argument("--template", choices=ROUTES, help="Expected built-in route.")
    parser.add_argument("--math-level", type=int, choices=(0, 1, 2, 3), help="Expected math level (3 is deep-study proof-level).")
    parser.add_argument("--contract", type=Path, help="Use the saved per-note decision contract.")
    args = parser.parse_args(argv)
    try:
        vault = resolve_vault_root(args.vault) if args.vault else None
        target = args.note.resolve()
        if vault and not is_within_vault(vault, target):
            raise ValueError("Note is outside the specified vault.")
        contract = json.loads(args.contract.read_text(encoding="utf-8-sig")) if args.contract else None
        findings = validate_text(
            target.read_text(encoding="utf-8-sig"),
            vault=vault, target=target, route=args.template or (contract or {}).get("template"),
            math_level=args.math_level if args.math_level is not None else (contract or {}).get("math_level"),
            decision_contract=contract,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps({"errors": len(findings), "findings": [
            {"file": str(args.note), "line": line, "code": "NOTE_CONTRACT", "fix": message}
            for line, message in findings]}))
        return 1 if findings else 0
    for line, message in findings:
        print(f"{args.note}:{line}: {message}")
    print(f"Errors: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
