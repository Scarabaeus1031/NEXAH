# Symmetry Graph Experiment

Experimental research environment for studying resonant symmetry networks, phase transitions, and toroidal dynamics in coupled oscillator systems.

This module explores how topology, resonance, and energy landscapes interact inside structured oscillator networks such as symmetry graphs.

The framework emerged during the development of the NEXAH Kernel research engine.

---

# Concept

The symmetry graph represents a network of coupled oscillators arranged in a geometric topology.

Each node evolves according to coupled phase dynamics similar to:

• Kuramoto-type oscillator models  
• gyroscopic coupling  
• resonant flow dynamics  

The system allows exploration of:

• phase synchronization  
• resonance webs  
• Arnold tongues  
• basin transitions  
• torus dynamics  
• energy landscapes  
• vortex formation in phase fields  

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

# New Experiments

Recent experiments explore how network size and shell geometry affect synchronization stability.

## Symmetry Graph 3-Cycle Model

symmetry_graph_3cycle.py  
symmetry_graph_3cycle_vortex_analysis.py  
symmetry_graph_3cycle_transition_tracker.py  

These experiments implement a structured symmetry graph with

center node  
17 spokes  

cycle layers

C5 + C6 + C6

Partition

5 + 6 + 6 = 17

The model studies

• vortex formation  
• cycle windings  
• Kuramoto phase locking  
• phase transition regimes  

---

## Prime Shell Synchronization Scan

prime_shell_scan.py

This experiment scans hub-shell networks of size

N = 8 … 40

Each network is structured as

center node  
+  
N ring oscillators

The experiment measures

• synchronization time  
• global order parameter R  
• stability regimes  

Initial results indicate that certain shell sizes produce strong synchronization instability or delayed locking, suggesting resonance or frustration regimes in the oscillator network.

---

# Visual Outputs

Generated experiment figures are stored in

visuals/

Examples include

• symmetry_graph.png  
• symmetry_graph_regime_map.png  
• symmetry_graph_3cycle.png  
• symmetry_graph_cycle_vortex_analysis.png  
• prime_shell_synchronization_scan.png  

These illustrate structural modes of the oscillator network.

---

# Research Findings (Preliminary)

Early experiments suggest that oscillator synchronization depends strongly on network topology.

Observed phenomena include

• rapid synchronization in balanced symmetry graphs  
• vortex formation along cycle layers  
• metastable phase clustering  
• synchronization failure for certain shell sizes  

Example structured topology

C5 + C6 + C6 = 17

This geometry shows particularly stable synchronization in several test runs.

The experiments also explore shell sizes such as

17  
19  
29  

which may correspond to resonance or frustration regimes in the phase dynamics.

Further investigation is ongoing.

---

# Research Goals

The symmetry graph experiments investigate whether structured oscillator networks produce

• universal resonance structures  
• emergent phase transitions  
• toroidal stability regimes  
• Arnold-web-like resonance networks  
• vortex structures in phase space  

The experiments serve as test environments for the NEXAH resonance framework.

---

# Relation to NEXAH

This module belongs to the research layer of the NEXAH Kernel.

It provides experimental infrastructure for studying

resonance  
topology  
phase transitions  
nonlinear oscillator networks  

inside the NEXAH system.

---

# Running Experiments

Example

python ENGINE/nexah_kernel/research/experiments/symmetry_graph_experiment/topology/symmetry_graph_torus_nodes.py

or

python ENGINE/nexah_kernel/research/experiments/symmetry_graph_experiment/dynamics/symmetry_graph_full_kuramoto.py

or

python ENGINE/nexah_kernel/research/experiments/symmetry_graph_experiment/prime_shell_scan.py

---

# Status

Active research environment.

The module continues to evolve as new resonance and topology experiments are added.
