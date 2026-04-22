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
- stability is measured directly from trajectory divergence  

The contribution is therefore:

→ not new mathematics  
→ but a structured method to extract **geometry, navigation, and stability** from known systems  

---

## 1. State Space

The system operates on a continuous 2D domain:

$$
x = (x_1, x_2) \in \mathbb{R}^2
$$

---

## 2. Potential Field

A scalar field is defined:

$$
V(x) : \mathbb{R}^2 \to \mathbb{R}
$$

Constructed as a superposition of Gaussian functions.

Interpretation:

- minima → attractor basins  
- maxima → repulsive regions  

---

## 3. Base Dynamics (Gradient Flow)

The fundamental flow is:

$$
\dot{x} = -\nabla V(x)
$$

Meaning:

- trajectories move toward local minima  
- this corresponds to a classical gradient descent system  

---

## 4. Rotational Component

A rotational perturbation is added:

$$
F(x) = -\nabla V(x) + R(x)
$$

Where:

- $R(x)$ is a curl-like component  
- introduces circulation and asymmetry  

Result:

→ trajectories are curved, not purely descending  

---

## 5. Second-Order Dynamics (Optional)

Extended system:

$$
\dot{x} = v
$$

$$
\dot{v} = F(x) - \gamma v
$$

Where:

- $\gamma > 0$ is a damping coefficient  

Interpretation:

- inertia + dissipation  
- produces spiral convergence  

---

## 6. Trajectories

Trajectories are solutions of:

$$
\dot{x}(t) = F(x(t))
$$

Important:

→ trajectories are not optimized  
→ they are **integral curves of the field**

---

## 7. Cost Functional (V7 Layer)

A scalar cost is assigned:

$$
J(x_0) = \int_0^T \ell(x(t), v(t)) \, dt
$$

Where:

$$
\ell(x, v) = \|v\| + \alpha \|\dot{v}\|
$$

Interpretation:

- movement cost (speed)  
- curvature cost (direction change)  

→ measures effort required to reach a target  

---

## 8. Value Field Interpretation

$$
J(x) \approx \text{Value Function}
$$

Interpretation:

- each point stores cost-to-go  
- approximates optimal control structure  

Important:

→ computed numerically via simulation  
→ not via HJB solution  

---

## 9. Navigation Field

$$
N(x) = -\nabla J(x)
$$

Interpretation:

- direction of steepest cost decrease  
- induces flow toward target  

→ navigation emerges from field geometry  

---

## 10. Relation to Optimal Control

Implicitly approximates:

$$
\min_{x(t)} \int_0^T \ell(x(t), v(t)) \, dt
$$

Related to:

- optimal control  
- Hamilton–Jacobi–Bellman theory  

But:

→ no PDE is solved  
→ structure is obtained via simulation  

---

## 11. Lyapunov Perspective (V8 Layer)

Finite-time Lyapunov-like quantity:

$$
\lambda(x) = \frac{1}{T} \log \frac{\|\delta x(T)\|}{\|\delta x(0)\|}
$$

Interpretation:

- $\lambda < 0$ → stable (convergence)  
- $\lambda > 0$ → unstable (divergence)  

Key point:

→ stability is **measured**, not assumed  

---

## 12. Boundary vs Stability

Observed:

- transition boundaries (from cost / classification)  
- stability structures (from Lyapunov)  

Result:

→ they do NOT coincide  

Interpretation:

- boundary = outcome transition  
- Lyapunov = local stability  

---

## 13. Boundary / Splinter Interpretation

Transition regions correspond to:

- non-smooth regions of $J(x)$  
- competing trajectories  

$$
\nabla J(x) \ \text{unstable or non-smooth}
$$

Interpretation:

→ finite-time separatrix-like structures  

---

## 14. Sensitivity and Instability

Sensitivity approximates:

$$
\frac{\partial x(T)}{\partial x(0)}
$$

Interpretation:

→ local amplification of perturbations  

Related to:

- finite-time Lyapunov behavior  

---

## 15. Structural Result (V8 Insight)

From experiments:

- gates exist (weak stability regions)  
- but no branching occurs  

Result:

```text
num_decision_points = 0
```
Interpretation:

→ system has transitions  
→ but no true decision nodes  

---

## 16. Structural Summary

The system combines:

- gradient flow (energy minimization)  
- rotational flow (circulation)  
- dissipation (stability)  
- cost accumulation (navigation)  
- Lyapunov estimation (stability geometry)  

This produces:

- attractor basins  
- orbit structures  
- transition corridors  
- energy barriers  
- stability gradients  

---

## 17. System Classification

The system is best described as:

$$
\text{Directed Dynamical System}
$$

Properties:

- constrained flow  
- dominant attractor  
- no multi-branch decision structure  

---

## 18. Scope

This framework is:

- numerical  
- exploratory  
- structurally consistent  

It is NOT:

- a closed-form theory  
- a new physical law  
- a claim of new mathematics  

---

## 19. Interpretation

The system can be summarized as:

$$
\text{Dynamical Field} 
+ \text{Cost Field} 
+ \text{Navigation Field} 
+ \text{Stability Field}
$$

Result:

→ a structured, navigable, stability-aware field representation  

---

## Visual Examples

### Navigation Field

![Navigation Field](outputs/v7_3/v7_3_navigation.png)

---

### Energy / Transition Structure

![Energy Map](outputs/v7_7/v7_7_energy_map.png)

---

### Lyapunov Stability Field

![Lyapunov Map](outputs/v8_0_lyapunov_map/v8_0_lyapunov_map.png)

---

### Injection Behavior

![Injection Tests](outputs/v8_5_injection_tests/v8_5_injection_tests.png)

---

## Final Remark

All observed structures:

- basins  
- boundaries  
- corridors  
- stability regions  

emerge from:

> the interaction of simple, standard mathematical components  

No structure is explicitly imposed.

---

## Final Insight

```text
The system does not offer choices.

It defines paths.
