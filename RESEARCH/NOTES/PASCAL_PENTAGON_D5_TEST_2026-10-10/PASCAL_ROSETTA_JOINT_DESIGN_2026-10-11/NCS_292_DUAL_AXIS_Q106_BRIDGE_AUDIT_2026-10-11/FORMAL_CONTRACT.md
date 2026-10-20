# NCS-292 dual-axis / Q106 bridge audit — formal contract

Date: `2026-10-11`  
Status: `FORMAL_DESIGN_VALIDATION_NOT_ADMITTED_NOT_PENT_08`

## Reused identity

This audit extends `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`. It creates no
new Navigator identity, Study, canonical operator, Family or eighth Pascal
test.

## Question

Can four recurrent source motifs be joined by explicit typed maps?

1. the historical `292 NCS Switch`, which visibly moves four points;
2. the adjacent cuts `97 <-> 101` about `99` and `97 <-> 103` about `100`;
3. a declared `C5 x P4 x C2_J` two-layer package carrier;
4. the independently verified 106-node SCC-003 quotient.

## Exact controls

The verifier must establish:

```text
292 is palindromic
2 + 9 = 9 + 2 = 11
29 = P10
P23..P27 = 83, 89, 97, 101, 103
97 <-> 101 has midpoint 99
97 <-> 103 has midpoint 100
right endpoint shift = 2
midpoint shift = 1
97 + 4 = 101
97 + 3 = 100
103 + 3 = 106
106 = 2 * 53 != 53^2
```

`Exit (26)` is therefore read first as the prime index `P26=101`. It is not
silently rewritten as the number `106`.

## Candidate carrier

Let

```text
X40 = C5 x P4 x C2_J,
P4  = {carrier, frame_cut, transform_view, return_record}.
```

The free horizontal layer swap identifies

```text
(s,p,A) ~ (s,p,B).
```

The quotient has twenty classes, each with fibre size two. This proves only
that the proposed `40 -> 20` construction compiles.

## Required intertwiners

Mechanism identity requires all of the following maps:

1. a permutation/action from the historical four NCS points to the four typed
   package roles;
2. a node map from the twenty quotient classes into or onto Q106;
3. declared preservation requirements for Q106 edges, weights and D5 action.

The 15 primary nodes depicted for Root Cube v15 remain a comparator count.
They are not inserted into `X40` and do not repair a missing map.

## Classification

- all maps compile: `COMPILED_WITH_TYPED_INTERTWINERS`;
- the finite quotient compiles but required maps are absent:
  `COMPILED_40_TO_20_CANDIDATE_OPEN_INTERTWINERS`;
- only number equalities survive: `ARITHMETIC_ONLY`;
- a frozen input or exact control fails: `CONTRACT_INVALID`.

The audit stops at classification.
