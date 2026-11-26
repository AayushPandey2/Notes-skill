---
id: eval-golden-knn-lab
aliases:
  - KNN Experimental Lab
topic: K-Nearest Neighbors
tags:
  - domain/ml
  - subject/machine-learning
  - topic/nearest-neighbors
nexttopics: []
---

# KNN Experimental Lab

Implement the complete path from query to prediction, then test a case where changing one setting changes the decision. Use Python 3.11 and its standard library. Start with [[k-nearest-neighbors|the theory]] and use the [[knn-cheatsheet-qa|mastery pack]] to practice independently.

## Track 1 — Exact neighbors, votes and averages

Use the five-case fixture from theory. Input order is stable record order. Distance ties at the cutoff go to the earlier row. The vote uses alphabetical class order for an equal score. The caller supplies positive feature scales. A scale of 6 divides that coordinate's contribution to Euclidean distance by 6 before computing its norm.

```python
from math import dist, isfinite


def nearest(rows, query, k, scales):
    if not query or len(query) != len(scales):
        raise ValueError("Supply one positive scale per feature")
    if type(k) is not int or not 1 <= k <= len(rows):
        raise ValueError("k must be an integer between 1 and the row count")
    if not all(isfinite(value) for value in query):
        raise ValueError("Query features must be finite")
    if not all(isfinite(scale) and scale > 0 for scale in scales):
        raise ValueError("Feature scales must be finite and positive")
    ranked = []
    for index, (point, label, target) in enumerate(rows):
        if len(point) != len(query) or not all(isfinite(value) for value in point):
            raise ValueError("Training feature dimensions must match and be finite")
        if not isfinite(target):
            raise ValueError("Regression targets must be finite")
        gaps = [(value - reference) / scale
                for value, reference, scale in zip(point, query, scales)]
        distance = dist(gaps, [0.0] * len(query))
        if not isfinite(distance):
            raise ValueError("Scaled distance is not finite")
        ranked.append((distance, index, label, target))
    return sorted(ranked, key=lambda row: (row[0], row[1]))[:k]


def aggregate(neighbors, inverse_distance=False):
    exact_match = any(distance == 0 for distance, *_ in neighbors)
    # Multiplying every positive inverse-distance weight by the minimum
    # distance leaves votes and means invariant and keeps weights <= 1.
    reference = neighbors[0][0]
    totals = {}
    weighted_target = 0.0
    for distance, _, label, target in neighbors:
        if not inverse_distance:
            weight = 1.0
        elif exact_match:
            weight = float(distance == 0)
        else:
            weight = reference / distance
        totals[label] = totals.get(label, 0.0) + weight
        weighted_target += weight * target
    weight_sum = sum(totals.values())
    winner = min(totals, key=lambda label: (-totals[label], label))
    return winner, weighted_target / weight_sum


weighted_fixture = [
    ((1, 0), "Red", 10), ((0, 2), "Blue", 20), ((0, 3), "Blue", 30),
    ((4, 0), "Red", 40), ((0, 5), "Red", 50),
]
geo_fixture = [
    ((1, 1), "Amber", 12), ((0, 1.8), "Blue", 6),
    ((3, 0), "Blue", 3), ((4, 3), "Amber", 9),
]
q = (0, 0)
neighborhood = nearest(weighted_fixture, q, 3, (1, 1))
assert [row[1] for row in neighborhood] == [0, 1, 2]
assert aggregate(neighborhood) == ("Blue", 20.0)
label, minutes = aggregate(neighborhood, inverse_distance=True)
assert label == "Red" and abs(minutes - 180 / 11) < 1e-12
assert aggregate(nearest(geo_fixture, q, 1, (1, 1)))[0] == "Amber"
assert aggregate(nearest(geo_fixture, q, 1, (6, 1)))[0] == "Blue"
assert aggregate(nearest(geo_fixture, q, 3, (6, 1)))[0] == "Blue"

ties = [((0, 0), "Red", 10), ((0, 0), "Blue", 20), ((1, 0), "Red", 100)]
assert aggregate(nearest(ties, q, 1, (1, 1)), True) == ("Red", 10.0)
assert aggregate(nearest(ties, q, 3, (1, 1)), True) == ("Blue", 15.0)
```

> [!example]- Understand this implementation — The neighbor and prediction contract
>
> **A. Inputs.** Use a shared feature order and a positive scale for each coordinate. The rows carry both a class and a target so classification and regression can reuse a ranking.
>
> **B. Distance.** Subtract the query before normalizing each gap. The Euclidean norm assigns one squared contribution to each scaled gap.
>
> **C. Selection.** Sort by distance and stable record index, then take exactly $k$. The cutoff rule decides which cases enter before the vote starts.
>
> **D. Aggregation.** Each selected case adds its weight to one class and contributes its weighted target. Divide the target sum by total weight to obtain the local mean.
>
> **E. Numerical trace.** In the five-case example the nearest distances are 1, 2, and 3. Uniform weights return Blue and 20 minutes. Inverse-distance weights return Red and $180/11$ minutes.
>
> **F. Boundary.** Selected exact matches suppress farther cases under inverse-distance weighting. With both zero-distance rows selected, their target average is 15 minutes and the class tie goes to Blue under the declared rule.
>
> **G. Diagnosis.** When a predicted label changes, compare the ranked rows before comparing vote totals. Here scaling changes the ranking, whereas weighting changes totals for a fixed ranking.

## Track 2 — Validation and failure diagnosis

Use a separate toy split with overlapping outcomes. Fit the feature scale on the training rows for each experiment. Validation outcomes may guide the choice of $k$. They may not enter the feature transform or the stored neighborhood.

```python
from statistics import pstdev

train = [
    ((0, 0), "Blue", 8), ((0.2, 0.4), "Blue", 9),
    ((0.5, 1.0), "Amber", 20), ((0.8, 0.6), "Blue", 12),
    ((1.0, 1.4), "Amber", 24), ((1.3, 1.6), "Amber", 28),
]
validation = [
    ((0.1, 0.3), "Blue", 9), ((0.45, 0.8), "Blue", 13),
    ((1.1, 1.5), "Amber", 26), ((1.5, 1.7), "Amber", 30),
]
train_scales = tuple(pstdev(row[0][j] for row in train) or 1.0 for j in range(2))


def score(queries, k):
    correct = 0
    absolute_error = 0.0
    for point, label, target in queries:
        prediction, minutes = aggregate(nearest(train, point, k, train_scales))
        correct += prediction == label
        absolute_error += abs(minutes - target)
    return correct, absolute_error / len(queries)


assert score(train, 1) == (len(train), 0.0)  # Distinct rows can retrieve themselves.
held_out_scores = {k: score(validation, k) for k in (1, 3)}
assert held_out_scores[1][0] < len(validation)
assert aggregate(nearest(train, (0.45, 0.8), 1, train_scales))[0] == "Amber"
assert aggregate(nearest(train, (0.45, 0.8), 3, train_scales))[0] == "Blue"
for k, (correct, mae) in held_out_scores.items():
    print(f"k={k}: {correct}/{len(validation)} correct, MAE={mae:.2f} min")
```

> [!example]- Understand this investigation — The effect of k on held-out data
>
> **A. Split.** The miniature validation queries never become stored candidates. Use a separate test set for a performance claim after tuning.
>
> **B. Transform.** Estimate feature scales from training features alone. An intercept or mean subtraction is unnecessary for these distances because a shared mean cancels from a coordinate gap.
>
> **C. Controlled choice.** Compare $k=1$ and $k=3$ using the same rows, scales, metric, and aggregation rule.
>
> **D. Classification score.** Count correct labels against the same four validation targets.
>
> **E. Regression score.** Absolute errors remain in minutes. Average them to compare the two settings without conflating class labels with repair times.
>
> **F. Distinguish self-match.** Perfect scores against these distinct training points at $k=1$ arise because the nearest point is the query itself. The same guarantee does not hold for held-out rows.
>
> **G. Follow-up.** Inspect the neighbors for $(0.45,0.8)$ under both settings. One nearby Amber case controls $k=1$. At $k=3$ two Blue cases join the neighborhood and reverse the decision. Repeat with grouped or temporal splits when appropriate.

The held-out rows are illustrative. They show how an evaluation is constructed and why self-matches matter. Their scores do not estimate performance on real machines.

Expected results are derived from the stated fixtures. This lab's separate repository execution record is in [the evaluation specification](evaluation-spec.md).
