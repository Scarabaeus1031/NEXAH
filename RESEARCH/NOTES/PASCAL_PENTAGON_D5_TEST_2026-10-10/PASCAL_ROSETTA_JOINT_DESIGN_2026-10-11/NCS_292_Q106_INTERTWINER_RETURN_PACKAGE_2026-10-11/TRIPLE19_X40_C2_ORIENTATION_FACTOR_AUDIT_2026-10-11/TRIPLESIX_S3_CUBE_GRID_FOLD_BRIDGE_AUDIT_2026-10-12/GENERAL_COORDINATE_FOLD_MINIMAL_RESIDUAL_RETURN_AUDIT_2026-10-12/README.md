# General Coordinate-Fold / Minimal Residual Return Audit

This package generalizes the declared `64 -> 63` coordinate fold from the
TripleSix audit to every `2m -> 2m-1` fold and every dimension `d >= 1`.

Run:

```sh
python3 verify_general_coordinate_fold_return.py
```

## Result

For a target with `k` central coordinates, the fibre has exactly `2^k`
source states. The number of such targets is
`C(d,k)(2m-2)^(d-k)`. Exact Return needs and suffices with `k` conditional
bits at that target; a uniform fixed-width Return address needs `d` bits.

The verifier exhaustively checks `m=1..5`, `d=1..4`, reconstructs every
source state in that range, runs the non-identical controls `(m,d)=(1,4)` and
`(2,3)`, and recovers the earlier `64 -> 63` profiles for dimensions 1–3.

Generated evidence:

- `RESULT.json`
- `FIBRE_PROFILE.csv`
- `RESIDUAL_RETURN_CASES.csv`

This is an internal formal-design validation under `A0-BL-025`. It reuses the
existing A0 and NN identities, creates no Study or Navigator node, and does
not complete the wider Grid–Fold–Channel specification.

## Full typed-chain extension

The nested
[`GRID_FOLD_CHANNEL_INTERFACE_ASSEMBLY_UPDATE_RETURN_AUDIT_2026-10-12`](GRID_FOLD_CHANNEL_INTERFACE_ASSEMBLY_UPDATE_RETURN_AUDIT_2026-10-12/README.md)
package completes the formal-design checklist for
`carrier -> fold -> embedding -> envelope -> interface -> assembly -> update -> Return`
on two non-identical finite controls. This is still not an admitted Study;
physical stability, flow semantics and the historical visual generator remain
outside the result.
