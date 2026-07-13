# Concept Traceability

This table prevents conceptual vocabulary, architecture, and implementation
from being treated as interchangeable.

| Concept | Technical identity | Current realization | Status | Next action |
|---|---|---|---|---|
| Orientation | Evidence-aware process for locating and relating possible action | Typed state, backend adapters, report generator, memory, and domain validation | Verified bounded vertical paths | Extend to a non-temporal graph representation |
| Q° Orientation Core | Contextual orientation and reporting boundary | `nexah/orientation/` contracts, generator, evidence, and memory attachment | Initial orchestration boundary verified | Refine semantics and calibrate uncertainty claim by claim |
| JANUS | Complementary-perspective principle | Theory, books, and diagrams | Defined concept | Preserve symbolic identity |
| Janus Bridge | Translation between representations of one situation | Architectural concept | Planned | Specify interface and invariants |
| Janus Directional Coherence Operator | Forward/backward local-flow comparison | Research implementation(s) | Experimental | Audit names, tests, and evidence |
| Frozen v0.7 Engine | Locally fitted state-space and transition analysis | `nexah/core.py` plus `V07BackendAdapter` | Characterized and adapted | Keep frozen; validate reports above it |
| Demonstrator | End-to-end reference behavior | Canonical Lorenz proxy connected through `validation/orientation_mvp/` | Reproducible proxy validation complete | Add external, independently labeled evidence |
| Field reconstruction | Trajectory-to-field experimental methods | Proto Core and Architecture experiments | Experimental | Keep evidence and boundaries explicit |
| Orientation Report | Evidence-linked decision-support output | Contract, generator, and `nexah orient` CLI | Verified for the v0.7 Demonstrator and scoped IEEE path | Add a graph-native report path |
| Episodic Memory | Outcome-linked storage and retrieval | Store, sequence-profile retrieval, immutable attachment, multi-episode benchmark | Memory V2 held-out synthetic validation complete | Add real outcome sequences and semantic relevance tests |
| Source Adapter Ecosystem | Evidence-preserving transport into representation layers | Array, table, directed graph, and coupled IEEE/Pandapower sources | Typed foundation implemented and tested | Add graph backend and an observed non-power domain case |
| Autonomous execution | Acting on external systems | Not part of current core | Out of MVP | Define separately if justified |

## Status vocabulary

- **Defined concept** — meaning is documented; no implementation is implied.
- **Planned** — accepted architecture work without a completed implementation.
- **Experimental** — implemented for research but not generalized or stable.
- **Implemented baseline** — available behavior with documented scope.
- **Verified reference path** — reproducible reference for a bounded claim.
- **Out of MVP** — deliberately excluded from the current delivery boundary.
