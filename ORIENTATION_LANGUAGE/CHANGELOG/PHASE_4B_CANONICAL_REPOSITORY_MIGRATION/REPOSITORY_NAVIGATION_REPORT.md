# Repository Navigation Report

## Current visitor path

```text
ORIENTATION_LANGUAGE/README.md
├── General visitor → OVERVIEW.md
├── Specification reader → SPECIFICATION_GUIDE.md
│   └── SPECIFICATION/README.md
│       ├── OLS-0 … OLS-6 entry points
│       └── OLS-RELEASE-1.0.0 canonical files
├── Informative reader → COMPANION/OLS-I/README.md
├── Registry reader → REGISTRIES/README.md
└── Maintainer → CHANGELOG/PHASE_4B_CANONICAL_REPOSITORY_MIGRATION/
```

## Updated navigation files

| File | Migration change |
| --- | --- |
| `ORIENTATION_LANGUAGE/README.md` | Replaced pre-migration status with current release and migration links |
| `SPECIFICATION_GUIDE.md` | Replaced source-path guidance with canonical release guidance |
| `NAVIGATION.md` | Added current release to the specification-reader journey |
| `ARCHITECTURE.md` | Clarified immutable release-unit storage and navigation-only part directories |
| `SPECIFICATION/README.md` | Added suite index and release identity |
| `SPECIFICATION/OLS-0...OLS-6/README.md` | Added one canonical document link per part |
| `COMPANION/README.md`, `COMPANION/OLS-I/README.md` | Added informative companion entry path |
| `REGISTRIES/README.md`, `REGISTRIES/RELEASE_MANIFEST/README.md` | Added manifest and registry navigation without duplication |

## Domain boundary

The existing subsystem overview continues to distinguish Research, Architecture, Orientation Language, Library, Applications, and Implementations by responsibility. This migration changes only the Orientation Language publication location and navigation; it does not relocate or redefine the other domains.

## Result

Current navigation reaches every released document, the release manifest, publication summary, checksum controls, registry report, and migration evidence without traversing phase-development paths.

