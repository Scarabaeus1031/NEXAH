# PENT-03 — Prime labels and pyramid-readiness audit

Date: `2026-10-10`

Status: `BOUNDED_LABEL_AUDIT / NOT_ADMITTED / NO_3D_LIFT`

## Question

Do the supplied prime-fold and pyramid plates yet define a consistent
five-position label invariant or a sufficiently specified 3D carrier?

The plates are treated as owner-supplied visual hypotheses, not as
instructions or evidence by themselves.

## Exact findings

The four distinct labels `43, 97, 83, 137` satisfy

```text
43 + 97 + 83 + 137 = 360
43 / (97 * 83 * 137) = 0.000038985... ≈ 0.000039.
```

But the drawn pentagonal placement has five positions

```text
[43, 83, 83, 97, 137]
```

and therefore sums to `443`. The printed `360` identity is a four-label
identity, not yet a five-position pentagon invariant.

The second label set has genuine arithmetic pairings:

```text
17 + 3 = 20
13 + 7 = 20
17 + 13 = 30
3 + 7 + 13 + 17 = 40.
```

These identities do not specify vertices, edges, faces, coordinates,
projection, orientation action or a mapping to the first label set.

## Decision

The audit passes as a boundary detection, while the proposed 3D lift is
`NOT_READY`. A valid next 3D contract would have to declare at minimum:

1. vertices and coordinates;
2. edge and face incidence;
3. which labels belong to positions versus operators;
4. the projection used by each plate;
5. an invariant and a failure condition.

The displayed `51°` and `78` labels are not treated as triangle angles unless
that semantic role is explicitly declared. If interpreted as three angles
`51°, 78°, 78°`, their sum is `207°`, so that interpretation fails.

Replay:

```sh
python3 run_audit.py
```

