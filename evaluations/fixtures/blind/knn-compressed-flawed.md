---
id: knn-01
aliases: [KNN, K-nearest neighbors]
topic: K-Nearest Neighbors
tags: [topic/knn, subject/machine-learning, domain/computer-science]
nexttopics: []
---
# K-Nearest Neighbors (KNN)

KNN predicts an outcome for a new example by borrowing outcomes from similar training examples. The prediction depends on how distance is measured, how many neighbors are selected, and how their outcomes are combined.

**Difficulty** · Introductory, with a statistical extension.

**Prerequisites** · Coordinate differences, arithmetic means, and class counts. Conditional probability is introduced where it enters the argument.

## Learning objectives

- Trace the same neighborhood through classification, regression, and distance-weighted voting.
- Explain how feature scale and $k$ alter which observations influence a prediction.
- Design a leak-free evaluation and distinguish poor neighborhoods from slow neighbor search.

## Contents

- [[#1. From a query to a neighborhood|Neighbor selection]]
- [[#2. From neighbors to predictions|Voting and averaging]]
- [[#3. Distance defines similarity|Metrics and scaling]]
- [[#4. What changing k does|Smoothing and locality]]
- [[#5. Validation and failure diagnosis|Evaluation]]
- [[#6. Search and computational cost|Search cost]]
- [[#7. Mental model and notation|Review]]

## 1. From a query to a neighborhood

Suppose a machine reports two readings, both in comparable units. Earlier inspections have recorded a status and a repair time. A global baseline predicts the most common status or the average repair time over **all** inspected machines. That baseline gives every new machine the same answer, even if machines with similar readings behave differently.

KNN uses a **training set** of paired features and outcomes. Each feature vector $x_i$ contains $d$ measurements, one per coordinate. Together, $n$ such rows form an $n\times d$ matrix. The **query** $q$ is a new vector in the same feature space. During fitting, KNN retains the labeled examples, potentially after preprocessing and with a search index. At prediction time it measures the distance from $q$ to each candidate, selects the $k$ closest rows, and uses their outcomes. This is why KNN is called instance-based, or lazy learning. There is no global coefficient vector or gradient descent step in ordinary KNN. [scikit-learn nearest neighbors guide](https://scikit-learn.org/stable/modules/neighbors.html)

For the synthetic example below, $q=(0,0)$. Euclidean distance is straight-line distance. For $A=(1,0)$ it is $\sqrt{(1-0)^2+(0-0)^2}=1$. Every row uses the same calculation:

$$
d_2(q,x_i)=\sqrt{\sum_{j=1}^{d}(q_j-x_{ij})^2}.
$$

| Rank and ID | Readings $x_i$ | Status | Repair time (min) | Distance to $q$ |
|---|---|---|---:|---:|
| 1 · A | $(1,0)$ | Red | 10 | 1 |
| 2 · B | $(0,2)$ | Blue | 20 | 2 |
| 3 · C | $(0,3)$ | Blue | 30 | 3 |
| 4 · D | $(4,0)$ | Red | 40 | 4 |
| 5 · E | $(0,5)$ | Red | 50 | 5 |

$N_k(q)$ is the set of indices of the first $k$ rows in distance order. Use an integer $1\le k\le n$. At $k=3$, $N_3(q)=\{A,B,C\}$. At $k=n=5$, a **uniform** rule recovers the global baseline. Equal distances across the selection boundary can change which rows enter the neighborhood. A stable record ID gives one reproducible tie-break rule. Use a separate rule for tied class totals. Library conventions can differ. [scikit-learn tie behavior](https://scikit-learn.org/1.7/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)

## 2. From neighbors to predictions

For classification, assign each neighbor a nonnegative weight $w_i$ and require at least one positive weight. The indicator $\mathbf{1}\{y_i=c\}$ is 1 when the neighbor has class $c$ and 0 otherwise. The weighted fraction of votes for $c$ is

$$
\widehat p_c(q)=
\frac{\sum_{i\in N_k(q)} w_i\mathbf{1}\{y_i=c\}}
     {\sum_{i\in N_k(q)} w_i}.
$$

Each neighbor contributes its weight to exactly one class, so the class fractions sum to one. Selecting the largest fraction minimizes weighted disagreement with the neighborhood. If $W$ is the total weight and $W_c$ is the weight of class $c$, choosing $c$ incurs disagreement $W-W_c$. Minimizing that quantity is equivalent to maximizing $W_c$ because $W$ is fixed. Under equal error costs, predict the class with the largest vote fraction. For $A,B,C$ and uniform weights, Blue wins with $2/3$. Blue's vote share estimates the population probability $P(Y=\text{Blue}\mid X=q)$, the chance of Blue given those readings. Whether the estimate is calibrated should be checked on held-out predictions.

For regression, the same neighbor indices select numeric targets $y_i$. A natural local prediction minimizes the weighted sum of squared errors for a constant $a$. The result is the weighted mean:

$$
\widehat y(q)=\frac{\sum_{i\in N_k(q)} w_i y_i}
                   {\sum_{i\in N_k(q)} w_i}.
$$

> [!example]- Understand this formula step by step — why the weighted mean minimizes local squared error
> With the neighborhood and weights fixed, vary only the candidate prediction $a$. Define $W=\sum_{i\in N_k(q)}w_i>0$.
>
> $$
> \begin{aligned}
> L(a)&=\sum_{i\in N_k(q)}w_i(a-y_i)^2,\\
> L'(a)&=2\sum_{i\in N_k(q)}w_i(a-y_i)
>       =2aW-2\sum_{i\in N_k(q)}w_i y_i,\\
> L'(a)=0&\iff a=\frac{\sum_{i\in N_k(q)}w_i y_i}{W},\\
> L''(a)&=2W>0.
> \end{aligned}
> $$
>
> The positive second derivative makes the stationary point the unique global minimizer. Multiplying the loss by $1/W$ changes its scale while preserving its minimizer. For uniform weights on $A,B,C$, the prediction is $(10+20+30)/3=20$ min.

The mean is a convex combination, so it stays between the minimum and maximum selected targets. A query beyond the observed range can therefore get a numerically plausible but misleading estimate if the true relationship keeps increasing.

With inverse-distance weights $w_i=1/d_2(q,x_i)$ for positive distances, $A$ supplies weight $1$ to Red, and $B,C$ supply $1/2+1/3=5/6$ to Blue. Red wins with $6/11$ of the weight. The regression prediction becomes $(10+10+10)/(1+1/2+1/3)=180/11\approx16.36$ min. A common exact-match policy gives equal positive weights to selected zero-distance observations and zero weight to all farther ones. Conflicting exact matches still require aggregation. [scikit-learn weights implementation](https://github.com/scikit-learn/scikit-learn/blob/1.7.2/sklearn/neighbors/_base.py)

> [!question] Concept Checkpoint
> What changes if $k$ goes from 3 to 5 with uniform weights?
>
> > [!success]- Reveal Answer
> > Red wins $3$ to $2$, and the regression mean becomes $150/5=30$ min. Both predictions now use every training row, independent of the query.

## 3. Distance defines similarity

Euclidean distance combines squared coordinate differences. Manhattan distance combines their absolute values, so moving two units horizontally and one vertically costs $3$. Euclidean distance for that displacement is $\sqrt{5}$. Both belong to the Minkowski family:

$$
d_p(q,x_i)=\left(\sum_{j=1}^{d}\lvert q_j-x_{ij}\rvert^p\right)^{1/p},
\qquad p\ge 1.
$$

For example, relative to the origin, $(2,2)$ has Euclidean distance $\sqrt{8}$ versus $3$ for $(3,0)$. Their Manhattan distances are $4$ and $3$, respectively, so the nearest point changes. The order changes because Euclidean distance combines simultaneous displacements through squares while Manhattan distance adds their magnitudes directly.

Changing units can also reorder neighbors. In the running fixture, multiplying the first coordinate by 3 moves $A$ to distance $3$ and leaves $B$ at distance $2$. So raw units alone can flip the 1-NN vote. Standardization estimates a center $\mu_j$ and scale $s_j$ from training observations and maps each coordinate to $(x_j-\mu_j)/s_j$, for $s_j>0$. It amounts to weighted Euclidean distance in the original representation:

$$
d_{2,\mathrm{scaled}}(q,x_i)=
\sqrt{\sum_{j=1}^{d}\frac{(q_j-x_{ij})^2}{s_j^2}}.
$$

> [!example]- Understand this formula step by step — how standardization changes distance
> In each coordinate both points use the same fitted center and scale.
>
> $$
> \begin{aligned}
> z(q)_j-z(x_i)_j
> &=\frac{q_j-\mu_j}{s_j}-\frac{x_{ij}-\mu_j}{s_j}\\
> &=\frac{q_j-x_{ij}}{s_j}.
> \end{aligned}
> $$
>
> Squaring the last expression, summing across coordinates, and taking the square root gives the displayed distance. The center cancels, while the scale changes each coordinate's contribution by $1/s_j^2$. A constant training feature offers no variation between candidates. A scaler needs a defined zero-variance convention, or the feature can be dropped.

Standardization gives each feature a comparable unit of variation. It can amplify low-variance noise, and redundant features can count the same signal multiple times. Choose the representation with domain knowledge and validation. For nominal categories, consider matching-based distances or one-hot encoding with suitable weights. An arbitrary integer coding imposes distances such as category 3 being twice as far from category 1 as category 2 is. Fit data-dependent preprocessing inside each training fold. [scikit-learn preprocessing and leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html)

## 4. What changing k does

For $k=1$ and distinct training sites, each site owns the region of queries closest to it. These are Voronoi cells under Euclidean distance. Between sites $(0,0)$ and $(2,0)$, equality of squared distances gives $u^2+v^2=(u-2)^2+v^2$, hence $u=1$. Other sites can truncate the corresponding cell boundary. With $k>1$, the prediction changes as the selected set or vote changes. With distance weighting, vote totals can change even within a fixed set.

Small $k$ preserves small local structures and can let a single mislabeled row drive the result. Larger $k$ spreads influence across more observations and can wash out a genuine local minority or average across a real boundary. In regression with fixed neighbor locations and conditionally independent errors of common variance $\sigma^2$, a uniform mean's noise variance is $\sigma^2/k$, since variances add and each weight is $1/k$. That calculation concerns noise conditional on the locations. It leaves out bias from averaging different underlying outcome means and variability from the random locations themselves.

The **neighborhood radius** is the distance to the $k$th neighbor. Fixed $k$ can mean a small radius in dense regions and a large one in sparse regions. A simple geometric model shows why density matters in high dimensions. Suppose inputs are uniform on the unit cube and a query is far enough from its boundary for a coordinate-aligned cube of side $s$ to fit. The neighborhood occupies fraction $s^d$, so its expected training count is $ns^d$. To capture an expected 1% of the points requires $s=0.01^{1/d}$, or $0.1$ in two dimensions and about $0.63$ in ten. This illustrates why enough apparent neighbors may require spanning a large range in each coordinate. Effective dimension and feature relevance matter when data occupy a lower-dimensional structure.

In classical Euclidean consistency results under i.i.d. sampling, letting $k$ grow while $k/n\to0$ balances increasing evidence with increasing locality. This is an asymptotic condition, while finite-sample $k$ selection still depends on the task and the representation. [Stone, Consistent Nonparametric Regression](https://doi.org/10.1214/aos/1176343886)

> [!question] Concept Checkpoint
> Can a prediction based on five unanimous neighbors still be unreliable?
>
> > [!success]- Reveal Answer
> > Yes. If the fifth-neighbor distance is large compared with distances seen in validation, the local estimate may represent distant training cases poorly matched to the query. Vote agreement and coverage answer different questions.

## 5. Validation and failure diagnosis

1. Define the prediction unit and the score before tuning. For independent labeled rows, use stratified classification folds when feasible. Keep repeated observations of one entity together, and use chronological splits for forward prediction.
2. Fit preprocessing inside each training fold. Tune $k$, distance, and weights on validation predictions. Every candidate $k$ must fit within the smallest training fold.
3. Compare with a global baseline and inspect the errors that matter. Accuracy can hide rare-class failures, so check per-class recall or balanced accuracy when appropriate. Use MAE for typical absolute regression error or RMSE to place more weight on large errors.
4. Evaluate the selected pipeline on held-out data. If repeated tuning and assessment must use the same limited dataset, use an outer evaluation split around the tuning process.

Training accuracy at 1-NN can look excellent because each training point can retrieve itself. Ordinary cross-validation avoids that self-match by querying held-out rows. Duplicates and related observations can still cross folds if splitting ignores their origin. [scikit-learn cross-validation guide](https://scikit-learn.org/stable/modules/cross_validation.html)

| Symptom | Diagnostic test |
|---|---|
| Neighbors change wildly after a unit conversion | Compare the per-feature distance contributions before and after scaling. |
| Minority recall drops as $k$ grows | Inspect vote counts and radii near minority cases. Compare smaller $k$ or alternative weighting under the same split and metric. |
| Accuracy drops when adding features | Check neighbor overlap and validation error with and without the new features, keeping folds fixed. |
| Query has high vote share far from all training rows | Compare its neighbor radius with validation radii. A rejection rule requires its own tuning and coverage evaluation. |

## 6. Search and computational cost

For $n$ dense training rows of dimension $d$, a brute-force query evaluates $n$ distances at $O(d)$ each. Full sorting adds $O(n\log n)$ time. A bounded heap of size $k$ gives $O(nd+n\log k)$ for $k\ge2$ and uses $O(k)$ auxiliary storage. For $k=1$, a linear minimum scan suffices. The stored dense feature matrix requires $O(nd)$ memory, in addition to outcomes and any index. Squared Euclidean distance preserves rank because the square root is increasing on nonnegative inputs. Inverse **distance** weighting still requires the actual distance to avoid changing the vote.

Exact indexes such as KD trees and ball trees prune regions whose distance bounds rule them out. Their benefit depends on dimension, metric, data distribution, and $k$. Approximate neighbor search may trade retrieval accuracy for latency. Check both neighbor recall and downstream prediction quality if replacing an exact search. A radius-neighbor model fixes distance and lets the neighbor count vary, including the possibility of zero neighbors. K-means instead groups unlabeled observations via learned centers. [scikit-learn search algorithms and radius neighbors](https://scikit-learn.org/stable/modules/neighbors.html)

## 7. Mental model and notation

A prediction depends on three choices. The metric sets the geometry, $k$ sets how much local evidence to gather, and aggregation translates that evidence into an outcome.

| Symbol | Meaning |
|---|---|
| $n,d$ | Number of training rows and number of coordinates per row |
| $x_i,y_i,q$ | Training features, corresponding target, and query features |
| $d_p(q,x_i)$ | Minkowski distance with order $p$ |
| $N_k(q)$ | Indices of the $k$ selected training rows |
| $w_i,\widehat p_c(q)$ | Neighbor weight and normalized vote share for class $c$ |
| $\widehat y(q)$ | Numeric regression prediction |

[[01 - K-Nearest Neighbors - Experimental Lab|Experimental lab]] · [[01 - K-Nearest Neighbors - Cheatsheet & Interview Q&A|Cheat sheet and practice]]
