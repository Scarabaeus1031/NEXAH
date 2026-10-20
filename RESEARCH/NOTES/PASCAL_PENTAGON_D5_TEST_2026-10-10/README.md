# Pascal pentagon / D5 boundary test

Date: `2026-10-10`

Status: `BOUNDED_CANDIDATE_EVIDENCE / WORKING_NAME / NOT_ADMITTED`

## Question

Can five depth-six Pascal triangles be rotated and mirrored into one connected
pentagonal carrier without breaking their binomial weights or recurrence?

`Pascal pentagon` is a working name for the declared construction below, not
a claim that this is an established mathematical object.

## Construction

Each face `f in Z5` carries the seven Pascal rows `n=0..6` with nodes

```text
(f,n,k),  0 <= k <= n <= 6,
w(f,n,k) = C(n,k).
```

The five copies become a connected pentagonal fan by gluing compatible side
chains:

```text
(f,n,n) ~ (f+1,n,0),  n=1..6,
```

and identifying the five apex nodes `(f,0,0)`.

The operators are

```text
r(f,n,k) = (f+1,n,k),
m(f,n,k) = (-f,n,n-k).
```

After quotienting the seams, `m` maps seam `s` to `-s-1 mod 5`.

## Result

The exhaustive finite test passes.

- `r^5 = e`: five orientations, equivalently identity/return plus four
  non-identity turns;
- `m^2 = e`;
- `m r m = r^-1`;
- the ten actions `r^a` and `m r^a` are distinct and form `D5`;
- all actions preserve binomial weights and quotient recurrence edges;
- the boundary weights agree on every glued seam because both Pascal side
  chains carry weight `1`;
- five separate triangles have `140` nodes and five components;
- the glued pentagonal fan has `106` unique nodes and one component;
- row `n=6` contains five distinct central nodes of weight
  `C(6,3)=20`; rotation cycles them and reflection preserves their set.

Replay:

```sh
python3 run_test.py
```

Interactive inspector:

- [`PASCAL_PENTAGON_EXPLORER.html`](PASCAL_PENTAGON_EXPLORER.html) keeps
  PENT-01 structure, PENT-02 metric realization, PENT-03 label boundary,
  PENT-04 pentagonal-bipyramid lift, PENT-05 `H2 direct-sum A1` root
  completion, PENT-06 dynamic-boundary growth and PENT-07 typed
  pentagon/hexagon coupling audit visually separate. Its additional `D30
  joint` view exposes the already verified `D1..D5 x C30` address/phase lift,
  accepts bounded `L/R` branch words and keeps C5 rotation, D5 reflection and
  local phase motion typed separately. This remains part of PENT-07, not
  `PENT-08`. It is a
  view over the replay records, not an additional experiment or evidence
  authority.

Formal specification and canonical reference object:

- [`SCC_003_REFERENCE/`](SCC_003_REFERENCE/) defines `P_6`, the five copies,
  open and closed seam quotients, weights, directed adjacency, facewise Pascal
  recurrence and the typed `D_5` action without reference to the Explorer.
- Its deterministic export contains the 106-node list, 180 directed edges,
  weights, all face incidences, seam classes, adjacency matrix, graph6
  serialization, ten automorphism permutations, expected metrics and a
  SHA-256 manifest.
- A separate union-find verifier reconstructs the quotient without importing
  the generator and currently passes all `177` checks. This is reproducibility
  infrastructure for the same PENT/SCC-003 object, not `PENT-08`.
- The frozen systematic prior-art audit identifies the six-sextant Pascal
  Hexagon as the strongest located baseline and Quint's two-copy infinite
  Pascal graph as the closest literal graph-joining baseline. No inspected
  source supplies the same five depth-six side-chain quotient. The result is
  explicitly coverage-limited and is not a worldwide novelty claim.

Formal Pascal–Rosetta Joint design:

- [`PASCAL_ROSETTA_JOINT_DESIGN_2026-10-11/`](PASCAL_ROSETTA_JOINT_DESIGN_2026-10-11/)
  defines an injective raw-incidence encoding into
  `C5_A x C5_B x C6_D x C12_Q` and verifies the two branch-dependent
  Pascal/gear intertwining equations.
- Its quotient joint is deliberately relational: the `106` quotient nodes
  retain `140` gear addresses with fibre profile `75x1 + 30x2 + 1x5`.
  Return to the quotient is exact, while a rotation-equivariant
  single-address selector fails at the fixed apex as expected.
- This is formal design validation for `A0-BL-023` / `A0-BL-051`, not an
  admitted run, `PENT-08`, new Family or claim promotion.

## Boundary

This establishes a finite binomial face complex with dihedral symmetry under
the declared gluing rule. It does not establish a new universal Pascal
algebra, a physical five-stage mechanism, a relation to the earlier trinomial
Pascal pyramid, or a reason that a separate four-layer interior must exist.
The screenshot's seven rows and central base value `20` are exact; the phrase
`four inner layers` still needs its own typed definition before it can become
part of this carrier.

