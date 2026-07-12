# Winding & Topology

## Definition

Given the unwrapped phase θ_unwrapped(t), we define the winding number:

w(t) = θ_unwrapped(t) / (2π)

This quantity measures the accumulated phase rotation over time.

---

## Interpretation of Winding

- w(t) increases (or decreases) continuously as phase evolves  
- each increment of 1 corresponds to one full rotation (2π)  
- the sign of w(t) encodes direction of rotation  

Thus, winding represents a **global accumulation of local phase dynamics**.

---

## Measurement

1. Compute phase:

θ(t) = atan2(y(t), x(t))

2. Unwrap phase:

θ_unwrapped(t) = unwrap(θ(t))

3. Compute winding:

w(t) = θ_unwrapped(t) / (2π)

---

## Observations

Across all analyzed systems:

- w(t) exhibits approximately linear growth over time  
- fluctuations in Δθ(t) accumulate into smooth global behavior  
- direction of winding is consistent with phase drift (μ_Δθ)  
- winding persists even in chaotic systems  

---

## Relation to Phase Drift

Local:
Δθ(t) → instantaneous phase increment  

Global:
w(t) → accumulated phase behavior  

Connection:

μ_Δθ ≠ 0  ⇒  w(t) grows linearly  

Thus:

phase drift induces winding.

---

## Topological Interpretation

Winding provides a **candidate topological signature of the projected trajectory**:

- persistent winding → cyclic / rotational structure  
- stable direction → global asymmetry  
- accumulation → long-term coherence  

Importantly:

The observed winding is induced by the chosen phase projection and accumulated
local motion. Additional analysis is required before inferring the topology of
the full state space.

---

## Key Result

Winding transforms local phase dynamics into a global structural observable.

It encodes:

→ global rotation  
→ accumulated transport  
→ candidate global structural signature

---

## Approximate Relation: Drift → Winding

Under the assumption of approximately stationary phase increments:

μ_Δθ = E[Δθ(t)] ≈ const

the winding number evolves approximately as:

w(t) ≈ (μ_Δθ / 2π) · t

---

## Interpretation

This relation shows that:

- local phase drift accumulates linearly over time  
- the slope of w(t) is directly determined by μ_Δθ  
- global topology (winding) is induced by local asymmetry  

---

## Implication

Under the stated stationarity approximation, statistical properties of Δθ
determine the large-scale behavior of this winding observable.

Thus:

local projected asymmetry ⇒ accumulated winding structure
