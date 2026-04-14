# ⚡ NEXAH — IEEE9 Stability Field Navigation

![Status](https://img.shields.io/badge/status-active-success)
![Field Model](https://img.shields.io/badge/field-model-blue)
![Navigation](https://img.shields.io/badge/navigation-enabled-brightgreen)
![Dynamics](https://img.shields.io/badge/dynamics-v6_public_|_v11_dev-orange)

---

## 🧭 Abstract

NEXAH introduces a new paradigm for power system stability:

> **Stability is not a binary condition — it is a navigable field.**

Instead of detecting collapse after it occurs, NEXAH:

- reconstructs the **underlying stability geometry**
- defines a **continuous risk field**
- enables **closed-loop trajectory-aware control**

---

## 🔬 Problem

Classical methods rely on:

- static thresholds  
- discrete labels  
- post-event detection  

→ instability is detected **too late**

---

## 💡 Approach

NEXAH models the system as a **structured stability landscape**

- each state has a **position in a field**
- instability is a **geometric property**
- control becomes **movement within that field**

---

## 🧱 Pipeline

```text
Simulation → Features → Manifold → Field → Risk → Policy → Control → Navigation
```

---

## 🧭 Version Map (Controller Evolution)

| Version | Status | Description |
|--------|--------|------------|
| v6 | ✅ public | stable closed-loop control |
| v7–v9 | 🧪 experimental | dynamical system behavior |
| v10–v11 | 🧪 internal | field geometry & navigation |

👉 v6 = reproducible baseline  
👉 newer versions = ongoing development  

---

## 🎬 Field Navigation (Prototype)

![Navigation GIF](results/visuals/nexah_navigation_v11.gif)

Controller approaches the stability boundary without triggering collapse.

- smooth convergence  
- reduced oscillation  

⚠️ Based on internal versions (v7–v11)

---

## 📊 Field Reconstruction

### Collapse Geometry

![Voltage Collapse](results/run_20260412_223816/plot.png)

Collapse appears as a **continuous boundary**, not a discrete event.

---

### Risk Field

![Risk](results/run_20260412_223816/risk.png)

- low → stable  
- sharp rise → instability boundary  

---

## 🧠 Interpretation

The system behaves as:

> a trajectory evolving inside a structured stability field

- field = extracted from system physics  
- geometry = stability structure  
- control = trajectory shaping  

---

## 🚀 Run (Public Version)

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v6.py
```

- v6 = stable & reproducible  
- v7–v11 = internal evolution  

---

## 🔥 Result

A complex system can be:

- mapped into a field  
- described geometrically  
- controlled via trajectory shaping  

---

## 🧠 Core Insight

Instability is not triggered by thresholds.

It emerges from **field structure**.

---

**Thomas K. R. Hofmann · 2026**
