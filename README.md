# NEXAH
*A framework for discovering, mapping and navigating stability in complex dynamical systems.*

---

## ⚡ Key Result — IEEE Power Systems

NEXAH detects voltage collapse up to **43.9 seconds earlier** than classical methods.

👉 [Full results](./APPLICATIONS/power_systems/README.md)

![NEXAH IEEE Result](APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)

---

## 🧭 What NEXAH Does

NEXAH transforms:

→ static monitoring  

into:

→ **structured field-based system analysis and navigation**

---

## 🔁 Core Pipeline

simulation → structure → field → geometry → navigation

---

## 🧮 Mathematical Perspective

NEXAH can be interpreted as a **controlled dynamical system in feature space**.

Let:

x(t) = system state

with features such as:

- coherence  
- fragmentation  
- curvature (d²c)  
- residual  
- distance to structural manifold  

The system evolves as:

dx/dt = f(x) + u(x, dx/dt)

where:

- f(x) represents intrinsic system dynamics  
- u(x, dx/dt) represents the NEXAH control policy  

---

### Stability Definition

Instead of voltage thresholds, stability is defined geometrically:

A system is stable if its trajectory remains within a region S:

S = { x : risk(x) < threshold }

---

### Risk Field

NEXAH introduces a continuous risk field:

risk(x) ∈ [0,1]

based on:

- structural deviation (residual)  
- curvature (instability acceleration)  
- trajectory dynamics (risk slope)  
- proximity to collapse manifold  

---

### Key Property

NEXAH operates on:

→ **trajectory-aware control**

instead of:

→ state-based thresholding  

---

## 🔥 Core Insights (Visual)

### 🧠 Emergent Navigation (Multi-Agent)

![NEXAH Multi-Agent Navigation](BUILDER_LAB/visuals/nexah_multi_agent.gif)

*Structure emerges without reward or predefined goal.*

---

### 🌐 Field Structure (V69)

![V69 Field](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

- trajectories follow structured flow  
- collapse emerges along field paths  
- instability is geometric, not threshold-based  

---

### 🔬 Discrete Systems (Prime / Modular Resonance)

NEXAH also reveals structure in fully discrete systems:

- non-random transitions  
- geometric modular patterns  
- corridor-like dynamics  

👉 structure is not tied to physics alone — it is **systemic**

---

## 🚀 Quick Start

👉 [START HERE](./START_HERE.md)

---

## 📂 Main Entry Points

- 🔌 [Power Systems](./APPLICATIONS/power_systems/README.md)  
- 🧠 [Framework](./FRAMEWORK/README.md)  
- 🧪 [Builder Lab](./BUILDER_LAB/)  
- 🧭 [NEXAH Layer](./nexah/README.md)  

---

## 🧠 What NEXAH Is

A system that:

1. extracts structure from dynamics  
2. constructs a continuous state-space representation  
3. reveals underlying field geometry  
4. identifies motion paths  
5. enables navigation across stability regimes  

---

## ⚠️ Status

- structure discovery: ✅  
- field modeling: ✅  
- early detection: ✅  
- adaptive control: ⚠️ emerging  
- real-world validation: ⚠️ ongoing  

---

## 🧠 Key Insight

> Complex systems do not just evolve —  
> they organize into structured state spaces  
> that can be mapped, analyzed and navigated.

---

## 📚 Deep Dive

👉 [Framework](./FRAMEWORK/README.md)  
👉 [Extended Docs](./NAVIGATOR/NEXAH_FRAMEWORK_EXTENDED.md)

---

## 📜 Citation

Hofmann, T.K.R. (2026)  
**NEXAH: Structural Discovery and Navigation in Complex Systems**

---

## License

Apache 2.0 / CC BY 4.0  
© 2026 Thomas K. R. Hofmann
