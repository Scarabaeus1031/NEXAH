# PENT-05 — Root completion of the Pascal pentagon lift

Date: `2026-10-10`

Status: `BOUNDED_CANDIDATE_EVIDENCE / NOT_ADMITTED`

## Question

Does the verified `D5 x C2` symmetry fixture from PENT-04 admit the standard
rank-three Coxeter root realization `H2 direct-sum A1`, with the pentagonal
bipyramid vertices embedded as a strict subset of its roots?

## Declared object

The equatorial plane contains ten unit vectors spaced by `36 degrees`:

```text
R_H2 = { (cos(-90° + 36° k), sin(-90° + 36° k), 0) | k = 0...9 }
```

The axial factor is

```text
R_A1 = { (0,0,+1), (0,0,-1) }.
```

Thus `R = R_H2 union R_A1` contains `12` roots. The five equatorial vertices
of PENT-04 are the even-indexed `H2` roots. Their five antipodes are the odd
indices; Zenith and Nadir are already the two `A1` roots. Root completion
therefore adds exactly five vectors without changing the seven-vertex carrier.

Choose simple roots `alpha_1`, `alpha_2`, `alpha_3` with angles `144 degrees`
between the first two and `90 degrees` to the axial root. Their reflections
must satisfy

```text
s_1^2 = s_2^2 = s_3^2 = e
(s_1 s_2)^5 = e
(s_1 s_3)^2 = (s_2 s_3)^2 = e.
```

## Result vocabulary

- `PASS`: the 12-vector set is reflection-closed, the generated action has
  order `20`, the Coxeter and Gram/Cartan checks hold, and the PENT-04 carrier
  embeds as declared;
- `FAIL`: at least one finite algebraic or geometric check fails;
- `UNDEFINED`: any semantic, physical, historical or crystallographic
  interpretation not specified by this contract.

Replay:

```sh
python3 run_test.py
```

## Accounting boundary for 80

The five equatorial Pascal midpoint nodes still carry weight `20` each. Four
non-identity turns therefore account for `4 x 20 = 80`; the complete five-node
orbit including the initial/return position accounts for `5 x 20 = 100`.
`80` is a transition-path subtotal, not the weight of a second inner pentagon.

## Claim boundary

`H2` is the standard non-crystallographic rank-two Coxeter root system, also
written `I2(5)`. This test does not establish a crystallographic Lie root
system, a new NEXAH Family, prime or resonance semantics, physical dynamics,
historical derivation, a universal Pascal solid or the phrase `four inner
layers`.
