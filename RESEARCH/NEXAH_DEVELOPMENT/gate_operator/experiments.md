# 🧪 NEXAH — Gate Operator Experiments

## 🧭 Purpose

This document defines **systematic experiments** to evaluate the NEXAH Gate Operator:

$$
G(x) = (1 - \hat{\rho})(1 - \hat{C})(1 - \hat{R})
$$

Goals:

- test consistency across systems  
- evaluate alignment with transitions  
- identify failure modes  

---

# 🔁 Experiment Pipeline

All experiments follow:

```text
System → Trajectories → Field → G(x) → Transition Analysis
```

---

# 🔬 Experiment 1 — Baseline (Lorenz System)

## Setup

System:

$$
\dot{x} = \sigma(y-x), \quad
\dot{y} = x(\rho - z) - y, \quad
\dot{z} = xy - \beta z
$$

Parameters:

```text
σ = 10, ρ = 28, β = 8/3
```

---

## Evaluation

```text
Do high G(x) regions align with trajectory switching behavior?
```

---

## Result (Observed)

- Gate regions appear between attractor lobes  
- Gates are **spatially extended**, not point-like  
- Structure is consistent with transition intuition  

---

# 🔬 Experiment 2 — Cross-System Consistency

## Systems

- Lorenz  
- Rössler  
- Kuramoto (projected)

---

## Goal

```text
Does G(x) detect similar transition regions across systems?
```

---

## Results (Observed)

### ✔ Lorenz

- Gate regions located between attractor branches  
- clear geometric transition zones  

---

### ✔ Rössler

- central instability region detected  
- circular structure → gate near core  

---

### ⚠ Kuramoto (Important Finding)

Observed:

```text
• density collapses into a narrow vertical strip  
• rotation collapses to 1D structure  
• gate shows sharp boundary edges
```

---

## Interpretation — Degenerate Structure

The Kuramoto projection behaves fundamentally differently:

```text
This is NOT a volumetric phase space.
```

Instead:

```text
the system evolves on a low-dimensional manifold
embedded in a higher-dimensional space.
```

---

## Key Insight

```text
Kuramoto acts like a measurement probe,
not a full field.
```

More precisely:

- the (r, ψ) projection captures **collective synchronization state**
- not the full oscillator dynamics  

---

## Conceptual Interpretation

```text
Kuramoto behaves like a "cross-sectional probe"
through the dynamical system.
```

Analogy:

```text
like inserting a measurement strip into a flow field
```

---

## Structural Consequence

```text
Gate Operator requires volumetric structure.
```

It fails or degenerates when:

```text
phase space collapses to low-dimensional manifolds
```

---

# 🔬 New Finding — Structural Regimes

From experiments so far:

---

## Type A — Volumetric Systems

Examples:

- Lorenz  
- Rössler  

Properties:

```text
• full 2D/3D field structure  
• meaningful density gradients  
• gates are spatial regions  
```

---

## Type B — Degenerate / Projected Systems

Example:

- Kuramoto (r, ψ projection)

Properties:

```text
• structure collapses to thin strip  
• no true gates  
• boundary artifacts appear  
```

---

## 🔬 Observation — Gradient Strip Artifact

In projected systems (e.g. Kuramoto):

- density collapses into a narrow band
- gradient becomes one-dimensional
- visualization produces apparent strip patterns

### Interpretation

These strips are not intrinsic structural features.

They result from:

- low-dimensional embedding
- density gradient discretization
- visualization mapping

### Insight

The system exhibits:

```text
gradient-dominated structure with reduced dimensionality
```

## 🔥 Key Insight

```text
The Gate Operator is valid only for systems with sufficient geometric dimensionality.
```

---

# 🔬 Experiment 3 — Component Ablation (Next)

## Goal

Understand contribution of each term:

$$
\rho(x), \quad C(x), \quad R(x)
$$

---

## Variants

```text
G₁ = (1 - ρ̂)
G₂ = (1 - Ĉ)
G₃ = (1 - R̂)
G_full = combined
```
---

## Target Question

```text
Is rotation essential or does density already explain transitions?
```

## 🔬 Result — Ablation Study

Observed:

- Density alone produces smooth inverse structure  
- Rotation introduces directional separation  
- Combined gate highlights regions of structural conflict  

Conclusion:

```text
Rotation is essential for capturing transition-relevant structure.
```

# 🔬 Experiment 3.1 — Gate Alignment with Transitions

## Goal

```text
Evaluate whether high G(x) values align spatially and temporally
with observed transitions.
```

---

## Method

- Overlay transition points on trajectory
- compare with G(x) field
- analyze temporal distribution of G(x)

---

## Observations

- transition points cluster in specific regions of phase space
- G(x) often increases near transition zones
- but alignment is not exact

---

## Key Finding

```text
G(x) correlates with transition regions,
but does not precisely localize transition events.
```

---

## Interpretation

```text
G(x) highlights regions of instability,
not discrete transition events.
```

---

# 🔬 Experiment 3.2 — Prediction Capability

## Goal

```text
Test whether G(x) can anticipate transitions
before they occur.
```

---

## Method

- detect peaks in G(x)
- compare timing with transition indices
- measure lead/lag behavior

---

## Observations

- some G(x) peaks occur shortly before transitions
- other peaks occur without any transition
- many transitions occur without strong preceding peak

---

## Key Finding

```text
G(x) has partial predictive power,
but produces both false positives and false negatives.
```

---

## Interpretation

```text
G(x) captures rising instability,
but lacks structural awareness of system state.
```

---

## Critical Insight

```text
Prediction based on G(x) alone is unreliable.
```

It requires:

```text
structural context (system state / sheet / basin)
```

---

# 🔬 Experiment 3.3 — False Positives & Structural Misalignment

## Goal

```text
Evaluate how well G(x) corresponds to true structural transitions
versus local instability peaks.
```

---

## Method

1. Detect peaks in the Gate Operator:

```text
G(x) > threshold
```

2. Compare detected peaks with known transition indices.

3. Classify events:

```text
TP = true positives
FP = false positives
FN = false negatives
```

---

## Result (Observed)

Observed result:

```text
Precision ≈ 0.50
Recall ≈ 0.02
```

Interpretation:

```text
G(x) produces some meaningful high-instability peaks,
but it misses most actual transitions when used alone.
```

---

## Critical Observation

```text
High G(x) does not automatically imply transition.

Low G(x) does not automatically imply stability.
```

---

# 🧩 Structural Analysis

Visual inspection shows:

- repeating arc-like patterns in the signal
- layered structures in phase space
- discrete switching behavior over time
- false positives often occur as local instability peaks without global transition

---

# 🔥 Interpretation — Sheet Structure

The system exhibits layered flow structure:

$$
\mathcal{S}_i = \{(r,\theta) \mid r \approx r_i\}
$$

Each sheet corresponds to a locally coherent dynamical regime.

---

# 🔁 Sheet Switching

Transitions are not fully defined by peaks in $G(x)$.

Instead, transitions appear when the trajectory switches between structural layers:

```text
transition(t) = sheet(t) ≠ sheet(t-1)
```

---

# 🔥 Core Insight

```text
Transition =
sheet switch
+ directional flow break
+ passage through low-density structure
```

---

# 🔬 Reinterpretation of TP / FP / FN

## True Positives

```text
G(x) peaks that coincide with sheet transitions.
```

---

## False Positives

```text
G(x) peaks inside a single sheet.

These indicate local turbulence or instability,
but not a global structural transition.
```

---

## False Negatives

```text
Smooth sheet transitions without strong G(x) peaks.

These indicate that a transition can occur through
an existing gate without producing a large scalar spike.
```

---

# ⚠️ Structural Limitation of G(x)

```text
G(x) is a local scalar instability field.

Transitions are global structural events.
```

Therefore:

```text
G(x) detects instability,
not transitions directly.
```

---

# 🧠 Continuous vs Discrete Structure

## Continuous Layer

```text
G(x), ρ(x), C(x), R(x)
→ local field properties
```

---

## Discrete Layer

```text
Sheets / basins
→ global system structure
```

---

## Connection

```text
Sheets → basins
Switches → transitions
```

---

# 🔬 Required Upgrade — Sheet-Aware Transition Model

To correctly detect transitions, the system requires:

## 1. Sheet Identification

```text
cluster (r, θ) into structural layers
```

---

## 2. Time Mapping

```text
sheet(t)
```

---

## 3. Transition Detection

```text
transition(t) = sheet(t) ≠ sheet(t-1)
```

---

## 4. Gate Validation

```text
transition(t) AND high G(x)
```

---

# 🔥 Resulting Model

```text
Transition =
sheet switch
+ instability signal
```

---

# 🧭 Updated Working Hypothesis

```text
Transitions occur when:

1. the system enters a low-density region
2. local flow coherence weakens
3. the trajectory switches structural sheet
```

---

# 🔥 Final Upgrade Statement

```text
The Gate Operator detects instability fields.

True transitions emerge only when instability interacts
with the underlying sheet / basin structure.
```
---

# 🔬 Experiment 4 — Parameter Sensitivity

## Goal

Test robustness to:

- KDE bandwidth  
- normalization  
- sampling density  

---

# 🔬 Experiment 5 — Synthetic System

## Goal

Validate against known transitions:

- double-well potential  
- bistable dynamics  

---

# 🔬 Experiment 6 — Prediction Capability

## Goal

```text
Does G(x) anticipate transitions earlier than trajectory analysis?
```

---

# 🔬 Experiment 7 — Noise Robustness

## Goal

Test stability under:

$$
\dot{x} = F(x) + \sigma \eta
$$

---

# 🔬 Experiment 8 — High-Dimensional Systems

## Goal

Evaluate:

```text
Does the Gate Operator scale?
```

---

# 📊 Evaluation Criteria

## 1. Alignment

```text
Does G(x) match transitions?
```

## 2. Stability

```text
Is G(x) robust?
```

## 3. Generality

```text
Does it work across systems?
```

## 4. Structural Validity

```text
Is the underlying phase space sufficiently dimensional?
```

---

# ⚠️ Known Risks

- KDE artifacts  
- projection errors  
- false gates in low-density regions  
- dimensional collapse  

---

# 🧠 Updated Working Hypothesis

```text
Transitions occur in regions of simultaneous
density loss, coherence loss, and rotational breakdown,
but only in sufficiently volumetric phase spaces.
```

---

# 🚀 Success Criteria

```text
• works in volumetric systems  
• fails predictably in degenerate systems  
• reveals structural transition regions  
```

---

# 🧠 Notes

Key new concept:

```text
"Measurement strip vs full field"
```

This distinction is critical for interpreting results.

---

**NEXAH — Gate Operator Experiments**  
Thomas K. R. Hofmann · 2026
