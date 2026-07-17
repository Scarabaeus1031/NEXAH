# Migration Strategy

## Objective

Move the completed Orientation Language publication and its historical record into the target subsystem without changing specification content, stable identifiers, authority, or recoverability.

Phase 4A does not perform these moves. It defines the controlled migration sequence.

## Non-negotiable invariants

- OLS file bytes remain unchanged during relocation.
- Document IDs, Clause IDs, Requirement IDs, Trace IDs, Annex IDs, Test IDs, Profile IDs, Operator IDs, Declaration IDs, Term IDs, and Conformance IDs remain unchanged.
- One release manifest identifies one canonical path and checksum for each current suite part.
- Historical records remain recoverable.
- Old public links receive an explicit redirect or migration-map entry.
- No copied file becomes a second semantic authority.

## Preflight gate

Migration shall not start until all of the following are true:

1. final files for OLS-0 through OLS-6 and OLS-I are present;
2. each file’s Document ID, edition, suite version, status, and dependencies are internally consistent;
3. the release manifest can name exactly one candidate file per Document ID;
4. checksums are recorded for every candidate file;
5. Requirement, Trace, Annex, and registry identifier uniqueness checks pass;
6. OLS-5 requirement-to-test coverage remains complete after OLS-6 is added;
7. OLS-I is marked informative and cites a compatible normative release;
8. the repository root domains and write permissions are known.

The present workspace does not contain OLS-6 or OLS-I. This is a source-availability condition, not permission to synthesize them during migration.

## Migration stages

### Stage 1 — Inventory and freeze

- enumerate all current specification, companion, ADR, framework, review, registry, diagram, and historical files;
- assign each source exactly one target category;
- record size, checksum, current path, target path, status, and owner;
- freeze content edits for the migration window.

Exit condition: complete migration ledger with no unclassified artifact.

### Stage 2 — Create navigation shell

- create the target directories and README hierarchy;
- publish the root, subsystem, specification, companion, registry, visual, changelog, and history entry pages;
- do not copy normative files yet.

Exit condition: every target directory states purpose, authority, and admission rule.

### Stage 3 — Relocate canonical publication artifacts

- use history-preserving repository moves where possible;
- place each OLS part under its Document-ID directory;
- place OLS-I under `COMPANION/OLS-I/`;
- place ADR-0001 under `ARCHITECTURE_DECISIONS/`;
- do not alter file contents to repair links during this step.

Exit condition: pre- and post-move checksums match.

### Stage 4 — Relocate development history

| Current class | Target |
| --- | --- |
| Corpus extraction and Phase 1A review | `HISTORY/STANDARDIZATION/PHASE_1/` |
| Phase 2 through Phase 2D artifacts | `HISTORY/STANDARDIZATION/PHASE_2/` |
| Phase 3 Charter and Phase 3A framework | `HISTORY/SPECIFICATION_DEVELOPMENT/` |
| Phase-specific editorial reviews | `HISTORY/SPECIFICATION_DEVELOPMENT/REVIEWS/` |
| Rejected alternatives and pre-freeze graphs | corresponding historical phase directory |

Exit condition: every historical artifact has one visible status and no current-release authority claim.

### Stage 5 — Build registries and manifest views

- generate or relocate controlled registry views without copying definitions;
- map stable IDs to owning documents and current paths;
- record suite version, checksums, dependencies, and status in the release manifest;
- publish a bidirectional migration map.

Exit condition: every normative reference resolves by stable ID and compatible version.

### Stage 6 — Repair navigation references

- update README and repository navigation links;
- add compatibility redirects or path mappings for previously public paths;
- leave normative internal text unchanged unless a separately governed editorial release authorizes a link-only correction;
- classify every broken normative reference as a publication defect rather than inferring intent.

Exit condition: link checker passes for public navigation and all normative references resolve through stable IDs.

### Stage 7 — Verification

- compare checksums against the freeze ledger;
- rerun identifier uniqueness and OLS-5 coverage tests;
- verify exactly one canonical current copy per Document ID;
- verify OLS-I and visuals have no normative authority edge;
- inspect navigation for all five audiences;
- record results in the changelog.

Exit condition: all checks pass with no semantic-content diff.

### Stage 8 — Cutover

- make `ORIENTATION_LANGUAGE/README.md` the canonical subsystem entry;
- update the NEXAH root README to expose the five domain paths;
- mark old phase-based entry points historical or redirected;
- publish the release manifest and migration record together.

## Rollback

Rollback uses the freeze ledger and repository history. A failed migration restores paths, not rewritten content. Any checksum mismatch, missing artifact, duplicate current authority, unresolved stable ID, or OLS-5 coverage regression blocks cutover.

## Migration ledger fields

| Field | Purpose |
| --- | --- |
| Source path | Existing location |
| Target path | Proposed canonical or historical location |
| Document or artifact ID | Stable identity where available |
| Status | Normative, informative, historical, analytical, implementation guidance, or navigation |
| Suite version | Compatibility scope |
| Pre-move checksum | Content preservation proof |
| Post-move checksum | Verification |
| Redirect or mapping | Old-path continuity |
| Owner | Maintenance responsibility |
| Verification result | PASS, FAIL, INCOMPLETE, UNSUPPORTED, or NOT APPLICABLE where OLS-5 applies |

