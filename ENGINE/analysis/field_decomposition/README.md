# NEXAH — Field Decomposition Layer

## Overview

This module explores a continuous 2D field system and extracts:

- structure (basins, boundaries, channels)
- dynamics (trajectories, orbits)
- transition behavior (sensitivity, separatrix-like regions)
- navigation properties (cost, reachability, optimal flow)

The system is built through iterative simulation and visualization.

It is **not a physical theory**.

It is a **computational exploration of structured dynamics**.

---

## Core Idea

> Structure shapes motion.

The system is defined by a field:

    dx/dt = -∇V + rotational component

Meaning:

- the gradient pulls toward minima
- rotation introduces curvature and persistence

Result:

→ motion emerges from field geometry

---

## What This Module Does

The pipeline transforms:

```text
raw field
→ trajectories
→ structure detection
→ boundary extraction
→ navigation
→ control interpretation
```

Key capabilities:

- basin detection
- orbit classification
- separatrix-like boundary detection
- sensitivity mapping
- cost-based navigation
- energy landscape estimation

---

## Visual System

The module produces multiple visual layers:

| Layer | Meaning |
|------|--------|
| Q1 | class map (where trajectories end) |
| Q2 | field + trajectories |
| Q3 | sensitivity (where small changes matter) |
| Q4 | projection / geometry |
| Q5 | orbit bands |
| Q6 | representative trajectories |

V7 adds:

- cost maps
- navigation fields
- reachability regions
- energy landscapes

---

## Key Observations

The system consistently shows:

- multiple attractor basins
- orbit-like trajectories
- structured transition regions ("Riss")
- narrow transition corridors (splinter)
- asymmetric flow behavior
- layered orbit families ("bands")

Important:

→ these structures emerge from the field  
→ they are not manually imposed  

---

## Transition Structures

Transitions are not points.

They are:

- spatial regions
- directional
- multi-phase

Often observed as:

- curved boundaries
- S-shaped structures
- narrow corridors between basins

---

## Navigation Layer (V7)

The system can be interpreted as a navigation problem:

- cost field → effort to reach a target
- navigation field → optimal direction
- reachability → where motion is possible

Key finding:

→ not all regions can reach the target  
→ motion is constrained by field geometry  

---

## Interpretation Scope

This work:

✔ explores structure in dynamical systems  
✔ provides reproducible simulations  
✔ identifies consistent geometric patterns  

This work does NOT:

✖ claim new physical laws  
✖ map directly to real-world systems  
✖ provide analytical proofs  

---

## Project Structure

```text
ENGINE/analysis/field_decomposition/

├── v2_*.py      → early field separation
├── v3_*.py      → structure detection
├── v4_*.py      → unified field views
├── v5_*.py      → gradient vs rotation
├── v6_*.py      → classification + boundaries
├── v7_*.py      → cost + navigation + energy

output/
├── v6_*/
├── v7_*/
```

## How to Run

Example:
```bash
python v6_6_core.py
python v7_2_transition_cost_map.py
python v7_3_cost_navigation.py
```
Outputs are saved to:

```text
ENGINE/analysis/field_decomposition/outputs/<version>/
```
## Status

Current phase:

→ exploratory but structurally consistent  

The system has evolved from:

visual exploration → structured field → navigable system  

---

## Next Steps

- stochastic navigation (Boltzmann-like)  
- multi-target control  
- phase-space extension  
- analytical approximation  
- integration into NEXAH Navigator  

---

## Final Note

This module is best understood by:

- running the scripts  
- inspecting the visuals  
- reading patterns across layers  

Understanding comes from:

> reading the field — not just observing trajectories
