# 🔬 Julia Path Analysis

## 🧭 Purpose

This experiment analyzes how **parameter motion**  
induces structural transitions in Julia sets.

---

## ⚙️ Setup

We define a parameter trajectory:

$$
c(t) = c_0 + r \cdot e^{i t}
$$

with:

- $c_0 = -0.75$  
- $r = 0.3$  
- $t \in [0, 2\pi]$

---

## 🔁 Procedure

For each $c(t)$:

1. compute Julia set  
2. normalize output  
3. compute frame difference  

---

## 📏 Metric

```text
Δ(t) = mean(|frame(t) - frame(t-1)|)
```

---

## 🔬 Observation

- Δ remains low during smooth evolution  
- Δ spikes at structural transitions  

---

## ⚡ Result

```text
parameter path crossing boundary → transition spike
```

---

## 🧠 Interpretation

```text
Transitions emerge from parameter-induced structural mismatch
```

---

## 📊 Visual

![Delta Plot](../../APPLIED_CASES/FRACTAL_SYSTEMS/scripts/outputs/delta_plot.png)

---

## 🔗 Connection to NEXAH

```text
Δ(t) ≈ M(t)

observable mismatch proxy
```

---

**NEXAH Fractal Experiment**  
Julia Parameter Path  
Thomas K. R. Hofmann · 2026
