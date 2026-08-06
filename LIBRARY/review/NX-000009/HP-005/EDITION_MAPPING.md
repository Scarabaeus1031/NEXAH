# HP-005 Edition Mapping and Proposed Execution Plan

Status: `PLAN ONLY — EXECUTION NOT AUTHORIZED`

## Current edition baseline

| Field | Current authority |
|---|---|
| Work | `NX-000009 — THE ATLAS OF ATLASES` |
| Edition | `NX-000009-E01`, version 1.0, approved |
| Published source | 72 Are.na elements |
| Reader sequence | 59 pages |
| Supplements | 13 source pages |

No HP-005 file is byte-identical to a current local edition asset.

## Mapping result

- 53 files are editorial candidates.
- 12 files are experimental or historical provenance.
- 11 files are duplicate or metadata held.
- 0 files are approved replacements.
- 0 files are approved supplements.
- 0 files are approved future-edition plates.

Functional overlap exists for Atlas architecture/index boards and for the
topics Memory, Prediction, Rhythm, Change, and Symmetry. Functional overlap is
not version identity.

OVS Parts I–III are treated only as an editorial visual series proposed inside
the Atlas handoff. They do not form an independent OVS Work or system.

## Count boundary

```text
HP-005 editorial proposal: 47 core plates

NX-000009-E01: 59 reader pages + 13 supplements = 72 source elements
```

The inventories have different purposes and no documented one-to-one mapping.
The source package also lacks a standalone `OVS_003` file.

## Destination

Source:

`/Users/tho2020/Desktop/00_INCOMING/ORION OVS _ orientation visual language/`

Future snapshot destination:

`/Users/tho2020/Documents/GitHub/NEXAH/LIBRARY/review/NX-000009/HP-005/source_snapshot/ORION OVS _ orientation visual language/`

Expected payload:

- 76 files;
- 138,431,870 bytes;
- 59 PNG visuals totaling 138,400,004 bytes;
- largest file 2,958,040 bytes;
- exact mappings and hashes in `SOURCE_MANIFEST.csv`.

## Repository and Git boundary

- PNG files are declared binary by `.gitattributes` and are not excluded.
- Git LFS is not configured or installed in this repository.
- No source file exceeds 2.83 MiB; Git LFS is therefore not required by an
  existing repository rule.
- The complete future payload would add approximately 132.02 MiB to a checkout
  and Git object storage if committed.
- `.DS_Store` and all CSV files are ignored by the current `.gitignore`.
- A future complete-snapshot commit would therefore require a separate decision
  to force-add the three `.DS_Store` files and the two manifests, or an explicit
  policy change. Neither is authorized by this plan.

## Proposed copy-first transaction

### Authority

- Transaction owner: Thomas.
- Accepting subsystem: NEXAH Library review and provenance.
- Edition authority remains unchanged.

### Preconditions

1. Separate Owner Execution Authorization exists.
2. Source contains exactly 76 files.
3. Every source SHA-256 matches `SOURCE_MANIFEST.csv`.
4. Snapshot destination contains no payload file.
5. Current Registry and edition paths are unchanged.
6. F011 and all unrelated Intake packages remain excluded.
7. Available disk space exceeds 276,863,740 bytes, allowing source and copy
   plus verification overhead.
8. Git treatment of ignored CSV and `.DS_Store` files is explicitly decided if
   a payload commit is requested.

Stop on any failed precondition.

### Copy phase

1. Copy the complete source package into the reserved destination without
   renaming, filtering, normalizing, or separating files.
2. Preserve the complete relative directory structure.
3. Do not use a merge mode. Any destination collision stops the transaction.
4. Do not remove the Intake source.

### Post-copy verification

1. Require exactly 76 destination files.
2. Require destination total size 138,431,870 bytes.
3. Compare every source and destination mapping in `SOURCE_MANIFEST.csv`.
4. Require 76 matching destination SHA-256 values.
5. Require all duplicate and metadata files to remain present.
6. Require `NX-000009-E01`, Registry, Are.na, ORION, OLS, F011, and unrelated
   Intake packages to remain unchanged.

Any mismatch triggers rollback.

### Rollback

Before source removal, rollback consists only of removing the newly created
destination payload after resolving its exact 76-file scope from the manifest.
The preparation documents remain as the transaction record unless the Owner
separately rejects them. The original Intake source remains the recovery copy.

No broad path, wildcard-only deletion, or source deletion is permitted.

### Source-removal gate

Copy verification does not authorize removal. After a successful copy, stop and
request a separate Owner Source-Removal Authorization. Only that later gate may
move or remove the verified Intake source. Permanent deletion is not implied.

### Commit boundary

1. Preparation documentation and source payload are separate commit scopes.
2. No commit is part of this plan execution unless separately authorized.
3. A preparation-only commit may contain the Markdown files; the CSV manifests
   are ignored and need an explicit force-add decision.
4. A payload commit must not include unrelated working-tree changes.
5. No push, deployment, publication, Registry update, Edition update, or Are.na
   update accompanies the snapshot transaction.

### M-INC01 and Control Desk updates

After a separately authorized and verified copy, update only:

- the HP-005 queue state;
- the M-INC01 incoming manifest final-path and verification fields;
- the move/copy ledger;
- the post-copy verification report;
- Decision Queue and Decision Log entries authorized by the Owner decision;
- Mission Control current action.

Do not mark HP-005 complete while the source-removal gate remains undecided.

### Owner Completion Review

The Completion Review must verify:

1. 76 source and 76 destination files;
2. 76 source and destination hash matches;
3. exact directory-structure preservation;
4. presence of all 11 held duplicate/metadata files;
5. empty collision report;
6. unchanged Registry and current edition;
7. unchanged Certified ORION and canonical OLS;
8. unchanged F011 and unrelated Intake packages;
9. no publication, push, deployment, or edition inclusion;
10. whether the source-removal decision remains open.

## Stop conditions

Stop immediately for a destination collision, missing source file, hash or size
mismatch, unexpected ignored-file loss, path normalization, unrelated working
tree inclusion, current-edition change, Registry change, authority leak, or any
attempt to discard duplicates or metadata.

Next permitted action: `OWNER REVIEW OF HP-005 EXECUTION PLAN`.
