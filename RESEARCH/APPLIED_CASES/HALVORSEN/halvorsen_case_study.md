# 🔬 NEXAH — Halvorsen System Case Study

## 🧭 Purpose

This document presents a full structural and control analysis  
of the Halvorsen system within the NEXAH framework.

It demonstrates that:

```text
NEXAH applies beyond classical attractor systems
to fragmented, multi-interaction dynamical fields
```

---

# 🧠 System Overview

The Halvorsen system is defined by:

$$
\begin{aligned}
\dot{x} &= -a x - 4y - 4z - y^2 \\
\dot{y} &= -a y - 4z - 4x - z^2 \\
\dot{z} &= -a z - 4x - 4y - x^2
\end{aligned}
$$

---

## Properties

- chaotic dynamics  
- strong nonlinearity  
- fragmented attractor structure  
- multi-directional flow interaction  

---

## Role in NEXAH

```text
Halvorsen serves as a stress test for structural extraction.
```

Unlike Lorenz, it lacks simple global symmetry.

---

# 🔬 1. Empirical Structure

Observed:

- no simple lobe structure (unlike Lorenz)  
- no simple spiral (unlike Rössler)  

---

## 🖼️ Figure A — Field Structure (Generalized)

![Field Structure](../../FIGURES/fig_01_field_structure.png)

---

## Interpretation

```text
Structure exists, but it is fragmented and distributed.
```

The system decomposes into multiple locally coherent regions  
instead of a global attractor geometry.

---

# 🌀 2. Field Structure

From trajectory and density:

```text
trajectory → density → flow → structure
```

Observed:

- multiple interacting flow regions  
- irregular density distribution  
- no globally dominant structure  

---

## Interpretation

```text
Structure emerges locally, not globally
```

---

# 🧩 3. Gate Structure (Critical)

From:

```text
detect_gates_halvorsen.py
build_gate_graph_halvorsen.py
```

Observed:

- multiple gate regions  
- irregular placement  
- non-symmetric transitions  

---

## Key Insight

```text
Gates exist even in fragmented systems
```

---

# 🔁 4. Transition Structure

From:

```text
extract_transitions_halvorsen.py
reachability_halvorsen.py
```

Observed:

- transitions are:
  - structured  
  - constrained  
  - multi-path  

NOT:

```text
random jumps
```

---

## 🖼️ Figure B — Transition Geometry (Generalized)

![Transition Geometry](../../FIGURES/fig_02_transition_geometry.png)

---

## Interpretation

```text
Transitions follow complex connectivity patterns
```

---

# 🧠 5. Graph Structure

From:

```text
build_gate_graph_halvorsen.py
connect_components_halvorsen.py
```

Observed:

- system decomposes into connected regions  
- transitions form a graph  

---

## Interpretation

```text
Continuous system → discrete connectivity structure
```

---

# ⚡ 6. Control & Policy Layer

From:

```text
policy_gradient_halvorsen.py
gate_aware_policy_halvorsen.py
global_policy_halvorsen.py
```

Observed:

- control is:
  - localized  
  - path-dependent  
  - non-linear  

---

## Key Insight

```text
Control operates on structure, not on state
```

---

# 🧠 7. Phase & Mismatch (Generalized)

Even without clear global phase coherence:

- local phase-like dynamics exist  
- mismatch regions correlate with transitions  

---

## 🖼️ Figure C — Phase Mismatch (Generalized)

![Phase Mismatch](../../FIGURES/fig_03_phase_mismatch.png)

---

## Interpretation

```text
Phase mismatch remains a transition driver,
even in irregular systems
```

---

# 🔁 8. Flow Decomposition

From:

```text
flow_decomposition_halvorsen.py
flow_residue_alignment_halvorsen.py
```

Observed:

- flow can be decomposed into components  
- residue structures exist  

---

## Interpretation

```text
System dynamics contain hidden structural layers
```

---

# 🌉 9. Bridge & Path Planning

From:

```text
adaptive_bridge_halvorsen.py
plan_path_halvorsen.py
```

Observed:

- transitions can be planned  
- paths exist between regions  

---

## Insight

```text
Navigation is possible even in fragmented systems
```

---

# 🧠 10. Comparison to Other Systems

| Property | Lorenz | Rössler | Halvorsen |
|----------|--------|--------|----------|
| Structure | dual-lobe | spiral | fragmented |
| Transitions | discrete | smooth | multi-path |
| Control | phase-aligned | smooth | graph-based |

---

# 🔷 11. Topology

Observed:

- no simple topology (Möbius / torus)  

Instead:

```text
irregular connectivity topology
```

---

## Interpretation

```text
Topology emerges from connectivity, not symmetry
```

---

# 🔥 12. Core Results

```text
1. Structure exists without global symmetry
2. Gates persist in fragmented systems
3. Transitions are structured and constrained
4. Connectivity defines system organization
5. Control operates via structural pathways
6. Navigation is possible in irregular dynamics
```

---

# 🧠 Unified Interpretation

```text
The Halvorsen system is not chaotic noise.

It is a structured, navigable field
with complex connectivity.
```

---

# 🚀 Role in NEXAH

The Halvorsen system provides:

- validation beyond symmetric systems  
- demonstration of robustness  
- extension to irregular dynamics  

---

# 🔥 Final Insight

```text
NEXAH does not depend on system simplicity.

It reveals structure even in highly irregular,
fragmented dynamical systems.
```

---

**NEXAH Case Study — Halvorsen System**  
Thomas K. R. Hofmann · 2026
