# 🔁 NEXAH — Transition Structure

## 🧭 Overview

The NEXAH framework separates system behavior into two layers:

```text
1. Continuous field (instability / geometry)
2. Discrete structure (regimes / transitions)
```

This document defines the **discrete transition structure** of dynamical systems.

---

# ⚠️ Conceptual Shift

Classical view:

```text
System = trajectory in state space
```

NEXAH view:

```text
System = structured space being traversed
```

Transitions are not random events, but **structured movements between coherent regions**.

---

# 🧠 Core Definition

Let a trajectory:

$$
x(t) \in \mathbb{R}^n
$$

We define a discrete structural mapping:

$$
s(t) \in \{0,1,\dots,N\}
$$

where:

```text
s(t) = sheet / regime index at time t
```

---

# 🧩 Sheets (Structural Layers)

## Definition

A **sheet** is a locally coherent region of the flow:

$$
\mathcal{S}_i = \{ x \mid x \text{ follows coherent dynamics} \}
$$

---

## Properties

```text
• local stability
• directional coherence
• persistence over time
```

---

## Practical Approximation

Example (used in experiments):

```text
s(t) = binning of radius r = √(x² + y²)
```

---

# 🔁 Transition Definition

A transition occurs when:

$$
T(t) = \mathbf{1}[s(t) \neq s(t-1)]
$$

---

## Interpretation

```text
Transition = change of structural layer
```

NOT:

```text
peak in signal
```

---

# 🔬 Transition Matrix

## Definition

We define transition counts:

$$
T(i,j) = \#\{t \mid s(t-1)=i, s(t)=j\}
$$

---

## Normalized Form

$$
P(i \rightarrow j) =
\frac{T(i,j)}{\sum_k T(i,k)}
$$

---

## Observed Structure

Empirically:

```text
• strong diagonal dominance
• local transitions only
• banded matrix structure
```

---

## Example

```text
P(5 → 5) ≈ 0.77   (stay)
P(5 → 4) ≈ 0.20   (backward)
P(5 → 6) ≈ 0.03   (forward)
```

---

## 🔥 Key Insight

```text
Transitions are local and constrained.

The system moves along a structured adjacency graph.
```

---

# 🧠 Structural Model

The system behaves as:

```text
a banded Markov process with geometric origin
```

More precisely:

```text
• states are ordered (sheets)
• transitions occur between neighbors
• global jumps are absent
```

---

# 🔁 Transition Geometry

We interpret the transition matrix as:

```text
a discrete projection of an underlying flow manifold
```

---

## Consequence

```text
The system does not jump randomly.

It flows along structured pathways.
```

---

# 🔬 Gate Relation

We define gate strength from transition probabilities:

$$
G_{ij} = -\log(P(i \rightarrow j))
$$

---

## Interpretation

```text
low probability → high resistance → gate-like behavior
```

---

## Observed Result

```text
• no extreme outliers
• no isolated transitions
• no sparse gate events
```

---

## 🔥 Critical Insight

```text
Gates are NOT discrete edges.

They are distributed transition regions.
```

---

# 🧠 Revised Gate Interpretation

Instead of:

```text
gate = rare transition
```

we define:

```text
gate = region of structured transition probability
```

---

# 🔁 Time Series View

Observed:

```text
• continuous sheet switching
• no singular transition spikes
• transitions distributed over time
```

---

## Insight

```text
Transitions are continuous processes,
not discrete impulses.
```

---

# 🧩 Hybrid System Model

The full system is:

```text
STATE = (x(t), s(t))
```

---

## Continuous Layer

```text
x(t)
→ geometry, flow, instability
```

---

## Discrete Layer

```text
s(t)
→ regime / structural position
```

---

## Combined Dynamics

```text
flow moves within sheets
transition moves between sheets
```

---

# 🔥 Final Model

```text
Transition =
movement across structured manifold layers
```

NOT:

```text
threshold crossing
```

---

# 🧭 Role in NEXAH

The transition structure provides:

```text
• regime identification
• connectivity structure
• navigation graph
• control targets
```

---

# 🔗 Relation to Gate Operator

See:

```text
gate_operator.md
```

---

## Key Relationship

```text
G(x) → where instability occurs
s(t) → where the system is structurally
```

---

## Combined Model

```text
Transition =
sheet switch
+ instability interaction
```

---

# ⚠️ Limitations

- sheet definition is approximate  
- clustering method affects structure  
- Markov assumption is local approximation  
- higher-dimensional systems require generalization  

---

# 🚀 Open Questions

- optimal sheet definition (clustering vs geometry)  
- relation to invariant manifolds  
- probabilistic interpretation of transition flow  
- extension to high-dimensional state spaces  

---

# 🧠 Key Insight

```text
The system is not a trajectory.

It is a structured space
being traversed through discrete layers.
```

---

# 🧠 Summary

The Transition Structure provides:

- a discrete representation of system dynamics  
- a structured transition graph  
- a bridge between geometry and control  

---

**NEXAH — Transition Structure**  
Thomas K. R. Hofmann · 2026
