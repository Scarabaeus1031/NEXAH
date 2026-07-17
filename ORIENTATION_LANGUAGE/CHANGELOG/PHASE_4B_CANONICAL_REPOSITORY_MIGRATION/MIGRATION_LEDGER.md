# Phase 4B — Migration Ledger

Migration: Canonical repository integration of `OLS-RELEASE-1.0.0`  
Date: 17 July 2026  
Status: Completed and verified

## Migration plan and execution

| Stage | Planned action | Executed result | Gate |
| ---: | --- | --- | --- |
| 1 | Freeze and verify the Phase 3J release source | 21 release files verified against all three published checksum controls | Pass |
| 2 | Confirm permanent target absence and Phase 4A navigation skeleton | Target absent; part, companion, and registry entry directories available | Pass |
| 3 | Copy the complete release tree without transformation | Release copied to `ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/` | Pass |
| 4 | Compare source and target byte-for-byte | Recursive comparison reported no difference | Pass |
| 5 | Activate navigation without duplicating released documents | Root, specification, part, companion, and manifest entry points updated | Pass |
| 6 | Verify identifiers, dependencies, references, links, and checksums | All migration audits passed | Pass |
| 7 | Record rollback and independent review | Rollback source and removal scope documented; review passed | Pass |
| 8 | Cut over the subsystem entry point | `ORIENTATION_LANGUAGE/README.md` names the migrated release as current | Pass |

## Source and target

| Field | Path |
| --- | --- |
| Sole migration source | `orientation-language/09_PHASE_3_SPECIFICATION/10_PHASE_3J_RELEASE_ASSEMBLY/OLS-RELEASE-1.0.0/` |
| Permanent canonical target | `ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/` |
| Delivery mirror | `outputs/09_PHASE_3_SPECIFICATION/10_PHASE_3J_RELEASE_ASSEMBLY/OLS-RELEASE-1.0.0/` — non-canonical delivery copy |
| Migration evidence | `ORIENTATION_LANGUAGE/CHANGELOG/PHASE_4B_CANONICAL_REPOSITORY_MIGRATION/` |

## Artifact movement ledger

The release was copied as one directory unit. No released file was renamed, split, merged, regenerated, or edited.

| Artifact class | Files | Operation | Identity result |
| --- | ---: | --- | --- |
| Specification documents | 8 | Byte-preserving copy | Exact SHA-256 match |
| Release manifest and detached digest | 2 | Byte-preserving copy | Exact SHA-256 match |
| Document and package checksum inventories | 2 | Byte-preserving copy | Exact match |
| Release inventories | 4 | Byte-preserving copy | Exact match |
| Release notes, summary, and tree | 3 | Byte-preserving copy | Exact match |
| Phase 3J verification and review | 2 | Byte-preserving copy | Exact match |
| Total | 21 | Byte-preserving copy | Recursive source/target equality |

## Navigation changes

Navigation documents are outside the immutable release and were updated only to point to the canonical target. Seven OLS part READMEs, two Companion READMEs, two registry READMEs, and a specification index were added. No second OLS document body was created.

## Authority classification

The permanent target is the repository’s canonical path. The Phase 3J source remains the migration source record; `outputs/` remains a delivery mirror. Neither is exposed by current repository navigation as a second permanent publication location. Authority continues to derive from Release ID, manifest, versions, stable identifiers, and digests rather than path alone.

