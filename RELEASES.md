# NEXAH Release and Version History

This document explains the repository's existing version signals without
renaming tags, rewriting history or assigning one version to the whole NEXAH
ecosystem.

## Independent version scopes

NEXAH does not have one shared ecosystem version. Each released artifact is
versioned inside its own authority:

| Artifact | Current meaning | Version source |
|---|---|---|
| NEXAH Framework repository | Maintained source containing Framework, Research, OLS, Kernel and current Library Registry responsibilities | Git commit |
| Orientation Kernel implementation | Current Python implementation track | `pyproject.toml`: `0.7.0` |
| Orientation Language Specification | Canonical semantic release within the OLS scope | OLS release documents and OLS changelog |
| Ecosystem Constitution | Adopted governance baseline, not a software release | Constitution v1.0 |
| ORION | Independently versioned navigation repository | ORION `VERSION` and release records |
| Experience | Independently versioned presentation repository | Experience package and publication records |

A version in one row does not upgrade, release or certify another row.

## Existing repository tags

| Tag | Date | Historical meaning | Current interpretation |
|---|---|---|---|
| `v0.5` | 3 March 2026 | Engine v0.5 milestone with editable installation and an operational test suite | Historical implementation milestone |
| `v1.0.0` | 4 March 2026 | Annotated stable finite abstract-interpretation Kernel for its declared finite scope | Historical Kernel-scope tag; not Constitution v1.0 and not an ecosystem-wide release |
| `v0.5.0` | 23 April 2026 | Tag later used by the public “Research Prototype Release” | Historical research-prototype release |

The non-chronological tag numbering is retained as repository history. Existing
tags and releases are not moved or reinterpreted as current package versions.

## Current implementation version

`pyproject.toml` declares `nexah` version `0.7.0`. The root README names this as
the maintained Orientation Kernel implementation track. It does not mean:

- NEXAH Ecosystem v0.7;
- Constitution v0.7;
- OLS v0.7;
- ORION v0.7; or
- a production-readiness declaration.

## Next public baseline

The next Framework release is prepared as **NEXAH Framework 1.0** with the
distinct planned tag `framework-v1.0.0`. This identity applies only to the
Framework repository and does not reuse or reinterpret the historical
Kernel-scope `v1.0.0` tag. Before publication:

1. the intended artifact scope must be named;
2. the exact commit and test evidence must be recorded;
3. public CI must pass on that commit;
4. release notes must state limits and compatibility;
5. the release owner must approve creation of the annotated tag.

Constitution v1.0 may be published or referenced as a governance baseline under
an unambiguous name such as `constitution-v1.0`; doing so does not create a
Framework or Kernel `v1.0` release.
