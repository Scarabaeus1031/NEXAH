# Run contract — Q106 46/106/194 contrast

Date: `2026-10-11`  
Reproducibility: `R2_LOCAL_REPLAY`

## Environment

- Python `3.x`, standard library only
- local read access to the frozen parent `RESULT.json`
- no network, randomness or external data

## Commands

From this directory:

```bash
python3 -B verify_q106_contrast.py --output PRIMARY_RESULT.json
python3 -B verify_q106_contrast.py --output REPLAY_RESULT.json
cmp PRIMARY_RESULT.json REPLAY_RESULT.json
python3 -B verify_result.py RESULT.json
```

`RESULT.json` is the byte-identical canonical copy of `PRIMARY_RESULT.json`.

## Resource bound

The largest requested prime index is `1001^2=1002001`. The deterministic
sieve remains below 64 MiB for its bit array and completes locally without
network access.

## Side effects

Only the declared JSON result files are written. No source, registry,
lifecycle, publication or public route is changed by the run itself.

## Failure semantics

Any frozen-source mismatch, arithmetic mismatch, unexpected hit or missing
boundary produces a non-PASS classification and a nonzero exit status.

## Claim ceiling

Finite selectivity in the declared windows only. No global uniqueness,
undefined `R` extension, Prime Pascal Pyramid, node embedding, physical law,
resonance or publication claim.
