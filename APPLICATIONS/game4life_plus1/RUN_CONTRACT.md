# LIFE08 — Run Contract

```yaml
RECORD_ID: LIFE08-BOUNDARY-CYLINDER-v1
PURPOSE: REPLAY
SOURCE_REPOSITORY: NEXAH-Science-Lab
SOURCE_REVISION: current working tree; package hashes in SHA256_MANIFEST.txt
ENTRYPOINT: run-study.cjs
WORKING_DIRECTORY: SCIENCE_LAB/CASE_STUDIES/NEXAH_LIFE_BOUNDARY_CYLINDER_LIFE08_2026-10-11
ENVIRONMENT_SPEC: local Node.js, standard library only
RUNTIME_VERSION: Node.js >= 20
DEPENDENCIES: none outside Node.js standard library
INPUTS: PREREGISTRATION.json and deterministic fixture definitions
DATA_ACCESS: generated local finite cellular-automaton states only
LICENSE_AND_PRIVACY: no personal, licensed or network data
COMMAND: node run-study.cjs && node tests.cjs && node audit.cjs
EXPECTED_OUTPUTS: results/PRIMARY_RESULT.json; results/REPLAY_RESULT.json; results/LIFE08_VALIDATION_REPORT.json; results/study-results.js
EXPECTED_HASHES_OR_TOLERANCES: Primary and Replay must be byte-identical; all six frozen gates must pass
RESOURCE_BOUNDS: under 60 seconds; under 512 MiB; no network
NETWORK_REQUIRED: NO
FILESYSTEM_SIDE_EFFECTS: writes only declared result, validation and manifest files inside the Study package
FAILURE_SEMANTICS: any control, replay, roundtrip or equivariance failure yields INVALID_STUDY; outputs are retained
SCIENTIFIC_CLAIM_BOUNDARY: finite B3/S23 boundary comparison only; no Prime, universal Life, biology, physics or cross-domain mechanism claim
RESULT_REPORT: ../../LABREPORTS/SYNTHESIS/LABREPORT_LIFE08_BOUNDARY_CYLINDER_001.md
ISSUE_ROUTE: Human Owner through Mission Control
OWNER: Human Owner
LAST_VERIFIED: 2026-10-11
```

