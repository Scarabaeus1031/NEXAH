# NEXAH Layer

This directory is the conceptual and lightweight package layer of the NEXAH framework.

It serves as the public-facing, readable and actionable surface of NEXAH.

---

## 🧭 Current Layers (April 2026)

| Layer                        | Status     | Description |
|-----------------------------|------------|-----------|
| Field Layer (V69)           | ✅         | Core field geometry |
| Spiral Coupling Layer       | ✅         | Water–Mercury–Ferro triple spiral |
| **URF Axial Space + Root Bridge (v9.1)** | ✅ **neu** | 3D coordinate system + Matroschka mapping |
| Switch Layer                | ✅         | 3x3 / 2x2 grid on Elastic Axis |

---

## URF Axial Space + Root Bridge – 3D Reference Frame

This new layer provides the **three-dimensional geometric backbone** for all Matroschka structures, Spiral Coupling and Switch dynamics.

It connects the 2D Dual-Strand Grey Channel and Elastic Axis into a unified 3D axial system and serves as NEXAH’s internal realization of the s-plane concept.

**Visual Gallery:**

**Root Cube** (neutral core)
![Root Cube](urf_axial_space/visuals/NEXAH_Root_Cube_v9.1.png)

**URF Axial Space – White Cube**
![White Cube](urf_axial_space/visuals/NEXAH_URF_Axial_Space_with_Matroschka_Switch_Grid_v9.1.png)

**URF Axial Space – Black Cube**
![Black Cube](urf_axial_space/visuals/NEXAH_URF_Axial_Space_with_Matroschka_Switch_Grid_v9.1_v.2.png)

**Triple Spiral Coupling + Root Bridge Interaction**
![Triple Spiral + Root Bridge](urf_axial_space/visuals/NEXAH_Triple_Spiral_Root_Cube_Interaction_v9.1.png)

---

## 📐 Connection to Existing Elements

- The **Switch Layer v9.0** (Dual-Strand Grey Channel) is the 2D projection of this 3D space.
- The **golden Elastic Axis** is the main diagonal through the cube.
- The **3x3 grid + 2x2 core** are the switch points at the center.
- All **Matroschkas** now live inside this unified 3D frame.

---

## 🧱 Position in the repository

A useful reading of the full stack is:

simulation  
↓  
structure extraction  
↓  
field representation  
↓  
transition geometry  
↓  
channel formation  
↓  
switch dynamics  
↓  
**URF Axial Space + Root Bridge** ← neu  
↓  
navigation language  

The `nexah/` directory lives primarily in:

- field representation  
- transition geometry  
- channel dynamics (v8)  
- dual-strand dynamics (v8.9)  
- switch systems (v9)  
- **triple spiral coupling + Root Bridge (v9.x)**  

---

## 🧠 Core Evolution (UPDATED)

NEXAH has evolved from:

simulation  
→ structure extraction  
→ geometry  
→ field channels (v8)  
→ dual-strand dynamics (v8.9)  
→ switch-layer systems (v9.0)  
→ **triple spiral coupling + elastic dual lock + Root Bridge (v9.1)**

---

## 🧩 Internal structure

### 5. spiral_coupling/  
Dreifache Spiralüberlagerung (Water–Mercury–Ferro) mit Grey Channel, Elastic Dual Lock und Switch-Verhalten.

### 6. urf_axial_space/ ← **NEU**  
3D coordinate system + Root Bridge (Root Cube, Elastic Axis, Restricted Axis √∫)

---

## 🧬 Core Idea

If ENGINE computes  
and FRAMEWORK describes  

then:

> nexah/ makes the system **navigable**

---

## ⚙️ Current maturity

- geometry ✔  
- field ✔  
- channels ✔  
- dual strands ✔  
- switching ✔  
- **triple spiral coupling + Root Bridge** ✔  

---

## 🧭 Suggested reading path

identity  
→ field  
→ navigation  
→ channel  
→ switch  
→ **spiral_coupling**  
→ **urf_axial_space** (neu)

---

## 🧩 Summary

The `nexah/` directory connects:

- computation  
- geometry  
- navigation  
- control  

NEXAH becomes a language for navigating systems.

**NEXAH Status**  
The structure is visible.  
The field is readable.  
The Matroschkas have their room.  
The Root Bridge is live.
