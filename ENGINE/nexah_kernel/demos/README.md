# NEXAH Demonstrations & Visual Exploration

The `demos` module contains runnable demonstrations and visual experiments for the NEXAH kernel.

These scripts illustrate how the kernel can be used to explore **structural dynamics, resonance landscapes, and navigation strategies** in complex systems.

The demos are intentionally exploratory.  
Their purpose is not benchmarking but **understanding the structure of system regimes**.

---

# Concept

The NEXAH kernel models systems as **regime landscapes**.

The demos allow these landscapes to be explored visually by generating:

- attractor basins
- resonance fields
- symmetry landscapes
- spiral dynamics
- multi-attractor systems
- navigation trajectories
- regime shifts
- cascade failures

Many demos produce visual datasets that reveal hidden structure in system dynamics.

---

# Demo Pipeline

The demonstrations follow the typical exploration pipeline used in the NEXAH framework:

xperiment
↓
demo
↓
visual exploration
↓
analysis tools
↓
kernel integration

Experiments explore dynamical behavior.  
Demos visualize the resulting regime landscapes.  
Tools generalize useful algorithms.

---

# Running Demos

All demos can be executed using Python modules.

Example:

python -m ENGINE.nexah_kernel.demos.demo_regime_navigation


| Demo | Description |
|-----|-------------|
| demo_regime_navigation.py | Basic regime detection and navigation pipeline |
| demo_double_well_navigation.py | Navigation across attractor basins in a double-well system |
| demo_regime_map_visualization.py | Visualizes trajectories within an energy landscape |
| demo_regime_phase_map.py | Generates regime maps across parameter space |

These demonstrations illustrate how systems can be interpreted as **navigable regime landscapes**.

---

# Navigation & Regime Analysis

| Demo | Description |
|-----|-------------|
| demo_navigation.py | Basic system navigation example |
| risk_navigation_demo.py | Navigation through risky and safe system regions |
| maze_navigation_demo.py | Navigation through complex state spaces |
| spiral_landscape_navigation_demo.py | Navigation in spiral-shaped landscapes |
| state_landscape_navigation_demo.py | Visualization of regime transitions |

---

# System Stability & Failures

| Demo | Description |
|-----|-------------|
| cascade_failure_demo.py | Simulates cascading failures in networks |
| regime_shift_demo.py | Demonstrates structural regime shifts |
| grid_resilience_demo.py | Tests resilience of network structures |

---

# Resonance & Symmetry Exploration

| Demo | Description |
|-----|-------------|
| symmetry_resonance_explorer.py | Explore resonance structures across symmetry orders |
| symmetry_resonance_detector.py | Detect resonance peaks |
| symmetry_resonance_atlas.py | Generate a visual atlas of symmetry fields |
| n_fold_symmetry_explorer_demo.py | Explore resonance across N-fold symmetries |

These tools generate datasets showing how system dynamics depend on structural symmetry.

---

# Multi-Attractor Systems

| Demo | Description |
|-----|-------------|
| multi_attractor_navigation_demo.py | Navigation across multiple attractors |
| pentagon_multi_attractor_navigation_demo.py | Navigation within pentagonal resonance systems |
| pentagon_multi_attractor_basin_map_demo.py | Visualization of attractor basins |

---

# Resonance Field Experiments

| Demo | Description |
|-----|-------------|
| pentagon_resonance_field_demo.py | Generates pentagonal resonance fields |
| pentagon_hexagon_interference_field_demo.py | Interference between symmetry systems |
| heptagon_octagon_interference_demo.py | Multi-symmetry interference experiments |

These experiments explore resonance patterns emerging from geometric symmetry.

---

# Generated Data

Many demos generate datasets for later analysis.

These are stored in:

ENGINE/nexah_kernel/demos/visuals

The visual archive currently includes:

- regime phase maps
- attractor landscapes
- resonance maps
- chaos maps
- Lyapunov maps
- KAM stability surfaces
- fractal parameter maps
- symmetry resonance atlases

These images form a growing **visual atlas of dynamical system structures**.

---

# Relationship to the Kernel

The demos do not extend the kernel itself.

Instead they act as **exploratory laboratories** built on top of the kernel.

Kernel:

system → regimes → navigation

Demos:

regime landscapes → visual exploration

---

# Status

Exploratory research demos.

Many scripts are experimental and intended for interactive exploration rather than production use.

---

# NEXAH

Part of the **SCARABÆUS1033 research framework**, exploring structural navigation and resonance dynamics in complex systems.

