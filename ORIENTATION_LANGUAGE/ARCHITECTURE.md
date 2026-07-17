# Orientation Language Architecture

## Purpose

This document explains the layered subsystem architecture without redefining the Orientation Language. Normative meaning remains in the OLS suite.

## Layers

```mermaid
flowchart TB
  AUTH["Architectural authority<br/>Phase 2D baseline · ADR-0001 · governed revisions"]
  SUITE["Normative specification<br/>OLS-0 through OLS-6"]
  INFO["Informative companion<br/>OLS-I"]
  REG["Controlled publication infrastructure<br/>registries · manifest · traceability · changelog"]
  APP["Applications<br/>domain realizations"]
  IMP["Implementations<br/>software and repeatable human procedures"]
  LIB["Library<br/>communication and reader paths"]
  RES["Research<br/>evidence and hypotheses"]

  AUTH --> SUITE
  SUITE -. "explained by" .-> INFO
  SUITE --> REG
  SUITE --> APP
  SUITE --> IMP
  SUITE --> LIB
  RES -. "informs through governed change" .-> AUTH
  RES -. "supports rationale" .-> INFO
  APP --> IMP
```

Solid arrows express authority, governed realization, or publication dependency. Dotted arrows are informative. No arrow authorizes a lower layer to redefine an upper layer.

## Normative suite dependency

The canonical architectural dependency diagram for the published suite shall be derived from the Phase 3A complete dependency graph and maintained against the release manifest:

```mermaid
flowchart TD
  O0["OLS-0<br/>Conventions"] --> O1["OLS-1<br/>Universal Base Language"]
  O1 --> O2["OLS-2<br/>Declarations and Contracts"]
  O2 --> O3["OLS-3<br/>Profiles and Composition"]
  O3 --> O4["OLS-4<br/>Derivations and Transitions"]
  O4 --> O5["OLS-5<br/>Conformance and Testing"]
  O1 --> O6["OLS-6<br/>Extensions and Governance"]
  O3 --> O6
  O5 --> O6
  O0 -.-> OI["OLS-I<br/>Informative Companion"]
  O1 -.-> OI
  O2 -.-> OI
  O3 -.-> OI
  O4 -.-> OI
  O5 -.-> OI
  O6 -.-> OI
```

This is an editorial simplification of the existing complete graph. The release manifest and each document’s normative dependency metadata remain controlling.

## Ownership boundaries

| Concern | Owner | May reference | Shall not become |
| --- | --- | --- | --- |
| Universal semantics | OLS-1 | OLS-0 conventions | Research claim, Library metaphor, or implementation type |
| Declarations and primitive contracts | OLS-2 | OLS-1 | Profile-specific redefinition |
| Profiles and composition | OLS-3 | OLS-1 and OLS-2 | Universal semantics by activation |
| Derivations and transitions | OLS-4 | OLS-1 through OLS-3 | Workflow or causal guarantee |
| Conformance | OLS-5 | OLS-0 through OLS-4 | Truth, quality, safety, or performance certification |
| Evolution and release governance | OLS-6 | Frozen architecture and applicable OLS parts | Silent architecture revision |
| Explanation and implementation guidance | OLS-I | Any compatible normative part | Normative authority |

## Repository boundaries

- `SPECIFICATION/RELEASES/` contains complete immutable release units; part directories provide reader navigation to their one canonical released file.
- `COMPANION/` provides the explicitly informative OLS-I entry point without duplicating the release-contained document.
- `REGISTRIES/` exposes controlled indexes without duplicating definitions.
- `VISUALS/` contains informative diagrams with source and status metadata.
- `EXAMPLES/` contains examples linked to controlling Requirement and Test IDs.
- `CHANGELOG/` records releases and migration without rewriting historical records.
- `HISTORY/` preserves standardization phases, reviews, rejected alternatives, and superseded diagrams.
- repository-wide Research, Library, Applications, and Implementations remain outside this subsystem.

## Invariants

1. One released Document ID has one canonical file per suite release.
2. Stable IDs survive path changes unchanged.
3. A path is never the sole normative reference.
4. Informative material cannot fill a normative gap.
5. Applications and implementations report mappings; they do not own semantics.
6. Historical material remains accessible and visibly historical.
7. Migration is content-preserving and checksum-verified.
