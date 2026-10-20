# NCS-292 / Q106 intertwiner and return package — formal contract

Date: `2026-10-11`  
Identity: `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`  
Class: formal design validation; not an admitted Study; not `PENT-08`

## Question

Which structures in the NCS animation, the frozen `Q106` Pascal quotient, the
candidate `40 -> 20` carrier and the Janus/Möbius return can be recovered as
typed finite mechanisms rather than inferred from recurring numbers?

## M1 — recovered NCS operator

For the four historical pink points the source implements

```text
T_d(x,y,z) = (x+d, y+d, z)
d(frame) = 0.8 * 0.28 * sin(0.16 frame).
```

The same `d` is applied to every point. Point labels and all pairwise distances
are preserved. No permutation of the four points, package transition or Janus
sheet action is present in that source.

## M2 — Q106 interface search

Let `G=D5` act through the ten frozen permutations in
`automorphisms.json`. A candidate interface must be a union of full `G`-orbits.
The search is exhaustive over all `2^16` orbit unions and checks connectivity
in the undirected support of the 180 directed Q106 edges.

The orbit profile is

```text
1^1 · 5^9 · 10^6 = 106.
```

The carrier comparators have the D5-set profiles

```text
RootCube15 comparator : 5 + 5 + 5
X20 quotient          : 5 + 5 + 5 + 5
X40 unfolded carrier  : eight 5-orbits.
```

Existence and connectivity are necessary, not sufficient, for an intertwiner.
An actual map must still preserve the declared adjacency and operator action.

## M3 — residual

The arithmetic split

```text
106 = 100 + 6 = 5*20 + 3*2
```

is tested in two stages. Q106 contains exactly one connected D5-invariant
six-node set: the apex and first seam ring. Its 100-node complement is also
connected and D5-invariant. This validates a typed `6 + 100` graph cut.

It does **not** validate five 20-node blocks, nor a bijection between the six
nodes and `ABC x {+,-}`. Those two maps remain open.

## M4 — Janus and return

On `X40=C5 x P4 x C2` with

```text
r(s,p,e)=(s+1 mod 5,p,e)
```

two candidate involutions compile:

```text
Jc(s,p,e)=( s,p,1-e)  with Jc r = r Jc
Jd(s,p,e)=(-s,p,1-e)  with Jd r Jd = r^-1.
```

The existing sources do not select between them. A seam walk that flips the
layer at the `4 -> 0` crossing returns to the same quotient class after one
turn and to the exact state after two turns.

## M6 — exact base-20 state decoder D20

For every tested non-negative integer, define

```text
D20(n)=(z,y,x),  n=400z+20y+x,  0<=x,y<20.
```

The verifier independently decodes and reconstructs the five recovered source
samples. This stage is exact and state-bearing.

## M7 — lossy display projection P20

The historical spiral-map coordinate is typed separately:

```text
P20(z,y,x)=(x+y/2,z).
```

It reproduces the five displayed coordinates but cannot be inverted. For
example, `(0,0,1)` and `(0,2,0)` both map to `(1,0)`. That collision is the
expected loss profile of a view, not a failure of D20.

## M8 — namespace boundary

The recovered materials use one legacy word for two different carriers:

```text
V5  = {-2,-1,0,+1,+2}
C20 = Z/20Z.
```

Their cardinalities differ and no typed map between them has been supplied.
The test therefore forbids silent identification.

## M9 — C30-to-C6 address bus

Define `pi6(k)=k mod 6` on `C30`. Its fibre profile is

```text
5,5,5,5,5,5
```

and the phase successor closes `29 -> 0`. This validates a six-address bus.
An address is not a seam choice and does not supply the missing intertwiner.

## M10 — β/Janus stop gate

Six residual labels can be bijected with six compatible seam choices in
`6!=720` ways. No source selects one β. Independently, both `Jc` and `Jd`
compile, but no source selects a historical Janus law. The correct terminal
state is therefore `OPEN`, not failure and not closure.

## M11 — Fibonacci Q5/Q10 rail

Reuse the closed `A0-BL-045` finite audit with

```text
Q   = [[1,1],[1,0]]
Q^5 = [[8,5],[5,3]],  det(Q^5)=-1, tr(Q^5)=11
Q^10=[[89,55],[55,34]].
```

The parent verifier recomputes these matrices and compares them with the
hash-bound Primary results. The same `Q^5` occurs for untwisted and twisted
strip quotients although they have respectively two and one boundary
components. Therefore `det(Q^5)=-1` does not select Möbius topology, and
`Q^10` is not an identity return.

For the explicitly declared signed reciprocal bridge, the `+` operator squares
to `+I`; the `-` operator squares to `-I` and reaches `+I` after four
applications. The inverse leg and sign are supplied data. No map transports
Fibonacci states into D20, C20, X20, X40 or Q106.

## Failure localization

| Stage | Passing observation | Localized non-pass meaning |
|---|---|---|
| D20 | exact round trip | decoder/source mismatch |
| P20 | collision reproduced | `INFORMATION_LOST_AS_EXPECTED` |
| V5 / C20 | types remain separate | contract-invalid namespace conflation |
| C30 -> C6 | six fibres of five, `29->0` | address-bus mismatch |
| β / Janus | 720 candidates, no selection | `OPEN` binding/selection seam |
| Fibonacci rail | exact Q5/Q10 and signed-return controls | transport remains `OPEN`; determinant cannot select topology |

## Decision boundary

The package may report the recovered translation, invariant interfaces,
`6+100` cut, exact D20 decoder, lossy P20 view, separated namespaces,
C30-to-C6 address bus and two algebraically valid Janus hypotheses. It must
stop before claiming that P20 is invertible, that V5 equals C20, that a C6
address selects a seam, that `det(Q^5)=-1` selects Möbius topology, that the
Fibonacci rail supplies a state map or transport to D20/C20/X20/X40/Q106,
that β is canonical, that a historical package
permutation or `X20 -> Q106` graph intertwiner exists, that five 20-node blocks
or an ABC node labeling have been recovered, or that one Janus law is uniquely
selected.

