# NEXAH Research System Map

This document provides a structural overview of the experimental systems inside the NEXAH research layer.

The goal is to organize experiments not by files, but by **conceptual system types and dynamics**.

---

# Overview

The NEXAH research environment currently explores two fundamental classes of systems:

---

## 1 — Continuous Dynamical Systems

Systems with explicit time evolution and coupling dynamics.

Examples:

• Kuramoto oscillator networks  
• phase synchronization systems  
• resonance flows  
• toroidal embeddings  
• energy landscapes  

---

## 2 — Discrete Transition Systems

Systems without explicit dynamics, where structure emerges from transitions.

Examples:

• prime modular residue systems  
• transition matrices  
• drift fields  
• modular state spaces  

---

# Core Research Axes

All experiments fall into the following conceptual axes:

• topology (network structure)  
• dynamics (time evolution)  
• transitions (state changes)  
• resonance (pattern propagation)  
• stability (basins & attractors)  
• geometry (embedding & visualization)  

---

# System A — Symmetry Graph Experiments (Continuous)

These experiments investigate nonlinear oscillator dynamics on structured graphs.

---

## Structure

center node  
+ radial spokes  
+ cycle layers  

Example:

C5 + C6 + C6 = 17

---

## Key Components

### dynamics/
Kuramoto simulations, drift, energy flow  

### topology/
toroidal embeddings, Arnold webs  

### resonance/
resonance flows and channel structures  

### phase_space/
vector fields and domain maps  

### transitions/
phase transitions, basin maps  

---

## Core Insight

> Balanced topology → stable synchronization dynamics  

---

# System B — Prime Modular Transition Experiments (Discrete)

These experiments investigate structure emerging from purely discrete systems.

---

## Structure

Prime sequence:

pₙ → residues mod m  

State space:

finite modular ring  

Dynamics:

defined by transition sequence  

---

## Key Components

• transition matrices  
• residue jumps  
• drift fields  
• cross-modulus comparison  
• clustering  

---

## Core Insight

> Structured transitions → emergent flow-like behavior  

---

# Cross-System Connection

Despite different definitions:

| Continuous Systems | Discrete Systems |
|------------------|-----------------|
| phase flow | transition flow |
| vortices | drift |
| synchronization | stabilization |
| attractors | clusters |

---

## Unified Principle

> Structure emerges from transition rules — not from the system type.

---

# Supporting Infrastructure

## core/

visualization  
kernel bridge  
vortex detection  

---

## visuals/

All generated figures and experiment outputs.

---

# Experiment Workflow

General pipeline:

1. define system  
2. generate transitions / dynamics  
3. extract structure  
4. detect patterns  
5. map regimes  
6. visualize  

---

# Current Status

✔ continuous systems established  
✔ discrete systems integrated  
✔ cross-system patterns observed  

---

# Next Directions

• spectral analysis (eigenvalues)  
• normalization and scaling laws  
• random control comparison  
• mapping between discrete and continuous systems  

---

# Role in NEXAH

This research layer provides:

→ structure discovery  
→ pattern extraction  
→ system comparison  

It acts as the experimental foundation for the NEXAH framework.

---
