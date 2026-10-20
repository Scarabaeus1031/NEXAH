# Pascal–Rosetta Joint — formal design fixture

Date: `2026-10-11`  
Status: `FORMAL_DESIGN_VALIDATION / NOT_ADMITTED / NOT_ACTIVE / NOT_PENT_08`  
Reused identity: `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`  
Related backlog records: `A0-BL-023`, `A0-BL-051`

This package makes the proposed Pascal–Rosetta Joint inspectable without
promoting it to a new NEXAH Family, experiment, physical mechanism or
Navigator identity.

The difference from a generic product of wheels is the **Pascal-induced
schedule**.  A raw face incidence `(f,n,k)` is encoded as

```text
F(f,n,k) = (a,b,d,q)
           (f, f+k mod 5, n mod 6, 2k-n mod 12).
```

The two Pascal branches then induce exact gear transitions:

```text
L(a,b,d,q) = (a, b,   d+1, q-1)
R(a,b,d,q) = (a, b+1, d+1, q+1),
```

with component arithmetic modulo `5,5,6,12`.  Thus the Pascal carrier chooses
which wheel advances and the sign of the envelope movement; the clock is not
an independently chosen locked/counter schedule.

## Why the quotient joint is a relation

`F` is injective on all `140` raw face incidences.  It is not constant on the
fibres of the quotient map `pi:P_6 x C_5 -> Q_106`:

- `75` interior quotient nodes have one gear address;
- `30` seam nodes have two gear addresses;
- the common apex has five gear addresses.

The honest quotient joint is therefore

```text
J(v) = { F(x) : pi(x)=v }.
```

This is not an implementation defect.  The multiplicity records precisely
which face incidences were glued.  Any selected gear address returns exactly
to its quotient node through `rho(F(x))=pi(x)`.

## Expected negative result

There is no rotation-equivariant single-address selector
`s:Q_106 -> image(F)` with `s(v) in J(v)`.  The quotient apex is fixed by the
`C5` rotation, while its five gear addresses form a free five-cycle and contain
no fixed address.  A forced single address would therefore destroy the `D5`
symmetry or erase provenance.

That failure is a useful boundary: exact return is available through the
relation; a canonical single-state quotient embedding is not.

## Files

- `FORMAL_CONTRACT.md` — typed objects, maps, commutative diagrams and claim
  boundary;
- `JOINT_CONTRACT.json` — machine-readable design contract;
- `verify_joint.py` — independent checker over the frozen SCC-003 artifacts;
- `RESULT.json` — generated validation record.
- `D30_BRANCH_WORD_AUDIT_2026-10-11/` — complete depth-six branch-word audit,
  exact signed C30 phase lift, C12 non-factorization result and bounded H3/E8
  adapter analysis.
- `LISSAJOUS_MOBIUS_RETURN_CANDIDATE_2026-10-11/` — exact `5:6` Lissajous
  phase chart, cylinder/Möbius seam controls, one-turn orientation reversal,
  two-turn return and reversible Pascal-word transport. This is a bounded
  formal candidate, not `PENT-08` or an admitted Study.
- `INTRINSIC_SEAM_HOLONOMY_AUDIT_2026-10-11/` — exact `F2` cycle-space and
  cellular-cohomology audit. The 75 Pascal diamonds span the full cycle space,
  so intrinsic `H1` is zero. A D5-invariant odd seam requires removal of one
  of six noncanonical ten-diamond orbits; the frozen carrier selects none.
- `NCS_292_DUAL_AXIS_Q106_BRIDGE_AUDIT_2026-10-11/` — source-frozen audit of
  the historical four-point NCS mover, adjacent `99/100` cuts, a declared
  `40 -> 20` Janus/package quotient and the separate Q106 carrier; the finite
  quotient compiles while all three required intertwiners remain open.
- `NCS_292_Q106_INTERTWINER_RETURN_PACKAGE_2026-10-11/` — five-module follow-up
  that recovers the NCS translation law, exhaustively searches D5-invariant
  Q106 interfaces, validates the unique connected `6+100` cut, compares two
  Janus algebras and exposes the bounded result in an interactive HTML
  instrument. The actual adjacency-preserving `X20 -> Q106` map remains open.

## Verify

From this directory:

```sh
python3 verify_joint.py
python3 verify_joint.py --write
python3 D30_BRANCH_WORD_AUDIT_2026-10-11/verify_d30_adapter.py
python3 LISSAJOUS_MOBIUS_RETURN_CANDIDATE_2026-10-11/verify_lissajous_mobius_return.py
python3 INTRINSIC_SEAM_HOLONOMY_AUDIT_2026-10-11/verify_intrinsic_seam.py
python3 NCS_292_DUAL_AXIS_Q106_BRIDGE_AUDIT_2026-10-11/verify_ncs_292_dual_axis_q106.py
python3 NCS_292_Q106_INTERTWINER_RETURN_PACKAGE_2026-10-11/verify_intertwiner_return.py
```

This command validates a formal design fixture.  It is not an admitted
Science-Lab run and does not resolve `A0-BL-023` or activate `A0-BL-051`.

The matched controls include the prior generic locked and counter-rotating
Gear schedules plus two branch-collapsed ablations.  Neither generic schedule
matches any of the `210` Pascal incidences; each branch-collapsed ablation
matches only its own `105` edges.  Only the branch-aware Pascal schedule
matches all `210`.

