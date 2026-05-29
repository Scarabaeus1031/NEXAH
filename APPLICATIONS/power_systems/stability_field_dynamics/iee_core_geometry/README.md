# NEXAH – Stability Field Dynamics on IEEE Power Systems

Module: APPLICATIONS/power_systems/stability_field_dynamics

Status: Experimental Validation Phase

---

## Overview

This module investigates whether instability in large-scale power systems can be detected as a geometric transition phenomenon before classical voltage-collapse indicators become visible.

The work is based on the NEXAH framework, which represents system evolution as a stability field and analyzes transitions through structural dynamics rather than scalar voltage measurements alone.

The current validation includes:

- IEEE 118-Bus
- IEEE 300-Bus
- IEEE 1354-Bus
- IEEE 9241-Bus (PEGASE)

---

## Repository Structure

```text
│ stability_field_dynamics/
├── iee_core_geometry/
├── field_dynamics_equations.md
├── nexah_operator.md │
└── implementation_matrix.md │
├── iee_scaling/ │
├── ieee118/ │
├── ieee300/ │
├── ieee1354/ │
├── ieee9241/ │
├── animations/ │
└── frames/ │
└── README.md 
```
---

## Mathematical Foundation

The framework combines several dynamical components into a unified field representation:

- Field Force
- Van der Pol Dynamics
- Kuramoto Synchronization
- Compass Modulation
- Winding Number Detection
- Iota Ring Dynamics
- Janus Reversal Operator
- Lyapunov Rhythm Modulation

The mathematical definitions are documented in:

- iee_core_geometry/field_dynamics_equations.md
- iee_core_geometry/nexah_operator.md

---

## Central Hypothesis

NEXAH assumes that approaching instability manifests as a structural transition inside a stability field.

Instead of observing only voltage collapse,

$$V(t) \rightarrow V_{collapse}$$

the framework searches for geometric signatures that appear before collapse becomes visible in conventional metrics.

Examples include:

- loss of coherence
- directional drift formation
- winding-number accumulation
- attractor deformation
- phase-regime transitions

---

## Scaling Validation

The primary objective of this module is to evaluate whether these transition signatures remain observable across network scales.

| Network | Status |
|----------|----------|
| IEEE118 | validated |
| IEEE300 | validated |
| IEEE1354 | validated |
| IEEE9241 | validated |

Observed transition times remain approximately consistent across tested systems.

This observation motivates the hypothesis that the detected transition corresponds to a structural property of the dynamics rather than a system-size-dependent artifact.

---

## Current Findings

The current experiments indicate:

- transition detection occurs before classical collapse indicators
- similar transition structures appear across network sizes
- field geometry remains interpretable at larger scales
- directional instability emerges before voltage collapse

These findings remain preliminary and require further statistical validation.

---

## Visual Results

Example outputs generated during the scaling experiments:

- IEEE118 field evolution
- IEEE300 transition geometry
- IEEE1354 scaling validation
- IEEE9241 PEGASE experiments

The repository contains both static visualizations and animation sequences used during analysis.

---

## Limitations

Current results should be interpreted as exploratory.

Open questions include:

- parameter sensitivity
- scenario dependence
- robustness under stochastic disturbances
- comparison with established early-warning indicators
- statistical significance across repeated runs

---

## Next Steps

Planned validation work:

1. Multi-scenario testing
2. Parameter sensitivity analysis
3. Monte Carlo validation
4. Transition metric formalization
5. Comparison against classical stability indicators
6. Navigation experiments using the NEXAH Operator

---

## Conclusion

The experiments suggest that instability may be observable as a geometric transition process before classical voltage-collapse metrics become critical.

The purpose of this repository is to investigate that hypothesis systematically across increasingly large benchmark power systems.
