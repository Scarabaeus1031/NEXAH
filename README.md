# ⚡ NEXAH — Navigating Structure in Dynamical Systems

> Complex systems are not random.  
> They evolve within **structured fields with direction and destination**.

---

![Off-Manifold Flow](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

This is a real system trajectory from an IEEE power grid model.

NEXAH reconstructs a local flow field around it,
revealing how the system moves within a structured stability landscape.

---

🧪 Reproduce this visualization (IEEE off-manifold flow field):

```bash
python APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/analysis/run_ieee_off_manifold_flow_v69.py
```

---

## 🧠 What NEXAH does

NEXAH reconstructs dynamical systems as:

- **fields** instead of states  
- **trajectories** instead of events  
- **attractors** instead of targets  

It reveals:

> how systems **move, transition, and converge** within their intrinsic structure  
> — and how **stability constrains which transitions are actually possible**

---

## 🔥 Core idea

dynamics → structure → field → topology → stability → navigation

---

## 🧭 How this emerges

### Step 1 — Chaos

![Lorenz Chaos](DISCOVERY_ENGINE/outputs/lorenz_core_v4.png)

At first, the system looks completely random.

---

### Step 2 — Structure

![Manifold](DISCOVERY_ENGINE/outputs/lorenz_v8_manifold.png)

Hidden geometry appears:

👉 transitions follow **specific paths**

---

### Step 3 — Representation

![State Graph](DISCOVERY_ENGINE/outputs/v15_state_machine.png)

The system can now be described as:

- states  
- transitions  
- structure  

👉 chaos becomes **organized**

---

### Step 4 — Navigation

![Controlled Navigation](APPLICATIONS/core_demos/lorenz/outputs/lorenz_meta_control_v6_switch.png)

Now something new becomes possible:

- trajectories stabilize  
- regimes are controlled  
- behavior becomes steerable  

👉 the system becomes **navigable**

---

## 🧭 Architecture

Dynamics  
→ Discovery Engine  
→ Field Layer (geometry + stability)  
→ Navigator  

### 🔬 Discovery Engine
Extracts structure from raw dynamics.

### 🌊 Field Layer
Transforms structure into a navigable representation,  
including geometry **and stability constraints**.

### 🧭 Navigator
Operates on the system as a trajectory within the field.

---

## ⚡ What this enables

- detection of regime transitions  
- geometric interpretation of instability  
- trajectory-based control  
- navigation within system dynamics  

---

## 🧠 Current State

### ✔ Working (Prototype)

- structure extraction (Lorenz)  
- transition detection  
- short-term prediction  
- adaptive control behavior  
- regime switching  

### ⚠️ Limitations

- not globally predictive  
- system-dependent  
- still under validation  

---

## 🚀 Entry Point

👉 [START HERE — Run your first demo](START_HERE.md)

---

## 🧭 Navigate the system

### 🔬 Core System
- 🧠 Framework → [FRAMEWORK/README.md](FRAMEWORK/README.md)  
- 🌊 Field Layer → [FIELD_LAYER/build_log.md](FIELD_LAYER/build_log.md)  
- 🔬 Discovery Engine → [DISCOVERY_ENGINE/discovery_core_log.md](DISCOVERY_ENGINE/discovery_core_log.md)  

---

### ⚡ Applications
- ⚡ Lorenz Demo → [APPLICATIONS/core_demos/lorenz/](APPLICATIONS/core_demos/lorenz/)  
- 🌐 Power Systems → [APPLICATIONS/power_systems/](APPLICATIONS/power_systems/)  

---

### 🧭 Navigation Layer
- 🧭 Navigator → [NAVIGATOR/README.md](NAVIGATOR/README.md)  
- 🧭 Architecture → [NAVIGATOR/CORE/NAVIGATION_ARCHITECTURE.md](NAVIGATOR/CORE/NAVIGATION_ARCHITECTURE.md)  

---

## 💡 Core Insight

> Stability is not a fixed state.  
> It is a **region within a structured dynamical field**

---

## 🔬 Stability Geometry (V8)

![Lyapunov Map](FIELD_LAYER/field_decomposition/outputs/v8_0_lyapunov_map/v8_0_lyapunov_map.png)

The system’s stability is not uniform.

- stable regions form basins  
- instability forms structured ridges  
- transitions occur within constrained zones  

Key insight:

> geometry defines possible motion  
> stability defines **viable motion**

---

## 🌀 NEXAH

dynamics → structure → field → regimes → stability → navigation

---

**Thomas K. R. Hofmann · 2026**
