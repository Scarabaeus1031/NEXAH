# Advisory Comparison Profile 0.1

Profile ID: `NC01-ADVISORY-0.1`

## Unit types

- `FACT` — a proposition presented as supported by admitted evidence;
- `ASSUMPTION` — a proposition taken as a condition rather than established;
- `CALCULATION` — declared formula, operands, units, time basis and result;
- `RECOMMENDATION` — a proposed action with conditions and boundaries.

The type is explicit. No statement changes type because of its wording.

## Multirecord comparison

One Human-confirmed AnalysisRecord is declared as the reference solely to make
directional `LOST` and `ADDED` classifications reproducible. Reference status
does not imply truth, quality or preference.

- `INVARIANT`: materially compatible units exist in the reference and every
  compared analysis under the declared criterion.
- `LOST`: a reference unit has no satisfying counterpart in one or more
  compared analyses.
- `ADDED`: a unit absent from the reference appears in one or more compared
  analyses.
- `UNAVAILABLE`: required evidence, metadata, unit, time basis, formula or
  comparison criterion is missing or incompatible, so the relation cannot be
  classified safely.

Each relation group is exclusive and lists all participating claim IDs. A
claim may occur in only one relation group for a ComparisonRecord.

## Calculation and boundary checks

Calculation checks retain formula, operands, result, unit, time basis and
tolerance. Unit or time mismatch yields `MISMATCH` or `UNRESOLVED`; it never
silently converts. Recommendations are compared as conditional records and
are never promoted to facts.

## Closed residual reasons

`MISSING_COUNTERPART`, `PRESENT_ONLY_OUTSIDE_REFERENCE`, `EVIDENCE_MISSING`,
`EVIDENCE_ASYMMETRY`, `ASSUMPTION_CONFLICT`, `FORMULA_MISMATCH`,
`OPERAND_MISMATCH`, `UNIT_MISMATCH`, `TIME_BASIS_MISMATCH`,
`RECOMMENDATION_BOUNDARY_CONFLICT`, `DOMAIN_INCOMPATIBLE`,
`CRITERION_UNAVAILABLE`, `REQUIRED_METADATA_UNAVAILABLE`.

## Claim ceiling

The profile compares declared confirmed records. It does not determine truth,
correctness, completeness, safety, suitability, causality, recommendation
quality, business success or product-market fit.
