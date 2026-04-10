# NEXAH IEEE X-Ray Pipeline

## Overview
The NEXAH IEEE X-Ray Pipeline transforms classical power system simulations into a low-dimensional geometric state space for structural analysis and experimental control.

The pipeline follows the transformation:
simulation → feature extraction → geometric state space → structural analysis → control attempts

It includes:
- Diagnostic pipeline (v1–v13)
- Experimental controllers (v14.x series)
- Root Cube navigation experiments (v31–v36)
- Evaluation on IEEE test systems

## Current Status (April 2026)

**Detection Layer:** Functional  
NEXAH detects structural precursors of instability earlier than classical voltage-based methods in tested IEEE systems.

**Controller / Navigation Layer:** Experimental  
Attempts to stabilize trajectories and achieve orbit-like behavior have shown measurable improvements in coherence, but sustained orbit formation and gate locking have not yet been achieved.

## Key Technical Elements

- Low-dimensional state space (coherence, switch signal, radius, phase angle)
- Polar and 3D (Root Cube) projections
- Experimental feedback controllers (v14 series)
- 3D geometric navigation experiments (v31–v36)

## Root Cube Navigation (v31–v36)

This series explores a 3D projection with the following coordinates:
- Radius
- Phase angle (θ)
- Distance to structural axis
- NCS proximity (gate score)

**Measured Results (v36b_good_final):**
- Mean coherence: 0.9512
- Mean distance to elastic axis: 2.3401
- Max NCS proximity: 0.0000
- Escape count: 300

Visuals:
- 3D projection
- Polar view
- Time series

## Limitations

- Navigation (sustained orbit and gate locking) has not yet been achieved.
- Physical coupling between geometric state space and real grid variables is still basic.
- Results are internally consistent but require further validation against classical stability methods.

## Next Steps

- Improve physical mapping and test response to realistic load and topology changes
- Develop quantitative benchmarks against standard power system stability tools
- Formalize metrics for structural stability and coherence

This pipeline serves as an experimental platform to investigate geometric and structural approaches to power system dynamics.
