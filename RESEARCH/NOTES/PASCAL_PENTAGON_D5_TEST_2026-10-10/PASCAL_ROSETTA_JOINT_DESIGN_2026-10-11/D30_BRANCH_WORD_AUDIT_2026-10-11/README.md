# Pascal–Rosetta D30 branch-word audit

Date: `2026-10-11`  
Status: `FORMAL_DESIGN_VALIDATION / NOT_ADMITTED / NOT_ACTIVE / NOT_PENT_08`  
Reused identity: `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`

This package tests the proposed 30-phase extension of the existing
Pascal–Rosetta Joint. It does not create a new NEXAH Family, Study, Navigator
node or physical mechanism.

## Exact phase lift

For a raw Pascal incidence `(f,n,k)` define

```text
p30(f,n,k) = 2k - n mod 30.
F30(f,n,k) = (f, f+k mod 5, n mod 6, p30).
```

The two Pascal branches become unit steps:

```text
left:  p -> p-1
right: p -> p+1.
```

With reflections `S0(theta)=-theta` and `F6(theta)=12deg-theta`, the ordered
compositions are

```text
TL = S0 o F6  = rotation -12deg
TR = F6 o S0  = rotation +12deg.
```

The orientation convention is chosen to match the Pascal left/right signs.
Both rotations have order `30`; exchanging the operator order reverses the
direction.

## Five D-registers

The already-present face coordinate `f in C5` now receives an explicit
one-based register view:

```text
D1 <-> f=0, D2 <-> f=1, ..., D5 <-> f=4.
```

Thus the phase cover is

```text
C5_D x C30_P = {D1,...,D5} x {0,...,29},
```

with capacity `5 x 30 = 150`. Each register contains the same local Pascal
compiler `L:-1`, `R:+1`; a branch step does not switch the D-register. The
pentagon rotation cycles `D1 -> D2 -> ... -> D5 -> D1`, while the declared
reflection fixes `D1`, exchanges `D2 <-> D5` and exchanges `D3 <-> D4`.

This notation must not be confused with `D5`, the order-ten dihedral symmetry
group. `D1..D5` are five address registers, not five new operators, Studies or
identities.

On the frozen depth-six object each register contains `28` raw incidences and
all `127` branch words. Only `13` phases occur per register, hence only `65`
of the `150` register-phase positions are observed. The projection
`(face,n,k) -> (Dj,p)` is intentionally lossy; adding depth restores exact
reconstruction as `(Dj,n,p)`.

## Complete frozen word audit

All `127` branch words of length `0..6` are enumerated. Across the five
D-registers this gives `635` word instances. At fixed depth `n`, a word with `k` right steps
lands at the Pascal endpoint `(n,k)` with multiplicity `binomial(n,k)` and
phase `2k-n`.

This proves two different facts that must not be conflated:

- the word history intentionally collapses to the Pascal endpoint;
- `(D-register, depth, phase)` still reconstructs each of the `140` frozen raw
  incidences exactly.

At depth at most six only `13` of the `30` phases occur. The frozen Pascal
fixture therefore supplies an exact partial D30 phase lift, not a complete
30-state orbit.

## Exact negative boundary for the old gear

The existing carrier is

```text
G = C5 x C5 x C6 x C12.
```

The verifier enumerates all `900` group characters `G -> C30`. None can map
the Pascal left and right transitions to `-1` and `+1` respectively: every
possible `C6` and `C12` contribution to `C30` is a multiple of five. The unit
D30 schedule therefore does not factor through the old C12 gear.

That failure is useful. It distinguishes the new phase lift from a relabelling
of the earlier gear and identifies the minimal design extension as an explicit
`C30_P` coordinate.

## H3 and E8 adapter boundary

- the standard H3 root orbit has `30` points, `60` nearest-neighbour edges and
  degree `4`; its Coxeter element decomposes the roots into `3 x 10` cycles;
- the E8 Coxeter coordinate model has `8 x 30` positions;
- choosing one oriented Pascal-to-E8 lane chart requires lane, origin and
  orientation: `8 x 30 x 2 = 480` candidates.

No source rule presently selects one of those 480 charts. The audit therefore
validates the coordinate family and preserves non-uniqueness instead of
inventing a canonical E8 identification. H3 is retained as a separate
30-point geometric carrier, not renamed as the D30 phase cycle.

## Files

- `FORMAL_CONTRACT.md` — typed maps and separation boundaries;
- `D30_CONTRACT.json` — machine-readable contract;
- `verify_d30_adapter.py` — deterministic audit;
- `RESULT.json` — generated validation record.

## Verify

```sh
python3 verify_d30_adapter.py
python3 verify_d30_adapter.py --write
```

This is formal fixture validation, not a Science-Lab run.
