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
5"}
---

## Experiment 05 — Cycle Balance Synchronization Test

File

symmetry_graph_cycle_balance_test.py

Goal

Determine whether the fast synchronization observed in the symmetry graph

C5 + C6 + C6

is specific to this partition or arises from the general hub-cycle topology.

Tested partitions

5 + 6 + 6  
4 + 6 + 7  
3 + 7 + 7  
5 + 5 + 7  

Method

Kuramoto oscillator simulation with

K = 1.5  
dt = 0.05  
50 runs per topology  

Measured quantity

Synchronization time to reach global order parameter

R > 0.95

Observations

All tested cycle partitions synchronized extremely rapidly.

Typical synchronization times

≈ 1.2 – 1.35

Standard deviations

≈ 0.3 – 0.6

No configuration showed a statistically significant advantage.

Interpretation

The synchronization efficiency appears to be caused primarily by the

hub + cycle topology

rather than the specific cycle partition.

This supports the hypothesis that hybrid networks combining

• global coupling (hub)  
• local cycle stabilization  

produce efficient synchronization dynamics.


# Status

Experiment completed.

Result integrated into the symmetry graph result summa


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

---

## Experiment 06 — Prime Modular Transition Dynamics

File

prime_modular_resonance/

---

### Goal

Investigate whether purely discrete systems (prime numbers under modular projection)  
produce structured transition dynamics comparable to continuous dynamical systems.

---

### Construction

Prime sequence:

pₙ = 2, 3, 5, 7, ...

Residue mapping:

rₙ = pₙ mod m

Transition definition:

Δrₙ = (rₙ₊₁ - rₙ) mod m

Embedding (optional):

θₙ = 2π rₙ / m  
(xₙ, yₙ) = (cos θₙ, sin θₙ)

---

### Methods

• Transition matrix construction  
• Residue jump distribution  
• Drift vector estimation  
• Spectral / geometric embedding  
• Cross-modulus comparison  
• Clustering in transition space  

---

### Visual Outputs

#### 1. Modular Transition Regimes

![Mod Comparison](analysis/output/plots/figure_1_mod_comparison.png)

- transition graphs for mod 7, 11, 13, 17  
- increasing connectivity with modulus size  
- emergence of dense transition structure  

---

#### 2. Drift Scaling

![Drift Scaling](analysis/output/plots/mod_drift_scaling.png)

Observation:

- drift strength increases monotonically with modulus  
- non-linear growth behavior  
- suggests scaling law in transition dynamics  

---

#### 3. Transition Matrix Distance (Raw)

![Distance Raw](analysis/output/plots/mod_distance_matrix_raw.png)

Observation:

- structured distance patterns across moduli  
- not random → clear gradient + clustering tendency  

---

#### 4. Transition Matrix Distance (Clustered)

![Distance Clustered](analysis/output/plots/mod_distance_matrix_clustered.png)

Observation:

- moduli form distinct clusters  
- block structure emerges  
- indicates dynamical regime families  

---

### Observations

1. Non-uniform transition structure

Prime residue transitions are not uniformly distributed.

→ clear directional bias in state transitions  

---

2. Emergent drift

Each modulus exhibits a consistent directional drift in residue space.

Example:

mod 7 → weak drift  
mod 17 → strong drift  
mod 47 → very strong drift  

---

3. Scaling behavior

Drift strength grows with modulus:

mod 7 → ~1.5  
mod 17 → ~4.8  
mod 31 → ~16  
mod 47 → ~32  

→ approximately superlinear growth  

---

4. Cluster formation

Moduli group into dynamic regimes:

Cluster A  
7, 11, 13, 17, 19  

Cluster B  
23, 29, 31  

Cluster C  
37, 41  

Cluster D  
43, 47  

---

5. Structural similarity to dynamical systems

Transition matrices exhibit:

• band structures  
• clustering  
• directional flow bias  

These resemble:

• Markov processes  
• transport operators  
• coarse-grained dynamical flows  

---

### Interpretation

The system behaves as a:

→ discrete Markov-like transition system  
→ with emergent directional bias (drift)  
→ and structured topology in state space  

Key insight:

> Structure is not imposed — it emerges from transition asymmetry.

---

### Connection to Symmetry Graph Experiments

Parallels observed:

| Symmetry Graph | Prime Modular System |
|------|----------------|
| Phase synchronization | Transition stabilization |
| Vortex structures | drift / directional bias |
| Cycle layers | modular residue loops |
| Domain locking | cluster formation |

Hypothesis:

Both systems may be governed by a shared principle:

→ **structured transitions induce emergent order**

---

### Open Questions

1. Is drift a universal property of prime residue systems?

2. Does normalization remove or preserve structure?

3. What is the spectral signature (eigenvalues) of these transition matrices?

4. Do similar patterns appear in non-prime sequences?

5. Can transition matrices be mapped to known dynamical operators?

---

### Next Steps

• eigenvalue analysis of transition matrices  
• stationary distribution computation  
• normalization tests (drift / m, drift / √m)  
• comparison with random controls  
• higher modulus extension (m > 50)  
• spectral clustering refinement  

---

### Status

✔ reproducible  
✔ quantified  
✔ scalable  
✔ connected to existing experiments  

→ integrated into research layer

---
