# NEXAH Framework 1.0 Release Candidate

## Status

**Prepared and not released.**

**Framework identity:** NEXAH Framework 1.0

**Planned tag:** `framework-v1.0.0`

**Preparation date:** July 25, 2026

This release identity applies only to the maintained Framework repository. It
does not rename or reinterpret any historical release and does not synchronize
the versions of artifacts with independent authority.

## Scope

The candidate preserves the maintained NEXAH Framework repository, including:

- the adopted Ecosystem Constitution v1.0 and Governance Index;
- Framework Architecture and the six repository subsystem responsibilities;
- Orientation Language specifications, registries, and OLS 1.0.0;
- the Orientation Kernel implementation track declared as `0.7.0`;
- bounded Research, validation, Applications, Library Registry, and Editorial
  Operating System material;
- the non-authoritative Evidence Atlas; and
- repository verification, contribution, security, licensing, and review
  records.

The candidate is a canonical source baseline. It is not a production-readiness
declaration and does not complete active Research or Library work.

## Independent version authorities

| Surface | Candidate statement |
|---|---|
| Framework repository | Released as NEXAH Framework 1.0 from one exact Git commit |
| Orientation Language | OLS 1.0.0 retains its own semantic release authority |
| Orientation Kernel | `nexah` remains on implementation track `0.7.0` |
| Constitution | Constitution v1.0 remains an adopted governance baseline, not software |
| ORION | ORION retains its independent version and exact Core pin; it is not bundled |
| Experience | Experience retains its independent publication and package records; it is not bundled |
| Historical tags | `v0.5`, `v0.5.0`, and `v1.0.0` retain their documented historical meanings |

The planned `framework-v1.0.0` tag is intentionally distinct from the
historical Kernel-scope `v1.0.0` tag.

## Included components

- canonical repository documentation and current navigation;
- adopted Governance and maintained Architecture;
- released OLS material, unchanged by this preparation pass;
- current Kernel source and tests, without a package-version change;
- reproducible validation bundles and bounded application records;
- Research and historical artifacts at their existing local status;
- Library and editorial records at their existing local status;
- six completed independent reviews and the Identity Alignment Pass;
- this release-preparation record and the Evidence Atlas.

## Excluded components

- independent ORION and Experience repositories;
- public hosting, DNS, TLS, legal, and deployment state;
- generated caches, credentials, private workspaces, model files, and
  temporary outputs;
- unavailable external or conversational evidence;
- any new architecture, OLS semantics, scientific claim, or synchronized
  ecosystem version.

## Verification

Release-preparation verification on July 25, 2026:

```text
python -m pytest -q -p no:cacheprovider
302 passed, 162 warnings
```

The final candidate must also pass:

- Markdown structure and local-link validation;
- documentation entry-point and release-integrity checks;
- `python -m nexah.library release-check`;
- Python source compilation;
- source distribution and wheel construction;
- `git diff --check`; and
- complete public CI on the exact candidate SHA.

The immutable candidate SHA and public CI URL belong in the annotated tag and
public release record after CI completes. A local green run is supporting
evidence, not a substitute for green public CI on that SHA.

## Reproducibility

From a clean checkout of the candidate commit:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
python -m pytest -q
python -m build
```

The release record must capture:

- exact candidate commit SHA;
- Python and build-tool versions;
- CI run URL and conclusions;
- filenames, sizes, and SHA-256 checksums of the source distribution and
  wheel;
- approved release identity and tag; and
- known limits stated here and in `ARCHITECTURE/SYSTEM_STATE.md`.

## Artifact inventory

| Artifact | Authority | Publication condition |
|---|---|---|
| Git source snapshot | Framework repository | exact approved commit |
| Python source distribution and wheel | Kernel implementation | built from the approved commit; package remains `0.7.0` |
| Constitution v1.0 | Governance | included unchanged from its canonical source |
| OLS 1.0.0 | Orientation Language | included unchanged from its canonical release |
| Architecture and repository documentation | owning Framework areas | included without promotion beyond current status |
| Research and validation records | Research | provenance and evidence boundaries preserved |
| Evidence Atlas | cross-system documentation | navigation only; source areas retain authority |
| Release notes, checksums, and tag | Operations | generated for the approved commit and Framework identity |

## Known limitations

- The Kernel remains a bounded `0.7.0` implementation track rather than one
  unified runtime for every repository lineage.
- Research maturity remains uneven and locally declared.
- Reader effect, generalized Processor conformance, broad operational domain
  validity, and universal mechanisms are not established.
- Library direct traversability and twelve manual editorial cleanup actions
  remain open.
- POA, NTO, and DERIS/HYDRA evidence chains identified by Discovery Atlas
  Review 01 remain blocked because their authoritative primary sources are not
  repository-addressable.

## Prohibited interpretations

Framework 1.0 must not be described as:

- an ecosystem-wide synchronized version;
- a new OLS, Kernel, Constitution, ORION, or Experience release;
- general OLS implementation conformance;
- a universal scientific theory or mechanism;
- operational prediction, recommendation, authorization, or control;
- proof that visual recurrence establishes shared mathematics;
- completion of active Research or the Living Library.

## Remaining publication gate

After the candidate commit is created, Operations must:

1. verify the clean checkout and exact candidate SHA;
2. obtain a complete green public CI run on that SHA;
3. build the source distribution and wheel from that SHA;
4. record filenames, sizes, SHA-256 checksums, tool versions, and CI URL;
5. create the annotated `framework-v1.0.0` tag without moving or reusing any
   historical tag.
