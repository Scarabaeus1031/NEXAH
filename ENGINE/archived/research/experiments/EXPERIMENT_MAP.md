Symmetry Graph Experiment — Experiment Map

This document provides a structural overview of all experiments inside the symmetry_graph_experiment module.

The goal is to make navigation through the research environment easier and to show how the experiments relate to each other conceptually.

⸻

System Overview

The symmetry graph experiments study nonlinear oscillator dynamics on structured networks.

Core research topics include:

• synchronization
• resonance structures
• phase transitions
• vortex dynamics
• toroidal phase space
• stability landscapes

The experiments are organized by physical interpretation.

⸻

Experiment Structure

symmetry_graph_experiment

core
central visualizers and kernel bridges

dynamics
Kuramoto-type oscillator dynamics

resonance
resonance channel flows and resonance webs

topology
toroidal embeddings and Arnold resonance webs

energy_landscapes
stability potentials and attractor landscapes

transitions
phase transition detection and separatrix tracing

phiC
φ-resonance structures and Lissajous dynamics

phase_space
vector fields and domain maps

experiments_misc
additional prototype experiments

visuals
generated figures and experiment outputs

⸻

Core Infrastructure

core/

symmetry_graph_visualizer.py
Graph layout and visualization utilities.

symmetry_graph_kernel_bridge.py
Connection between symmetry graph experiments and the NEXAH kernel.

symmetry_graph_vortex_detector.py
Detection of phase vortices via winding number calculations.

⸻

Dynamics Experiments

dynamics/

symmetry_graph_full_kuramoto.py
Full Kuramoto synchronization simulation on symmetry graphs.

symmetry_graph_drift_simulation.py
Investigates phase drift behavior.

symmetry_graph_gyroscope_dynamics.py
Oscillator coupling with gyroscopic effects.

symmetry_graph_mode_dynamics.py
Analysis of mode structures inside the oscillator network.

symmetry_graph_energy_flow.py
Energy transfer between oscillator nodes.

⸻

Resonance Experiments

resonance/

symmetry_graph_resonance_flow.py
Simulates resonance propagation through the network.

symmetry_graph_resonance_web_lines.py
Visualizes resonance channels forming web-like structures.

symmetry_graph_resonance_modes.py
Mode decomposition of resonance patterns.

symmetry_graph_resonance_generator.py
Generator for structured resonance networks.

symmetry_graph_resonance_flow_web.py
Combined visualization of resonance channels and phase flow.

⸻

Topology Experiments

topology/

symmetry_graph_torus_nodes.py
Embeds symmetry graph nodes onto toroidal surfaces.

symmetry_graph_torus_resonance.py
Studies resonance patterns on torus-embedded graphs.

symmetry_graph_torus_arnold_web.py
Investigates Arnold resonance webs.

symmetry_graph_torus_resonance_web.py
Visualizes toroidal resonance channels.

symmetry_graph_torus_chaos.py
Explores chaotic regimes on toroidal oscillator systems.

⸻

Energy Landscape Experiments

energy_landscapes/

symmetry_graph_energy_landscape.py
Computes energy potentials of oscillator states.

symmetry_graph_resonance_landscape.py
Studies resonance potential fields.

symmetry_graph_stability_landscape.py
Maps attractor basins and stability ridges.

symmetry_graph_entropy_scan.py
Measures entropy and structural disorder across phase states.

⸻

Phase Space Experiments

phase_space/

symmetry_graph_vector_field.py
Vector field representation of oscillator dynamics.

symmetry_graph_domain_map.py
Mapping of stable and unstable domains.

symmetry_graph_cluster_map.py
Visualization of cluster formation in phase space.

⸻

Transition Experiments

transitions/

symmetry_graph_phase_transition_detector.py
Detects transitions between dynamical regimes.

symmetry_graph_phase_transition_scan.py
Parameter sweep for transition detection.

symmetry_graph_basin_map.py
Maps attractor basins.

symmetry_graph_separatrix_tracer.py
Traces separatrix boundaries between regimes.

⸻

φ-Resonance Experiments

phiC/

symmetry_graph_phiC_bridge.py
Explores φ-based resonance coupling.

symmetry_graph_phiC_lissajous_flow.py
Studies Lissajous-type resonance flows.

⸻

Structured Symmetry Experiments

symmetry_graph_3cycle.py
Basic symmetry graph with three cycle layers.

symmetry_graph_3cycle_vortex_analysis.py
Cycle-based vortex detection.

symmetry_graph_3cycle_transition_tracker.py
Tracks synchronization phases and transition regimes.

Graph structure used

center node
17 spokes

cycle layers

C5 + C6 + C6

Partition

5 + 6 + 6 = 17

⸻

Shell Synchronization Experiments

prime_shell_scan.py

Scans synchronization behavior for hub-ring networks of size

N = 8 … 40

Each system consists of

center node
+
N ring oscillators

Measured properties include

• synchronization time
• global order parameter
• metastable phase clustering

Initial results suggest that some shell sizes produce delayed synchronization or frustration regimes.

⸻

Visual Outputs

All generated figures are stored in

visuals/

Examples include

symmetry_graph.png
symmetry_graph_3cycle.png
symmetry_graph_regime_map.png
symmetry_graph_geometric.png

These images illustrate structural modes of the oscillator network.

⸻

Experiment Flow

Typical experiment workflow
	1.	Construct symmetry graph topology
	2.	Simulate oscillator dynamics
	3.	Analyze phase fields
	4.	Detect resonance structures
	5.	Map stability regimes
	6.	Visualize results

⸻

Research Status

The symmetry graph experiment environment is an active exploratory research system.

New experiments and analysis modules are added continuously as part of the NEXAH research program.
