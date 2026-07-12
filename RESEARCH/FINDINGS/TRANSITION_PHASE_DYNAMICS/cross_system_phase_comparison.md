# Cross-System Phase Comparison

## Systems

The following system classes are analyzed:

- Discrete system:
  - prime modular transitions (pₙ mod m)

- Continuous dynamical systems:
  - Lorenz system
  - Rössler system
  - Halvorsen system

- Coupled oscillator system:
  - Kuramoto model

---

## Phase Construction

For all systems, a phase coordinate θ is defined:

- Continuous systems:
  θ(t) = atan2(y(t), x(t))

- Discrete systems:
  θₙ = mapping of residue rₙ to angular coordinate

- Kuramoto:
  θᵢ(t) are intrinsic oscillator phases

This provides a **common coordinate representation** across system types.

---

## Observed Invariants

Across all analyzed systems, the following properties are consistently observed:

| Property | Observation |
|----------|------------|
| Phase definable | ✔ phase coordinate can be constructed |
| Phase increments Δθ | ✔ computable and structured |
| Non-zero drift μ_Δθ | ✔ directional bias present |
| Winding behavior | ✔ accumulation over time |
| Structure in Δθ distribution | ✔ non-random patterns |

---

## Observations

Empirically:

- phase trajectories can be unwrapped in all systems  
- phase increments Δθ are not symmetric around zero  
- drift persists over long time scales  
- winding emerges from accumulation of Δθ  
- Δθ distributions show structure beyond random noise  

These observations hold despite differences in:

- dimensionality  
- governing equations  
- system type (discrete vs continuous)  

---

## Interpretation

The consistency of these properties suggests:

- phase behavior is not specific to a given system  
- drift reflects asymmetry in transition dynamics  
- winding encodes global structural behavior  

Thus, phase acts as a **unifying coordinate** across systems.

---

## Key Insight

Related phase-derived patterns occur in the tested system representations.
Whether they arise from a shared transition mechanism rather than from the
chosen projections remains open.

---

## Implication

Different systems can be analyzed within a shared framework:

→ phase coordinate  
→ drift statistics  
→ winding behavior  

This enables direct comparison between:

- discrete transition systems  
- continuous dynamical systems  
- coupled oscillator systems  

within a common structural representation.
