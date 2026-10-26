# NEXAH.de Design Delta

Status: `PARKED_EXISTING_WORKTREE / REVIEW BEFORE BUILD / NO DEPLOY`

Date: `2026-10-26`

Reused inventory identity: `BT-020 · NEXAH Experience`

## What this is

`http://localhost:4323/` is the running development view of the canonical
NEXAH.de source checkout:

`40 EXPERIENCE PRODUCTION/NEXAH-Experience`

It is a substantial unfinished design draft for the public NEXAH house. It is
not an A0 page, not a second NEXAHEDRON homepage and not a new website
identity. The owning repository remains authoritative for NEXAH.de
presentation and routing.

The draft currently exists as uncommitted work on `main` above repository
HEAD `9463e4f60b53e665260c027a5d2618117acaf977`. Its working tree also contains
other material, so a future checkpoint must select and review exact paths
rather than committing the entire tree indiscriminately.

## What is valuable in the draft

- the brighter editorial language and stronger public NEXAH voice;
- the mission-led homepage and Human-oriented explanation;
- the visual transition between NEXAH, NEXAHEDRON and Scarabæus;
- the attempt to make method, Library, Laboratory and public entrances feel
  like one house without collapsing their roles;
- the emerging bridge from public explanation into the bounded A0 Human View.

## The present delta

### Navigation

The draft header and ecosystem rail are now obsolete as a final navigation
decision. They were designed before the current separation of:

- NEXAH.de as public and intellectual home;
- NEXAHEDRON as the bounded Human Experience;
- A0 as a reference object with a distinct public projection and private
  working surface;
- Builder Desk, Science Desk and Mission Control as internal workspaces.

The current draft must therefore be read as visual and editorial material,
not as the accepted site map.

### A0

The draft contains its own A0 route and NEXAHEDRON bridge. A0 has since gained
a different integrated navigation and public/private distinction. A later
NEXAH.de cut must compare these two states explicitly and choose one bounded
public A0 door. It must not expose the internal A0 Desk navigation or silently
copy the whole A0 surface into NEXAH.de.

### Source state

The working tree is not a release candidate merely because the development
server renders it. Source changes, generated output, tests, deployment state
and the live nexah.de page remain separate states.

## Next bounded Builder cut

Goal: preserve the strongest visual/editorial parts of the draft while
replacing its obsolete navigation with the current public-house model.

Owning source: `40 EXPERIENCE PRODUCTION/NEXAH-Experience`

Proposed review sequence:

1. compare the draft against live nexah.de and the current A0 public route;
2. classify each changed source path as `KEEP`, `ADAPT`, `RESTORE` or
   `UNRELATED`;
3. freeze the public information architecture before changing styling;
4. retain only one explicit A0 door and one NEXAHEDRON door;
5. preserve internal Science Desk, Builder Desk and Mission Control outside
   public navigation;
6. run the repository's complete `pnpm verify` gate;
7. prepare an exact reviewed commit path set;
8. return the result to B0 and Mission Control before any push or deployment.

Finish condition: a reviewed NEXAH.de source cut with current navigation,
preserved visual strengths, passing repository verification and an explicit
deployment hold or release recommendation.

## Boundary

This record creates no new Navigator identity, website, publication state,
release authorization or scientific claim. It reuses `BT-020`, records the
existing design delta and keeps implementation authority in NEXAH-Experience.
