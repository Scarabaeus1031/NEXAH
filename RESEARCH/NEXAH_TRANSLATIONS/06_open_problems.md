# 🧠 NEXAH — Open Problems & Research Directions

## 🧭 Purpose

This document outlines **open questions, limitations, and research directions**  
for the NEXAH framework.

It serves to:

- clarify current limitations  
- identify missing formalization  
- guide future development  

---

# 🔬 1. Formal Definition of Coherence

Current definition:

```text
C(x) ≈ alignment between flow and structure
```

Problem:

- not uniquely defined  
- depends on approximation  

---

## Open Question

$$
\text{How can coherence } C(x) \text{ be rigorously defined?}
$$

---

# 🔬 2. Mathematical Properties of the Gate Operator

Definition:

$$
G(x) = (1 - \hat{\rho})(1 - \hat{C})(1 - \hat{R})
$$

---

## Open Questions

- continuity and differentiability of $G(x)$  
- sensitivity to normalization  
- invariance under coordinate transformations  

---

# 🔬 3. Relation to Lyapunov Stability

Current interpretation:

```text
low G(x) → stable region
```

---

## Open Question

$$
\text{Is there a formal relation between } G(x) \text{ and Lyapunov functions?}
$$

---

# 🔬 4. Connection to Invariant Manifolds

Observed:

```text
density ridges resemble manifolds
```

---

## Open Questions

- Are ridges approximations of invariant manifolds?  
- Can they be formally linked to stable/unstable manifolds?  

---

# 🔬 5. High-Dimensional Scaling

Current limitation:

- KDE does not scale well  

---

## Open Questions

- Can $\rho(x)$ be replaced by learned density models?  
- How does structure behave in high-dimensional systems?  

---

# 🔬 6. Probabilistic Interpretation

Observation:

```text
G(x) behaves like transition likelihood
```

---

## Open Question

$$
\text{Can } G(x) \text{ be interpreted as a probability density or hazard function?}
$$

---

# 🔬 7. Relation to Control Theory

Current approach:

```text
geometry-based feedback
```

---

## Open Questions

- stability guarantees under NEXAH control  
- relation to optimal control  
- compatibility with MPC  

---

# 🔬 8. Learning the Field

Current:

```text
field derived from trajectories
```

---

## Open Questions

- can $G(x)$ be learned via neural networks?  
- can structure be inferred without full trajectory data?  

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
- extension to continuous fields (PDEs)  

---

# 🔬 10. Janus Field Formalization

Current:

```text
F_J(x) = F_forward + F_backward
```

---

## Open Questions

- how to define backward flow rigorously  
- relation to reversible dynamics  
- connection to time-symmetric formulations  

---

# 🧠 Summary

NEXAH currently provides:

```text
• strong empirical observations  
• consistent geometric interpretation  
• promising control framework  
```

But lacks:

```text
• formal proofs  
• theoretical grounding  
• scalability guarantees  
```

---

# 🚀 Research Direction

Future work should focus on:

```text
1. Formalization
2. Validation
3. Integration with existing theory
```

---

# 🧠 Final Statement

```text
NEXAH is not a finished theory.

It is a structured hypothesis about how geometry governs dynamics.
```

---

**NEXAH — Open Problems**  
Thomas K. R. Hofmann · 2026
