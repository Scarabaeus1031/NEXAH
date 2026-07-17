# Rollback Plan

## Purpose

Rollback reverses repository integration paths and navigation only. It never rewrites released content.

## Recovery sources

| Recovery need | Source |
| --- | --- |
| Immutable release | Phase 3J source at `orientation-language/09_PHASE_3_SPECIFICATION/10_PHASE_3J_RELEASE_ASSEMBLY/OLS-RELEASE-1.0.0/` |
| Pre-migration Phase 4A navigation | `outputs/10_PHASE_4A_ORIENTATION_LANGUAGE_INTEGRATION/ORIENTATION_LANGUAGE/` |
| Migration evidence | This changelog directory |

## Rollback sequence

1. Record the failing check and preserve the migrated target for forensic comparison.
2. Deactivate links to `SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/` by restoring the four modified Phase 4A navigation files from the Phase 4A output mirror.
3. Remove only the navigation files introduced by this migration from `SPECIFICATION/`, `COMPANION/`, and `REGISTRIES/`.
4. Remove only the migrated target directory after its content is verified against the Phase 3J source and retained there.
5. Retain this ledger, failure evidence, and checksum reports as history.
6. Re-run the repository link audit and confirm that the pre-migration Phase 4A state is restored.

## Exact rollback scope

- one target tree: `ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/`;
- four modified navigation files: `README.md`, `SPECIFICATION_GUIDE.md`, `ARCHITECTURE.md`, `NAVIGATION.md`;
- twelve new navigation README files under `SPECIFICATION/`, `COMPANION/`, and `REGISTRIES/`;
- this migration-record directory, retained rather than removed.

Rollback does not touch the Phase 3J source, delivery mirror, historical standardization files, prior Phase 4B controlled-stop record, or any released file content.

