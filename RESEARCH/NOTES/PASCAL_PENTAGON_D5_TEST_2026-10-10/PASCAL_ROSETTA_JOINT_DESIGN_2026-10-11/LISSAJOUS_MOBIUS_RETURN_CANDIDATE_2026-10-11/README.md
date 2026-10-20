# Pascal Lissajous–Möbius return candidate

Date: `2026-10-11`  
Status: `FORMAL_DESIGN_VALIDATION / NOT_ADMITTED / NOT_ACTIVE / NOT_PENT_08`  
Reused identity: `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`

This package tests the missing candidate map between the existing D30 phase
lift and the ORION-style Möbius seam contract. It introduces an explicit
orientation fibre and keeps the Lissajous curve, phase state and strip
topology separate.

## What is tested

- a `5:6` Lissajous phase view on the exact `C30` common cover;
- exact reconstruction of phase from `(p mod 6,p mod 5)`;
- the expected information loss in the drawn `(x,y)` curve;
- cylinder versus Möbius seam controls on the same carrier;
- one-turn orientation reversal and two-turn exact return;
- one versus two boundary components;
- reversible transport for all 127 Pascal branch words of depth at most six;
- coverage of all 140 frozen Pascal face incidences.

## Important boundary

This is the first executable formal candidate for the previously open
Möbius-to-Lissajous bridge. It is not yet `PENT-08`: no new Study or Family is
created, and the constructed seam is not evidence that a historical visual,
the Pascal carrier or a physical system already possessed this topology.

The subsequent
[`INTRINSIC_SEAM_HOLONOMY_AUDIT_2026-10-11`](../INTRINSIC_SEAM_HOLONOMY_AUDIT_2026-10-11/)
confirms this boundary exactly: the fully closed Pascal cell complex has
trivial `H1`; the Möbius seam is an added extension, not an intrinsic recovery.
Preserving D5 symmetry leaves six noncanonical ten-diamond seam-orbit choices.

## Files

- `FORMAL_CONTRACT.md` — typed question, maps, controls and pass criteria;
- `CONTRACT.json` — machine-readable frozen candidate;
- `verify_lissajous_mobius_return.py` — deterministic verifier;
- `RESULT.json` — generated result record.

## Verify

```sh
python3 verify_lissajous_mobius_return.py
python3 verify_lissajous_mobius_return.py --write
```

This is formal fixture validation, not a Science-Lab run.
