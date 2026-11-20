"""Scoped semantic checks for the shared KCP, not a general theorem prover.

Checks consume explicit authored contracts. Numerical counterexamples refute
claims; passing samples never establish a universally quantified proposition.
"""
from __future__ import annotations

import ast
from fractions import Fraction
import math
import re
from typing import Any


CLAIM_CLASSES = frozenset({"definition", "identity", "proved_proposition", "empirical_observation",
                          "reported_source_claim", "engineering_inference", "hypothesis", "speculation"})
EXAMPLE_CLASSES = frozenset({"conceptual_illustration", "synthetic_numerical", "deterministic_simulation",
                            "executable_demonstration", "model_backed_execution", "experimental_reproduction",
                            "source_reported_result"})
TRAINING_STAGES = frozenset({"input_preparation", "forward", "hidden_state_extraction", "labels",
                             "loss_terms", "reductions", "gradient_flow", "optimizer_update", "diagnostics", "tests"})


def arithmetic(expression: str, variables: dict[str, float]) -> float:
    # Reuse E5's safe AST evaluator; never eval code from a note or specification.
    from ..quality import safe_eval_expr
    if len(expression) > 2000 or len(list(ast.walk(ast.parse(expression, mode="eval")))) > 200:
        raise ValueError("Arithmetic expression exceeds the validation budget")
    for node in ast.walk(ast.parse(expression, mode="eval")):
        if isinstance(node, ast.Pow) or isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
            if isinstance(node, ast.BinOp) and (not isinstance(node.right, ast.Constant)
                                               or not isinstance(node.right.value, (int, float))
                                               or abs(node.right.value) > 32):
                raise ValueError("Exponent exceeds the validation budget")
    value = safe_eval_expr(expression, variables)
    if not math.isfinite(value):
        raise ValueError("Nonfinite arithmetic result")
    return value


def _polynomial(expression: str) -> dict[tuple[str, ...], Fraction]:
    """Exact rational polynomial normalization, deliberately excludes division by variables."""
    def add(a, b):
        out = dict(a)
        for key, value in b.items():
            out[key] = out.get(key, Fraction(0)) + value
        return {k: v for k, v in out.items() if v}

    def multiply(a, b):
        if len(a) * len(b) > 4096:
            raise ValueError("Polynomial expansion budget exceeded")
        out = {}
        for ka, va in a.items():
            for kb, vb in b.items():
                key = tuple(sorted(ka + kb))
                out[key] = out.get(key, Fraction(0)) + va * vb
        return {k: v for k, v in out.items() if v}

    def walk(node):
        if isinstance(node, ast.Constant) and type(node.value) in {int, float}:
            return {(): Fraction(str(node.value))}
        if isinstance(node, ast.Name):
            return {(node.id,): Fraction(1)}
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            return {k: (-v if isinstance(node.op, ast.USub) else v) for k, v in walk(node.operand).items()}
        if isinstance(node, ast.BinOp):
            left = walk(node.left)
            if isinstance(node.op, ast.Pow):
                if not isinstance(node.right, ast.Constant) or type(node.right.value) is not int or not 0 <= node.right.value <= 12:
                    raise ValueError("Only bounded nonnegative integer powers are supported")
                out = {(): Fraction(1)}
                for _ in range(node.right.value):
                    out = multiply(out, left)
                return out
            right = walk(node.right)
            if isinstance(node.op, ast.Add):
                return add(left, right)
            if isinstance(node.op, ast.Sub):
                return add(left, {k: -v for k, v in right.items()})
            if isinstance(node.op, ast.Mult):
                return multiply(left, right)
            if isinstance(node.op, ast.Div) and set(right) == {()} and right[()]:
                return {k: v / right[()] for k, v in left.items()}
        raise ValueError("Expression is outside the exact polynomial verifier domain")

    if len(expression) > 2000:
        raise ValueError("Polynomial expression too large")
    return {k: v for k, v in walk(ast.parse(expression, mode="eval").body).items() if v}


def check_proof(proof: dict[str, Any]) -> list[str]:
    errors = []
    for field in ("claim", "assumptions", "domain", "steps", "scope", "approximations", "boundary_conditions"):
        if field not in proof or field not in {"approximations"} and not proof[field]:
            errors.append(f"proof missing {field}")
    if set(proof.get("conclusion_assumptions", [])) - set(proof.get("assumptions", [])):
        errors.append("theorem conclusion requires unstated assumptions")
    if proof.get("scope") == "finite_update" and proof.get("justification_scope") == "first_order":
        errors.append("first-order geometry cannot prove finite-step preservation")
    for step in proof.get("steps", []):
        if not isinstance(step, dict) or not all(step.get(k) for k in ("lhs", "rhs", "reason", "relation")):
            errors.append("proof step needs two sides, a relation and a reason")
            continue
        if step["relation"] == "identity":
            try:
                if _polynomial(step["lhs"]) != _polynomial(step["rhs"]):
                    errors.append("exact algebraic identity fails")
            except (ValueError, SyntaxError, ArithmeticError) as exc:
                errors.append(f"identity requires another verifier: {exc}")
        elif step["relation"] in {"approximation", "implication"}:
            if not step.get("assumptions") or not step.get("justification"):
                errors.append("nonidentity step requires assumptions and explicit justification")
        else:
            errors.append("unknown proof-step relation")
    for check in proof.get("checks", []):
        errors.extend(check_numerical(check))
    if proof.get("verification") == "numerical_samples" and proof.get("universal", True):
        errors.append("numerical samples are not a universal proof")
    return errors


def check_numerical(check: dict[str, Any]) -> list[str]:
    errors = []
    try:
        atol, rtol = float(check.get("atol", 1e-12)), float(check.get("rtol", 1e-9))
        if not all(math.isfinite(t) and t >= 0 for t in (atol, rtol)):
            raise ValueError("Invalid comparison tolerance")
        actual = arithmetic(check["expression"], check.get("variables", {}))
        expected = float(check["expected"])
        if not math.isfinite(expected):
            raise ValueError("Nonfinite expected result")
        mode = check.get("comparison", "allclose")
        if mode not in {"exact", "allclose"}:
            raise ValueError("Unsupported equality convention")
        if not (actual == expected if mode == "exact" else math.isclose(actual, expected, rel_tol=rtol, abs_tol=atol)):
            errors.append(f"counterexample: observed {actual}, expected {expected}")
        if check.get("epsilon", 0) and not check.get("stabilizer_effect"):
            errors.append("stabilizer changes near-singular behavior; explain its effect")
    except (ValueError, KeyError, TypeError, ArithmeticError, SyntaxError) as exc:
        errors.append(f"numerical check failed: {exc}")
    return errors


def attention_mask(segments: list[dict[str, Any]], permissions: dict[str, list[str]], *, causal: bool) -> list[list[bool]]:
    """Rows are queries; columns are keys. Zero-length segments are valid."""
    names = [s["id"] for s in segments]
    if len(set(names)) != len(names) or any(type(s["length"]) is not int or s["length"] < 0 for s in segments):
        raise ValueError("Invalid attention segments")
    if set(permissions) != set(names) or any(set(v) - set(names) for v in permissions.values()):
        raise ValueError("Attention permissions reference unknown segments")
    tokens = [s["id"] for s in segments for _ in range(s["length"])]
    return [[key in permissions[query] and (not causal or j <= i) for j, key in enumerate(tokens)]
            for i, query in enumerate(tokens)]


def check_flow(flow: dict[str, Any]) -> list[str]:
    errors, known, provenance = [], set(flow.get("external_inputs", [])), {}
    for branch in flow.get("branches", []):
        required_fields = ("id", "inputs", "outputs", "accessible", "forbidden", "requires", "labels",
                           "readout", "shared_parameters", "gradient_owner", "attention_permissions")
        if any(k not in branch for k in required_fields):
            errors.append("information-flow branch is missing its access, label, readout or gradient contract")
            continue
        inputs, allowed = set(branch["inputs"]), set(branch["accessible"])
        reachable = set(inputs)
        for name in inputs:
            reachable.update(provenance.get(name, set()))
        if inputs - known or set(branch["requires"]) - allowed or set(branch["requires"]) - reachable:
            errors.append(f"branch {branch['id']} cannot access required information")
        if reachable.intersection(branch["forbidden"]) or set(branch["attention_permissions"]) - allowed:
            errors.append(f"branch {branch['id']} accesses forbidden information")
        if allowed - reachable:
            errors.append(f"branch {branch['id']} claims access without an input path")
        for output in branch["outputs"]:
            if output in known:
                errors.append(f"multiply owned flow output: {output}")
            known.add(output)
            provenance[output] = reachable
    if not flow.get("branches"):
        errors.append("information flow needs branches")
    if "mask" in flow:
        try:
            mask = flow["mask"]
            observed = attention_mask(mask["segments"], mask["permissions"], causal=mask["causal"])
            if "expected" in mask and observed != mask["expected"]:
                errors.append("mask disagrees with actual query/key permissions")
            for position in mask.get("readout_indices", []):
                if type(position) is not int or not 0 <= position < len(observed):
                    errors.append("readout index outside the attention context")
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f"invalid attention mask: {exc}")
    return errors


def check_tensor(tensor: dict[str, Any]) -> list[str]:
    fields = ("name", "shape", "dtype", "role", "valid_range", "gradient_owner", "indexing", "padding",
              "boundaries", "tokenizer", "label_shift", "readout")
    errors = [f"tensor missing {f}" for f in fields if f not in tensor]
    if errors:
        return errors
    dimensions = tensor.get("dimensions", {})
    shape = [dimensions.get(v, v) if isinstance(v, str) else v for v in tensor["shape"]]
    if any(type(v) is not int or v < 0 for v in shape):
        errors.append("tensor shape must resolve to nonnegative integer dimensions")
        return errors
    if tensor["indexing"] not in {"zero_based", "one_based"}:
        errors.append("unknown tensor indexing convention")
    if tensor.get("readout") is not None:
        readout = tensor["readout"]
        try:
            size = shape[readout["axis"]]
            offset = 0 if tensor["indexing"] == "zero_based" else 1
            if not offset <= readout["position"] < size + offset:
                errors.append("tensor readout outside its axis, including empty token axes")
        except (KeyError, TypeError, IndexError):
            errors.append("invalid tensor readout contract")
    if tensor.get("schematic_tokens") and tensor["tokenizer"] != "schematic" and not tensor.get("tokenization_evidence"):
        errors.append("schematic tokens cannot assert real tokenizer boundaries")
    return errors


def check_execution(record: dict[str, Any], *, minimum: str = "executed") -> list[str]:
    levels = ["written", "syntax_checked", "executed", "unit_tested", "model_inference", "training", "reproduced"]
    if record.get("level") not in levels or levels.index(record["level"]) < levels.index(minimum):
        return [f"execution evidence does not establish {minimum}"]
    fields = ("command", "code_hash", "runtime", "dependencies", "inputs", "stdout", "limitations", "hardware", "seed")
    return [f"execution evidence missing {f}" for f in fields if f not in record]


def check_execution_artifact(record: dict[str, Any], body: str) -> list[str]:
    from scriptorium.models import content_hash
    code = record.get("code", "")
    errors = []
    if not code or code not in body or content_hash(code) != record.get("code_hash"):
        errors.append("execution evidence does not bind the actual displayed code")
    if record.get("stdout") and str(record["stdout"]).strip() not in body:
        errors.append("observed execution output is missing from the chapter")
    return errors


def check_example(example: dict[str, Any]) -> list[str]:
    kind = example.get("kind")
    if kind not in EXAMPLE_CLASSES:
        return ["unknown example authenticity classification"]
    errors = []
    if kind in {"model_backed_execution", "experimental_reproduction"} and example.get("state_origin") != "model_execution":
        errors.append("hand-specified vectors are not executed model states")
    minimum = {"deterministic_simulation": "executed", "executable_demonstration": "executed",
               "model_backed_execution": "model_inference", "experimental_reproduction": "reproduced"}.get(kind)
    if minimum:
        errors.extend(check_execution(example.get("execution", {}), minimum=minimum))
    if kind in {"model_backed_execution", "experimental_reproduction"}:
        for field in ("model_revision", "tokenizer_revision", "attention_backend"):
            if not example.get("execution", {}).get(field):
                errors.append(f"model execution missing {field}")
    return errors


def check_implementation(implementation: dict[str, Any], body: str) -> list[str]:
    errors = []
    level = implementation.get("level")
    if level not in {"component_snippet", "illustrative_demonstration", "end_to_end", "reproducible_experiment", "production_system"}:
        errors.append("unknown implementation-path level")
    if implementation.get("claims_full_training_step"):
        if level not in {"end_to_end", "reproducible_experiment", "production_system"}:
            errors.append("a complete training step requires end-to-end implementation scope")
        stages = implementation.get("stages", {})
        if TRAINING_STAGES - set(stages):
            errors.append("component snippet does not implement a complete training step")
        for name, code in stages.items():
            if not code or code not in body:
                errors.append(f"training stage {name} has no code in the chapter")
        errors.extend(check_execution(implementation.get("execution", {}), minimum="training"))
    if level in {"end_to_end", "reproducible_experiment", "production_system"}:
        if not implementation.get("backend") or not implementation.get("assumptions"):
            errors.append("complete implementation needs backend and model assumptions")
        errors.extend(check_execution(implementation.get("execution", {}), minimum="executed"))
        errors.extend(check_execution_artifact(implementation.get("execution", {}), body))
    return errors


def check_claim(claim: dict[str, Any], *, source_policy: str) -> list[str]:
    errors = []
    classification = claim.get("classification")
    if not claim.get("text") or classification not in CLAIM_CLASSES:
        errors.append("claim needs exact text and a calibrated classification")
    if re.search(r"\b(always|never|guarantees?|proves?|solves?)\b", claim.get("text", ""), re.I):
        if not claim.get("scope_review") or not claim.get("limits"):
            errors.append("strong claim wording requires evidence-scope review")
    if claim.get("origin") not in {"reported", "derived", "reproduced", "inferred", "hypothetical", "unverified"}:
        errors.append("claim needs provenance status")
    if claim.get("origin") == "unverified":
        errors.append("consequential claim remains unverified")
    if classification in {"reported_source_claim", "empirical_observation"} or claim.get("origin") == "reported":
        source = claim.get("source", {})
        if not isinstance(source, dict):
            return errors + ["claim source must be a versioned evidence object"]
        for field in ("id", "version", "location", "verification_method", "status", "limits", "snapshot", "excerpt"):
            if not source.get(field):
                errors.append(f"claim provenance missing {field}")
        if source.get("status") != "verified":
            errors.append("claim source remains unverified")
        if source_policy == "strict" and source.get("origin") != "supplied":
            errors.append("source-only policy rejects external claim evidence")
    if classification == "empirical_observation":
        empirical = claim.get("empirical", {})
        if not isinstance(empirical, dict) or not isinstance(empirical.get("uncertainty", {}), dict):
            return errors + ["empirical uncertainty must identify its type and observed context"]
        for field in ("dataset", "model", "adaptation", "metric", "protocol", "hyperparameters", "model_selection",
                      "runs", "uncertainty", "compute", "location", "value", "units"):
            if field not in empirical:
                errors.append(f"empirical result missing {field}")
        if empirical.get("uncertainty", {}).get("type") not in {"SD", "SE", "CI", "not_reported"}:
            errors.append("uncertainty must distinguish SD, SE, CI, and not reported")
        uncertainty = empirical.get("uncertainty", {})
        if uncertainty.get("type") in {"SD", "SE", "CI"}:
            if not isinstance(empirical.get("runs"), int) or empirical["runs"] < 2:
                errors.append("reported repeated-run uncertainty requires an actual run count")
            if not isinstance(uncertainty.get("value"), (int, float)) or uncertainty["value"] < 0:
                errors.append("reported uncertainty requires its nonnegative measured value")
        if uncertainty.get("type") == "CI" and not 0 < uncertainty.get("level", 0) < 1:
            errors.append("confidence interval needs its confidence level")
        if empirical.get("comparison") and empirical.get("change_unit") not in {"percentage_points", "relative_percent", "absolute"}:
            errors.append("metric change needs an explicit percent convention")
    return errors


def check_failure(failure: dict[str, Any]) -> list[str]:
    fields = ("symptom", "latent_property", "candidate_cause", "diagnostic", "measurement", "evidence_status", "remediation")
    errors = [f"failure diagnosis missing {f}" for f in fields if not failure.get(f)]
    if failure.get("cause_established") and failure.get("evidence_status") != "controlled_measurement":
        errors.append("a symptom alone cannot establish a cause")
    if failure.get("family") == "representation" and failure.get("latent_property") not in {
        "hidden_state_collapse", "selected_embedding_collapse", "directional_collapse", "dimensional_collapse", "generation_failure"}:
        errors.append("representation failure needs a specific latent property")
    return errors


def representation_metrics(states: list[list[float]]) -> dict[str, Any]:
    """Operational variability and participation ratio; no causal or intrinsic-rank claim."""
    if len(states) < 2 or not states[0] or any(len(r) != len(states[0]) for r in states):
        raise ValueError("Diagnostics require at least two equal-width observations")
    if any(not math.isfinite(x) for row in states for x in row):
        raise ValueError("Nonfinite representation measurement")
    if len(states) > 64 or len(states[0]) > 512:
        raise ValueError("Use a scientific backend for diagnostics exceeding the small-matrix verifier budget")
    mean = [sum(col) / len(states) for col in zip(*states)]
    centered = [[x - m for x, m in zip(row, mean)] for row in states]
    gram = [[sum(x*y for x, y in zip(a, b)) for b in centered] for a in centered]
    trace = sum(gram[i][i] for i in range(len(gram)))
    squares = sum(x*x for row in gram for x in row)
    if not math.isfinite(trace) or not math.isfinite(squares):
        raise ValueError("Representation measurement overflow; rescale observations or use a scientific backend")
    # Symmetric Jacobi rotations compute the finite sample singular spectrum.
    eigen = [list(row) for row in gram]
    for _ in range(50 * len(states)**2):
        p, q = max(((i, j) for i in range(len(eigen)) for j in range(i+1, len(eigen))), key=lambda ij: abs(eigen[ij[0]][ij[1]]))
        if abs(eigen[p][q]) <= 1e-12 * max(1., trace):
            break
        theta = 0.5 * math.atan2(2*eigen[p][q], eigen[q][q]-eigen[p][p])
        c, s = math.cos(theta), math.sin(theta)
        app, aqq, apq = eigen[p][p], eigen[q][q], eigen[p][q]
        for i in range(len(eigen)):
            if i not in {p, q}:
                aip, aiq = eigen[i][p], eigen[i][q]
                eigen[i][p] = eigen[p][i] = c*aip-s*aiq
                eigen[i][q] = eigen[q][i] = s*aip+c*aiq
        eigen[p][p] = c*c*app-2*s*c*apq+s*s*aqq
        eigen[q][q] = s*s*app+2*s*c*apq+c*c*aqq
        eigen[p][q] = eigen[q][p] = 0.
    values = sorted((max(0., eigen[i][i]) for i in range(len(eigen))), reverse=True)
    probabilities = [v / trace for v in values if v > 0 and v / trace > 0] if trace else []
    return {"norms": [math.sqrt(sum(x*x for x in row)) for row in states],
            "between_example_variance": trace / len(states),
            "participation_ratio": trace*trace / squares if squares else 0.0,
            "singular_spectrum": [math.sqrt(v) for v in values],
            "effective_dimension": math.exp(-sum(p*math.log(p) for p in probabilities)) if probabilities else 0.,
            "scope": "finite centered observations; a singular spectrum or effective dimension does not establish causal utility"}


def heldout_linear_probe(train: list[list[float]], targets: list[float], test: list[list[float]], labels: list[float], *, ridge: float = 1e-6) -> dict:
    """Small deterministic ridge regression with an explicit held-out split; no causal claim."""
    if not train or not test or len(train) != len(targets) or len(test) != len(labels) or not math.isfinite(ridge) or ridge <= 0:
        raise ValueError("Linear probe needs training and held-out observations and positive regularization")
    width = len(train[0])
    if not width or width > 64 or any(len(row) != width for row in train+test):
        raise ValueError("Invalid small linear-probe dimensions")
    if any(not math.isfinite(v) for row in train+test for v in row) or any(not math.isfinite(v) for v in targets+labels):
        raise ValueError("Nonfinite linear-probe input")
    matrix = [[sum(row[i]*row[j] for row in train) + (ridge if i == j else 0.) for j in range(width)]
              + [sum(row[i]*y for row, y in zip(train, targets))] for i in range(width)]
    for i in range(width):
        pivot = max(range(i, width), key=lambda j: abs(matrix[j][i]))
        matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
        divisor = matrix[i][i]
        if abs(divisor) < 1e-15:
            raise ValueError("Ill-conditioned linear probe; rescale or use a scientific backend")
        matrix[i] = [v/divisor for v in matrix[i]]
        for j in range(width):
            if i != j:
                factor = matrix[j][i]
                matrix[j] = [v-factor*w for v, w in zip(matrix[j], matrix[i])]
    weights = [row[-1] for row in matrix]
    predicted = [sum(x*w for x, w in zip(row, weights)) for row in test]
    mse = sum((a-b)**2 for a, b in zip(predicted, labels)) / len(labels)
    return {"heldout_mse": mse, "weights": weights, "predictions": predicted, "train_observations": len(train),
            "heldout_observations": len(test), "limits": "Supplied split and targets; predictive association is not causal usefulness."}


def check_diagnostics(record: dict[str, Any]) -> list[str]:
    errors = []
    if not all(record.get(k) for k in ("measurement", "controls", "evidence", "limits")):
        errors.append("latent-structure claim needs operational measurement, controls, evidence and limits")
    if record.get("conclusion") in {"intrinsic_rank", "causal_usefulness"} and record.get("measurement") == "2d_projection":
        errors.append("a 2D projection cannot establish intrinsic rank or causal usefulness")
    if "states" in record:
        try:
            measured = representation_metrics(record["states"])
            for key, expected in record.get("expected", {}).items():
                actual = measured.get(key)
                matches = (isinstance(expected, list) and len(actual) == len(expected)
                           and all(math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12) for a, b in zip(actual, expected))) if isinstance(actual, list) else (
                               actual is not None and math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-12))
                if not matches:
                    errors.append(f"representation diagnostic disagrees with computed {key}")
        except (ValueError, TypeError) as exc:
            errors.append(str(exc))
    if "linear_probe" in record:
        try:
            measured = heldout_linear_probe(**record["linear_probe"])
            if "expected_mse" in record and not math.isclose(record["expected_mse"], measured["heldout_mse"], rel_tol=1e-6, abs_tol=1e-10):
                errors.append("held-out linear-predictability measurement disagrees with its observations")
        except (ValueError, TypeError) as exc:
            errors.append(str(exc))
    return errors


def check_cost(record: dict[str, Any]) -> list[str]:
    fields = ("dense_tensor_size", "operations", "activation_memory", "backward_cost", "padding", "kernel", "hardware", "protocol", "kind")
    errors = [f"resource analysis missing {f}" for f in fields if f not in record]
    if record.get("kind") not in {"theoretical_estimate", "measured_benchmark"}:
        errors.append("resource analysis must distinguish estimates from benchmarks")
    if record.get("kind") == "measured_benchmark":
        errors.extend(check_execution(record.get("execution", {})))
    if record.get("comparison") and record.get("protocol") not in {"equal_epochs", "equal_compute"}:
        errors.append("cost comparison needs equal-epochs or equal-compute protocol")
    return errors
