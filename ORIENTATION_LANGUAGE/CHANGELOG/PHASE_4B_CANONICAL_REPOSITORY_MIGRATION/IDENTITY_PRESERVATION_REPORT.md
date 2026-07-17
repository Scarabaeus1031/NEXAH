# Identity Preservation Report

## Release and manifest identity

| Identity | Source | Migrated target | Result |
| --- | --- | --- | --- |
| Release ID | `OLS-RELEASE-1.0.0` | `OLS-RELEASE-1.0.0` | Preserved |
| Manifest filename | `RELEASE_MANIFEST.md` | `RELEASE_MANIFEST.md` | Preserved |
| Manifest version | `1.0.0` | `1.0.0` | Preserved |
| Manifest SHA-256 | `90cc8d6579eb3e4ff3d2d48747886d0fe952810699208790e2622a77a0a83c0f` | Same | Preserved |
| Architecture generation | Generation 1 / ADR-0001 | Same | Preserved |

The release does not define a separate Manifest ID. Its manifest identity is the combination of Release ID, manifest version, filename, and detached SHA-256. No new Manifest ID was inferred.

## Stable identity counts

| Class | Migrated unique definitions | Duplicates | Result |
| --- | ---: | ---: | --- |
| Document IDs | 8 | 0 | Preserved |
| Clause IDs | 204 | 0 | Preserved |
| Requirement IDs | 820 | 0 | Preserved |
| Annex IDs | 39 | 0 | Preserved |
| Trace IDs | 230 | 0 | Preserved |
| Test IDs for OLS-0 through OLS-5 requirements | 682 | 0 | Preserved |

Trace IDs remain the contiguous range `TRACE-000001`–`TRACE-000230`. Every released filename and document byte stream matches the migration source.

## Authority preservation

The canonical target contains exactly one released file per Document ID. Part directories and registry directories contain navigation only. No ownership assignment, definition, metadata field, or stable identifier was rewritten during migration.

