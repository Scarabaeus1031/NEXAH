# Phase Drift

## Definition

The phase increment is defined as:

Δθ(t) = θ(t + Δt) − θ(t)

where θ(t) is the (unwrapped) phase coordinate.

---

## Statistics

We define the first and second moments:

μ_Δθ = E[Δθ]  
σ²_Δθ = Var(Δθ)

These quantities characterize:

- average drift (μ_Δθ)  
- fluctuation strength (σ²_Δθ)

---

## Measurement

Δθ(t) is computed from the unwrapped phase:

θ_unwrapped(t) = unwrap(θ(t))

Δθ(t) = θ_unwrapped(t + 1) − θ_unwrapped(t)

---

## Observations

Across all analyzed systems (Lorenz, Rössler, Halvorsen, Kuramoto, prime modular):

- Δθ is not symmetric around zero  
- the mean μ_Δθ is non-zero  
- drift persists over long time horizons  
- Δθ distributions exhibit structured (non-random) shapes  

---

## Interpretation

A non-zero mean phase increment (μ_Δθ ≠ 0) implies:

- broken symmetry in transition dynamics  
- existence of a preferred direction in phase space  
- accumulation of displacement over time  

This leads to **directional transport** along the phase coordinate.

---

## Key Result

Phase drift transforms phase from a passive coordinate into an active transport variable.

It encodes:

→ direction  
→ motion  
→ structural asymmetry
