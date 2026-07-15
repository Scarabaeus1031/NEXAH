# NEXAH Library — Phase VIII Editorial Traversability

## Decision boundary

Phase VIII prepares human navigation. It does not alter Architecture v1.0,
Registry records, Proposal state, Operators, identities, or Series decisions.

No direct Are.na edit was performed. The connector remains GET-only, and the
human editor has not yet approved individual public modifications. This report
therefore provides a precise manual plan.

## Evidence

- Accepted Reader Policies: UQ-01 through UQ-06
- Source Snapshot: `arena-2026-07-15.yaml`
- Snapshot scope: 71 public Channels, 50 direct Channel connections
- Live Traversability check: `2026-07-15T21:28:52+00:00`
- Curated transitions: 15
- Directly walkable: 1
- Missing: 14
- Cleanup Queue: 16 pending actions, including 3 P0 and 13 P1

## Editorial finding

The Library already contains strong explanations and coherent Works. Its main
public problem is that editorial meaning and public movement are separated.

- START is a genuine entrance, but 79 blocks and 23 mixed Channel connections
  present too many routes before a new reader can choose a purpose.
- Visitor’s Guide explains how to navigate but contains no direct Channel
  continuation.
- FIELD GUIDE and several navigation hubs describe systems and layers but offer
  no direct exits into those layers.
- Accepted Beginner, Builder, and Research Journeys are conceptually complete,
  but only START → Visitor’s Guide is publicly walkable.
- Several Series are editorially ordered in GitHub but have no public Channel
  path expressing that order.

## Reader-first intervention

Use a small orientation layer at the top of START:

```text
Choose a path

Beginner → THE VISITOR’S GUIDE
Builder → THE OPERATOR
Research → FIELD ATLAS I — WATER
Atlases → NEXAH · SYSTEM ATLASES
```

Keep the existing exploratory material below this orientation layer under a
plain `Explore further` heading. Do not delete Works or reinterpret their
identity.

Beginner uses an existing connection and Builder is ACQ-006. The Research and
Atlases entrances are new Phase VIII recommendations (P8-R00A/B) and require
separate human approval before they are added.

At each accepted path transition, add one short label and one Channel
connection:

- `Continue →`
- `Next Volume →`
- `Builder Path →`
- `Bridge →`
- `Reference →`

The label describes reader purpose only. It is not metadata or a Registry
relationship.

## Index strategy

Use three levels:

1. **Primary entrance** — START offers Beginner, Builder, Research, and Atlases.
2. **Path guide** — Visitor’s Guide explains the paths and links to their first
   useful Work.
3. **Thematic hubs** — System Atlases, FIELD GUIDE, Whiteboard Series,
   Perspectives & References, and Relational Field remain specialized rooms.

Do not describe Operator Library, Language Atlas, or Atlas of Atlases as public
site indexes merely because their titles sound indexical. They remain Works.

## Editorial symbols

Do not introduce the proposed color-dot system during the first cleanup pass.
The current public Library already uses several unrelated symbols (`🜂`, `🧭`,
`◈`, `°°`, `Λ`). No accepted NEXAH color vocabulary was found in the reviewed
architecture. Plain labels are therefore clearer and less likely to create a
second uncontrolled visual language.

## Series policy

- Express only the four confirmed linear Series as ordered public routes.
- Keep Operator Series and Whiteboard Series editorially unsettled.
- Keep both Mathematica IV Channels unresolved.
- Keep XV Volumes I–II as the ordered core and three satellites unordered.
- Keep Odyssey 2040 intentionally unordered.

## Success measurement after manual edits

Run:

```bash
python -m nexah.library source-snapshot --output LIBRARY/review/source_snapshots/arena-<new-date>.yaml
python -m nexah.library traversability --all
python -m nexah.library editorial-diff --all
python -m nexah.library health
python -m nexah.library release-check
```

The first public pass succeeds when all 15 accepted transitions are direct
Channel connections, the Morphology residue is absent, and START exposes a
clear choice before its exploratory field.

## Current conclusion

**READY FOR HUMAN APPROVAL OF MANUAL ARE.NA EDITS**
