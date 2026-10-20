# Triple-19 / X40 C2 Orientation Factor Audit

This package tests the smallest exact bridge that survives the source-contract audit: the orientation bit shared by the Triple-19 antipode carrier and the NCS X40 Janus carrier.

## Result

Run `python3 verify_triple19_x40_c2_factor.py` to regenerate the result and tables.

The bounded conclusion is:

- Triple-19 and X40 have an exact shared `C2` orientation factor.
- Both admissible X40 Janus laws induce the same flip on that factor, so the factor does not select one of them.
- The declared quotient `X40 -> X20` collapses the two orientation states in every fibre. No `X20 -> C2` readout can reconstruct the erased bit.
- The `C7` and `C5` base cycles have no nontrivial group homomorphism between them.
- Consequently there is no established full-carrier intertwiner, Triple-19-to-X20 map, X20 adjacency or Q106 map.

Generated evidence:

- `RESULT.json`
- `TRIPLE19_C2_FACTOR.csv`
- `X40_X20_QUOTIENT_FIBERS.csv`
- `JANUS_FACTOR_COMPARISON.csv`

This is an internal formal design extension of `A0-BL-023`. It creates no new Study, Family, Navigator identity, PENT-08 admission, publication state or physical claim.

## Tested TripleSix / cube-grid successor

[`TRIPLESIX_S3_CUBE_GRID_FOLD_BRIDGE_AUDIT_2026-10-12`](TRIPLESIX_S3_CUBE_GRID_FOLD_BRIDGE_AUDIT_2026-10-12/README.md)
tests the owner-supplied six-permutation and Alpha–Omega cube-grid visuals as a
bounded formal extension. The six states form an exact three-axis plus parity
address. That address resolves one selected `64 -> 63` fold crossing, but not
the simultaneous two- or three-axis pivot fibres. The result passes `58/58`
checks and preserves null historical Janus selection and null cube identity.

