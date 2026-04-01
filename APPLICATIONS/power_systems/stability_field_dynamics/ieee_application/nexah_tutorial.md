
# NEXAH Tutorial: A Step-by-Step Guide

## 🚀 Introduction

Welcome to the NEXAH Tutorial! This guide will help you understand the core functionalities of the NEXAH framework and walk you through the process of using it to navigate complex dynamical systems.

NEXAH is a field-based navigation system that models and optimizes stability within systems like power grids, data centers, and oscillatory networks. This tutorial will cover the following steps:

1. **Setting up NEXAH** 
2. **Understanding Core Features** 
3. **Running the Demo** 
4. **Interpreting Results**

---

## 1. Setting Up NEXAH

Before you start, you need to set up NEXAH on your local machine. 

### Step 1: Clone the Repository

First, clone the repository:

```bash
git clone https://github.com/Scarabaeus1031/NEXAH.git
cd NEXAH
```

### Step 2: Install Dependencies

Install the required Python dependencies:

```bash id="g9kxiy"
pip install -r requirements.txt
```

---

## 2. Understanding Core Features

NEXAH consists of several key modules:

### Field-based System Modeling

NEXAH models systems as continuous fields. This allows for more accurate representation of dynamics, identifying regions of stability and instability.

### Instability Detection

NEXAH detects "rifts," which are instability corridors within the system. These rifts are areas where the system is at risk of collapse.

### Intervention Application

Once a critical point is identified, NEXAH applies a minimal intervention to move the system away from collapse and toward stability.

---

## 3. Running the Demo

To run the demo, execute the following script:

```bash id="p6zn75"
python APPLICATIONS/power_systems/ieee_application/run_ieee_navigation_demo.py
```

This will run the NEXAH field navigation demo on an IEEE power grid model. The system will simulate the power grid, detect instabilities, apply interventions, and improve the overall stability of the system.

---

## 4. Interpreting Results

The output will show:

- **Before Stability**: The stability value of the system before intervention.
- **After Stability**: The stability value after applying the intervention.
- **Critical Point**: The index and values for the critical point (the system’s most unstable area).
- **Intervention**: The applied intervention and its effect on the stability.

Additionally, a plot will be generated showing the system's trajectory, the detected rift, the critical point, and the system after intervention.

### Example Output

```plaintext id="428d39"
⚡ NEXAH FIELD NAVIGATION RESULT

Before Stability: 0.924
After Stability:  0.964

Critical Point:
  index = 146
  c = 0.934
  dc_before = 0.622
  dc_after  = 0.747

📊 Plot saved to:
APPLICATIONS/power_systems/stability_field_dynamics/ieee_application/results/demo_plot.png
```

---

## Additional Features

- **Field Visualization**: The demo produces visual outputs such as system trajectories, instability zones (rifts), and post-intervention states.
- **Rift Detection**: The demo identifies the critical rift (instability region) and intervenes by applying a minimal adjustment.
- **Stability Metrics**: The stability metric shows the system’s stability before and after intervention.

---

## Conclusion

This tutorial demonstrates how NEXAH can be used to identify and address instability in complex systems, such as power grids. By modeling the system as a field and detecting instability through rift identification, NEXAH can provide actionable interventions to improve stability. 

The next steps involve expanding NEXAH’s capabilities and applying it to real-world systems with larger networks and more complex dynamics.
