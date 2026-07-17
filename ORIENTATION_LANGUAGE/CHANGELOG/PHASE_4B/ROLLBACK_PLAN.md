# Rollback Plan

## Current rollback

No content file was moved, copied into a canonical target, renamed, or edited. Current rollback requires no repository-content operation. The created skeleton and migration reports are additive and non-authoritative.

## Rollback for resumed migration

1. stop cutover immediately on checksum, identity, link, registry, or uniqueness failure;
2. prevent new target paths from becoming public navigation targets;
3. move each executed target back to the exact ledger source path in reverse order;
4. verify the restored file against its pre-move SHA-256;
5. remove or deactivate redirects created by the failed migration;
6. restore the prior root and subsystem navigation pointers;
7. retain the failed migration ledger and verification evidence;
8. rerun source-area identity and link checks.

## Rollback evidence

Every resumed move must record source, target, timestamp, pre-move checksum, post-move checksum, reverse action, and verification result before cutover.

## Prohibited rollback behavior

Rollback shall not reconstruct files from excerpts, rewrite internal links, merge delivery copies, or choose among mismatched checksums by inferred intent.

