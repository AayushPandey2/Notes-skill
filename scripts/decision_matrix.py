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
from note_layout import ADAPTIVE_ROUTES, DEEP_ROUTES
from note_verification import required_examples, split_blocks

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

DOMAIN_MATH = {
    "social-studies-humanities": (0, 0),
    "biology": (0, 1),
    "coding-systems": (0, 1),
    "chemistry": (0, 2),
    "ml-applied": (1, 1),
    "ml-theory": (1, 2),
    "physics": (1, 2),
    "pure-mathematics": (2, 3),
    "general": (0, 2),
}
DOMAIN_PATTERNS = tuple((domain, re.compile(rf"(?<!\w)(?:{words})(?!\w)", re.I)) for domain, words in (
    ("ml-theory", r"statistical learning|learning theory|convergence|novikoff|universal approximation|uat|optimization theory|bayes[- ]optimal|backpropagation|manual gradients?"),
    ("deep-learning", r"deep learning|neural networks?|multi[- ]layer perceptron|mlp|cnn|rnn|lstm|transformers?|attention|batch[ -]?norm|activation functions?|optimizers?|keras|forward pass|convolution"),
    ("classical-ml", r"perceptron|machine learning|classical[ -]ml|regression|svm|loss functions?|k[- ]means|pca|clustering|classifiers?|classification|gradient descent"),
    ("biology", r"biology|genetics|anatomy|physiology|botany|ecology|evolution|hardy[-– ]weinberg|michaelis[-– ]menten"),
    ("chemistry", r"chemistry|stoichiometry|kinetics|thermochemistry|electrochemistry|chemical equilibrium|quantum orbitals?|ph"),
    ("physics", r"physics|optics|huygens|snell|refraction|reflection|diffraction|interference|polarization|mechanics|kinematics|dynamics|thermodynamics|electromagnetism|quantum|relativity|acoustics|lorentz|compton|gauss(?:'s)? law"),
    ("pure-mathematics", r"pure math(?:ematics)?|calculus|linear algebra|real analysis|topology|number theory|probability theory|measure theory|abstract algebra"),
    ("social-studies-humanities", r"history|economics|macroeconomics|microeconomics|literature|philosophy|psychology|sociology|geography|political science|social studies|humanities"),
    ("database", r"databases?|sql|joins|isolation levels?|window functions?|database indexes"),
    ("web", r"web|http|front[- ]?end|back[- ]?end|javascript|typescript|event loops?|promises|state management|ui"),
    ("systems", r"arrays?|pointers?|allocators?|concurrency|operating systems?|memory|linux|cpu|scheduling|paging|segmentation|rust"),
    ("dsa", r"dsa|algorithms?|data structures?|graphs?|dynamic programming|trees?|heaps?|sorting|recursion|hash tables?|two sum"),
    ("coding-systems", r"apis?|software engineering|compilers?|networking|tcp|programming|coding|python|cpp|c\+\+(?=\W|$)|java|docker|git|c programming|C language"),
))
COMPUTING_DOMAINS = {"ml-theory", "ml-applied", "coding-systems"}
STACKS = {
    "classical-ml": ("python-numpy", "scikit-learn", "pytorch"),
    "deep-learning": ("python-numpy", "pytorch", "tensorflow-keras"),
    "dsa": ("python", "cpp"),
    "systems": ("c", "rust"),
    "database": ("sql",),
    "web": ("typescript", "javascript"),
}
STACK_NAMES = {
    "python-numpy": ("numpy", "python + numpy"),
    "scikit-learn": ("sklearn", "python + scikit-learn"),
    "pytorch": ("torch", "python + pytorch"),
    "tensorflow-keras": ("tensorflow", "tf", "keras", "python + tensorflow"),
    "python": ("py", "python3"),
    "cpp": ("c++", "c++20"),
    "c": (), "rust": (), "sql": ("sqlite", "sqlite3"),
    "javascript": ("js",), "typescript": ("ts",),
    "java": (), "go": (), "csharp": ("c#",), "kotlin": (),
}
STACK_ALIASES = {alias: name for name, aliases in STACK_NAMES.items() for alias in (name, *aliases)}
REFERENCE_ROUTES = {"api-table", "cheat-sheet", "summary"}
NON_MATH_TITLE = re.compile(
    r"\b(?:implementations?|pytorch|scikit-learn|tensorflow|apis?|syntax|set[ -]?up|debugging|"
    r"deployment|history|historical|overview|taxonomy|comparisons?|vs|anatomy|lifecycle|architecture)\b", re.I,
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
DISPLAY_MATH = re.compile(r"(?<![\\$])\$\$(?!\$)(.+?)(?<![\\$])\$\$(?!\$)", re.S)
FORMAL_HEADING = re.compile(r"^\s*(?:#{1,6}\s+|\*\*|>\s*\[!\w+\]\s*)(?:\d+\.\s+)?(?:Theorem|Proposition|Lemma|Proof)\b", re.I | re.M)
DERIVATION_HEADING = re.compile(r"^\s*#{1,6}\s+.*\bDerivation\b", re.I | re.M)


def explicit_code_requested(request: str = "", title: str = "") -> bool:
    """Return True when the user request or title explicitly asks for code or simulation."""
    return bool(SIMULATION_REQUEST_RE.search(f"{request} {title}"))


def _specialty(topic: str, title: str, request: str, tags: list[str] | None) -> str:
    canonical_tag = next((tag.lower() for tag in tags or [] if tag.lower() in DOMAIN_MATH), "")
    for value in (title, topic, canonical_tag, " ".join(tags or []).replace("-", " "), request):
        if value and value == canonical_tag:
            return canonical_tag
        matches = [name for name, pattern in DOMAIN_PATTERNS if pattern.search(value)]
        if not matches:
            continue
        selected = matches[0]
        if value == title and title != topic:
            parent = next((name for name, pattern in DOMAIN_PATTERNS if pattern.search(topic)), None)
            if parent and (selected in {"social-studies-humanities", "coding-systems"}
                           or (selected == "physics" and parent == "chemistry")):
                return parent
        return selected
    return "general"


def _domain(specialty: str) -> str:
    if specialty in {"classical-ml", "deep-learning"}:
        return "ml-applied"
    return specialty if specialty in DOMAIN_MATH else "coding-systems"


def classify_domain(topic: str, title: str = "", request: str = "", tags: list[str] | None = None) -> str:
    """Resolve the mathematical domain independently of code inclusion."""
    return _domain(_specialty(topic, title, request, tags))


def classify_subject(topic: str, title: str = "", request: str = "", tags: list[str] | None = None) -> str:
    """Classify a topic into 'non-computing', 'computational-science', 'computing', or 'general'."""
    domain = classify_domain(topic, title, request, tags)
    if domain in COMPUTING_DOMAINS:
        return "computing"
    if domain != "general":
        if explicit_code_requested(request, "" if request.strip() else title):
            return "computational-science"
        return "non-computing"
    if COMPUTING_RE.search(f"{topic} {title} {request} {' '.join(tags or [])}"):
        return "computing"
    return "general"


def normalize_stack(values: list[str]) -> list[str]:
    if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
        raise ValueError("implementation_stack must be a list of supported stack names.")
    try:
        return list(dict.fromkeys(STACK_ALIASES[value.strip().lower()] for value in values))
    except KeyError as exc:
        raise ValueError(f"Unsupported implementation stack: {exc.args[0]}") from exc


def requested_stack(request: str) -> list[str] | None:
    if flag := re.search(r"--stack(?:=|\s+)([\w+,-]+(?:\s*,\s*[\w+-]+)*)", request, re.I):
        return normalize_stack(flag[1].split(","))
    names = "|".join(re.escape(name) for name in sorted(STACK_ALIASES, key=len, reverse=True))
    tools = rf"(?:{names})(?![\w+-])"
    match = re.search(
        rf"\b(?:implement|write|code|simulate|example|demo)\b[^.\n]*?\bin\s+({tools}(?:(?:\s*,\s*(?:and\s+)?|\s+and\s+){tools})*)",
        request, re.I,
    )
    return normalize_stack(re.split(r"\s*,\s*(?:and\s+)?|\s+and\s+", match[1], flags=re.I)) if match else None


def is_non_math_subtopic(title: str, purpose: str) -> bool:
    return purpose in {"implement", "compare"} or bool(NON_MATH_TITLE.search(title))


def resolve_decisions(
    request: str,
    item: dict[str, Any] | None = None,
    topic: str = "",
    *,
    existing_workflow: str | None = None,
    tags: list[str] | None = None,
    allow_math_override: bool = False,
) -> dict[str, Any]:
    """Resolve DM-00 through DM-20 into a concrete Decision Contract for one note."""
    item = item or {}
    title = str(item.get("title") or "").strip()
    effective_topic = str(topic or item.get("topic") or title or "").strip()
    specialty = _specialty(effective_topic, title, request, tags)
    domain = _domain(specialty)
    subject_family = classify_subject(effective_topic, title, request, tags)

    template = item.get("template")
    if not template:
        if existing_workflow == "notes" or "/scribe-notes" in request.lower():
            template = "studynotes"
        else:
            template = "deepstudy-master"
    if template in DEEP_ROUTES:
        template = "deepstudy-master"

    req_lang = str(item.get("language") or "none").strip().lower()
    impl_weight = str(item.get("impl_weight") or "low").strip().lower()
    purpose = str(item.get("purpose") or "explain").strip().lower()
    default, cap = DOMAIN_MATH[domain]
    context = f"{effective_topic} {title}"
    if domain == "biology" and not re.search(r"hardy[-– ]weinberg|michaelis[-– ]menten|quantitative|population growth", context, re.I):
        cap = 0
    if domain == "chemistry" and not re.search(r"physical chemistry|thermodynamics|thermochemistry|kinetics|quantum orbitals?", context, re.I):
        cap = 1 if re.search(r"stoichiometry|\bph\b|equilibrium|titration", context, re.I) else 0
    requested_level = item.get("math_level")
    if requested_level is None:
        requested_level = 0 if template == "studynotes" else default
    if type(requested_level) is not int or requested_level not in range(4):
        raise ValueError("math_level must be an integer from 0 through 3.")
    if template in REFERENCE_ROUTES and domain != "pure-mathematics" and requested_level >= 2:
        raise ValueError(f"{template} accepts at most math_level 1 for {domain}.")
    route_cap = 3 if template in DEEP_ROUTES and domain == "pure-mathematics" else 2
    if is_non_math_subtopic(title, purpose):
        cap = 0
    math_level = min(requested_level, route_cap, requested_level if allow_math_override else cap)

    override = item["implementation_stack"] if "implementation_stack" in item else requested_stack(request)
    if override is not None:
        override = normalize_stack(override)
    dedicated = purpose == "implement" or bool(re.search(r"\bimplementations?\b", title, re.I))

    if subject_family == "non-computing":
        code_depth = "none"
        language = "none"
    elif override is not None:
        code_depth = "from-scratch" if dedicated and override else "illustrative" if override else "none"
        language = override[0] if override else "none"
    elif req_lang not in ("", "none"):
        code_depth = "from-scratch" if purpose == "implement" or impl_weight == "high" else "illustrative"
        language = req_lang
    elif dedicated or impl_weight == "high":
        code_depth = "from-scratch" if dedicated else "illustrative"
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

    if code_depth == "none":
        implementation_stack = []
    elif override is not None:
        implementation_stack = override
    elif dedicated and template in DEEP_ROUTES and req_lang in {"", "none", "python"}:
        if specialty == "ml-theory":
            specialty = _specialty(effective_topic, "", "", None)
        implementation_stack = list(STACKS.get(specialty, (language,)))
    elif domain in {"ml-applied", "ml-theory"} and req_lang in {"", "none"}:
        implementation_stack = ["python-numpy"]
    else:
        implementation_stack = [STACK_ALIASES.get(language, language)]
    if implementation_stack:
        primary = implementation_stack[0]
        language = "python" if primary in STACKS["classical-ml"] or primary == "tensorflow-keras" else primary

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
        "domain": domain,
        "template": template,
        "math_level": math_level,
        "require_math_floor": True,
        **({"clamped_from": requested_level} if math_level < requested_level else {}),
        "code_depth": code_depth,
        "language": language,
        "implementation_stack": implementation_stack,
        "verify_stack": bool(implementation_stack) and (
            dedicated and template in ADAPTIVE_ROUTES
            or override is not None
        ),
        "visual_modality": visual_modality,
        "max_qa_items": 3,
        "required_sections": required_sections,
        "omitted_sections": omitted_sections,
        "forbidden_patterns": forbidden_patterns,
    }


def audit_math(prose: list[str], contract: dict[str, Any]) -> list[tuple[int, str]]:
    """Check structural evidence of the intended math depth."""
    level = contract.get("math_level")
    if type(level) is not int:
        return []
    visible = "\n".join(re.sub(r"`[^`]+`", "", line.lstrip("> ")) for line in prose)
    equations = list(DISPLAY_MATH.finditer(visible))
    derivation = DERIVATION_HEADING.search(visible)
    proof = FORMAL_HEADING.search(visible)
    justification = re.search(r"Why this step holds:", visible, re.I)
    if level == 0:
        if equations:
            return [(1, "DM-07 violation: math_level 0 forbids display equations.")]
        if proof or derivation or justification:
            return [(1, "DM-07 violation: math_level 0 forbids formal derivation and proof headings.")]
        return []

    findings = []
    seen = set()
    for eq in equations:
        normalized = re.sub(r"\s+", "", eq[1])
        number = visible.count("\n", 0, eq.start()) + 1
        if normalized in seen:
            findings.append((number, "DM-09: display the canonical equation once and refer to it elsewhere."))
        seen.add(normalized)
        atom = r"(?:[A-Za-z](?:_[A-Za-z0-9])?|-?\d+(?:\.\d+)?)"
        if (re.fullmatch(rf"{atom}(?:=|[<>]|\\le|\\ge)(?:{atom}|[A-Za-z]{{2}})", normalized)
                or re.fullmatch(r"(?:O|\\mathcal\{O\})\([^=<>]+\)", normalized)):
            findings.append((number, "DM-07: keep a simple assignment or comparison inline."))

    ceiling = {1: 3, 2: 6}.get(level)
    if ceiling and len(equations) > ceiling:
        findings.append((1, f"DM-07: math_level {level} permits at most {ceiling} display equations."))
    if level == 1 and (proof or derivation or justification or re.search(
        r"\b(?:Leibniz|Cauchy[– -]Schwarz)\b", visible, re.I
    )):
        findings.append((1, "DM-07: math_level 1 forbids formal derivation and proof machinery."))
    if not contract.get("require_math_floor", True):
        return findings

    if level in {1, 2}:
        minimum = 1 if level == 1 else 2
        if len(equations) < minimum:
            findings.append((1, f"DM-07: math_level {level} requires at least {minimum} display equation(s)."))
        if not re.search(
            r"\b(?:symbols?|notation)\b[^\n]*(?:meaning|defin|:)|\b(?:where|denotes?|represents?)\b"
            r"|\blet\s+\$|\$[^$\n]+\$\s+(?:is|are)\b|\|\s*Meaning\b", visible, re.I
        ):
            findings.append((1, "DM-09: define the symbols and relevant units, shapes or domains at first use."))
    if level == 1:
        if not re.search(r"(?:trace|worked|example|given|substitut|for instance)[\s\S]{0,650}\d", visible, re.I):
            findings.append((1, "DM-09: math_level 1 needs a small numeric trace."))
    if level == 2:
        derivation_text = visible
        if derivation:
            depth = len(derivation[0].lstrip().split()[0])
            derivation_text = re.split(rf"^#{{1,{depth}}}\s+", visible[derivation.end():], maxsplit=1, flags=re.M)[0]
        steps = re.findall(r"^\s*\d+[.)]\s+\S", derivation_text, re.M)
        chain = re.search(r"\\begin\{align(?:ed|\*?)\}", derivation_text)
        if not (((derivation or justification) and len(steps) >= 2 or chain) and re.search(
            r"\b(?:because|since|assum\w*|by the|using the)\b|Why this step holds:", derivation_text, re.I
        )):
            findings.append((1, "DM-09: math_level 2 needs a justified, stepped derivation."))
        limits = re.search(
            r"^#{2,6}\s+[^\n]*(?:Limits?|Boundar(?:y|ies))[^\n]*\n([\s\S]*?)(?=^#{1,2}\s|\Z)", visible, re.I | re.M
        )
        regimes = set(re.findall(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|#{3,6}\s+)(\S[^\n]*)", limits[1], re.M)) if limits else set()
        if len(regimes) < 2:
            findings.append((1, "DM-09: math_level 2 needs two distinct regimes in the Limits section."))
    if level == 3:
        for label, pattern in (
            ("a quantified Theorem or Proposition", r"(?:Theorem|Proposition)\b[\s\S]*?(?:\bfor (?:all|every|any)\b|\bthere exists\b|\\forall|\\exists|[∀∃])"),
            ("a Proof", r"(?:^\s*#{1,6}\s+.*\bProof\b|^\s*\*\*Proof\b)"),
            ("a Counterexample", r"(?:^\s*#{1,6}\s+.*\bCounterexample\b|^\s*\*\*Counterexample\b)"),
        ):
            if not re.search(pattern, visible, re.I | re.M):
                findings.append((1, f"DM-09: math_level 3 requires {label}."))
    return findings


def audit_note_against_contract(note_text: str, contract: dict[str, Any]) -> list[tuple[int, str]]:
    """Audit authored note Markdown against its Decision Contract. Returns (line_no, message) pairs."""
    findings: list[tuple[int, str]] = []
    blocks, lines = split_blocks(note_text)
    code_depth = contract.get("code_depth", "none")
    subject_family = contract.get("subject_family", "general")
    visual_modality = contract.get("visual_modality", "none")
    max_qa = int(contract.get("max_qa_items", 3))

    for idx, line in enumerate(note_text.splitlines(), 1):
        if LEGACY_SECTION_COMMENT_RE.search(line):
            findings.append((idx, "Legacy <!-- SECTION: S* --> marker is forbidden; use adaptive headings."))

    # Check fenced code blocks & Mermaid modality
    enforce_no_code = code_depth == "none" and (subject_family == "non-computing" or bool(contract.get("explicit_contract")))
    has_code_fence = any(block.lang in CODE_LANG_FENCES for block in blocks)
    for block in blocks:
        if enforce_no_code and block.lang in CODE_LANG_FENCES:
            findings.append((block.line, f"DM-14 violation: '{block.lang}' code block is forbidden when code_depth is 'none' ({subject_family})."))
        if (block.lang == "mermaid" and visual_modality in {"ascii-geometry", "diagram-image"}
                and re.search(r"^\s*(?:flowchart|graph)\b", block.code, re.M)):
            findings.append((block.line, "DM-13 violation: use an embedded .png/.svg diagram instead of mermaid flowchart for spatial geometry."))

    if contract.get("template", "deepstudy-master") in ADAPTIVE_ROUTES:
        findings.extend(audit_math(lines, contract))
    stack = contract.get("implementation_stack", [])
    if stack and contract.get("verify_stack", True):
        _, missing = required_examples(blocks, stack)
        findings.extend(missing)
        if len(stack) > 1:
            if not any(re.match(r"^(?:\*\*)?Shared fixture(?:\*\*)?:(?:\*\*)?\s*\S", line, re.I) for line in lines):
                findings.append((1, "DM-17: document the shared inputs and parameters in a Shared fixture: field."))
            header = next((idx for idx, line in enumerate(lines) if re.match(
                r"^\s*\|\s*(?:Framework|Language|Stack)\s*\|\s*Exposes\s*\|\s*Hides\s*\|\s*(?:Main\s+)?Pitfall\s*\|\s*$", line, re.I
            )), None)
            rows = {}
            if header is not None:
                for line in lines[header + 2:]:
                    if not line.lstrip().startswith("|"):
                        break
                    cells = [cell.strip().strip("`") for cell in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
                    if len(cells) == 4 and all(cells):
                        rows[cells[0].lower()] = cells[1:]
            if not set(stack) <= rows.keys():
                findings.append((1, "DM-17: add a Framework or Language table with Exposes, Hides and Pitfall columns for each stack."))

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
        visible = "\n".join(lines)
        qa_matches = list(QA_HEADING_RE.finditer(visible))
        if len(qa_matches) > max_qa:
            line_no = visible[: qa_matches[max_qa].start()].count("\n") + 1
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
    p_res.add_argument("--stack")
    p_res.add_argument("--template")
    p_res.add_argument("--math-level", type=int, choices=range(4))
    p_res.add_argument("--allow-math-override", action="store_true")
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
                "template": args.template,
                "implementation_stack": args.stack.split(",") if args.stack else None,
                "math_level": args.math_level,
            },
            args.topic,
            existing_workflow=args.existing_workflow,
            allow_math_override=args.allow_math_override,
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
