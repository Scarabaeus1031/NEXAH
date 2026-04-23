# ⚡ NEXAH — A Geometric Framework for Dynamical Systems

> NEXAH is a computational framework that reveals structure, transitions, and stability directly from system dynamics.

> Complex systems are not random.  
> They evolve within **structured fields that constrain motion, transitions, and outcomes**.

---

# 🚀 Quick Start

```bash
pip install -e .
pytest
python run_nexah_demo.py
```

---

## 📊 Current System State

Before diving deeper, read:

→ [SYSTEM_STATE.md](ARCHITECTURE/SYSTEM_STATE.md)

This document defines:

- what is implemented  
- what works  
- what is validated  
- what is still missing  

---

![Off-Manifold Flow](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

This visualization shows a trajectory from a real IEEE power grid model.

NEXAH reconstructs the local **flow field** around the system state.

What becomes visible:

- directional structure  
- transition channels  
- stability constraints  

→ the system does not move freely  
→ it is **guided by an underlying field geometry**

---

🧪 Reproduce this visualization:

```bash
python APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/analysis/run_ieee_off_manifold_flow_v69.py
```

---

# 🧠 What NEXAH does

NEXAH transforms time-series system data into a **geometric representation**:

- states → field  
- time evolution → trajectories  
- events → regime transitions  

Instead of detecting isolated failures, NEXAH identifies:

> how systems **move within structured dynamical landscapes**  
> and how **stability constrains possible transitions**

---

# ❌ What NEXAH is NOT

NEXAH does not rely on:

- machine learning models  
- predefined control rules  
- purely simulation-based analysis  

It is:

> a **structure–field–geometry framework**  
> that reconstructs and navigates dynamical systems directly from their dynamics

---

# 🔥 Core Principle

```text
dynamics → structure → field → geometry → stability → control → navigation
```

---

# 🧭 System Architecture

```text
Dynamics  
→ Structure Extraction (Discovery phase)  
→ Field Reconstruction (CORE)  
→ Field Layer (geometry + stability)  
→ Control Layer (CORE)  
→ Navigation  
```

---

## 🔬 Structure Extraction  
Extracts structure from raw dynamics.

## 🌊 Field Reconstruction (CORE)  
Builds the field from trajectory data:

- density  
- flow  
- boundary structure  
- validity regions  

## 🌐 Field Layer  
Transforms structure into:

- geometry  
- stability  
- interpretable field structure  

## 🎮 Control Layer (CORE)  
Operates on transition structure:

- basin detection  
- separatrix extraction  
- gate detection  
- trajectory steering  

## 🧭 Navigation  
Executes constrained motion through the field:

- transition-aware movement  
- stability-constrained paths  
- convergence to attractors  

---

# 🔥 Key Result — Power Systems (IEEE)

NEXAH has been tested on real IEEE grid models (118 → 9241 buses).

Result:

> Voltage collapse can be detected **~43.9 seconds earlier**  
> than classical methods — consistently across system sizes.

---

![IEEE Result](APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/ieee300_transition_detection.png)

Interpretation:

- classical methods detect **state failure**  
- NEXAH detects **structural transition**
