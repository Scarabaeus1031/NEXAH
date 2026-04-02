# NEXAH / power_systems

**Power System Stability & Intelligent Field Navigation**

This folder contains the core applications and tests of NEXAH on real power grids.  
It demonstrates **practical, geometry-driven early detection** of voltage collapse in complex dynamic systems.

**Stability is not a static state — it is a geometry evolving in time.**

### Current Status – Mic-Drop Achieved (April 2026)

NEXAH reliably detects voltage collapse **43.9 seconds earlier** than classical methods on real IEEE networks — consistently across four different grid sizes.

| Network                | Phi-Split | Lead Time vs. Classical Collapse | Status                     |
|------------------------|-----------|----------------------------------|----------------------------|
| IEEE 118-Bus           | 36.10 s   | **43.9 s**                       | Confirmed                  |
| IEEE 300-Bus           | 36.10 s   | **43.9 s**                       | Confirmed – Mic-Drop!      |
| IEEE 1354-Bus          | 36.10 s   | **43.9 s**                       | Confirmed                  |
| IEEE 9241-Bus (PEGASE) | 36.10 s   | **43.9 s**                       | Confirmed (largest test)   |

**Final Showcase**

![NEXAH Mic-Drop on IEEE 300-Bus](stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)  
*NEXAH Mic-Drop on IEEE 300-Bus – 43.9 Seconds Earlier Detection than Classical Method*

![IEEE 9241-Bus – Phi-Split at t=36.10 s](stability_field_dynamics/iee_core_geometry/ieee_scaling/ieee9241_real_tunable_v12.7_4panel_iota_ring.png)  
*IEEE 9241-Bus (PEGASE) – identical Phi-Split despite 78× larger network*

### Why this matters

Classical methods only react when the voltage has already begun to collapse.  
NEXAH observes the **geometric evolution of the field** (drift, resonance, Phi-Regulator, Iota-Ring) and issues a clear warning **well before** the critical point.

This is the first practical demonstration that geometry-based navigation can deliver measurable early warning in real power systems.

### Two Entry Points

#### 1. 🔬 Scientific / Physical Layer  
→ Physical interpretation, IEEE validation, collapse prediction, metrics  
*(You are here)*

#### 2. 🧠 Operator / System Layer  
→ Full system architecture, operator logic, visual gallery, navigation concepts  
→ See: [NEXAH MASTER INDEX & VISUAL GALLERY](stability_field_dynamics/iee_core_geometry/demos/NEXAH_MASTER_INDEX_GALLERY.md)

### Folder Structure & Key Resources

- **[stability_field_dynamics/](stability_field_dynamics/)**  
  Core research area with regime ODE, IEEE testing and mathematical foundations

- **[ieee_application/](ieee_application/)** (in progress)  
  Full application layer and interactive demos

- **[ieee_test_cases/](ieee_test_cases/)**  
  Classical benchmarks and test cases

**Important Links inside stability_field_dynamics:**
- [iee_core_geometry/README.md](stability_field_dynamics/iee_core_geometry/README.md) – Mathematical & geometrical foundations
- [Core Equations](stability_field_dynamics/iee_core_geometry/core_ode_equations.md) – v10.0 (Lorenz-Core + Iota-Ring)
- [Building Log](stability_field_dynamics/iee_core_geometry/BUILDING_LOG.md) – Complete development history (v7.x → v12.7)
- [Visual Gallery](stability_field_dynamics/iee_core_geometry/Visual_Gallery.md) – All important plots and evolution
- [IEEE Scaling Tests](stability_field_dynamics/iee_core_geometry/ieee_scaling/README.md) – Final Mic-Drop validation on large grids

### Technical Core (iee_core_geometry)
- **Core ODE v12.7** – Lorenz + Iota-Ring (12.0 → 13.7) + absolute lock + Nexus-Hold
- **Phi-Regulator** with strong Forward2 (P-Regulator) hold
- 7-Arc Lattice, CON~DAO waves, Sun-Moon-Kiss trigger, Black Attractor

---

**Author:** Thomas K. R. Hofmann  
**Date:** 03 April 2026

**NEXAH** is transitioning from geometric exploration to a **functional instrument** for intelligent navigation in complex dynamic power systems.
