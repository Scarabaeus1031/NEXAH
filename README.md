# NEXAH
*A framework for discovering, mapping and navigating stability in complex dynamical systems.*

NEXAH unifies:

→ early detection  
→ field-based modeling  
→ adaptive control  
→ emergent navigation  

into a single framework for understanding and interacting with complex systems.

---

## ⚡ Key Result — IEEE Power Systems

NEXAH detects voltage collapse up to **43.9 seconds earlier** than classical methods.

👉 [Full results](./APPLICATIONS/power_systems/README.md)

![NEXAH IEEE Result](APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)

---

### ⚡ Beyond Detection — Adaptive Control (NEW)

Recent results extend NEXAH beyond early detection:

→ from **prediction**  
→ to **closed-loop, field-based control**

In the IEEE9 system:

- continuous risk field enables real-time interpretation  
- adaptive policy reacts to trajectory (not just state)  
- system evolution is actively influenced  

✔ early intervention before critical states  
✔ structured escalation (STABILIZE → EMERGENCY)  
✔ first real-grid prototype (pandapower integration)  

👉 NEXAH is no longer only detecting collapse —  
it begins to **interact with system dynamics**.

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

## 🔥 Core Insights (Visual)

### 🧠 Emergent Navigation (Multi-Agent)

![NEXAH Multi-Agent Navigation](BUILDER_LAB/visuals/nexah_multi_agent.gif)

*Structure emerges without reward or predefined goal.*

#### Interpretation

Agents can learn navigation behavior **without an explicit reward function**.

Instead of optimizing a predefined objective, they operate inside a  
**structured stability landscape**:

- states correspond to positions in a geometric field  
- transitions follow system dynamics  
- stability acts as an implicit signal  

---

#### Key Idea

Classical reinforcement learning:

state → action → reward → policy  

NEXAH multi-agent systems:

structure → field → movement → emergent policy  

---

#### Insight

> Navigation behavior can emerge directly from system structure  
> without requiring externally defined rewards.

---

### 🌐 Field Structure (V69)

![V69 Field](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

- trajectories follow structured flow  
- collapse emerges along field paths  
- instability is geometric, not threshold-based  

#### Interpretation

The vector field reveals:

- preferred directions of evolution  
- regions of attraction and repulsion  
- structural pathways toward collapse  

---

#### Consequence

Prediction becomes:

→ reading the field  

instead of:

→ extrapolating trajectories  

---

### 🔬 Discrete Systems (Prime / Modular Resonance)

NEXAH also reveals structure in fully discrete systems:

- non-uniform transition dynamics  
- geometric modular patterns  
- corridor-like motion behavior  

👉 structure is not tied to physics alone — it is **systemic**

---

### 🧭 Emergent Flow in Discrete Systems

![Prime Modular Flow](ENGINE/research/experiments/prime_modular_resonance/analysis/output/curated/mod7_particle_flow_trails.gif)

#### Interpretation

Even in a purely discrete system (prime numbers mod 7), we observe:

- coherent flow structures  
- cyclic trajectories  
- basin-like clustering  
- directional transport behavior  

---

#### Key Insight

> Continuous structure and flow can emerge  
> from purely discrete arithmetic systems.

---

#### Conceptual Role

This module provides a **minimal system** where:

- no physics is present  
- no differential equations are used  

yet:

→ **NEXAH structure still appears**

---

👉 This suggests that NEXAH captures a  
**general principle of structured dynamics**, not a domain-specific phenomenon.

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

## 🧮 Mathematical Perspective (Optional)

<details>
<summary>Click to expand formal interpretation</summary>

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

A system is stable if its trajectory remains within:

S = { x : risk(x) < threshold }

---

### Risk Field

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

</details>

---

## 📚 Deep Dive

👉 [Framework](./FRAMEWORK/README.md)  
👉 [Extended Docs](./NAVIGATOR/NEXAH_FRAMEWORK_EXTENDED.md)

---

## 📜 Citation

Hofmann, Thomas K.R. (2026)  
**NEXAH: Structural Discovery and Navigation in Complex Systems**

---

## License

Apache 2.0 / CC BY 4.0  
© 2026 Thomas K. R. Hofmann
