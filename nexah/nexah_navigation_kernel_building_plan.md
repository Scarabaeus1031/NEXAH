# NEXAH Navigation Kernel — Building Plan 
*(neu APPLICATIONS/power_systems/ieee_xray_pipeline/README.md)*

This document outlines the planned architecture of the **NEXAH Navigation Kernel**.

It is not a code file and not yet a complete control implementation.

Its purpose is to define:

- what the kernel should do  
- which layers it should contain  
- what already exists  
- what is still missing  
- how development proceeds toward an operational navigation system  

---

## 1. Current status

NEXAH has already produced the structural prerequisites for a navigation kernel.

The strongest existing components are:

- field extraction  
- transition geometry  
- grey-channel formation  
- dual-strand separation  
- switch-layer emergence  

Recent extensions include:

- triple spiral coupling + Elastic Dual Lock (v9.x)  
- URF Axial Space + Root Bridge (v9.1)  

This means:

> the system already detects structure, channels, and transition zones —  
> but does not yet perform controlled navigation.

What exists:

- an axis-aware structural field  
- channel behavior (grey channel)  
- dual-strand transport  
- switch detection  
- early coherence signals  

What is missing:

- decision-making  
- controlled movement  
- goal-directed navigation  
- active collapse avoidance  

---

## 2. Guiding idea

The navigation kernel is not a generic controller.

It implements:

> movement through a system based on its structural dynamics

Key principles:

- the field representation is primary  
- channels represent valid motion regions  
- switches represent regime transitions  
- motion must remain aligned with structure  
- navigation must remain interpretable  

The kernel emerges from:

```text
field → channel → strand → switch → decision → navigation
```

---

## 3. Architectural target

The navigation kernel consists of five layers:

### 3.1 Field Layer
Provides the geometric structure:

- attractors and basins  
- directional flow  
- coherence gradients  
- region separation  
- channel formation  

### 3.2 Signal Layer
Extracts interpretable signals from the field:

- coherence  
- drift direction  
- distance to channel  
- strand classification (upper / lower)  
- switch indicators  
- regime proximity  

### 3.3 Decision Layer
Defines navigation logic:

- stay in channel vs exit  
- strand switching  
- stability vs exploration  
- collapse avoidance  

### 3.4 Action Layer
Executes motion:

- step direction  
- correction toward channel  
- oscillatory stabilization  
- controlled strand switching  

### 3.5 Geometric Reference Layer (Experimental)

Includes:

- URF Axial Space  
- Root Cube  
- Root Bridge  

Purpose:

- provide a stable coordinate reference  
- embed structure in a consistent geometry  
- support future 3D navigation  

This layer is experimental and not yet part of the validated core system.

---

## 4. Development roadmap

### Phase A — Structure & Field (completed)
- structure extraction  
- field representation  
- coherence detection  

### Phase B — Channel Formation (completed)
- grey channel  
- axis alignment  
- dual strands  

### Phase C — Switch Detection (completed)
- regime boundaries  
- transition points  

### Phase D — Controlled Motion (ongoing)
- movement within channel  
- drift stabilization  

### Phase E — Navigation Logic (next)
- corridor following  
- collapse avoidance  
- branch selection  
- return paths  

### Phase F — Extended Geometry (experimental)
- integration of URF Axial Space  
- Root Bridge embedding  
- higher-dimensional structure mapping  

---

## 5. Current system interpretation

The system currently behaves as:

> a structure-aware field with stable channel formation and detectable transition points

Observed:

- high channel stability  
- clear separation of strands  
- consistent switch detection  

Limitation:

- no active steering  
- no explicit navigation decisions  

---

## 6. Key insight

The grey channel is not just a visualization artifact.

It represents:

> a structurally valid region of motion within the system

Switch points represent:

> transitions between stability regimes

This provides the basis for navigation.

---

## 7. Immediate next step

- connect signal layer to decision logic  
- implement simple motion policies  
- validate navigation behavior on IEEE systems  

Goal:

> transform structural detection into controlled movement

---

## 8. Summary

The NEXAH Navigation Kernel evolves through:

```text
structure → field → channel → strand → switch → navigation
```

Current position:

- structure ✔  
- field ✔  
- channel ✔  
- strand ✔  
- switch ✔  
- navigation ❌  

Target:

> transform detected structure into controlled movement
