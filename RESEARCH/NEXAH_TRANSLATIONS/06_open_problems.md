# 🧠 NEXAH — Open Problems & Research Directions

## 🧭 Purpose

This document outlines **open questions, limitations, and research directions**  
for the NEXAH framework.

It serves to:

- clarify current limitations  
- identify missing formalization  
- guide future development  

All questions arise from the structural framework and empirical results of the NEXAH research layer.

---

# 🔷 Context: What is already established

From the current framework:

- structure can be extracted from trajectories  
- coherent regions (regimes) can be identified  
- transition regions emerge at low-density / low-coherence zones  
- transitions are structured and non-random  
- phase mismatch correlates with transition activation  

---

# 🔬 1. Formal Definition of Coherence

Current interpretation:

```text
C(x) ≈ alignment between motion and local flow structure
```

Problem:

- not uniquely defined  
- depends on representation and projection  

---

## Open Question

How can coherence $begin:math:text$ C\(x\) $end:math:text$ be defined:

- in a coordinate-independent way  
- robust under noise  
- stable across systems  

---

# 🔬 2. Mathematical Properties of the Gate Function

Current interpretation:

```text
G(x) ∝ low density × low coherence × low residence
```

---

## Open Questions

- continuity and differentiability of $begin:math:text$ G\(x\) $end:math:text$  
- sensitivity to normalization  
- invariance under coordinate transformations  
- relation to geometric singularities or separatrices  

---

# 🔬 3. Relation to Lyapunov Stability

Observed:

```text
low G(x) ↔ stable regions
```

---

## Open Question

Is there a formal relation between:

- $begin:math:text$ G\(x\) $end:math:text$ and Lyapunov functions  
- or other stability certificates?  

---

# 🔬 4. Connection to Invariant Structures

Observed:

```text
density ridges resemble structured manifolds
```

---

## Open Questions

- Are density ridges approximations of invariant manifolds?  
- Can sheet structures be linked to stable/unstable manifolds?  
- Do sheets define a generalized foliation of phase space?  

---

# 🔬 5. High-Dimensional Scaling

Current limitation:

```text
density estimation (KDE) does not scale well
```

---

## Open Questions

- Can $begin:math:text$ \\rho\(x\) $end:math:text$ be replaced by learned density models?  
- Can structure be extracted in latent spaces?  
- How stable are structural features under dimensionality reduction?  

---

# 🔬 6. Probabilistic Interpretation

Observed:

```text
G(x) behaves like transition likelihood
```

---

## Open Question

Can structural quantities be interpreted as:

- transition probabilities  
- hazard rates  
- stochastic switching kernels?  

---

# 🔬 7. Relation to Control Theory

Current approach:

```text
geometry-based, phase-aligned control
```

---

## Open Questions

- stability guarantees under NEXAH control  
- relation to optimal control  
- compatibility with MPC  
- controllability of transitions between regimes  

---

# 🔬 8. Learning the Field

Current:

```text
structure is reconstructed from trajectories
```

---

## Open Questions

- can $begin:math:text$ G\(x\) $end:math:text$ be learned directly (e.g. neural fields)?  
- can structure be inferred from partial observations?  
- can dynamics → structure mapping be learned end-to-end?  

---

# 🔬 9. Physical Interpretation

Current:

```text
geometric interpretation of dynamics
```

---

## Open Questions

- relation to energy landscapes  
- compatibility with conservation laws  
- extension to PDE systems  
- relation to transport phenomena  

---

# 🔬 10. Bidirectional / Janus Field

Concept:

```text
F_J(x) = F_forward + F_backward
```

---

## Open Questions

- how to define backward flow rigorously  
- relation to reversible systems  
- connection to Koopman / Perron–Frobenius operators  

---

# 🔬 11. Temporal Structure of Transitions

Observed:

- transitions are temporally clustered  
- switching is non-uniform  

---

## Open Questions

- what governs transition intensity $begin:math:text$ \\kappa\(t\) $end:math:text$?  
- are there scaling laws?  
- can transition timing be predicted from structure?  

---

# 🔬 12. Structural Quantity Separation

Current quantities:

```text
ρ(x) → density / occupancy  
C(x) → coherence / alignment  
∇ρ(x) → structural gradient  
G(x) → transition susceptibility
```

---

## Core Problem

These quantities are:

- empirically meaningful  
- but not yet formally unified  

---

## Open Question

Can $begin:math:text$ G\(x\) $end:math:text$ be defined as a principled function of:

- density  
- coherence  
- residence time  
- structural gradients  

---

## Candidate Form

$$
G(x) \propto W_\rho(x)\, W_C(x)\, W_R(x)\, W_{\nabla}(x)
$$

---

## Interpretation

```text
C(x): describes aligned motion

G(x): describes structural breakdown
```

Important:

```text
G(x) is NOT an inverse of C(x)
```

---

## Research Direction

Compare predictive power of:

- density-only  
- coherence-only  
- gradient-only  
- combined gate score  

---

# 🔬 13. Measurement Axis / GH Hypothesis (Exploratory)

A conceptual measurement axis (e.g. "trajectory sled")  
has been used to probe transitions across structural layers.

---

## Status

```text
exploratory / not formalized
```

---

## Open Question

Can transition behavior be consistently measured along a  
low-dimensional projection that captures:

- density variation  
- coherence breakdown  
- transition activation  

---

## Requirement

This concept requires:

- formal definition  
- reproducibility  
- independence from visualization choices  

---

# 🧠 Summary

NEXAH currently provides:

- strong empirical observations  
- consistent geometric interpretation  
- structured transition model  
- initial control framework  

But lacks:

- formal proofs  
- theoretical grounding  
- scalability guarantees  
- probabilistic formalization  

---

# 🚀 Research Direction

Future work should focus on:

1. Formalization  
2. Quantitative validation  
3. Integration with existing theory  
4. High-dimensional scaling  
5. Control guarantees  

---

# 🧠 Final Statement

```text
NEXAH is not a finished theory.

It is a structured hypothesis that:

geometry extracted from dynamics  
governs transitions and emergent topology.
```

---

**NEXAH — Open Problems**  
Thomas K. R. Hofmann · 2026
