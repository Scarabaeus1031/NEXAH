# Recommended Repository Architecture

## Target tree

```text
NEXAH/
├── README.md
├── RESEARCH/
│   └── README.md
├── ORIENTATION_LANGUAGE/
│   ├── README.md
│   ├── OVERVIEW.md
│   ├── ARCHITECTURE.md
│   ├── NAVIGATION.md
│   ├── SPECIFICATION_GUIDE.md
│   ├── SPECIFICATION/
│   │   ├── README.md
│   │   ├── OLS-0/
│   │   │   ├── README.md
│   │   │   └── OLS-0_SPECIFICATION_CONVENTIONS_AND_SUITE_OVERVIEW_V1.0.md
│   │   ├── OLS-1/
│   │   ├── OLS-2/
│   │   ├── OLS-3/
│   │   ├── OLS-4/
│   │   ├── OLS-5/
│   │   └── OLS-6/
│   ├── COMPANION/
│   │   ├── README.md
│   │   └── OLS-I/
│   ├── REGISTRIES/
│   │   ├── README.md
│   │   ├── RELEASE_MANIFEST/
│   │   ├── TERMINOLOGY/
│   │   ├── OWNERSHIP/
│   │   ├── REQUIREMENTS/
│   │   ├── TESTS/
│   │   └── TRACEABILITY/
│   ├── EXAMPLES/
│   │   └── README.md
│   ├── VISUALS/
│   │   ├── README.md
│   │   ├── CANONICAL/
│   │   └── ARCHIVE/
│   ├── ARCHITECTURE_DECISIONS/
│   │   ├── README.md
│   │   └── ADR-0001_ORIENTATION_LANGUAGE_ARCHITECTURE_BASELINE.md
│   ├── CHANGELOG/
│   │   ├── README.md
│   │   └── MIGRATION_MAP.md
│   └── HISTORY/
│       ├── README.md
│       ├── STANDARDIZATION/
│       └── SPECIFICATION_DEVELOPMENT/
├── LIBRARY/
│   └── README.md
├── APPLICATIONS/
│   └── README.md
├── IMPLEMENTATIONS/
│   └── README.md
└── ARCHITECTURE/
    └── README.md
```

## Why this structure

- Normative parts are separated from the informative companion.
- Registries are discoverable without becoming duplicate definitions.
- Historical phases are preserved inside the subsystem history rather than mixed with current publication files.
- Architecture decisions remain close to the subsystem they govern.
- Applications and implementations are distinct: one defines a domain use; the other realizes execution.
- The top level exposes the five public paths without requiring knowledge of the project’s historical phases.

## Directory rules

| Directory | Admission rule | Exclusion rule |
| --- | --- | --- |
| `RESEARCH/` | Evidence, hypotheses, experiments, datasets, research code, research reports | Published OLS definitions |
| `ORIENTATION_LANGUAGE/` | OLS suite, companion, registries, subsystem decisions, navigation | General research and Library works |
| `LIBRARY/` | Books, collections, reader journeys, editorial metadata, public communication | Normative semantics and runtime implementations |
| `APPLICATIONS/` | Domain-specific uses, policies, examples, configurations | Primitive ownership and core definitions |
| `IMPLEMENTATIONS/` | Software, schemas, adapters, test harnesses, repeatable procedures | Semantic authority |
| `ARCHITECTURE/` | Repository-wide decisions and domain boundaries | Subsystem content better owned locally |

## Canonical-copy rule

The target tree shall not contain both a phase-development copy and a release copy claiming current authority. Development records go to `HISTORY/`; release files go to `SPECIFICATION/` or `COMPANION/`. A release manifest maps each Document ID to exactly one current path and checksum.

