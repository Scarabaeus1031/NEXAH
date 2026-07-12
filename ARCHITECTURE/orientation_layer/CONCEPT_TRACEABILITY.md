# Concept Traceability

This table prevents conceptual vocabulary, architecture, and implementation
from being treated as interchangeable.

| Concept | Technical identity | Current realization | Status | Next action |
|---|---|---|---|---|
| Orientation | Evidence-aware process for locating and relating possible action | Repository framing plus typed contracts | Partially implemented | Generate and validate reports |
| Q° Orientation Core | Contextual orientation and reporting boundary | `nexah/orientation/` contracts | Contract layer implemented | Implement report generation |
| JANUS | Complementary-perspective principle | Theory, books, and diagrams | Defined concept | Preserve symbolic identity |
| Janus Bridge | Translation between representations of one situation | Architectural concept | Planned | Specify interface and invariants |
| Janus Directional Coherence Operator | Forward/backward local-flow comparison | Research implementation(s) | Experimental | Audit names, tests, and evidence |
| Frozen v0.7 Engine | Locally fitted state-space and transition analysis | `nexah/core.py` plus `V07BackendAdapter` | Characterized and adapted | Keep frozen; validate reports above it |
| Demonstrator | End-to-end reference behavior | `PROTO_CORE/NEXAH_DEMONSTRATOR/` | Verified reference path | Use for MVP validation |
| Field reconstruction | Trajectory-to-field experimental methods | Proto Core and Architecture experiments | Experimental | Keep evidence and boundaries explicit |
| Orientation Report | Evidence-linked decision-support output | Typed contract implemented | Contract only | Implement evidence-bound generator |
| Episodic Memory | Outcome-linked storage and retrieval | Not implemented | Later | Prototype after MVP validation |
| Autonomous execution | Acting on external systems | Not part of current core | Out of MVP | Define separately if justified |

## Status vocabulary

- **Defined concept** — meaning is documented; no implementation is implied.
- **Planned** — accepted architecture work without a completed implementation.
- **Experimental** — implemented for research but not generalized or stable.
- **Implemented baseline** — available behavior with documented scope.
- **Verified reference path** — reproducible reference for a bounded claim.
- **Out of MVP** — deliberately excluded from the current delivery boundary.
