# ⚡ NEXAH — Scalable Stability Field System (IEEE X)

This module demonstrates the **scaling of the NEXAH framework**  
from small benchmark systems to **real-scale power grids (PEGASE 9241-bus)**.

---

# 🧠 Concept

NEXAH transforms power system dynamics into:

- structural fields
- risk landscapes
- adaptive intervention strategies

Instead of reacting to collapse, the system:

> **detects instability early and navigates stability regimes**

---

# 📊 Results Overview

## 🔹 IEEE 118 — Baseline

![IEEE118](results/run_ieee118_20260413_004449/overview.png)

- clear voltage collapse structure  
- early risk detection  
- proof of pipeline functionality  

---

## 🔹 IEEE 300 — Scaling Phase

![IEEE300](results/run_ieee300_20260413_015843/plot.png)

- emergence of nonlinear dynamics  
- structural feature activation  
- adaptive control becomes relevant  

---

## 🔹 IEEE 1354 — Large Grid

![IEEE1354](results/run_ieee1354_20260413_020204/plot.png)

- stable large-scale voltage field  
- distributed risk fluctuations  
- system remains controllable  

---

## 🔹 IEEE 9241 (PEGASE) — Real Scale

![IEEE9241](results/run_ieee9241_20260413_021422/plot.png)

- real-world scale behavior  
- early risk spike detection  
- stable regime after intervention  
- no full collapse observed  

---

# ⚙️ Pipeline

The system follows:

Simulation → Features → Manifold → Risk → Policy → Actions

Core components:

- Generic power flow solver (pandapower)
- Structural feature extraction
- Manifold fitting
- Risk prediction
- Adaptive intervention policy

---

# 🚀 Key Result

NEXAH successfully scales across:

collapse detection → stability navigation

---

# 🧭 Next Steps

- lead-time analysis vs classical methods  
- robustness across random seeds  
- integration with real grid data  

---

# 🌀 NEXAH

> From simulation to structure  
> From structure to navigation  
> From navigation to stability
