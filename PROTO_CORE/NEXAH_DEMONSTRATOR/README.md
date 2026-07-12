# 🧪 NEXAH — Gate Operator & Transition Structure (Demonstrator)

## 🧭 Overview

This module demonstrates a **geometry-based approach to analyzing dynamical systems**,  
focusing on how **structure, instability, and transitions emerge from trajectories**.

The core idea is simple:

```text
We do not impose transitions as discrete events.
We extract them from the observed structure of the system.
```

---

## 🔁 Pipeline

All experiments follow a consistent pipeline:

```text
System → Trajectories → Field → Structure → Transitions → Navigation
```

This separates the problem into two layers:

```text
1. Continuous field (density, flow, instability)
2. Discrete structure (sheets, transitions)
```

---

## 🔬 What This Module Does

This repository implements and tests:

### 1. Field Construction

From simulated trajectories (e.g. Lorenz):

- density field ρ(x) (via KDE)  
- flow field F(x)  
- derived quantities:
  - coherence C(x)
  - rotation R(x)

---

### 2. Gate Operator

A continuous instability measure:

$$
G(x) = (1 - \hat{\rho})(1 - \hat{C})(1 - \hat{R})
$$

Interpreted as:

```text
high G(x) → local structural instability
low G(x) → stable region
```

---

### 3. Transition Structure

A discrete representation induced from the trajectory:

```text
s(t) = sheet index
```

From this:

- transition events:  
  ```text
  s(t) ≠ s(t-1)
  ```

- transition matrix:
  $$
  P(i \rightarrow j)
  $$

---

### 4. Navigation Kernel

A hybrid motion model:

```text
continuous flow
+ structure-aware correction
```

$$
\dot{x} = F(x) - \lambda \nabla G(x) + \mu \nabla \rho(x)
$$

combined with:

```text
discrete transition constraints from P(i → j)
```

---

## 🔍 Key Observations (from Experiments)

The following findings are directly supported by the implemented experiments:

---

### 1. Structure emerges from trajectories

```text
trajectory aggregation → density → geometry
```

No explicit model of structure is required.

---

### 2. Transitions are not point events

Observed:

```text
• no isolated spikes
• transitions occur over regions
```

---

### 3. Transition structure is local

Transition matrices show:

```text
• strong diagonal dominance
• transitions only between neighboring states
```

→ the system behaves like a **banded Markov process**

---

### 4. Gate operator detects instability — not transitions

Empirically:

```text
• high G(x) does not guarantee a transition
• many transitions occur without strong G(x)
```

Interpretation:

```text
G(x) = local instability field
NOT a transition detector
```

---

### 5. Transitions require structure

Reliable transitions occur only when:

```text
sheet switch (discrete)
+ interaction with instability (continuous)
```

---

### 6. No evidence for sparse “gate events”

From transition matrix analysis:

```text
• no rare edges
• no isolated transitions
```

Interpretation:

```text
transitions are distributed processes,
not discrete triggers
```

---

## 🧠 Resulting Model

The system is best described as a **hybrid dynamical system**:

```text
STATE = (x(t), s(t))
```

with:

```text
continuous dynamics → geometry & instability
discrete dynamics → structural transitions
```

---

## ⚠️ What This Is NOT

This module does **not** claim:

- a universal theory of dynamical systems  
- optimal control solutions  
- formal proofs of stability or convergence  

It is:

```text
an empirical, code-driven exploration of structure in dynamics
```

---

## 📂 Module Structure

```text
scripts/
    run_demo.py                 → canonical entry point
    generate_transition_structure.py → importable reference-data generator
    kernel/                     → continuous gate and navigation layer
    hero/                       → transition-aware navigation

visuals/
    generated data, plots, and curated figures
```

---

## ▶️ How to Run

Requirements:

- Python 3.10 or newer
- dependencies installed through the repository package

Follow the installation steps in the repository **[Quick Start](../../README.md#-quick-start)**.

Then, from the repository root, run:

```bash
python PROTO_CORE/NEXAH_DEMONSTRATOR/scripts/run_demo.py
```

This command executes three stages:

```text
1. Transition Structure → discrete sheets and transition matrices
2. Navigation Kernel    → continuous gate-aware field behavior
3. Hero Animation       → transition-aware navigation
```

The run is complete when the terminal reports:

```text
✅ All steps completed.
```

The complete Quick Start was verified with Python 3.12. Generated figures and
data are written below `PROTO_CORE/NEXAH_DEMONSTRATOR/visuals/`.

Primary outputs:

```text
visuals/structure/transition_structure_timeseries.png
visuals/structure/transition_structure_matrix.png
visuals/structure/transition_structure_phase.png
visuals/structure/transition_matrix.npy
visuals/structure/transition_matrix_prob.npy
visuals/structure/transition_trajectory.npy
visuals/hero/nexah_transition_navigation_v13.gif
```

`generate_transition_data()` exposes the deterministic Lorenz trajectory,
constructed radial-sheet labels, transition events, and matrices directly for
tests and downstream validation. The historical sheet construction is preserved
unchanged: requesting six sheets currently yields seven observed labels because
the maximum radius enters an additional `np.digitize` boundary bin. This is a
recorded Demonstrator limitation, not an externally validated regime model.

---

## 📊 Key Outputs

- Gate-field and navigation visualizations
- Sheet-partition plots
- transition count and probability matrices
- time series of structural switching
- transition-aware navigation animation

---

## 🔗 Related Documents

- `gate_operator.md` → definition of G(x)  
- `transition_structure.md` → discrete transition model  
- `navigation_kernel.md` → hybrid motion model  

---

## 🚀 Why This Matters

This work suggests a shift in perspective:

```text
From:
    predicting trajectories

To:
    extracting and navigating structure
```

If validated further, this could impact:

- transition detection  
- control of nonlinear systems  
- interpretation of complex dynamics  

---

## 🧠 Summary

```text
Dynamical systems generate structure.

Structure defines transitions.

Transitions are not events —
they are movements within that structure.
```

---

**NEXAH Demonstrator — Gate Operator & Transition Structure**  
Thomas K. R. Hofmann · 2026
