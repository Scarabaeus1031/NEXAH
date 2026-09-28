# WP4 Validation Report

Date: `2026-09-28`

Status: `VALID / REPLAYABLE_LOCAL_INSTRUMENT_ONLY`

## Suite

```text
/opt/anaconda3/bin/python scripts/validate_runtime.py
```

Observed:

```json
{"profile":"NC01-ADVISORY-0.1","runtime_tests":14,"schema_engine":"jsonschema Draft202012Validator","status":"VALID"}
```

The fourteen tests comprise seven WP3 core tests and seven WP4 package tests.
WP4 covers deterministic run/replay, exact Markdown projection, evidence
tamper rejection, undeclared-file rejection, symlink rejection, separate
hash-bound Human Return and CLI run/verify.

## Independent temporary clean run

One synthetic package was assembled with real evidence bytes, run, verified,
returned with explicit Human action `ABSTAIN`, and verified again.

| Artifact | SHA-256 |
|---|---|
| ComparisonRecord | `0ac593a071b342690ce938bee11143d2b011784d9dd2f76995eeeddaf8d503db` |
| Package manifest | `8ab0b18a471d67c0237abfde6d9252be9cdc57ac66171d4076b37051796a8b44` |
| Markdown report | `19f6fbe1be461faabc17e8e0a9e1990951148710305d7f70ea0932512c6680f0` |
| Run receipt | `1823d0146262f467ba7a5384ea77c14c7b885bf3de2aad23c62220042b633c8c` |
| Human Return | `c9a74d12fb10dbb078b30f8a6d864f71b4a7c97716390c989224697ede908ca0` |

Final verification returned `status=VALID` and `human_return=ABSTAIN`.

## Regression

The WP2 contract checker remains valid and the WP3 deterministic result hash
is unchanged. Package controls add no semantic equivalence inference and do
not alter the five frozen application record schemas.

## Claim boundary

This is a local synthetic machine-and-package validation. It is not the WP5
preregistered technical benchmark and supplies no incremental-value or Human
utility result.
