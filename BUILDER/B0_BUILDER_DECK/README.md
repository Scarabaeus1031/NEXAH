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
- `achievements.html` — regenerierbarer Größen- und Werkbestand-Snapshot mit
  Repository-, Commit-, Datei-, Datenvolumen- und Registerzahlen;
- `build-ecosystem-achievements.mjs` — erzeugt die source-bound JSON- und
  Direct-file-JavaScript-Snapshots für die Achievements-Seite;
- `systems-desk.html` — system roles, working inventory and technical map;
- `build-desk.html` — Chore projection, decisions, build cuts, returns and the
  fifteen-entry `Latest Builds` inspection log;
- `public-field.html` — Public Desk: nexah.de, NEXAHEDRON and Scarabæus;
- `public-nexahedron-page-shelf.html` — generated source-bound shelf for all 75
  HTML pages and runtimes in the current NEXAHEDRON A0 Human View, including
  surfaces not directly linked from the Aperture Journey;
- `build-nexahedron-page-shelf.mjs` — regenerates that shelf from the owning
  NEXAHEDRON source without copying or reclassifying its content;
- `a0-tools.html` — A0 Builder Desk, Builder Log and the
  direct Instrument Atlas / Latest Builds routes plus the explicit return to
  the A0 Science Desk.
- `archive.html` — searchable map of logs, releases, inventories and backlogs.
- `project-a0-pentagon-body-return.html` — source-bound Builder project for the
  Pentagon/Lantern body, projection ambiguity and explicit return path; the
  full gate plan lives in `PROJECT_A0_PENTAGON_BODY_RETURN_2026-10-25.md`.
- `PROJECT_THE_MACHINA_EXHIBITION_2026-10-26.md` — parked source-bound project
  brief for the existing THE MACHINA exhibition, Machine Series, Parts Shelf
  and explicit Human Return; no build or publication activation.
- `PROJECT_NEXAH_DE_DESIGN_DELTA_2026-10-26.md` — parked review brief for the
  unfinished NEXAH.de design worktree: preserve its visual/editorial strengths,
  replace the obsolete navigation and reconcile its A0 door before any build,
  commit or deployment decision.
- `project-scarabaeus-living-workshop.html` and
  `PROJECT_SCARABAEUS_LIVING_WORKSHOP_2026-10-27.md` — source-bound visual
  dossier and active-cut project brief for the existing SCARABÆUS 1033
  workshop. They bind the current repository, public-house role, shelf/work
  page architecture, Rödelheim Observatory and ten supplied direction boards
  without creating a second website identity. Source history remains in the
  Scarabäus repository; B0 records status, dispositions and returns.

The shared navigation keeps all six desks reachable without deep dropdowns.
The Architect Desk opens with the controlling Mission, a visual blueprint and
a compact source-bound work queue. The searchable Archive Desk binds 17
controlling or operational source documents without copying their authority.
Logs, release notes and backlogs remain at their owning sources.

## Parked design concept — NEXAH Aperture Compass

The proposed NEXAH mark remains a Builder idea, not an adopted logo or a new
brand identity. Its stable center may later carry a dynamic navigation halo:
circle as field, axes as position, angle as selected view, aperture as current
cut, depth arc as progress and an explicit Return. Any implementation must be
tested first as a small SVG/CSS navigation instrument before a separate Human
Owner brand decision.

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
