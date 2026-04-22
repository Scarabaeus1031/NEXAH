# NEXAH — Field Reading Guide (V6 Phase)

## Purpose

This document explains how to read and interpret the visual outputs
of the NEXAH field simulation system.

It does NOT introduce new theory.

It provides a translation layer between:

- raw simulation output
- human interpretation

---

## Core Idea

The visuals do not show objects moving in space.

They show:

→ a field (structure)  
→ and trajectories emerging from it  

Key principle:

> Motion is not imposed — it is revealed by the field.

---

## The Field

The system is based on:

- a scalar potential field V(x, y)
- a derived flow field:

    dx/dt = -∇V + rotational component

Meaning:

- ∇V → pulls toward minima (basins)
- rotation → bends trajectories

The result is:

→ structured flow instead of straight motion

---

## Key Elements

### 1. Basin (Attractor)

A basin is:

→ a region where trajectories tend to end up

Visual indicators:

- dark regions in potential maps
- convergence of trajectories
- stable endpoints

Interpretation:

→ stable state of the system

---

### 2. Trajectory

A trajectory is:

→ a path following the field

Important:

- trajectories do not "choose"
- they follow the structure of the field

Types:

- direct (escape-like)
- curved (retained / orbit-like)

---

### 3. Orbit-like Motion

Some trajectories:

- loop around basins
- form arcs or spirals

This is NOT imposed.

It emerges from:

- interaction of gradient and rotation

---

### 4. Boundary (Separatrix-like)

Boundaries are:

→ regions separating different outcomes

Observed as:

- sharp transitions in class maps
- "Riss" (split) structures
- vertical or curved bands

Interpretation:

→ small changes → different final states

---

### 5. Gate Region (G0)

A special region where:

- motion slows down
- outcomes become highly sensitive

Characteristics:

- low force magnitude
- high directional change

Interpretation:

→ decision layer of the system

---

### 6. Drift

Drift is:

→ a directional bias in the system

Effect:

- breaks symmetry
- tilts trajectories
- shifts basin dominance

Without drift:

- system would be more symmetric

With drift:

→ realistic asymmetry emerges

---

### 7. Sensitivity Zones

Some regions show:

- strong reaction to small changes

Indicators:

- bright bands in sensitivity maps
- unstable trajectory behavior

Interpretation:

→ transition amplifiers

---

### 8. Orbit Bands

Instead of single paths, we observe:

→ families of trajectories

These appear as:

- rings
- layered bands
- "rolls" or "cylinders"

Interpretation:

→ structured regions of similar dynamics

---

### 9. Interference Regions

Where multiple influences meet:

- flow becomes complex
- trajectories diverge

Typical locations:

- between basins
- near elevated regions

Interpretation:

→ competing field influences

---

### 10. Central Structure

Many maps show:

- radial patterns from a central region

Interpretation:

- structural reference point
- not a physical source

---

## How to Read the Visuals

### Q1 — Class Map

Shows:

- where trajectories end up

Colors:

- different outcome classes

Use:

→ identify basins and boundaries

---

### Q2 — Field + Trajectories

Shows:

- flow structure
- example trajectories

Use:

→ understand motion behavior

---

### Q3 — Sensitivity Map

Shows:

- where the system is unstable

Use:

→ locate transition zones

---

### Q4 — Physical Projection

Shows:

- spatial interpretation

Use:

→ connect abstract field to geometry

---

### Q5 — Orbit Bands

Shows:

- regions of similar orbit behavior

Use:

→ identify structured motion families

---

### Q6 — Representative Trajectories

Shows:

- example paths

Use:

→ understand qualitative differences

---

---

## V7 Extension — Reading Navigation & Cost Fields

The V7 layer introduces a new type of visualization:

→ not only *what the system does*  
→ but *what the system allows*

---

### 11. Cost Field

The cost field represents:

→ how difficult it is to reach a target region

Visual indicators:

- smooth gradients → easy movement  
- steep gradients → difficult transitions  
- sharp ridges → barriers  

Interpretation:

→ cost encodes a **navigation landscape**

Important:

- this is not physical energy  
- it is a **constructed effort measure**

---

### 12. Navigation Field (−∇cost)

The navigation field shows:

→ the direction of optimal movement

Visual indicators:

- arrows / flow lines  
- trajectories aligning into channels  

Interpretation:

→ trajectories follow the geometry of the cost field  

Key idea:

> optimal paths are embedded in the field — not externally computed  

---

### 13. Reachability Regions

Not all starting points can reach the target.

Visual indicators:

- clear separation between:
  - reachable zones  
  - unreachable zones  

Interpretation:

→ the system defines **where motion is possible**

---

### 14. Splinter / Transition Wedge

A central structure in V7:

→ narrow, wedge-like region connecting space to the target  

Visual indicators:

- triangular or funnel-shaped region  
- sharp boundaries  
- asymmetric geometry  

Interpretation:

→ this is the **only efficient transition corridor**

Important:

- not an artifact  
- appears consistently across methods  

---

### 15. Energy Ridge

The boundary of the splinter often appears as:

→ a ridge in the cost field  

Visual indicators:

- high-cost line or arc  
- strong gradient change  

Interpretation:

→ crossing this region requires significantly higher effort  

---

### 16. Curved Convergence ("Hook")

Trajectories approaching the target:

- do not move straight  
- bend into the attractor  

Visual indicators:

- arc-shaped approach paths  
- spiral or hook-like structures  

Interpretation:

→ convergence follows field geometry, not direct distance  

---

### 17. Directional Boundaries

Boundaries in V7 are:

- not symmetric  
- not equally crossable from all directions  

Observed:

- some angles allow crossing  
- others deflect trajectories  

Interpretation:

→ boundaries act as **directional gates**

---

### 18. Alignment with V6 Structures

The V7 visuals should be read together with V6:

- splinter ↔ "Riss"  
- reachability ↔ class boundaries  
- cost ridges ↔ sensitivity zones  

Interpretation:

→ both layers describe the same structure  
→ from different perspectives  

---

### 19. Reading Strategy (V6 + V7)

To interpret a scene:

1. Identify basins (V6)  
2. locate boundaries (V6)  
3. check sensitivity zones (V6)  
4. overlay cost structure (V7)  
5. identify reachable corridor (V7)  

Result:

→ a complete picture of:

- structure  
- dynamics  
- navigation constraints  

---
---

## V8–V10 Extension — Reading Stability, Transport, and Time

With V8–V10, the visuals extend beyond structure and navigation.

They now show:

→ **how stable the system is**  
→ **how movement propagates**  
→ **how transitions evolve over time**

---

### 20. Stability Field (Lyapunov Map)

The stability map shows:

→ how trajectories behave under small perturbations  

Visual indicators:

- dark regions → stable (converging flow)  
- bright regions → unstable (diverging flow)  

Important:

- stability is **not uniform**
- it forms **structured ridges and basins**

Interpretation:

→ the field contains a **stability geometry layer**

---

### 21. Boundary vs Stability

A key insight:

- boundaries (V6/V7)  
- stability (V8)  

→ do NOT coincide

Meaning:

- a region can be:
  - stable but still a boundary  
  - unstable but not a transition  

Interpretation:

→ different structural layers coexist  

---

### 22. Gate Points (Weak Stability Regions)

Along boundaries, some regions show:

- slightly reduced stability  

Visual indicators:

- local maxima in Lyapunov map  

Interpretation:

→ these are **entry points into transition zones**  

Important:

- they do NOT create new outcomes  
- they only **enable passage**

---

### 23. Transport Map (V9)

Transport maps show:

→ where trajectories from a region end up  

Visual indicators:

- colored paths (e.g. orbit / core / escape)  
- structured flow patterns  

Interpretation:

→ the system defines a **mapping from input → outcome**

Key insight:

→ transport is **not random**  
→ it is geometrically constrained  

---

### 24. Channels

Certain regions act as:

→ preferred pathways through the system  

Visual indicators:

- dense bundles of trajectories  
- aligned flow lines  

Interpretation:

→ these are **transport channels**

Important:

- not all paths are equally likely  
- flow concentrates into **specific routes**

---

### 25. Regime Structure (V9.8+)

The field can be decomposed into:

- orbit regions  
- shear regions  
- escape regions  
- drift regions  

Interpretation:

→ the system consists of **distinct motion regimes**

Each regime:

- has its own behavior  
- follows its own geometry  

---

### 26. Temporal Signals (V10)

Tracking boundary or field intensity over time reveals:

- smooth evolution  
- sudden increases before transitions  

Visual indicators:

- rising boundary signal  
- correlation with system collapse (in IEEE tests)

Interpretation:

→ boundaries act as **early-warning indicators**

---

### 27. Reading Time Evolution

Instead of static maps:

→ read the system as evolving in time  

Key questions:

- where does structure change?  
- where does instability grow?  
- where do transitions begin?  

Interpretation:

→ the field is **dynamic, not static**

---

## Updated Reading Strategy (V6 → V10)

To fully interpret a scene:

1. Identify structure (basins, boundaries) — V6  
2. understand navigation constraints — V7  
3. analyze stability distribution — V8  
4. trace transport paths — V9  
5. observe temporal signals — V10  

---

## Final Insight (Updated)

```text
The system is not just a field.

It is a structured, dynamic, and directed flow system
with constrained motion, stable regions, and predictable transitions.
```

---
---

## Important Notes

This system is **computational and exploratory**, but not arbitrary.

- based on reproducible simulations  
- structurally consistent across multiple layers (V6–V10)  
- partially validated on real-world systems (e.g. IEEE grids)  

It does NOT claim:

- new physical laws  
- exact real-world equivalence  
- closed-form analytical solutions  

It DOES provide:

→ a **structured dynamical field framework**  
→ consistent geometric and stability patterns  
→ a basis for further mathematical and applied analysis  

---

## Interpretation Layer

Some terms used during exploration:

- "Riss" → transition boundary  
- "Korbstruktur" → layered orbit bands  
- "Gate" → locally weakened stability region  
- "Channels" → preferred transport paths  

These are:

→ intuitive descriptors  
→ grounded in observed structure  
→ candidates for later formalization  

---

## Final Thought

The system demonstrates:

- how structure generates motion  
- how motion reveals hidden geometry  
- how simple components produce constrained complexity  

Understanding emerges from:

→ reading the field  
→ interpreting structure, stability, and flow together  

---

## Final Insight

```text
The field does not describe what could happen.

It describes what can happen.
