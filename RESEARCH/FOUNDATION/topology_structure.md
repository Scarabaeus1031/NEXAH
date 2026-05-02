# NEXAH — Topology from Structural Connectivity

## 🧭 Purpose

This document defines how topology arises in the NEXAH framework.

Topology is not imposed.

It emerges from:

- sheet structure  
- transition connectivity  
- global motion constraints  

---

# 🔷 Definition (Conceptual)

Let:

- Sᵢ = sheets  
- Pᵢⱼ = transition probability between sheets  

Then:

```text
Topology = structure induced by the connectivity graph over sheets
```

---

# 🔷 Sheet Graph

Define a graph:

- Nodes: sheets Sᵢ  
- Edges: transitions between sheets  

Weighted by:

$$
P_{ij} = P(S_j | S_i)
$$

---

# 🔷 Emergent Topology

Different connectivity structures induce different effective topologies:

| System | Sheet Structure | Emergent Topology |
|------|---------------|------------------|
| Lorenz | two-sheet switching | Möbius-like |
| Rössler | spiral layering | torus / disk-like |
| Halvorsen | fragmented sheets | irregular / mixed |

---

# 🔷 Key Principle

```text
Topology is not a property of space.

It is a property of structured motion.
```

---

# 🔷 Interpretation

- sheets define local structure  
- transitions define connectivity  
- connectivity defines global topology  

---

# 🔷 Mathematical Direction (Open)

Possible formalizations:

- spectral graph theory (Laplacian of sheet graph)  
- persistent homology  
- Koopman-based structure  
- transition operator topology  

---

# 🔷 Relation to NEXAH Pipeline

```text
Flow → Field → Sheets → Transitions → Connectivity → Topology
```

---

# 🔥 Final Insight

```text
Topology emerges from how the system is allowed to move,
not from the space it occupies.
```

---

**Status:** semi-formal / empirically supported / not yet proven
