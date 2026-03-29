# NEXAH Framework — META Layer: Definitions

This document defines the **core formal objects** of the NEXAH Framework.

The purpose of this layer is to establish a **minimal, consistent vocabulary** for describing systems before any simulation, analysis, or navigation is performed.

---

## 1. System

A **system** is defined as a set of entities and relations:

S = (E, R)

where:
- E is a set of entities
- R is a set of relations between entities

The system is fully described by its relational structure.

---

## 2. State

A **state** is a complete configuration of all system variables at a given time:

x ∈ X

where:
- X is the state space of the system

A state captures the current condition of the system.

---

## 3. State Space

The **state space** X is the set of all possible states of the system.

X defines the domain over which system dynamics occur.

---

## 4. Transition

A **transition** is a mapping between states:

T: X → X

A transition describes how the system evolves from one state to another.

---

## 5. Trajectory

A **trajectory** is a sequence of states connected by transitions:

τ = (x₀, x₁, ..., xₙ)

Trajectories represent the temporal evolution of the system.

---

## 6. Transition Structure

The **transition structure** is the set of all observed or possible transitions between states.

It can be represented as a directed graph:

G = (X, T)

where:
- nodes are states
- edges are transitions

---

## 7. Regime

A **regime** is a subset of the state space characterized by consistent transition behavior.

Formally:

Rᵢ ⊂ X

A regime represents a region where the system behaves in a structurally similar way.

---

## 8. Attractor

An **attractor** is a state or set of states toward which trajectories converge.

Formally:

x* is an attractor if trajectories entering its neighborhood remain close or converge to it.

---

## 9. Basin of Attraction

The **basin of attraction** of an attractor is the set of all states that lead to that attractor under system transitions.

---

## 10. Collapse

A **collapse** is a transition into a regime where the system loses functionality, stability, or viability.

Collapse is defined relative to system objectives or constraints.

---

## 11. Stability

A **stable state or regime** is one in which small perturbations do not lead to large deviations in system behavior.

---

## 12. Instability

An **unstable state or regime** is one in which small perturbations lead to significant changes in system trajectories.

---

## 13. Risk

**Risk** is defined as the likelihood or proximity of a state transitioning into a collapse regime.

Risk is not intrinsic to a state but emerges from its position within the transition structure.

---

## 14. Distance to Collapse

The **distance to collapse** is a measure of how far a state is from entering a collapse regime.

This can be defined in terms of:
- transition steps
- probability of collapse
- structural proximity in the regime graph

---

## 15. Navigation

**Navigation** is the process of selecting transitions to guide the system through the state space toward desired regimes while avoiding collapse.

---

## 16. Policy

A **policy** is a rule or function that determines which transitions should be taken from a given state:

π: X → T

---

## 17. Action

An **action** is an intervention that influences or overrides the natural transition of the system.

---

## 18. Field (NEXAH Definition)

The **NEXAH Field** is a composite structure defined over the state space that integrates:

- transition dynamics  
- regime structure  
- stability and risk geometry  
- admissible navigation policies  

Formally:

F_NEXAH: X → (Φ(x), R(x), Π(x))

where:
- Φ(x) represents local transition dynamics  
- R(x) represents risk and stability measures  
- Π(x) represents admissible navigation policies  

---

## 19. Key Insight

Systems are not only defined by trajectories,  
but by the structure of transitions that enables navigation across regimes.

---

## Summary

These definitions form the minimal formal foundation of the NEXAH Framework.

All higher-level layers (ARCHY, MESO, NEXAH, MEVA) operate on top of these objects.
