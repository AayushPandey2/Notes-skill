"""Execute the trusted KNN fixture blocks and verify YAML, callouts, links, and error guards."""

from contextlib import redirect_stdout
from hashlib import sha256
from io import StringIO
import json
from math import dist, isclose
from pathlib import Path
import platform
import re
import yaml

BUNDLE = Path(__file__).resolve().parent / "fixtures/bundles/knn"


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
    lab = BUNDLE / "knn-experimental-lab.md"
    theory = BUNDLE / "k-nearest-neighbors.md"
    mastery = BUNDLE / "knn-cheatsheet-qa.md"
    blocks = re.findall(r"(?ms)^```python\n(.*?)^```$", lab.read_text())
    check(len(blocks) == 2, f"Expected 2 python blocks, found {len(blocks)}")
    namespace = {}
    captured = StringIO()
    with redirect_stdout(captured):
        for number, block in enumerate(blocks, 1):
            exec(compile(block, f"{lab.name}:track-{number}", "exec"), namespace)

    nearest = namespace["nearest"]
    aggregate = namespace["aggregate"]
    weighted = namespace["weighted_fixture"]
    geo = namespace["geo_fixture"]
    q = namespace["q"]
    base = nearest(geo, q, 4, (1, 1))
    scaled = nearest(geo, q, 4, (6, 1))
    check([entry[1] for entry in base] == [0, 1, 2, 3], "Unexpected unscaled ordering")
    check([entry[1] for entry in scaled] == [2, 0, 1, 3], "Unexpected scaled ordering")
    check(min(range(len(geo)), key=lambda i: sum(abs(v) for v in geo[i][0])) == 1, "L1 index check failed")
    check(dist(q, geo[0][0]) < 2, "Chebyshev/Euclidean comparison failed")
    check(round(100 * .01 ** .1, 1) == 63.1, "Dimension edge-length identity failed")
    check(isclose(max(map(abs, (-.3, .15, .4))), .4), "Cosine L-inf margin check failed")
    check(max(map(abs, (-2, 1.6, 3))) == 3, "Non-orthogonal L-inf check failed")
    rows = nearest(weighted, q, 3, (1, 1))
    winner, prediction = aggregate(rows, True)
    check(winner == "Red" and isclose(prediction, 180 / 11), "Weighted aggregation check failed")
    for query, k, scales in (((0,), 1, (1, 1)), (q, 0, (1, 1)), (q, 1, (1, 0))):
        try:
            nearest(weighted, query, k, scales)
        except ValueError:
            continue
        raise RuntimeError("Invalid neighbor input was accepted")

    # Verify aggregate() input validation and overflow-safe target aggregation
    for bad_rows in (
        [],
        [(-1.0, 0, "Red", 10)],
        [(float("nan"), 0, "Red", 10)],
        [(1.0, 0, "Red", float("inf"))],
    ):
        try:
            aggregate(bad_rows, True)
        except ValueError:
            continue
        raise RuntimeError(f"Invalid aggregate input was accepted: {bad_rows}")

    _, large_pred = aggregate([(1.0, 0, "Red", 1e308), (1.0, 1, "Red", 1e308)], True)
    check(isclose(large_pred, 1e308), "Normalized large-target aggregation overflowed")

    files = (theory, lab, mastery)
    assets = list((BUNDLE / "assets").glob("*.png"))
    for path in files:
        text = path.read_text()
        parse_frontmatter(text, path)
        for previous, line in zip(text.splitlines(), text.splitlines()[1:]):
            check(not (previous.startswith(">") and line and not line.startswith(">")),
                  f"{path}: unquoted continuation after blockquote: {line}")
        for target in re.findall(r"!?\[\[([^]|]+)(?:\|[^]]+)?\]\]", text):
            if target.startswith("#"):
                check(re.search(rf"(?m)^## {re.escape(target[1:])}$", text), f"{path}: missing heading {target}")
            elif target.startswith("assets/"):
                check((BUNDLE / target) in assets, f"{path}: missing asset {target}")
            else:
                check(BUNDLE / f"{target}.md" in files, f"{path}: missing bundle link {target}")
    check(len(assets) == 8, f"Expected 8 KNN PNG assets, found {len(assets)}")
    check(set(re.findall(r"!\[\[assets/([^]|]+)", theory.read_text())) == {p.name for p in assets},
          "Theory note does not embed all 8 PNG assets")
    dynamic_scores = namespace["held_out_scores"]
    check(dynamic_scores[1][0] == 3 and dynamic_scores[3][0] == 4, "Held-out validation score check failed")
    print(json.dumps({
        "python": platform.python_version(),
        "executed_lab_tracks": len(blocks),
        "invalid_inputs_rejected": 7,
        "yaml_and_link_checks": "passed",
        "verified_figure_links": len(assets),
        "weighted_vote": winner,
        "weighted_regression_minutes": prediction,
        "held_out_scores": captured.getvalue().splitlines(),
        "sha256": {p.relative_to(BUNDLE).as_posix(): sha256(p.read_bytes()).hexdigest()
                   for p in (*files, *sorted(assets))},
    }, indent=2))


if __name__ == "__main__":
    main()
