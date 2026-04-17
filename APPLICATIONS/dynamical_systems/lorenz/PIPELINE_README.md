# 🧪 NEXAH — Lorenz Pipeline (Clean Entry)

This document describes the **current working Lorenz pipeline**  
inside the NEXAH framework.

It is the **first concrete, reproducible system** that demonstrates:

dynamics → structure → field → regimes

---

# 🧭 Purpose

The goal of this pipeline is simple:

- take a chaotic system (Lorenz)
- extract structure from it
- represent that structure geometrically
- prepare it for navigation

This is the **entry point for collaborators**.

---

# ▶️ Run the Demo

From repo root:

```bash
python APPLICATIONS/dynamical_systems/lorenz/pipeline/run_lorenz_core_pipeline.py
```

---

# 📦 What the Pipeline Does

The pipeline runs **two core stages**:

---

## 1. 🔹 Trajectory + Regimes

Script:
`pipeline/lorenz_visual_pipeline.py`

Generates:

- Lorenz trajectory (3D)
- regime classification (LEFT / RIGHT / TRANSITION / ESCAPE)
- regime timeline
- attractor visualization

Outputs:

```
APPLICATIONS/outputs/lorenz/
├── lorenz_trajectory.csv
├── lorenz_switch_events.csv
├── lorenz_attractor.png
├── lorenz_regime_timeline.png
└── lorenz_regime_attractor.png
```

---

## 2. 🔹 Structure → Field (Density)

Script:
`attractor/lorenz_density_map.py`

Generates:

- density map of attractor (X-Z projection)
- CSV representation of density
- implicit field structure (via density gradient)

Outputs:

```
APPLICATIONS/outputs/lorenz_density/
├── lorenz_density.csv
└── lorenz_density_map.png
```

---

## 3. 🔹 Field Visualization (Optional but Important)

Scripts:

- `attractor/lorenz_field_visualization.py`
- `attractor/lorenz_field_gradient.py`

Generates:

- density vs field comparison
- gradient vector field (direction of motion tendency)

Outputs:

```
APPLICATIONS/outputs/lorenz_field/
├── lorenz_density_vs_field.png
└── lorenz_field_gradient.png
```

---

# 🧠 What This Actually Shows

This pipeline demonstrates three key transformations:

---

### 1. Dynamics → Structure

The Lorenz system produces chaotic trajectories  
that can be segmented into regimes.

---

### 2. Structure → Geometry

Density mapping reveals:

- attractor shape  
- stability regions  
- high-frequency visitation zones  

---

### 3. Geometry → Field

The gradient of density acts as a **proto-field**:

- shows direction of movement  
- reveals implicit flow tendencies  
- enables navigation interpretation  

---

# 🔥 Core Insight

The system is not defined by trajectories.  
It is defined by the structure that generates them.

---

# 📊 Role of CSV Data

All major outputs are saved as CSV:

- trajectory → raw system evolution  
- density → structural field representation  
- regimes → discrete system states  

These allow:

- reproducibility  
- post-processing  
- integration with `nexah/` core modules  
- future adapter / graph layers  

---

# 🚧 Current Limitations

- no unified in-memory pipeline (file-based flow)  
- field is approximated via density (not full vector field)  
- navigation is not yet integrated  
- coherence / risk not formalized here  

---

# 🚀 Next Steps

Planned extensions:

1. unify output structure  
2. connect density → field layer in `nexah/`  
3. introduce navigation on field  
4. add IEEE real-world system  
5. integrate adapter layer  

---

# 🧭 Position in NEXAH

This pipeline represents:

APPLICATIONS layer → concrete systems

It feeds into:

nexah/ → field + navigation layer

and later:

DISCOVERY_ENGINE → generalized dynamics

---

# 🧠 Final Takeaway

This is not a full framework.

It is:

a minimal, working proof  
that structure can be extracted from chaos  
and turned into a navigable representation

---

NEXAH · Lorenz Pipeline · 2026
