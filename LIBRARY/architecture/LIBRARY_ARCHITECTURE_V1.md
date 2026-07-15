# NEXAH Library Architecture v1.0

The NEXAH Library is a human-readable visual library with a small canonical
registry that can also support later Kernel navigation.

## Authority boundaries

- **Are.na** is authoritative for visual publication, descriptions, and
  editorial sequence.
- **The Canonical Library Registry** is authoritative for stable NEXAH
  identity, curated classification, Edition resolution, controlled Operator
  references, and curated relationships.
- **GitHub** is authoritative for code, technical specifications, validation,
  and formal definitions.
- **The Orientation Kernel** produces derived queries and suggestions. It may
  not silently overwrite canonical metadata.

## Object families

- `work`: books, atlases, guides, reports, visual essays, bounded notebooks
- `environment`: laboratories and ongoing research spaces
- `navigation`: entries, indexes, series, collections, and reading paths
- `asset`: reusable media and supporting artifacts
- `concept`: controlled semantic entities; v1.0 begins with Operators only

## Work model

```text
Work
└── Edition
    └── Part / Chapter / Page / Plate
```

Works receive typeneutral public IDs such as `NX-000002`. Operator Concepts
use the controlled namespace `NX-OP-0005`. Published Works resolve to a
specific current Edition such as `NX-000002-E01`.

## Classification

The following fields remain separate:

- `type`: structural kind, for example `book` or `atlas`
- `form`: editorial form, for example `handbook` or `field_atlas`
- `library_function`: reader-facing purpose, for example `foundation`,
  `practice`, or `research`
- `publication_status`: `working`, `published`, or `archived`
- `revision_state`: `draft`, `review`, `approved`, or `superseded`
- `content_maturity`: optional `exploratory`, `developing`, or `stable`

## Controlled relationships

The v1.0 Registry accepts a deliberately small relationship vocabulary:

`contains`, `member_of_series`, `continues`, `derives_from`, `applies`,
`maps`, `documents`, `implements`, `references`, `synthesizes`, `has_asset`,
`requires`, `recommended_next`, `supersedes`, and `related_to`.

## Kernel boundary

The Kernel may read the Registry to produce Reading Paths, Operator queries,
relationship graphs, and recommendations. Inferred occurrences and suggested
metadata remain a separate overlay until human confirmation.

Page-level semantic annotation is intentionally deferred until the work-level
pilot has been evaluated in practice.
