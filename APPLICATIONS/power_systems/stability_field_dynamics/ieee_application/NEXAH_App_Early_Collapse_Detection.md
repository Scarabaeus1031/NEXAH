
# 	NEXAH – Predictive Collapse Detection für Power Systems

## 🎯 Goal

Demonstrate that NEXAH detects instability **earlier than classical methods**.

---

## 📦 Folder Structure

APPLICATIONS/power_systems/demo/

    ├── run_demo.py
    ├── plot_results.py
    ├── demo_config.json
    └── README.md

---

## ⚙️ Core Idea

Input:
- Load scaling (λ)

Outputs:
- Classical:
  - min(V)
  - dV/dλ

- NEXAH:
  - curvature (d²c/dλ²)
  - fragmentation

---

## 🔥 Killer Moment

Plot all signals together:

- Classical → smooth degradation
- NEXAH → sharp spike BEFORE collapse

Mark:
- Collapse point
- Early warning point

---

## 🧪 run_demo.py (Outline)

1. Load IEEE system
2. Loop over load scaling λ
3. Run power flow
4. Extract:
   - voltage
   - phase
5. Compute:
   - classical metrics
   - NEXAH metrics
6. Detect:
   - collapse (non-convergence)
7. Save results

---

## 📊 plot_results.py (Outline)

1. Load saved data
2. Plot:
   - min(V)
   - dV/dλ
   - curvature
   - fragmentation
3. Highlight:
   - collapse point
   - early warning (curvature peak)

---

## 🧠 Key Message

"NEXAH detects instability before classical indicators."

---

## 🚀 Success Criteria

- Works in < 5 minutes
- One command to run
- One plot to convince

---

## ▶️ Command

python run_demo.py
