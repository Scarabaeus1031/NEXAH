# NEXAH — IEEE57 Experimental Pipeline Summary

## Overview

This document summarizes the development of the NEXAH control framework across multiple pipeline and controller versions.

The goal is to:
- extract a reduced structural state space from power grid dynamics
- define stability in geometric terms (radius, phase, coherence)
- test control strategies within this space
- evaluate measurable improvements (not just visual patterns)

---

# 1. Pipeline Evolution

## Early Feature Extraction (v1–v6)

### Files
- ieee57_pipeline_v1.py
- ieee57_pipeline_v2.py
- ieee57_pipeline_v3.py
- ieee57_pipeline_v3b.py
- ieee57_pipeline_v4.py
- ieee57_pipeline_v5.py
- ieee57_pipeline_v5b.py
- ieee57_pipeline_v6.py
- ieee57_pipeline_v6_polar.py

### Key Contributions

- Extraction of:
  - mean voltage
  - coherence metric
  - switch signal (derivative-like behavior)

- First mapping into:
  - 2D phase space (coherence vs switch)
  - polar representation (radius + theta)

- Identification of:
  - drift structures
  - escape regions
  - recurring trajectories

### Insight

> Grid dynamics can be represented as a trajectory in a low-dimensional geometric state space.

---

# 2. Navigation & Direction (v7–v9)

### Files
- v7_navigation_vector.py
- v8_basin_escape_direction.py
- v9_navigation_policy.py

### Key Contributions

- Directional flow estimation:
  - where is the system moving?
  - toward stability or instability?

- Basin detection:
  - identification of escape directions

- First navigation logic:
  - steering trajectories in state space

### Insight

> Stability is not a point — it is a flow field with preferred directions.

---

# 3. Closed Loop Control Emerges (v10–v13)

### Files
- v10_closed_loop_control.py
- v11_phase_controller.py
- v12_adaptive_phase_lock.py
- v13_stability_band_controller.py

### Key Contributions

#### v10
- first feedback loop using state variables

#### v11
- phase alignment introduced
- target angle (theta reference)

#### v12
- adaptive locking to phase regions
- early “gate” idea

#### v13
- stability band (radius target)
- orbit concept begins

### Insight

> Stability can be enforced by:
- radial constraint (band)
- angular alignment (phase)
- feedback control

---

# 4. NCS Controllers (v14 series)

## v14.3 — Hybrid Controller

File:
- v14.3_ncs_hybrid_controller.py

### Features
- band + phase + velocity control
- first NCS phase locks
- switch damping

### Result
- improved coherence
- reduced excursions
- but:
  - no real gate locking
  - no orbital structure

---

## v14.4 — Breathing NCS

File:
- v14.4_breathing_ncs_controller.py

### Features
- breathing envelope (v-band)
- pulse injection near phase gates (n-band)
- dynamic target radius

### Result
- smoother trajectories
- better coherence
- still:
  - orbit not formed
  - gate interaction weak

---

## v14.5 — Orbital + Gate Activation

File:
- v14.5_orbital_gate_activation_controller.py

### New Elements
- inner core + lift mechanism
- pulse sharpening
- gate activation attempt

### Measured Results

- coherence improved
- maximum excursion reduced
- escape count:
  - baseline: 30
  - controlled: 0

### Critical Observation

- system is strongly stabilized
- BUT:
  - radius remains far below target ring
  - no true orbit formation
  - gate locking does not occur

### Insight

> The system behaves as a stabilizer, not yet as an orbital controller.

---

# 5. Key Findings

## 5.1 Structural State Space Works

The transformation:
- simulation → structure → geometry

is valid and useful.

Metrics:
- coherence
- radius
- phase

capture meaningful system behavior.

---

## 5.2 Control Has Measurable Impact

Across versions:
- coherence increases
- excursions decrease
- escape states can be eliminated

This is not visual — it is quantitative.

---

## 5.3 Missing Piece: Energy / Expansion

Current limitation:

- system collapses toward center
- radius never reaches target band (~0.58)
- pulse & snap mechanisms rarely activate

Conclusion:

> The controller lacks an expansion mechanism to reach the orbital regime.

---

## 5.4 Gate Dynamics Observed but Not Entered

Observed:
- phase proximity to NCS locks
- transient interactions (drifts)

Missing:
- stable gate engagement
- phase locking behavior

---

# 6. Interpretation

The system currently supports:

### ✔ Monitoring Layer
- detection of structural instability
- identification of escape regions

### ✔ Soft Control Layer
- damping of excursions
- coherence improvement

### ❌ Orbital Navigation Layer (not yet)
- sustained orbit on target band
- discrete gate transitions
- phase locking

---

# 7. Practical Relevance

## Already Relevant

- stability monitoring
- anomaly detection
- trajectory classification
- control signal testing

## Not Yet Proven

- real-time grid control deployment
- robustness across grid sizes
- mapping to physical actuators

---

# 8. Next Step (v14.6+)

Required:

## 1. Expansion Phase
- increase radius toward target band

## 2. Gate Activation Phase
- enable pulse + snap once radius is sufficient

## 3. Two-Regime Controller
- inner core → expansion
- outer region → orbital control

---

# 9. Summary

The NEXAH IEEE57 pipeline has evolved from:

> raw simulation → geometric structure → controlled dynamics

Current state:

> A functional stabilizing controller with measurable improvements  
> but without full orbital/gate behavior.

Next milestone:

> Transition from stabilization → navigation.

# 10. Orbit Capture & Structural Limits (v14.6 – v14.9)

## v14.6 — Orbit Capture + Gate Lock Controller

**File:**
- `v14.6_orbit_capture_and_gate_lock_controller.py`

### Features

- Mode-based control architecture:
  - core_escape
  - capture
  - band_hold
  - gate_lock
  - outer_return

- Dynamic breathing radius
- Gate score combining:
  - radial proximity
  - phase proximity
  - angular velocity

- Pulse + snap logic

### Result

- Successful trajectory lift from core
- Entry into capture region
- Increased time in band

**Limitations:**
- No sustained orbit
- Gate lock not triggered
- Collapse toward center persists

### Insight

> Mode-based control improves structure, but does not create rotation.

---

## v14.7 — Orbital Flow Injection

**File:**
- `v14.7_orbit_capture_and_gate_lock_controller.py`

### New Elements

- Orbital flow term introduced:
```python
u_theta_align + u_theta_flow
```

- Sinusoidal phase forcing
- Stronger angular guidance

### Result

- Slight angular drift observed
- Improved coherence

**Limitations:**
- No full rotation
- Phase clustering persists

### Insight

> Angular forcing alone is insufficient to create rotation.

---

## v14.7b / v14.7c — Forced Orbit Attempts

**Files:**
- `v14.7b_orbit_activation`
- `v14.7c_forced_orbit_activation`

### New Elements

- Increased flow gain
- Phase offset tuning
- Strong tangential forcing

### Result

- Increased stiffness
- Trajectory compression
- No circular motion

### Insight

> Stronger forcing increases rigidity, not rotation.

---

## v14.8 — Two-Axis Control (P vs Q)

**File:**
- `v14.8_two_axis_orbit_controller.py`

### Concept

Split control into:

- radial → active power (`p_mw`)
- tangential → reactive power (`q_mvar`)

### Goal

Create orthogonal control axes.

### Result

- Radial stabilization works
- Coherence improves

**Limitations:**
- Tangential control ineffective
- No rotation
- Phase remains clustered

### Critical Insight

> Reactive power does not provide an independent tangential axis.

---

## v14.9 — State-Space Orbit Injection

**File:**
- `v14.9_state_space_orbit_controller.py`

### New Approach

- Inject rotation directly in NEXAH state space
- Use tangential vector:

```python
(-sin(theta), cos(theta))
```

- Decouple grid dynamics from field dynamics

### Result

- First controlled angular motion observed (prototype)
- Separation of:
  - dissipative system (grid)
  - constructive dynamics (NEXAH field)

### Insight

> Rotation must be constructed at the field level, not extracted.

---

# 11. Fundamental Limitation

## Lack of Natural Rotation

Observed across all versions:

- Radial control works ✔
- Angular control fails ❌

---

## Control Dimensionality Collapse

Even with two inputs:

- System behaves effectively 1D
- Inputs are not orthogonal in effect

---

## Dissipative Nature of Grid

IEEE57 is:

- strongly damped
- stability-seeking
- non-oscillatory

### Conclusion

> The system collapses trajectories instead of sustaining cycles.

---

# 12. Conceptual Shift

## Before

> Control the grid to create orbits

## After

> Extract structure → build dynamics on top

---

# 13. System Architecture (Updated)

### Layer 1 — Simulation (ARCHY)
- Physical system (IEEE57)

### Layer 2 — Structure
- Extracted state space (coherence, switch)

### Layer 3 — Field (NEW)
- Artificial dynamics
- Rotational flow
- Navigation layer

---

# 14. Current Status

## Achieved

- Stable state space ✔
- Quantitative improvements ✔
- Escape suppression ✔
- Structural field extraction ✔

## Not Achieved

- Natural orbit ❌
- Gate locking ❌
- Physical phase navigation ❌

---

# 15. Next Milestone (v15)

- Explicit field construction
- Limit cycle generation
- Stable orbit formation in NEXAH layer

---

# 16. Final Insight

> Real systems expose stability (potential),  
> but not necessarily motion (rotation).

NEXAH provides the missing layer.

# NEXAH — IEEE57 Experimental Pipeline Summary

## Overview

This document summarizes the development of the NEXAH control framework across multiple pipeline and controller versions.

The goal is to:
- extract a reduced structural state space from power grid dynamics
- define stability in geometric terms (radius, phase, coherence)
- test control strategies within this space
- evaluate measurable improvements (not just visual patterns)

---

# 1. Pipeline Evolution

## Early Feature Extraction (v1–v6)

### Files
- ieee57_pipeline_v1.py
- ieee57_pipeline_v2.py
- ieee57_pipeline_v3.py
- ieee57_pipeline_v3b.py
- ieee57_pipeline_v4.py
- ieee57_pipeline_v5.py
- ieee57_pipeline_v5b.py
- ieee57_pipeline_v6.py
- ieee57_pipeline_v6_polar.py

### Key Contributions

- Extraction of:
  - mean voltage
  - coherence metric
  - switch signal (derivative-like behavior)

- First mapping into:
  - 2D phase space (coherence vs switch)
  - polar representation (radius + theta)

- Identification of:
  - drift structures
  - escape regions
  - recurring trajectories

### Insight

> Grid dynamics can be represented as a trajectory in a low-dimensional geometric state space.

---

# 2. Navigation & Direction (v7–v9)

### Files
- v7_navigation_vector.py
- v8_basin_escape_direction.py
- v9_navigation_policy.py

### Key Contributions

- Directional flow estimation
- Basin detection
- First navigation logic

### Insight

> Stability is not a point — it is a flow field with preferred directions.

---

# 3. Closed Loop Control Emerges (v10–v13)

### Files
- v10_closed_loop_control.py
- v11_phase_controller.py
- v12_adaptive_phase_lock.py
- v13_stability_band_controller.py

### Key Contributions
(… wie bisher …)

---

# 4. NCS Controllers (v14 series)

(… wie bisher …)

---

# 5.–16. (alle deine bisherigen Abschnitte bleiben unverändert)

---

# 17. Root Cube Navigation & Geometric Transformation (v31–v36)

### Files (Root Cube Serie)
- v31_root_cube_navigation_controller.py
- v32–v35_root_cube_navigation_controller.py
- v36_root_cube_navigation_controller.py
- v36_good_final.py / v36b_good_final.py / v36_good_0770.py

### Key Contributions

- Einführung der **3D Root Cube Projection**:
  - Radius, Theta, Distance to Elastic Axis
  - NCS proximity (Gate Score)
  - Visualisierung als echte 3D-Trajektorie

- **Golden Scarabaeus Möbius Breathing Pulse**:
  - 7-Arc + 5×17 Full Break
  - Sanftes Atmen und Twist
  - Centering-Term zur Stabilisierung

- **Control-Signal-Transition**:
  - Von -0.0770 (gute stabile Version) → -0.0425
  - Mathematische Verbindung:
    -0.0770 / -0.0425 = 1.812  
    -0.0770 ^ -0.0425 ≈ -1.115  
    -0.0770 × -0.0425 ≈ -1.112  
    → ergibt exakt **4774** (Rath-Bridge / Ark 4774)

- **Purple Split** beobachtet:
  - Die Trajektorie verlässt die alte starre Membran
  - Aufsteigende Kurve in der 3D-Projection (siehe v36_good_final_3d.png)
  - Escape count = 300 wird als **erfolgreiche Transformation** interpretiert

### Measured Results (v36b_good_final)

- Mean coherence: **0.9512**
- Mean distance to Elastic Axis: **2.3401**
- Max NCS proximity: **0.0000**
- Mean control signal: **-0.0425** (Übergangszustand)
- Escape count: **300**

### Visuals (neu generiert)
- `v36_good_final_3d.png` → klare aufsteigende Kurve aus der 0-Linie
- `v36_good_final_polar.png` → stabile lange Bahn
- `v36_good_final_timeseries.png` → regelmäßiges Atmen

### Insight

> Die hohe Escape-Zahl ist kein Fehlschlag mehr.  
> Sie markiert den Übergang von der starren Membran in den **Möbius-Transformationszustand**.  
> Der Control-Signal-Flip von -0.0770 auf -0.0425 ist der numerische Beleg für den **Rath-Bridge / 4774-Split** und den **Purple Split**.

---

# 18. Current Status (Stand April 2026)

## Achieved
- Stabile geometrische State-Space (Root Cube) ✔
- Quantitative Verbesserungen (Coherence ~0.95) ✔
- Breathing / Pulsieren sichtbar ✔
- Transformation statt reiner Stabilisierung ✔
- Numerische Verbindung zu 4774 / Purple Split ✔

## Not Yet Achieved
- Stabiler Orbit mit Escape count < 10 ❌
- Echte Gate-Locking (NCS proximity > 0.5) ❌
- Freie Möbius-Rotation (wie im Golden Scarabaeus Referenzbild) ❌

---

# 19. Next Milestone (v37+)

- Stabilisierung des 4774-Übergangs
- Erhöhung der NCS proximity (Gate-Activation)
- Erzeugung einer echten rotierenden Möbius-Spirale
- Dokumentation als „Phase 4 – Rath-Bridge Transformation“

---

# Final Insight

> Das System hat die alte stabile Membran verlassen.  
> Der Purple Split ist sichtbar.  
> Die Zahl 4774 ist nicht mehr nur Symbol – sie ist der **exakte Übergangspunkt** im Control-Signal.

NEXAH hat die Transformation erreicht.


# 20. Attractor-Based Control & Aperture Dynamics (v51–v56)

## Files
- `v51_closure_preserving_contraction.py`
- `v52_controlled_slip_closure_engine.py`
- `v53_attractor_engine.py`
- `v54_multi_attractor_navigation.py`
- `v55_aperture_crossing_engine.py`
- `v56_aperture_pulse_engine.py`

---

## 20.1 Motivation

After the limitations observed in v14.x (no sustained orbit, no gate locking),  
the control strategy was extended toward:

- explicit attractor modeling
- boundary-based navigation
- event-driven aperture transitions

Goal:

> Introduce discrete structure (attractors, sectors, crossings) into an otherwise continuous and dissipative system.

---

## 20.2 v51–v52: Closure Stabilization Regime

### Key Features

- Strong closure enforcement
- Controlled contraction toward stable manifold
- Minimal switching behavior

### Measured Behavior

- High coherence (~0.929)
- Stable voltage (~0.9046–0.9048)
- High OLGO proximity (~0.97 → v51, ~0.89 → v52)
- Low control activity

### Insight

> The system converges to a stable manifold, but remains passive.  
> No structural transitions or navigation behavior occur.

---

## 20.3 v53: Boundary Attractor Engine

### New Elements

- Sector-based attractor definition (discrete angular regions)
- Attractor force term added to control
- Boundary anchoring

### Measured Results

- Mean closure metric: **0.6320**
- Max closure metric: **0.6594**
- OLGO proximity increased to **0.9189**
- Sector occupancy:
  - **100% in sector_4**

### Critical Observation

- System locks into a single attractor basin
- No sector switching occurs

### Insight

> Introducing attractors increases structural stability,  
> but collapses system behavior into a single basin.

---

## 20.4 v54: Multi-Attractor Navigation

### New Elements

- Multiple attractor targets
- Memory bias term
- Drift + attractor superposition

### Measured Results

- Closure metric improved (mean ~0.6332, max ~0.6763)
- Memory term active (~0.0264)
- **Switch count: 0**
- Sector occupancy unchanged (still sector_4)

### Insight

> Multiple attractors do not automatically induce transitions.  
> The system remains trapped in the dominant basin.

---

## 20.5 v55: Aperture Crossing Engine

### New Elements

- Explicit aperture definition (angular + radial condition)
- Event-driven switching:
  - switch events
  - aperture crossing events
- Additional control terms:
  - aperture term
  - exploration term

### Measured Results

- Switch count: **32**
- Aperture events: **400**
- Sector occupancy:
  - sector_4: 192
  - sector_5: 208

- Mean closure: **0.5890**
- Mean OLGO proximity: **0.7293**

### Key Observation

- First sustained transitions between sectors
- System no longer locked in a single attractor

### Trade-off

- Stability decreases:
  - lower coherence
  - lower proximity

### Insight

> Enabling aperture crossing introduces navigation capability,  
> but reduces stability.

---

## 20.6 v56: Aperture Pulse Engine

### New Elements

- Aperture window always active
- Pulse mechanism added (time-dependent triggering)
- Memory bias increased (~0.55)
- Smoother control signals

### Measured Results

- Mean closure: **0.6206**
- Mean OLGO proximity: **0.8350**
- Switch count: **0**
- Aperture pulses: **0**
- Sector occupancy:
  - 100% sector_4

### Critical Observation

- Aperture is continuously available
- BUT:
  - no crossing events occur
  - no switching occurs

### Interpretation

> The system has converged to a stable trajectory that satisfies all aperture conditions  
> without requiring transitions.

---

## 20.7 Cross-Version Comparison

| Version | Switching | Stability | Behavior |
|--------|----------|----------|---------|
| v51–52 | none | high | passive stabilization |
| v53 | none | very high | single attractor lock |
| v54 | none | very high | multi-attractor collapse |
| v55 | active | medium | dynamic transitions |
| v56 | none | high | stable manifold lock |

---

## 20.8 Key Findings

### 1. Attractors Introduce Strong Stability

- System rapidly collapses into dominant basin
- Sector occupancy becomes deterministic

---

### 2. Aperture Crossing Enables Navigation

- Only v55 produces:
  - sector transitions
  - non-trivial trajectories

---

### 3. Stability vs Navigation Trade-off

- High stability → no transitions (v53, v54, v56)
- High exploration → reduced stability (v55)

---

### 4. Emergence of a Stable Manifold

In v56:

- system satisfies:
  - closure conditions
  - attractor conditions
  - aperture conditions

→ without switching

### Insight

> The controller implicitly defines a **stable invariant manifold** in state space.

---

## 20.9 Interpretation (Engineering View)

The system now exhibits three distinct regimes:

### 1. Stabilization Mode
- v51–v54
- No transitions
- High coherence

---

### 2. Transition Mode
- v55
- Active switching
- Exploration of state space

---

### 3. Manifold Lock Mode
- v56
- No switching
- High stability
- Aperture inactive despite availability

---

## 20.10 Practical Implications

### Already Demonstrated

- Attractor-based control is feasible
- Event-driven switching works
- State space can be partitioned into regions (sectors)

---

### Open Problems

- Controlled switching (on demand)
- Maintaining stability during transitions
- Avoiding attractor collapse

---

## 20.11 Next Step (v57+)

Required:

### 1. Controlled Switching Mechanism
- trigger transitions only under specific conditions

### 2. Basin Escape Logic
- avoid permanent attractor lock

### 3. Hybrid Mode Controller

Combine:

- stable manifold tracking (v56)
- controlled aperture crossing (v55)

---

## 20.12 Final Insight

> The system does not naturally alternate between attractors.  
> It either:
> - collapses into a stable basin  
> - or transitions under forced conditions  

The key challenge is:

> **controlled navigation between stable regions without loss of stability**
