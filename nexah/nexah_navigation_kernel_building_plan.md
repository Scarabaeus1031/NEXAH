# NEXAH Navigation Kernel — Building Plan

This document outlines the planned architecture of the **NEXAH Navigation Kernel**.

It is **not** a code file and **not** yet a complete control implementation.

Its purpose is to define:

- what the kernel should do
- which layers it should contain
- what already exists
- what is still missing
- how the development should proceed without losing the structural insights of the current NEXAH field series

---

## 1. Current status

At the present stage, NEXAH has already produced the necessary precursors for a navigation kernel.

The strongest existing layers are:

- field extraction
- transition geometry
- grey-channel formation
- dual-strand separation
- switch-layer emergence
- **triple spiral coupling + Elastic Dual Lock (v9.x)**

This means:

> the structural prerequisites for navigation already exist,  
> but the navigation kernel itself is not yet finished.

What currently exists is best described as:

- an **axis-aware structural field**
- with **channel behavior**
- **dual-strand transport**
- **proto-switch detection**
- **coherence-guided spiral coupling**

What does **not** yet exist is a full decision engine that can:

- choose motion policies
- switch strands intentionally
- maintain goals
- avoid collapse by rule
- steer movement through the field in a controlled way

---

## 2. Guiding idea

The navigation kernel should not be understood as a generic controller.

It should not be built as:

- shortest-path optimization
- abstract reward maximization
- purely symbolic rule switching
- blind numerical steering

Instead, the kernel should implement:

> coherence-guided movement through structured transition geometry

In practical terms, this means:

- the field is primary
- the geometry is not decoration
- the channel is not a plotting artifact
- the switch layer is not just classification
- motion must stay legible in relation to structure

The kernel should therefore emerge from the chain:

field  
↓  
channel  
↓  
strand  
↓  
switch  
↓  
decision  
↓  
navigation

---

## 3. Architectural target

The long-term kernel should consist of four main layers.

### 3.1 Field Layer

This is the geometric substrate.

It provides:
- attractor structure  
- directional organization  
- coherence gradients  
- axis relations  
- region separation  
- channel formation  
- lobe and bridge geometry  

This layer already exists in large parts through the v8–v9 series.

Current evidence:
- grey channel  
- dual strands  
- 2x2 / 3x3 core structures  
- axis-aligned transport geometry  
- lobe-to-bridge transitions (blue ↔ green ↔ red)  

### 3.2 Signal Layer

This layer extracts measurable quantities from the field.

It provides:
- coherence signals  
- drift vectors (along / across axis)  
- strand identification (upper / lower)  
- distance-to-axis metrics  
- switch indicators  
- regime proximity signals  

This layer translates geometry into readable dynamics.

Current status:
- partially implemented (coherence, angular velocity, grey score)  
- needs consolidation into a unified signal interface  

### 3.3 Decision Layer

This is the core of navigation.

It determines how the system reacts to signals.

It should decide:
- remain in current channel or exit  
- move forward or backward along axis  
- switch between upper / lower strand  
- stabilize vs explore  
- avoid collapse regions  

This layer does not yet exist in a true sense.

Current status:
- implicit / passive behavior only  
- no explicit decision rules  

Target:  
> transform signals into structured decisions

### 3.4 Action Layer

This layer executes movement.

It translates decisions into actual trajectory updates.

It provides:
- step direction  
- controlled oscillation  
- correction toward channel  
- expansion / contraction motion  
- strand switching execution  

Current status:
- basic movement exists  
- but not yet coupled to decision logic  

Target:  
> controlled movement instead of passive drift

---

## 4. Development roadmap

### Phase A — Passive Alignment (completed)
- axis projection  
- grey channel detection  
- dual strand separation  
- coherence measurement  

Result: system discovers structure

### Phase B — Controlled Channel Motion (next)
Goal: enable directed motion within the grey channel  

Key tasks:
- separate axial vs transversal drift  
- introduce forward/backward directionality  
- reduce over-constraining to axis  

### Phase C — Strand Logic
Goal: treat upper and lower strands as distinct dynamical regimes  

Interpretation:
- upper strand → expansion dynamics  
- lower strand → contraction dynamics  

Key tasks:
- map strand to regime behavior  
- introduce strand-dependent motion rules  

### Phase D — Switch Layer & Spiral Coupling (v9.x)
Goal: elevate switching from detection to control  

Key tasks:
- define switch conditions  
- define switch cost / threshold  
- define switch consequences  
- integrate triple spiral coupling (Water–Mercury–Ferrofluid)  
- use Elastic Dual Lock (Span-Gurt) as active coupling mechanism  

Target: switching becomes a controlled regime transition

### Phase E — Navigation Logic
Goal: full navigation capability  

This includes:
- corridor following  
- collapse avoidance  
- branch selection  
- return paths  
- stability optimization  

---

## 5. Current system interpretation

The current kernel behavior is best described as:

> axis-locked drift inside a detected channel with emerging spiral coupling

Observed:
- high grey-channel occupancy  
- minimal switching  
- dominance of neutral states  
- rapid stabilization after transient chaos (Pair Coupling Distances → ~0)

Implication:
- system is over-stabilized  
- lacks lateral exploration  
- lacks decision-driven behavior  

---

## 6. Key insight

The grey channel is not just a passive region.

It is:

> an active transformation layer between regimes

Relations:
- blue → contraction basin  
- red → expansion seed  
- green → bridge field  
- grey → transition engine  
- **triple spiral coupling** → active magnetic flow connector

---

## 7. Immediate next step

Before extending the kernel:

- reduce axis attraction strength  
- increase lateral oscillation  
- amplify switch sensitivity  
- integrate the Spiral Coupling Kernel as the active coupling engine  

Goal:
> force visible strand differentiation and switching behavior

---

## 8. Summary

The NEXAH Navigation Kernel evolves through:

structure → field → channel → strand → switch → spiral coupling → navigation

Current position:
- structure ✔  
- field ✔  
- channel ✔  
- strand ✔  
- switch (detected) ✔  
- **spiral coupling (implemented)** ✔  
- navigation ❌  

Target:
> transform detected structure into controlled movement
