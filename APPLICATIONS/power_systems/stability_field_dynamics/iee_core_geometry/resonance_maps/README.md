# NEXAH / power_systems / stability_field_dynamics / iee_core_geometry

**Mathematical and Geometrical Foundations of the Instrument**

This folder contains the core mathematical structures that form the foundation of the NEXAH instrument:

- Phi–π–√2 Resonance  
- 5-Phi States + 5-Mode Drive  
- Core Geometry as Vessel / Regime ODE  
- Root Resonance Maps  

These foundations are directly integrated into the Field Layer and the navigation system.

### Key Insights from 2D Development (v13 – v3.8)
- Phi-State acts as the **primary regulator** (starts at 0 and advances in discrete steps)  
- Q functions as a **geometry amplifier** (band formation above ~1.28, strong regime transitions above ~1.5)  
- c(t) exhibits clear **damping intervals** corresponding to regime transitions  
- Phase Portrait evolves from nested Möbius-type attractors to complex self-similar structures  
- Discrete impulsive behavior appears between attractor clusters  
- The background grid shows continuous oscillatory modulation (pulsating field)  

### Major Milestone – April 2026: Full Lorenz Core (3D)
- Complete transition from Kuramoto to **Lorenz dynamics** as Field-Force  
- 3D polar grid with Phi–π–√2 as third dimension  
- Visual language: **Hirtenstock**, **smiling L**, **open channel + Durchfluss**, **Bezel (X im Kreis)**, **J-Spiegel**, **Thoth’s Vogel**, **Vortex Winding**, **Waffelschicht** and **Fold**  
- Tunable Phi-Split with late slow-start ramp and late-boost for controlled regime transition timing  

**Current Status:**  
The instrument now produces coherent, narrative 3D geometries that visualize power-system instability in a completely new way. The classical voltage-collapse curve is always shown for direct comparison.

### Folder Structure
- `phi_geometry/`      → Resonance Maps, Spirals, 3×3 Interference  
- `core_odes/`         → Regime Navigation Equations (ODEs) and IEEE integrations  
- `resonance_maps/`    → All 3D Lorenz visualizations and building logs  

**See also:**  
- [BUILDING_LOG_2026-04-02_Lorenz_MicDrop_Tuning.md](./BUILDING_LOG_2026-04-02_Lorenz_MicDrop_Tuning.md) – detailed log of today’s tuning session  
- [Visual Gallery](./VISUAL_GALLERY.md) – curated highlights

**Next Goal:** Finalize reliable Phi-Split timing (target 34–38 s) and create a quantitative metric (e.g. Vortex-Winding-Number or Resonance-Energy).
