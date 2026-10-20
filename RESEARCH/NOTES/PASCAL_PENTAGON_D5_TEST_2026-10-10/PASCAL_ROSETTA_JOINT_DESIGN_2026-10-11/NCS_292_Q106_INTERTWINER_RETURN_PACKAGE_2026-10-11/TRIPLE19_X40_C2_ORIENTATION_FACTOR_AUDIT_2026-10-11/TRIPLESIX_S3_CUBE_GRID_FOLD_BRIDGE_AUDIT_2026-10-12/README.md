# TripleSix S3 / Cube-Grid Fold Bridge Audit

This bounded extension tests the proposed bridge from the six TripleSix
permutations to the `63 <-> 64` fold and the displayed Alpha–Omega cube grids.

Run:

```sh
python3 verify_triplesix_cube_grid_fold.py
```

## Result

The exact bridge is:

```text
six permutations = three reversal axes x two parity orientations
                 = an axis-plus-side address
```

The explicitly declared coordinate fold `q:{0,...,63}->{0,...,62}` collapses
only the central pair `{31,32}`. Coordinatewise, it produces exact
`64x64 -> 63x63` and `64^3 -> 63^3` quotient maps.

TripleSix resolves one selected-axis fold crossing. It does **not** carry all
simultaneous side choices at a two- or three-axis pivot. The 3D central fibre
has `2^3=8` states, so a six-state carrier cannot reconstruct it.

The operator comparison also keeps an important distinction visible:

- displayed reversal plus left axis-cycle: commuting grammar (`J_c`-like);
- same-side right actions: dihedral grammar (`J_d`-like), but no descent to
  the displayed axis-pair quotient.

No historical Janus choice follows because the visuals do not declare the
action convention.

Generated evidence:

- `RESULT.json`
- `TRIPLESIX_AXIS_ORIENTATION.csv`
- `GRID_FOLD_FIBER_PROFILE.csv`
- `JANUS_ACTION_CONVENTIONS.csv`
- `VISUAL_SOURCE_LEDGER.json`

General theorem extension:

- `GENERAL_COORDINATE_FOLD_MINIMAL_RESIDUAL_RETURN_AUDIT_2026-10-12/`
- proves the exact `2m -> 2m-1` fibre profile in every dimension;
- proves pointwise-minimal `k`-bit and uniform-minimal `d`-bit Return;
- leaves the wider Grid–Fold–Channel specification open.

This package reuses `A0-BL-023`, the existing Pascal `S3/C3` carrier result,
and `NN:MRB_ACR_NCS_Q106_RETURN_CROSSWALK`. It creates no new Study, Family,
canonical Navigator identity or publication state.
