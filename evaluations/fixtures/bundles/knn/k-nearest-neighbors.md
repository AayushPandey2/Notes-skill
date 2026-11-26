---
id: eval-golden-knn
aliases:
  - K-Nearest Neighbors
  - KNN
topic: K-Nearest Neighbors
tags:
  - domain/ml
  - subject/machine-learning
  - topic/nearest-neighbors
nexttopics: []
---

# K-Nearest Neighbors

A technician wants to decide which of two inspections a machine needs. Past cases have readings and inspection labels. A rule based on the whole workshop gives every new machine the same answer. K-nearest neighbors (KNN) instead asks which cases most resemble this machine and uses their outcomes.

**Difficulty:** Beginner

**Prerequisites:** Coordinates, averages, comparison of positive numbers, and the Pythagorean theorem. The optional derivation of weighted averaging uses a derivative of a square.

## Learning objectives

- Trace a prediction from a query through distance, ranking, and aggregation.
- Explain why changing the metric, feature scale, or neighbor count can change a prediction.
- Distinguish distance ties, voting ties, and low evidence for a unanimous vote.
- Use neighborhood geometry and held-out validation to diagnose where KNN will struggle.

**Table of Contents**

- [[#1. What the model retains|Training and prediction]]
- [[#2. From distances to one prediction|Worked classification]]
- [[#3. What counts as close|Metrics and scales]]
- [[#4. What changes when k changes|Boundaries and reliability]]
- [[#5. Predicting a number|Regression and weights]]
- [[#6. Why neighborhoods grow in higher dimensions|Dimensionality]]
- [[#7. Search and validation|Implementation choices]]
- [[#8. Reconstruct the model|Mental model]]

## 1. What the model retains

Each past case stores **features**, the measured inputs, and an **outcome**, the result we want to predict. Learning with these labeled examples is supervised learning. The machine under inspection is the **query**. Its outcome is unknown at prediction time, and it needs measurements in the same order and units as the stored examples.

An instance-based model retains past cases for prediction. Fitting can still estimate preprocessing parameters or build a search index. Most work in finding a neighborhood and making a prediction happens when a query arrives. A linear model, by comparison, evaluates fitted coefficients at the query to obtain a prediction.

In the toy dataset below, $x$ is a temperature deviation in chosen units and $y$ is a vibration deviation in chosen units. The two classes, Amber and Blue, stand for inspection routes. These illustrative values teach the calculation. They do not establish a safe inspection rule.

| Case | $x$ | $y$ | Inspection |
|---|---:|---:|---|
| A | 1 | 1 | Amber |
| B | 0 | 1.8 | Blue |
| C | 3 | 0 | Blue |
| D | 4 | 3 | Amber |

## 2. From distances to one prediction

Set the query at $(0,0)$. Case A is one unit away on each coordinate. The straight-line distance is the hypotenuse of a right triangle:

$$
d(q,A)=\sqrt{1^2+1^2}=\sqrt 2\approx1.414.
$$

The same calculation gives these distances in the original feature units. Retain the exact values for ranking.

| Rank | Case | Exact distance | Class |
|---:|---|---:|---|
| 1 | A | $\sqrt 2$ | Amber |
| 2 | B | $1.8$ | Blue |
| 3 | C | $3$ | Blue |
| 4 | D | $5$ | Amber |

The **neighbor count** $k$ says how many rows of this ranking to keep. With $k=1$, A gives one Amber vote. With $k=3$, A, B, and C give one Amber and two Blue votes, so the prediction is Blue. With $k=4$, the neighborhood is the whole training set. Every query then receives the global vote under uniform weights, and this dataset needs a tie rule.

For general vectors $q$ and $x$ with $d$ coordinates, each squared difference contributes once to squared Euclidean distance.

$$
d_2(q,x)=\sqrt{\sum_{j=1}^d(q_j-x_j)^2}.
$$

> [!example]- Understand this formula step by step — From coordinate gaps to Euclidean distance
>
> In one dimension, distance is the absolute gap. To add a perpendicular coordinate, form a right triangle whose legs are the existing distance and the absolute gap on the new axis. The Pythagorean theorem adds their squares. Repeating for all perpendicular axes accumulates one squared gap per coordinate and taking the nonnegative square root returns the distance.
>
> The same ranking results if all candidates are compared using squared distance, since square root is increasing on nonnegative values.

A **selection tie** occurs when two candidates have equal distance across the cutoff. A **vote tie** occurs when leading classes receive equal support among the selected neighbors. A fixed record order can break selection ties in this example, and a declared class order can break vote ties. Neither convention changes the distances.

> [!question] Can an odd neighbor count still produce a vote tie?
> Imagine the nearest three labels are Amber, Blue, and Green.
> > [!success]- Reveal Answer
> > Yes. Each class receives one vote. An odd count prevents a two-class count tie under uniform voting, but multiclass votes and unequal weights require separate reasoning.

## 3. What counts as close

Euclidean distance follows the diagonal from the query to A. Manhattan distance measures the total movement along the axes. The route to A contains a horizontal step of one and a vertical step of one, so the Manhattan distance is $2$.

![[assets/metric-paths.png|520]]

The solid diagonal has length $\sqrt 2$. The dashed two-leg path has total length $2$.

Author-created illustration using the toy dataset.

For B, both distances are $1.8$ because it lies on one axis. Euclidean distance therefore ranks A first, while Manhattan distance ranks B first. The labels and coordinate values stay fixed. Only the meaning of proximity changes.

Feature scaling changes the contribution of a coordinate even with the same metric. Divide the horizontal coordinate of the query and all training points by six. The distances from the query to A and C become $\sqrt{1+(1/6)^2}\approx1.014$ and $3/6=0.5$. B is still $1.8$ away and D is over $3$ away. C becomes the nearest case.

![[assets/neighbor-scaling.png|700]]

The star marks the query and the connecting line identifies the nearest stored case. Both panels share the same visible plotting scale and label their horizontal units. Compare how C moves horizontally while its class remains Blue.

Author-created illustration using the toy dataset.

In a deployed workflow, estimate a scaling rule on training data only and apply it to both stored cases and queries. Here the divisor is stipulated to isolate a geometric effect. Choosing a scale in practice requires domain judgment or validation.

> [!question] Can scaling change the prediction at k = 3 here?
> Rank the four cases after horizontal rescaling. Identify which outcomes enter the vote.
> > [!success]- Reveal Answer
> > The new ranking is C, A, B, D. The nearest case changes, but the three selected cases are the same, with two Blue votes.

## 4. What changes when k changes

Move the query around the original feature space. At $k=1$, each case owns the region closer to it than any other case. These are Voronoi regions under Euclidean distance. The boundary between two cases lies where their distances agree. When adjacent regions carry the same class, their shared edge is invisible in the class prediction.

![[assets/vote-boundaries.png|700]]

The outlines show where the predicted class changes on the plotted grid. Marker shapes identify stored classes. The query star lies in an Amber region at $k=1$ and a Blue region at $k=3$. The figure approximates boundaries on a grid and omits same-class Voronoi edges.

Author-created illustration using the toy dataset.

Larger neighborhoods often reduce sensitivity to one noisy label. They can also mix observations from different mechanisms. Nearby minority cases can lose their vote as more distant majority cases enter. This is the intuition behind a bias–variance trade-off, with outcomes that depend on the data and metric.

A unanimous vote does not measure coverage. If a query is distant from every training case, the vote can be unanimous and still give weak evidence about the query. The farthest selected distance is a useful additional diagnostic. A vote fraction becomes a probability estimate only under modeling assumptions and should be checked for calibration if used that way.

## 5. Predicting a number

Keep the same neighbors and use illustrative time outcomes. A took 12 minutes, B took 6, and C took 3. For $k=3$, uniform regression averages those outcomes to $(12+6+3)/3=7$ minutes.

Suppose the chosen weighting rule instead gives these neighbors weights $3,2,1$. The weighted total is $36+12+3=51$ and weight mass is $6$, so the prediction is $8.5$ minutes. A larger weight gives that case more say.

$$
\hat t=\frac{\sum_{i\in N_k(q)} w_i t_i}{\sum_{i\in N_k(q)} w_i}.
$$

> [!example]- Understand this formula step by step — Why the weights are normalized
>
> Choose a local constant $c$ that minimizes the weighted squared prediction errors, with nonnegative weights and positive total weight. Each squared error contributes derivative $2w_i(c-t_i)$. Their sum is zero precisely when
>
> $$
> c\sum_i w_i=\sum_i w_i t_i.
> $$
>
> Divide by the positive weight total. The second derivative is twice that total, so the stationary value is the unique minimum for the selected neighborhood. This also explains why multiplying all weights by the same positive number leaves the result unchanged.

Nonnegative normalized weights sum to one, so the prediction lies between the smallest and largest selected outcomes. Ordinary averaging cannot extrapolate beyond those outcomes. If using inverse-distance weights, declare what happens at zero distance. One rule averages only the exact matches when they occur.

## 6. Why neighborhoods grow in higher dimensions

Imagine observations spread uniformly through a unit square. A smaller square with side length $s$ contains fraction $s^2$ of the area, so a square with side $0.1$ covers one percent of the area. In three dimensions, a cube with that same side covers only $0.1^3=0.001$ of the volume.

To keep the fraction fixed at $f$, the required side length increases with dimension $d$.

$$
s^d=f\quad\Longrightarrow\quad s=f^{1/d},
\qquad 0<f<1.
$$

> [!example]- Understand this formula step by step — Side length for a fixed volume fraction
>
> A $d$-dimensional cube has one side factor $s$ per coordinate. Its volume is their product, and the unit cube has volume one. To obtain fraction $f$, solve $s^d=f$ by taking the positive $d$th root. For fixed $f$ in $(0,1)$, $\ln s=(\ln f)/d$ approaches zero from below as $d$ grows, so the side length approaches one.
>
> At one percent volume, $s=0.1$ in two dimensions and $s\approx0.631$ in ten.

![[assets/cube-side-length.png|620]]

The vertical axis gives the required side as a percentage of a full unit side, for a region containing one percent of the volume. Compare the 10% required in two dimensions with 63.1% in ten.

Author-created illustration of the uniform unit-cube calculation.

A substantial sample fraction can require a wide region along each coordinate. This toy model explains why local evidence may be sparse in many dimensions. It uses axis-aligned cubes and uniform data, so it does not predict the exact Euclidean radius or sample requirement for a real dataset.

## 7. Search and validation

**Brute-force search.** Calculate a distance to each of $n$ stored cases. Each distance uses $d$ features, so distance computation scales as $O(nd)$ per query. A full comparison sort adds $O(n\log n)$ ranking cost. Maintaining only the best $k$ entries with a bounded heap takes $O(n\log k)$ comparison work for $k\ge2$ and avoids sorting all distances.

**Exact indexing.** A KD tree partitions feature space by coordinate splits. After finding a tentative neighbor, it can skip regions whose lower-bound distance exceeds the current cutoff. A ball tree uses bounding regions defined by centers and radii. Pruning saves work only when the bounds exclude enough candidates. High dimension, metric choice, or data arrangement can weaken pruning enough that brute force is preferable.

**Approximate search.** An approximate index can return neighbors without certifying the exact top $k$. Evaluate retrieval against exact neighbors on a sample, then check whether missed cases change model predictions. Search recall and classification recall measure different things.

**Model validation.** Compare neighborhood count, metric, scaling, and weighting on held-out data. Fit preprocessing within each training split. Keep the final test split separate from tuning, and match the evaluation metric to the decision or probability use. Leave room to abstain or request more evidence when a query has no nearby support.

K-means has a different goal: it groups unlabeled cases around learned centers. KNN makes supervised predictions from stored outcomes. A nearest-center rule can resemble a nearest-neighbor prediction geometrically while using a different representation and training objective.

## 8. Reconstruct the model

A query creates its own ranked neighborhood. The metric and feature scales determine that ranking. The neighbor count determines how many outcomes influence the vote or average. Checking distance as well as the reported prediction tells you when the apparent consensus may have little local support.

In this note, $n$ counts training cases, $d$ counts coordinates, $d_2$ denotes Euclidean distance, $k$ counts selected neighbors, and $N_k(q)$ denotes their index set.
