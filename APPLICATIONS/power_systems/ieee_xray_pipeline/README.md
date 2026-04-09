# NEXAH IEEE X-Ray Pipeline — Building Plan

This document outlines the planned architecture of the **NEXAH IEEE X-Ray Pipeline**.

Its purpose is to define how NEXAH will be applied systematically to IEEE power systems in order to extract:

- classical baseline behavior  
- structural field dynamics  
- channel and switch structure  
- early instability signals  
- future navigation and intervention logic  

It is not yet a complete control system.

It is the first **full diagnostic pipeline** that moves from:

```text
IEEE system → structure → field → channel → switch → decision → navigation
```

---

## 1. Current status

NEXAH already provides the structural prerequisites for this pipeline.

The strongest existing components are:

- field extraction  
- transition geometry  
- grey-channel formation  
- dual-strand separation  
- switch-layer emergence  
- early coherence signals  
- IEEE early-warning results  

Recent extensions include:

- triple spiral coupling + Elastic Dual Lock (v9.x)  
- URF Axial Space + Root Bridge (v9.1, experimental)  

This means:

> the system already detects structure, channels, and transition zones in dynamical systems,  
> but does not yet provide a full operational navigation pipeline for IEEE grids.

What already exists:

- an axis-aware structural field  
- channel behavior (grey channel)  
- dual-strand transport  
- switch detection  
- early coherence signals  
- initial early-warning results on IEEE systems  

What is still missing:

- a unified IEEE analysis pipeline  
- a clean baseline vs NEXAH comparison  
- structured decision logic  
- controlled movement / intervention logic  
- reproducible reporting across multiple grids  

---

## 2. Guiding idea

The IEEE X-Ray Pipeline is not a generic simulator wrapper.

It implements:

> structural diagnosis of power-system dynamics through field, channel, and switch analysis

Key principles:

- the classical baseline remains visible  
- the field representation is primary  
- channels represent valid motion regions  
- switches represent regime transitions  
- the system must remain interpretable  
- every added layer must improve real diagnostic value  

The pipeline emerges from:

```text
classical baseline → field → channel → strand → switch → decision → navigation
```

---

## 3. Architectural target

The full IEEE X-Ray Pipeline consists of six layers.

### 3.1 Classical Baseline Layer
Provides the reference system behavior:

- voltage magnitude  
- phase angle  
- load evolution  
- branch loading  
- classical collapse time  

This layer defines what standard methods see and when they see it.

---

### 3.2 Field Layer
Provides the structural geometry:

- attractors and basins  
- directional flow  
- coherence gradients  
- region separation  
- transition manifolds  
- channel formation  

This is the first true NEXAH layer.

---

### 3.3 Signal Layer
Extracts interpretable signals from the field:

- coherence  
- drift direction  
- distance to channel  
- strand classification (upper / lower)  
- switch indicators  
- regime proximity  
- early instability markers  

---

### 3.4 Channel & Switch Layer
Describes valid motion and transition structure:

- grey-channel detection  
- axis alignment  
- dual-strand separation  
- switch region localization  
- collapse-near transition zones  

This is where structure becomes operationally meaningful.

---

### 3.5 Decision Layer
Defines navigation-ready system logic:

- stay in channel vs exit  
- stabilize vs monitor  
- switch strands  
- alert on collapse proximity  
- prioritize stability-preserving motion  

This layer begins the shift from diagnosis to action.

---

### 3.6 Geometric Reference Layer (Experimental)
Includes:

- URF Axial Space  
- Root Cube  
- Root Bridge  

Purpose:

- provide an extended coordinate reference  
- embed extracted structure in a consistent geometry  
- support future 3D navigation and intervention concepts  

This layer is experimental and not yet part of the validated core pipeline.

---

## 4. Development roadmap

### Phase 0 — Setup & Benchmark Lock (immediate)
- choose primary benchmark system  
- connect pandapower / IEEE data cleanly  
- define reproducible baseline  
- store first reference outputs  

Recommended start:
- IEEE 57-Bus for fast iteration  
- IEEE 118-Bus for stronger realism  

---

### Phase 1 — IEEE X-Ray Core (next)
- baseline extraction  
- field representation  
- channel detection  
- switch detection  

Goal:

> identify where instability begins structurally, before classical collapse is visible

---

### Phase 2 — Decision Layer
- connect signal layer to simple decision rules  
- HOLD / MONITOR / SWITCH / ALERT logic  
- compare decision timing against classical collapse indicators  

Goal:

> move from structural observation to operational interpretation

---

### Phase 3 — Mic-Drop Visualization
- clean comparison plots  
- one-figure summary  
- reproducible report generation  
- minimal dashboard or notebook  

Goal:

> show clearly that NEXAH sees instability earlier and structurally

---

### Phase 4 — Extended Geometry (experimental)
- integrate URF Axial Space  
- Root Bridge embedding  
- higher-dimensional structural mapping  
- optional spiral / resonance overlays  

Goal:

> test whether extended geometry improves interpretability or intervention logic

---

## 5. Current system interpretation

At the current stage, the system behaves as:

> a structure-aware field diagnostic with stable channel formation and detectable transition points

Observed:

- high channel stability  
- clear separation of strands  
- consistent switch detection  
- early instability signals before classical collapse  

Current limitation:

- no full intervention logic  
- no robust closed-loop control  
- no final navigation engine yet  

---

## 6. Key insight

The grey channel is not just a visualization artifact.

It represents:

> a structurally valid region of motion within the system

Switch points represent:

> transitions between stability regimes

In IEEE systems, this means:

> instability may become visible first as structural deformation in the field,  
> before it becomes visible as classical voltage collapse.

This is the central working hypothesis of the pipeline.

---

## 7. Immediate next step

- build the first clean IEEE 57 / 118 pipeline  
- compare classical voltage curve vs NEXAH field signals  
- implement minimal signal-based decision logic  
- generate one reproducible mic-drop figure  

Goal:

> establish a robust baseline for full IEEE structural diagnosis

---

## 8. Summary

The NEXAH IEEE X-Ray Pipeline evolves through:

```text
baseline → field → channel → strand → switch → decision → navigation
```

Current position:

- baseline ✔  
- field ✔  
- channel ✔  
- strand ✔  
- switch ✔  
- decision ⚠️ emerging  
- navigation ❌  

Target:

> transform structural detection into interpretable and ultimately controllable movement within complex power-system dynamics
