# PENT-07 — Pentagon / hexagon coupling audit

Date: `2026-10-10`

Status: `PASS_WITH_BOUNDARY / BOUNDED_CANDIDATE_EVIDENCE / NOT_ADMITTED`

## Question

Which existing NEXAH pentagon/hexagon visuals instantiate a declared coupling,
and which remain arithmetic, reference-axis or provenance markers?

This audit extends the existing Pascal-pentagon lens identity. It creates no
new Family and does not identify an archived visual with the verified Pascal
carrier merely because both contain a pentagon.

## Exact cardinality ledger

```text
C5 + C6       = 11
C6 + C6       = 12
C5 + C6 + C6  = 17
```

These are exact node counts for disjoint cycle shells. They do not by
themselves add a cross-edge, choose a phase relation or define an operator.

## Coupling audit

### 1. Direct boundary identification

There is no bijection between `C5` and `C6`. Exhaustive enumeration also finds
zero graph homomorphisms from the odd cycle `C5` to the bipartite cycle `C6`.
A direct edge-preserving identification therefore fails. Any 5/6 boundary
gluing must declare a refinement, contraction, hub, cover or different typed
relation.

### 2. Common phase cover

Both cycles inject as anchor sets into `Z30`:

```text
C5 anchors: 0, 6, 12, 18, 24
C6 anchors: 0, 5, 10, 15, 20, 25
shared:     0
```

This is a valid phase-cover relation, not an embedding of cycle edges into
adjacent edges of `C30`. The joint rotational stabilizer is the identity.

### 3. Two hexagons

Two abstract `C6` cycles admit `12` dihedral isomorphisms: six offsets in each
of two orientations. Consequently `6+6=12` records the shell cardinality, but
does not select whether the second hexagon is aligned, shifted, reflected or
counter-oriented. One correspondence must be declared before it becomes an
operator.

### 4. Archived 5+6+6 hub graph

The Core fixture is exactly reconstructed:

```text
without hub: 17 nodes · 17 edges · 3 components
with hub:    18 nodes · 34 edges · 1 component
```

Its coupling operator is the common hub. The prior Core controls further show
that the reported synchronization behavior was not unique to the `5+6+6`
partition. This is a qualified comparator, not a Pascal-carrier identity.

### 5. Interference and “12-mode” demos

The interference demo declares a vector field, but samples unseeded random
initial particle positions. The companion 12-mode demo draws twelve reference
axes in a literal `for i in range(12)` loop. It does not infer twelve modes from
the simulated data. Therefore:

```text
field equations:       defined
displayed trajectories: not exactly replayable as written
12-mode emergence:     undefined / not tested by the demo
```

## 110 / 111 / 112 provenance boundary

The nearby historical traces are retained as search markers:

```text
110 = 2 × 5 × 11
111 = 3 × 37
112 = 2^4 × 7
```

The Core contains historical `111×111` grid material and an earlier symbolic
`1/112` “draft” label. PENT-06 independently establishes `112` as the open
five-face preclosure node count. Those facts are provenance, not a common
operator.

“Modular shadow” is meaningful only after specifying a modulus `N` and a map
such as `x -> -x mod N`. Because no canonical modulus or intertwiner is
declared here, the sequence `110,111,112` remains a hypothesis/search corridor.
The screenshot title “NEXAH Orientation Architecture v55” is likewise retained
as visual provenance; no matching source identity was promoted by this audit.

## Result

- `C5 -> C6` direct identification: `FAIL_CARDINALITY_AND_GRAPH_HOMOMORPHISM`;
- `C5` and `C6` in the common `C30` phase cover: `PASS_WITH_TYPE_BOUNDARY`;
- `C6A -> C6B`: `UNDEFINED` until one of 12 isomorphisms is selected;
- archived `C5+C6+C6` hub coupling: `PASS`;
- interference equations: `DEFINED`, trajectory sample unseeded;
- claimed twelve-mode emergence: `UNDEFINED_REFERENCE_AXES_DRAWN_NOT_INFERRED`;
- map to the 106-node Pascal quotient: `UNDEFINED_NO_INTERTWINER`.

Replay:

```sh
python3 run_test.py --write
```

## Boundary

This is a finite graph, cycle, phase-cover, source-code and arithmetic audit.
It establishes no resonance, physical field, canonical role for 110/111/112,
identity between the Pascal carrier and an archived fixture, or new NEXAH
Family.
