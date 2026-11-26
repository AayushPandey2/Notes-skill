"""Run the trusted Logistic Regression golden lab blocks and verify YAML, links, and callouts."""

from contextlib import redirect_stdout
from hashlib import sha256
from io import StringIO
import json
import math
from pathlib import Path
import platform
import re
import yaml

import numpy as np
import sklearn

BUNDLE = Path(__file__).resolve().parent / "fixtures/bundles/logistic-regression"
LAB = BUNDLE / "logistic-regression-lab.md"
THEORY = BUNDLE / "logistic-regression.md"
MASTERY = BUNDLE / "logistic-regression-mastery.md"


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def parse_frontmatter(text, path):
    check(text.startswith("---\n"), f"{path}: missing opening YAML ---")
    end = text.find("\n---\n", 4)
    check(end != -1, f"{path}: missing closing YAML ---")
    meta = yaml.safe_load(text[4:end])
    check(isinstance(meta, dict), f"{path}: frontmatter did not parse to a mapping")
    for key in ("id", "aliases", "topic", "tags", "nexttopics"):
        check(key in meta, f"{path}: missing YAML key {key}")
    check(isinstance(meta["id"], str) and meta["id"], f"{path}: empty id")
    check(isinstance(meta["topic"], str) and meta["topic"], f"{path}: empty topic")
    check(isinstance(meta["aliases"], list), f"{path}: aliases must be a list")
    check(isinstance(meta["tags"], list), f"{path}: tags must be a list")
    check(isinstance(meta["nexttopics"], list), f"{path}: nexttopics must be a list")


def main():
    source = LAB.read_text()
    blocks = re.findall(r"(?ms)^```python\n(.*?)^```$", source)
    check(len(blocks) == 3, f"Expected 3 python blocks, found {len(blocks)}")
    namespace = {}
    captured = StringIO()
    with redirect_stdout(captured):
        for number, block in enumerate(blocks, start=1):
            exec(compile(block, f"{LAB.name}:track-{number}", "exec"), namespace)

    fit = namespace["fit_logistic_l2"]
    x, y = namespace["X"], namespace["y_cls"]
    for features, labels, options in (
        (x, y[:, None], {}),
        (x, y[:-1], {}),
        (x[:0], y[:0], {}),
        (x, [0, 0, 1, 2], {}),
        (np.full_like(x, np.nan), y, {}),
        (x, y, {"lr": 0}),
        (x, y, {"lam": np.inf}),
        (x, y, {"max_iter": 1.5}),
    ):
        with np.testing.assert_raises(ValueError):
            fit(features, labels, **options)
    with np.testing.assert_raises(FloatingPointError):
        fit(x * 1e200, y)

    with np.errstate(over="raise", invalid="raise"):
        np.testing.assert_allclose(namespace["sigmoid"]([-1000, 0, 1000]), [0, .5, 1])
    tiny = float(namespace["logit_gradient"](np.array([50.0]), np.array([1.0]))[0])
    check(namespace["sigmoid"](50.0) - 1.0 == 0.0, "Expected float64 sigmoid(50) saturation")
    np.testing.assert_allclose(tiny, -np.exp(-50), rtol=1e-14, atol=0)

    w, b, one_step = fit(x, y, max_iter=1)
    np.testing.assert_allclose([w[0], b], [.75, 0.0])
    objective = namespace["bce_from_logits"](x @ w + b, y) + .025 * float(w @ w)
    np.testing.assert_allclose(one_step.final_loss, objective)
    check(math.isclose(one_step.history[-1], one_step.final_loss), "One-step history mismatch")
    check(one_step.iterations == 1 and not one_step.converged, "One-step iteration flag mismatch")
    final = namespace["report"]
    check(final.converged and math.isclose(final.history[-1], final.final_loss), "Convergence check failed")

    files = (THEORY, LAB, MASTERY)
    for path in files:
        text = path.read_text()
        parse_frontmatter(text, path)
        lines = text.splitlines()
        for previous, line in zip(lines, lines[1:]):
            check(not (previous.startswith(">") and line and not line.startswith(">")),
                  f"{path}: unquoted line after blockquote: {line}")
        for target in re.findall(r"!?\[\[([^]|]+)(?:\|[^]]+)?\]\]", text):
            if target.startswith("#"):
                check(re.search(rf"(?m)^## {re.escape(target[1:])}$", text), f"{path}: missing heading {target}")
            else:
                check(BUNDLE / f"{target}.md" in files, f"{path}: missing bundle link {target}")

    report = {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scikit_learn": sklearn.__version__,
        "sha256": {path.name: sha256(path.read_bytes()).hexdigest() for path in files},
        "checks": {
            "lab_tracks_executed": len(blocks),
            "invalid_input_cases_rejected": 8,
            "nonfinite_state_rejected": True,
            "yaml_and_link_checks": "passed",
            "tiny_signed_gradient": tiny,
            "first_gradient_step": w.tolist(),
            "first_gradient_step_objective": one_step.final_loss,
            "first_unpenalized_newton_step": namespace["theta_unpenalized"].tolist(),
            "first_regularized_newton_step": namespace["theta_ridge"].tolist(),
            "gradient_descent_iterations": final.iterations,
            "gradient_descent_final_objective": final.final_loss,
            "gradient_descent_final_gradient_norm": final.gradient_norm,
            "max_coefficient_delta_vs_lbfgs": float(np.max(np.abs(namespace["w_fit"] - namespace["clf"].coef_[0]))),
            "intercept_delta_vs_lbfgs": abs(namespace["b_fit"] - float(namespace["clf"].intercept_[0])),
            "held_out_rows_lambda_weight_bce_precision_recall": [
                [float(value) for value in row.split()] for row in captured.getvalue().splitlines()
            ],
            "callout_boundary_check": "passed",
        },
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
