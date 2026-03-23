# DISCOVERY_ENGINE

Tools for architecture exploration, resilience analysis and **dynamic structure discovery**.

This folder contains the computational laboratory of NEXAH — a set of research tools that generate, evolve and analyze system architectures, simulate dynamic behavior, and extract **topological structure from flow**.

---

## What you can do here

- Generate and evolve system architectures  
- Map resilience landscapes  
- Detect phase transitions  
- Discover structural laws  
- Simulate dynamic systems  
- Extract loops, channels, and networks from flow (**NEW**)  
- Visualize complex dynamics  
- Convert dynamic systems into **navigable state graphs (NEW)**  

---

## Quick Start

Most tools can be run directly:

```bash
python resilience_architecture_evolver.py
python resilience_landscape.py
python visualize_system.py
```

Dynamic navigation examples:

```bash
python ENGINE/analysis/navigation_level60_persistent_flow.py
python ENGINE/analysis/navigation_level61_multi_loop_engine.py
```

Phase-space + topology extraction:

```bash
python pipelines/phase_map.py
```

→ **[Tool Capabilities & Pipeline](./TOOL_CAPABILITIES.md)**

---

## Tool Capabilities Highlights

### Core

- **Architecture Exploration** – generate and evolve thousands of system designs  
- **Resilience Analysis** – evaluate stability and failure propagation  
- **Landscape Mapping** – create 3D resilience landscapes and phase diagrams  
- **Law Discovery** – search for universal structural principles  

---

### Advanced (NEW)

- **Dynamic System Simulation** – multi-agent field evolution  
- **Resonance Detection** – φ-based transition behavior  
- **Flow Structuring** – emergence of persistent trajectories  
- **Topology Formation** – loops, knots, channels, networks  
- **Topology Extraction** – explicit detection of structure from dynamics  
- **Phase Space Mapping** – parameter-space exploration via grid sampling  
- **Meta-Field Analysis** – unified structural intensity mapping  
- **State Graph Conversion (NEW)** – transformation into navigable graphs  

---

## Core Idea (Updated)

Traditional systems analysis asks:

> Where are systems stable?

NEXAH now asks:

> **How do systems move, stabilize, and organize into connected structures?**

---

## System Evolution

The framework has evolved into a multi-layer discovery engine:

```
Dynamics  
→ Geometry  
→ Resonance  
→ Flow  
→ Topology  
→ Extraction  
→ Navigation
```

---

## Key Discoveries

The system demonstrates:

- geometry emerging from dynamics  
- resonance-driven state selection  
- φ as an emergent transition operator  
- flow organizing into persistent structures  
- topology emerging from motion  
- separation of density vs structural skeleton  
- formation of loop–channel networks  
- emergence of navigable phase-space structures  

---

## New Capability

The system can now:

> **extract and convert dynamic processes into navigable structural graphs**

This includes:

- loop detection  
- channel extraction  
- transition node identification  
- network reconstruction  
- phase-space mapping  
- meta-field construction  
- graph generation via adapters  

---

## New Tool Layer (Topology Extraction)

Core modules:

- `loop_detector.py`  
- `channel_extractor.py`  
- `transition_node_finder.py`  
- `topology_builder.py`  
- `topology_signature.py`  
- `topology_classifier.py`  

These tools transform:

> simulation output → explicit structural representation  

---

## New Tool Layer (Phase & Meta Analysis)

- `phase_map.py`  
- `phase_gradient.py`  
- `phase_transition_detector.py`  
- `topology_diversity.py`  
- `flow_field.py`  
- `basin_detector.py`  
- `transition_overlay.py`  
- `meta_field.py`  

These tools enable:

- phase space exploration  
- detection of transition zones  
- flow direction analysis  
- basin / attractor identification  
- unified meta-field construction  

---

## 🔷 NEW: Adapter Integration Layer

The Discovery Engine now connects directly to the **NEXAH Adapter Layer**.

This allows:

> simulation → structure → graph → navigation

---

### PhaseSpaceAdapter

- converts phase-map outputs into state graphs  
- each grid point becomes a state  
- transitions derived from structural similarity and adjacency  

---

### Result

> The Discovery Engine is no longer only analytical —  
> it becomes a **generator of navigable systems**

---

## Navigation Pipeline (Extended)

```
Architecture  
↓  
Evolution  
↓  
Analysis  
↓  
Landscape Mapping  
↓  
Phase Detection  
↓  
Law Discovery  
↓  
Validation  
↓  
Dynamics Simulation  
↓  
Resonance Formation  
↓  
Flow Structuring  
↓  
Topology Formation  
↓  
Topology Extraction  
↓  
Graph Construction  
↓  
Navigation
```

---

## Interpretation

The system is no longer only analyzing structures.

It is:

> **generating, evolving, extracting, and converting structure into navigable systems**

---

## System Architecture

![NEXAH Discovery Engine](visuals/nexah_kernel_architecture_map.png)

This visual shows the **core architecture of the NEXAH Discovery Engine**.

### Core Layers

- **META** – relational system structure  
- **ARCHY** – local dynamics modeling  
- **MESO** – stability and risk landscapes  
- **MEVA** – intervention strategies  

### Extended Layers

- **DYNAMICS** – multi-agent flow evolution  
- **TOPOLOGY** – loop/channel network emergence  
- **PHASE SPACE** – parameter exploration  
- **META FIELD** – unified structural field  
- **GRAPH LAYER** – navigation-ready representation  

---

## 🔥 Key Insight (Updated)

> Systems are not static objects —  
> they are **flows that organize into structure  
> and can be navigated through transitions**

---

## 🚧 TO DO / NEXT STEPS

### 🔴 Phase System

- introduce instability / chaos into phase_map  
- generate real phase transitions  
- expand parameter space (beyond orbit + helix)  
- break "uniform Structured Network" regime  

---

### 🟠 Topology & Graph

- replace linear graph connections with spatial adjacency  
- introduce weighted transitions  
- integrate flow direction into graph edges  
- represent basins as attractor nodes  

---

### 🔵 Meta Layer

- refine meta_field weighting  
- validate basin detection robustness  
- identify stable vs unstable regions  
- link meta-field to navigation decisions  

---

### 🟢 Adapter & Navigation

- improve PhaseSpaceAdapter (true phase transitions)  
- connect real-world systems (power grid, traffic, compute)  
- build policy layer for system control  
- enable intervention strategies  

---

### 🟣 Control Layer (Next Major Milestone)

- action selection system  
- transition steering  
- stability optimization  
- collapse prevention  

---

## Want to go deeper?

→ **[Tool Capabilities & Pipeline](./TOOL_CAPABILITIES.md)**  
→ **[Extended Documentation](./README_extended.md)**  

---

## License

Apache 2.0
