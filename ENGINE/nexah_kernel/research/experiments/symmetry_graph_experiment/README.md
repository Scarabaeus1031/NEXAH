# Symmetry Graph Experiment

Experimental research environment for studying resonant symmetry networks, phase transitions, and toroidal dynamics in coupled oscillator systems.

This module explores how topology, resonance, and energy landscapes interact inside structured oscillator networks such as symmetry graphs.

The framework emerged during the development of the NEXAH Kernel research engine.

---

# Concept

The symmetry graph represents a network of coupled oscillators arranged in a geometric topology.

Each node evolves according to coupled phase dynamics similar to:

Kuramoto-type models  
Gyroscopic coupling  
Resonant flow dynamics  

The system allows exploration of:

• phase synchronization  
• resonance webs  
• Arnold tongues  
• basin transitions  
• torus dynamics  
• energy landscapes  

---

# Experimental Modules

The experiment folder is organized by physical interpretation.

symmetry_graph_experiment

core  
central visualizers and kernel bridges

dynamics  
Kuramoto and oscillator dynamics

resonance  
resonance network flows

topology  
torus structures and Arnold webs

energy_landscapes  
stability and resonance potentials

transitions  
phase transitions and separatrix detection

phiC  
φ-resonance structures and Lissajous flows

phase_space  
vector fields and system domains

experiments_misc  
additional experimental tests

visuals  
generated experiment figures

---

# Key Experiments

## Kuramoto Dynamics

dynamics/symmetry_graph_full_kuramoto.py

Simulates phase synchronization on symmetry graphs.

---

## Resonance Web

resonance/symmetry_graph_resonance_flow.py  
resonance/symmetry_graph_resonance_web_lines.py  

Visualizes resonance channels inside the oscillator network.

---

## Energy Landscape

energy_landscapes/symmetry_graph_energy_landscape.py  
energy_landscapes/symmetry_graph_stability_landscape.py  

Computes stability basins and attractor structures.

---

## Phase Transition Detection

transitions/symmetry_graph_phase_transition_detector.py  
transitions/symmetry_graph_separatrix_tracer.py  

Detects boundaries between dynamical regimes.

---

## Toroidal Dynamics

topology/symmetry_graph_torus_nodes.py  
topology/symmetry_graph_torus_resonance.py  
topology/symmetry_graph_torus_arnold_web.py  

Explores torus embeddings and Arnold resonance webs.

---

# Visual Outputs

Generated experiment figures are stored in

visuals/

Examples include:

• symmetry_graph.png  
• symmetry_graph_regime_map.png  
• symmetry_graph_3cycle.png  

These illustrate structural modes of the oscillator network.

---

# Research Goals

The symmetry graph experiments investigate whether structured oscillator networks produce:

• universal resonance structures  
• emergent phase transitions  
• toroidal stability regimes  
• Arnold-web-like resonance networks  

The experiments serve as test environments for the NEXAH resonance framework.

---

# Relation to NEXAH

This module belongs to the research layer of the NEXAH Kernel.

It provides experimental infrastructure for studying:

resonance  
topology  
phase transitions  
nonlinear oscillator networks  

inside the NEXAH system.

---

# Running Experiments

Example:

python ENGINE/nexah_kernel/research/experiments/symmetry_graph_experiment/topology/symmetry_graph_torus_nodes.py

or

python ENGINE/nexah_kernel/research/experiments/symmetry_graph_experiment/dynamics/symmetry_graph_full_kuramoto.py

---

# Status

Active research environment.

The module continues to evolve as new resonance and topology experiments are added.
