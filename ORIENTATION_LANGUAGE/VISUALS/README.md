# Visual Architecture Review

## Scope reviewed

The local Phase 4A workspace contains five actual Mermaid diagrams across three Orientation Language documents:

1. Phase 2B directed reconstruction graph;
2. Phase 2D consolidated semantic dependency graph;
3. Phase 3A complete specification dependency graph;
4. Phase 3A architectural source mapping;
5. Phase 3A registry dependency graph.

The Phase 1 inventories cite thousands of external visual records, but those binary source assets are not present in this workspace. They were therefore not visually re-evaluated in Phase 4A. Their historical references remain preserved by the corpus extraction.

## Three canonical visual roles

### 1. Canonical ecosystem diagram

Use the ecosystem diagram in `OVERVIEW.md`:

```text
Research → Orientation Language → Library
                         ├──────→ Applications → Implementations
                         └────────────────────→ Implementations
```

Purpose: show repository responsibilities and interfaces. It is the canonical top-level ecosystem diagram.

### 2. Simple public explanation diagram

Use the universal process:

```text
OBSERVE → REPRESENT → COMPARE → ORIENT → EXPLAIN
```

Purpose: explain what the base language does without exposing the whole suite. Its caption must preserve the boundary that orientation does not imply recommendation, authority, execution, outcome, or learning.

### 3. Architectural dependency diagram

Use the simplified suite graph in `ARCHITECTURE.md`, derived from the Phase 3A complete dependency graph. The full Phase 3A graph remains the detailed historical/source diagram; the release manifest and document metadata remain controlling.

## Disposition of existing diagrams

| Existing visual | Public status | Target disposition | Reason |
| --- | --- | --- | --- |
| Phase 3A complete specification dependency graph | Source for canonical dependency visual | Preserve in history; derive maintained canonical release visual | Closest complete suite-level model; originally a drafting artifact |
| Phase 3A architectural source mapping | Supporting technical visual | Historical/traceability archive | Useful for provenance, not public navigation |
| Phase 3A registry dependency graph | Maintainer visual | Registry documentation or history | Too detailed for general entry; still operationally useful |
| Phase 2D consolidated semantic dependency graph | Frozen-baseline analytical visual | Architecture history | Describes the pre-specification architecture, not repository ecosystem |
| Phase 2B reconstruction graph | Historical analytical visual | Standardization archive | Contains provisional and pre-freeze relationships; not current public authority |

## Archival criteria for historical visuals

A visual moves to `VISUALS/ARCHIVE/` or the relevant historical phase when it:

- predates the architecture freeze;
- uses provisional profile or operator relationships;
- mixes research, metaphor, and normative semantics;
- duplicates a current canonical role;
- depends on obsolete paths or phase names;
- could be mistaken for normative authority.

Archival status does not mean deletion. Each archived visual retains source path, date, phase, status, and replacement link where applicable.

## Canonical visual metadata

Every maintained visual should state:

- title and visual role;
- informative status;
- source document and revision;
- compatible suite release;
- last reviewed date;
- maintainer;
- replacement/supersession history;
- text alternative.

