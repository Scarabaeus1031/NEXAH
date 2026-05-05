# 🌀 NEXAH — Fractal Validation

## 🧭 Purpose

This module validates the NEXAH transition model on **parameter-driven systems**:

- Mandelbrot (parameter space)

- Julia sets (dynamical realization)

---

## 🔬 Core Idea

```text

parameter motion → induces mismatch → triggers transitions

```

---

## 🧠 Role in NEXAH

This module extends validation beyond intrinsic system dynamics:

```text

internal dynamics → transition via mismatch  

parameter dynamics → transition via induced mismatch  

```

---

## 🔁 Key Observation

When moving along a parameter path $begin:math:text$ c\(t\) $end:math:text$:

- Julia sets evolve continuously

- sudden structural changes occur

- these correspond to spikes in:

```text

Δ = frame-to-frame change

```

---

## ⚡ Result

```text

Transitions are detectable as mismatch spikes

induced by parameter motion

```

---

## 📊 Files

- `julia_path_analysis.md` → experiment setup  

- `transition_detection.md` → Δ definition & threshold  

- `figures/` → visual evidence  

---

## 🔥 Interpretation

```text

Fractals act as a parameter-driven transition system

```

---

## 🧭 Status

- reproducible  

- visually validated  

- not yet fully formalized  

---

**NEXAH Fractal Validation Layer**  

Thomas K. R. Hofmann · 2026

# 🔬 julia_path_analysis.md

# Julia Path Analysis

## Setup

We define a parameter trajectory:

```text

c(t) = center + r * exp(i t)

```

- center = -0.75  

- radius = 0.3  

- t ∈ [0, 2π]

---

## Procedure

For each $begin:math:text$ c\(t\) $end:math:text$:

1. compute Julia set  

2. normalize output  

3. compute frame difference  

---

## Metric

```text

Δ(t) = mean(|frame(t) - frame(t-1)|)

```

---

## Observation

- Δ remains low during smooth evolution  

- Δ spikes at structural transitions  

---

## Result

```text

parameter path crossing boundary → transition spike

```

---

## Visual

![Delta Plot](../../APPLIED_CASES/FRACTAL_SYSTEMS/scripts/outputs/delta_plot.png)

# ⚡ transition_detection.md

# Transition Detection

## Definition

We define transition intensity as:

```text

Δ(t) = mean absolute frame difference

```

---

## Threshold

Empirically:

```text

Δ > 0.08 → transition

```

---

## Observed Transitions

Example:

- frame 13 → Δ ≈ 0.13  

- frame 47 → Δ ≈ 0.13  

---

## Interpretation

```text

Transitions correspond to structural change

in Julia set topology

```

---

## Key Insight

```text

Transition is not continuous —

it appears as a discrete event in a continuous parameter flow

```

---

## Visual

![Delta Plot](./figures/delta_plot.png)

# 📌 INSERT INTO RESEARCH/README.md (UNDER VALIDATION SECTION)

---

### Fractal Systems (Mandelbrot / Julia)

NEXAH was applied to fractal systems by analyzing parameter-induced transitions.

Key observation:

```text

parameter motion → induces mismatch → triggers transitions

```

This extends the framework beyond intrinsic system dynamics

to externally driven transition structures.
