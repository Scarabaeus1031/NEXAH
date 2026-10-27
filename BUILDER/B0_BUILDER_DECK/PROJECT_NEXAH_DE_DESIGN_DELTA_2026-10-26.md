# NEXAH.de Design Delta

Status: `LIVE_BASELINE_ARCHIVED_REFERENCE / DRAFT_OWNER_REVIEW_ACTIVE / SOFTWARE_VERIFIED / BROWSER_ACCEPTANCE_OPEN / NO_DEPLOY`

Date: `2026-10-26`

Reused inventory identity: `BT-020 · NEXAH Experience`

## What this is

The current local Owner-review projection is generated from the canonical
NEXAH.de source checkout:

`40 EXPERIENCE PRODUCTION/NEXAH-Experience`

into:

`50 PUBLISHING/20 WEBSITE STAGING/nexah`

It is a substantial unfinished design draft for the public NEXAH house. It is
not an A0 page, not a second NEXAHEDRON homepage and not a new website
identity. The owning repository remains authoritative for NEXAH.de
presentation and routing.

## Owner disposition · 27 October 2026

The currently public NEXAH.de state is retained in Builder Desk as
`ARCHIVED REFERENCE / LIVE BASELINE`. This is a classification of the known
public state, not a copied website master, shutdown, rollback or deployment.
The public URL and the owning Git history remain the baseline evidence.

The local NEXAH Draft remains visible as the active Owner-review surface
because it still contains pages, navigation and information needed for the
next bounded cut. Editable source continues to live only in
`40 EXPERIENCE PRODUCTION/NEXAH-Experience`; the projection under
`50 PUBLISHING/20 WEBSITE STAGING/nexah` remains non-authoritative. This
disposition creates no new Navigator identity and changes no Science or
publication status.

The reviewed homepage and navigation delta currently exists as uncommitted
work on `main` above repository HEAD `040e24f`. Its exact changed paths are
`src/pages/index.astro`, `src/components/SiteHeader.astro` and
`tests/site.test.mjs`. The wider working tree contains other material, so a
future checkpoint must continue to select and review exact paths rather than
committing the entire tree indiscriminately.

## 27 October review checkpoint

The homepage now expresses NEXAH as an orientation space for knowledge and
retains the current live public navigation: `Start Here`, `Library`,
`Laboratory`, `Atlas of Atlases` and `About`. Existing routes and content have
not been removed; the draft changes the root entrance and its framing only.
The live `nexah.de` surface remains unchanged until a separate release gate.

Repository verification passes with the certified ORION source path:

- Astro diagnostics: `0` errors, warnings or hints;
- test suite: `59 / 59 PASS`;
- static build: `210` pages;
- internal-link check: no broken links.

The local staging projection is an Owner-acceptance view, not a second editable
website source and not evidence of deployment.

### Human Owner acceptance · 27 October 2026

The Human Owner accepts the current homepage direction and first-page
composition. The dark/black connective band is retained as the visual binder
that holds the public worlds together. This binder expresses relation and
shared orientation; it does not merge the identities, sources or authorities
of NEXAH, NEXAHEDRON, A0, Science Lab or Scarabæus.

This acceptance freezes the homepage concept and desktop first impression for
the next bounded cut. It does not yet accept narrow-width behavior, keyboard
and focus behavior, reduced motion, scientific wording review, commit, push or
deployment.

## Three-desk governance

| Role | Decision scope for this draft | Does not replace |
|---|---|---|
| Builder Desk / B0 | information architecture, interaction, responsive and accessibility checks, build integrity, exact source cut, rollback and release readiness | Science authority or Owner release decision |
| Science Desk / Science Lab | scientific wording, source bindings, evidence status, uncertainty, Claim Ceiling and the distinction between navigation, finding and publication | frontend implementation, portfolio priority or deployment custody |
| Mission Control / M-PUB01 | strategic fit, public-house roles, priority, cross-channel consistency and the Owner publication gate | source authority, repository ownership or scientific validation |

Any change to a scientific statement or public A0 Science representation must
return to the owning Science Desk / Science Lab record before release. This
review participation creates no new Study, Finding, Paper or research cycle.

## What is valuable in the draft

- the brighter editorial language and stronger public NEXAH voice;
- the mission-led homepage and Human-oriented explanation;
- the visual transition between NEXAH, NEXAHEDRON and Scarabæus;
- the attempt to make method, Library, Laboratory and public entrances feel
  like one house without collapsing their roles;
- the emerging bridge from public explanation into the bounded A0 Human View.

## The present delta

### Navigation

The earlier draft header and ecosystem rail were obsolete as a final
navigation decision. They were designed before the current separation of:

- NEXAH.de as public and intellectual home;
- NEXAHEDRON as the bounded Human Experience;
- A0 as a reference object with a distinct public projection and private
  working surface;
- Builder Desk, Science Desk and Mission Control as internal workspaces.

The current checkpoint now mirrors the live public menu while leaving internal
A0, Builder Desk, Science Desk and Mission Control routes outside the public
primary navigation. This is a reviewed local information architecture, not a
publication decision.

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

Goal: convert the verified local Owner-review checkpoint into one bounded,
reviewable release candidate without absorbing unrelated worktree changes.

Owning source: `40 EXPERIENCE PRODUCTION/NEXAH-Experience`

Proposed review sequence:

1. obtain Owner acceptance of homepage wording and the current live-menu cut;
2. obtain Science Desk / Science Lab review of scientific wording, source
   roles, uncertainty and Claim Ceiling;
3. complete Builder browser acceptance at normal and narrow width, including
   keyboard focus, reduced motion and route return;
4. classify the three changed source paths as `KEEP`, `ADAPT`, `RESTORE` or
   `UNRELATED` and prepare an exact path allowlist;
5. repeat the repository's complete `npm run verify` gate on that cut;
6. return the bounded candidate to M-PUB01 for the separate Owner release
   decision before any push or deployment.

Finish condition: a reviewed NEXAH.de source cut with current navigation,
preserved visual strengths, passing repository verification and an explicit
deployment hold or release recommendation.

## NEXAH Science / Laboratory projection · 27 October 2026

The existing public `Laboratory` route has now been rebuilt locally as the
curated NEXAH Science entrance. It projects the Science Desk position,
research fields, research architecture, programme doors and Cartography
reading into NEXAH.de without copying the Desk, Mission Control or A0 working
surface into the public site. It now also carries the bounded A0 public status
(`Results available`, `R2–R3 internal`, `Structure Freeze · 0 active`, next
gate `External review`) and names SCC-003, the rejected Euler-support route,
Return without identity and the operable comparison views as distinct result
types. The scientific source status remains the A0 synchronization of
24 October 2026; the website does not invent a newer evidence date. A0 /
Science Desk remains the scientific authority; the NEXAH pages are public
presentation and routing.

The bounded source change is:

`40 EXPERIENCE PRODUCTION/NEXAH-Experience/src/pages/laboratory/index.astro`

The same bounded status plate is projected on the public homepage through
`src/pages/index.astro`; it links back to the Laboratory rather than creating
a second result record.

Owner direction on 27 October 2026 resolves the visual/infrastructure split:
NEXAH.de is not to maintain a parallel house style beside A0. The website is a
reduced public A0 projection. Its existing Astro routes, Library, Atlas, legal
pages and build infrastructure remain useful delivery infrastructure; A0
supplies the public shell, visual tokens, status blocks and source-bound
Science projections. The first local cut therefore aligns the shared tokens,
Brand, header and footer to the A0 night/ivory/gold/cyan contract while keeping
all 210 routes intact. Internal Desks and Owner controls are not projected.

Direct verification of this page and its generated site passes: Astro reports
`0` diagnostics, the static build produces `210` pages, the internal-link
check reports no broken links, and the three Laboratory-specific software
tests pass. The complete repository gate is not reported as passing: its
certified ORION generation step currently stops because the configured frozen
ORION checkout is unavailable. That is a pre-existing source-path blocker,
not evidence against the Laboratory page and not permission to bypass the
generator in a release cut.

The local Owner-review projection was regenerated from the canonical checkout
into `50 PUBLISHING/20 WEBSITE STAGING/nexah`. The staging builder now prepares
that projection in a temporary sibling and replaces it atomically, excluding
iCloud conflict-copy filenames. This makes the projection replaceable and
keeps it non-authoritative; it is not another editable website source.

Observed browser scope: the normal and `700 px` layouts load, the hero remains
legible and the narrow layout stacks correctly. Full lower-page interaction,
keyboard/focus and final Owner wording acceptance remain open. The source is
uncommitted and unpushed; the live `nexah.de` page is unchanged.

The A0-public-shell cut passes Astro diagnostics (`0` errors/warnings/hints),
builds all `210` static pages and has no broken internal links. The repository
test suite is `49/50`; only the already recorded frozen-ORION-checkout path
blocks deterministic generation. This is not a total release PASS.

This extends the future exact-path review beyond the earlier homepage-only
three-path cut. It does not authorize staging unrelated dirty files, a push or
deployment.

## Boundary

This record creates no new Navigator identity, website, publication state,
release authorization or scientific claim. It reuses `BT-020`, records the
existing design delta and keeps implementation authority in NEXAH-Experience.

## Source-Werk correction · 27 October 2026

The Human Owner has closed the parallel-design route. Public NEXAH Science is
now built as a manifest-bound export from the canonical A0 Book rather than as
independently maintained Astro page content. Builder retains responsibility
for packaging, browser acceptance, retained Library/legal routes, rollback and
deployment, while Science Desk / Science Lab retains the exported wording,
evidence classes and Claim Ceiling. Mission Control retains the release gate.

The first exporter admits `14` existing A0 pages and writes a receipt for `94`
files. Private Desk, Backlog, Builder and Mission-Control destinations remain
in the A0 source graph but are not emitted as public routes. The local Owner
preview passes its software gate; commit, push, live route replacement and
Library/legal migration remain separate and open.
