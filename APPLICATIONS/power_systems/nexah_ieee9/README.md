# ⚡ NEXAH — IEEE9 Stability Field System (v3)

## 🧭 Overview

This module implements the **NEXAH framework** on a power system test case (IEEE 9-bus).

It transforms classical voltage stability analysis into a:

> **continuous stability field with adaptive, closed-loop control**

---

## 🔬 Core Idea

Instead of asking:

> *"Will the system collapse?"*

NEXAH answers:

> *"Where are we in the stability field — and how can we navigate it?"*

---

## 🧱 Pipeline Architecture

```text
Simulation → Features → Manifold → Overlay → Prediction → Policy → Adaptive Control → System Evolution
```

---

## 📊 System Behavior (Latest Run)

### 🧪 Run ID

```
run_20260412_223816
```

---

### ⚡ Voltage Collapse (Adaptive Closed Loop)

![Voltage Collapse](results/run_20260412_223816/plot.png)

✔ Collapse dynamics preserved (no artificial suppression)  
✔ Adaptive stabilization in mid-regime  
✔ Structural transitions remain visible  

---

### 📉 Collapse Risk Field

![Collapse Risk](results/run_20260412_223816/risk.png)

✔ Peak risk ≈ 0.77  
✔ Fewer warnings (~3 vs ~37 in unstable runs)  
✔ Cleaner, more stable signal (less noise)  

---

### 🛠 Intervention Field

![Intervention](results/run_20260412_223816/intervention.png)

✔ Controlled intervention (no overreaction)  
✔ Smooth transition between regimes  
✔ Reduced saturation effects  

---

## 🧠 Interpretation (v3)

The system now behaves as:

> **adaptive field controller instead of reactive trigger system**

---

### 🔄 Evolution Across Versions

| Version | Behavior |
|--------|--------|
| v1 | reactive control |
| v2 | recovery + memory |
| v3 | **pre-emptive field control** |

---

### 🔍 What Changed in v3

- Risk becomes **stable and interpretable**
- Warnings reduced to meaningful events
- Control avoids oscillation and saturation
- System reacts to **trajectory**, not just state

---

## ⚖️ Classical vs NEXAH

| Feature                | Classical IEEE | NEXAH |
|----------------------|---------------|------|
| Static thresholds     | Yes           | No   |
| Dynamic risk field    | No            | Yes  |
| Early warning         | Limited       | Yes  |
| Closed-loop control   | No            | Yes  |
| Structural modeling   | No            | Yes  |
| Adaptive control      | No            | Yes  |

---

## 🚀 Run

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/decision/main_v2.py
```

---

## 📁 Results Folder

```
APPLICATIONS/power_systems/nexah_ieee9/results/
```

Each run contains:

- `plot.png` → system + states
- `risk.png` → collapse risk field
- `intervention.png` → control signal
- `states.txt`
- `actions_base.txt`
- `actions_adaptive.txt`
- `meta.json`

---

## 🧭 Status

```
Baseline      DONE
Manifold      DONE
Predictor     DONE
Policy        DONE
Closed Loop   DONE
Adaptive v3   DONE
Real Grid     IN PROGRESS
```

---

## ⚠️ Important Note

The current system uses a:

→ **synthetic solver (structural proxy)**

This means:

- physics-inspired, but not AC-accurate
- control affects abstract system behavior
- not yet a real power grid simulation

---

## 🔮 Next Step (Critical)

- Integrate **real AC power flow solver** (e.g. pandapower)
- Map actions to **physical interventions**:
  - load shedding
  - generation control
  - voltage support

---

## 🔥 Final Insight

> **Power systems are not binary (stable / unstable)**  
> → they exist inside a **structured stability landscape**

NEXAH turns this landscape into something we can:

→ **measure, interpret, and actively navigate**
