"""Dedicated Mathematical Deconstruction (M01-M14) & Numerical Problem-Solving Engine (Step 1-12).

Owned cleanly by A2 (Tutor) and verified by A9 (Checker). Never stores hardcoded
subject-specific lessons; inspects arbitrary mathematical expressions, matrix/vector
shapes, symbolic notation, worked arithmetic, and Markdown explanations structurally.
"""
from __future__ import annotations

import math
import re
from typing import Any

from scriptorium.models import (
    FormulaTeachingRecord,
    content_hash,
    parse_note,
    scan_display_math_blocks,
)

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


GENERIC_FOLD_PHRASES: tuple[str, ...] = (
    "substitute the values",
    "this computes the result",
    "plug in the numbers",
    "plug in the values",
    "compute the final value",
    "this formula gives the result",
)


def _format_callout_block(
    lines: list[str],
    *,
    title: str = "📐 Understand this formula",
    callout_type: str = "note",
    quote_prefix: str = "",
) -> list[str]:
    """Wrap explanatory lines inside an Obsidian-native collapsed callout block."""
    out = [f"{quote_prefix}> [!{callout_type}]- {title}"]
    for ln in lines:
        if not ln.strip():
            out.append(f"{quote_prefix}>")
        else:
            # Guard against recursive display $$ inside the formula fold itself.
            cleaned_ln = ln.replace("$$", "$") if "$$" in ln else ln
            out.append(f"{quote_prefix}> {cleaned_ln}")
    return out


def render_formula_component(
    spec: dict[str, Any] | FormulaTeachingRecord,
    *,
    learner_level: str = "beginner",
    quote_prefix: str = "",
) -> dict[str, Any]:
    """Single owned renderer binding one display formula with its immediate folded explanation."""
    if isinstance(spec, FormulaTeachingRecord):
        data: dict[str, Any] = {
            "formula_id": spec.formula_id,
            "equation": spec.expression,
            "concept_owner": spec.concept_owner,
            "purpose": spec.purpose,
            "pronunciation": spec.plain_reading,
            "symbols": spec.symbols,
            "shapes_units_domains": spec.shapes_units_domains,
            "operation_breakdown": spec.operation_sequence,
            "derivation_reasoning": spec.derivation_reasoning,
            "numerical_example": spec.numerical_example,
            "interpretation": spec.interpretation,
            "assumptions": spec.assumptions,
            "misconceptions": spec.misconceptions,
            "placement": spec.placement,
        }
    else:
        data = dict(spec)

    eq = str(data.get("equation") or "").strip()
    if not eq:
        raise ValueError("Formula component requires a non-empty 'equation' string")

    features = detect_equation_features(eq, learner_level=learner_level)
    active = features["active_obligations"]

    symbols = list(data.get("symbols") or [])
    for sym in symbols:
        if not sym.get("symbol") or not sym.get("meaning"):
            raise ValueError("Each symbol entry requires non-empty 'symbol' and 'meaning'")
        otype = sym.get("type")
        if otype and otype not in MATHEMATICAL_OBJECT_TYPES:
            raise ValueError(f"Unknown mathematical object type: {otype}")

    dim_check: dict[str, Any] | None = None
    if data.get("dimension_operands"):
        dim_check = check_dimension_compatibility(
            data["dimension_operands"],
            operation=str(data.get("dimension_operation") or "matmul"),
        )
        if not dim_check["valid"]:
            raise ValueError(dim_check["error"])

    calc_check: dict[str, Any] | None = None
    num_ex = data.get("numerical_example")
    if isinstance(num_ex, dict) and num_ex.get("steps"):
        calc_check = verify_worked_calculation(
            num_ex["steps"],
            variables=num_ex.get("inputs"),
            expected_result=num_ex.get("expected_result"),
        )
        if not calc_check["valid"]:
            raise ValueError(f"Worked numerical substitution failed verification: {calc_check['errors']}")

    purpose_text = str(data.get("purpose") or "").strip()
    pron_text = str(data.get("pronunciation") or "").strip()
    prereq_text = str(data.get("prerequisites") or "").strip()
    vis_text = str(data.get("visual_interpretation") or "").strip()
    param_text = str(data.get("parameter_behavior") or "").strip()
    py_impl = str(data.get("python_implementation") or "").strip()
    recall_qs = [str(q).strip() for q in (data.get("recall_questions") or []) if str(q).strip()]

    fold_inner: list[str] = []

    def _add_stage(heading: str, stage_lines: list[str]) -> None:
        if not stage_lines:
            return
        if fold_inner:
            fold_inner.append("")
        fold_inner.append(f"### {heading}")
        fold_inner.extend(stage_lines)

    # Stage 1: Formula Introduction and Intuition
    if purpose_text:
        _add_stage("1. Why this formula exists", [purpose_text])

    # Stage 2: Formula Decomposition
    if data.get("operation_breakdown"):
        comp_lines = [f"{idx}. {step_text}" for idx, step_text in enumerate(data["operation_breakdown"], 1)]
        _add_stage("2. Formula components", comp_lines)

    # Stage 3: Symbol-by-Symbol Decoding
    sym_lines: list[str] = []
    if symbols:
        sym_lines.extend(["| Symbol | Name / Meaning | Type | Shape / Units | Role |", "|---|---|---|---|---|"])
        for s in symbols:
            sym_lines.append(
                f"| ${s['symbol']}$ | {s['meaning']} | {s.get('type', 'quantity')} | "
                f"{s.get('shape') or s.get('units') or 'scalar'} | {s.get('role', s['meaning'])} |"
            )
    if data.get("shapes_units_domains"):
        if sym_lines:
            sym_lines.append("")
        sym_lines.append("**Shapes, units, and domains:** " + "; ".join(str(x) for x in data["shapes_units_domains"]))
    if dim_check:
        sym_lines.append(f"**Shape compatibility:** `{dim_check.get('compatibility_summary') or dim_check.get('output_shape')}`.")
    _add_stage("3. Symbol-by-symbol breakdown", sym_lines)

    # Stage 4: Mathematical Pronunciation
    if pron_text:
        _add_stage("4. How to read it", [pron_text])

    # Stage 5: Prerequisite Mathematics
    if prereq_text:
        _add_stage("5. Prerequisites", [prereq_text])

    # Stage 6: Complete Numerical Example
    if isinstance(num_ex, dict) and (calc_check or num_ex.get("summary")):
        num_lines: list[str] = []
        if num_ex.get("inputs"):
            formatted_inputs = ", ".join(f"`{k} = {v}`" for k, v in num_ex["inputs"].items())
            num_lines.append(f"- **Declared inputs:** {formatted_inputs}")
        if calc_check:
            for st in calc_check["evaluated_steps"]:
                expl = f" — {st['explanation']}" if st.get("explanation") else ""
                num_lines.append(f"- **{st['label']}:** `{st['expr']}` = `{st['computed']}`{expl}")
        elif num_ex.get("summary"):
            num_lines.append(f"- **Trace:** {num_ex['summary']}")
        if num_ex.get("interpretation"):
            num_lines.append(f"- **Result meaning:** {num_ex['interpretation']}")
        if num_ex.get("sanity_check"):
            num_lines.append(f"- **Sanity check:** {num_ex['sanity_check']}")
        _add_stage("6. Numerical example", num_lines)

    # Stage 7: Visual and Geometric Intuition
    if vis_text:
        _add_stage("7. Visual interpretation", vis_text.splitlines())

    # Stage 8: Parameter Experimentation
    if param_text:
        _add_stage("8. Parameter behavior", param_text.splitlines())

    # Stage 9: Mathematical Derivation
    deriv_lines: list[str] = []
    if data.get("expanded_form"):
        exp_clean = str(data["expanded_form"]).strip().replace("\n", " ")
        deriv_lines.append(f"**Expanded elementary form:** ${exp_clean}$")
    if data.get("derivation_reasoning"):
        if deriv_lines:
            deriv_lines.append("")
        deriv_lines.append(str(data["derivation_reasoning"]).strip())
    _add_stage("9. Derivation", deriv_lines)

    # Stage 10: Python Implementation
    if py_impl:
        if "```" in py_impl:
            _add_stage("10. Python implementation", py_impl.splitlines())
        else:
            _add_stage("10. Python implementation", ["```python", *py_impl.splitlines(), "```"])

    # Stage 11: Applications, Limitations, and Misconceptions
    lim_lines: list[str] = []
    if data.get("assumptions"):
        lim_lines.append("**Assumptions & conditions:** " + "; ".join(str(x) for x in data["assumptions"]))
    if data.get("misconceptions"):
        if lim_lines:
            lim_lines.append("")
        lim_lines.append("**Common mistakes to avoid:**")
        lim_lines.extend(f"- {mc}" for mc in data["misconceptions"])
    _add_stage("11. Limitations and mistakes", lim_lines)

    # Stage 12: Mental Model and Active Recall
    mental_lines: list[str] = []
    interp_text = str((num_ex or {}).get("interpretation") if isinstance(num_ex, dict) else "" or data.get("interpretation") or "").strip()
    if data.get("interpretation") and str(data["interpretation"]).strip() != interp_text:
        mental_lines.append(f"**Mental model:** {str(data['interpretation']).strip()}")
    elif interp_text and not (isinstance(num_ex, dict) and (calc_check or num_ex.get("summary"))):
        mental_lines.append(f"**Mental model:** {interp_text}")
    if data.get("generalization"):
        mental_lines.append(f"**Generalization:** {str(data['generalization']).strip()}")
    if recall_qs:
        mental_lines.append("**Quick recall checks:**")
        mental_lines.extend(f"- {q}" for q in recall_qs)
    _add_stage("12. Mental model and recall", mental_lines)

    while fold_inner and not fold_inner[-1].strip():
        fold_inner.pop()
    if not fold_inner:
        raise ValueError("Formula teaching component cannot render an empty explanation fold")

    fold_lines = _format_callout_block(fold_inner, title="📐 Understand this formula", callout_type="note", quote_prefix=quote_prefix)
    display_lines = [f"{quote_prefix}$$", f"{quote_prefix}{eq}", f"{quote_prefix}$$"]
    pre_prose = ([f"{quote_prefix}{purpose_text}", quote_prefix.rstrip() if quote_prefix else ""] if purpose_text and not quote_prefix else [])
    if purpose_text and quote_prefix:
        pre_prose = [f"{quote_prefix}{purpose_text}", quote_prefix.rstrip()]

    all_lines = [*pre_prose, *display_lines, quote_prefix.rstrip() if quote_prefix else "", *fold_lines]
    formula_id = str(data.get("formula_id") or f"eq-{content_hash(eq)[:10]}")
    record = FormulaTeachingRecord(
        formula_id=formula_id,
        expression=eq,
        concept_owner=str(data.get("concept_owner") or ""),
        purpose=purpose_text,
        plain_reading=pron_text,
        symbols=symbols,
        shapes_units_domains=list(data.get("shapes_units_domains") or ([dim_check.get("compatibility_summary")] if dim_check else [])),
        operation_sequence=list(data.get("operation_breakdown") or []),
        prerequisites=prereq_text,
        derivation_reasoning=str(data.get("derivation_reasoning") or ""),
        numerical_example=dict(num_ex) if isinstance(num_ex, dict) else {},
        visual_interpretation=vis_text,
        parameter_behavior=param_text,
        python_implementation=py_impl,
        interpretation=str((num_ex or {}).get("interpretation") or data.get("interpretation") or ""),
        assumptions=list(data.get("assumptions") or []),
        misconceptions=list(data.get("misconceptions") or []),
        recall_questions=recall_qs,
        validation_status="verified",
        placement=str(data.get("placement") or "prose"),
    )

    return {
        "formula_id": formula_id,
        "equation": eq,
        "complexity": features["complexity"],
        "active_obligations": active,
        "dimension_check": dim_check,
        "calculation_check": calc_check,
        "record": record,
        "display_block": "\n".join(display_lines),
        "folded_callout": "\n".join(fold_lines),
        "markdown": "\n".join(all_lines).strip() + "\n",
    }


def deconstruct_equation(spec: dict[str, Any], *, learner_level: str = "beginner") -> dict[str, Any]:
    """Produce a domain-independent M01-M14 structured breakdown with bound Obsidian formula fold."""
    if not isinstance(spec, dict) or not str(spec.get("equation") or "").strip():
        raise ValueError("Equation specification requires a non-empty 'equation' string")

    component = render_formula_component(spec, learner_level=learner_level)
    return {
        "formula_id": component["formula_id"],
        "equation": component["equation"],
        "complexity": component["complexity"],
        "active_obligations": component["active_obligations"],
        "dimension_check": component["dimension_check"],
        "calculation_check": component["calculation_check"],
        "record": component["record"],
        "folded_callout": component["folded_callout"],
        "markdown": component["markdown"],
    }


def validate_formula_folds(
    note_text: str,
    *,
    learner_level: str = "beginner",
) -> dict[str, Any]:
    """Validate that every displayed $$...$$ block owns an adequate non-nested folded explanation."""
    blocks = scan_display_math_blocks(note_text)
    issues: list[dict[str, Any]] = []
    block_reports: list[dict[str, Any]] = []

    def _add(code: str, severity: str, description: str, line: int) -> None:
        issues.append({"code": code, "severity": severity, "description": description, "location": f"line_{line}"})

    for blk in blocks:
        blk_errors: list[str] = []
        if blk.nested_inside_formula_fold:
            msg = f"Display formula on line {blk.start_line} is recursively nested inside a formula explanation fold; keep fold arithmetic inline or use a sibling formula block."
            _add("FORMULA-FOLD-NESTED", "critical", msg, blk.start_line)
            blk_errors.append(msg)

        # Guard against bundling unrelated equations inside a single display block
        expr_clean = re.sub(r"\\begin\{(?:bmatrix|pmatrix|vmatrix|cases)\}[\s\S]*?\\end\{(?:bmatrix|pmatrix|vmatrix|cases)\}", " ", blk.expression)
        non_empty_rows = [r.strip() for r in re.split(r"\\\\|\n", expr_clean) if r.strip() and r.strip() not in {r"\begin{aligned}", r"\end{aligned}"}]
        if len(non_empty_rows) >= 3 and "=" in expr_clean:
            unlinked = [r for r in non_empty_rows[1:] if not r.lstrip("& ").startswith(("=", r"\approx", r"\implies", r"\iff", r"\le", r"\ge", "<", ">"))]
            if len(unlinked) >= 2 and "cases" not in blk.expression:
                msg = f"Display block on line {blk.start_line} bundles {len(unlinked) + 1} separate equations; split them so each formula receives its own folded explanation."
                _add("FORMULA-BUNDLED", "major", msg, blk.start_line)
                blk_errors.append(msg)

        if not blk.nested_inside_formula_fold:
            if not blk.has_following_fold:
                msg = f"Display formula on line {blk.start_line} lacks an immediately following collapsed '> [!example]-' explanation callout."
                _add("FORMULA-FOLD-MISSING", "critical", msg, blk.start_line)
                blk_errors.append(msg)
            else:
                fold_low = blk.fold_body.lower()
                fold_words = re.findall(r"\b\w+\b", blk.fold_body)
                # Detect generic boilerplate folds
                hit_generic = [p for p in GENERIC_FOLD_PHRASES if p in fold_low]
                if len(fold_words) < 20 or (hit_generic and len(fold_words) < 45):
                    msg = f"Formula explanation fold on line {blk.fold_start_line} uses sparse/generic filler ({hit_generic or f'{len(fold_words)} words'}) instead of real symbol and operation teaching."
                    _add("FORMULA-FOLD-GENERIC", "critical", msg, blk.fold_start_line or blk.start_line)
                    blk_errors.append(msg)

                # Verify that actual symbols from the equation appear explained in the fold or surrounding prose
                feat = detect_equation_features(blk.expression, learner_level=learner_level)
                req_syms = [s for s in feat["detected_symbols"] if len(s) >= 1 and s not in {"i", "j", "k", "n"}]
                if req_syms:
                    fold_norm = re.sub(r"\\(?:mathbf|boldsymbol|hat|bar|tilde|vec|text)\{([^}]+)\}", r"\1", blk.fold_body)
                    covered = sum(
                        1 for sym in req_syms
                        if sym in blk.fold_body
                        or re.sub(r"\\|\{|\}", "", sym) in fold_norm
                    )
                    if covered == 0 and len(req_syms) >= 2:
                        msg = f"Formula fold on line {blk.fold_start_line} does not resolve the equation's actual symbols ({', '.join(req_syms[:5])})."
                        _add("FORMULA-FOLD-SYMBOLS", "major", msg, blk.fold_start_line or blk.start_line)
                        blk_errors.append(msg)

                if "$$" in blk.fold_body:
                    msg = f"Formula fold on line {blk.fold_start_line} contains nested display math delimiters; use inline arithmetic instead."
                    _add("FORMULA-FOLD-NESTED-MATH", "critical", msg, blk.fold_start_line or blk.start_line)
                    blk_errors.append(msg)

        block_reports.append({
            "index": blk.index,
            "start_line": blk.start_line,
            "end_line": blk.end_line,
            "in_list": blk.in_list,
            "in_callout": blk.in_callout,
            "has_following_fold": blk.has_following_fold,
            "errors": blk_errors,
        })

    crit_or_major = [i for i in issues if i["severity"] in {"critical", "major"}]
    return {
        "passed": not crit_or_major,
        "display_count": len(blocks),
        "folded_count": sum(1 for b in blocks if b.has_following_fold),
        "issues": issues,
        "blocks": block_reports,
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

    # 2. Check consecutive equation dumping (ignoring code blocks & currency via scan_display_math_blocks)
    blocks = scan_display_math_blocks(note_text)
    body_lines = body.splitlines()
    for i in range(len(blocks) - 1):
        between_start = blocks[i].end_line
        between_end = blocks[i + 1].start_line - 1
        between_txt = "\n".join(note_text.splitlines()[between_start:between_end]).strip()
        prose_words = [w for w in between_txt.split() if not w.startswith(("#", "|", "$", "`", ">"))]
        if len(prose_words) < 6 and not between_txt.startswith("="):
            _issue("MATH-DECON-02", "major", "Back-to-back display equations appear without bridging interpretation or explanation between them.", "display_equations")
            break

    # 3. Inspect matrix/transpose/sum equations for beginner/intermediate scaffolding
    lowered = body.lower()
    for blk in blocks:
        feat = detect_equation_features(blk.expression, learner_level=level)
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
    if blocks and not defined and len(blocks) >= 2:
        _issue("MATH-DECON-05", "major", "Display equations appear with no identifiable symbol definitions or variable table in surrounding prose.", "symbol_inventory")

    # 5. Enforce immediate folded formula explanation contract across all display math blocks
    fold_audit = validate_formula_folds(note_text, learner_level=level)
    issues.extend(fold_audit["issues"])

    # 6. Deterministically verify supplied structured equation specs
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
        "display_equation_count": len(blocks),
        "folded_equation_count": fold_audit["folded_count"],
        "formula_folds": fold_audit,
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
    sym_defs = list(problem_spec.get("symbols") or [])
    if not sym_defs:
        # Derive honest minimal symbol entries from declared inputs + formula symbols
        given_dict = problem_spec.get("given") if isinstance(problem_spec.get("given"), dict) else {}
        sym_defs = [{"symbol": k, "meaning": f"input variable (example value {v})", "type": "scalar"} for k, v in given_dict.items()]
        if not sym_defs:
            sym_defs = [{"symbol": problem_spec.get("find", "result"), "meaning": "target quantity computed by the formula", "type": "scalar"}]

    assump_list = list(problem_spec["assumptions"]) if isinstance(problem_spec["assumptions"], list) else [str(problem_spec["assumptions"])]
    formula_component = render_formula_component(
        {
            "equation": str(problem_spec["formula"]).strip(),
            "purpose": f"Computes {problem_spec['find']} for {problem_spec['problem']}",
            "pronunciation": str(problem_spec.get("pronunciation") or f"Formula computing {problem_spec['find']}."),
            "symbols": sym_defs,
            "operation_breakdown": [
                f"{st['label']}: evaluate `{st['expr']}` -> `{st['computed']}`"
                + (f" ({st['explanation']})" if st.get("explanation") else "")
                for st in calc["evaluated_steps"]
            ],
            "interpretation": str(problem_spec.get("interpretation") or f"Evaluates to `{calc['final_value']}` under {given_str}."),
            "assumptions": assump_list,
            "misconceptions": list(problem_spec.get("common_mistakes") or ["Check variable signs, denominator constraints, and units before computing."])
            if not isinstance(problem_spec.get("common_mistakes"), str)
            else [problem_spec["common_mistakes"]],
            "placement": "worked_example",
        },
        learner_level=learner_level,
    )

    lines = [
        f"### Worked Problem: {problem_spec.get('title') or 'Step-by-Step Solution'}",
        "",
        f"- **Question & Objective:** {problem_spec['problem']} Find: {problem_spec['find']}",
        f"- **Given Inputs:** {given_str}",
        f"- **Method & Why It Applies:** {problem_spec.get('method_rationale') or problem_spec['formula']}",
        f"- **Required Assumptions:** {'; '.join(assump_list)}",
        "",
        formula_component["display_block"],
        "",
        formula_component["folded_callout"],
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
