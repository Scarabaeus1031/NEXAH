# NEXAH Layer

This directory is the conceptual and lightweight package layer of the NEXAH framework.

It serves as the public-facing, readable and actionable surface of NEXAH.

---

## Current Layers (April 2026)

| Layer                        | Status     | Description |
|-----------------------------|------------|-----------|
| Field Layer (V69)           | ✅         | Core field geometry |
| Spiral Coupling Layer       | ✅         | Water–Mercury–Ferro triple spiral |
| URF Axial Space (v9.1)      | ✅ **neu** | 3D coordinate system + Matroschka mapping |
| Switch Layer                | ✅         | 3x3 / 2x2 grid on Elastic Axis |

---

## URF Axial Space – 3D Reference Frame

This new layer provides the three-dimensional geometric backbone for all Matroschka structures, Spiral Coupling and Switch dynamics.

**Visuals:**

![URF Axial Space – White Cube](urf_axial_space/visuals/NEXAH_URF_Axial_Space_with_Matroschka_Switch_Grid_v9.1.png)

![URF Axial Space – Black Cube](urf_axial_space/visuals/NEXAH_URF_Axial_Space_with_Matroschka_Switch_Grid_v9.1_v2.png)

---

## Quick Start

from nexah import URFAxialSpaceKernel, SwitchGridMapper

kernel = URFAxialSpaceKernel()
mapper = SwitchGridMapper()

# Example: map your existing 3x3/2x2 switch grid into 3D space
result = mapper.map_grid_to_urf(your_grid_data)

---

## Suggested Reading Path

1. identity/NEXAH_IDENTITY.md  
2. navigation/NEXAH_NAVIGATION_PRIMITIVES.md  
3. urf_axial_space/README.md ← new 3D layer  
4. spiral_coupling/README.md

---

**NEXAH Status**  
The structure is visible.  
The field is readable.  
The Matroschkas now live in 3D.  
The next task is action.
