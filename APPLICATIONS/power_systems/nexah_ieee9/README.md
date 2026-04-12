# ⚡ NEXAH — IEEE9 Stability Field System

## 🧭 Overview

This module implements the **NEXAH framework** on a power system test case (IEEE 9-bus).

It transforms classical voltage stability analysis into a:

> **continuous stability field with dynamic intervention capability**

---

## 🔬 Core Idea

Instead of asking:

> *"Will the system collapse?"*

NEXAH answers:

> *"Where are we in the stability field — and how can we navigate it?"*

---

## 🧱 Pipeline Architecture

Simulation → Features → Manifold → Overlay → Prediction → Policy → Control

### 🔹 Key Components

- Structural State (`c`)
- Dynamics (`dc`, `d2c`)
- Fragmentation (`frag`)
- Residual Field
- Distance-to-Rift
- Risk Field
- Intervention Policy

---

## ⚡ Closed-Loop Control

This implementation includes a **lightweight closed-loop solver**:

- Each simulation step reacts to the previous action
- Control actions modify system dynamics in real-time
- Collapse is delayed but not eliminated

---

## 📊 Results

### 📁 Result Folder

All runs are stored here:

    APPLICATIONS/power_systems/nexah_ieee9/results/

Each run contains:

- `plot.png` → full pipeline visualization  
- `risk.png` → collapse risk evolution  
- `intervention.png` → control signal  
- `states.txt` → NEXAH state timeline  
- `actions.txt` → applied intervention policy  

---

### 🧪 Latest Run

    run_20260412_210330

#### 🔹 Observations

- Early instability detected (λ ≈ 0.6–0.8)
- Risk peaks around ~0.88
- Intervention reduces risk amplitude
- Collapse still occurs at high λ

---

### 📉 Collapse Risk

- Smooth but structured risk field  
- Clear warning zones  
- Early detection capability  

---

### 🛠 Intervention Field

- High signal in unstable regions  
- Adaptive response over time  
- Decay near collapse (control saturation)  

---

### ⚡ Voltage Behavior

- Baseline collapse curve preserved  
- Slight delay under control  
- No artificial stabilization  

---

## 🧠 Interpretation

NEXAH does NOT replace physics.

It adds a new layer:

> **field-based navigation of system stability**

---

## ⚖️ Comparison to Classical Methods

| Feature                | Classical IEEE | NEXAH |
|----------------------|---------------|------|
| Static thresholds     | Yes           | No   |
| Dynamic risk field    | No            | Yes  |
| Early warning         | Limited       | Yes  |
| Closed-loop control   | No            | Yes  |
| Structural modeling   | No            | Yes  |

---

## 🚀 How to Run

    PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/main.py

---

## 📦 Structure

    nexah_ieee9/
    │
    ├── simulation/
    ├── features/
    ├── overlay/
    ├── analysis/
    ├── decision/
    ├── control/
    ├── results/
    └── main.py

---

## 🔮 Next Steps

- Integrate real AC solver (pandapower / PYPOWER)
- Extend to IEEE 14 / 30 / 118
- Add topology-aware interventions
- Multi-step predictive control
- Stability basin navigation

---

## 🧭 Status

    Baseline      DONE
    Manifold      DONE
    Predictor     DONE
    Policy        DONE
    Closed Loop   DONE
    Real Grid     IN PROGRESS

---

## 🔥 Final Insight

NEXAH shows that:

> **power systems are not just stable or unstable —  
they exist inside a navigable stability landscape**

---
