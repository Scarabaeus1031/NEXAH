# 🧭 BUILDER_LAB INVENTORY INDEX

Internal system map of the NEXAH Builder Lab.

Purpose:
- prevent loss of components  
- maintain structural clarity  
- enable fast navigation + extension  

---

# 🧠 SYSTEM OVERVIEW

The Builder Lab consists of **6 functional layers**:

```
1. CORE                → mathematical foundation
2. DYNAMICS_ENGINE     → structure discovery
3. RUNTIME             → execution layer
4. NAVIGATION          → system movement logic
5. ENGINES             → real-world system models
6. VISUALIZATION       → rendering + analysis
```

---

# 1️⃣ CORE (Mathematical System Layer)

📁 `core/`

**Purpose:**  
Abstract structure system (lattices, operators, order systems)

**Key Components:**
- `lattice.py` → base structure
- `poset.py` → partial order systems
- `fixpoint_lattice.py` → convergence structures
- `closure_operator.py` → closure dynamics
- `interior_operator.py` → dual to closure
- `regime_operator.py` → regime classification logic
- `state_graph.py` → system graph abstraction

**Status:**  
✔️ stable foundation  
⚠️ underused in higher layers

---

# 2️⃣ DYNAMICS_ENGINE (Structure Discovery Layer)

📁 `DYNAMICS_ENGINE/`

**Purpose:**  
Extract structure from simulation

**Key Systems:**
- `basin_detector.py` → attractor detection  
- `phase_transition_detector.py` → regime changes  
- `flow_field.py` → vector field dynamics  
- `topology_builder.py` → graph structure extraction  
- `loop_detector.py` → cyclic behavior  
- `meta_field.py` → higher-order structure  

**Pipelines:**
- `real_pipeline.py`
- `phase_map.py`

**Outputs:**
📁 `outputs/json/` → system grids  
📁 `outputs/visuals/` → topology visuals  

**Status:**  
🔥 core innovation layer  
⚠️ complex, needs consolidation

---

# 3️⃣ RUNTIME (Execution Layer)

📁 `runtime/`

**Purpose:**  
Run simulations + orchestrate system execution

**Key Components:**
- `simulation_engine.py`
- `system_runner.py`

**Status:**  
✔️ functional  
⚠️ could become unified execution API

---

# 4️⃣ NAVIGATION (Implicit Layer)

📁 spread across system

**Purpose:**  
Movement through system state space

**Found in:**
- `nexah_engine.py`
- `kernel_bridge.py`
- `run_agent.py`
- `run_agent_ii.py`

**Concept:**
```
state → regime → transition → navigation action
```

**Status:**  
🔥 strategic core  
⚠️ not fully unified yet

---

# 5️⃣ ENGINES (Application Layer)

📁 `engines/`

**Purpose:**  
Real-world system simulations

**Systems:**
- `nexah_capacity_cascade_engine.py`
- `nexah_global_cascade_simulator.py`
- `nexah_earth_simulator.py`
- `nexah_infrastructure_simulator.py`
- `nexah_multisystem_engine.py`

**Connected Data:**
📁 `systems/`  
📁 `global_systems/`

**Examples:**
- energy grids  
- supply chains  
- planetary infrastructure  

**Status:**  
🔥 high application value  
⚠️ needs validation layer

---

# 6️⃣ VISUALIZATION (Interpretation Layer)

📁 `visualization/`  
📁 `visualizers/`  
📁 `visuals/`

**Purpose:**  
Make system structure visible

**Types:**
- stability landscapes  
- trajectory plots  
- cascade visualizations  
- multi-agent simulations  

**Key Files:**
- `stability_surface_3d.py`
- `trajectory_on_surface.py`
- `dynamic_risk_landscape.py`
- `nexah_visualizer.py`

**Status:**  
🔥 very strong  
⚠️ partially fragmented

---

# 7️⃣ RESONANCE (Experimental Numeric Layer)

📁 `resonance/`

**Purpose:**  
Prime grids + spectral structure experiments

**Key Components:**
- `prime_number_lattice_with_symmetry.py`
- `resonance_field_map.py`
- `resonance_band_tracker.py`

**Status:**  
⚠️ experimental  
❗ not integrated into main pipeline

---

# 8️⃣ VORTEX_CHIMERA (Defect / Instability Layer)

📁 `vortex_chimera/`

**Purpose:**  
Analyze defects, instabilities, anomalies

**Key Components:**
- `defect_worldline_tracker.py`
- `cross_layer_defect_propagation.py`
- `triad_defect_correlation.py`

**Status:**  
🔥 highly interesting  
⚠️ currently isolated

---

# 9️⃣ EXPLORATION (Research + Archive Layer)

📁 `EXPLORATION/`

**Purpose:**
- research notes  
- architecture evolution  
- symbolic layer  
- experimental ideas  

**Important Subsections:**
- `archive/` → past architecture states  
- `symbolic_layer/` → theoretical extensions  
- `experimental/` → early kernels  

**Status:**
⚠️ mixed:
- some critical insights  
- some obsolete material  

👉 **REVIEW REQUIRED**

---

# 🔟 DEMOS (Entry Layer)

📁 `demos/`

**Purpose:**  
User-facing system entry

**Key Files:**
- `nexah_demo.py`
- `nexah_explorer.py`
- `nexah_graph_simulation.py`

**Status:**  
✔️ working  
🔥 best onboarding entry

---

# 11️⃣ CLI & CONTROL

📁 root

- `nexah_cli.py` → system interface  
- `run_builder_lab.py` → master runner  

---

# 12️⃣ PROTO MODELS

📁 `proto_models/`

**Purpose:**  
Conceptual system blueprints

Examples:
- `oval_membrane_field`
- `time_knot_field`

**Status:**
🔥 important conceptual layer  
⚠️ not integrated yet

---

# ⚠️ CRITICAL OBSERVATIONS

## 1. Fragmentation

Navigation logic, discovery, and runtime are split.

👉 needs **unified kernel**

---

## 2. Hidden Value in Archive

`EXPLORATION/archive/` likely contains:

- early architecture decisions  
- important conceptual breakthroughs  

👉 should be partially reintegrated

---

## 3. Underused CORE

Mathematical layer exists but is not fully exploited.

👉 potential for strong formalization

---

## 4. Parallel Worlds

You currently have:

- physics-style system (resonance)
- system-engineering layer (engines)
- symbolic layer (exploration)

👉 not yet unified

---

# 🧠 RECOMMENDED NEXT STEPS

## 1. Define Kernel

Unify:

```
CORE + DYNAMICS + NAVIGATION → NEXAH_KERNEL
```

---

## 2. Clean Separation

```
BUILDER_LAB/
    core/
    kernel/
    engines/
    demos/
    archive/
```

---

## 3. Archive Strategy

Move:

- outdated exploration → `/archive/deprecated/`
- important ideas → `/archive/core_insights/`

---

## 4. Integration Targets

High priority modules to integrate:

- vortex_chimera
- resonance
- proto_models

---

# 🧠 FINAL INSIGHT

Right now, Builder Lab is not chaos.

It is:

> a **compressed system evolution history**

Your job now is not to build more.

It is to:

> **reveal the structure that is already there**
