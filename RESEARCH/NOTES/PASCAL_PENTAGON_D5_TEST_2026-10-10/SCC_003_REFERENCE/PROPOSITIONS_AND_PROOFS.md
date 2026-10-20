# SCC-003 propositions and proofs

Date: `2026-10-10`  
Status: `COMPACT_PROOF_PACKAGE / EXISTING_BOUNDED_CONSTRUCTION / NOT_ACTIVE`

The notation is fixed in [FORMAL_SPECIFICATION.md](FORMAL_SPECIFICATION.md).
These propositions concern only the declared depth-six, five-face object.

## Proposition 1 — one carrier has 28 vertices

`P_6` has

```text
sum_(n=0)^6 (n+1) = 1+2+...+7 = 28
```

vertices. It has

```text
sum_(n=0)^5 2(n+1) = 2(1+...+6) = 42
```

directed edge incidences. ∎

## Proposition 2 — every open attachment adds exactly 21 vertices

Attach a new copy of `P_6` to `K_open(j)` along the current terminal radial
side. Its intersection with the existing quotient consists of:

- the already common apex; and
- six non-apex side vertices at levels `1,...,6`.

These seven vertices are distinct before attachment, and no interior vertex
is identified. Hence the net increment is

```text
28 - 7 = 21.
```

The same attachment shares the six directed side edges, so it adds
`42-6=36` directed quotient edges. ∎

## Proposition 3 — the open counts are 28, 49, 70, 91, 112

By Proposition 1, `|V(K_open(1))|=28`. Repeated application of Proposition 2
gives

```text
|V(K_open(j))| = 28 + 21(j-1) = 21j+7.
```

For `j=1,...,5`, this is

```text
28, 49, 70, 91, 112.
```

Similarly, the directed quotient-edge counts are
`42,78,114,150,186`. ∎

## Proposition 4 — cyclic closure identifies exactly six vertices

In `K_open(5)`, the two terminal radial sides already share the apex, but
their non-apex vertices at levels `1,...,6` lie in twelve distinct quotient
classes. Cyclic closure pairs them level by level. The six pairs are disjoint
and the closure rule generates no additional identifications. Therefore the
vertex count decreases by exactly six:

```text
|V(K_closed)| = 112 - 6 = 106.
```

The six terminal side edges likewise become six duplicate quotient edges, so
`|E_closed|=186-6=180`. ∎

## Proposition 5 — the open and closed quotients are connected

Each `P_6` is connected because every vertex has an upward path to the apex
when edge directions are ignored. All face apices are identified in every
`K_open(j)`, so the union is connected. A further quotient of a connected
graph is connected; hence `K_closed` is connected. ∎

## Proposition 6 — weights and Pascal recurrences survive the quotient

Singleton classes present no ambiguity. Every nontrivial non-apex class
identifies a right-side vertex `(f,n,n)` with a left-side vertex
`(f+1,n,0)`, and both have weight `1`. The apex class also has constant weight
`1`. Thus the quotient weight is well-defined.

For every retained face incidence, the ordinary binomial identity

```text
binom(n,k)=binom(n-1,k-1)+binom(n-1,k)
```

holds with zero extension at the two sides. The quotient map does not change
any of these numerical terms. Hence all five facewise Pascal recurrences are
preserved.

This proposition does not claim that a seam weight equals the sum over *all*
incoming edges of the simple quotient graph: that sum forgets face incidence
and may double-count a glued side. ∎

## Proposition 7 — `r` and `m` are automorphisms

Rotation sends the seam pair

```text
(f,n,n) ~ (f+1,n,0)
```

to the seam pair with index `f+1`. Reflection sends it to the same relation
with reversed side order between faces `-f-1` and `-f`. Both maps preserve the
apex class. They therefore descend to the quotient.

Rotation plainly preserves the two recurrence-edge types. Reflection swaps
the left and right child types, so it preserves their union. Binomial
symmetry `binom(n,k)=binom(n,n-k)` proves weight preservation. Direct
substitution yields `r^5=e`, `m^2=e`, and `mrm=r^-1`. Thus the ten declared
maps act as typed automorphisms. ∎

## Proposition 8 — the typed automorphism group is exactly `D_5`

Any typed automorphism permutes the five retained macro-faces and preserves
which pairs share a full radial seam. It therefore induces an automorphism of
the face-adjacency cycle `C_5`, whose automorphism group is `D_5` of order
`10`.

This induced map is injective. Once a face and its two bounding seams are
fixed, level, directed parent/child incidence and distance from the two sides
fix every `(n,k)` position in that face. Hence an automorphism inducing the
identity on the five faces is the identity on the whole typed complex.

Proposition 7 supplies all ten cycle rotations and reflections. The typed
automorphism group is therefore exactly `D_5`. ∎

## Proposition 9 — canonical export metrics

The quotient consists of:

- one apex class;
- `5*6=30` non-apex seam classes; and
- `5*(1+2+3+4+5)=75` singleton interior classes.

Thus `1+30+75=106`. The raw `210` edge incidences collapse in pairs along
the six level transitions of each of five cyclic seams, removing `5*6=30`
duplicates and leaving `180` directed quotient edges. ∎

## Verification boundary

The independent verifier checks the finite counts, union-find quotient,
weights, all facewise recurrences, adjacency, graph6 serialization, hash
manifest, the ten declared actions and the dihedral relations. The exactness
of the typed group also uses the face-cycle argument above; graph6 alone is
not used to claim an exhaustive automorphism group for the untyped graph.

