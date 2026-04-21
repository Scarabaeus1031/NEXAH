# NEXAH — Mathematical Foundations (Field Decomposition Layer)

## Purpose

This document formalizes the mathematical structure underlying the NEXAH field simulations.

It does NOT introduce new mathematics.

It clarifies:

- which standard concepts are used
- how they are combined
- what is actually computed in the system

---

## Positioning

This work does not introduce new equations.

Instead, it proposes a different perspective:

- dynamics are treated as a field
- trajectories are treated as probes of structure
- cost is constructed from simulated motion
- navigation emerges from this constructed field

The contribution is therefore:

→ not new mathematics,  
→ but a structured way to extract geometry and navigation from known systems

---

## 1. State Space

The system operates on a continuous 2D domain:

\[
x = (x_1, x_2) \in \mathbb{R}^2
\]

---

## 2. Potential Field

A scalar field is defined:

\[
V(x) : \mathbb{R}^2 \to \mathbb{R}
\]

Constructed as a superposition of Gaussian functions.

Interpretation:

- minima → attractor basins  
- maxima → repulsive regions  

---

## 3. Base Dynamics (Gradient Flow)

The fundamental flow is:

\[
\dot{x} = -\nabla V(x)
\]

Meaning:

- trajectories move toward local minima  
- this is a classical gradient descent system  

---

## 4. Rotational Component

A rotational perturbation is added:

\[
F(x) = -\nabla V(x) + R(x)
\]

Where:

- \(R(x)\) is a curl-like component  
- introduces circulation and asymmetry  

Result:

→ trajectories are curved, not purely descending  

---

## 5. Second-Order Dynamics (Optional)

Extended system:

\[
\dot{x} = v
\]
\[
\dot{v} = F(x) - \gamma v
\]

Where:

- \( \gamma > 0 \) is a damping coefficient  

Interpretation:

- inertia + dissipation  
- produces spiral convergence  

---

## 6. Trajectories

Trajectories are solutions of:

\[
x'(t) = F(x(t))
\]

or second-order form.

Important:

→ trajectories are not optimized  
→ they are **integral curves of the field**

---

## 7. Cost Functional (V7 Layer)

A scalar cost is assigned to each initial condition:

\[
J(x_0) = \int_0^T \ell(x(t), v(t)) \, dt
\]

Where:

\[
\ell(x, v) = \|v\| + \alpha \|\dot{v}\|
\]

Components:

- speed term → movement cost  
- turning term → curvature penalty  

Interpretation:

→ measures effort required to reach a target  

---

## 8. Value Field Interpretation

The computed cost map can be interpreted as:

\[
J(x) \approx \text{Value Function}
\]

from optimal control theory.

Meaning:

- each point stores the cost of reaching the target  
- structure emerges from dynamic simulation  

---

## 9. Navigation Field

The navigation field is defined as:

\[
N(x) = -\nabla J(x)
\]

Interpretation:

- direction of steepest cost decrease  
- approximates optimal motion  

Important:

→ this is not analytically solved  
→ it is numerically constructed  

---

## 10. Relation to Optimal Control

The system implicitly approximates:

\[
\min_{x(t)} \int_0^T \ell(x(t), v(t)) dt
\]

This is related to:

- optimal control theory  
- Hamilton–Jacobi–Bellman (HJB) framework  

However:

- no explicit HJB equation is solved  
- solution is obtained via simulation  

---

## 11. Lyapunov Perspective

The potential field \(V(x)\) acts as a Lyapunov candidate:

\[
\dot{V}(x) = \nabla V \cdot \dot{x}
\]

For pure gradient flow:

\[
\dot{V}(x) \le 0
\]

With rotation:

- monotonic decrease is broken locally  
- but global stability persists  

Interpretation:

→ system remains dissipative but not strictly gradient  

---

## 12. Boundary / Splinter Interpretation

Observed transition regions correspond to:

- regions where \(J(x)\) is non-smooth  
- multiple competing trajectories exist  

Interpretation:

\[
\nabla J(x) \text{ is discontinuous or unstable}
\]

These regions behave like:

→ finite-time separatrices  

---

## 13. Sensitivity and Instability

Sensitivity maps approximate:

\[
\frac{\partial x(T)}{\partial x(0)}
\]

Meaning:

- how strongly trajectories diverge  

Interpretation:

→ local instability / transition amplification  

Related to:

- Lyapunov-like behavior (finite-time)

---

## 14. Structural Summary

The system combines:

- gradient descent (energy minimization)  
- rotational dynamics (circulation)  
- dissipation (stability)  
- path-based cost accumulation  

This produces:

- attractor basins  
- orbit-like structures  
- transition corridors  
- energy barriers  

---

## 15. Scope

This framework is:

- numerical  
- exploratory  
- structurally consistent  

It is NOT:

- an analytical solution  
- a physical theory  
- a claim of new mathematics  

---

## 16. Interpretation

The system can be viewed as:

\[
\text{Dynamical System} + \text{Cost Functional} + \text{Navigation Field}
\]

Result:

→ a structured, navigable field representation  

---

---

## Visual Examples

### Navigation Field (Cost Gradient)

![Navigation Field](outputs/v7_3/v7_3_navigation.png)

Shows:

- cost landscape
- navigation field (−∇J)
- resulting trajectories

---

### Reachability / Failure Map

![Failure Map](outputs/v7_4/v7_4_failure_map.png)

Shows:

- regions from which the target is reachable
- sharp transition boundary ("splinter")

---

## Final Remark

All observed structures:

- basins  
- boundaries  
- corridors  
- orbit bands  

emerge from:

> the interaction of simple, standard mathematical components  

No structure is explicitly imposed.
