# Visual Research Pass Plan

## Goal

Review research-oriented publication pages without mirroring the full Are.na
image corpus or converting visual language into unsupported semantics.

## Pipeline

1. Resolve a selected Work through its Publication Catalog record.
2. Create a temporary thumbnail/contact-sheet cache.
3. Visually triage every ordered Block into one visual role.
4. Mark `no_research_content` when appropriate; empty extraction is valid.
5. Open full resolution only for clearly eligible pages.
6. Record visible text and diagrams with exact Are.na Block provenance.
7. Preserve publication assertions as publication assertions.
8. Queue semantic records for human review; accept nothing automatically.
9. Recompute source fingerprints before reuse and mark changed/missing Blocks
   stale.

## Eligibility

Deep extraction is allowed only for a visible definition, research question,
method, model, labeled diagram, map, table, hypothesis, observation, evidence
statement, limitation, uncertainty, open question, implementation description,
explicit Concept, or explicit Operator. Decorative geometry, color, layout, and
symbolism are not semantic evidence unless explicitly labeled by the Work.

## Review batches

### Batch A — Foundation and field definition

- ORIENTATION SCIENCE
- ORIENTATION DESIGN — VOLUME II
- ORIENTATION THEORY — VOLUME III
- THE ARCHITECTURE OF ORIENTATION — VOLUME IV

Questions: Do they form an explicit or implied program? Which definitions,
methods, research questions, architectures, and claim boundaries are visible?
The allowed relationship statuses are `explicit`, `strongly_implied`, and
`editorial_proposal`.

### Batch B — Laboratory and research documentation

THE CARTOGRAPHY LABORATORY, DESIGNING ORIENTATION, selected Whiteboards, and
selected Field Atlases. Begin only after reviewing Batch A quality.

### Batch C — Mathematics and transition research

NEXAH MATHEMATICA I–IV, GEOMETRIA NOVA, and selected XV Atlases.

### Batch D — Broader atlas review

Begin only after the Research Structure workflow has been evaluated.

Journey Works remain outside semantic research extraction until a human editor
explicitly includes them.

## Image policy

- Temporary local caching is permitted outside the repository.
- Contact sheets or thumbnails are sufficient for triage.
- Full-resolution images are fetched only for selected eligible pages.
- The source URL remains authoritative; the record stores a SHA-256 fingerprint
  of source metadata and image URL.
- A changed fingerprint or missing Block is stale evidence.
- Source images are not committed by default.
- Derived transcriptions may be committed with exact Block provenance, review
  state, and claim boundary.
- Screenshots are retained only for a documented review discrepancy and after
  copyright/publication-integrity consideration.

## Human gates

Human review is required before accepting definitions, Operators, scientific
support claims, publication-series identity, Work dependency, evidence status,
or canonical relationships. Machine assistance can observe and propose;
authority remains human.

## Batch A acceptance criteria

- all 96 pages visually triaged;
- only a bounded subset deeply extracted;
- exact Channel and Block identities on every output;
- no duplicate Block records;
- stale-source checks pass;
- explicit null/empty values replace guesses;
- no Registry, Proposal, Operator, Kernel, or Are.na mutation capability;
- deterministic regeneration of machine-composed triage data;
- report distinguishes publication statements from supported repository
  findings.

