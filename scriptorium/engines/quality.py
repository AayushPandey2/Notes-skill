"""Engine E5 — Quality and Verification Engine for Scriptorium.

Consolidates:
- Code/runtime verification (_verification.py — consolidated from scripts/note_verification.py)
- Repository link/CLI/syntax auditing (consolidated from scripts/audit_repository.py)
- Mechanism 10: Representation Consistency Checker (safe AST math evaluator, units, shapes, code-equation alignment)
- Mechanism 18: Failure-Aware Targeted Repair Engine (structured issue reports, bounded retries, local repair)
- Mechanism 19: Evaluation Harness and Golden Examples (13 cross-domain & cross-master golden cases)
"""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field
import subprocess
from pathlib import Path
import re
from typing import Any, Callable
from urllib.parse import unquote

from scriptorium.engines._verification import (
    EXTENSIONS,
    FENCE,
    Block,
    check_evidence,
    check_python,
    quoted_line,
    required_examples,
    split_blocks,
    verify_runtimes,
)
from scriptorium.engines.orchestration import (
    OrchestrationEngine,
    lint_instruction_authority,
    validate_master_output,
)
from scriptorium.engines.vault import (
    VaultEngine,
    build_obsidian_properties,
    incremental_update_note,
    render_note_with_properties,
    validate_obsidian_properties,
)
from scriptorium.models import REPO_ROOT, heading_slug as _heading_slug, parse_note, safe_eval_expr

# ---------------------------------------------------------------------------
# Consolidated Repository Auditor (formerly scripts/audit_repository.py)
# ---------------------------------------------------------------------------


def audit_repository(root: Path = REPO_ROOT) -> dict[str, Any]:
    """Audit local Markdown connectivity, script CLI flags, and Python syntax across the repository."""
    errors: list[dict[str, str]] = []
    checked = 0
    files = [
        p for p in root.rglob("*")
        if p.is_file() and not any(x in p.parts for x in (".git", "__pycache__", ".pytest_cache", ".test-deps", ".venv"))
        and not (".scriptorium" in p.parts and "cache" in p.parts)
    ]
    for path in files:
        if path.suffix not in {".md", ".py"}:
            continue
        text = path.read_text(encoding="utf-8-sig")
        if path.suffix == ".py":
            ast.parse(text, filename=str(path))
            continue
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if re.match(r"(?:https?:|mailto:|plugin:)", target) or any(x in target for x in ("<", ">", "*")):
                continue
            name, _, anchor = unquote(target).partition("#")
            dest = (path.parent / name).resolve() if name else path
            checked += 1
            if not dest.is_file():
                errors.append({"file": str(path.relative_to(root)), "target": target, "fix": "Resolve local target"})
            elif anchor and dest.suffix == ".md":
                headings = re.findall(r"^#+ (.+)$", dest.read_text(encoding="utf-8-sig"), re.M)
                if anchor not in {_heading_slug(h) for h in headings}:
                    errors.append({"file": str(path.relative_to(root)), "target": target, "fix": "Resolve heading anchor"})
        for script, arguments in re.findall(r"scripts/([\w]+\.py)([^\n]*)", text):
            dest = root / "scripts" / script
            if not dest.is_file():
                errors.append({"file": str(path.relative_to(root)), "target": script, "fix": "Resolve script path"})
                continue
            if not arguments.startswith(")"):
                arguments = arguments.split("`", 1)[0]
            implementation = dest.read_text(encoding="utf-8")
            for flag in re.findall(r"--[a-z][a-z-]+", arguments):
                if flag not in implementation:
                    errors.append({"file": str(path.relative_to(root)), "target": script + " " + flag, "fix": "Resolve CLI flag"})
    return {"files": len(files), "local_links": checked, "errors": errors}


def audit_reconstruction_compliance(root: Path = REPO_ROOT) -> dict[str, Any]:
    """Static CI check detecting retired SVG creation paths, versioned branding, or hardcoded lessons in production."""
    versioned_re = re.compile(r"\bScriptorium\s+\d+(?:\.\d+)?\b")
    svg_gen_re = re.compile(r"\b(?:scientific_svg|architecture_svg|mask_svg|flow_svg|graph_svg|coordinate_svg|evaluate_svg_fallback_gate)\b")
    preset_re = re.compile(r"\b(?:CONCEPT_PRESETS|TOPIC_PRESETS|LESSON_PRESETS|KNOWN_CONTRASTS|COLLECTION_CURRICULA)\b")

    branding_hits: list[str] = []
    svg_hits: list[str] = []
    preset_hits: list[str] = []

    for py_root in (root / "scriptorium", root / "scripts"):
        if not py_root.is_dir():
            continue
        for py_file in sorted(py_root.rglob("*.py")):
            rel = py_file.relative_to(root).as_posix()
            text = py_file.read_text(encoding="utf-8-sig")
            for lineno, line in enumerate(text.splitlines(), 1):
                if rel != "scriptorium/engines/quality.py":
                    if versioned_re.search(line):
                        branding_hits.append(f"{rel}:{lineno}")
                    if svg_gen_re.search(line):
                        svg_hits.append(f"{rel}:{lineno}")
                    if preset_re.search(line):
                        preset_hits.append(f"{rel}:{lineno}")

    active_docs = [root / "SKILL.md", root / "router.md", root / "README.md"]
    active_docs.extend(sorted((root / "skills").rglob("*.md")) if (root / "skills").is_dir() else [])
    active_docs.extend(sorted((root / "shared").rglob("*.md")) if (root / "shared").is_dir() else [])
    for doc in active_docs:
        if not doc.is_file():
            continue
        rel = doc.relative_to(root).as_posix()
        for lineno, line in enumerate(doc.read_text(encoding="utf-8-sig").splitlines(), 1):
            if versioned_re.search(line):
                branding_hits.append(f"{rel}:{lineno}")
            if svg_gen_re.search(line):
                svg_hits.append(f"{rel}:{lineno}")

    return {
        "passed": not (branding_hits or svg_hits or preset_hits),
        "versioned_branding_hits": branding_hits,
        "retired_svg_generator_hits": svg_hits,
        "hardcoded_preset_hits": preset_hits,
    }


def repository_inventory(root: Path = REPO_ROOT) -> dict[str, Any]:
    """Read-only dependency/size evidence. Textual reachability never authorizes deletion."""
    listed = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                            cwd=root, capture_output=True, check=True).stdout.decode("utf-8").split("\0")
    paths = sorted({name for name in listed if name and (root/name).is_file()})
    changed = set(subprocess.run(["git", "diff", "--name-only"], cwd=root, capture_output=True, check=True).stdout.decode("utf-8").splitlines())
    modules = {p[:-3].replace("/", "."): p for p in paths if p.endswith(".py")}
    modules.update({name.removesuffix(".__init__"): path for name, path in list(modules.items()) if name.endswith(".__init__")})
    outgoing, entries = {}, []
    for name in paths:
        path = root/name
        try:
            raw = path.read_text(encoding="utf-8-sig")
        except (UnicodeError, OSError):
            raw = ""
        dependencies = set()
        purpose = next((line.lstrip("# ") for line in raw.splitlines() if line.startswith("# ")), "supporting data or configuration")
        if name.endswith(".py"):
            import importlib.util
            tree = ast.parse(raw)
            purpose = (ast.get_docstring(tree) or "Python runtime/helper").splitlines()[0]
            module = name[:-3].replace("/", ".")
            package = module.removesuffix(".__init__") if module.endswith(".__init__") else module.rpartition(".")[0]
            for node in ast.walk(tree):
                names = []
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    target = "."*node.level+(node.module or "")
                    try:
                        target = importlib.util.resolve_name(target, package) if node.level else target
                    except (ImportError, ValueError):
                        continue
                    names = [target, *[target+"."+alias.name for alias in node.names]]
                dependencies.update(modules[n] for n in names if n in modules)
        for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", raw):
            if "://" not in target:
                resolved = (path.parent/unquote(target)).resolve()
                if resolved.is_relative_to(root.resolve()) and resolved.is_file():
                    dependencies.add(resolved.relative_to(root.resolve()).as_posix())
        dependencies.update(target for target in re.findall(r"(?:references|shared|skills|scripts|scriptorium)/[\w./-]+\.(?:md|py|json|yaml)", raw)
                            if target in paths)
        outgoing[name] = sorted(dependencies-{name})
        action = "OPTIMIZE" if name in changed else "KEEP"
        entries.append({"path": name, "purpose": purpose, "action": action, "lines": len(raw.splitlines()), "bytes": path.stat().st_size,
                        "estimated_context_tokens": (len(raw)+3)//4, "outbound": outgoing[name], "inbound": [],
                        "execution_path": "CLI/test import or selectively loaded reference; inspect inbound edges",
                        "safety": "preserve; absence of a static caller is not proof of dead behavior"})
    by_name = {e["path"]: e for e in entries}
    for name, targets in outgoing.items():
        for target in targets:
            if target in by_name:
                by_name[target]["inbound"].append(name)
    return {"scope": "Tracked and nonignored repository files, before emitting this inventory; dynamic imports and prose references may be incomplete.",
            "token_method": "ceil(characters/4) estimate; not provider tokens", "files": entries,
            "deletion_authorized_by_inventory": False, "totals": {"files": len(entries), "bytes": sum(e["bytes"] for e in entries)}}


# ---------------------------------------------------------------------------
# Mechanism 10 — Representation Consistency Checker (Section 19)
# ---------------------------------------------------------------------------


def check_representation_consistency(spec: dict[str, Any]) -> dict[str, Any]:
    """Mechanism 10: Verify numerical, symbol, unit, tensor-shape, diagram, and code consistency against canonical spec."""
    conflicts: list[dict[str, Any]] = []
    concept_id = str(spec.get("concept_id") or "concept")
    equation = spec.get("equation")  # e.g. "w * x + b"
    variables = {k: float(v) for k, v in (spec.get("variables") or {}).items()}
    canonical_value: float | None = None

    if equation:
        canonical_value = safe_eval_expr(str(equation), variables)
        if "expected_output" in spec and spec["expected_output"] is not None:
            exp = float(spec["expected_output"])
            if abs(canonical_value - exp) > 1e-6:
                conflicts.append({
                    "type": "equation_expected_mismatch",
                    "concept_id": concept_id,
                    "detail": f"Equation '{equation}' evaluates to {canonical_value}, but expected_output is {exp}.",
                    "repair_target": "expected_output",
                })
        for rep_name in ("prose_output", "table_output", "code_output", "example_output"):
            if rep_name in spec and spec[rep_name] is not None:
                obs = float(spec[rep_name])
                if abs(canonical_value - obs) > 1e-6:
                    conflicts.append({
                        "type": "numerical_mismatch",
                        "concept_id": concept_id,
                        "representation": rep_name,
                        "detail": f"{rep_name}={obs} disagrees with authoritative equation value {canonical_value}.",
                        "repair_target": rep_name,
                    })

    # Symbol set consistency between equation and code/prose
    eq_symbols = set(spec.get("equation_symbols") or [])
    code_symbols = set(spec.get("code_symbols") or [])
    if eq_symbols and code_symbols:
        mapping = spec.get("symbol_to_code_map") or {}
        mapped_eq = {mapping.get(s, s) for s in eq_symbols}
        unmapped = sorted(mapped_eq - code_symbols)
        if unmapped:
            conflicts.append({
                "type": "symbol_code_mismatch",
                "concept_id": concept_id,
                "detail": f"Equation symbols {unmapped} missing from code representation.",
                "repair_target": "code",
            })

    # Units consistency
    units = spec.get("units") or {}
    if isinstance(units, dict) and len(set(units.values())) > 1 and spec.get("require_same_units"):
        conflicts.append({
            "type": "unit_mismatch",
            "concept_id": concept_id,
            "detail": f"Representations use conflicting units: {units}.",
            "repair_target": "units",
        })

    # Tensor shapes consistency
    shapes = spec.get("tensor_shapes") or {}
    if "input" in shapes and "weight" in shapes and "output" in shapes:
        inp = shapes["input"]
        wt = shapes["weight"]
        out = shapes["output"]
        if len(inp) == 2 and len(wt) == 2 and len(out) == 2:
            if inp[1] != wt[0] or (inp[0], wt[1]) != tuple(out):
                conflicts.append({
                    "type": "tensor_shape_mismatch",
                    "concept_id": concept_id,
                    "detail": f"Incompatible matmul shapes: {inp} @ {wt} != {out}.",
                    "repair_target": "tensor_shapes",
                })

    # Diagram direction check
    diagram_edges = spec.get("diagram_edges") or []
    expected_edges = spec.get("expected_diagram_edges") or []
    for edge in expected_edges:
        if edge not in diagram_edges:
            conflicts.append({
                "type": "diagram_direction_mismatch",
                "concept_id": concept_id,
                "detail": f"Expected diagram edge {edge} missing or reversed in diagram.",
                "repair_target": "diagram",
            })

    return {
        "consistent": not conflicts,
        "canonical_value": canonical_value,
        "conflicts": conflicts,
    }


# ---------------------------------------------------------------------------
# Mechanism 18 — Failure-Aware Targeted Repair Engine (Section 27)
# ---------------------------------------------------------------------------

@dataclass
class IssueReport:
    issue_id: str
    concept_id: str
    location: str
    severity: str  # critical | major | moderate | minor
    type: str
    description: str
    repair_scope: str
    dependent_checks: list[str] = field(default_factory=list)
    systemic: bool = False


class RepairEngine:
    """Apply minimal local repairs with bounded retries and dependent revalidation."""

    def __init__(self, *, max_retries: int = 3):
        self.max_retries = max_retries
        self.history: list[dict[str, Any]] = []

    def apply_local_repair(
        self,
        note_text: str,
        issue: IssueReport,
        *,
        find_text: str,
        replace_text: str,
        validator: Callable[[str], list[str]] | None = None,
    ) -> dict[str, Any]:
        """Apply a minimal localized fix without regenerating unrelated sections; enforce retry cap."""
        attempts_for_issue = sum(1 for h in self.history if h["issue_id"] == issue.issue_id)
        if attempts_for_issue >= self.max_retries:
            return {
                "repaired": False,
                "stopped_reason": "max_retries_exceeded",
                "issue": asdict(issue),
                "content": note_text,
            }

        if find_text not in note_text:
            record = {
                "issue_id": issue.issue_id,
                "attempt": attempts_for_issue + 1,
                "repaired": False,
                "reason": "target_span_not_found",
            }
            self.history.append(record)
            return {**record, "issue": asdict(issue), "content": note_text}

        repaired_text = note_text.replace(find_text, replace_text, 1)
        remaining_errors = validator(repaired_text) if validator else []
        success = not remaining_errors

        record = {
            "issue_id": issue.issue_id,
            "attempt": attempts_for_issue + 1,
            "repaired": success,
            "repair_scope": issue.repair_scope,
            "dependent_checks": list(issue.dependent_checks),
            "remaining_errors": remaining_errors,
            "full_regeneration_avoided": True,
        }
        self.history.append(record)
        return {**record, "issue": asdict(issue), "content": repaired_text if success else note_text}

    def detect_systemic_defect(self, issues: list[IssueReport], *, threshold: int = 3) -> list[str]:
        """Flag recurring defect types across artifacts as systemic template/module issues."""
        counts: dict[str, int] = {}
        for issue in issues:
            counts[issue.type] = counts.get(issue.type, 0) + 1
        return sorted(t for t, c in counts.items() if c >= threshold)


# ---------------------------------------------------------------------------
# Mechanism 19 — Evaluation Harness & Golden Examples (Section 28)
# ---------------------------------------------------------------------------

GOLDEN_CASES: list[dict[str, Any]] = [
    {"id": "G01_basic_math", "request": "Explain derivatives deeply from first principles", "expected_master": "M1", "expected_domain": "Mathematics", "expected_note_type": "deep-notes"},
    {"id": "G02_advanced_math", "request": "Solve these 5 calculus integration problems step by step", "expected_master": "M4", "expected_domain": "Mathematics", "expected_note_type": "worked-solutions"},
    {"id": "G03_programming", "request": "Implement binary search from scratch in Python", "expected_master": "M5", "expected_domain": "Computer Science", "expected_note_type": "implementation-guide"},
    {"id": "G04_machine_learning", "request": "Create comprehensive notes about gradient descent, including intuition, equations, worked examples, and Python implementation", "expected_master": "M1", "expected_domain": "Artificial Intelligence", "expected_note_type": "deep-notes"},
    {"id": "G05_physics", "request": "Make structured study notes on Biot-Savart Law from this lecture", "expected_master": "M2", "expected_domain": "Physics", "expected_note_type": "study-notes", "has_source": True},
    {"id": "G06_history", "request": "Create an exam revision pack on the French Revolution", "expected_master": "M7", "expected_domain": "History", "expected_note_type": "synthesis-revision"},
    {"id": "G07_source_chapter", "request": "Make notes on this lecture PDF using only its formulas and preserving its lecture order", "expected_master": "M2", "expected_source_policy": "strict", "has_source": True},
    {"id": "G08_cheat_sheet", "request": "Give me a cheat sheet for Pandas Data Cleaning", "expected_master": "M3", "expected_domain": "Computer Science", "expected_note_type": "quick-reference"},
    {"id": "G09_worked_solutions", "request": "Show worked examples of Bayes theorem", "expected_master": "M4", "expected_domain": "Mathematics", "expected_note_type": "worked-solutions"},
    {"id": "G10_quiz", "request": "Create flashcards for cellular respiration", "expected_master": "M6", "expected_domain": "Biology", "expected_note_type": "assessment"},
    {"id": "G11_revision_pack", "request": "Compare Keynesian vs Monetarist economics", "expected_master": "M7", "expected_domain": "Economics", "expected_note_type": "synthesis-revision"},
    {"id": "G12_multi_artifact", "request": "Create deep notes on Signal Sampling and a separate formula sheet", "expected_master": "M1", "expected_multi_artifact": True, "expected_artifact_masters": ["M1", "M3"]},
    {"id": "G13_incremental_update", "mode": "incremental_update", "topic": "Thermodynamic Equilibrium"},
]


class EvaluationHarness:
    """Mechanism 19: Deterministic golden-case evaluation harness across all masters and lifecycle tasks."""

    def __init__(self, root: Path = REPO_ROOT):
        self.orchestration = OrchestrationEngine(root)
        self.vault = VaultEngine()

    def run_all(self, cases: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        selected = cases if cases is not None else GOLDEN_CASES
        results: list[dict[str, Any]] = []
        passed = 0

        for case in selected:
            cid = case["id"]
            failures: list[str] = []
            if case.get("mode") == "incremental_update":
                initial_props = build_obsidian_properties(
                    topic=case["topic"],
                    note_type="deep-notes",
                    custom_properties={"custom_property": "keep-me"},
                    user_tags=["my-personal-tag"],
                    created="2026-01-01",
                )
                initial = render_note_with_properties(
                    initial_props,
                    f"# {case['topic']}\n\n## Intuition\nInitial intuition.\n\n## Personal Notes\nKeep this annotation.\n",
                )
                upd = incremental_update_note(
                    initial,
                    section_updates={"Intuition": "Updated intuition with step-size bound."},
                    update_date="2026-11-20",
                )
                if "Keep this annotation." not in upd["content"]:
                    failures.append("Lost unrelated user section.")
                if upd["properties"].get("custom_property") != "keep-me":
                    failures.append("Lost custom user property.")
                if "my-personal-tag" not in upd["properties"].get("tags", []):
                    failures.append("Lost user-managed tag.")
                if upd["properties"].get("created") != "2026-01-01":
                    failures.append("Altered original created date.")
                prop_errs = validate_obsidian_properties(upd["content"])
                failures.extend(prop_errs)
            else:
                norm = self.orchestration.normalize(case["request"], has_source=bool(case.get("has_source")))
                routed = norm["routed"]
                if routed["master"] != case["expected_master"]:
                    failures.append(f"Expected master {case['expected_master']}, got {routed['master']}.")
                if "expected_source_policy" in case and routed["source_policy"] != case["expected_source_policy"]:
                    failures.append(f"Expected source_policy {case['expected_source_policy']}, got {routed['source_policy']}.")
                if case.get("expected_multi_artifact"):
                    if not routed["multi_artifact"]:
                        failures.append("Expected multi_artifact=True.")
                    actual_masters = [a["master"] for a in routed["artifacts"]]
                    if actual_masters != case.get("expected_artifact_masters"):
                        failures.append(f"Expected artifact masters {case.get('expected_artifact_masters')}, got {actual_masters}.")
                # Verify generated Obsidian Properties
                note_type = routed["artifacts"][0]["master_route"]
                props = self.vault.build_properties(topic=norm["topic"], note_type=note_type, content=case["request"])
                sample_note = self.vault.render_note(props, f"# {norm['topic']}\n\n## Overview\nSample body.\n")
                failures.extend(self.vault.validate_properties(sample_note, expected_note_type=note_type))
                if "expected_domain" in case and props["domain"] != case["expected_domain"]:
                    failures.append(f"Expected domain '{case['expected_domain']}', got '{props['domain']}'.")
                if "expected_note_type" in case and props["note_type"] != case["expected_note_type"]:
                    failures.append(f"Expected note_type '{case['expected_note_type']}', got '{props['note_type']}'.")

            ok = not failures
            if ok:
                passed += 1
            results.append({"id": cid, "passed": ok, "failures": failures})

        return {
            "total": len(selected),
            "passed": passed,
            "failed": len(selected) - passed,
            "all_passed": passed == len(selected),
            "results": results,
        }


# ---------------------------------------------------------------------------
# EIS-07 — Reader Simulation & Cognitive Friction Detection (CF-01 .. CF-12)
# ---------------------------------------------------------------------------

COGNITIVE_FRICTION_TAXONOMY: dict[str, str] = {
    "CF-01": "Undefined technical terminology",
    "CF-02": "Undefined mathematical symbol",
    "CF-03": "Unmotivated mathematical or algorithmic operation",
    "CF-04": "Abrupt conceptual transition",
    "CF-05": "Excessive semantic density",
    "CF-06": "Unnecessary repetition",
    "CF-07": "Hidden assumption",
    "CF-08": "Misleading analogy without boundary disclosure",
    "CF-09": "Unclear pronoun referent",
    "CF-10": "Representation mismatch",
    "CF-11": "Premature advanced detail in introductory reasoning",
    "CF-12": "Missing explanatory destination (central question unresolved)",
}

_BEGINNER_JARGON_TERMS = (
    "lipschitz", "hessian", "jacobian", "subgradient", "diffeomorphism",
    "homeomorphism", "banach", "hilbert", "manifold", "eigenspace", "covariant",
    "epistemic", "stochastic", "asymptotic", "orthogonality", "idempotent",
)
_AMBIGUOUS_PRONOUN_RE = re.compile(
    r"(?:^|[.!?]\s+)(This|It|They)\s+(?:is|are|was|were|causes|produces|changes|reduces|increases|implies|shows|makes)\b"
)
_ANALOGY_RE = re.compile(r"\b(?:just\s+like|like\s+a|analogous\s+to|think\s+of\s+.+?\s+as|imagine\s+a)\b", re.I)
_ANALOGY_LIMIT_RE = re.compile(r"\b(?:breaks?\s+down|unlike\s+the\s+analogy|limit(?:ation)?s?\s+of\s+this\s+analogy|however,?\s+in\s+reality|unlike\s+a\s+real)\b", re.I)


def _collect_prose_and_structural_friction(
    document: str,
    parsed: Any,
    body: str,
    profile: str,
    explanation_blueprint: Any | None,
    add_issue: Callable[..., None],
) -> None:
    """Inspect sections, density, repetition, analogies, and pronoun ambiguity (CF-03..CF-09)."""
    from scriptorium.engines.pedagogy import ExplanationBlueprint, analyze_information_density

    if re.search(
        r"(?:^|[.!?]\s+)(?:Now\s+differentiate|Just\s+apply|Simply\s+substitute|Now\s+multiply\s+both\s+sides)",
        body,
        re.I | re.M,
    ):
        add_issue("CF-03", "major", "Operation is narrated mechanically without stating its explanatory purpose.", "add_operation_motivation")

    for sec in parsed.sections:
        sec_lines = [ln.strip() for ln in sec.content.splitlines()[1:] if ln.strip()]
        if sec_lines and sec_lines[0].startswith("$$") and (
            not isinstance(explanation_blueprint, ExplanationBlueprint) or explanation_blueprint.context.get("selected_master") != "M3"
        ):
            add_issue(
                "CF-04",
                "minor",
                f"Section '{sec.heading}' opens abruptly with a display equation before motivating its purpose.",
                f"add_framing_sentence_before_equation:{sec.slug}",
                location=sec.slug,
            )

    density = analyze_information_density(document, reader_level=profile)
    for sec_rep in density.get("overloaded_sections", []):
        add_issue(
            "CF-05",
            "major" if profile == "beginner" else "minor",
            f"Section '{sec_rep['heading']}' introduces high semantic density ({sec_rep['estimated_new_terms']} terms, {sec_rep['unique_symbols']} symbols).",
            "split_dense_paragraph_and_anchor_with_example",
            location=sec_rep["heading"],
        )

    sentences = [
        re.sub(r"\s+", " ", s).strip()
        for s in re.split(r"(?<=[.!?])\s+", re.sub(r"```.*?```|\$\$.*?\$\$", " ", body, flags=re.S))
        if len(s.split()) >= 8 and not s.strip().startswith(("#", "|", ">"))
    ]
    seen_sent: set[str] = set()
    for sent in sentences:
        key = re.sub(r"[^a-z0-9 ]+", "", sent.lower())
        if key in seen_sent:
            add_issue("CF-06", "minor", f"Repeated sentence detected: '{sent[:70]}...'", "remove_redundant_sentence")
            break
        seen_sent.add(key)

    if _ANALOGY_RE.search(body) and not _ANALOGY_LIMIT_RE.search(body):
        add_issue(
            "CF-08",
            "minor",
            "Analogy introduced without disclosing where the analogy breaks down.",
            "add_analogy_breakdown_clause",
            deterministic=False,
        )

    if m_pron := _AMBIGUOUS_PRONOUN_RE.search(body):
        add_issue(
            "CF-09",
            "minor",
            f"Ambiguous standalone pronoun '{m_pron.group(1)}' starts a sentence without naming its referent.",
            f"replace_ambiguous_pronoun_with_explicit_noun:{m_pron.group(1)}",
        )


def review_explanatory_clarity(
    document: str,
    explanation_blueprint: Any | None = None,
    *,
    learner_profile: str = "intermediate",
    representation_spec: dict[str, Any] | None = None,
    source_mode: str | None = None,
) -> dict[str, Any]:
    """EIS-07: Hypothetical reader simulation detecting CF-01..CF-12 and EIS structural issues.

    Reuses PedagogyEngine (gap & density detectors), QualityEngine (representation checker),
    and EIS-01..06 validators. Never claims measured human mastery.
    """
    from scriptorium.engines.pedagogy import (
        ExplanationBlueprint,
        detect_explanation_gaps,
        validate_explanation_structure,
    )

    parsed = parse_note(document)
    body = parsed.body
    lowered = body.lower()
    profile = (
        learner_profile
        or (explanation_blueprint.context.get("audience_depth") if isinstance(explanation_blueprint, ExplanationBlueprint) else "intermediate")
    ).strip().lower()
    eff_source_mode = source_mode or (
        explanation_blueprint.context.get("source_mode", "adaptive")
        if isinstance(explanation_blueprint, ExplanationBlueprint)
        else "adaptive"
    )

    issues: list[dict[str, Any]] = []

    def _add(code: str, severity: str, description: str, proposed_repair: str, *, location: str = "body", deterministic: bool = True) -> None:
        issues.append({
            "type": code,
            "category": COGNITIVE_FRICTION_TAXONOMY.get(code, code),
            "severity": severity,
            "location": location,
            "description": description,
            "proposed_repair": proposed_repair,
            "check_basis": "deterministic" if deterministic else "semantic_heuristic",
        })

    if profile in {"beginner", "intermediate"}:
        intro_text = parsed.sections[0].content if parsed.sections else body[:500]
        for term in _BEGINNER_JARGON_TERMS:
            if re.search(rf"\b{term}\b", body, re.I) and not re.search(
                rf"\b{term}\b[^.\n]{{0,40}}(?:\b(?:means?|is\s+(?:a|an|the)|denotes?|refers?\s+to|measures?)|\(|—)",
                body,
                re.I,
            ):
                if profile == "beginner" and re.search(rf"\b{term}\b", intro_text, re.I):
                    _add("CF-11", "major", f"Advanced term '{term}' appears in introductory reasoning for a beginner without plain-language grounding.", f"define_or_defer_advanced_term:{term}", location="introduction")
                else:
                    _add("CF-01", "major", f"Technical term '{term}' is used without definition for a {profile} reader.", f"define_term_near_first_use:{term}")

    gap_report = detect_explanation_gaps(body, reader_level=profile)
    for gap in gap_report.get("gaps", []):
        if gap["type"] == "undefined_symbol":
            _add("CF-02", "major", gap["description"], f"define_symbol_before_equation:{gap.get('symbol', '')}", location=f"line_{gap.get('line', 0)}")
        elif gap["type"] == "missing_assumption":
            _add("CF-07", "major", gap["description"], "state_applicability_assumptions")
        elif gap["type"] == "skipped_derivation_step":
            _add("CF-03", "major", gap["description"], "add_intermediate_derivation_motivation")

    _collect_prose_and_structural_friction(document, parsed, body, profile, explanation_blueprint, _add)

    if representation_spec:
        rep_res = check_representation_consistency(representation_spec)
        for conf in rep_res.get("conflicts", []):
            _add("CF-10", "critical", conf["detail"], f"repair_representation:{conf.get('repair_target', 'spec')}")

    eis_issues: list[dict[str, Any]] = []
    if isinstance(explanation_blueprint, ExplanationBlueprint):
        eis_issues = validate_explanation_structure(document, explanation_blueprint)
        cq_topic = explanation_blueprint.topic.lower()
        if explanation_blueprint.activation_levels.get("eis_02_questions") in {"standard", "deep"}:
            if cq_topic and cq_topic not in lowered and len(body.split()) < 40:
                _add("CF-12", "major", f"Section does not clearly resolve the central question for '{explanation_blueprint.topic}'.", "add_explicit_resolution_of_central_question")

    major_or_critical = [i for i in issues if i["severity"] in {"critical", "major"}]
    major_or_critical_eis = [i for i in eis_issues if i["severity"] in {"critical", "major"}]
    return {
        "simulated_reader": profile,
        "hypothetical_review": True,
        "claims_measured_mastery": False,
        "source_mode": eff_source_mode,
        "passed": not (major_or_critical or major_or_critical_eis),
        "friction_issues": issues,
        "eis_issues": eis_issues,
        "summary": {
            "total_friction_issues": len(issues),
            "major_or_critical_friction": len(major_or_critical),
            "eis_structural_issues": len(eis_issues),
        },
    }


def repair_explanatory_friction(
    note_text: str,
    *,
    find_text: str,
    replace_text: str,
    issue_code: str,
    concept_id: str = "concept",
    source_mode: str = "adaptive",
    introduces_external_facts: bool = False,
    repair_engine: RepairEngine | None = None,
) -> dict[str, Any]:
    """Apply a bounded, local explanation repair while strictly enforcing source-only safety."""
    if source_mode == "strict" and introduces_external_facts:
        return {
            "repaired": False,
            "blocked_by_source_policy": True,
            "reason": "Strict source-only mode forbids adding external factual claims during friction repair.",
            "content": note_text,
        }
    engine = repair_engine or RepairEngine()
    issue = IssueReport(
        issue_id=issue_code,
        concept_id=concept_id,
        location="local_span",
        severity="major",
        type=issue_code,
        description=f"Targeted local repair for {issue_code}.",
        repair_scope="local_span",
        dependent_checks=["explanatory_clarity", "source_fidelity"],
    )
    return engine.apply_local_repair(note_text, issue, find_text=find_text, replace_text=replace_text)


class QualityEngine:
    def validate_composition(self, vault_root: Path, composition: dict[str, Any]) -> dict[str, Any]:
        from .composition import validate_published_composition
        return validate_published_composition(vault_root, composition)

    def validate_composition_chapter(self, text: str, **kwargs: Any) -> list[str]:
        from .composition import validate_chapter
        return validate_chapter(text, **kwargs)

    def evaluate_chapter_depth(self, plan: dict[str, Any], chapter: dict[str, Any], body: str) -> dict[str, Any]:
        from .composition.contracts import evaluate_chapter_depth_contract
        return evaluate_chapter_depth_contract(plan, chapter, body)

    def evaluate_teaching(
        self,
        note_text: str,
        *,
        concept_spec: dict[str, Any] | None = None,
        equations: list[dict[str, Any]] | None = None,
        worked_examples: list[dict[str, Any]] | None = None,
        visuals: list[dict[str, Any]] | None = None,
        learner_level: str = "beginner",
    ) -> dict[str, Any]:
        return evaluate_teaching_quality(
            note_text,
            concept_spec=concept_spec,
            equations=equations,
            worked_examples=worked_examples,
            visuals=visuals,
            learner_level=learner_level,
        )

    """Cohesive Engine E5 facade for verification, representation checks, EIS-07 clarity review, targeted repair, auditing, and golden evals."""

    def __init__(self, root: Path = REPO_ROOT):
        self.root = root
        self.repair = RepairEngine()
        self.harness = EvaluationHarness(root)

    def check_representations(self, spec: dict[str, Any]) -> dict[str, Any]:
        return check_representation_consistency(spec)

    def review_explanatory_clarity(
        self,
        document: str,
        explanation_blueprint: Any | None = None,
        *,
        learner_profile: str = "intermediate",
        representation_spec: dict[str, Any] | None = None,
        source_mode: str | None = None,
    ) -> dict[str, Any]:
        return review_explanatory_clarity(
            document,
            explanation_blueprint,
            learner_profile=learner_profile,
            representation_spec=representation_spec,
            source_mode=source_mode,
        )

    def repair_clarity(self, note_text: str, **kwargs: Any) -> dict[str, Any]:
        return repair_explanatory_friction(note_text, repair_engine=self.repair, **kwargs)

    def audit_repo(self, *, include_inventory: bool = False) -> dict[str, Any]:
        result = audit_repository(self.root)
        if include_inventory:
            result["inventory"] = repository_inventory(self.root)
        return result

    def audit_compliance(self) -> dict[str, Any]:
        return audit_reconstruction_compliance(self.root)

    def lint_authority(self) -> dict[str, Any]:
        return lint_instruction_authority(self.root)

    def run_golden_evaluations(self, cases: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        return self.harness.run_all(cases)

    def validate_master(self, note_text: str, master: str, *, variant: str | None = None) -> list[str]:
        return validate_master_output(note_text, master, variant=variant)

    def validate_properties(self, note_text: str, *, expected_note_type: str | None = None) -> list[str]:
        return validate_obsidian_properties(note_text, expected_note_type=expected_note_type)

    def validate_collection(self, vault_root: Path, plan: Any, *, manifest: dict[str, Any] | None = None) -> dict[str, Any]:
        return validate_note_collection(vault_root, plan, manifest=manifest)

    def validate_competencies(self, note_text: str, outcomes: list[dict[str, Any]]) -> dict[str, Any]:
        from scriptorium.engines._collection_intelligence import validate_competency_coverage
        return validate_competency_coverage(note_text, outcomes)

    def process_feedback(self, vault_root: Path, plan: Any, feedback_text: str, **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._collection_intelligence import process_reader_feedback
        return process_reader_feedback(vault_root, plan, feedback_text, **kwargs)

    # Zero-Redundancy Validation & Minimal Targeted Repair Context (Opt I, J, U)
    def validate_zero_redundancy(self, note_text: str, **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._token_optimizer import run_zero_redundancy_validation
        return run_zero_redundancy_validation(note_text, **kwargs)

    def build_repair_context(self, note_text: str, *, target_section: str, issue_description: str, **kwargs: Any) -> dict[str, Any]:
        from scriptorium.engines._token_optimizer import build_targeted_repair_context
        return build_targeted_repair_context(note_text, target_section=target_section, issue_description=issue_description, **kwargs)


# ---------------------------------------------------------------------------
# Part 24 — Collection-Wide Quality Validation
# ---------------------------------------------------------------------------

_WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
_PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|coming\s+soon|insert\s+content\s+here|placeholder\s+note)\b", re.I)


def _has_cycle(graph: dict[str, list[str]]) -> bool:
    state: dict[str, int] = {}  # 0=unvisited, 1=visiting, 2=done

    def _dfs(node: str) -> bool:
        state[node] = 1
        for nxt in graph.get(node, []):
            if nxt not in graph:
                continue
            if state.get(nxt, 0) == 1:
                return True
            if state.get(nxt, 0) == 0 and _dfs(nxt):
                return True
        state[node] = 2
        return False

    return any(_dfs(n) for n in graph if state.get(n, 0) == 0)


def validate_note_collection(
    vault_root: Path,
    plan: Any,
    *,
    manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate structural, wikilink, Obsidian Properties, coverage, DAG, duplication, and consistency integrity across a collection."""
    vault_root = Path(vault_root)
    issues: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    def _err(category: str, node_id: str, detail: str) -> None:
        issues.append({"category": category, "node_id": node_id, "severity": "error", "detail": detail})

    def _warn(category: str, node_id: str, detail: str) -> None:
        warnings.append({"category": category, "node_id": node_id, "severity": "warning", "detail": detail})

    node_map: dict[str, Any] = {}
    for node in plan.nodes:
        if node.concept_id in node_map:
            _err("structural_integrity", node.concept_id, f"Duplicate concept_id '{node.concept_id}' in collection plan.")
        node_map[node.concept_id] = node

    # Index all existing vault titles/stems + collection titles for wikilink resolution
    vault_stems = {p.stem.lower() for p in vault_root.rglob("*.md") if ".scriptorium" not in p.parts}
    collection_titles = {n.title.lower(): n for n in plan.nodes}
    collection_stems = {Path(n.proposed_path).stem.lower(): n for n in plan.nodes}

    # Check root index existence for hierarchical collections
    if plan.organization == "hierarchical_collection":
        root_node = node_map.get(plan.root_topic_id)
        if root_node is None or root_node.note_role != "root_index":
            _err("structural_integrity", plan.root_topic_id, "Hierarchical collection is missing a root_index node.")

    # Check prerequisite DAG acyclicity
    prereq_graph = {n.concept_id: list(n.prerequisite_ids) for n in plan.nodes}
    if _has_cycle(prereq_graph):
        _err("cross_note_consistency", plan.root_topic_id, "Circular dependency detected in prerequisite_ids graph.")

    parsed_notes: dict[str, Any] = {}
    domains_seen: set[str] = set()
    master_topics_seen: set[str] = set()
    collection_ids_seen: set[str] = set()
    files_found = 0

    for node in plan.nodes:
        fpath = vault_root / node.proposed_path
        if not fpath.is_file():
            _err("coverage_completeness", node.concept_id, f"Planned note file missing on disk: {node.proposed_path}")
            continue
        files_found += 1
        text = fpath.read_text(encoding="utf-8-sig")
        parsed = parse_note(text)
        parsed_notes[node.concept_id] = (text, parsed)

        # 1. Obsidian Properties validation
        expected_nt = "index" if node.note_role in {"root_index", "group_index"} else None
        prop_errs = validate_obsidian_properties(text, expected_note_type=expected_nt)
        for pe in prop_errs:
            _err("obsidian_properties", node.concept_id, f"{node.proposed_path}: {pe}")

        meta = parsed.metadata
        if meta.get("domain"):
            domains_seen.add(str(meta["domain"]))
        if meta.get("master_topic"):
            master_topics_seen.add(str(meta["master_topic"]))
        if meta.get("collection_id"):
            collection_ids_seen.add(str(meta["collection_id"]))

        # 2. Structural parent-child checks & orphan check
        if node.note_role not in {"root_index", "single"}:
            if not node.parent_id or node.parent_id not in node_map:
                _err("structural_integrity", node.concept_id, f"Orphan note '{node.title}' has no valid parent_id.")
            else:
                parent_node = node_map[node.parent_id]
                if node.concept_id not in parent_node.child_ids:
                    _err("structural_integrity", node.concept_id, f"Parent '{parent_node.title}' does not list '{node.title}' in child_ids.")
                # Verify child links back to parent
                if f"[[{parent_node.title}]]" not in parsed.body:
                    _err("wikilink_navigation", node.concept_id, f"Child note '{node.title}' does not link back to parent [[{parent_node.title}]].")

        # 3. Non-placeholder & depth checks
        words = len(re.findall(r"\b\w+\b", parsed.body))
        if _PLACEHOLDER_RE.search(parsed.body):
            _err("coverage_completeness", node.concept_id, f"Placeholder stub text detected in '{node.proposed_path}'.")
        if node.note_role in {"child", "single"}:
            if words < 40:
                _err("coverage_completeness", node.concept_id, f"Note '{node.title}' is too shallow ({words} words) to be a substantive educational note.")
            if len(parsed.sections) < 2:
                _err("coverage_completeness", node.concept_id, f"Note '{node.title}' has fewer than 2 structured sections.")
        else:
            # Parent MOC checks: must link to every child AND must not duplicate child bodies
            for cid in node.child_ids:
                child = node_map.get(cid)
                if child and f"[[{child.title}]]" not in parsed.body:
                    _err("wikilink_navigation", node.concept_id, f"Parent MOC '{node.title}' is missing wikilink to child [[{child.title}]].")
            if "```python" in parsed.body or "$$" in parsed.body:
                _warn("duplication_boundary", node.concept_id, f"Parent MOC '{node.title}' contains code or display derivations that belong inside child notes.")

        # 4. Wikilink resolution check (flag broken internal links while allowing explicit external prerequisite labels)
        external_allowed = {
            (node_map[x].title if x in node_map else x).lower()
            for x in (*node.prerequisite_ids, *node.related_ids)
            if x not in node_map
        }
        for target in _WIKILINK_RE.findall(parsed.body):
            t_low = target.strip().lower()
            if (
                t_low not in collection_titles
                and t_low not in collection_stems
                and t_low not in vault_stems
                and t_low not in external_allowed
            ):
                _err("wikilink_navigation", node.concept_id, f"Broken wikilink [[{target}]] in '{node.proposed_path}'.")

    # 5. Cross-note metadata consistency
    if len(domains_seen) > 1:
        _warn("cross_note_consistency", plan.root_topic_id, f"Multiple domains across collection: {sorted(domains_seen)}")
    if len(master_topics_seen) > 1:
        _warn("cross_note_consistency", plan.root_topic_id, f"Multiple master_topics across collection: {sorted(master_topics_seen)}")
    if len(collection_ids_seen) > 1:
        _err("cross_note_consistency", plan.root_topic_id, f"Inconsistent collection_id values across notes: {sorted(collection_ids_seen)}")

    # 6. Manifest honesty check
    if manifest is not None:
        if manifest.get("completed_count") != files_found:
            _err(
                "coverage_completeness",
                plan.root_topic_id,
                f"Manifest claims completed_count={manifest.get('completed_count')} but {files_found} files exist on disk.",
            )

    return {
        "valid": not issues,
        "collection_id": plan.collection_id,
        "organization": plan.organization,
        "planned_notes": len(plan.nodes),
        "verified_files": files_found,
        "domains": sorted(domains_seen),
        "master_topics": sorted(master_topics_seen),
        "issues": issues,
        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# Part 16 — Evidence-Based Teaching-Quality Verification & Beginner Reader Simulation
# ---------------------------------------------------------------------------

TEACHING_QUALITY_DIMENSIONS: tuple[str, ...] = (
    "conceptual_completeness",
    "prerequisite_sufficiency",
    "intuitive_clarity",
    "mathematical_explanation",
    "worked_example_quality",
    "intermediate_reasoning",
    "narrative_continuity",
    "visual_integration",
    "beginner_accessibility",
    "technical_accuracy",
    "appropriate_depth",
    "assessment_quality",
)

BEGINNER_READER_SIMULATION_QUESTIONS: tuple[tuple[str, str], ...] = (
    ("first_concept_defined", "Is the first unfamiliar technical concept defined before relying on it?"),
    ("motivation_clear", "Does the reader understand why this problem or concept matters?"),
    ("mechanism_followable", "Can a beginner follow how each step or component produces the result?"),
    ("math_understandable", "Are equations prepared, symbolized, dimensioned, and decomposed clearly?"),
    ("example_reconstructible", "Can the reader reconstruct a worked example from declared inputs alone?"),
    ("images_explained", "Are embedded figures accompanied by clear reading guides and observations?"),
    ("assumptions_clear", "Are applicability conditions, failure cases, and limits explicitly stated?"),
    ("continuity_smooth", "Can the reader transition cleanly to adjacent/next concepts?"),
)


def _body_excerpt(body: str, pattern: str) -> str | None:
    m = re.search(pattern, body, re.I | re.S)
    if not m:
        return None
    return body[max(0, m.start() - 20):min(len(body), m.end() + 90)].replace("\n", " ").strip()


def _record_dimension(
    dimensions: dict[str, dict[str, Any]],
    repairs: list[dict[str, str]],
    name: str,
    applicable: bool,
    score: int | None,
    evidence: str,
    justification: str,
    repair_action: str | None = None,
) -> None:
    dimensions[name] = {
        "applicable": applicable,
        "score": score,
        "evidence": evidence,
        "justification": justification,
    }
    if applicable and score is not None and score <= 1 and repair_action:
        repairs.append({"dimension": name, "action": repair_action, "reason": justification})


def _run_teaching_subchecks(
    note_text: str,
    body: str,
    *,
    equations: list[dict[str, Any]] | None,
    worked_examples: list[dict[str, Any]] | None,
    visuals: list[dict[str, Any]] | None,
    learner_level: str,
    has_math: bool,
    has_visuals: bool,
) -> dict[str, Any]:
    """Execute underlying clarity, math deconstruction, worked-example, and visual checks."""
    from scriptorium.engines.mathematics import validate_worked_solution, verify_math_deconstruction

    clarity = review_explanatory_clarity(note_text, learner_profile=learner_level)
    math_check = (
        verify_math_deconstruction(note_text, equations=equations, learner_level=learner_level)
        if has_math else {"passed": True, "issues": []}
    )
    worked_errors: list[str] = []
    if worked_examples:
        for ex in worked_examples:
            wk = validate_worked_solution(note_text, ex, learner_level=learner_level)
            if not wk["valid"]:
                worked_errors.extend(wk["errors"])
    elif has_math and learner_level in {"beginner", "intermediate"}:
        worked_errors.extend(validate_worked_solution(note_text, learner_level=learner_level)["errors"])

    visual_errors: list[str] = []
    if has_visuals:
        from scriptorium.engines.composition.bvia import validate_image_grounded_explanation
        for idx, vis in enumerate(visuals or [{"id": "embedded_visual", "objective": "visual explanation"}]):
            vr = validate_image_grounded_explanation(body, vis)
            if not vr["passed"]:
                visual_errors.extend(f"visual[{idx}]: {e}" for e in vr["errors"])

    return {
        "clarity": clarity,
        "math_check": math_check,
        "worked_errors": worked_errors,
        "visual_errors": visual_errors,
    }


def _score_foundation_and_clarity(
    parsed: Any,
    body: str,
    lowered: str,
    words: int,
    *,
    has_problem: bool,
    concept_spec: dict[str, Any] | None,
    clarity: dict[str, Any],
    dimensions: dict[str, dict[str, Any]],
    critical_defects: list[str],
    repairs: list[dict[str, str]],
) -> None:
    """Score dimensions 1-3: conceptual completeness, prerequisite sufficiency, intuitive clarity."""
    intro_prose = parsed.sections[0].content if parsed.sections else body[:300]
    _record_dimension(
        dimensions, repairs, "conceptual_completeness", True,
        4 if (has_problem and len(parsed.sections) >= 3 and words >= 200) else 3 if (has_problem and words >= 100) else 2 if words >= 60 else 1,
        intro_prose[:160].replace("\n", " ").strip(),
        "Checks whether motivating problem, structure, and substantive explanation depth are present.",
        None if words >= 100 else "expand_motivating_problem_and_core_mechanism",
    )

    missing_prereqs = []
    for pr in (concept_spec or {}).get("prerequisites", []):
        p_label = pr.get("title") or pr.get("concept") or str(pr) if isinstance(pr, dict) else str(pr)
        if p_label and p_label.lower() not in lowered:
            missing_prereqs.append(p_label)
    prereq_ev = _body_excerpt(body, r"\b(?:prerequisite|recall|before|foundation|straight line|vector|first)\b") or "No explicit prerequisite bridge found."
    prereq_score = 1 if missing_prereqs else (4 if "recall" in lowered or "foundation" in lowered or not (concept_spec or {}).get("prerequisites") else 3)
    if missing_prereqs:
        critical_defects.append(f"Missing required prerequisite grounding: {', '.join(missing_prereqs)}")
    _record_dimension(
        dimensions, repairs, "prerequisite_sufficiency", True, prereq_score, prereq_ev,
        "Checks declared prerequisite coverage and foundation preparation before dependent notation.",
        f"add_foundation_bridge:{','.join(missing_prereqs)}" if missing_prereqs else None,
    )

    intuition_ev = _body_excerpt(body, r"\b(?:intuit\w*|mental model|in simple words|meaning|simply|think of|concrete|picture|imagine|just like)\b") or ""
    _record_dimension(
        dimensions, repairs, "intuitive_clarity", True,
        4 if (intuition_ev and not any(i["type"] == "CF-08" for i in clarity["friction_issues"])) else 3 if intuition_ev else 1,
        intuition_ev or "No intuitive explanation passage found.",
        "Checks intuitive mental model before abstract notation and analogy boundary disclosure.",
        None if intuition_ev else "add_starting_intuition_before_formal_equation",
    )


def _score_math_and_examples(
    body: str,
    lowered: str,
    *,
    has_math: bool,
    has_worked: bool,
    worked_examples: list[dict[str, Any]] | None,
    learner_level: str,
    checks: dict[str, Any],
    dimensions: dict[str, dict[str, Any]],
    critical_defects: list[str],
    repairs: list[dict[str, str]],
) -> None:
    """Score dimensions 4-6 & 10: math explanation, worked examples, intermediate reasoning, accuracy."""
    math_check = checks["math_check"]
    worked_errors = checks["worked_errors"]
    clarity = checks["clarity"]

    if has_math:
        m_issues = math_check["issues"]
        crit_m = [i for i in m_issues if i["severity"] == "critical"]
        maj_m = [i for i in m_issues if i["severity"] == "major"]
        if crit_m:
            critical_defects.extend(i["description"] for i in crit_m)
        m_score = 0 if len(maj_m) >= 3 else 1 if (crit_m or len(maj_m) >= 2) else 2 if maj_m else (3 if m_issues else 4)
        _record_dimension(
            dimensions, repairs, "mathematical_explanation", True, m_score,
            m_issues[0]["description"] if m_issues else (_body_excerpt(body, r"\$\$") or "Equations prepared cleanly."),
            "Evaluates equation preparation, symbol definitions, dimension checks, and anti-equation-dumping.",
            "apply_m01_m14_equation_deconstruction" if m_score <= 2 else None,
        )
    else:
        _record_dimension(dimensions, repairs, "mathematical_explanation", False, None, "N/A (non-mathematical)", "Mathematical deconstruction not required on pure non-math topics.")

    if has_worked or has_math:
        w_score = 1 if worked_errors else 4 if (worked_examples or re.search(r"\b(?:sanity|verify|check)\b", lowered)) else 3
        if worked_errors and has_math and learner_level == "beginner":
            critical_defects.append(f"Worked solution incomplete: {worked_errors[0]}")
        _record_dimension(
            dimensions, repairs, "worked_example_quality", True, w_score,
            worked_errors[0] if worked_errors else (_body_excerpt(body, r"\b(?:example|suppose|given|substitute)\b") or "Worked calculation checked."),
            "Checks declared inputs, intermediate operations, interpretation, and sanity verification.",
            "complete_12_step_worked_example" if worked_errors else None,
        )
    else:
        _record_dimension(dimensions, repairs, "worked_example_quality", False, None, "N/A", "Quantitative worked example not triggered.")

    cf_03 = [i for i in clarity["friction_issues"] if i["type"] == "CF-03"]
    inter_score = 1 if cf_03 else (4 if re.search(r"(?:^|\n)\s*\d+\.|step\s+1|expanding|substituting", lowered) else 3)
    _record_dimension(
        dimensions, repairs, "intermediate_reasoning", True, inter_score,
        cf_03[0]["description"] if cf_03 else (_body_excerpt(body, r"(?:step|therefore|because|implies|expanding)") or "Continuous reasoning."),
        "Checks for skipped derivation/mechanism steps or unmotivated operation jumps.",
        "expand_intermediate_transitions" if cf_03 else None,
    )

    spec_errors = [i["description"] for i in math_check["issues"] if i["severity"] == "critical"]
    acc_tech = 0 if (spec_errors or worked_errors) else 4
    _record_dimension(
        dimensions, repairs, "technical_accuracy", True, acc_tech,
        spec_errors[0] if spec_errors else (worked_errors[0] if worked_errors else "Deterministic shape/arithmetic checks clear."),
        "Verifies arithmetic/dimensional consistency and absence of unsupported overclaims.",
        "fix_arithmetic_or_dimension_error" if acc_tech == 0 else None,
    )


def _score_continuity_accessibility_depth(
    note_text: str,
    parsed: Any,
    body: str,
    words: int,
    *,
    has_visuals: bool,
    learner_level: str,
    concept_spec: dict[str, Any] | None,
    checks: dict[str, Any],
    dimensions: dict[str, dict[str, Any]],
    critical_defects: list[str],
    repairs: list[dict[str, str]],
) -> None:
    """Score dimensions 7-9 & 11-12: narrative continuity, visual integration, accessibility, depth, assessment."""
    clarity = checks["clarity"]
    visual_errors = checks["visual_errors"]

    cf_04 = [i for i in clarity["friction_issues"] if i["type"] in {"CF-04", "CF-06", "CF-09"}]
    has_leaked_stub = bool(re.search(r"\*Key mathematical claim:\*|<!--", body))
    if has_leaked_stub:
        critical_defects.append("Internal authoring stub or comment leaked into finished prose.")
    dup_h1_h2 = bool(re.search(r"^#\s+(.+)\n+^##\s+\1\s*$", body, re.M | re.I))
    if dup_h1_h2:
        critical_defects.append("Duplicate consecutive H1 and H2 chapter-title headings detected.")
    nav_score = 1 if (has_leaked_stub or dup_h1_h2 or len(cf_04) >= 2) else 2 if cf_04 else 4
    _record_dimension(
        dimensions, repairs, "narrative_continuity", True, nav_score,
        "Duplicate consecutive H1/H2 heading." if dup_h1_h2 else (cf_04[0]["description"] if cf_04 else "Section openings and transitions maintain continuous prose."),
        "Checks natural problem-to-concept bridges, avoids heading-into-equation drops, duplicate H1/H2 headers, and stub leaks.",
        "add_natural_transitions_and_strip_stubs" if nav_score <= 2 else None,
    )

    if has_visuals:
        post_code_fig = bool(re.search(r"```\s*\n+!\[\[", body))
        all_vis_errors = list(visual_errors)
        if post_code_fig:
            all_vis_errors.append("Figure appears immediately after a code fence instead of where the learner first needs the visual concept.")
        v_score = 1 if all_vis_errors else 4
        _record_dimension(
            dimensions, repairs, "visual_integration", True, v_score,
            all_vis_errors[0] if all_vis_errors else (_body_excerpt(body, r"!\[\[|```mermaid") or "Visual integrated cleanly."),
            "Checks local embed + Explain -> Show -> Decode -> Connect reading walkthrough and conceptual visual placement.",
            "place_visuals_at_conceptual_need_with_walkthrough" if all_vis_errors else None,
        )
    else:
        _record_dimension(dimensions, repairs, "visual_integration", False, None, "N/A", "No embedded visual in this note.")

    from scriptorium.engines.pedagogy import analyze_information_density
    density_rep = analyze_information_density(note_text, reader_level=learner_level)
    heavy_density = [
        sec for sec in density_rep.get("overloaded_sections", [])
        if sec.get("unique_symbols", 0) > 5 or sec.get("display_equations", 0) >= 4
    ]
    jargon_issues = [i for i in clarity["friction_issues"] if i["type"] in {"CF-01", "CF-02", "CF-11"}]
    if heavy_density and learner_level == "beginner":
        jargon_issues.append({
            "type": "CF-05",
            "severity": "major",
            "description": f"Section '{heavy_density[0]['heading']}' packs excessive symbols/equations without intermediate anchoring.",
        })
    acc_score = 1 if len(jargon_issues) >= 2 else 2 if jargon_issues else 4
    if learner_level == "beginner" and any(i["type"] == "CF-11" for i in jargon_issues):
        critical_defects.append("Premature unexplained advanced jargon appears in beginner introduction.")
    _record_dimension(
        dimensions, repairs, "beginner_accessibility", True, acc_score,
        jargon_issues[0]["description"] if jargon_issues else "Technical vocabulary and density match learner level.",
        "Checks undefined jargon, high symbol density, and cognitive load in introductory prose.",
        "define_terms_before_first_use" if jargon_issues else None,
    )

    concepts_claimed = len((concept_spec or {}).get("subconcepts", [])) or 1
    overcompressed = concepts_claimed >= 3 and words < concepts_claimed * 90
    if overcompressed:
        critical_defects.append(f"Overcompressed chapter: {concepts_claimed} subconcepts packed into {words} words.")
    _record_dimension(
        dimensions, repairs, "appropriate_depth", True,
        1 if overcompressed else (4 if words >= 250 else 3 if words >= 120 else 2),
        f"{words} words across {len(parsed.sections)} sections ({concepts_claimed} subconcept scope).",
        "Detects superficial compression where major concepts are reduced to sparse bullets.",
        "split_or_deepen_overcompressed_concepts" if overcompressed else None,
    )

    has_q = bool(re.search(r"(?:###\s+Q\d|\*\*Question\s*\(|> \[!(?:hint|answer|tip)\]-)", body, re.I))
    has_detailed_ans = bool(re.search(r"> \[!(?:answer|tip)\]-[\s\S]{40,}", body, re.I))
    _record_dimension(
        dimensions, repairs, "assessment_quality", has_q,
        (4 if has_detailed_ans else 2) if has_q else None,
        _body_excerpt(body, r"> \[!(?:answer|tip)\]-") or "No assessment section included.",
        "Checks collapsible hints and step-by-step detailed solutions rather than bare final values.",
        "expand_answer_reasoning" if (has_q and not has_detailed_ans) else None,
    )


def evaluate_teaching_quality(
    note_text: str,
    *,
    concept_spec: dict[str, Any] | None = None,
    equations: list[dict[str, Any]] | None = None,
    worked_examples: list[dict[str, Any]] | None = None,
    visuals: list[dict[str, Any]] | None = None,
    learner_level: str = "beginner",
) -> dict[str, Any]:
    """Evaluate 12 teaching quality dimensions (0-4 scale) with passage evidence and non-averaging critical gates."""
    parsed = parse_note(note_text)
    body = parsed.body
    lowered = body.lower()
    level = (learner_level or "beginner").strip().lower()
    words = len(re.findall(r"\b\w+\b", body))

    has_math = bool(re.search(r"\$\$.*?\$\$|(?<!\$)\$(?!\$)[^$\n]+\$", body, re.S)) or bool(equations)
    has_visuals = ("![[" in body or "```mermaid" in body) or bool(visuals)
    has_worked = bool(worked_examples) or bool(re.search(r"\b(?:worked\s+example|numerical|substitution|step\s+1)\b", lowered))
    has_problem = bool(_body_excerpt(body, r"\b(?:problem|why|need|motivat|solve|predict|imagine|suppose|consider)\b"))

    checks = _run_teaching_subchecks(
        note_text, body,
        equations=equations, worked_examples=worked_examples, visuals=visuals,
        learner_level=level, has_math=has_math, has_visuals=has_visuals,
    )

    dimensions: dict[str, dict[str, Any]] = {}
    critical_defects: list[str] = []
    repairs: list[dict[str, str]] = []

    _score_foundation_and_clarity(
        parsed, body, lowered, words,
        has_problem=has_problem, concept_spec=concept_spec, clarity=checks["clarity"],
        dimensions=dimensions, critical_defects=critical_defects, repairs=repairs,
    )
    _score_math_and_examples(
        body, lowered,
        has_math=has_math, has_worked=has_worked, worked_examples=worked_examples,
        learner_level=level, checks=checks,
        dimensions=dimensions, critical_defects=critical_defects, repairs=repairs,
    )
    _score_continuity_accessibility_depth(
        note_text, parsed, body, words,
        has_visuals=has_visuals, learner_level=level, concept_spec=concept_spec,
        checks=checks, dimensions=dimensions, critical_defects=critical_defects, repairs=repairs,
    )

    simulation = {
        "first_concept_defined": dimensions["beginner_accessibility"]["score"] >= 3,
        "motivation_clear": has_problem,
        "mechanism_followable": dimensions["intermediate_reasoning"]["score"] >= 3,
        "math_understandable": (not has_math) or (dimensions["mathematical_explanation"]["score"] >= 3),
        "example_reconstructible": (not dimensions["worked_example_quality"]["applicable"]) or (dimensions["worked_example_quality"]["score"] >= 3),
        "images_explained": (not has_visuals) or (dimensions["visual_integration"]["score"] >= 3),
        "assumptions_clear": bool(re.search(r"\b(?:assum|condition|limit|avoid|when\s+not|invalid|fail)\b", lowered)),
        "continuity_smooth": dimensions["narrative_continuity"]["score"] >= 3,
    }
    failing_dims = [
        k for k, d in dimensions.items()
        if d["applicable"] and d["score"] is not None and d["score"] < 2
    ]
    return {
        "passed": (not critical_defects) and (not failing_dims),
        "learner_level": level,
        "critical_defects": critical_defects,
        "failing_dimensions": failing_dims,
        "dimensions": dimensions,
        "beginner_reader_simulation": simulation,
        "formula_folds": checks["math_check"].get("formula_folds"),
        "targeted_repairs": repairs,
        "evidence_based": True,
        "non_averaging_gate": True,
    }

