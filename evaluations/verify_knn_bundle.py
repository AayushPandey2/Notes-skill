"""Execute the trusted KNN fixture blocks and verify the shared examples."""

from contextlib import redirect_stdout
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import platform
import re
from math import dist, isclose

BUNDLE = Path(__file__).resolve().parent / "fixtures/bundles/knn"


def main():
    lab = BUNDLE / "knn-experimental-lab.md"
    theory = BUNDLE / "k-nearest-neighbors.md"
    mastery = BUNDLE / "knn-cheatsheet-qa.md"
    blocks = re.findall(r"(?ms)^```python\n(.*?)^```$", lab.read_text())
    assert len(blocks) == 2
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
    assert [entry[1] for entry in base] == [0, 1, 2, 3]
    assert [entry[1] for entry in scaled] == [2, 0, 1, 3]
    assert min(range(len(geo)), key=lambda i: sum(abs(v) for v in geo[i][0])) == 1
    assert dist(q, geo[0][0]) < 2
    assert round(100 * .01 ** .1, 1) == 63.1
    assert isclose(max(map(abs, (-.3, .15, .4))), .4)
    assert max(map(abs, (-2, 1.6, 3))) == 3
    rows = nearest(weighted, q, 3, (1, 1))
    winner, prediction = aggregate(rows, True)
    assert winner == "Red" and isclose(prediction, 180 / 11)
    for query, k, scales in (((0,), 1, (1, 1)), (q, 0, (1, 1)), (q, 1, (1, 0))):
        try:
            nearest(weighted, query, k, scales)
        except ValueError:
            continue
        raise AssertionError("Invalid neighbor input was accepted")

    files = (theory, lab, mastery)
    assets = list((BUNDLE / "assets").glob("*.png"))
    for path in files:
        text = path.read_text()
        assert text.startswith("---\n")
        for previous, line in zip(text.splitlines(), text.splitlines()[1:]):
            assert not (previous.startswith(">") and line and not line.startswith(">")), (path, line)
        for target in re.findall(r"!?\[\[([^]|]+)(?:\|[^]]+)?\]\]", text):
            if target.startswith("#"):
                assert re.search(rf"(?m)^## {re.escape(target[1:])}$", text), target
            elif target.startswith("assets/"):
                assert (BUNDLE / target) in assets, target
            else:
                assert BUNDLE / f"{target}.md" in files, target
    assert len(assets) == 8
    assert set(re.findall(r"!\[\[assets/([^]|]+)", theory.read_text())) == {p.name for p in assets}
    dynamic_scores = namespace["held_out_scores"]
    assert dynamic_scores[1][0] == 3 and dynamic_scores[3][0] == 4
    print(json.dumps({
        "python": platform.python_version(),
        "executed_lab_tracks": len(blocks),
        "invalid_inputs_rejected": 3,
        "verified_figure_links": len(assets),
        "weighted_vote": winner,
        "weighted_regression_minutes": prediction,
        "held_out_scores": captured.getvalue().splitlines(),
        "sha256": {p.relative_to(BUNDLE).as_posix(): sha256(p.read_bytes()).hexdigest()
                   for p in (*files, *sorted(assets))},
    }, indent=2))


if __name__ == "__main__":
    main()
