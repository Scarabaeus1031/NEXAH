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
- enables **trajectory-aware control**

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
| v7–v9 | 🧪 experimental | dynamical behavior |
| v10–v11 | 🧪 internal | field navigation |

👉 v6 = reproducible baseline  

---

# 📊 From Collapse → Field → Navigation

## 🔹 1. Collapse Geometry

![Voltage Collapse](results/run_20260412_223816/plot.png)

Collapse is a **continuous boundary in state space**.

---

## 🔹 2. Flow Field Dynamics

![Flow Field](results/controller_runs/controller_replay_20260413_214411/field_overlay.png)

System trajectories follow **structured flow paths**.

👉 Instability is directional, not random.

---

## 🔹 3. Risk Field

![Risk](results/run_20260412_223816/risk.png)

- low → stable  
- sharp rise → instability boundary  

---

## 🔹 4. Field Navigation (Prototype)

![Navigation GIF](results/visuals/nexah_navigation_v11.gif)

Controller approaches the boundary without triggering collapse.

- smooth convergence  
- reduced oscillation  

⚠️ Based on internal versions (v7–v11)

---

## 🧠 Interpretation

The system behaves as:

> a trajectory evolving inside a structured stability field

---

## 🚀 Run

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v6.py
```

---

## 🔥 Core Insight

Instability is not triggered by thresholds.

It emerges from **field structure**.

---

**Thomas K. R. Hofmann · 2026**
