# NEXAH IEEE X-Ray Pipeline

X-Ray = structural projection of power system dynamics into geometric state space

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

## Extended Control Experiments (v51–v56)

Following the Root Cube experiments (v31–v36), the pipeline was extended toward  
**attractor-based control and event-driven navigation mechanisms**.

This phase introduces:
- discrete attractor regions (sector-based state partitioning)
- aperture conditions (state-dependent transition boundaries)
- event-triggered control (switching and crossing logic)

---

### Attractor-Based Control

**Versions:** v53, v54

- Introduction of angular sectors as discrete attractor basins
- Attractor force term added to control input
- Optional memory bias to reinforce trajectories

**Observed Behavior:**
- System rapidly collapses into a dominant attractor basin
- No spontaneous transitions between sectors
- High structural stability (closure metric ~0.63)

**Conclusion:**

> Attractor-based control improves stability but suppresses navigation.

---

### Aperture Crossing Dynamics

**Version:** v55

- Explicit definition of aperture conditions:
  - angular window
  - radial proximity
- Event-driven switching:
  - sector transitions triggered by aperture crossing
- Additional control components:
  - aperture term
  - exploration term

**Measured Results:**
- Switch count: 32
- Aperture events: 400
- Sector occupancy split across two regions (sector_4 / sector_5)
- Reduced stability:
  - lower coherence
  - lower OLGO proximity

**Conclusion:**

> Aperture crossing enables navigation but introduces instability.

---

### Aperture Pulse Regime

**Version:** v56

- Continuous aperture availability (always active window)
- Pulse mechanism introduced (time-dependent triggering)
- Increased memory bias
- Smooth control behavior

**Measured Results:**
- Mean coherence: ~0.9288
- Mean closure metric: ~0.6206
- Mean OLGO proximity: ~0.8350
- Switch count: 0
- Aperture pulses: 0
- Sector occupancy: 100% in single sector

**Critical Observation:**

- Aperture conditions are satisfied continuously
- No transitions are triggered

**Interpretation:**

> The system converges to a stable invariant trajectory within a single attractor basin.  
> Aperture conditions are no longer used for transitions.

---

### Key Findings

1. **Attractor Collapse**
   - System naturally converges into a dominant basin
   - Multi-attractor setups do not produce transitions without explicit forcing

2. **Navigation Requires Events**
   - Only event-driven logic (v55) produces sector transitions

3. **Stability vs Exploration Trade-off**
   - Stable regime → no switching (v53, v54, v56)
   - Exploratory regime → reduced stability (v55)

4. **Emergent Manifold Behavior**
   - In v56, the system stabilizes on a trajectory that satisfies:
     - closure conditions
     - attractor conditions
     - aperture constraints
   - without triggering transitions

---

### Implication

The system now exhibits three distinct operating modes:

- **Stabilization mode:** high coherence, no transitions  
- **Transition mode:** active switching, reduced stability  
- **Manifold lock mode:** stable trajectory without switching  

---

### Open Challenges

- Controlled switching between attractors
- Maintaining stability during transitions
- Avoiding permanent attractor lock

---

### Next Steps

- Introduce controlled transition triggers
- Develop hybrid controller:
  - stable manifold tracking
  - conditional aperture crossing
- Evaluate robustness under perturbations


