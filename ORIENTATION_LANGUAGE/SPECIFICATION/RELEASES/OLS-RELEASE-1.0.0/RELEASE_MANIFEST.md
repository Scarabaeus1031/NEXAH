# Orientation Language Specification — Release Manifest

| Manifest field | Value |
| --- | --- |
| Release ID | `OLS-RELEASE-1.0.0` |
| Suite version | `1.0.0` |
| Release date | 17 July 2026 |
| Architecture generation | Generation 1 — Phase 2D Canonical Architecture frozen by ADR-0001 |
| Manifest version | `1.0.0` |
| Publication set | Seven normative documents and one informative companion |
| Publication status | Published by inclusion in this approved release manifest |
| Prior release | None |
| Included extensions | None |
| Applicable errata | None |
| Applicable deprecations | None |
| Conformance test-suite version | OLS-5 document revision `1.0.0`; embedded Version 1.0 test registry |
| Traceability export version | OLS-I document revision `1.0.0`; `TRACE-000001`–`TRACE-000230` |
| Release authority | Orientation Language Specification Release Process — Phase 3J |
| Approval record | `OLS-RELEASE-1.0.0-APPROVAL` |
| Approval basis | Successful Phase 3J release verification and independent publication review |
| Manifest checksum | Detached SHA-256 recorded in `RELEASE_MANIFEST.sha256` |

## 1 Canonical publication declaration

This manifest fixes exactly one canonical Orientation Language Specification Version 1.0 publication. The released specification artifact set consists exclusively of the eight documents in Table 1. Each document is included once, under its existing Document ID, title, edition, revision, and content digest.

The text of every included document is byte-identical to its approved publication candidate. No embedded metadata, semantic content, identifier, ownership assignment, requirement, clause, annex, or trace record was changed during assembly.

The embedded document status remains part of the immutable candidate content. Release status is assigned externally: inclusion in this valid manifest records each included document as **Published** for `OLS-RELEASE-1.0.0`, consistently with OLS-6 Clause 21.

## 2 Included documents and content digests

### Table 1 — Canonical released documents

| Publication ID | Document ID | Title | Edition | Revision | Release status | Role | SHA-256 |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| `OLS-PUB-1.0.0-OLS-0` | `OLS-0` | Specification Conventions and Suite Overview | 1 | `1.0.0` | Published | Normative | `4be9c059362e10cb7b8d29f75225bc05c9458af1b453ed0d5a64c30b4d30f157` |
| `OLS-PUB-1.0.0-OLS-1` | `OLS-1` | Universal Base Language | 1 | `1.0.0` | Published | Normative | `fe1e71aed19be46fe62c99219c599ec470c1becebce1e3b6ab0fcc5230a2c7dc` |
| `OLS-PUB-1.0.0-OLS-2` | `OLS-2` | Declarations and Operator Contracts | 1 | `1.0.0` | Published | Normative | `77358857c7eaea1db36e501d2a53bfa194a5f264b6608fb88d38ca000028ede7` |
| `OLS-PUB-1.0.0-OLS-3` | `OLS-3` | Semantic Profiles and Composition | 1 | `1.0.0` | Published | Normative | `a06a15a291c3cbdb2206ec658442ec4c02ed0ee76a796896a7de1a3e94cb836d` |
| `OLS-PUB-1.0.0-OLS-4` | `OLS-4` | Derivations and Semantic Transitions | 1 | `1.0.0` | Published | Normative | `c1ed8f5b224829b03d19d1326fbfb6fc6f0f8d66a627ef741e7df0a32f6bfba4` |
| `OLS-PUB-1.0.0-OLS-5` | `OLS-5` | Conformance and Testing | 1 | `1.0.0` | Published | Normative | `726136a423d0e3f2ad21b5d775c3132303d9b1733cee34058f90b7e223440aed` |
| `OLS-PUB-1.0.0-OLS-6` | `OLS-6` | Extensions, Versioning, and Governance | 1 | `1.0.0` | Published | Normative | `05d8a8937d76f599c14302f15ac331998f6a26c6aabdfcfcaf7fda0feaf93454` |
| `OLS-PUB-1.0.0-OLS-I` | `OLS-I` | Informative Companion | 1 | `1.0.0` | Published | Informative | `0c40e2db39c09ccbcf96bba941ee54259eeb6219b731780b6b3770b754cb13ab` |

## 3 Dependency inventory

| Document | Normative dependencies | Informative dependencies |
| --- | --- | --- |
| `OLS-0` | None within suite | ADR-0001 and Phase 2D for rationale/traceability only |
| `OLS-1` | `OLS-0` | None required |
| `OLS-2` | `OLS-0`, `OLS-1` | None required |
| `OLS-3` | `OLS-0`, `OLS-1`, `OLS-2` | None required |
| `OLS-4` | `OLS-0`, `OLS-1`, `OLS-2`, `OLS-3` | None required |
| `OLS-5` | `OLS-0`, `OLS-1`, `OLS-2`, `OLS-3`, `OLS-4` | None required |
| `OLS-6` | `OLS-0`, `OLS-1`, `OLS-3`, `OLS-5` | ADR-0001 where architecture revision is evaluated |
| `OLS-I` | Applicable controlling parts `OLS-0`–`OLS-6` | ADR-0001 and retained research evidence |

All normative dependencies resolve to the exact revisions and digests in Table 1.

## 4 Registry versions and digests

Version 1.0 normative registries remain embedded in their owning documents. Their exact published content is therefore fixed by the owning-document digest; no detached registry export is assigned independent authority by this release.

| Registry group | Owner | Version | Container digest |
| --- | --- | --- | --- |
| Document and suite conventions registries | `OLS-0` | `1.0.0` | `4be9c059362e10cb7b8d29f75225bc05c9458af1b453ed0d5a64c30b4d30f157` |
| Universal concept and boundary registries | `OLS-1` | `1.0.0` | `fe1e71aed19be46fe62c99219c599ec470c1becebce1e3b6ab0fcc5230a2c7dc` |
| Declaration and primitive operator registries | `OLS-2` | `1.0.0` | `77358857c7eaea1db36e501d2a53bfa194a5f264b6608fb88d38ca000028ede7` |
| Profile, dependency, and primitive concept ownership registries | `OLS-3` | `1.0.0` | `a06a15a291c3cbdb2206ec658442ec4c02ed0ee76a796896a7de1a3e94cb836d` |
| Product, transition, derivation, and prohibited-derivation registries | `OLS-4` | `1.0.0` | `c1ed8f5b224829b03d19d1326fbfb6fc6f0f8d66a627ef741e7df0a32f6bfba4` |
| Conformance class, test, and status registries | `OLS-5` | `1.0.0` | `726136a423d0e3f2ad21b5d775c3132303d9b1733cee34058f90b7e223440aed` |
| Release, extension, change, version, and deprecation governance | `OLS-6` | `1.0.0` | `05d8a8937d76f599c14302f15ac331998f6a26c6aabdfcfcaf7fda0feaf93454` |
| Informative traceability export | `OLS-I` | `1.0.0` | `0c40e2db39c09ccbcf96bba941ee54259eeb6219b731780b6b3770b754cb13ab` |

## 5 Traceability summary

The publication contains:

- 204 unique stable Clause IDs;
- 820 unique Requirement IDs;
- 39 unique Annex IDs;
- 230 unique defined Trace IDs, `TRACE-000001` through `TRACE-000230`;
- 682 unique Test IDs in the embedded conformance material.

OLS-I Annex D provides an informative bidirectional index for all 230 Trace IDs. Normative trace authority remains with each owning document.

## 6 Compatibility statement

All eight included documents declare suite version `1.0.0`, edition 1, revision `1.0.0`, and the same architecture baseline. Their declared dependencies resolve within this release. No extensions, deprecations, errata, prior releases, or alternative architecture generations are included.

Compatibility is limited to the exact document set and digests in this manifest. A changed artifact, missing artifact, substituted digest, or conflicting dependency is not this release.

## 7 Publication approval

Approval record `OLS-RELEASE-1.0.0-APPROVAL` covers the exact manifest and artifact set assembled in Phase 3J. Approval is supported by the Release Verification Report and Independent Release Review in this package. It does not certify truth, usefulness, scientific validity, or implementation quality.

## 8 Citation information

**Suite citation:** *Orientation Language Specification, Version 1.0.0, OLS-RELEASE-1.0.0, 17 July 2026.*

**Part citation:** *Orientation Language Specification, [Document ID and title], Edition 1, Revision 1.0.0, in OLS-RELEASE-1.0.0, 17 July 2026, [stable clause/requirement/annex identifier where applicable].*

No DOI or external persistent citation identifier is assigned by this release.

## 9 Manifest integrity

The manifest checksum is intentionally detached to avoid a self-referential digest. `RELEASE_MANIFEST.sha256` records the SHA-256 of this exact manifest. `PACKAGE_SHA256SUMS` records all release-control artifacts other than itself and includes the manifest and all eight released documents.
