# 📐 NEXAH — Formal Risk Field Definition

---

## 🧠 Purpose

This document defines the **NEXAH risk function**:

risk(x)

which maps system states to a **continuous scalar instability measure**.

---

## 🔬 State Space

We define the system state:

x ∈ ℝⁿ

In applications (e.g. power systems), this is typically:

x = (c, f, κ, r, d)

Where:

- c → coherence  
- f → fragmentation  
- κ → curvature (instability acceleration)  
- r → residual (distance from learned manifold)  
- d → distance to separatrix  

---

## 🔧 Normalization

All features are normalized:

ẑᵢ = (zᵢ - zᵢ_min) / (zᵢ_max - zᵢ_min + ε)

We define instability-aligned variables:

c⁻ = 1 - ĉ  
d⁻ = 1 - d̂  

---

## ⚙️ Risk Function

We define:

s(x) = w_c·c⁻ + w_f·f + w_κ·κ + w_r·r + w_d·d⁻ + b

with:

- wᵢ ≥ 0  
- Σ wᵢ = 1  

Final mapping:

risk(x) = 1 / (1 + exp(-s(x)))

---

## 🔁 Dynamic Risk

For trajectories:

R(t) = risk(x(t))

Time evolution:

Ṙ = ∇risk(x) · ẋ

Interpretation:

- R → current instability  
- Ṙ → direction toward instability  

---

## 🧭 Geometric Interpretation

Define:

- Stability region:
  
  Ω = { x | risk(x) < τ }

- Separatrix:

  S = { x | risk(x) = τ }

Distance to boundary:

d(x, S) = inf ||x - y||, y ∈ S

---

## 🧠 Interpretation

risk(x) approximates:

→ probability of entering unstable regime  

It combines:

- structural deviation  
- dynamic instability  
- geometric proximity  

---

## ⚠️ Status

This is a **formal working definition**, not yet fully proven.

Open tasks:

- weight identification  
- separatrix construction  
- Lyapunov validation  

---

## 🌀 NEXAH

Structure → Field → Risk → Trajectory → Control
