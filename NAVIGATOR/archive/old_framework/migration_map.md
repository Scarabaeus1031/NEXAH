# NEXAH Framework Migration Map
**Date:** April 15, 2026
**Purpose:** Traceability after cleaning the FRAMEWORK folder

## Migration Summary

### CORE
- FRAMEWORK/CORE_GEOMETRY/          → FRAMEWORK/NEXAH/geometry/

### APPLICATIONS
- FRAMEWORK/applications/           → APPLICATIONS/
- FRAMEWORK/models/                 → APPLICATIONS/models/
- FRAMEWORK/dynamical_models/       → APPLICATIONS/models/

### EXPERIMENTAL
- FRAMEWORK/explorer/               → BUILDER_LAB/experimental/
- FRAMEWORK/scripts/                → BUILDER_LAB/experimental/scripts/

### ARCHIVE
- FRAMEWORK/legacy/                 → navigator/archive/old_framework/legacy/
- FRAMEWORK/research/               → RESEARCH/ (top-level)

### TEMPORARY (not moved yet)
- FRAMEWORK/visuals/                → stays in FRAMEWORK/ for now (used in READMEs)

## Notes
- Nothing was deleted.
- All moves are only reclassifications.
- visuals/ remains in FRAMEWORK until all links are updated.

Last updated: 2026-04-15
