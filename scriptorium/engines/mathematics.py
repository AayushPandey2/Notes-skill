"""Dedicated Mathematical Deconstruction (M01-M14) & Numerical Problem-Solving Engine (Step 1-12).

Owned cleanly by A2 (Tutor) and verified by A9 (Checker). Never stores hardcoded
subject-specific lessons; inspects arbitrary mathematical expressions, matrix/vector
shapes, symbolic notation, worked arithmetic, and Markdown explanations structurally.
"""
from __future__ import annotations

import math
import re
from typing import Any

from scriptorium.models import parse_note

MATH_EXPLANATION_OBLIGATIONS: dict[str, tuple[str, str]] = {
    "M01": ("Purpose", "Why does this equation exist and what quantity does it compute?"),
    "M02": ("Pronunciation", "How is the mathematical notation read aloud cleanly?"),
    "M03": ("Symbol Inventory", "What does every symbol, subscript, superscript, transpose, and operator mean?"),
    "M04": ("Object Types", "Which quantities are scalars, vectors, matrices, tensors, functions, parameters, or operators?"),
    "M05": ("Dimensions", "What shapes, sizes, or physical units make each operation valid?"),
    "M06": ("Operation Breakdown", "What individual operations occur and in what evaluation order?"),
    "M07": ("Expanded Form", "How does compact matrix or summation notation look when written out explicitly?"),
    "M08": ("Numerical Substitution", "How do declared concrete numbers plug into the formula?"),
    "M09": ("Step-by-Step Arithmetic", "What are the intermediate values before reaching the final output?"),
    "M10": ("Interpretation", "What does the computed numerical result mean in context?"),
    "M11": ("Sanity Check", "Do dimensions, signs, units, bounds, or special cases confirm plausibility?"),
    "M12": ("Common Misunderstandings", "What notation, transpose, scaling, or assumption mistakes commonly happen?"),
    "M13": ("Generalization", "How does the concrete worked case map back to arbitrary dimensions or inputs?"),
    "M14": ("Advanced Details", "What deeper assumptions, edge regimes, or alternative formulations apply once basics hold?"),
}

MATHEMATICAL_OBJECT_TYPES = frozenset({
    "scalar",
    "vector",
    "matrix",
    "tensor",
    "function",
    "parameter",
    "random_variable",
    "index",
    "operator",
    "set",
})

NUMERICAL_SOLUTION_STEPS: tuple[tuple[str, str], ...] = (
    ("Step 1", "Understand the Question"),
    ("Step 2", "Identify Relevant Concepts"),
    ("Step 3", "State Assumptions"),
    ("Step 4", "Define Symbols"),
    ("Step 5", "Choose the Formula"),
    ("Step 6", "Substitute Values"),
    ("Step 7", "Perform Intermediate Operations"),
    ("Step 8", "Compute the Result"),
    ("Step 9", "Interpret the Answer"),
    ("Step 10", "Verify"),
    ("Step 11", "Discuss Common Mistakes"),
    ("Step 12", "Generalize the Method"),
)

_STOP_LATEX_WORDS = frozenset({
    "frac", "sum", "prod", "int", "min", "max", "argmin", "argmax", "log", "ln", "exp",
    "sin", "cos", "tan", "sqrt", "top", "mathbf", "boldsymbol", "vec", "hat", "bar", "tilde",
    "text", "mathbb", "mathcal", "left", "right", "begin", "end", "bmatrix", "pmatrix",
    "cdot", "times", "approx", "implies", "leq", "geq", "neq", "in", "mid", "nabla", "partial",
    "forall", "exists", "where", "and", "or", "if", "else", "for", "of", "the", "is", "are",
})

_DISPLAY_MATH_RE = re.compile(r"\$\$(.*?)\$\$", re.S)
_INLINE_MATH_RE = re.compile(r"(?<!\$)\$(?!\$)([^$\n]+?)(?<!\$)\$(?!\$)")
_MATRIX_HINT_RE = re.compile(r"(?:\^\{?\\top\}?|\^T\b|\\mathbf|\\vec|\\bmatrix|\\times|@\s*|\\in\s*\\mathbb\{R\}\^)", re.I)
_DERIV_HINT_RE = re.compile(r"(?:\\nabla|\\partial|\\frac\{d|\\frac\{\\partial|d/d[a-zA-Z])")
_PROB_HINT_RE = re.compile(r"(?:\\mathbb\{E\}|\\text\{Var\}|\\text\{Cov\}|\\mathcal\{N\}|\\mid|P\([^)]+\))")
_OPT_HINT_RE = re.compile(r"(?:\\min|\\max|\\arg\\?min|\\arg\\?max|J\(|L\(|\\lambda|\|\|[^|]+\|\|)")
_SUM_HINT_RE = re.compile(r"(?:\\sum|\\prod|\\int)")


def detect_equation_features(equation: str, *, learner_level: str = "beginner") -> dict[str, Any]:
    """Analyze a mathematical expression structurally and determine active M01-M14 obligations."""
    eq = (equation or "").strip()
    if not eq:
        raise ValueError("Equation string must be nonempty")

    has_transpose = bool(re.search(r"\^\{?\\top\}?|\^T\b", eq))
    has_matrix_or_vector = bool(_MATRIX_HINT_RE.search(eq))
    has_sum = bool(_SUM_HINT_RE.search(eq))
    has_deriv = bool(_DERIV_HINT_RE.search(eq))
    has_prob = bool(_PROB_HINT_RE.search(eq))
    has_opt = bool(_OPT_HINT_RE.search(eq))
    has_hat_or_accent = bool(re.search(r"\\(?:hat|bar|tilde)\b", eq))
    has_subscripts = bool(re.search(r"_[A-Za-z0-9{]", eq))

    # Extract symbolic tokens (LaTeX commands + single-letter identifiers) cleanly.
    raw_cmds = re.findall(r"\\([A-Za-z]+)", eq)
    cmd_syms = [f"\\{c}" for c in raw_cmds if c not in _STOP_LATEX_WORDS]
    stripped = re.sub(r"\\[A-Za-z]+", " ", eq)
    letter_syms = re.findall(r"\b([A-Za-z](?:_[A-Za-z0-9]+)?)\b", stripped)
    symbols = list(dict.fromkeys([*cmd_syms, *[s for s in letter_syms if s not in {"T"}]]))

    op_count = len(re.findall(r"[=+\-*/]|\\(?:cdot|times|sum|nabla|partial|frac)", eq))
    complexity = (
        "complex"
        if (has_matrix_or_vector and (has_opt or has_deriv or op_count >= 4)) or op_count >= 5
        else "moderate"
        if (has_matrix_or_vector or has_sum or has_deriv or has_prob or has_opt or op_count >= 2)
        else "simple"
    )

    level = (learner_level or "beginner").strip().lower()
    active = ["M01", "M03", "M06"]
    if level == "beginner" or has_transpose or has_hat_or_accent or complexity in {"moderate", "complex"}:
        active.append("M02")
    if has_matrix_or_vector or has_sum or has_opt:
        active.extend(["M04", "M05"])
    if has_transpose or has_sum or complexity in {"moderate", "complex"}:
        active.append("M07")
    if level != "advanced" or complexity in {"moderate", "complex"}:
        active.extend(["M08", "M09", "M10", "M11", "M12"])
    if complexity in {"moderate", "complex"}:
        active.append("M13")
    if level in {"intermediate", "advanced"} or complexity == "complex":
        active.append("M14")

    # Preserve M01..M14 canonical ordering
    active_set = set(active)
    ordered_obligations = [k for k in MATH_EXPLANATION_OBLIGATIONS if k in active_set]

    return {
        "equation": eq,
        "complexity": complexity,
        "learner_level": level,
        "detected_symbols": symbols,
        "features": {
            "has_transpose": has_transpose,
            "has_matrix_or_vector": has_matrix_or_vector,
            "has_summation": has_sum,
            "has_derivative": has_deriv,
            "has_probability": has_prob,
            "has_optimization": has_opt,
            "has_subscripts": has_subscripts,
        },
        "active_obligations": ordered_obligations,
    }


def _parse_shape(raw: Any) -> tuple[int | str, ...]:
    if isinstance(raw, (list, tuple)) and raw:
        return tuple(int(x) if isinstance(x, (int, float)) and int(x) == x else str(x).strip() for x in raw)
    if isinstance(raw, str) and raw.strip():
        parts = [p.strip() for p in re.split(r"\s*[x×,]\s*", raw.strip()) if p.strip()]
        if parts:
            return tuple(int(p) if p.isdigit() else p for p in parts)
    raise ValueError(f"Invalid shape specification: {raw!r}")


def check_dimension_compatibility(
    operands: list[dict[str, Any]],
    *,
    operation: str = "matmul",
) -> dict[str, Any]:
    """Deterministically verify vector/matrix shapes and inner dimensions before prose cites them."""
    if not isinstance(operands, list) or len(operands) < 1:
        raise ValueError("At least one operand is required for dimension checking")

    normalized: list[dict[str, Any]] = []
    for idx, op in enumerate(operands):
        name = str(op.get("name") or f"operand_{idx + 1}")
        shape = _parse_shape(op.get("shape"))
        transpose = bool(op.get("transpose", False))
        if transpose:
            if len(shape) != 2:
                raise ValueError(f"Transpose requires a 2D shape for '{name}', got {shape}")
            eff_shape: tuple[int | str, ...] = (shape[1], shape[0])
        else:
            eff_shape = shape
        normalized.append({
            "name": name,
            "original_shape": shape,
            "transpose": transpose,
            "effective_shape": eff_shape,
            "unit": op.get("unit"),
        })

    op_kind = operation.strip().lower()
    if op_kind in {"matmul", "matrix_multiply"}:
        if len(normalized) < 2:
            raise ValueError("Matrix multiplication requires at least two operands")
        current = normalized[0]["effective_shape"]
        if len(current) != 2:
            return {"valid": False, "operation": op_kind, "error": f"Expected 2D matrix/column-vector shape for {normalized[0]['name']}, got {current}", "operands": normalized}
        for nxt in normalized[1:]:
            right = nxt["effective_shape"]
            if len(right) != 2:
                return {"valid": False, "operation": op_kind, "error": f"Expected 2D shape for {nxt['name']}, got {right}", "operands": normalized}
            if str(current[1]) != str(right[0]):
                return {
                    "valid": False,
                    "operation": op_kind,
                    "error": f"Dimension mismatch: inner dimensions {current[1]} and {right[0]} do not match for {current} @ {right}",
                    "operands": normalized,
                }
            current = (current[0], right[1])
        is_scalar = len(current) == 2 and str(current[0]) == "1" and str(current[1]) == "1"
        return {
            "valid": True,
            "operation": op_kind,
            "operands": normalized,
            "output_shape": current,
            "output_type": "scalar" if is_scalar else "vector_or_matrix",
            "compatibility_summary": " × ".join(f"({o['effective_shape'][0]}×{o['effective_shape'][1]})" for o in normalized) + f" = ({current[0]}×{current[1]})",
        }

    if op_kind in {"dot", "dot_product", "inner_product"}:
        if len(normalized) != 2:
            raise ValueError("Dot product checks exactly two operands")
        s0, s1 = normalized[0]["effective_shape"], normalized[1]["effective_shape"]
        # Accept two 1D vectors (n,), or column vectors (n, 1) and (n, 1), or (1, n) and (n, 1)
        flat0 = s0[0] if len(s0) == 1 else (s0[0] if len(s0) == 2 and s0[1] == 1 else (s0[1] if len(s0) == 2 and s0[0] == 1 else None))
        flat1 = s1[0] if len(s1) == 1 else (s1[0] if len(s1) == 2 and s1[1] == 1 else (s1[1] if len(s1) == 2 and s1[0] == 1 else None))
        if flat0 is None or flat1 is None or str(flat0) != str(flat1):
            return {"valid": False, "operation": op_kind, "error": f"Dot product requires matching vector lengths, got {s0} and {s1}", "operands": normalized}
        return {
            "valid": True,
            "operation": op_kind,
            "operands": normalized,
            "output_shape": (1, 1),
            "output_type": "scalar",
            "compatibility_summary": f"dot({s0}, {s1}) -> scalar (1×1)",
        }

    if op_kind in {"add", "subtract", "elementwise", "hadamard"}:
        first_shape = normalized[0]["effective_shape"]
        first_unit = normalized[0].get("unit")
        for nxt in normalized[1:]:
            if tuple(str(x) for x in nxt["effective_shape"]) != tuple(str(x) for x in first_shape):
                return {"valid": False, "operation": op_kind, "error": f"Shape mismatch for {op_kind}: {first_shape} vs {nxt['effective_shape']}", "operands": normalized}
            if first_unit and nxt.get("unit") and first_unit != nxt["unit"]:
                return {"valid": False, "operation": op_kind, "error": f"Unit mismatch for {op_kind}: '{first_unit}' vs '{nxt['unit']}'", "operands": normalized}
        return {"valid": True, "operation": op_kind, "operands": normalized, "output_shape": first_shape, "output_type": "scalar" if first_shape == (1, 1) else "array"}

    raise ValueError(f"Unsupported dimension operation: {operation}")


def verify_worked_calculation(
    steps: list[dict[str, Any]],
    *,
    variables: dict[str, float] | None = None,
    expected_result: float | None = None,
    tol: float = 1e-4,
) -> dict[str, Any]:
    """Deterministically verify step-by-step numerical substitutions and intermediate arithmetic."""
    from scriptorium.engines.composition.checks import arithmetic

    if not isinstance(steps, list) or not steps:
        return {"valid": False, "errors": ["Worked calculation requires at least one step"], "evaluated_steps": []}

    env: dict[str, float] = {}
    for k, v in (variables or {}).items():
        if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v)):
            env[k] = float(v)

    errors: list[str] = []
    evaluated: list[dict[str, Any]] = []
    last_val: float | None = None

    for idx, step in enumerate(steps, 1):
        expr = str(step.get("expr") or "").strip()
        target = str(step.get("assign") or step.get("label") or f"step_{idx}").strip()
        if not expr:
            errors.append(f"Step {idx}: missing arithmetic expression")
            continue
        try:
            computed = arithmetic(expr, env)
        except Exception as exc:
            errors.append(f"Step {idx} ({target}): invalid arithmetic expression '{expr}': {exc}")
            continue
        stated = step.get("result")
        if stated is not None:
            if not isinstance(stated, (int, float)) or not math.isfinite(float(stated)):
                errors.append(f"Step {idx} ({target}): nonfinite stated result {stated!r}")
            elif abs(computed - float(stated)) > tol:
                errors.append(f"Step {idx} ({target}): stated {stated} disagrees with computed {round(computed, 6)}")
        env[target] = computed
        last_val = computed
        evaluated.append({
            "step": idx,
            "label": step.get("label") or target,
            "expr": expr,
            "computed": round(computed, 6),
            "stated": stated,
            "explanation": step.get("explanation", ""),
        })

    if expected_result is not None and last_val is not None:
        if abs(last_val - float(expected_result)) > tol:
            errors.append(f"Final computed result {round(last_val, 6)} disagrees with expected {expected_result}")

    return {"valid": not errors, "errors": errors, "evaluated_steps": evaluated, "final_value": round(last_val, 6) if last_val is not None else None}


def deconstruct_equation(spec: dict[str, Any], *, learner_level: str = "beginner") -> dict[str, Any]:
    """Produce a domain-independent M01-M14 structured breakdown + beginner-readable prose."""
    if not isinstance(spec, dict) or not str(spec.get("equation") or "").strip():
        raise ValueError("Equation specification requires a non-empty 'equation' string")

    eq = str(spec["equation"]).strip()
    features = detect_equation_features(eq, learner_level=learner_level)
    active = features["active_obligations"]

    symbols = list(spec.get("symbols") or [])
    for sym in symbols:
        if not sym.get("symbol") or not sym.get("meaning"):
            raise ValueError("Each symbol entry requires non-empty 'symbol' and 'meaning'")
        otype = sym.get("type")
        if otype and otype not in MATHEMATICAL_OBJECT_TYPES:
            raise ValueError(f"Unknown mathematical object type: {otype}")

    dim_check: dict[str, Any] | None = None
    if spec.get("dimension_operands"):
        dim_check = check_dimension_compatibility(
            spec["dimension_operands"],
            operation=str(spec.get("dimension_operation") or "matmul"),
        )
        if not dim_check["valid"]:
            raise ValueError(dim_check["error"])

    calc_check: dict[str, Any] | None = None
    num_ex = spec.get("numerical_example")
    if isinstance(num_ex, dict) and num_ex.get("steps"):
        calc_check = verify_worked_calculation(
            num_ex["steps"],
            variables=num_ex.get("inputs"),
            expected_result=num_ex.get("expected_result"),
        )
        if not calc_check["valid"]:
            raise ValueError(f"Worked numerical substitution failed verification: {calc_check['errors']}")

    lines: list[str] = []
    if spec.get("purpose"):
        lines.append(str(spec["purpose"]).strip())
        lines.append("")
    lines.extend(["$$", eq, "$$", ""])
    if spec.get("pronunciation"):
        lines.append(f"*Read aloud:* {spec['pronunciation'].strip()}")
        lines.append("")
    if symbols:
        lines.extend(["| Symbol | Name / Meaning | Type | Shape / Units | Role |", "|---|---|---|---|---|"])
        for s in symbols:
            lines.append(
                f"| ${s['symbol']}$ | {s['meaning']} | {s.get('type', 'quantity')} | "
                f"{s.get('shape') or s.get('units') or 'scalar'} | {s.get('role', s['meaning'])} |"
            )
        lines.append("")
    if dim_check:
        lines.append(f"**Shape compatibility:** `{dim_check.get('compatibility_summary') or dim_check.get('output_shape')}`.")
        lines.append("")
    if spec.get("expanded_form"):
        lines.extend(["**Expanded elementary form:**", "", "$$", str(spec["expanded_form"]).strip(), "$$", ""])
    if spec.get("operation_breakdown"):
        lines.append("**Step-by-step operations:**")
        for idx, step_text in enumerate(spec["operation_breakdown"], 1):
            lines.append(f"{idx}. {step_text}")
        lines.append("")
    if isinstance(num_ex, dict) and (calc_check or num_ex.get("summary")):
        lines.append("**Concrete numerical substitution (synthetic example):**")
        if num_ex.get("inputs"):
            formatted_inputs = ", ".join(f"`{k} = {v}`" for k, v in num_ex["inputs"].items())
            lines.append(f"- **Declared inputs:** {formatted_inputs}")
        if calc_check:
            for st in calc_check["evaluated_steps"]:
                expl = f" — {st['explanation']}" if st.get("explanation") else ""
                lines.append(f"- **{st['label']}:** `{st['expr']}` = `{st['computed']}`{expl}")
        if num_ex.get("interpretation"):
            lines.append(f"- **Interpretation:** {num_ex['interpretation']}")
        if num_ex.get("sanity_check"):
            lines.append(f"- **Sanity check:** {num_ex['sanity_check']}")
        lines.append("")
    if spec.get("misconceptions"):
        lines.append("**Common misunderstandings to avoid:**")
        for mc in spec["misconceptions"]:
            lines.append(f"- {mc}")
        lines.append("")
    if spec.get("generalization"):
        lines.append(f"**Generalizing beyond the example:** {spec['generalization']}")
        lines.append("")

    return {
        "equation": eq,
        "complexity": features["complexity"],
        "active_obligations": active,
        "dimension_check": dim_check,
        "calculation_check": calc_check,
        "markdown": "\n".join(lines).strip() + "\n",
    }


def verify_math_deconstruction(
    note_text: str,
    *,
    equations: list[dict[str, Any]] | None = None,
    learner_level: str = "beginner",
) -> dict[str, Any]:
    """Audit Markdown note prose around equations against M01-M14 requirements (deterministic + structural)."""
    parsed = parse_note(note_text)
    body = parsed.body
    level = (learner_level or "beginner").strip().lower()
    issues: list[dict[str, Any]] = []

    def _issue(code: str, severity: str, description: str, location: str = "body") -> None:
        issues.append({"code": code, "severity": severity, "description": description, "location": location})

    lines = body.splitlines()
    # 1. Check heading directly followed by display equation (unprepared formula drop -> M01 failure)
    for idx, line in enumerate(lines):
        if re.match(r"^#{1,6}\s+", line.strip()):
            j = idx + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].strip().startswith("$$"):
                _issue("MATH-DECON-01", "major", f"Display equation on line {j + 1} immediately follows heading '{line.strip()}' without preparing purpose or context.", f"line_{j + 1}")

    # 2. Check consecutive equation dumping (two $$ blocks separated by < 12 prose words)
    display_spans = [(m.start(), m.end(), m.group(1).strip()) for m in _DISPLAY_MATH_RE.finditer(body)]
    for i in range(len(display_spans) - 1):
        between = body[display_spans[i][1]:display_spans[i + 1][0]].strip()
        prose_words = [w for w in between.split() if not w.startswith(("#", "|", "$", "`"))]
        if len(prose_words) < 6 and not between.startswith("="):
            _issue("MATH-DECON-02", "major", "Back-to-back display equations appear without bridging interpretation or explanation between them.", "display_equations")
            break

    # 3. Inspect matrix/transpose/sum equations for beginner/intermediate scaffolding
    lowered = body.lower()
    for _, _, eq in display_spans:
        feat = detect_equation_features(eq, learner_level=level)
        if feat["features"]["has_transpose"] and level in {"beginner", "intermediate"}:
            if not re.search(r"\b(?:transpose|row\s+vector|column\s+vector|rows?\s+and\s+columns?|inner\s+dimensions?|\\times)\b", lowered):
                _issue("MATH-DECON-03", "major", "Transpose notation appears without explaining row/column orientation or dimension compatibility.", "matrix_dimensions")
        if feat["features"]["has_summation"] and level == "beginner":
            if not re.search(r"\b(?:sum|sigma|add\s+(?:all|up|together)|expand|w_1|x_1)\b", lowered):
                _issue("MATH-DECON-04", "minor", "Compact summation notation appears for a beginner without showing how it expands into terms.", "summation_expansion")

    # 4. Verify symbol introductions for non-trivial symbols appearing in display math
    prose_outside_display = _DISPLAY_MATH_RE.sub(" ", body)
    defined_markers = {
        m.group(1).lstrip("\\")
        for m in re.finditer(r"(?:where|let|denotes?|represents?|means?)\s+\$?(?:\\mathbf\{)?(\\?[A-Za-z]+)", prose_outside_display, re.I)
    }
    table_defined = {
        m.group(1).lstrip("\\")
        for m in re.finditer(r"^\|\s*\$(?:\\hat\{|\\mathbf\{|\\tilde\{)?(\\?[A-Za-z]+)", prose_outside_display, re.M)
    }
    defined = defined_markers | table_defined
    if display_spans and not defined and len(display_spans) >= 2:
        _issue("MATH-DECON-05", "major", "Display equations appear with no identifiable symbol definitions or variable table in surrounding prose.", "symbol_inventory")

    # 5. Deterministically verify supplied structured equation specs
    verified_specs: list[dict[str, Any]] = []
    for spec in equations or []:
        try:
            res = deconstruct_equation(spec, learner_level=level)
            verified_specs.append({"equation": res["equation"], "valid": True, "active_obligations": res["active_obligations"]})
        except ValueError as exc:
            _issue("MATH-DECON-06", "critical", str(exc), "structured_equation_spec")
            verified_specs.append({"equation": spec.get("equation", ""), "valid": False, "error": str(exc)})

    major_or_crit = [i for i in issues if i["severity"] in {"critical", "major"}]
    return {
        "passed": not major_or_crit,
        "issues": issues,
        "display_equation_count": len(display_spans),
        "verified_specs": verified_specs,
    }


def build_worked_solution(problem_spec: dict[str, Any], *, learner_level: str = "beginner") -> dict[str, Any]:
    """Build and deterministically verify a complete Step 1-12 worked numerical solution."""
    required = ("problem", "given", "find", "assumptions", "formula", "steps")
    missing = [k for k in required if not problem_spec.get(k)]
    if missing:
        raise ValueError(f"Worked solution specification missing required fields: {missing}")

    calc = verify_worked_calculation(
        problem_spec["steps"],
        variables=problem_spec.get("given") if isinstance(problem_spec.get("given"), dict) else None,
        expected_result=problem_spec.get("expected_result"),
    )
    if not calc["valid"]:
        raise ValueError(f"Worked calculation verification failed: {calc['errors']}")

    given_str = (
        ", ".join(f"`{k} = {v}`" for k, v in problem_spec["given"].items())
        if isinstance(problem_spec["given"], dict)
        else str(problem_spec["given"])
    )
    lines = [
        f"### Worked Problem: {problem_spec.get('title') or 'Step-by-Step Solution'}",
        "",
        f"- **Question & Objective:** {problem_spec['problem']} Find: {problem_spec['find']}",
        f"- **Given Inputs:** {given_str}",
        f"- **Method & Why It Applies:** {problem_spec.get('method_rationale') or problem_spec['formula']}",
        f"- **Required Assumptions:** {'; '.join(problem_spec['assumptions']) if isinstance(problem_spec['assumptions'], list) else problem_spec['assumptions']}",
        f"- **Governing Formula:** $${problem_spec['formula']}$$",
        "",
        "**Step-by-Step Substitution & Intermediate Operations:**",
    ]
    for st in calc["evaluated_steps"]:
        expl = f" ({st['explanation']})" if st.get("explanation") else ""
        lines.append(f"{st['step']}. **{st['label']}:** `{st['expr']}` = `{st['computed']}`{expl}")
    lines.append("")
    lines.append(f"- **Final Result & Interpretation:** `{calc['final_value']}` — {problem_spec.get('interpretation') or 'Evaluated from the declared inputs under the stated assumptions.'}")
    if problem_spec.get("verification_note"):
        lines.append(f"- **Sanity Verification:** {problem_spec['verification_note']}")
    if problem_spec.get("common_mistakes"):
        mistakes = "; ".join(problem_spec["common_mistakes"]) if isinstance(problem_spec["common_mistakes"], list) else str(problem_spec["common_mistakes"])
        lines.append(f"- **Common Mistakes to Avoid:** {mistakes}")
    if problem_spec.get("generalization") and learner_level != "concise":
        lines.append(f"- **Generalization:** {problem_spec['generalization']}")

    return {
        "valid": True,
        "calculation": calc,
        "steps_covered": len(NUMERICAL_SOLUTION_STEPS),
        "markdown": "\n".join(lines).strip() + "\n",
    }


def validate_worked_solution(
    markdown: str,
    problem_spec: dict[str, Any] | None = None,
    *,
    learner_level: str = "beginner",
) -> dict[str, Any]:
    """Validate that a worked problem includes setup, assumptions, intermediate operations, result, and verification."""
    body = parse_note(markdown).body
    lowered = body.lower()
    errors: list[str] = []

    checks = [
        ("given_and_objective", r"\b(?:given|problem|find|objective|suppose)\b"),
        ("assumptions_or_method", r"\b(?:assum|condition|method|formula|since|because)\b"),
        ("intermediate_operations", r"(?:\n\s*\d+\.|\bstep\b|=.*=)"),
        ("interpretation", r"\b(?:interpret|means?|therefore|result|predict|answer)\b"),
        ("verification_or_check", r"\b(?:verify|verification|check|sanity|plausib|unit|dimension)\b"),
    ]
    for label, pattern in checks:
        if not re.search(pattern, lowered, re.S):
            errors.append(f"Worked solution missing {label.replace('_', ' ')}")

    if learner_level == "beginner" and not re.search(r"\b(?:mistake|trap|error|avoid|careful|confused)\b", lowered):
        errors.append("Beginner worked solution omits common mistake prevention")

    calc_result = None
    if problem_spec and problem_spec.get("steps"):
        calc_result = verify_worked_calculation(
            problem_spec["steps"],
            variables=problem_spec.get("given") if isinstance(problem_spec.get("given"), dict) else None,
            expected_result=problem_spec.get("expected_result"),
        )
        if not calc_result["valid"]:
            errors.extend(calc_result["errors"])
        elif calc_result["final_value"] is not None and str(calc_result["final_value"]) not in body and str(int(calc_result["final_value"]) if float(calc_result["final_value"]).is_integer() else calc_result["final_value"]) not in body:
            errors.append(f"Verified result '{calc_result['final_value']}' is absent from the written worked solution")

    return {"valid": not errors, "errors": errors, "calculation": calc_result}
