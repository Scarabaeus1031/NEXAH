# WP4 Package, Report and Return

Decision: `PASS / LOCAL_INSTRUMENT_COMPLETE / WP5_READY_NOT_ACTIVE`

## Implemented

- strict local Case-directory contract;
- three Draft-2020-12 package schemas for descriptor, manifest and receipt;
- evidence byte-hash verification;
- package-root, path-traversal, symlink and undeclared-file rejection;
- canonical ComparisonRecord output;
- deterministic faithful Markdown report;
- evidence/input/output manifest;
- deterministic replay receipt;
- replay verification against fresh WP3 execution;
- separate comparison-hash-bound Human Return;
- confirm, amend, abstain and STOP actions with target validation.

## Integrity chain

```text
Case + Analyses + Alignment + Evidence bytes
  -> WP3 ComparisonRecord
  -> canonical comparison SHA-256
  -> faithful Markdown SHA-256
  -> package manifest SHA-256
  -> deterministic run receipt
  -> separate Human Return bound to comparison SHA-256
```

The manifest does not include itself or the receipt. The receipt binds the
manifest, comparison and report; verification reconstructs the expected
receipt exactly. The later Human Return is intentionally outside the machine
output manifest and is verified separately against the comparison.

## Privacy boundary

Only `SYNTHETIC` and `LICENSED_DEIDENTIFIED` packages are admitted. File-system
inventory is allowlist-based. Undeclared notes, metadata or additional files
cause rejection rather than accidental packaging. Nothing is uploaded and no
network, account, database, telemetry or cloud path is used.

## Replay boundary

The run receipt is deterministic and clock-free. A Human Return contains its
explicit Human-supplied timestamp. Once a Return exists, automatic rerun is
blocked; a new reviewed comparison requires a new package identity rather than
silent replacement.

## Excluded scope

WP4 does not establish benchmark performance, correct defect detection, Human
comprehension, product utility, demand, safety, recommendation quality or
product readiness. No arbitrary documents, LLM inference, UI, ORION call,
publication, deployment or external action is authorized.
