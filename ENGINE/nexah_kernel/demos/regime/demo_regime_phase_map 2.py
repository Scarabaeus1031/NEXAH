"""
NEXAH Demo — Regime Phase Map

This demo generates a simple regime phase map for a nonlinear dynamical system.

A logistic map is simulated across a parameter grid. The resulting dynamics
are classified into regimes:

• STABLE
• PERIODIC
• CHAOTIC

The map illustrates how different dynamical regimes emerge across parameter space.

The resulting visualization is saved into:

ENGINE/nexah_kernel/demos/visuals
"""

import numpy as np
import matplotlib.pyplot as plt
import os


# ---------------------------------------------------------
# logistic map
# ---------------------------------------------------------

def logistic_map(r, x):

    return r * x * (1 - x)


# ---------------------------------------------------------
# classify regime
# ---------------------------------------------------------

def classify_series(series):

    variance = np.var(series)

    if variance < 1e-4:
        return 0  # stable

    if variance < 0.02:
        return 1  # periodic

    return 2  # chaotic


# ---------------------------------------------------------
# parameter grid
# ---------------------------------------------------------

r_values = np.linspace(2.5, 4.0, 300)
x0_values = np.linspace(0.01, 0.99, 200)

regime_map = np.zeros((len(x0_values), len(r_values)))


# ---------------------------------------------------------
# simulation
# ---------------------------------------------------------

for i, x0 in enumerate(x0_values):

    for j, r in enumerate(r_values):

        x = x0
        series = []

        for t in range(300):

            x = logistic_map(r, x)

            if t > 100:
                series.append(x)

        regime_map[i, j] = classify_series(series)


# ---------------------------------------------------------
# plot map
# ---------------------------------------------------------

plt.figure(figsize=(10,6))

plt.imshow(
    regime_map,
    extent=[r_values.min(), r_values.max(), x0_values.min(), x0_values.max()],
    origin="lower",
    aspect="auto",
    cmap="viridis"
)

plt.colorbar(label="Regime")

plt.title("NEXAH Regime Phase Map (Logistic System)")
plt.xlabel("Parameter r")
plt.ylabel("Initial State x0")

plt.tight_layout()


# ---------------------------------------------------------
# save visualization
# ---------------------------------------------------------

output_dir = "ENGINE/nexah_kernel/demos/visuals"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, "logistic_regime_phase_map.png")

plt.savefig(output_file, dpi=150)
plt.show()

print("\nSaved visualization to:", output_file)
