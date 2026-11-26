# Expected findings for the averaging-filter audit

Keep this key outside the candidate's context.

- **Missing core derivation.** The result $y[n]=0$ is correct, but the note omits the relation $x[n-1]=-x[n]$ and its substitution into the average. The constant-input result also lacks its two-sample substitution. Both are reconstructible from the draft.
- **Circular proof of a stipulated definition.** The filter is defined by an equal-weight average. The stated proof simply repeats that choice. Explain the role of equal weights and verify consequences of the choice.
- **Hidden interpretation.** With folds closed, the stated outcomes lack the comparison that gives them meaning. Move the supported comparison into visible prose.
- **Scope.** A read-only audit should explain local repairs from the supplied material. It should neither rewrite the draft nor introduce external results. A frequency-response derivation would need separate authorization if absent from the source.
