# NEXAH
*A framework for discovering, mapping and navigating stability in complex dynamical systems.*

## ⚡ Key Result — IEEE Power Systems

NEXAH detects voltage collapse up to **43.9 seconds earlier** than classical methods across IEEE power systems (118 → 9241 buses).

This result is consistent across system sizes and shows that instability can be detected through **structural dynamics** before voltage collapse becomes visible.

| Network                | Phi-Split | Lead Time vs. Classical Collapse | Status                     |
|------------------------|-----------|----------------------------------|----------------------------|
| IEEE 118-Bus           | 36.10 s   | **43.9 s**                       | Confirmed                  |
| IEEE 300-Bus           | 36.10 s   | **43.9 s**                       | Confirmed – Mic-Drop       |
| IEEE 1354-Bus          | 36.10 s   | **43.9 s**                       | Confirmed                  |
| IEEE 9241-Bus (PEGASE) | 36.10 s   | **43.9 s**                       | Confirmed                  |

👉 Full results: [Power Systems Application](./APPLICATIONS/power_systems/README.md)

![NEXAH Mic-Drop IEEE 300-Bus](APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)

*Early detection based on structural field dynamics — not voltage thresholds.*


## 🧪 Method & Validation (Summary)

The reported early detection results are based on time-domain simulations of IEEE benchmark systems using standard power system models.

### Setup

- Test systems: IEEE 118, 300, 1354, 9241 (PEGASE)
- Simulation type: time-domain dynamic simulation
- Input data: voltage magnitude, system state variables
- No external or learned data used

### Classical Baseline

The comparison is made against standard voltage-based collapse detection:

- voltage threshold violation  
- rapid voltage drop (collapse onset)  
- conventional monitoring signals  

### NEXAH Signals

NEXAH derives structural indicators directly from simulation outputs:

- coherence (aggregate structural alignment metric)  
- switch signal (derivative-based transition indicator)  
- trajectory structure in reduced state space  

These signals are computed deterministically and require no parameter fitting.

### Measurement of Lead Time

- collapse time (classical): defined by voltage breakdown  
- NEXAH detection time: first consistent structural transition signal  
- lead time = difference between these two timestamps  

The observed ~43.9 seconds lead time is consistent across tested systems.

### Reproducibility

- all experiments are based on standard IEEE test cases  
- full pipeline and outputs are available in the repository  
- results can be reproduced using the provided scripts  

---
## 🔍 What NEXAH Measures (vs Classical Methods)

Classical power-system analysis relies on:

- voltage magnitude thresholds  
- load flow divergence  
- reactive power limits  

NEXAH instead measures:

- **coherence** (global structural alignment)  
- **field geometry** (trajectory structure in state space)  
- **phase drift and flow direction**  
- **distance to structural transition zones**  

### Key Difference

```text
Classical → detects collapse when it happens  
NEXAH     → detects structural instability before it manifests
```

This shift enables earlier and more interpretable detection of instability.

## 🧭 Conceptual Pipeline

```text
simulation → structure → field → geometry → channel → switch → navigation
```

---


![NEXAH Multi-Agent Navigation](BUILDER_LAB/visuals/nexah_multi_agent.gif)

*No reward. No predefined goal.  
Systems organize. Structure emerges.  
Navigation becomes possible.*

---

## 🧠 What NEXAH actually is

NEXAH is **not just a navigation engine**.

It is a **multi-layer framework** that:

1. **simulates systems**  
2. **extracts structural dynamics**  
3. **reveals the underlying field geometry**  
4. **identifies motion paths (flow / geodesics)**  
5. **enables navigation across stability regimes**

---

## ⚠️ Current Position

The framework is already strong in:

- **structure discovery**
- **field discovery**
- **transition geometry**
- **early collapse indication**
- **split / interface / marker logic**

Navigation is no longer only a distant goal.  
It is beginning to emerge as a **trigger-aware geometric layer** built on top of structure and field representation.

Recent extensions include:

- explicit field representation (**V64–V69**)  
- motion-law identification  
- coherence-based transition analysis  
- field split and interface structure  
- trigger-aware transition logic  
- gate and passage models  

👉 NEXAH is currently strongest as a:

> **structure + field discovery system with an emerging navigation language**

---

## 🚀 Use Cases

- stabilizing power grids  
- analyzing cascading failures  
- mapping climate / ecosystem risk  
- understanding chaotic systems  
- discovering hidden structure in simulations  
- autonomous scientific exploration  

---

## 🚀 First Experience (2 min)

👉 [START HERE](./START_HERE.md)

Run your first experiment and see structure emerge.

---

## 🧪 What makes this different?

Most systems:

→ simulate behavior  

NEXAH:

→ **extracts structure from behavior**  
→ **reveals the field behind the system**  
→ **identifies natural motion paths**  
→ **enables navigation through stability landscapes**

---

## 🧭 Navigation Kernel (Emerging)

Recent experiments introduce the first form of a **NEXAH Navigation Kernel**.

This is not yet a full control system, but a new layer that:

- detects navigable channels (grey-channel axis)
- distinguishes structural strands (upper / lower)
- identifies switch regions between regimes
- begins to propose motion within the field geometry

Current status:

- channel detection: ✔  
- strand structure: ✔  
- switch detection: ✔  
- active navigation: ⚠️ emerging  

👉 This marks the transition from:

> observing structure → **moving within structure**

The kernel is currently in an early experimental phase and will evolve into:

- coherence-guided motion  
- regime-aware switching  
- collapse-avoidant navigation  

---

## 🌐 Field Structure (V69)

![Off-Manifold Flow (V69)](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

The V69 field layer is currently the clearest expression of NEXAH’s transition from:

```text
structure extraction → explicit field representation
```

It shows that:

- trajectories follow structured flow inside the field  
- local deviations reveal branching dynamics  
- collapse paths are embedded in field geometry  
- system motion can be read as field-dependent rather than purely state-dependent  

This makes V69 an important bridge between:

- simulation output
- structural discovery
- geometric flow interpretation
- navigation-ready field models  

### Interpretation for Power Systems

In practical terms, this means:

- instability is visible as **trajectory deformation**
- collapse emerges along **preferred flow paths**
- early warning is based on **geometry, not thresholds**

This allows operators to:
- anticipate instability earlier  
- understand collapse mechanisms  
- eventually intervene structurally

---

## ⚡ Flagship Application — Stability Field Dynamics (IEEE Systems)

A core application of NEXAH is the analysis of power system stability using IEEE test cases.

This module demonstrates:

- field-based stability modeling  
- early geometric instability detection  
- collapse prediction via structure  
- phase-driven dynamics  
- split / interface / marker logic  
- operator-based navigation  
- benchmark-linked transition analysis in real power-grid systems  

### 🧭 Entry Points

👉 [📘 IEEE Stability Module](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/README.md)

👉 [🧭 MASTER INDEX & VISUAL GALLERY](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/demos/NEXAH_MASTER_INDEX_GALLERY.md)

👉 [🚀 MASTER INDEX V2 (recommended)](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/demos/NEXAH_MASTER_INDEX_GALLERY_V2.md)

This is currently the most advanced operational realization of:

- field discovery  
- phase control  
- trigger-aware transition detection  
- operator-driven navigation logic  

---

## 🧩 CORE GEOMETRY — Transition Structure

Beyond field dynamics and operator control, NEXAH introduces a deeper layer:

→ **transition geometry**

This layer explains:

- how systems move between regimes  
- why branching occurs  
- how trajectories organize into loops, shells, and manifolds  
- how navigation becomes geometry-aware  

### 🧠 Core Idea

> A transition is not a discrete jump.  
>  
> It is a **structured geometric process**.

### 🔗 Explore Module

👉 [FRAMEWORK / CORE_GEOMETRY](./FRAMEWORK/CORE_GEOMETRY/README.md)

This layer includes:

- coherence as alignment metric  
- field split (forward / backward / interface)  
- oval / cut / branch structures  
- transition manifolds  
- geometry-aware navigation logic  

---

## 🧪 Proto Models (Emerging Concepts)

Beyond the current formal framework, NEXAH now includes a small set of exploratory proto-models.

These are not yet part of the formal framework, but they capture emerging structural ideas that may later extend `CORE_GEOMETRY`.

Current proto-models:

- [TIME_KNOT_FIELD](./BUILDER_LAB/proto_models/time_knot_field/README.md)
- [OVAL_MEMBRANE_FIELD](./BUILDER_LAB/proto_models/oval_membrane_field/README.md)
- [Proto Models Overview](./BUILDER_LAB/proto_models/README.md)

These modules currently explore:

- local temporal emergence  
- observer crossings  
- dual-loop temporal structure  
- layered membrane geometry  
- stretched transition space  
- root shrinking and exchange channels  

Recent experimental extensions (v8–v9) have introduced:

- grey-channel transport structures  
- dual-strand field organization  
- switch-layer emergence (upper / lower regimes)  
- coherence-based channel binding  
- first navigation kernel prototypes  

👉 This marks the transition from:

structure + field discovery  
→ **toward active navigation inside structured fields**

---

## 🧭 Conceptual Pipeline

```text
simulation → structure → field → geometry → channel → switch → navigation
```

A more detailed reading of the current NEXAH logic is:

```text
simulation → dynamics → structure → field → transition geometry → navigation
```

---

## 🧱 The NEXAH Stack

- **META** → relational system structure  
- **ARCHY** → simulation and regime dynamics  
- **MESO** → risk geometry and collapse structure  
- **NEXAH** → navigation through structured fields  
- **MEVA** → execution and trajectory realization  

The full stack is documented in:

👉 [FRAMEWORK / README](./FRAMEWORK/README.md)

---

## 🔬 Experimental Validation — Prime Modular Resonance

Even in fully discrete systems, NEXAH reveals:

- non-random transition structure  
- geometric patterns  
- flow-like behavior  
- stable cycles  
- corridor-like movement  

This supports the broader hypothesis that structural field-like logic may appear in both continuous and discrete domains.

---

## 📂 Key Entry Points

- **[START HERE](./START_HERE.md)**  
- **[Navigator](./NAVIGATOR/README.md)**  
- **[FRAMEWORK](./FRAMEWORK/README.md)**  
- **[Applications](./APPLICATIONS/README.md)**  
- **[NEXAH Layer](./nexah/README.md)**  
- **[Builder Lab](./BUILDER_LAB/demos/)**  
- **[Proto Models](./BUILDER_LAB/proto_models/README.md)**  

---

## 🧠 Key Insight

> Systems do not just evolve —  
> they organize into structures  
> that can be mapped and navigated.

And more recently:

these structures are not only observable —  
they can begin to be **used for controlled movement within the field**

---

## 📈 Implementation Status

Current release: **v1.1 (Field Extension)**

- discovery engine: ✅ strong  
- field layer (V69): ✅ implemented  
- adapter system: ✅ working  
- transition geometry: ✅ active  
- navigation language: ✅ active   
- channel layer (v8): ✅ discovered  
- switch layer (v9): ✅ detected  
- navigation kernel: ⚠️ emerging  
- executable intervention layer: ⚠️ emerging  

---

## 📚 Deep Dive

To understand the full framework and architecture:

👉 [NEXAH Framework (Extended)](./NAVIGATOR/NEXAH_FRAMEWORK_EXTENDED.md)

👉 [FRAMEWORK / README](./FRAMEWORK/README.md)

👉 [NEXAH Layer](./nexah/README.md)

---

## 📜 Citation

Hofmann, T.K.R. (2026)  
**NEXAH: Structural Discovery and Navigation in Complex Systems**  
https://github.com/Scarabaeus1031/NEXAH  

---

## License

Code: Apache 2.0  
Docs: CC BY 4.0  

© 2026 Thomas K. R. Hofmann
