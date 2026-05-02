# NEXAH — Core Figures

This folder contains the central visual figure set for the NEXAH research layer.

The figures are organized into:

- `main/` — core paper figures
- `extended/` — extended framework and atlas figures

Structure is not assumed.  
It is extracted from trajectory data through slice-based field, sheet, gate and transition analysis.

---

## Main Figures

### Figure 1 — Structural Framework

![Figure 1](main/fig_01_framework.png)

**NEXAH — From Flow to Topology in Dynamical Systems**

Conceptual overview of the core pipeline:

**Flow → Sheets → Regimes & Gates → Transitions → Connectivity → Topology**

This figure shows how continuous flow can be reduced into locally coherent sheets, how transitions occur between sheets, and how global topology emerges from sheet connectivity.

---

### Figure 2 — Data-Driven Extraction

![Figure 2](main/fig_02_extraction.png)

**Empirical Extraction of Structure and Transitions**

Hybrid figure combining a clean extraction pipeline with data-driven evidence from v13 / v16.

Main steps:

**Dynamics → Slice → Density → Sheets → Gates → Transitions**

It shows how sheets, gates and transition structures are extracted from trajectory data rather than imposed as predefined categories.

---

### Figure 3 — Quantitative Characterization

![Figure 3](main/fig_03_quantitative.png)

**Quantitative Characterization of Transitions and Topology**

Quantitative layer of the framework, including transition probability, event density, switching dynamics, residence times, transition matrices and connectivity-to-topology summaries.

This figure supports the claim that transitions are governed by structural geometry and sheet connectivity.

---

## Extended Figures

### Figure 4 — Extended Flow-to-Topology Framework

![Figure 4](extended/fig_04_extended_pipeline.png)

Extended visual explanation of the flow-to-topology pathway, including cross-system topology mappings.

---

### Figure 5 — Structural Atlas

![Figure 5](extended/fig_05_structural_atlas.png)

Atlas-style overview of the core NEXAH concepts:

- state space
- field
- sheets
- regimes
- gates
- transitions
- temporal dynamics
- topology

---

### Figure 6 — Topology Emergence Framework

![Figure 6](extended/fig_06_topology_framework.png)

Cross-system comparison showing how Lorenz-like, Rössler-like and Halvorsen-like systems can induce different effective topologies through sheet connectivity.

---

### Figure 7 — Regime Geometry Pipeline

![Figure 7](extended/fig_07_regime_geometry.png)

Detailed pipeline emphasizing sheet decomposition, regime geometry, gates, temporal switching and navigation.

---

### Figure 8 — Full Structural Pipeline with Slice Operator

![Figure 8](extended/fig_08_full_pipeline.png)

Full structural pipeline:

**Dynamics → Slice → Field → Structure → Sheets → Regimes → Gates → Transitions → Time → Navigation**

This figure emphasizes the slice operator as the extraction layer connecting raw dynamics to structural and temporal representations.

---

## Core Principle

```text
Flow creates structure.
Structure forms sheets.
Sheets define transitions.
Transitions create connectivity.
Connectivity defines topology.
```

---

## Suggested Paper Mapping

| Paper role | Figure |
|---|---|
| Conceptual framework | Figure 1 |
| Empirical extraction (v13/v16) | Figure 2 |
| Quantitative validation | Figure 3 |
| Supplementary atlas | Figures 4–8 |

---

## Repository Integration

Recommended links:

- ../CORE_CONCEPT_MAP.md — conceptual overview  
- ../FINDINGS/core_findings.md — empirical findings  
- ../VALIDATION/README.md — validation layer  
- ../NEXAH_DEVELOPMENT/gate_operator/ — gate operator experiments  

---

## Summary

These figures form the visual backbone of the NEXAH research framework.

They describe a consistent structural reduction:

Dynamics → Slice → Field → Sheets → Gates → Transitions → Connectivity → Topology

Key claim:

Topology is not imposed on the system.  
It emerges from the connectivity of coherent structural sheets extracted from dynamics.

---

## Notes

- All results are computed from trajectory data  
- No topological assumptions are imposed  
- Structural elements are robust across different dynamical systems  
- The same extraction pipeline applies to Lorenz, Rössler, Halvorsen and beyond  

---

## Practical Reading Guide

Recommended order:

1. Figure 1 — understand the conceptual pipeline  
2. Figure 2 — see how structure is extracted from data  
3. Figure 3 — verify the quantitative behavior  
4. Figures 4–8 — explore extended structure and generalizations  

---

## Positioning

This figure set bridges:

- dynamical systems (continuous trajectories)  
- geometric structure (fields, sheets, basins)  
- discrete representations (transitions, graphs)  
- topology (emergent global structure)  

It provides a unified view from motion to structure to connectivity.

---
