# Specification Reader Guide

## Read OLS-0 first

OLS-0 defines suite-wide conventions, identifiers, normative status, citations, and reading paths. It is the entry point but does not own Orientation Language semantics.

## Choose the owning part

| Need | Read |
| --- | --- |
| Universal concepts, boundaries, or universal process | OLS-1 |
| Declaration values, omission, incompatibility, or primitive operator contract | OLS-2 |
| Profile activation, dependencies, composition, or profile-owned concepts | OLS-3 |
| Derivation, semantic product, transition, outcome, recording, or learning | OLS-4 |
| Conformance class, test, evidence, result, or report | OLS-5 |
| Extension, release, version, deprecation, or architecture-revision boundary | OLS-6 |
| Explanation, example, implementation guidance, history, or rationale | OLS-I, then verify the cited normative part |

## Authority rule

Definitions are read from their owning normative part. A registry, Library page, application, implementation, diagram, or OLS-I explanation cannot replace that definition.

## Citation form

A normative citation identifies at least the Document ID, stable element identifier, and compatible suite version. A path may be added for convenience but is not the authority key.

Example form:

```text
OLS-3, OLS3-REQ-0042, suite version 1.0.0
```

## Current workspace note

The canonical suite is published as [OLS-RELEASE-1.0.0](SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/PUBLICATION_SUMMARY.md). The immutable files are held once in its `DOCUMENTS/` directory. The OLS part directories and Companion directory provide stable reader entry points without duplicating the released documents.
