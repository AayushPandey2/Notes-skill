---
id: eval-golden-knn-qa
aliases:
  - KNN Cheatsheet and Interview Q&A
topic: K-Nearest Neighbors
tags:
  - domain/ml
  - subject/machine-learning
  - topic/nearest-neighbors
nexttopics: []
---

# KNN Cheatsheet and Interview Q&A

Use the [[k-nearest-neighbors|theory chapter]] for derivations and the [[knn-experimental-lab|experimental lab]] for executable checks.

| Decision | What to reconstruct |
|---|---|
| Representation | Use the same feature order and transform for training rows and each query. Fit learned preprocessing inside the training split. |
| Distance | A metric ranks candidates. Scaling changes contributions before ranking. |
| Selection | Keep the first $k$ rows, using a declared cutoff tie rule. Inspect the $k$th distance for locality. |
| Classification | Compare class weight totals. Apply a separate policy for tied top totals. |
| Regression | Divide the weighted target sum by positive total weight. Nonnegative weights keep the estimate within the selected target range. |
| Search | An exact bound can prune a region. Approximate search trades away the guarantee of returning the exact neighborhood. |

## Explain and compare

> [!question] Why can weighting reverse the five-case fixture's three-neighbor vote?
>
> > [!success]- Reveal Answer
> > A is Red at distance 1. B and C are Blue at distances 2 and 3. Uniform counts give Blue two votes to one. Inverse distances give Red 1 and Blue $1/2+1/3=5/6$. A's influence beats the two farther cases combined.

> [!question] When does the output behave like a global baseline?
>
> > [!success]- Reveal Answer
> > Selecting every stored row with uniform weights makes the class vote or numerical mean independent of the query. A global class tie still needs a convention. Distance weighting can retain query dependence even with every row selected.

## Calculate and diagnose

> [!question] A query has two selected exact matches with labels Red and Blue and times 10 and 20 minutes. A farther Red case took 100 minutes. What happens under the lab's inverse-distance convention?
>
> > [!success]- Reveal Answer
> > The exact matches receive equal positive weight. The farther case has zero weight. The predicted time is 15 minutes. Alphabetical class order resolves the tied scores to Blue in the lab. At $k=1$, the cutoff rule can exclude one exact match before either outcome is combined.

> [!question] Why can raising k change nothing about accuracy but still change model behavior?
>
> > [!success]- Reveal Answer
> > Changing the neighborhood can alter vote shares, repair-time estimates, or radii without changing the winning labels on the validation set. Report a metric for the behavior you care about. Check held-out calibration if the vote share is used as a probability.

## Transfer

> [!question] At a new query, your current nearest point is 1.7 units away. A split gives a lower bound of 1.5 for the unsearched subtree. Can you prune it for k = 1?
>
> > [!success]- Reveal Answer
> > No. A lower bound of 1.5 leaves room for a point closer than 1.7. If the bound were 2, the whole subtree would be too far away. Equality needs care when record order resolves distance ties.

> [!question] A dataset has one row per visit and several visits per machine. Standardization was fit before random row splitting. Identify two leaks and fix them.
>
> > [!success]- Reveal Answer
> > The global scaling rule saw validation features. Fit the transform inside each training fold. Random row splits can place visits from the same machine in both training and evaluation. Split by machine for the target of generalizing to unseen machines, then fit the scale inside each split.
