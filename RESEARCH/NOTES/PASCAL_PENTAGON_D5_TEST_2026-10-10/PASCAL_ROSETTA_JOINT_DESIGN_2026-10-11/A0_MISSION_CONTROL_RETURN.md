# A0 / Mission Control return — Pascal–Rosetta Joint design

Date: `2026-10-11`  
Authority: `CORE SOURCE RETURN / NO STATUS PROMOTION`  
Source identity reused: `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`

## Bounded return

The formal design fixture now supplies the missing candidate map requested by
`A0-BL-023`:

```text
F(f,n,k) = (f, f+k mod 5, n mod 6, 2k-n mod 12).
```

It passes the two Pascal branch intertwining equations over all `210` frozen
face-edge incidences and preserves exact return to the `106`-node quotient as
a relation.

The quotient fibres are:

```text
75 interior nodes x 1 address
30 seam nodes     x 2 addresses
 1 apex node      x 5 addresses
                         = 140 addresses.
```

The expected single-state control fails: no rotation-equivariant selector can
choose one of the five apex addresses because the quotient apex is fixed while
its gear-address fibre is a free `C5` orbit.

Matched generic controls also separate the mechanism.  The prior locked and
counter-rotating Gear schedules match `0/210` Pascal incidences.  Collapsing
both branches to the left rule matches only the `105` left incidences; using
the right rule everywhere matches only the `105` right incidences.  The
branch-aware Pascal schedule alone matches `210/210`.

## Backlog disposition

### `A0-BL-023`

Recommended status remains `ADMISSION_REQUIRED`.

Preparation gained:

- typed domain, quotient and codomain;
- explicit candidate encoding;
- left/right intertwining equations;
- exact return relation;
- `D5` equivariance checks;
- a non-existence control for the single-state selector;
- information-loss controls for removing the `B` or `Q` coordinate.

What is not authorized here:

- activation of an existence Study;
- promotion from relational joint to canonical operator;
- generalization beyond the frozen depth-six object.

### `A0-BL-051`

Recommended status remains `PREPARE`.

The fixture can now serve as the formal Pascal-side adapter in a future
Generation Return Run Contract.  It does not supply that Run Contract,
Admission, frozen Return fixture or owner-approved execution by itself.

## Navigator disposition

```text
REUSE   A0OE:PASCAL_PENTAGON_D5_TEST
RELATE  A0-BL-023
RELATE  A0-BL-051
CREATE  none
```

Recommended relation type after governance admission:

```text
formal-design-candidate
```

The Navigator may expose the result only as source-bound preparation.  It may
not infer a new Study lifecycle, Family, `PENT-08`, publication state or claim
ceiling.

## Mission Control decision gate

One Human Owner decision is still required before scientific execution:

> Admit or decline the bounded question whether the verified relational
> Pascal–Rosetta Joint selects or constrains a Return fixture beyond matched
> generic gear controls.

Until then the Core package is clean formal infrastructure and the Science
Lab record remains non-active.

## D30 branch-word extension

The nested `D30_BRANCH_WORD_AUDIT_2026-10-11` package adds a complete frozen
word audit without changing that disposition. It verifies the exact phase
lift `p=2k-n mod 30`, the signed unit transitions `L:-1` and `R:+1`, all 127
words of length zero through six and all 635 face-word instances.

It also preserves three important limits:

- only 13 of 30 phases occur at frozen depth six;
- none of the 900 characters from the old `C5 x C5 x C6 x C12` gear to C30
  realizes the signed unit schedule;
- H3 is a separate 30-point carrier with Coxeter decomposition `10+10+10`,
  while an E8 lane/origin/orientation chart has 480 unselected candidates.

Therefore the D30 lift strengthens the formal adapter while supplying no
canonical H3/E8 identity and no reason to change `ADMISSION_REQUIRED` or
`PREPARE`.

The same audit now exposes the existing five face addresses as the register
view `D1..D5 x C30`. Each register has 28 frozen incidences, 127 branch words
and 13 observed phases. The full cover has 150 positions, of which 65 are
occupied at depth six. `D1..D5` are address registers; `D5` remains separately
the dihedral group name. No new operator or identity is created.

The source-bound `PASCAL_PENTAGON_EXPLORER.html` now includes this as a `D30
joint` interaction inside PENT-07. The view permits bounded `L/R` words,
register rotation and reflection while displaying the partial phase path. It
is interface integration over the frozen audit only: no new replay, evidence
class, Study, relation or PENT identity is introduced.

## NCS-292 dual-axis / Q106 bridge audit

The nested `NCS_292_DUAL_AXIS_Q106_BRIDGE_AUDIT_2026-10-11` package reuses the
same identity and freezes the historical NCS four-point source against the
owner-supplied adjacent-axis, transition-gap and Root Cube comparators.

The declared finite candidate

```text
C5 x P4 x C2_J = 40 states -> 20 horizontal-gluing classes
```

compiles exactly. The prime-index and cut controls also separate correctly:
`P25=97`, `P26=101`, `P27=103`; the two midpoints are `99` and `100`; and
`103+3=106=2*53`, while `53^2=2809`.

The result is deliberately bounded. No typed map currently identifies the
four animated NCS points with the four package roles, no node/edge map sends
the twenty quotient classes to Q106, and the visually declared fifteen Root
Cube nodes remain a comparator count. Classification is therefore
`COMPILED_40_TO_20_CANDIDATE_OPEN_INTERTWINERS`, not a recovered NCS operator,
Q106 derivation, new Study or `PENT-08`.

## NCS-292 / Q106 intertwiner and return package

The nested `NCS_292_Q106_INTERTWINER_RETURN_PACKAGE_2026-10-11` package carries
the bridge audit through five bounded modules and passes `25/25` deterministic
checks.

The historical NCS source now has a precise operator reading: it applies one
common XY translation to all four points, preserves their labels and pairwise
distances, and contains no package permutation. The frozen Q106 D5 action has
orbit profile `1^1 · 5^9 · 10^6`. Exhaustive search over all orbit unions finds
one unique connected pure-five-orbit interface at size 15 and one at size 20;
there is no connected eight-five-orbit interface at size 40.

Q106 also contains exactly one connected invariant six-node residual — apex
plus first seam ring — with a connected invariant 100-node complement. This
makes `106=100+6` a graph-typed cut. It does not yet define five 20-node blocks
or an `ABC x {+,-}` node labeling.

Both candidate Janus laws compile: `Jr=rJ` for the commuting sheet flip and
`JrJ=r^-1` for the dihedral reflection. The source does not select one. The
seam walk returns to the same 20-class quotient after one turn and to the exact
40-state address after two turns.

Mission Control disposition stays `PREPARE / ADMISSION_REQUIRED`. Reuse
`A0OE:PASCAL_PENTAGON_D5_TEST`; create no new identity, Study or `PENT-08`.
The next honest research question is the still-missing adjacency-preserving
`X20 -> Q106` intertwiner or a proof that none exists under the declared
carrier adjacency.

## Q106 prime-index / radix-mirror / root-growth audit

The nested
`NCS_292_Q106_INTERTWINER_RETURN_PACKAGE_2026-10-11/Q106_PRIME_INDEX_RADIX_ROOT_GROWTH_AUDIT_2026-10-11`
subtest passes `28/28` deterministic checks and binds the new 2–3–5 proposal
to the frozen Q106 carrier without creating a new identity.

The cumulative level counts are exactly

```text
Q_m = 1 + 5 T_m = 1, 6, 16, 31, 51, 76, 106.
```

Their second difference is constantly `+5`; the residual sequence
`106-Q_m = 105,100,90,75,55,30,0` has second difference `-5`. Therefore
forward growth is discretely convex and the residual room discretely
concave. Parity is a separate observable with pattern
`odd,even,even,odd,odd,even,even`.

The `2–3–5` seed has bounded exact content: `2+3=5` supplies the coefficient,
`2*3=6=Q_1`, and `Q_2=16=2^4`. The expression `2/3=0.666...` is a rational
identity, not the integer 6. `2^3=8` remains an external comparator because
8 is absent from the Q-sequence.

The frozen D5 action has orbit profile `1^1 · 5^9 · 10^6`. With `O=16`
orbits, `F=9` five-orbits and `L=25` final-level interior nodes, the exact
prime-index joint is

```text
O+F=L,  p_16=53,  p_25=97,
106=2*p_16,  106-F=p_25,  53+97=150.
```

There are nine prime-index steps from 16 to 25 and eight primes strictly
between the endpoints. A negative boundary is equally exact: no union of
the D5 orbits has size 53, since invariant sizes are `0` or `1 mod 5`, while
`53 mod 5 = 3`.

Euclidean coordinates `(floor(n/b), n mod b)` verify that 53 and 97 retain
columns 13 and 17 under Base 20 -> Base 40 while their rows halve; 106 does
not retain its column. The declared Base-50 involution `J_50(x)=150-x`
exchanges 53 and 97 and fixes 75. This is a coordinate construction, not a
Q106 automorphism.

Mission Control / NN / A0 disposition remains `PREPARE / ADMISSION_REQUIRED`:
reuse `A0OE:PASCAL_PENTAGON_D5_TEST`, create nothing, and expose the audit
only as source-bound formal evidence. The established growth is quadratic;
a fractal remains `NOT_ESTABLISHED` until a recursive substitution and scale
law are supplied.

## Leo/Lilith · 3:2 · square-index prime ladder

The nested
`Q106_PRIME_INDEX_RADIX_ROOT_GROWTH_AUDIT_2026-10-11/LEO_LILITH_3_2_ROOT_PAIR_CONNECTOR_AUDIT_2026-10-11`
follow-up passes `39/39` deterministic checks. It also adds documentary
archaeology without changing the existing identity or claim ceiling.

The strongest new exact object is the consecutive-square prime-index ladder:

```text
roots:          1   2   3   4   5
square indices: 1   4   9  16  25
prime values:   2   7  23  53  97
adjacent sums:    9  30  76 150
```

The sums bind in order to the frozen Q106 joint: `F=9` five-node orbits, the
outer level size `30`, `Q_5=76`, and the `53+97=150` mirror closure. The edge
between roots 2 and 3 has directed ratio `3:2`, square indices `4 -> 9`, prime
values `7 -> 23` and sum `30`.

Archaeology confirms that `3/2` appears literally in the historical
`v13.13 Lilith-Gegenrotation` executable, paired there with `4/3`. The earlier
operator addendum independently records `3/2 <-> 2/3` as reciprocal readings
under reversal. A separate `Lilith-Edge` source uses `3/4`, and the historical
`Lilith/Leo Clamps` source contains both observer labels but no ratio law.

Therefore the result supports a **historical Lilith-side 3:2 marker** plus an
**arithmetic observer-joint candidate**. It does not recover
`Leo:Lilith=3:2`, a Leo-side `2/3` source term, or a typed Leo/Lilith return
operator. The proposed lift `Lambda(2,3)=(2^2,2+3)=(4,5)` is explicitly new.

Across the declared control range `r=1..100`, `r=4` is uniquely the adjacent
square-index pair that simultaneously sums to 150, has decimal suffixes
`53 -> 97`, and satisfies `4*5=20`, equal to the prime-index gap from 97 to
the next prime ending in 97 (`197`, index `45`).

Mission Control / NN / A0 remains `PREPARE / ADMISSION_REQUIRED`. Reuse
`A0OE:PASCAL_PENTAGON_D5_TEST`; create no new identity or canonical relation.

### 432 record/play extension

The supplied ring view extends exactly by `1440`:

```text
540,720,1080,1440 = 180 * (3,4,6,8)
10 * 432/d         =       (8,6,4,3)
```

Thus the track is governed by the finite involution `k -> 24/k`, with
`3 <-> 8` and `4 <-> 6`. The added term obeys
`1440=2*720=12^2*(2*5)`. Existing yellow/blue/purple assignments remain
display metadata; the returned `3` receives no inferred color.

### Navigator / ILAU return

The supplied HTML sequence is already present in NN as the nineteen-file
internal route `#ilau-orientation`, binder
`NEXAH:NAVIGATOR:ILAU_ORIENTATION_INSTRUMENTS:V1:2026-10-09`. Reuse its
existing instruments, especially `ILAU:RECORD_PLAY_432`,
`ILAU:BPS_MS_COVER_CUT_KERNEL_GAP` and `ILAU:FROM_GAP_TO_RETURN`; do not create
a duplicate series identity.

The binder integrity audit passes `63/63`. This verifies custody, hashes and
route boundaries. It is not the still-open operational work: the source intake
records `RC-01` and `NBV-01` as proposed but not executed and leaves BPS–MS at
`COHERENT_OPERATIONAL_EXTENSION_TEST_REQUIRED`. The present `39/39` arithmetic
audit therefore supplies a bounded Record/Play note, not a BPS–MS validation.

### Q432 and loose visual-source return

The additional poster supplies the exact involution `Q_432(x)=432/x`, hence
`Q_432^2=id` for every nonzero input. Its `400/420/432` factor track, the
`432/pi` and `432/sqrt(2)` coordinates, and the approximately
`0.002106781 degrees` golden-angle difference replay. Standard `phi` instead
gives `432/phi=266.990683...`, so the displayed `267.0031` is retained as a
failed numerical label, not silently normalized.

The MIAU visual has a real but provisional Navigator custody source:
`ART:HTML:0A614C567C41`, the frozen `NEXAH_MIAU_VOWEL_SOURCE_FILTER_TEST.html`.
It contains the `i`-formant tuple `(270,2290,3010)`; `2290+3010=5300` and
`5300/270=19.629629...` reproduce the dial. Registry status remains
historical/provisional, low-confidence and `UNASSESSED`. No governed source
match was recovered for WUFF or the rendered Q432 poster, and no new NN
relation is created.

### A0 Record / Crystal / Rooms architecture

The larger supplied image family belongs around the already frozen A0 Book
sequence, not inside a new mechanism identity:

```text
Record / Play -> Crystal View -> Rooms of the Machine -> Human Gate
```

Record/Play is the bounded source-cut-record-replay opening; Crystal View is
the Chapter-06 illustration of conditioned appearance; Rooms of the Machine
is the Chapter-08 closing atlas. The A0 manifest explicitly marks the two GLBs
as illustrative rather than scientific evidence, universal projection law or
physical mechanism. Canon/Echo/Shadow/Reveal, OIL/RIS, Pearl/Matroshka,
Relation Loom, scale/tonearm, Storm in Glass and the B&W cylinder are therefore
recorded as compatible explanatory panels around the same comparison grammar,
not as proof that all panels describe one machine.

### Pascal × Quaternion Return Switchyard design

The recommended next build reuses `A0OE:PASCAL_QUATERNION_TEST` and extends
its existing HTML as a supporting view. No new module or Navigator route is
needed. The introduced connector is

```text
Phi(a,b,c)=(a+b+c)*1+a*i+b*j+c*k.
```

It makes all four quaternion basis channels explicit while keeping the scalar
component tied to Pascal depth. Conjugation by
`u=(1+i+j+k)/2` realizes the already verified `C3` axis cycle, preserves the
weighted recurrence carrier and fixes the scalar layer. `Q°` remains the
fifth control position, not a fifth quaternion component.

The proposed HTML separates quaternion inverse-conjugation return from the
scalar `Q_432` Record/Play involution and carries forward the IJQ-01 negative
controls. During structure freeze this remains formal design; execution or NN
promotion requires a separate admission/reopen decision and Run Contract.

### Pascal × Quaternion Return Switchyard built return

The permitted non-evidentiary prototype is now stored under the existing
`A0OE:PASCAL_QUATERNION_TEST` source package:

- `PASCAL_QUATERNION_RETURN_SWITCHYARD.html` — interactive supporting view;
- `PASCAL_QUATERNION_RETURN_SWITCHYARD_BINDING.json` — identity, route and
  claim-boundary return record.

The return reuses the existing A0 evidence lens, `ILAU:RECORD_PLAY_432`, the
two already registered Q° HTML surfaces and the Pascal/quaternion carrier
relations. Mission Control may expose the file through its read-only Source
Field, while the Science Navigator continues to expose it through the existing
`A0OE:PASCAL_QUATERNION_TEST` source record. No new Study, module, Family,
route, canonical relation count or publication state is created. The HTML is
an instrument projection, not execution of a new `T1..T10` Lab run.
