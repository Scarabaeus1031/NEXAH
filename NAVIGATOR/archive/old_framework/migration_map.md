# NEXAH Framework Migration Map
**Date:** April 17, 2026
**Purpose:** Final traceability after cleaning the FRAMEWORK folder

## Final Migration Summary

### CORE (kept / integrated)
- FRAMEWORK/CORE_GEOMETRY/          → FRAMEWORK/NEXAH/geometry/
- FRAMEWORK/core/                   → nexah/core/ (after cleanup)

### APPLICATIONS (moved out)
- FRAMEWORK/applications/           → APPLICATIONS/
- FRAMEWORK/models/                 → APPLICATIONS/models/
- FRAMEWORK/dynamical_models/       → APPLICATIONS/models/

### EXPERIMENTAL (moved out)
- FRAMEWORK/explorer/               → BUILDER_LAB/experimental/
- FRAMEWORK/scripts/                → BUILDER_LAB/experimental/scripts/

### ARCHIVE (moved out)
- FRAMEWORK/legacy/                 → navigator/archive/old_framework/legacy/

### DOCUMENTATION (moved back / kept)
- FRAMEWORK/00_OVERVIEW.md          → FRAMEWORK/docs/00_OVERVIEW.md
- FRAMEWORK/system_stack.md         → FRAMEWORK/docs/system_stack.md
- FRAMEWORK/research/               → RESEARCH/ (top-level)

### TEMPORARY (not moved)
- FRAMEWORK/visuals/                → stays in FRAMEWORK/ for now (used in READMEs)

## Notes
- Nothing was deleted.
- All moves are only reclassifications to improve clarity.
- visuals/ remains in FRAMEWORK until all documentation links are updated.
- Two important overview documents (00_OVERVIEW.md and system_stack.md) were moved back into FRAMEWORK/docs/.

Last updated: 2026-04-17


# NEXAH Framework Migration Map
**Date:** April 17, 2026
**Purpose:** Final traceability after cleaning the FRAMEWORK folder

## Final Migration Summary

### CORE (kept / integrated)
- FRAMEWORK/CORE_GEOMETRY/          → FRAMEWORK/NEXAH/geometry/
- FRAMEWORK/core/                   → nexah/core/ (after cleanup)

### APPLICATIONS (moved out)
- FRAMEWORK/applications/           → APPLICATIONS/
- FRAMEWORK/models/                 → APPLICATIONS/models/
- FRAMEWORK/dynamical_models/       → APPLICATIONS/models/

### EXPERIMENTAL (moved out)
- FRAMEWORK/explorer/               → BUILDER_LAB/experimental/
- FRAMEWORK/scripts/                → BUILDER_LAB/experimental/scripts/

### ARCHIVE (moved out)
- FRAMEWORK/legacy/                 → navigator/archive/old_framework/legacy/

### DOCUMENTATION (moved back / kept)
- FRAMEWORK/00_OVERVIEW.md          → FRAMEWORK/docs/00_OVERVIEW.md
- FRAMEWORK/system_stack.md         → FRAMEWORK/docs/system_stack.md
- FRAMEWORK/research/               → RESEARCH/ (top-level)

### TEMPORARY (not moved yet)
- FRAMEWORK/visuals/                → stays in FRAMEWORK/ for now (used in READMEs)

## Additional ARCHY Internal Cleanup (April 17)
- FRAMEWORK/ARCHY/regime_mapper.py          → FRAMEWORK/ARCHY/core/
- FRAMEWORK/ARCHY/stability_models/         → FRAMEWORK/ARCHY/core/
- FRAMEWORK/ARCHY/ARCHY_ARCHITECTURE.md     → FRAMEWORK/ARCHY/docs/
- FRAMEWORK/ARCHY/archy_layer_principles.md → FRAMEWORK/ARCHY/docs/
- FRAMEWORK/ARCHY/ARCHY_SYSTEM_MAP.md       → FRAMEWORK/ARCHY/docs/
- FRAMEWORK/ARCHY/ARCHY_MODULE_INDEX.md     → FRAMEWORK/ARCHY/docs/
- FRAMEWORK/ARCHY/ARCHY_SIMULATION_CAPABILITIES.md → FRAMEWORK/ARCHY/docs/
- FRAMEWORK/ARCHY/ARCHY_UPDATE_v1.md        → FRAMEWORK/ARCHY/docs/

## Notes
- Nothing was deleted.
- All moves are only reclassifications to improve clarity and maintainability.
- visuals/ remains in FRAMEWORK until all documentation links are updated.
- Two important overview documents (00_OVERVIEW.md and system_stack.md) were moved back into FRAMEWORK/docs/.
- ARCHY was internally cleaned to better reflect its role as "Regime & Dynamics Layer".

Last updated: 2026-04-17
© Thomas K. R. Hofmann
