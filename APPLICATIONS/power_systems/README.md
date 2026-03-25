# IEEE Test Systems in NEXAH

Application: Stability Analysis of Real Power Grid Benchmarks

This module introduces IEEE test systems as a first real-world application of the NEXAH framework.

---

## What this module does

We use standard IEEE power grid models (starting with the 14-bus system) and perform a simple experiment:

Gradually increase system load and observe when the grid becomes unstable.

At each step:
- power flow is computed
- system stability is evaluated (convergence vs collapse)

---

## Why IEEE test systems?

IEEE test systems (14, 30, 57, 118 bus) are widely used benchmarks in power systems research.

They provide:
- realistic network topology
- well-defined load and generation profiles
- a standard reference for stability analysis

---

## First goal (Phase 1)

Detect the stability boundary of the IEEE 14-bus system.

Result:
- below threshold → system stable
- above threshold → collapse (no convergence)

---

## Run the demo

```bash
cd APPLICATIONS/power_grid/ieee
python run_scan.py
```

## Output (example)
```bash
Load factor: 1.00 → Stable
Load factor: 1.30 → Stable
Load factor: 1.60 → Stable
Load factor: 1.75 → Unstable
```
## Why this matters

This is the first step toward constructing a stability landscape for real infrastructure systems.

⸻

## Roadmap

	•	IEEE 14-bus loading and simulation
	•	stability scan (collapse detection)
	•	stability landscape (2D parameter space)
	•	structural extraction
	•	navigation layer

⸻

## Goal of this module

To demonstrate that NEXAH can operate on real-world benchmark systems, not just abstract models.
---

# 🧠 **Code – Phase 1 (läuft wirklich)**

## 📄 ieee_loader.py

```python
import pandapower.networks as pn

def load_ieee14():
    return pn.case14()
```

# 📄 stability_scan.py
```python
	import pandapower as pp

	def run_stability_scan(net, min_factor=1.0, max_factor=2.0, steps=20):
    results = []

    for i in range(steps + 1):
        factor = min_factor + (max_factor - min_factor) * i / steps

        net_copy = net.deepcopy()
        net_copy.load["p_mw"] *= factor

        try:
            pp.runpp(net_copy)
            stable = True
        except:
            stable = False

        results.append((factor, stable))

    return results
---
```
# 📄 run_scan.py
```python
from ieee_loader import load_ieee14
from stability_scan import run_stability_scan

def main():

    net = load_ieee14()

    results = run_stability_scan(net)

    for factor, stable in results:
        status = "Stable" if stable else "Unstable"
        print(f"Load factor: {factor:.2f} → {status}")
        
        if __name__ == "__main__":
        main()
```
# ⚡ Installation (nicht vergessen)
```python

pip install pandapower
