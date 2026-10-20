# NCS X20 typed carrier · Triple-19 Pc/Pd · Q106 audit

Date: `2026-10-11`  
Parent: `A0-BL-023:NCS_292_Q106_INTERTWINER_RETURN_PACKAGE:V1`  
Class: source-contract audit; formal design validation; not an admitted Study

## Question

Do the frozen source-side records independently define enough structure to
test the twenty-four inherited D5-equivariant charts from X20 to Q106?

The required source contract is

```text
X20 = C5 x P4
E_X subset of unordered or directed pairs of X20
tau_X : E_X -> declared edge types
T_19 : Triple19_oriented -> X20
```

Only after `E_X`, `tau_X` and `T_19` are fixed independently of Q106 may a
chart `iota:X20->Q106` be tested for adjacency, edge-type and antipode
compatibility.

## Source-side result

The sources establish the state coordinates and C5 rotation

```text
P4 = {carrier, frame_cut, transform_view, return_record}
r_X(s,p) = (s+1 mod 5,p).
```

They do not declare `P4` to be the path graph on four vertices. They do not
supply `E_X` or `tau_X`. MRB-06, MRB-09, MRB-10, ACR-44 and OIL/RIS provide
useful but differently typed carriers and operators; none provides a typed
transport into X20.

## Triple-19 correction and gate

The Triple-19 source defines

```text
P_c(r) = (r,c_r,+1)
P_d(r) = (r,c_r,-1)
A(r,c_r,sigma) = (6-r,c_r,-sigma).
```

`P_c` and `P_d` are oriented-state constructors. `A` is the fixed-point-free
involution. The source has fourteen oriented states, not twenty, and explicitly
records a null intertwiner. Cardinality mismatch alone proves neither
incompatibility nor a map; an independently typed transport is required.

## Closed-gate sequence

```text
G1 source hash and type freeze                         PASS
G2 independent X20 adjacency and edge-type contract   OPEN / NULL
G3 Triple-19-to-X20 map                               OPEN / NULL
G4 D5 chart adjacency test                            NOT EVALUATED
G5 Pc/Pd/A compatibility test                         NOT EVALUATED
G6 uniqueness modulo automorphisms                    NOT EVALUATED
```

The inherited 24 D5-equivariant orbit charts are enumerated only as a blocked
candidate register. No chart receives a score, rank or preference.

## Classification

```text
SOURCE_CONTRACT_UNRECOVERED
x20_edge_set = null
x20_edge_types = null
triple19_to_x20_map = null
typed_intertwiner_to_q106 = null
```

This is a completed bounded source audit, not a failed graph search. It keeps
the next requirement exact: a Human-declared new source model or newly found
historical source must define X20 adjacency without reference to Q106.

## Nonclaims

- Q106 adjacency is not pulled back into X20.
- `P4` is not silently retyped as a path graph.
- `P_c` and `P_d` are not mislabeled as involutions.
- No Triple-19, MRB, ACR, OIL/RIS, NCS or Q106 carrier identity is asserted.
- No Study, PENT-08, Family, canonical operator or publication state is created.
