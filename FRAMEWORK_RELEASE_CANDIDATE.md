# NEXAH Framework Release Candidate

## Status

**Prepared, unnamed, and not released.**

This package contains the release material that can be completed before the
release owner assigns the next Framework version and tag. It does not rename
or reinterpret any historical release.

## Release scope

The candidate publishes the maintained NEXAH Framework repository, including:

- the adopted Ecosystem Constitution v1.0 and Governance Index;
- the Framework architecture and six repository subsystems;
- Orientation Language specifications and registries;
- the Orientation Kernel implementation track currently declared as `0.7.0`;
- bounded Research, Applications, Library Registry and Editorial Operating
  System material; and
- repository verification, contribution, security and licensing records.

The candidate is not an ecosystem-wide version, ORION release, Experience
release, production-readiness declaration or universal scientific claim.

## Compatibility summary

| Surface | Candidate statement |
|---|---|
| Python | The maintained package declares Python `>=3.10`. |
| Kernel package | `nexah` remains on implementation track `0.7.0`. |
| Orientation Language | OLS versions retain their own release authority. |
| Constitution | Constitution v1.0 is governance, not a software version. |
| ORION | ORION keeps its independent version and exact Core pin. This candidate does not change that pin. |
| Experience | Experience consumes only explicitly recorded public baselines; it is not bundled. |
| Historical tags | `v0.5`, `v0.5.0` and `v1.0.0` retain their documented historical meanings. |

## Verification summary

Local verification on 21 July 2026:

```text
python -m pytest -q
302 passed, 164 warnings
```

Public CI evidence for public Governance commit `6ac32ec481e8932fd388fef1dd2dc2cfd2529117`:

- Python 3.10 smoke job: passed;
- Python 3.11 smoke job: passed;
- Python 3.12 smoke job: passed;
- full repository test job: failed after 49 minutes 26 seconds in
  `Run repository tests` with exit code 1.

The anonymous public API exposes no failing test name, and anonymous GitHub
access requires sign-in to view logs. Local execution of the same
`python -m pytest -q` command passes all 302 tests. The precise CI-only failure
must therefore be read from an authorized job log before any test or workflow
change is made.

The final release commit must receive a new complete green public CI run. A
local green run or partial public run is supporting evidence, not a substitute.

## Reproducibility

From a clean checkout of the final candidate commit:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
python -m pytest -q
python -m build
```

The release record must capture:

- the final commit SHA;
- Python and build-tool versions;
- CI run URL and conclusions;
- filenames, sizes and SHA-256 checksums of the source distribution and wheel;
- approved release name and tag; and
- known limits stated in the root README and `ARCHITECTURE/SYSTEM_STATE.md`.

## Artifact inventory

| Artifact | Authority | Publication condition |
|---|---|---|
| Git source snapshot | Framework repository | Exact approved commit |
| Python source distribution | Kernel implementation | Built from the approved commit |
| Python wheel | Kernel implementation | Built from the approved commit |
| Constitution v1.0 | Governance | Published unchanged from its canonical German source |
| Architecture and repository documentation | Owning Framework areas | Included as documentation, not promoted beyond current status |
| Research and validation records | Research | Provenance and evidence boundaries preserved |
| Release notes and checksums | Operations | Generated for the approved commit and release name |

Generated caches, local workspaces, credentials, model files, private research,
temporary outputs and independent ORION or Experience repositories are never
release artifacts.

### Wheel preflight

The package sources at local Framework commit `7daa0ecc…` were exported with
`git archive` and built outside the working tree without dependencies or build
isolation:

```text
nexah-0.7.0-py3-none-any.whl
157918 bytes
SHA-256 41128146de0c84ba20fa81761afd0b09abfc079f9bf00444bd64838663ba76e7
```

This proves the current package can produce a wheel in the available build
environment. It is preflight evidence only. The final wheel and source
distribution must be rebuilt and rehashed from the owner-approved release
commit after the release identity is assigned.

## Owner gate

The only unresolved semantic release field is the next Framework release name
and tag. After owner approval, Operations records that identity, publishes the
local commits, waits for green CI, builds and hashes the final artifacts, and
creates the release without rewriting prior tags.
