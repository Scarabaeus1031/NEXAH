# Orientation Language

## Start here

Orientation Language is the NEXAH subsystem that specifies how bounded orientation is described. It provides a stable semantic foundation, declarations, operator contracts, profiles, derivations, conformance rules, governance, and informative guidance without turning research, communication, or implementation into semantic authority.

This directory is the public entry point for the subsystem. The canonical Version 1.0 publication is [OLS-RELEASE-1.0.0](SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/PUBLICATION_SUMMARY.md). Its manifest, documents, inventories, checksums, notes, and release reviews are preserved as one immutable release unit.

## Choose a path

| Visitor | Start | Continue |
| --- | --- | --- |
| General visitor | [OVERVIEW.md](OVERVIEW.md) | Public diagram in [VISUALS/README.md](VISUALS/README.md) |
| Specification reader | [SPECIFICATION_GUIDE.md](SPECIFICATION_GUIDE.md) | OLS-0, then the part owning the needed material |
| Researcher | [ENTRY_POINTS.md](ENTRY_POINTS.md#researchers) | Research sources and traceability, then the applicable OLS part |
| Developer | [ENTRY_POINTS.md](ENTRY_POINTS.md#developers) | OLS-2, OLS-3, OLS-4, and OLS-5 |
| Implementer | [ENTRY_POINTS.md](ENTRY_POINTS.md#implementers) | Operator contracts, active profiles, conformance tests, and OLS-I guidance |
| Repository maintainer | [REPOSITORY_ARCHITECTURE.md](REPOSITORY_ARCHITECTURE.md) | [MIGRATION_STRATEGY.md](MIGRATION_STRATEGY.md) and [CROSS_REFERENCE_STRATEGY.md](CROSS_REFERENCE_STRATEGY.md) |

## What belongs here

- the published Orientation Language Specification Suite;
- the informative companion associated with a declared suite release;
- controlled registries, manifests, and traceability indexes;
- subsystem architecture decisions and change history;
- clearly informative examples and diagrams;
- navigation and implementation guidance that cites its normative source.

## What does not belong here

- open research presented as normative language;
- Library books, reader journeys, or cultural collections presented as definitions;
- application-specific policies presented as universal semantics;
- software behavior presented as the source of an operator contract;
- historical visual vocabulary presented as current conformance material;
- duplicate or rewritten copies of normative OLS documents.

## Relationship to NEXAH

NEXAH is the wider ecosystem. Orientation Language is one independent subsystem within it. It does not replace NEXAH research, the Library, applications, or implementations.

| Domain | Primary responsibility | Boundary |
| --- | --- | --- |
| Research | Creates knowledge and preserves evidence, hypotheses, experiments, and uncertainty. | Research may inform the language but does not define published semantics. |
| Orientation Language | Describes orientation through the OLS suite. | It does not produce research findings, curate the Library, or execute applications. |
| Library | Communicates orientation through books, collections, reader paths, and cultural context. | It may cite the language but does not redefine it. |
| Applications | Realize orientation in declared domains and use cases. | They select applicable semantics but do not own them. |
| Implementations | Execute or support declared language operations. | Runtime behavior does not define semantic authority. |

## Authority

Normative authority belongs to the compatible OLS release identified by its release manifest. Directory paths and README files are navigation aids, not semantic authority. Stable Document IDs, Clause IDs, Requirement IDs, Trace IDs, Annex IDs, registry identifiers, and suite versions control references.

The Phase 2D Canonical Architecture and ADR-0001 remain the architectural baseline and rationale recorded for Version 1.0. Migration shall preserve every identifier and document identity byte-for-byte.

## Current publication

`OLS-RELEASE-1.0.0` is the current canonical publication. Use the [Specification Reader Guide](SPECIFICATION_GUIDE.md) for part-level navigation, the [Release Manifest](SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/RELEASE_MANIFEST.md) for publication identity, and the [Phase 4B migration record](CHANGELOG/PHASE_4B_CANONICAL_REPOSITORY_MIGRATION/) for repository integration evidence.
