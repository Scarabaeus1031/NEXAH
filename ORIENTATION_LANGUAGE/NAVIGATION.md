# Navigation Model

## Root journey

```text
START HERE
└── Choose one path
    ├── Research — evidence, hypotheses, experiments
    ├── Orientation Language — normative descriptions and conformance
    ├── Library — books, collections, reader journeys
    ├── Applications — domain uses
    └── Implementations — executable realizations
```

The repository root README should present these five choices before project history, internal phases, or detailed terminology.

## Orientation Language journey

```text
ORIENTATION_LANGUAGE/README.md
├── New visitor → OVERVIEW.md → public diagram → OLS-I
├── Specification reader → SPECIFICATION_GUIDE.md → OLS-RELEASE-1.0.0 → OLS-0 → selected OLS part
├── Researcher → ENTRY_POINTS.md → traceability → relevant OLS owner
├── Developer → OLS-2 → OLS-3 → OLS-4 → OLS-5 → OLS-I guidance
├── Implementer → claimed capability → contracts/profiles → tests → report
└── Maintainer → ARCHITECTURE.md → OLS-6 → CHANGELOG → release manifest
```

Current release: [OLS-RELEASE-1.0.0](SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/PUBLICATION_SUMMARY.md). Its [Release Manifest](SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/RELEASE_MANIFEST.md) controls publication identity and digests.

## Navigation principles

1. Show responsibility before content volume.
2. Present current publication before history.
3. Separate normative and informative links visually and textually.
4. Use reader intent rather than internal phase number as the first choice.
5. Never require the Library to locate the specification.
6. Never require the specification to understand repository history.
7. Provide one route back to the subsystem README from every local README.

## Breadcrumb model

Every subsystem page should show:

```text
NEXAH → Orientation Language → Zone → Document
```

Normative documents retain their own Document ID and metadata; the breadcrumb is editorial only.

## Cognitive-load controls

- The public entry page lists no more than five primary paths.
- OLS parts appear as a short ordered suite, not interleaved with reviews.
- Historical phases remain one link away under `HISTORY/`.
- Registries are grouped by function and accessed after the owning document.
- Each README states authority status, intended reader, and next step near the top.
