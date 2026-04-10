# NEXAH / Power Systems
**Structural Field Navigation for Power System Stability**

This module applies NEXAH’s orientation-based approach to power system stability analysis. The goal is to detect structural precursors of instability earlier than classical voltage-based methods and to explore geometric representations of system dynamics.

### Current Status (April 2026)

**Detection Layer:** Functional  
NEXAH detects the onset of voltage collapse **approximately 43.9 seconds earlier** than classical voltage-based methods in tested IEEE systems. This result is based on structural indicators (resonance deformation and coherence breakdown) and has been observed consistently across multiple test cases.

| Network                  | Lead Time vs. Classical Methods | Status          |
|--------------------------|---------------------------------|-----------------|
| IEEE 118-Bus             | ~43.9 s                         | Confirmed       |
| IEEE 300-Bus             | ~43.9 s                         | Confirmed       |
| IEEE 1354-Bus            | ~43.9 s                         | Confirmed       |
| IEEE 9241-Bus (PEGASE)   | ~43.9 s                         | Confirmed       |

**Navigation Layer:** Experimental  
Attempts to actively control and maintain stable orbits or phase-locked states are still under development and have not yet achieved sustained performance.

### Final Showcase – Detection Layer

![NEXAH Early Detection](stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)  
*NEXAH detects collapse approximately 43.9 seconds earlier than classical voltage-based methods*

![IEEE Scaling](stability_field_dynamics/iee_core_geometry/ieee_scaling/ieee1354_real_tunable_v12.7_4panel_iota_ring.png)  
*Structural behavior remains consistent across different grid sizes*

### Why this approach matters

Classical methods typically detect voltage collapse only after significant voltage degradation has already begun.  
NEXAH attempts to identify earlier structural changes:
- resonance deformation
- coherence breakdown
- drift in geometric state space

### IEEE X-Ray Pipeline (v1–v14.x)

The pipeline transforms IEEE simulation data into a low-dimensional geometric state space with the following variables:
- coherence (x)
- switch signal (y)
- radius (r)
- phase angle (θ)

**Visual Evolution**

**Early Structure Discovery (v1–v6)**  
![v3 detection](ieee_xray_pipeline/results/ieee57_pipeline_v3_detection.png)

**Polar Geometry (v6)**  
![v6 polar](ieee_xray_pipeline/results/ieee57_pipeline_v6_polar_morphology.png)

**Stability Band (v13)**  
![v13 band](ieee_xray_pipeline/results/ieee57_v13_band_polar.png)

**Controller Layer (v14 series)**  
![v14.5 stabilization](ieee_xray_pipeline/results/ieee57_v14_5_orbital_gate_polar.png)

**Root Cube Navigation (v31–v36)**  
![v36 3D](ieee_xray_pipeline/results/v36b_good_final_3d.png)  
![v36 polar](ieee_xray_pipeline/results/v36b_good_final_polar.png)

### Current Limitations

- The physical coupling between NEXAH structures and real grid variables (voltage, phase angle, load) is still basic.
- Navigation (sustained orbit formation, gate locking, stable rotation) has not yet been achieved.
- Results are internally consistent but require further validation against established stability metrics (e.g. PV curves, eigenvalue analysis, continuation power flow).

### Next Milestones

1. Improve physical coupling and test response to realistic load and topology changes
2. Develop quantitative comparison with classical stability methods
3. Formalize metrics for coherence and structural stability
4. Advance from stabilization toward sustained navigation

### Summary

NEXAH provides a structural, geometry-based perspective on power system dynamics.  
While early detection shows promising results, robust navigation and full physical validation remain open challenges.

**Author:** Thomas K. R. Hofmann  
April 2026
