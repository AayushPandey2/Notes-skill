#!/usr/bin/env python3
"""Executable Decision Matrix engine for Scriptorium (DM-00 through DM-20)."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

NON_COMPUTING_RE = re.compile(
    r"\b(?:"
    r"physics|optics|wave optics|huygens|snell|refraction|reflection|diffraction|interference|polarization|"
    r"mechanics|kinematics|dynamics|thermodynamics|electromagnetism|quantum|relativity|acoustics|"
    r"chemistry|organic chemistry|inorganic chemistry|thermochemistry|electrochemistry|"
    r"biology|genetics|anatomy|physiology|botany|ecology|evolution|"
    r"history|economics|macroeconomics|microeconomics|literature|philosophy|psychology|sociology|"
    r"geography|political science|pure math|calculus|linear algebra|real analysis|topology|number theory"
    r")\b",
    re.I,
)

COMPUTING_RE = re.compile(
    r"\b(?:"
    r"dsa|algorithm|algorithms|data structure|data structures|compiler|operating system|operating systems|"
    r"database|databases|sql|distributed system|distributed systems|networking|tcp|http|web|"
    r"backend|frontend|api|pytorch|tensorflow|scikit-learn|numpy|pandas|"
    r"machine learning|deep learning|neural network|neural networks|transformer|transformers|"
    r"cnn|rnn|linux|docker|kubernetes|git|software|programming|coding|"
    r"c\+\+|cpp|rust|java|javascript|typescript|python|recursion|dynamic programming|"
    r"graph theory|binary tree|hash table|sorting|cpu|scheduling|paging|segmentation"
    r")\b",
    re.I,
)

SIMULATION_REQUEST_RE = re.compile(
    r"\b(?:"
    r"python|c\+\+|cpp|rust|java|javascript|typescript|sql|code|script|program|"
    r"simulate|simulation|fdtd|monte carlo|finite difference|finite element|numerical solver|implement(?:ation)?"
    r")\b",
    re.I,
)

SPATIAL_GEOMETRY_RE = re.compile(
    r"\b(?:"
    r"optics|wave optics|huygens|snell|refraction|reflection|diffraction|interference|"
    r"ray diagram|prism|lens|mirror|triangle|geometry|geometric|wavefront|vector addition|free-body"
    r")\b",
    re.I,
)

CODE_LANG_FENCES = {
    "python", "py", "python3", "cpp", "c++", "c", "rust", "java", "go",
    "javascript", "js", "typescript", "ts", "sql", "csharp", "c#", "kotlin", "bash", "sh",
}

LEGACY_SECTION_COMMENT_RE = re.compile(r"<!--\s*SECTION:\s*S\d+[^>]*-->", re.I)

CS_JARGON_PHRASES = (
    "Computational Purpose",
    "Executive Synthesis & Architectural Significance",
    "Position in the Broader Architecture",
    "Taxonomic Lineage",
    "Deep Theory Stack",
    "Cross-Architecture Trade-Off",
    "Parameter Synthesis & Reverse-Engineering",
    "Executable Verification",
)

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\((https?://[^)\s]+)\)")
QA_HEADING_RE = re.compile(r"^#{2,4}\s+(?:Question\s+\d+|Q\d+)\b", re.I | re.M)
EXEC_CLAIM_RE = re.compile(
    r"\b(?:"
    r"(?:was\s+)?(?:\*\*)?executed(?:\*\*)?\s+via|"
    r"observed\s+execution\s+output|"
    r"all\s+assertions\s+passed"
    r")\b",
    re.I,
)


def explicit_code_requested(request: str = "", title: str = "") -> bool:
    """Return True when the user request or title explicitly asks for code or simulation."""
    return bool(SIMULATION_REQUEST_RE.search(f"{request} {title}"))


def classify_subject(topic: str, title: str = "", request: str = "", tags: list[str] | None = None) -> str:
    """Classify a topic into 'non-computing', 'computational-science', 'computing', or 'general'."""
    haystack = " ".join(filter(None, [topic, title, request, " ".join(tags or [])]))
    if NON_COMPUTING_RE.search(haystack):
        if explicit_code_requested(request, title):
            return "computational-science"
        return "non-computing"
    if COMPUTING_RE.search(haystack):
        return "computing"
    return "general"


def resolve_decisions(
    request: str,
    item: dict[str, Any] | None = None,
    topic: str = "",
    *,
    existing_workflow: str | None = None,
    tags: list[str] | None = None,
) -> dict[str, Any]:
    """Resolve DM-00 through DM-20 into a concrete Decision Contract for one note."""
    item = item or {}
    title = str(item.get("title") or "").strip()
    effective_topic = str(topic or item.get("topic") or title or "").strip()
    subject_family = classify_subject(effective_topic, title, request, tags)

    template = item.get("template")
    if not template:
        if existing_workflow == "notes" or "/scribe-notes" in request.lower():
            template = "studynotes"
        else:
            template = "deepstudy-master"

    math_level = item.get("math_level", 0)
    req_lang = str(item.get("language") or "none").strip().lower()
    impl_weight = str(item.get("impl_weight") or "low").strip().lower()
    purpose = str(item.get("purpose") or "explain").strip().lower()

    if subject_family == "non-computing":
        code_depth = "none"
        language = "none"
    elif req_lang not in ("", "none"):
        code_depth = "from-scratch" if purpose == "implement" or impl_weight == "high" else "illustrative"
        language = req_lang
    elif purpose == "implement" or impl_weight == "high":
        code_depth = "illustrative"
        language = "python"
    else:
        code_depth = "none"
        language = "none"

    if SPATIAL_GEOMETRY_RE.search(f"{effective_topic} {title} {request}"):
        visual_modality = "diagram-image"
    elif subject_family in {"computing", "computational-science"}:
        visual_modality = "mermaid-flow"
    else:
        visual_modality = "none"

    ml_topic_re = re.compile(
        r"\b(perceptron|regression|classifier|classification|svm|neural|cnn|rnn|transformer|clustering|k-means|gradient\s+descent|ml|machine\s+learning|deep\s+learning)\b",
        re.I,
    )
    if code_depth == "none":
        implementation_stack = []
    elif ml_topic_re.search(f"{effective_topic} {title} {request}"):
        implementation_stack = ["python-numpy", "scikit-learn", "pytorch"]
    else:
        implementation_stack = [language]

    required_sections = ["core_model", "intuition_and_mechanism", "boundary_and_limits", "sources_and_links"]
    if isinstance(math_level, int) and math_level >= 1:
        required_sections.append("formal_math")
    if isinstance(math_level, int) and math_level >= 2:
        required_sections.append("derivation")
    if code_depth != "none":
        required_sections.append("code_verification")

    omitted_sections = []
    if code_depth == "none":
        omitted_sections.append("code_verification")
    if math_level == 0:
        omitted_sections.extend(["formal_math", "derivation"])

    forbidden_patterns = ["legacy_section_comments", "bare_root_domain_citations"]
    if code_depth == "none":
        forbidden_patterns.extend(["fenced_code_blocks", "execution_claims"])
    if subject_family == "non-computing":
        forbidden_patterns.append("cs_architecture_jargon")
    if visual_modality == "diagram-image":
        forbidden_patterns.append("mermaid_flowchart_for_geometry")

    return {
        "subject_family": subject_family,
        "template": template,
        "math_level": math_level,
        "code_depth": code_depth,
        "language": language,
        "implementation_stack": implementation_stack,
        "visual_modality": visual_modality,
        "max_qa_items": 3,
        "required_sections": required_sections,
        "omitted_sections": omitted_sections,
        "forbidden_patterns": forbidden_patterns,
    }


def audit_note_against_contract(note_text: str, contract: dict[str, Any]) -> list[tuple[int, str]]:
    """Audit authored note Markdown against its Decision Contract. Returns (line_no, message) pairs."""
    findings: list[tuple[int, str]] = []
    lines = note_text.splitlines()
    code_depth = contract.get("code_depth", "none")
    subject_family = contract.get("subject_family", "general")
    visual_modality = contract.get("visual_modality", "none")
    max_qa = int(contract.get("max_qa_items", 3))

    for idx, line in enumerate(lines, 1):
        if LEGACY_SECTION_COMMENT_RE.search(line):
            findings.append((idx, "Legacy <!-- SECTION: S* --> marker is forbidden; use adaptive headings."))

    # Check fenced code blocks & Mermaid modality
    in_fence = False
    fence_lang = ""
    fence_line = 0
    fence_body: list[str] = []
    enforce_no_code = code_depth == "none" and (subject_family == "non-computing" or bool(contract.get("explicit_contract")))
    has_code_fence = False
    for idx, line in enumerate(lines, 1):
        stripped = line.lstrip("> ").strip()
        m_fence = re.match(r"^```([a-zA-Z0-9_+-]*)", stripped)
        if not in_fence and m_fence:
            in_fence = True
            fence_lang = m_fence.group(1).lower()
            fence_line = idx
            fence_body = []
            if fence_lang in CODE_LANG_FENCES:
                has_code_fence = True
        elif in_fence and stripped.startswith("```"):
            if enforce_no_code and fence_lang in CODE_LANG_FENCES:
                findings.append(
                    (fence_line, f"DM-14 violation: '{fence_lang}' code block is forbidden when code_depth is 'none' ({subject_family}).")
                )
            if fence_lang == "mermaid" and visual_modality in {"ascii-geometry", "diagram-image"}:
                joined = "\n".join(fence_body)
                if re.search(r"^\s*(?:flowchart|graph)\b", joined, re.M):
                    findings.append(
                        (fence_line, "DM-13 violation: use an embedded .png/.svg diagram instead of mermaid flowchart for spatial geometry.")
                    )
            in_fence = False
        elif in_fence:
            fence_body.append(line)

    if code_depth == "none" or not has_code_fence:
        for idx, line in enumerate(lines, 1):
            if EXEC_CLAIM_RE.search(line):
                findings.append((idx, "DM-18 violation: execution claim is forbidden when code_depth is 'none' or no code block exists."))

    if subject_family == "non-computing":
        for idx, line in enumerate(lines, 1):
            for phrase in CS_JARGON_PHRASES:
                if phrase.lower() in line.lower():
                    findings.append((idx, f"DM-00 violation: CS/architecture phrasing '{phrase}' is forbidden in non-computing notes."))

    if subject_family == "non-computing" or bool(contract.get("explicit_contract")):
        qa_matches = list(QA_HEADING_RE.finditer(note_text))
        if len(qa_matches) > max_qa:
            line_no = note_text[: qa_matches[max_qa].start()].count("\n") + 1
            findings.append((line_no, f"DM-20 violation: {len(qa_matches)} Q&A items exceed max_qa_items ({max_qa})."))

    for idx, line in enumerate(lines, 1):
        for match in MARKDOWN_LINK_RE.finditer(line):
            url = match.group(1)
            parsed = urlsplit(url)
            if parsed.path in ("", "/"):
                findings.append((idx, f"DM-18 violation: bare root-domain citation '{url}' is not a specific source link."))

    return findings


def check_slug_and_forward_links(
    note_text: str,
    *,
    metadata: dict[str, Any] | None = None,
    target_filename: str | None = None,
    existing_stems: set[str] | None = None,
) -> list[tuple[int, str]]:
    """Verify numbered '01 - Title' slug consistency and forward wikilink hygiene against YAML nexttopics."""
    findings: list[tuple[int, str]] = []
    nexttopics = (metadata or {}).get("nexttopics") or []
    next_stems = set()
    for entry in nexttopics:
        if isinstance(entry, str):
            m = re.search(r"\[\[([^\]|#]+)", entry)
            ref = m.group(1) if m else entry
            next_stems.add(Path(ref.strip()).stem.casefold())

    uses_space_hyphen = bool(target_filename and re.match(r"^\d{2}\s+-\s+", Path(target_filename).name))
    space_hyphen_links: list[tuple[int, str]] = []
    kebab_seq_links: list[tuple[int, str]] = []

    for idx, line in enumerate(note_text.splitlines(), 1):
        for match in re.finditer(r"\[\[([^\]]+)\]\]", line):
            raw_target = re.split(r"\\?\|", match.group(1), maxsplit=1)[0].split("#", 1)[0].strip()
            if not raw_target:
                continue
            stem = Path(raw_target).stem
            if re.match(r"^\d{2}\s+-\s+", stem):
                space_hyphen_links.append((idx, stem))
            elif re.match(r"^\d{2}-[a-z0-9-]+$", stem, re.I) and not stem.lower().startswith("00-moc-"):
                kebab_seq_links.append((idx, stem))

            if existing_stems is not None and re.match(r"^\d{2}(?:\s+-\s+|-[a-z0-9])", stem, re.I) and not stem.lower().startswith("00-moc-"):
                stem_cf = stem.casefold()
                if stem_cf not in existing_stems and stem_cf not in next_stems:
                    findings.append((
                        idx,
                        f"Forward wikilink '[[{raw_target}]]' does not exist on disk and is not listed in YAML 'nexttopics'.",
                    ))

    if (uses_space_hyphen or space_hyphen_links) and kebab_seq_links:
        for idx, stem in kebab_seq_links:
            findings.append((
                idx,
                f"Mixed filename slug style '[[{stem}]]': standardize sequential links on '01 - <Title>' rather than '02-hyphenated-slug'.",
            ))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_res = sub.add_parser("resolve", help="Resolve Decision Matrix contract before writing.")
    p_res.add_argument("--request", required=True)
    p_res.add_argument("--topic", required=True)
    p_res.add_argument("--title", default="")
    p_res.add_argument("--purpose", default="explain")
    p_res.add_argument("--impl-weight", default="low")
    p_res.add_argument("--language", default="none")
    p_res.add_argument("--math-level", type=int, default=0)
    p_res.add_argument("--existing-workflow", default=None)

    p_aud = sub.add_parser("audit", help="Audit a written note against its Decision Contract.")
    p_aud.add_argument("note", type=Path)
    p_aud.add_argument("--contract", type=Path, help="Optional JSON contract file.")
    p_aud.add_argument("--request", default="")
    p_aud.add_argument("--topic", default="")
    p_aud.add_argument("--format", choices=("text", "json"), default="text")

    args = parser.parse_args(argv)
    if args.cmd == "resolve":
        contract = resolve_decisions(
            args.request,
            {
                "title": args.title or args.topic,
                "purpose": args.purpose,
                "impl_weight": args.impl_weight,
                "language": args.language,
                "math_level": args.math_level,
            },
            args.topic,
            existing_workflow=args.existing_workflow,
        )
        print(json.dumps(contract, indent=2, ensure_ascii=False))
        return 0

    text = args.note.read_text(encoding="utf-8-sig")
    if args.contract:
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
    else:
        contract = resolve_decisions(args.request or args.topic, {"title": args.note.stem}, args.topic or args.note.stem)
    findings = audit_note_against_contract(text, contract)
    if args.format == "json":
        print(json.dumps({"errors": len(findings), "findings": [{"line": l, "message": m} for l, m in findings]}))
    else:
        for line, msg in findings:
            print(f"{args.note}:{line}: {msg}")
        print(f"Errors: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
