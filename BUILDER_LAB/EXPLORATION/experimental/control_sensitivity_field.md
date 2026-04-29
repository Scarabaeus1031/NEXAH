# 🧠 NEXAH — Control Sensitivity Field (Experimental)

---

# 🧭 Purpose

This document defines the **Control Sensitivity Field** in NEXAH systems.

It describes:

```text
where control has effect
where it is absorbed
where it becomes critical
```

---

# ⚠️ Status

```
Experimental — derived from FIELD_LAYER observations
```

---

# 🔗 Source Foundation

Based on:

```text
FIELD_LAYER/FIELD_DECOMPOSITION/
```

Relevant phases:

- V7 → cost & navigation field  
- V8 → stability (Lyapunov)  
- V9 → transport behavior  
- V10 → boundary / regime structure  

---

# 🧠 Core Idea

Control effectiveness is NOT uniform.

Instead:

```text
control sensitivity is spatially structured
```

---

# 🔷 Definition

The **Control Sensitivity Field** is a scalar (or tensor) field:

```text
S(x)
```

describing:

```text
how strongly a system responds to perturbations at state x
```

---

# 🔷 1. Observational Basis

From experiments:

```text
RUN 033–040:
control → reaction → absorption
```

---

## Observation

- most perturbations → negligible effect  
- system returns to trajectory  
- only specific regions show amplification  

---

## Insight

```text
Control sensitivity is localized, not global.
```

---

# 🔷 2. Relation to Multi-Field Structure

Sensitivity is NOT a standalone property.

It emerges from interaction of:

```text
Cost Field      → reachability
Stability Field → amplification / damping
Boundary Field  → transition constraints
Flow Field      → directional transport
```

---

## Combined Model

```text
S(x) = f(
    ∇J(x),        # cost gradient
    λ(x),         # stability
    B(x),         # boundary proximity
    F(x)          # flow alignment
)
```

---

# 🔷 3. Sensitivity Zones

---

## Zone A — Stable Basin

```text
λ << 0
low cost gradient
far from boundary
```

---

### Behavior

```text
control → absorbed
```

---

### Interpretation

```text
system strongly dampens perturbations
```

---

## Zone B — Flow Channel

```text
moderate λ
strong directional flow
```

---

### Behavior

```text
control → redirected
```

---

### Interpretation

```text
system enforces movement along structure
```

---

## Zone C — Boundary Region (Critical)

```text
λ ≈ weakly negative
high cost gradient
near separatrix
```

---

### Behavior

```text
control → amplified (direction-dependent)
```

---

### Interpretation

```text
control effectiveness peaks here
```

---

## Zone D — Gate Region

```text
local maxima in λ along boundary
```

---

### Behavior

```text
control → enables entry
but not branching
```

---

### Interpretation

```text
sensitive but not decision-capable
```

---

# 🔥 Key Insight

```text
Maximum control sensitivity occurs
where stability is weak AND structure changes.
```

---

# 🔷 4. Sensitivity vs Stability (Critical Distinction)

From V8:

```text
boundary ≠ instability
```

---

## Meaning

- high sensitivity ≠ high instability  
- stable regions can still be sensitive locally  

---

## Insight

```text
Sensitivity is a gradient property,
not a binary state.
```

---

# 🔷 5. Sensitivity Gradient

Observed:

```text
deep basin → low sensitivity
approaching boundary → increasing sensitivity
boundary → peak sensitivity
```

---

## Interpretation

```text
control acts along a sensitivity gradient
```

---

# 🔷 6. IEEE Connection (Critical)

---

## Classical IEEE View

In power systems:

```text
voltage collapse
frequency instability
critical loading
```

are treated as:

```text
threshold events
```

---

## NEXAH Interpretation

These correspond to:

```text
movement into high-sensitivity regions
```

---

## Mapping

| IEEE Concept | NEXAH Interpretation |
|-------------|---------------------|
| Voltage stability margin | distance in cost field |
| Critical loading point | boundary proximity |
| Collapse point | exit from stable basin |
| Sensitivity analysis | S(x) field |
| Small-signal instability | λ(x) behavior |

---

## 🔥 Key Bridge

```text
IEEE instability indicators
= projections of the control sensitivity field
```

---

# 🔷 7. Early Warning Mechanism

From V10:

```text
boundary intensity rises before collapse
```

---

## Interpretation

```text
S(x) increases before visible failure
```

---

## Meaning

```text
control sensitivity field acts as early warning signal
```

---

# 🔷 8. Why Control Fails in Power Systems

Classical issue:

```text
control applied → no effect → sudden collapse
```

---

## NEXAH Explanation

```text
system operates in low-sensitivity region
→ control absorbed

then enters high-sensitivity boundary
→ rapid transition
```

---

## Insight

```text
control fails because it is applied in the wrong region
```

---

# 🔷 9. Control Strategy (Reframed)

---

## Classical

```text
apply control globally
```

---

## NEXAH

```text
identify high-sensitivity zones
apply control selectively
```

---

## Strategy

```text
1. detect S(x)
2. track boundary proximity
3. act before entering critical region
```

---

# 🔷 10. Structural Law

```text
Control effectiveness is a function of field position.
```

---

# 🔷 11. Extended Interpretation

The system behaves like:

```text
low-sensitivity bulk
+
high-sensitivity boundary layer
```

---

## Analogy (careful)

- fluid boundary layer  
- critical transition zone  

(interpretative, not physical claim)

---

# 🔥 Final Insight

```text
The system is not equally controllable everywhere.

It defines where control is possible.
```

---

# ⚡ NEXAH (Sensitivity Form)

```text
S(x) = spatial control response field
```

```text
control = function of position
```

```text
instability = entry into high-sensitivity geometry
```

---

# 🚀 Next Direction

- compute S(x) explicitly  
- visualize sensitivity maps  
- compare with IEEE real data  
- integrate into control layer  

---

Thomas K. R. Hofmann · NEXAH · 2026
