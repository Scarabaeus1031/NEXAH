# ⚡ Stability Field Dynamics — IEEE Systems

## Overview

This module transforms classical power system stability analysis into a:

- continuous field representation  
- dynamic flow system  
- memory-based recurrence model  
- resonance-driven structure formation  
- topological state graph  

Standard IEEE test systems (starting with 14-bus) are used as real-world benchmarks.

---

## Core Idea

> Stability is not a binary state — it is a geometry.  

Extended into:

- Geometry → field representation  
- Field → flow dynamics  
- Dynamics → memory (recurrence)  
- Memory → resonance structure  
- Resonance → coupled system  

---

## Development Levels

| Level | Description |
|------|-------------|
| V1–V3 | Stability field + boundary detection |
| V4–V7 | Bipolar field, folds, eigenmodes |
| V8–V10 | Current field, time evolution, recurrence |
| V11–V13 | State detection, closure, activation |
| V14–V15 | Resonance detection, dual-band structure |
| V15b | Gap stabilization → first loops + states |
| V16 | State graph + loop topology |
| V17 | Coupling metric (P × R × L) |
| V17b | Coupling heatmap (birth zones) |
| V21 | Phase scan → stable coupling regime |

---

## Key Results — IEEE 14 (Coupled System)

- Dual resonance peaks:
  - Band A ≈ 0.008  
  - Band B ≈ 0.84  

- Gap:
  - ≈ 0.832 (active interface)

- Emergent structure:
  - States: 2  
  - Loops: 6  
  - Interface-coupled dynamics  

- Coupling metric:
  - C ≈ 0.0036  
  - P ≈ 0.47 (flow persistence)  
  - R ≈ 0.27 (recurrence concentration)  
  - L ≈ 0.028 (loop density)  

---

## Key Results — IEEE 9 (Diffuse System)

- Dual resonance peaks:
  - ≈ 0.007, ≈ 0.012  

- Gap:
  - ≈ 0.004  

- Structure:
  - States: 0  
  - Loops: 0  

---

## Fundamental Discovery

Both systems share the same structural decomposition:

→ **3 + 1 structure**

- Band A  
- Band B  
- Gap  
- Global flow field  

BUT:

| System | Behavior |
|--------|----------|
| IEEE 9 | latent structure (decoupled) |
| IEEE 14 | coupled system (active dynamics) |

---

## Coupling Metric

We define:

C = P × R × L

Where:

- P → flow persistence  
- R → recurrence concentration  
- L → loop density  

Interpretation:

- C ≈ 0 → diffuse field  
- C > 0 → system formation  

---

## Coupling Field (New)

Coupling is spatially localized:

C(x,y) = P(x,y) × R(x,y) × L(x,y)

Result:

- structure emerges only in **localized regions**
- these regions are:

→ **Birth Zones of Structure**

---

## Phase Behavior (IEEE 14)

Parameter scan (base load):

- system remains invariant  
- coupling metric constant  
- topology unchanged  

Interpretation:

→ system resides in a **stable coupling regime**

This implies:

- existence of a **phase plateau**
- structural robustness

---

## System Classification

We distinguish:

### 1. Diffuse Field
- no loops  
- no states  
- no coupling  

### 2. Transition Field
- partial structure  
- unstable dynamics  

### 3. Coupled Field
- stable loops  
- stable states  
- persistent coupling  

---

## Architecture Layers

1. **Field Layer**
   - continuous geometry  

2. **Dynamic Layer**
   - trajectories / flow  

3. **Memory Layer**
   - recurrence  

4. **Resonance Layer**
   - band structure  

5. **Topological Layer**
   - states + loops  

6. **Coupling Layer (NEW)**
   - interaction zones  
   - structure emergence  

---

## Repository Structure

APPLICATIONS/power_systems/stability_field_dynamics/
│
├── ieee_test_cases/
│   ├── run_scan_v*.py
│   ├── *_dynamics_v*.py
│   ├── state_graph_v*.py
│   ├── coupling_metric_v17.py
│   ├── validate_ieee9.py
│
├── logs/
│   └── stability_field_log.md
