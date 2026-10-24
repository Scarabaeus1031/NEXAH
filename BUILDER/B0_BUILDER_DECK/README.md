# B0 · Builder Deck

Status: `LOCAL_OPERATIONAL_SURFACE / NO_RESEARCH_OR_RELEASE_ACTIVATION`

Date: `2026-10-24`

## Role

This is the owner-facing Builder Desk for the NEXAH software landscape. It
turns the existing Builder View, Vision, Atlas and Tool Inventory into a
navigable operating deck without copying their authority. A human can use it
to check Mission Control, direct the Builder Vision editorially, choose the
next build and retrieve the history behind an implementation.

The deck now uses a six-desk architecture. The start page is the operational
Architect Desk; deeper inventories and work surfaces live on their own pages:

- `index.html` — Architect Desk: Big Picture, priority, strategy and blueprint;
- `systems-desk.html` — system roles, working inventory and technical map;
- `build-desk.html` — Chore projection, decisions, build cuts and returns;
- `public-field.html` — Public Desk: nexah.de, NEXAHEDRON and Scarabæus;
- `a0-tools.html` — A0 Builder Desk, Builder Log and the
  explicit return to the A0 Science Desk.
- `archive.html` — searchable map of logs, releases, inventories and backlogs.

The shared navigation keeps all six desks reachable without deep dropdowns.
The Architect Desk opens with the controlling Mission, a visual blueprint and
a compact source-bound work queue. The searchable Archive Desk binds 16
controlling or operational source documents without copying their authority.
Logs, release notes and backlogs remain at their owning sources.

`BUILDER_POLICY.md` is the compact operating contract: one active cut, reuse
before creation, proportional checks, one writer on shared files, explicit
Return and a separate Owner gate for push, deployment or publication.

The `Public Integration / Three Houses` section locally projects the existing
`M-PUB01` release strategy into a Builder work path. It reuses the established
NEXAH, NEXAHEDRON and Scarabæus public identities and adds no Navigator node,
publication state or release authority.

```text
MISSION CONTROL
  strategy · priority · owner decision · release
       ↕
B0 BUILDER DECK
  editorial direction · software inventory · next-build selection · history
       ↕
OWNING SOURCES
  A0 · OLS · Kernel · ORION · Navigator · THE EYE · NEXAHEDRON
```

## Boundary

- no new research programme or Study;
- no new OLS semantics or processor capability;
- no claim that the ecosystem is already one integrated machine;
- no product, publication, deployment or external-utility claim;
- all source and implementation authority remains with the owning repositories;
- `B0` is a qualified working title for this surface and does not replace the
  existing Builder maturity label `B0 = idea`.

Open `index.html` directly or serve this directory with any static HTTP server.
