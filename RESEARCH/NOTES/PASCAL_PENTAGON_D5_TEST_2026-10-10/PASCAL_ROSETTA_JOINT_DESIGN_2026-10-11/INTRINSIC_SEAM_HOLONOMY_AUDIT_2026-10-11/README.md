# Pascal intrinsic seam / Z2 holonomy audit

Date: `2026-10-11`  
Status: `VALIDATED_NEGATIVE_INTRINSIC_RESULT / NOT_ADMITTED / NOT_PENT_08`  
Reused identity: `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`

This audit asks whether the Möbius twist used by the Lissajous–Möbius return
candidate was already forced by the frozen Pascal quotient.

## Result

The answer is **no under the declared Pascal local-consistency contract**.

- the graph has cycle rank `180-106+1=75`;
- its 75 Pascal-diamond boundaries are linearly independent over `F2`;
- those boundaries span the complete graph cycle space;
- therefore every edge labeling that is locally closed on every Pascal
  diamond has trivial holonomy on every cycle;
- equivalently, `dim H1=0` for this declared finite cell complex.

The graph alone has 75 cycle degrees of freedom, but it supplies no rule for
selecting one. Adding the Pascal 2-cells removes all of them rather than
selecting a Möbius class.

## Minimal seam controls

Removing one diamond constraint creates one nontrivial degree of freedom but
breaks D5 symmetry. The 75 diamonds form nine D5 orbits:

```text
3 orbits of size 5
6 orbits of size 10.
```

An odd D5-invariant seam is incompatible with each centered size-5 orbit. It
is compatible after removing any one of the six off-center size-10 orbits.
Consequently:

- a D5-preserving Möbius extension requires at least ten released diamond
  constraints;
- six symmetry-compatible seam-orbit choices remain;
- the frozen carrier does not choose among them.

Classification:

```text
ONLY_AFTER_ADDED_SEAM
SIX_NONCANONICAL_D5_COMPATIBLE_SEAM_ORBITS
```

## Meaning

The earlier Lissajous–Möbius candidate is a valid external extension, not an
intrinsic topology recovered from `Q106`. A later admitted test could add one
declared ten-diamond seam orbit and compare the six alternatives, but it may
not claim that the original Pascal quotient selected that seam.

## Verify

```sh
python3 verify_intrinsic_seam.py
python3 verify_intrinsic_seam.py --write
```

This is formal finite fixture validation, not a Science-Lab run.
