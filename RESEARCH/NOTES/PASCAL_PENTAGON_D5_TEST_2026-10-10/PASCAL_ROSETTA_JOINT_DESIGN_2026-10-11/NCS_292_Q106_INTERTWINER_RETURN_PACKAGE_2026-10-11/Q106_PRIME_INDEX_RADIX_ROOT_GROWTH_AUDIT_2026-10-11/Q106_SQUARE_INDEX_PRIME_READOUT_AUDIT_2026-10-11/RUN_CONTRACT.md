# Run Contract

## Identity and authority

- Run: `A0_Q106_SQUARE_INDEX_PRIME_READOUT_2026_10_11`
- Owner gate: Mission Control decision dated `2026-10-11`
- Reused identity: `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`
- Method class: theoretical / exhaustive finite computation
- Reproducibility target: `R2_LOCAL_REPLAY`

## Environment

- Python `3.x`, standard library only
- Working directory: NEXAH Core repository root
- No network access

## Frozen inputs

The exact paths and SHA-256 values are declared in `CONTRACT.json`. A mismatch
is a failed run, not an instruction to repair the source.

## Commands

```bash
python3 RESEARCH/NOTES/PASCAL_PENTAGON_D5_TEST_2026-10-10/PASCAL_ROSETTA_JOINT_DESIGN_2026-10-11/NCS_292_Q106_INTERTWINER_RETURN_PACKAGE_2026-10-11/Q106_PRIME_INDEX_RADIX_ROOT_GROWTH_AUDIT_2026-10-11/Q106_SQUARE_INDEX_PRIME_READOUT_AUDIT_2026-10-11/verify_square_index_prime_readout.py
```

Execute twice. The two UTF-8 JSON byte streams must match. Then run:

```bash
python3 RESEARCH/NOTES/PASCAL_PENTAGON_D5_TEST_2026-10-10/PASCAL_ROSETTA_JOINT_DESIGN_2026-10-11/NCS_292_Q106_INTERTWINER_RETURN_PACKAGE_2026-10-11/Q106_PRIME_INDEX_RADIX_ROOT_GROWTH_AUDIT_2026-10-11/Q106_SQUARE_INDEX_PRIME_READOUT_AUDIT_2026-10-11/verify_result.py RESULT.json
```

## Expected outputs

- `PRIMARY_RESULT.json`
- `REPLAY_RESULT.json`
- `RESULT.json`

All three must be byte-identical. The independent verifier must return PASS.

## Resource and side-effect bounds

- expected runtime below one second;
- expected memory below 32 MiB;
- reads only the three frozen JSON sources;
- writes only the three declared result snapshots when integrated;
- makes no network, publication, registry, Family or identity change.

## Failure semantics and STOP

Any failed hash, arithmetic assertion, replay mismatch or independent-verifier
failure classifies the run as invalid. Stop before reinterpretation or source
repair. Passing remains bounded by the claim boundary in `CONTRACT.json`.
