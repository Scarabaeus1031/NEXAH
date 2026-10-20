# PENT-02 — Pascal pentagon metric realization test

Date: `2026-10-10`

Status: `BOUNDED_CANDIDATE_EVIDENCE / NOT_ADMITTED`

## Question

Can the five-face glued Pascal fan from PENT-01 be embedded in a regular
pentagon so that its combinatorial `C5` / `D5` operators become exact Euclidean
isometries and the standard golden-ratio relations remain visible?

## Declared realization

Use a regular pentagon of circumradius `1`, with vertices

```text
V_f = (cos(-pi/2 + 2 pi f / 5), sin(-pi/2 + 2 pi f / 5)).
```

The Pascal node `(f,n,k)` at depth six is placed by

```text
t = n/6,  q = k/n,
P(f,n,k) = (1-t) C + t ((1-q) V_f + q V_(f+1)),
```

with all five apex nodes identified at the centre `C`. Compatible edge chains
are glued exactly as in PENT-01.

## Result

The finite numerical test passes at tolerance `1e-10`.

- the quotient embedding is well-defined and injective for all `106` nodes;
- rotation by `72°` realizes `r` and reflection in the declared axis realizes
  `m`;
- every `D5` action preserves the full vertex distance matrix;
- a regular-pentagon diagonal divided by a pentagram intersection has the
  golden-section ratio;
- `diagonal / side = phi`;
- the five Pascal base-centre nodes of weight `20` form one metric `C5` orbit.

Replay:

```sh
python3 run_test.py
```

## Boundary

This is a metric representation of the already declared finite carrier. The
golden ratio does not generate Pascal coefficients, and the Pascal recurrence
does not prove that physical pentagonal objects, prime labels or resonance
claims follow from this embedding. No 3D pyramid is defined here.

