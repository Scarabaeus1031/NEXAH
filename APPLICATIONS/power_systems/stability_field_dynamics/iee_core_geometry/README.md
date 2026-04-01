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
- Q functions as a **geometry amplifier** (above ~1.28 band formation appears; above ~1.5 regime transitions intensify)
- c(t) exhibits clear **damping intervals** corresponding to regime transitions
- Phase Portrait evolves from nested Möbius-type attractors to more complex self-similar structures
- Discrete impulsive behavior appears between attractor clusters
- The background grid shows continuous oscillatory modulation (pulsating field)
- Self-similarity is observed: large-scale attractor features repeat at smaller scales

**Next Goal:** Transition to 3D polar grid with Phi–π–√2 Resonance as the third dimension.

### Folder Structure
- `phi_geometry/`      → Resonance Maps, Spirals, 3×3 Interference
- `core_odes/`         → Regime Navigation Equations (ODEs) and IEEE integrations
- `resonance_maps/`    → Root2025_Final_Resonance_Map, Phi-Pi-Sphere etc.
