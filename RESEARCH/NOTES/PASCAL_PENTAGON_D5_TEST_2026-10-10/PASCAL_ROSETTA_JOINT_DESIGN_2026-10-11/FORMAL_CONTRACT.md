# Pascal–Rosetta Joint formal contract

Status: `FORMAL_DESIGN_VALIDATION / NON-EXECUTED-SCIENCE BOUNDARY`

## 1. Source carrier

Let `X=C5 x T6` be the `140` raw face-incidence positions of the frozen
SCC-003 reference object.  Let

```text
pi:X -> Q106
```

be its already-defined seam-and-apex quotient map.  `Q106` is the existing
weighted directed five-face Pascal quotient; this document does not define a
new graph.

## 2. Gear carrier

Let

```text
G = C5_A x C5_B x C6_D x C12_Q.
```

For `x=(f,n,k)` in `X`, define

```text
F(x) = (f, f+k mod 5, n mod 6, 2k-n mod 12).
```

Interpretation is deliberately limited:

- `A` retains the Pascal face address;
- `B` is the face-plus-within-row address;
- `D` is the depth clock;
- `Q` is the centered envelope coordinate.

No physical gear, energy, resonance or calendar identity is asserted.

## 3. Pascal-induced transitions

The raw Pascal incidence graph has two branch maps where defined:

```text
tL(f,n,k) = (f,n+1,k)
tR(f,n,k) = (f,n+1,k+1).
```

Define on `G`:

```text
TL(a,b,d,q) = (a,b,  d+1,q-1)
TR(a,b,d,q) = (a,b+1,d+1,q+1).
```

All gear coordinates are reduced in their declared cyclic carrier.  The two
intertwining equations are

```text
F o tL = TL o F
F o tR = TR o F.
```

These equations, rather than the mere factors `5,5,6,12`, are the proposed
Pascal Joint.

## 4. Quotient relation and return

Because `F` is not constant on the fibres of `pi`, it does not descend to a
single-valued map `Q106 -> G`.  Define instead

```text
J(v) = {F(x) | pi(x)=v}.
```

Since `F` is injective on `X`, define the return on its image by

```text
rho(F(x)) = pi(x).
```

Then every address in every relation fibre returns exactly:

```text
rho(g)=v for all g in J(v).
```

The return reconstructs the quotient node, not the unique raw face incidence
after the quotient provenance has been discarded.

## 5. Symmetry

The existing raw actions are

```text
r(f,n,k) = (f+1,n,k)
m(f,n,k) = (-f,n,n-k).
```

Because `F` is injective, these induce permutations on `image(F)`.  The
relation is equivariant as a set-valued map:

```text
J(r v) = rG J(v)
J(m v) = mG J(v).
```

There is no `C5`-equivariant selector choosing one member of every `J(v)`:
the apex is rotation-fixed in `Q106`, while its five addresses have no
rotation-fixed point.

## 6. Controls

The validator must preserve the following outcomes:

1. exact `140 -> 140` injective raw encoding;
2. exact left and right intertwining equations on all `210` face-edge
   incidences;
3. quotient fibre profile `75x1 + 30x2 + 1x5 = 140`;
4. exact return for every relation address;
5. exact `D5` relation equivariance;
6. expected failure of a rotation-equivariant single-address selector;
7. information-loss controls when `B` or `Q` is removed;
8. separation from the generic independent/locked Gear schedules.

## 7. Claim boundary

Passing validation establishes only that this explicitly declared finite
encoding and relation satisfy their algebraic contract against the frozen
SCC-003 reference tables.  It does not establish:

- a new canonical Family or `PENT-08`;
- an admitted A0 experiment or resolution of `A0-BL-023`;
- a unique map from quotient nodes to single gear states;
- a physical, astronomical, calendrical, musical or metrological mechanism;
- novelty, priority, generalization beyond depth six or publication readiness.

