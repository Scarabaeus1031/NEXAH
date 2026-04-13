# NEXAH
*A framework for discovering, mapping and navigating stability in complex dynamical systems.*

NEXAH unifies:

→ early detection  
→ field-based modeling  
→ adaptive control  
→ emergent navigation  

into a single framework for understanding and interacting with complex systems.

---

## 🧭 Where to Start

| Goal | Start Here |
|------|-----------|
| ⚡ See real-world results | [Power Systems](./APPLICATIONS/power_systems/README.md) |
| 🧠 Understand the framework | [Framework](./FRAMEWORK/README.md) |
| 🌀 Explore chaos & geometry | [Lorenz Module](./APPLICATIONS/dynamical_systems/lorenz/README.md) |
| ⚙️ Run experiments | [Applications](./APPLICATIONS/) |

---

## ⚡ Key Result — IEEE Power Systems

NEXAH detects voltage collapse up to **43.9 seconds earlier** than classical methods.

👉 Results & Scaling:
- [Full System Overview](./APPLICATIONS/power_systems/README.md)  
- [Scaling Experiments (IEEE118 → 9241)](./APPLICATIONS/power_systems/nexah_ieeeX/README.md)

![NEXAH IEEE Result](APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)

---

## 🔁 Core Pipeline

```text
simulation → structure → field → geometry → navigation
```

## ⚡ Beyond Detection — Adaptive Control

<details>
<summary>Click to expand</summary>

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

</details>

---

## 🔥 Core Insights (Visual)

### 🧠 Emergent Navigation (Multi-Agent)

![NEXAH Multi-Agent Navigation](BUILDER_LAB/visuals/nexah_multi_agent.gif)

<details>
<summary>Interpretation</summary>

Agents can learn navigation behavior **without an explicit reward function**.

Instead of optimizing a predefined objective, they operate inside a  
**structured stability landscape**:

- states correspond to positions in a geometric field  
- transitions follow system dynamics  
- stability acts as an implicit signal  

Classical RL:
state → action → reward → policy  

NEXAH:
structure → field → movement → emergent policy  

</details>

---

### 🌐 Field Structure (V69)

![V69 Field](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

<details>
<summary>Interpretation</summary>

- trajectories follow structured flow  
- collapse emerges along field paths  
- instability is geometric, not threshold-based  

Prediction becomes:

→ reading the field  

instead of:

→ extrapolating trajectories  

</details>

---

### 🧭 Emergent Flow in Discrete Systems

![Prime Modular Flow](ENGINE/research/experiments/prime_modular_resonance/analysis/output/curated/mod7_particle_flow_trails.gif)

<details>
<summary>Interpretation</summary>

Even in purely discrete systems:

- coherent flow structures  
- cyclic trajectories  
- basin-like clustering  
- directional transport  

→ structure is **not domain-specific**

</details>

---

## 🧠 What NEXAH Is

<details>
<summary>Click to expand</summary>

A system that:

1. extracts structure from dynamics  
2. constructs a continuous state-space representation  
3. reveals underlying field geometry  
4. identifies motion paths  
5. enables navigation across stability regimes  

</details>

---

## ⚠️ Status

- structure discovery: ✅  
- field modeling: ✅  
- early detection: ✅  
- adaptive control: ⚠️ emerging  
- real-world validation: ⚠️ ongoing  

---

## 🧮 Mathematical Perspective

<details>
<summary>Click to expand</summary>

NEXAH can be interpreted as a **controlled dynamical system in feature space**.

Let:

x(t) = system state

The system evolves as:

dx/dt = f(x) + u(x, dx/dt)

where:

- f(x) = system dynamics  
- u(x, dx/dt) = NEXAH control  

### Stability

S = { x : risk(x) < threshold }

### Risk Field

risk(x) ∈ [0,1]

based on:

- residual  
- curvature  
- trajectory dynamics  
- manifold distance  

### Key Property

→ trajectory-aware control  
(not threshold-based)

</details>

---

## 📚 Deep Dive

- [Framework](./FRAMEWORK/README.md)  
- [Extended Docs](./NAVIGATOR/NEXAH_FRAMEWORK_EXTENDED.md)

---

## 📜 Citation

Hofmann, Thomas K.R. (2026)  
**NEXAH: Structural Discovery and Navigation in Complex Systems**

---

## License

Apache 2.0 / CC BY 4.0  
© 2026 Thomas K. R. Hofmann
