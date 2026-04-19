# ⚡ NEXAH — Structure & Transition Discovery in Dynamical Systems

> Most systems are analyzed after failure.  
> **NEXAH explores how structure and transitions emerge before failure occurs.**

![Status](https://img.shields.io/badge/status-experimental-blue)
![Field Model](https://img.shields.io/badge/field-analysis-lightblue)
![Dynamics](https://img.shields.io/badge/dynamics-active-orange)

---

## 🧭 NEXAH

**A computational framework for extracting structure from dynamical systems.**

NEXAH does not start from predefined states or thresholds.  
Instead, it reconstructs:

> **how systems evolve, organize, and transition in continuous space**

---

## 🔬 Discovery Core (NEW)

At its core, NEXAH performs **structure discovery from raw dynamics**.

From a trajectory, it extracts:

- transition events  
- geometric structure (manifolds / channels)  
- probability fields  
- energy landscapes  
- flow properties (divergence / curl)  
- temporal coupling between system components  

---

## 🔁 Core Perspective

Classical system analysis asks:

→ *Is the system stable?*

NEXAH instead asks:

> **Where and how does the system transition?**

---

## 🌊 Field Interpretation

Rather than discrete states, systems are modeled as:

- **probability fields** → where trajectories concentrate  
- **energy landscapes** → stability vs transition regions  
- **flow fields** → how the system moves  

---

## 🧠 Key Insight

> Complex systems are not purely chaotic.  
> They exhibit **structured, measurable transition dynamics**.

---

## 🧭 Overview (Updated)

Classical approaches focus on:

→ threshold violations  
→ event detection  

NEXAH provides a complementary view:

> systems evolve as **trajectories within structured fields**

This shifts the question from:

→ "Is the system stable?"  

to:

→ **"How does the system move within its structure?"**

---

## ✅ What is actually working (Prototype Status)

NEXAH is not only conceptual — several components are already implemented and tested.

### ✔ Implemented in the Lorenz system

- structure extraction from chaotic dynamics  
- symbolic state representation  
- pattern detection and short-term prediction  
- anticipatory control (trajectory shaping)  
- adaptive meta-control (mode selection)  
- memory (state + sequence dependent behavior)  
- regime / transition detection (switch events)

👉 This forms a **complete local navigation pipeline**:

dynamics → states → prediction → control → adaptive behavior

---

### ✔ Observed behavior

- chaotic trajectories become **partially predictable (locally)**  
- control can **reduce instability without fixed targets**  
- the system **adapts strategy based on context**  
- transitions between regimes can be **detected and reacted to**

---

### ⚠️ Important

- results are currently **prototype-level**  
- behavior is **locally reliable, not globally predictive**  
- validation across systems is **ongoing**

---

👉 Interpretation:

> NEXAH demonstrates that chaotic systems can be  
> **structured, partially predicted, and locally navigated**

👉 See implementation:  
`APPLICATIONS/core_demos/lorenz/`

---

## 🌊 Field Structure (Concept)

![NEXAH Field Structure](FRAMEWORK/visuals/output/v6_risk_field.png)

- valleys → low risk (stable regions)  
- slopes → transition zones  
- peaks → instability  

> Systems evolve within this landscape.

---

## ⚡ Real System Example (IEEE Flow Field)

![Flow Field](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

**Observation:**
- trajectories follow structured flow patterns  
- system evolution is directional  

> Even real-world systems exhibit structured dynamics.

---

## 🚀 Start Here

👉 [START HERE — Run your first demo](START_HERE.md)

---

## 🎬 What you will see

- structured dynamics in chaotic systems  
- trajectories evolving in reduced state spaces  
- regime transitions in system behavior  
- geometric interpretations of dynamics  

---

## 🎥 Visual System (Core)

👉 [Full Visual Gallery → APPLICATIONS/core_demos/lorenz/FRAMEWORK_visual_gallery.md](APPLICATIONS/core_demos/lorenz/FRAMEWORK_visual_gallery.md)

![NEXAH Coherence Dynamics](FRAMEWORK/visuals/output/nexah_v2_coherence.gif)

The visualization pipeline includes:

- V1–V4 → field, coherence, risk, control  
- V5–V8 → multi-agent dynamics & networks  
- V9–V11 → navigation & emergence  
- **V12 → field-level navigation (final synthesis)**  

> The V1–V12 sequence documents the progressive emergence of navigation behavior.

---
  
## 🎬 Visual System — From Dynamics to Navigation

👉 [Full Lorenz Gallery → APPLICATIONS/core_demos/lorenz/FRAMEWORK_visual_gallery.md](APPLICATIONS/core_demos/lorenz/FRAMEWORK_visual_gallery.md)

![V12](APPLICATIONS/core_demos/lorenz/outputs/lorenz_nexah_v12_final.gif)

V1 → V4   → Field & Metrics  
V5 → V8   → Multi-Agent & Networks  
V9 → V11  → Navigation & Emergence  
V12       → Field-Level Navigation  

**Key idea:**

- systems are not controlled via targets  
- systems are not optimized via rewards  

Instead:

> they are navigated within their stability field  

---

## 🧪 Core Demonstration — Lorenz System (NEXAH Engine)

![Lorenz Meta-Control](APPLICATIONS/core_demos/lorenz/outputs/lorenz_meta_control_v6_switch.png)

The Lorenz module is the **primary reference system** for NEXAH.

👉 This is not just visualization —  
it is a working prototype of a navigation system in a chaotic environment.

---

**What emerges:**

- coherence → alignment with dynamics  
- risk → deviation from structure  
- interaction → stabilization  
- navigation → movement within valid regions  

---

👉 This is a first experimental demonstration of:

> field-based navigation without explicit objectives

---

## 🧭 Explore the System

- 🧠 [Framework](FRAMEWORK/README.md)  
- ⚡ [Applications](APPLICATIONS/README.md)  
- 🧭 [Navigator](NAVIGATOR/README.md)  

---

## 🔁 Core Pipeline

```text
dynamics → structure → field → regimes → navigation
```

## 🔥 Core Insight

Classical control:

→ reacts to deviations  

NEXAH:

→ analyzes trajectory evolution within structure  

👉 Stability becomes a function of:
- regime  
- trajectory  
- structural alignment  

---

## 📊 From Structure → Dynamics

### 🔹 Trajectory-Based Control (Prototype)

![Control](APPLICATIONS/power_systems/nexah_ieee9/results/controller_v9/output_v9_plot.png)

> Control acts as **trajectory shaping within system dynamics**

---

## 📊 Experimental Insights

Early experiments suggested strong early-warning signals —  
but later analysis revealed important limitations (see MicFlop section below).

---

## ⚠️ Early Experiment — Misinterpreted Signal (“MicDrop”)

![MicDrop](APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)

**Re-evaluation revealed:**

- not consistently reproducible  
- high sensitivity to processing  
- no reliable lead time  
- partial artifacts  

👉 Result:

> “MicDrop” → **MicFlop — but a useful one**

---

## 🔥 Emergent System (V12)

![NEXAH Full System](FRAMEWORK/visuals/output/v12_full_system.gif)

- field dynamics  
- trajectory evolution  
- multi-agent interaction  
- emergent coordination  

> Stability emerges through **local interaction within the field**

---

## ⚖️ Classical vs NEXAH

| Classical | NEXAH |
|----------|------|
| threshold-based | structure-based |
| event detection | regime analysis |
| reactive | trajectory-aware |
| state-focused | dynamics-focused |

---

## 🚀 Run Example

PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v6.py

---

## 🧭 Status

| Component | Status |
|----------|--------|
| Structure Discovery | ✅ |
| Field Interpretation | ✅ |
| Regime Detection | ⚠️ experimental |
| Control | ⚠️ prototype |
| Navigation | 🚧 emerging |

---

## ⚠️ Limitations

- no validated universal early-warning metric  
- sensitivity to system representation  
- limited real-world validation  
- navigation layer still evolving  

---

## 🧠 Final Insight

Complex systems are not binary.

They evolve within:

> **intrinsic dynamical regimes**

---

## 🌀 NEXAH

> dynamics → structure → field → regimes → navigation  

---

**Thomas K. R. Hofmann · 2026**
