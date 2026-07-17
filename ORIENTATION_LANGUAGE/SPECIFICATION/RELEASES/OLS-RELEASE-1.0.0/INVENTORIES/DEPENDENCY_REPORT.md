# Dependency and Cross-reference Report

Release: `OLS-RELEASE-1.0.0`  
Report version: `1.0.0`

## Dependency closure

```text
OLS-0
├── OLS-1
│   └── OLS-2
│       └── OLS-3
│           └── OLS-4
│               └── OLS-5
├── OLS-6 (also depends on OLS-1, OLS-3, and OLS-5)
└── OLS-I (informative; references all controlling normative parts)
```

| Dependent | Required suite parts | Resolution |
| --- | --- | --- |
| `OLS-0` | None | Closed |
| `OLS-1` | `OLS-0` | Exact revision `1.0.0` included |
| `OLS-2` | `OLS-0`, `OLS-1` | Exact revisions included |
| `OLS-3` | `OLS-0`, `OLS-1`, `OLS-2` | Exact revisions included |
| `OLS-4` | `OLS-0`–`OLS-3` | Exact revisions included |
| `OLS-5` | `OLS-0`–`OLS-4` | Exact revisions included |
| `OLS-6` | `OLS-0`, `OLS-1`, `OLS-3`, `OLS-5` | Exact revisions included |
| `OLS-I` | Applicable `OLS-0`–`OLS-6` | All controlling parts included |

## Cross-reference audit

The audit compared stable Clause, Requirement, Annex, Trace, Test, Operator, Profile, Declaration, Term, Product, Transition, Derivation, and Conformance identifiers used in the package with their owning clauses or registries.

| Check | Result |
| --- | --- |
| Required Document IDs present | 8 of 8 |
| Required dependency revisions compatible | Pass |
| Stable Clause references resolve | Pass |
| Stable Requirement references resolve | Pass |
| Annex references resolve | Pass |
| Registry-owner references resolve | Pass |
| OLS-I controlling-document references resolve | Pass |
| Alternative or missing dependency detected | None |
| Duplicate semantic authority detected | None |

Plain-language references to architectural history and ADR-0001 remain informative dependencies; they are not required semantic publications and are not copied into the canonical eight-document set.

## Boundary statement

Repository paths are not dependency identities. Dependency resolution is fixed by Document ID, suite version, revision, publication ID, and digest in the Release Manifest.

