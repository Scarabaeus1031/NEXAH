# NEXAH – Building Log (Kernel Development)

## Purpose

This document tracks the incremental construction of the NEXAH core system.

Goal:
A minimal functional system that can:

- extract structure from time series
- detect transitions
- enable navigation
- suggest interventions

---

## Core API

python nexah.analyze(trajectory, target_state=None)

Returns:

- system states (clusters)
- transition dynamics
- stability structure
- navigation paths
- intervention suggestions

---

## Architecture (Kernel)

The system consists of 3 minimal layers:

### 1. Representation
Transforms raw trajectory into state space

- sliding window embedding

### 2. Structure
Extracts discrete system states

- clustering (KMeans)
- transitions (Markov-like)

### 3. Navigation + Control
Operates on the state graph

- path finding (BFS)
- probabilistic exploration
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

### v0.7 – System-Level Capability
- state signatures (system fingerprint)
- batch analysis (multiple trajectories)
- system comparison (similarity metric)
- config traceability in output

---

## Current Capabilities (v0.7)

### State Modeling
- Discrete states via clustering
- Transition matrix between states

### Stability Analysis
- Stable states via self-transition probability
- Escape difficulty per state

### Regime Detection
- Regime shifts (label changes)
- Local instability score

### Navigation
- Shortest path (BFS)
- Probabilistic path (realistic dynamics)

### Intervention Layer
- Minimal intervention estimation
- Transition cost along paths

### Dynamics Estimation
Monte Carlo simulation:

- hit probability (reach target)
- expected steps

### Control Suggestion
Heuristic optimization:

- tests small perturbations of transitions
- identifies most impactful transition

### System Signature (NEW)
Each trajectory produces a structural fingerprint:

- number of observed states
- dominant state
- occupancy distribution
- escape difficulty
- transition entropy

### Batch Processing (NEW)
- analyze multiple trajectories consistently

### System Comparison (NEW)
- similarity score between systems
- based on stability + entropy profiles

---

## Example Insight

Given:

Current: 1  
Target: 0  
Path: [1 → 2 → 0]

System detects:

- strong lock-in at state 1
- indirect path required via state 2

Control suggestion:

increase transition 1 → 2

Result:

- higher probability of reaching target
- reduced expected transition time

---

## Design Principles

- minimal complexity
- no overengineering
- interpretable structure
- simulation over assumption
- modular extensibility

---

## Core Freeze (v0.7)

The NEXAH kernel is now considered functionally stable.

No further structural changes will be made to:

- embedding method
- clustering approach
- transition modeling
- navigation logic
- control heuristic

Reason:

- preserve reproducibility
- maintain interpretability
- avoid instability from continuous refactoring

All future work will be implemented outside the kernel.

---

## Known Limitations

- discrete state approximation
- clustering instability (label permutations)
- comparison currently ignores phase alignment
- control is heuristic (not globally optimal)
- no continuous control field
- no direct real-world actuation layer

---

## Future Ideas (Logged, not implemented)

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
- CLI interface
- JSON export
- batch pipelines

### Applications
- power grids
- financial markets
- sensor systems
- ecological systems

---

## Next Phase (Post-Core)

The focus shifts from:

→ building the core

to:

→ using the core

### Immediate Next Steps

1. CLI tool (v0.8)
2. real dataset integration
3. visualization layer
4. domain-specific application

---

## Summary

NEXAH Kernel v0.7 provides:

- structure extraction
- dynamic modeling
- navigation capability
- intervention estimation
- system comparison

It is a minimal, interpretable engine for analyzing and navigating dynamical systems.

The core is now frozen.

Future progress will come from:

→ applications  
→ tooling  
→ analysis layers  

not from modifying the kernel.

---
