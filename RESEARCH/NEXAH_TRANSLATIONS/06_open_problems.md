# 🧠 NEXAH — Open Problems & Research Directions

## 🧭 Purpose

This document outlines **open questions, limitations, and research directions**  
for the NEXAH framework.

It serves to:

- clarify current limitations  
- identify missing formalization  
- guide future development  

All questions arise from the structural framework and empirical results shown in:

- Fig.1 — Structural Framework  
- Fig.2 — Data-driven Extraction  
- Fig.3 — Quantitative Characterization  

---

# 🔷 Context: What is already established

From the current framework:

- structure can be extracted from trajectories  
- sheets define coherent motion regions  
- gates emerge at low-density, low-coherence regions  
- transitions are structured and non-random  
- phase mismatch activates transitions  

---

# 🔬 1. Formal Definition of Coherence

Current interpretation:

C(x) ≈ alignment between flow and structure

Problem:

- not uniquely defined  
- depends on approximation and representation  

---

## Open Question

How can coherence C(x) be rigorously defined  
in a coordinate-independent and stable way?

---

# 🔬 2. Mathematical Properties of the Gate Operator

Current interpretation:

G(x) ∝ low density × low coherence × low residence

---

## Open Questions

- continuity and differentiability of G(x)  
- sensitivity to normalization and scaling  
- invariance under coordinate transformations  
- relation to geometric singularities  

---

# 🔬 3. Relation to Lyapunov Stability

Observed:

low G(x) corresponds to stable regions

---

## Open Question

Is there a formal relationship between G(x)  
and Lyapunov functions or stability certificates?

---

# 🔬 4. Connection to Invariant Manifolds

Observed:

density ridges resemble structured manifolds

---

## Open Questions

- Are density ridges approximations of invariant manifolds?  
- Can sheet structures be formally linked to stable/unstable manifolds?  
- Do sheets define a generalized foliation of phase space?  

---

# 🔬 5. High-Dimensional Scaling

Current limitation:

density estimation (KDE) does not scale well

---

## Open Questions

- Can ρ(x) be replaced by learned density models?  
- Can sheets be extracted in latent spaces?  
- How stable are sheet structures under dimensionality reduction?  

---

# 🔬 6. Probabilistic Interpretation of Transitions

Observed:

G(x) behaves like transition likelihood

---

## Open Question

Can G(x) or derived quantities be interpreted as:

- transition probability  
- hazard rate  
- stochastic switching kernel  

---

# 🔬 7. Relation to Control Theory

Current approach:

geometry-based, phase-aligned control

---

## Open Questions

- stability guarantees under NEXAH control  
- relation to optimal control formulations  
- compatibility with MPC and feedback linearization  
- controllability of sheet transitions  

---

# 🔬 8. Learning the Field

Current:

field is reconstructed from trajectory data

---

## Open Questions

- can G(x) be learned via neural networks?  
- can structure be inferred from partial observations?  
- can dynamics → structure mapping be learned directly?  

---

# 🔬 9. Physical Interpretation

Current:

geometric interpretation of dynamics

---

## Open Questions

- relation to energy landscapes  
- compatibility with conservation laws  
- extension to continuous systems (PDEs)  
- relation to transport phenomena  

---

# 🔬 10. Bidirectional / Janus Field Formalization

Current idea:

F_J(x) = F_forward + F_backward

---

## Open Questions

- how to define backward flow rigorously  
- relation to reversible dynamics  
- connection to time-symmetric formulations  
- link to Koopman or Perron–Frobenius operators  

---

# 🔬 11. Temporal Structure of Transitions

From Fig.3:

- transitions are temporally clustered  
- switching is not uniform  

---

## Open Questions

- what governs switching density κ(t)?  
- are there universal scaling laws?  
- can transition timing be predicted from structure?  

---

# 🔬 12. Coherence, Gradient and Gate Separation

Current interpretation:

C(x) measures local coherence or alignment between motion and structure.

ρ(x) measures where the system tends to reside.

∇ρ(x) measures the local density gradient and may reveal ridges, slopes, apertures or gate candidates.

G(x) measures transition susceptibility and should not be identified with C(x) or ∇ρ(x) alone.

---

## Working Distinction

C(x): coherence / alignment  
ρ(x): density / occupancy  
R(x): residence / persistence  
∇ρ(x): density gradient / structural slope  
G(x): gate score / structural weakness  

---

## Open Question

Can the gate score be defined as a principled combination of:

low density,  
low coherence,  
low residence time,  
and high local structural contrast?

---

## Candidate Form

G(x) ∝ Wρ(x) · WC(x) · WR(x) · W∇(x)

where:

Wρ(x) increases when density is low  
WC(x) increases when coherence is low  
WR(x) increases when residence time is low  
W∇(x) increases near strong structural gradients or boundary regions  

---

## Interpretation

G(x) is not an inverted coherence field.

Rather, it is a compound indicator of structural weakness.

Coherence describes where motion remains aligned.  
Gate score describes where aligned structure becomes permeable.

---

## GH / Measurement Axis Hypothesis

The GH resonance bar / trajectory sled is currently interpreted as a conceptual measurement axis across structural layers.

Possible interpretation:

GH samples how transitions move across density, coherence and response gradients.

This remains hypothetical and requires formal validation.

---

## Research Direction

Future work should test whether gate events correlate more strongly with:

- low C(x) alone  
- low ρ(x) alone  
- high |∇ρ(x)| alone  
- or a combined gate score G(x)

This comparison is necessary before assigning mathematical status to GH, G(x), or the density-gradient field.

---

# 🧠 Summary

NEXAH currently provides:

• strong empirical observations  
• consistent geometric interpretation  
• structured transition model  
• initial control framework  

But lacks:

• formal proofs  
• theoretical grounding  
• scalability guarantees  
• probabilistic formalization  

---

# 🚀 Research Direction

Future work should focus on:

1. Formalization  
2. Quantitative validation  
3. Integration with existing theory  
4. Scaling to high-dimensional systems  
5. Control guarantees  

---

# 🧠 Final Statement

NEXAH is not a finished theory.

It is a structured hypothesis that:

geometry extracted from dynamics  
governs transitions and emergent topology.

---

NEXAH — Open Problems  
Thomas K. R. Hofmann · 2026
