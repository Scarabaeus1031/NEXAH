# NEXAH – Building Log (Kernel Development)

## Purpose

This document tracks the incremental construction of the NEXAH core system.

Goal:
A minimal, interpretable system that can:

- extract structure from time series  
- detect transitions  
- enable navigation  
- suggest interventions  

---

## Core API

```python
nexah.analyze(trajectory, target_state=None)
```

Returns:

- system states (clusters)  
- transition dynamics  
- stability structure  
- navigation paths  
- intervention suggestions  

---

## Architecture (Kernel)

The kernel is intentionally minimal and consists of 3 layers:

### 1. Representation
Transforms raw trajectory into state space

- sliding window embedding  

---

### 2. Structure
Extracts discrete system states

- clustering (KMeans)  
- transition matrix (Markov-like)  

---

### 3. Navigation + Control
Operates on the state graph

- path finding (BFS)  
- probabilistic exploration (Monte Carlo)  
- intervention estimation  

---

## Evolution of the System

### v0.1 – Initial Kernel
- sliding window embedding  
- clustering  
- transition matrix  

### v0.2 – Dynamics
- stability detection  
- regime shifts  

### v0.3 – Navigation
- probabilistic transitions  
- BFS pathfinding  

### v0.4 – Decision Layer
- minimal intervention  
- cost estimation  

### v0.5 – Control Layer
- transition optimization  
- Monte Carlo dynamics (probability + time)  

### v0.6 – Robustness Upgrade
- deterministic mode (random_state)  
- preprocessing (normalization)  
- multi-dimensional support  
- reproducibility  

### v0.7 – System-Level Capability (FINAL KERNEL)
- state signatures (system fingerprint)  
- batch analysis (multiple trajectories)  
- system comparison (similarity metric)  
- config traceability in output  

---

## Current Capabilities (v0.7)

### State Modeling
- discrete states via clustering  
- transition matrix between states  

### Stability Analysis
- stable states via self-transition probability  
- escape difficulty per state  

### Regime Detection
- regime shifts (label changes)  
- local instability score  

### Navigation
- shortest path (BFS)  
- probabilistic path (realistic dynamics)  

### Intervention Layer
- minimal intervention estimation  
- transition cost along paths  

### Dynamics Estimation
Monte Carlo simulation:

- hit probability (reach target)  
- expected steps  

### Control Suggestion
heuristic optimization:

- tests small perturbations of transitions  
- identifies most impactful transition  

### System Signature
Each trajectory produces a structural fingerprint:

- number of observed states  
- dominant state  
- occupancy distribution  
- escape difficulty  
- transition entropy  

### Batch Processing
- analyze multiple trajectories consistently  

### System Comparison
- similarity score between systems  
- based on stability + entropy profiles  

---

## Example Insight

Given:

```
Current: 1  
Target: 0  
Path: [1 → 2 → 0]
```

System detects:

- strong lock-in at state 1  
- indirect path required via state 2  

Control suggestion:

```
increase transition 1 → 2
```

Result:

- higher probability of reaching target  
- reduced expected transition time  

---

## Design Principles

- minimal complexity  
- no overengineering  
- fully interpretable structure  
- simulation over assumption  
- deterministic behavior  
- modular extensibility (outside the kernel)  

---

## Core Freeze (v0.7)

The NEXAH kernel is now considered **final and frozen**.

No further structural changes will be made to:

- embedding method  
- clustering approach  
- transition modeling  
- navigation logic  
- control heuristic  

Reason:

- preserve reproducibility  
- maintain interpretability  
- ensure comparability across systems  

All future work is implemented **outside the kernel**.

---

## Known Limitations

- discrete approximation of continuous systems  
- clustering instability (label permutations)  
- comparison ignores phase alignment  
- control is heuristic (not globally optimal)  
- no continuous control field  
- no real-world actuation layer  

---

## Post-Kernel Direction

The system now separates into:

```text
KERNEL        → structure extraction (frozen)
LAYER SYSTEM  → field, navigation, control (active)
APPLICATIONS  → real-world use cases
```

---

## Future Directions (Outside Core)

### Control & Intervention
- continuous control field  
- gradient-based optimization  
- multi-step planning  

### Sensitivity Analysis
- transition influence ranking  
- robustness under perturbation  

### Improved Comparison
- occupancy distance metrics  
- transition graph similarity  
- sequence alignment  

### Embeddings
- delay embedding  
- frequency features  
- learned representations (optional)  

### Visualization
- state timelines  
- instability heatmaps  
- transition graphs  

### Tooling
- CLI interface (v0.8+)  
- JSON export  
- batch pipelines  

### Applications
- power grids  
- financial markets  
- sensor systems  
- ecological systems  

---

## Next Phase

Focus shifts from:

```
building the core
```

to:

```
using the core
```

### Immediate Next Steps

1. CLI refinement (v0.8)  
2. real dataset integration  
3. visualization layer (active)  
4. domain-specific applications  

---

## Summary

NEXAH Kernel v0.7 provides:

- structure extraction  
- dynamic modeling  
- navigation capability  
- intervention estimation  
- system comparison  

It is a **minimal, deterministic, and interpretable engine** for analyzing dynamical systems.

The core is frozen.

Future progress comes from:

```
→ applications  
→ tooling  
→ higher-level system layers  
```
