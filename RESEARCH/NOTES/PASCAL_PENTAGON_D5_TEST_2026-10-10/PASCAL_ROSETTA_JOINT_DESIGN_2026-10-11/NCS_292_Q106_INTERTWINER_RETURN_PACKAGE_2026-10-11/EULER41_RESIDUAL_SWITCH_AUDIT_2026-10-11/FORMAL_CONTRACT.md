# Euler-41 / Q106 Residual Switch — Formal Contract

## Scope and identity

This is an owner-authorized formal-design extension of
`A0OE:PASCAL_PENTAGON_D5_TEST`, bound to `A0-BL-023` and the existing
NCS-292/Q106 package. It creates no Study, Run, evidence identity, Navigator
identity or `PENT-08`.

## C1 — the exact 29/41 bridge

Let `p_k` denote the `k`th prime. Then

```text
p_10 = 29
p_13 = 41
41 = 32_base13
reverse_base13(32) = 23_base13 = 29
```

The last line is a radix-13 representation operator. It is not a
base-independent identity between 29 and 41. In base 16, `41=29_base16`; that
glyph coincidence is a different representation fact and must not be merged
with the base-13 reversal.

For Euler's polynomial in MRB-04,

```text
E_minus(n) = n^2 - n + 41 = E_plus(n-1)
```

the values are prime for `n=1..40`; at `n=41`, with shifted index `u=40`, the
value is `41^2=1681`. This is the exact `40 -> +1 -> 41` boundary used here.

## C2 — the +1 controller is external

The parent carrier is

```text
X40 = C5 x P4 x C2_J.
```

The owner-declared controller extension is the disjoint union

```text
X41+ = X40 disjoint-union {q}.
```

Thus `|X41+|=41`, while `q` is not a forty-first payload state of `X40`. It is
a typed control channel. Any action selected by `q` must still be declared;
cardinality alone supplies no switching law.

## C3 — canonical residual readout

The unique connected D5-invariant six-node residual in Q106 is

```text
R6 = {A} disjoint-union {S_01_00,...,S_01_04}.
```

Its D5 orbit decomposition is `1+5`. Therefore the orbit-class map

```text
rho(A)=0
rho(S_01_j)=1
```

is canonical relative to the frozen D5 action: it is surjective and D5
invariant. This gives a valid binary residual readout, naturally interpretable
as `off/on`.

## C4 — why the seam remains open

The intrinsic seam audit proves `dim H1=0`. A Möbius seam appears only after
releasing an added diamond orbit, and six D5-compatible size-10 choices remain.
Each choice is itself D5 invariant, so the six-choice set carries the trivial
D5 action.

No D5-equivariant bijection exists from `R6` to that six-choice set: five
nodes of `R6` are moved transitively while all six seam choices are fixed as
whole orbits. Hence `rho` can say **seam channel off/on**, but it cannot say
**which seam**. It also does not select `Jc` versus `Jd`.

## C5 — thirteen-step stair and Fibonacci rail

The prime-index stair has thirteen positions and terminates at `p_13=41`.
The Fibonacci rail can be indexed by the first thirteen Fibonacci weights.
The source-bound Fibonacci matrix still satisfies

```text
Q^5 = [[8,5],[5,3]],  det(Q^5)=-1.
```

This supports an orientation-reversing comparator, not an intrinsic Möbius
proof or a Pascal/Fibonacci conjugacy. The blue rail and green-yellow stair are
owner-declared display semantics. LIFE06B is a related predecessor with ten
prime shells and a different existing palette; it is not silently rewritten.

## C6 — the two 34 plates are a negative control

Both the Dürer and Khajuraho 4x4 placements have magic sum 34 and realize Q4
bit complement, but their spatial operators differ:

```text
Dürer:     P(C(v)) = R180(P(v))
Khajuraho: P(C(v)) = T(2,2)(P(v)) on the torus
```

Equal scalar invariant does not identify the placement operator. This is the
appropriate control for the NCS switch: a shared output signature cannot by
itself choose a mechanism.

## C7 — two exact ingress routes meet at 29

MRB-08 contains two distinct dyadic families:

```text
M_k(5) = 2^k * 5, including 10 -> 20 -> 40
M_k(7) = 2^k * 7, including 14 -> 28 -> 56.
```

The external-controller grammar can be instantiated at 28 and at 40:

```text
E28 = X28 disjoint-union {q29},  |E28|=29
E40 = X40 disjoint-union {q41},  |E40|=41.
```

Together with C1, two routes meet at the integer 29:

```text
E28 -> 29
E40 -> 41 ->[reverse digits in base 13]-> 29.
```

They share a terminal value, not a carrier identity. `X28`, `X40`, the two
controller states and the representation operator remain distinct.

## C8 — 29 enters C30 as an address

The Pascal–Lissajous audit verifies `C30 ~= C6 x C5`. Define only

```text
iota(29) = [29]_30
tau([t]_30) = [t+1]_30
pi6([t]_30) = [t]_6.
```

Then `tau([29]_30)=[0]_30`. The projection `pi6` is surjective with six
fibres of size five. C30 is therefore a valid six-address phase bus. This is
not a proof that “29 becomes 30,” and C30 is not part of the dyadic 10/20/40
carrier family.

Let `S6` be the six compatible Q106 seam orbits. Every bijection
`beta:C6->S6` would compile

```text
sigma(rho,t) = OFF                 if rho=0
               beta(pi6(t))       if rho=1.
```

There are `6! = 720` such bijections and the sources distinguish none. The
enable line and address bus are typed; the pin assignment `beta` remains open.
The common period `lcm(10,20,30,40)=120` is a synchronization cover only.

## C9 — exact 41-by-20 gap joint

The supplied process cards display an independently checkable identity:

```text
206^2 - 204^2
= (206-204)(206+204)
= 2 * 410
= 820
= 41 * 20.
```

This is an exact multiplicative joint between the Euler-41 boundary and a
20-factor. It does not identify a 41-degree arc with a 20-degree arc or
establish “Euclid Echo,” torsion, resonance, Tessarec, octave or physical
interpretations.

## C10 — visual source role

The process, vigesimal, Cheops and Rootroom plates are hash-bound in
`VISUAL_SOURCE_LEDGER.md`. They locate the intended controller/clock/gate
grammar. They do not establish `beta`, an intrinsic Möbius seam, physical
causation or a cross-domain law.

## C11 — exact base-20 layer/ring/point decoder

For every nonnegative integer `n`, define its first three base-20 digits by

```text
z = floor(n/400)
y = floor((n mod 400)/20)
x = n mod 20
n = 400z + 20y + x,       0 <= x,y < 20.
```

This is an exact positional decoder. The recovered Thread-V view then applies
the separate display projection

```text
P20(z,y,x) = (x + y/2, z).
```

The five displayed samples replay exactly:

| n | `(z,y,x)_20` | `P20(n)` |
|---:|---:|---:|
| 1729 | `(4,6,9)` | `(12,4)` |
| 417 | `(1,0,17)` | `(17,1)` |
| 1836 | `(4,11,16)` | `(21.5,4)` |
| 378 | `(0,18,18)` | `(27,0)` |
| 718 | `(1,15,18)` | `(25.5,1)` |

`P20` is lossy: for example `(z,0,1)` and `(z,2,0)` both project to
`(1,z)`. Therefore the original digit tuple must remain the state; the plotted
horizontal coordinate is only a visualization. The source title calls the
view a spiral, but the recovered formula establishes a two-dimensional affine
projection of base-20 digits, not a three-dimensional spiral or transport law.

The separate 15-step frame family is an arithmetic progression
`1+15k` (including `1,16,31,...,121`). It is retained as a source-bound index
pattern only. Odd-eighth axes satisfy `(j/8)*360 = 45j` degrees, so the shown
`3/8` axis is exactly 135 degrees. These elementary identities do not validate
the displayed energy, drift, planetary or resonance interpretations.

## C12 — “vendissimal” is a source-level namespace collision

The recovered sources use the same word for two different objects:

```text
V5  = {-2,-1,0,+1,+2}       (five-state alphabet in UCRT_TRINARY_CODE)
C20 = integers modulo 20     (base-20 address/radix family)
```

They have cardinalities 5 and 20 and are not identified. A map between them
must be declared explicitly. This audit uses **five-state** for `V5` and
**base-20/vigesimal** for `C20` and the positional decoder. The shared legacy
label “vendissimal” supplies lineage only, not an isomorphism.

## Verdict rule

Return `PASS_EXACT_CONTROLLER_ARCHITECTURE_WITH_OPEN_SEAM_BINDING` exactly
when the prime/index/radix boundary, external `40+1` controller, D5-invariant
binary residual quotient, seam-selection obstruction, Fibonacci comparator,
dual-34 control, dual ingress, C30 quotient, 41-by-20 gap identity, exact
base-20 decoder, source-namespace separation and selector non-uniqueness all
replay. A canonical Möbius switch is established only after a source-bound
`beta` and Janus law are supplied.
