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

# 🔬 Experiment 3.4 — Sheet-Aware Gate Operator

## Goal

```text
Integrate structural information (sheets / basins)
with the Gate Operator to improve transition detection.
```

---

## Motivation

Previous experiments show:

```text
• G(x) detects instability
• but fails to reliably detect transitions
```

Root cause:

```text
Transitions are structural (sheet switching),
not purely local (scalar peaks).
```

---

## Core Idea

Instead of:

```text
Transition ≈ G(x)
```

we define:

```text
Transition ≈ Sheet Switch + Gate Activation
```

---

## Formal Model

Let:

- $s(t)$ = sheet index at time $t$
- $G(x_t)$ = Gate Operator

Define transition event:

$$
T(t) = \mathbf{1}[s(t) \neq s(t-1)]
$$

---

## Sheet-Aware Gate Condition

We define:

$$
T_{\text{gate}}(t) =
\mathbf{1}[s(t) \neq s(t-1)] \cdot \mathbf{1}[G(x_t) > \tau]
$$

---

## Interpretation

```text
A transition occurs only when:

1. the system switches structural layer
2. AND passes through a high-instability region
```

---

# 🔬 Method

## Step 1 — Sheet Identification

```text
Cluster trajectory into sheets (e.g. via r or phase)
```

Example:

```text
s(t) ∈ {0,1,2,3,4,5}
```

---

## Step 2 — Sheet Transition Detection

```text
transition(t) = s(t) ≠ s(t-1)
```

---

## Step 3 — Gate Filtering

```text
keep only transitions where G(x) > threshold
```

---

## Step 4 — Evaluation

Compare:

```text
• raw G(x) peaks
• sheet transitions
• sheet-aware gated transitions
```

---

# 🔬 Expected Behavior

## Before (Experiment 3.3)

```text
• many false positives
• many missed transitions
```

---

## After (Sheet-Aware)

```text
• false positives reduced
• recall increases
• transitions align with structure
```

---

# 🔬 Result (Observed Pattern)

Empirically:

```text
• G(x) peaks occur before transitions
• transitions occur during relaxation phase
• sheet switching captures actual transition moment
```

---

# 🔥 Key Insight

```text
G(x) ≠ Transition

G(x) = Pre-transition instability field
```

and

```text
Transition = structural reconfiguration (sheet switch)
```

---

# 🧠 Combined Model

```text
Instability builds → G(x) rises
→ system destabilizes
→ sheet switch occurs
→ system relaxes into new structure
```

---

# 🔬 Structural Interpretation

The system is best described as:

```text
continuous field + discrete switching system
```

---

## Continuous Layer

```text
G(x), ρ(x), C(x), R(x)
→ instability dynamics
```

---

## Discrete Layer

```text
s(t)
→ structural regime
```

---

## Hybrid Model

```text
(s(t), x(t)) defines system state
```

---

# 🔬 Transition Matrix Extension

Using sheet-aware transitions:

$$
P(i \rightarrow j) =
\mathbb{P}(s(t)=j \mid s(t-1)=i, G(x_t) > \tau)
$$

---

## Insight

```text
Transition probabilities become conditional on instability.
```

---

# 🚀 Implication

```text
We move from:

signal-based detection

to:

structure-aware transition modeling
```

---

# 🔥 Final Statement

```text
The Gate Operator identifies where instability exists.

The sheet structure determines when a transition actually occurs.

Only their combination yields a valid transition model.
```

---

# 🔬 Experiment 3.5 — Transition Matrix (Sheet Dynamics)

## Goal

```text
Extract the discrete transition structure of the system
independent of the Gate Operator.
```

---

## Method

1. Discretize trajectory into sheets:

```text
s(t) ∈ {0,1,...,N}
```

2. Build transition counts:

$$
T(i,j) = \#\{t \mid s(t-1)=i, s(t)=j\}
$$

3. Normalize:

$$
P(i \rightarrow j) = \frac{T(i,j)}{\sum_k T(i,k)}
$$

---

## Result (Observed)

- Strong diagonal dominance:

```text
P(i → i) ≫ P(i → j)
```

- Local transitions only:

```text
|i - j| ≈ 1
```

- No long-range jumps

---

## 🔥 Structural Insight

```text
The system behaves as a banded Markov process.
```

More precisely:

```text
• sheets form ordered structure
• transitions occur locally
• system exhibits directional drift
```

---

## Key Observation

Example:

```text
P(5 → 6) ≈ 0.033
P(5 → 5) ≈ 0.766
P(5 → 4) ≈ 0.2
```

Interpretation:

```text
• system prefers to stay
• occasionally moves backward
• rarely moves forward
```

---

## 🔥 Interpretation

```text
Transitions are NOT random.

They follow constrained local geometry.
```

---

## 🧠 Conclusion

```text
The system already encodes transition structure
independently of G(x).
```

---

## Visual

```text
output_results/experiment_3_5_transition_matrix.png
```

---

# 🔬 Experiment 3.6 — Gate Field from Transition Matrix

## Goal

```text
Derive gate structure purely from transition probabilities.
```

---

## Method

Define gate strength:

$$
G_{ij} = -\log(P(i \rightarrow j))
$$

---

## Interpretation

```text
• high probability → low gate
• low probability → strong gate
```

---

## Result (Observed)

```text
Detected gate edges: 0
Gate events in time: 0
```

---

## 🔥 Critical Insight

```text
The system contains almost no "rare" transitions.
```

Meaning:

```text
• transitions are smooth
• transitions are distributed
• transitions are NOT sparse events
```

---

## Structural Consequence

```text
Halvorsen / Lorenz-type systems do NOT have sharp gates.
```

Instead:

```text
they exhibit continuous transition corridors
```

---

## Visual Interpretation

### Gate Strength Matrix

```text
• strong diagonal symmetry
• banded structure
• no isolated spikes
```

---

### Time Series

```text
sheet switching occurs continuously
→ no discrete gate events
```

---

## 🔥 Final Insight

```text
Gate ≠ rare event

Gate = distributed transition region
```

---

## 🧠 Revised Definition

```text
A gate is not a point or spike.

A gate is a region of structured transition probability.
```

---

## 🔥 Consequence for G(x)

```text
G(x) tries to detect "events"

but the system exhibits "fields"
```

---

## 🧠 Final Model Upgrade

```text
Transition =
movement along structured probability manifold
```

NOT:

```text
threshold crossing
```

---

## Visuals

```text
output_results/experiment_3_6_gate_matrix.png
output_results/experiment_3_6_gate_events.png
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
