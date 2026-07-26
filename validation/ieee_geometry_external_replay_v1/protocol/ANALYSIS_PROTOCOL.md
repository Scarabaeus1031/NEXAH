# G2 Analysis Protocol Candidate

Status: **candidate for review; no comparison executed**

The machine-readable authority is
[`g2_protocol_candidate.json`](g2_protocol_candidate.json).

## Units of alignment

- indicator level: one available campaign position;
- local change, adjacent displacement, and normalized local drift: the adjacent
  pair ending at campaign index `i`;
- centred absolute second difference, direction change, and curvature: the
  centred triplet at campaign index `i`;
- cumulative comparator variation and V1 path length: the same contiguous
  converged prefix within a segment;
- distance-to-last-converged: reported descriptively against availability only;
  it is not assigned a fabricated physical comparator.

Development and evaluation cases remain separate. No statistic pools IEEE-9
and IEEE-14.

## Predeclared comparisons

1. Verify exact case ID, role, campaign index, load scale, and availability
   alignment.
2. Compare adjacent displacement and normalized local drift separately with
   each Tier 0 absolute adjacent change.
3. Compare direction change and discrete curvature separately with each Tier 0
   centred absolute second difference.
4. Compare campaign path length with each Tier 0 cumulative absolute variation.
5. Report Spearman rank correlation for each aligned pair only when there are at
   least five paired observations and both variables have at least three
   tolerance-distinct groups.
6. Report tie-inclusive top-3 and top-5 overlap as intersection count, union
   count, and Jaccard ratio for local measures.
7. Preserve the signed comparator changes beside the absolute-magnitude
   analysis so direction is not hidden.

No p-values, confidence intervals, accuracy, AUROC, lead time, false-alarm
rate, forecast skill, outcome label, threshold tuning, or combined score is
permitted.

## Result classification

The analysis records primitive statistics, availability counts, tie groups,
and discrepancies first. The package-level class is then one of:

- `reproduced_descriptively_distinct`;
- `reproduced_substantially_redundant`;
- `reproduced_comparison_indeterminate`;
- `not_reproduced`;
- `protocol_specification_ambiguity`.

`substantially_redundant` may be used only when one direct comparator shows
absolute Spearman correlation of at least `0.90` for every applicable local
geometry measure in both cases and its tie-inclusive top-5 set is identical in
both cases. Otherwise the report must not infer redundancy from a single high
coefficient. If a statistic is unavailable or conditions disagree, preserve
the ambiguity or contradiction.

These labels are descriptive and are not claims of prediction, stability
assessment, control value, or external validity.

## Sensitivity boundary

No leave-one-feature-out analysis is included in SR-1 G2. It would recompute a
changed representation and is not needed for the bounded comparator question.
Only the frozen numerical comparison tolerance may be applied.

