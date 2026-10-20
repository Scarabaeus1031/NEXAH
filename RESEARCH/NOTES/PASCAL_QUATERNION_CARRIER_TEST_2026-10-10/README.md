# Pascal–Quaternion carrier/operator test

Date: `2026-10-10`

Status: `BOUNDED_CANDIDATE_EVIDENCE / NOT_ADMITTED / NO_ACTIVATION`

## Question

Which quaternion rotations preserve the finite trinomial Pascal carrier

```text
P_N = {(i,j,k) in Z^3_{≥0} : i+j+k ≤ N}
```

as a discrete weighted recurrence graph, rather than merely rotating its
Euclidean rendering?

The weight at a node is

```text
w(i,j,k) = (i+j+k)! / (i! j! k!).
```

## Test contract

The executable checks depths `N=0..11`.

1. All six coordinate permutations are tested for preservation of the finite
   carrier, multinomial weights and parent→child recurrence edges.
2. Their determinant separates proper rotations (`SO(3)`) from reflections.
3. The two non-identity cyclic permutations are represented by the unit
   quaternions for `120°` and `240°` about `(1,1,1)`.
4. A `37°` rotation about `(1,2,3)` is the negative control: it preserves a
   view with attached node data but must fail discrete lattice membership.

Replay:

```sh
python3 run_test.py
```

The expected machine-readable result is stored in `RESULT.json`.

## Result

```text
full coordinate-permutation symmetry:  S3  (6 elements)
quaternion-realizable proper subgroup: C3  (3 elements)
generic quaternion rotation:           not a lattice automorphism
```

All declared checks pass for `N=0..11`.

The distinction is structural:

- every coordinate permutation preserves the symmetric multinomial formula
  and the recurrence graph;
- only the even permutations have determinant `+1` and are spatial rotations;
- therefore the quaternion-realizable discrete carrier automorphisms found by
  this test are exactly the cyclic axis permutations `C3 = {e,(ijk),(ikj)}`;
- a generic unit quaternion remains a valid view/orientation operator, but it
  moves the nodes away from the integer simplex lattice.

## Claim ceiling

This is an exact finite carrier/automorphism fixture under the declared
embedding. It does **not** establish that quaternion multiplication generates
Pascal coefficients, that the Pascal carrier is quaternion algebra, or that a
physical mechanism is present. It does not modify the closed result of the
existing trinomial Pascal package or the conditional Root/sign→Quaternion→Hopf
bridge.

## Existing identities reused

- `ART:NUMBER:PRIMEGRID_BLOCK02B_TRINARY_ANTIPODE` — finite trinomial Pascal
  carrier and multiplicity boundary;
- `NEXAH_PCA_PHASE_SPACE_CORE_2026_10_03` — separately typed quaternion/Hopf
  bridge candidate;
- `A0OE:T1_T7` — transformation-control context.

The relation is `RELATED_BY_BOUNDED_OPERATOR_TEST`, explicitly not identity.

## Supporting Return Switchyard

The interactive
[`Pascal × Quaternion Return Switchyard`](PASCAL_QUATERNION_RETURN_SWITCHYARD.html)
is now stored beside this controlling replay rather than as a separate module.
It introduces the explicit display embedding

```text
Phi(a,b,c) = (a+b+c)*1 + a*i + b*j + c*k
```

and lets the reader compare the already verified `C3` axis cycle, an `S3`
reflection and a generic quaternion view control. The same surface keeps the
scalar Record/Play involution `Q_432(x)=432/x` in a separate lane.

The surface is a **non-evidentiary supporting projection**. It reuses this
test's identity, `ART:A0:MATHEMATICAL_JOINTS`, `A0OE:T1_T7` and
`ILAU:RECORD_PLAY_432`; it creates no Study, module, Family, canonical route or
fifth quaternion component. The introduced `Phi` map is a formal design, not
recovered historical intent. The exact return checks displayed by the HTML do
not replace `run_test.py` or constitute a new Science Lab run.

Machine-readable custody and return boundaries are recorded in
[`PASCAL_QUATERNION_RETURN_SWITCHYARD_BINDING.json`](PASCAL_QUATERNION_RETURN_SWITCHYARD_BINDING.json).

## Tested successor — A0-BL-052

On `2026-10-11` the Human Owner opened one bounded Science Lab cycle to test
the switchyard's explicit connector rather than treating the HTML as evidence.
`A0_BL_052_PASCAL_QUATERNION_FOUR_CHANNEL_RETURN_2026_10_11` froze T1–T10,
executed one Primary and one byte-identical Replay and passed the repaired
independent verifier.

The retained result is `EXACT_FOUR_CHANNEL_CONNECTOR_PASS`: `Phi` is injective
and `C3`-equivariant on `P_0..P_11`, and inverse quaternion conjugation returns
exactly. The reflection, generic-view, `Q°`, scalar `Q_432`, `4²/5²` and prime
readout boundaries also pass. The result is registered as candidate finding
`F-A0-12`. The Human Owner accepted the bounded result and closed the Study on
`2026-10-11`. The HTML remains a supporting projection; the Science Lab result
controls the tested claim. Independent review, paper use and publication remain
separate gates.

