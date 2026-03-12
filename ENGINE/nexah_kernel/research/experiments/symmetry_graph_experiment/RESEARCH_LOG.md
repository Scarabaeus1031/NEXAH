# Symmetry Graph Experiment — Research Log

This document records the experimental development history of the symmetry graph experiments inside the NEXAH Kernel research layer.

The goal is to track experiments, observations, and hypotheses in a structured chronological format.

---

# Experiment Log

---

## Experiment 01 — Base Symmetry Graph

File

symmetry_graph_3cycle.py

Structure

center node  
17 spokes  

cycle layers

C5 + C6 + C6

Partition

5 + 6 + 6 = 17

Goal

Investigate synchronization behavior of a balanced symmetry graph topology.

Observations

The graph structure is highly symmetric and supports stable phase relationships between nodes.

Balanced partitions appear to stabilize the oscillator network.

Status

Baseline structural model.

---

## Experiment 02 — Cycle Vortex Analysis

File

symmetry_graph_3cycle_vortex_analysis.py

Goal

Detect phase winding numbers along graph cycles.

The analysis identifies vortex structures in phase space.

Methods

Cycle detection  
Phase winding calculation  
Visualization of vortex candidates

Observations

Some cycles exhibit non-zero winding numbers, indicating vortex-like structures in the oscillator phase field.

These vortices appear along cycle layers and near symmetry boundaries.

Status

Preliminary vortex detection working.

---

## Experiment 03 — Transition Tracking

File

symmetry_graph_3cycle_transition_tracker.py

Goal

Track synchronization phases of the system.

Transitions measured

Θ — random phase field  
Τ — local clustering  
Δ — domain locking  
Ι — vortex collapse  
Υ — global synchronization

Observations

The network often transitions through intermediate clustering states before reaching global synchronization.

In some runs vortex states persist for longer periods before collapsing.

Status

Transition tracking operational.

---

## Experiment 04 — Prime Shell Synchronization Scan

File

prime_shell_scan.py

Structure

center node  
+  
N ring oscillators

Tested range

N = 8 … 40

Measured quantities

Synchronization time  
Global order parameter R

Observations

Most shell sizes synchronize quickly.

However several shell sizes produce delayed synchronization or instability.

Notable cases

29  
30  
34  
39

These sizes sometimes fail to synchronize within the simulation window.

This suggests resonance frustration or metastable phase structures.

Status

First topology scan completed.

Further runs needed for statistical confirmation.

---

# Structural Hypothesis

Several geometric structures appear repeatedly in the experiments.

Example balanced symmetry graph

C5 + C6 + C6 = 17

Possible interpretation

Inner symmetric cycle structure stabilizes synchronization.

Outer shell sizes may introduce frustration effects depending on ring symmetry.

Numbers explored in experiments

17  
19  
29

These values may correspond to resonance or frustration regimes in oscillator networks.

Further experiments are required.

---

# Open Questions

1. Why do some shell sizes produce delayed or failed synchronization?

2. Do prime shell sizes behave differently from composite shell sizes?

3. How do vortex structures influence synchronization transitions?

4. Can layered symmetry graphs (such as 17 inner nodes + outer shells) produce stable toroidal phase structures?

---

# Next Experiments

Planned experiments include

• multi-layer symmetry graphs  
• vortex tracking across parameter sweeps  
• phase-space visualization of oscillator networks  
• statistical synchronization scans across larger shell ranges  
• comparison of prime vs composite shell topologies

---

# Research Context

These experiments serve as a dynamic testing environment for studying nonlinear oscillator networks and resonance structures.

The results may contribute to understanding:

• synchronization phenomena  
• resonance webs  
• toroidal phase dynamics  
• emergent structures in coupled oscillator systems

within the broader NEXAH research framework.

---

# Status

Active research.

Experiments are exploratory and ongoing.
