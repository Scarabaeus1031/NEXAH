# 🧠 NEXAH — Dynamical Models

This directory contains the **core dynamical system models** used in the NEXAH framework.

These models describe how systems evolve within a **stability landscape**.

---

## 🧭 Overview

All models in this directory are based on the same foundational idea:

> Systems evolve within a structured state space defined by stability.

The differences between models arise from how system dynamics are defined.

---

## 📦 Model Hierarchy

The models form a clear progression of complexity:

### 🔹 1. Stability Landscape (Core)

👉 `../core/STABILITY_LANDSCAPE/`

The foundational concept of NEXAH.

Defines:
- state space structure  
- attractors  
- stability regions  
- transition boundaries  

> This is the **base layer** for all other models.

---

### 🔹 2. Gradient Systems

👉 `GRADIENT_SYSTEM/`

Dynamics follow the gradient of the stability function:

```
dx/dt = -∇V(x)
```

Characteristics:
- deterministic motion  
- convergence to attractors  
- no external forcing  

---

### 🔹 3. Drift Systems

👉 `DRIFT_SYSTEM/`

Extends gradient systems by adding external forces:

```
dx/dt = -∇V(x) + F(x,t)
```

Characteristics:
- directional drift  
- forced transitions  
- non-equilibrium behavior  

---

### 🔹 4. Regime Systems

👉 `REGIME_SYSTEM/`

Introduces multiple attractor basins and structural transitions:

```
dx/dt = -∇V(x) + R(x,t)
```

Characteristics:
- multiple stable states  
- tipping points  
- regime shifts  

---

## 🧠 Interpretation

These models describe increasing levels of system complexity:

| Model | Description |
|------|-------------|
| Gradient | single attractor, smooth convergence |
| Drift | external forcing modifies trajectories |
| Regime | multiple attractors and transitions |

---

## 🔗 Role in NEXAH

This directory provides the **theoretical foundation** for:

- structure discovery  
- field modeling  
- navigation logic  

Applications such as:

- Lorenz systems  
- power grids  
- multi-agent systems  

are built on top of these models.

---

## 🧭 How to Use

If you are new to NEXAH:

1. Start with **Stability Landscape**
2. Continue with **Gradient Systems**
3. Explore **Drift Systems**
4. Understand **Regime Systems**

This progression builds intuition step by step.

---

## ⚠️ Note

These models are:

- conceptual and mathematical  
- not executable applications  

For runnable examples, see:

👉 `APPLICATIONS/`  
👉 `APPLICATIONS/demos/`

---

## 🌀 Summary

> Stability defines structure.  
> Structure defines dynamics.  
> Dynamics enables navigation.

---

**NEXAH Framework · 2026**
