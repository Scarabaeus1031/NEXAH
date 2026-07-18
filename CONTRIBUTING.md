# Contributing to NEXAH

Thank you for helping NEXAH become clearer, more inspectable, and more useful.
NEXAH is an evidence-bound orientation ecosystem, so a contribution begins by
identifying which subsystem owns the proposed change and where that subsystem's
authority stops.

## Choose the responsible area

| Contribution | Responsible area |
| --- | --- |
| hypotheses, experiments, evidence, findings | [`RESEARCH/`](RESEARCH/README.md) |
| published semantics or conformance | [`ORIENTATION_LANGUAGE/`](ORIENTATION_LANGUAGE/README.md) |
| Python implementation or CLI behavior | [`nexah/`](nexah/README.md) |
| domain-specific realization or validation | [`APPLICATIONS/`](APPLICATIONS/README.md) |
| Works, identities, editions, or reader journeys | [`LIBRARY/`](LIBRARY/README.md) |
| editorial review, explanation, or controlled execution | [`EDITORIAL_OPERATING_SYSTEM/`](EDITORIAL_OPERATING_SYSTEM/README.md) |

Architecture documents describe relationships and current state. Governance
review does not create a seventh subsystem or provide a shortcut around the
authority of a responsible area.

## Before opening a change

1. Read the responsible subsystem's README and status boundaries.
2. State whether the change is research, proposal, implementation,
   documentation, validation, or canonical specification work.
3. Identify sources, assumptions, uncertainty, and affected authority.
4. Keep unsupported implications and known limits visible.
5. Do not promote experimental or informative material by changing its label or
   location alone.

Changes to OLS, canonical Registry identity, frozen architecture, or public
Are.na state require their own documented governance and explicit approval.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
```

For implementation-only work, `python -m pip install -e .` installs the current
runtime dependencies without the validation test extra.

## Contribution licensing

By submitting a contribution for inclusion in NEXAH, you agree that:

- software, tests, configuration, and implementation contributions are
  provided under the Apache License 2.0;
- original documentation and research contributions are provided under
  CC BY 4.0;
- third-party or source-derived material must retain its original license,
  attribution, and provenance and must be clearly identified; and
- you have the right to provide the contribution under the applicable terms.

See the complete [Licensing Scope](LICENSES.md) before contributing mixed or
externally sourced material.

## Pull requests

A pull request should explain:

- what changed and why;
- the responsible subsystem and status of the work;
- evidence or issue being addressed;
- tests or review performed;
- boundaries, exclusions, and unresolved questions;
- whether any generated artifact, identity, public state, or canonical text is
  affected.

Keep unrelated changes separate. Preserve earlier governed artifacts and
history rather than silently replacing them.

## Conduct and security

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Report
security-sensitive issues according to [SECURITY.md](SECURITY.md), not through a
public issue containing exploit details or credentials.
