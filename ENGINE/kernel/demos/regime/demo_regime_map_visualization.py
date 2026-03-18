"""
NEXAH Demo — Regime Map Visualization

This demo visualizes a simple dynamical system evolving inside
a double-well energy landscape.

The goal is to illustrate how system trajectories move across
different regimes and how these regimes correspond to regions
of the landscape.

This script produces a visualization showing:

• the energy landscape
• the system trajectory
• regime regions
"""

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# potential landscape
# ---------------------------------------------------------

def potential(x):
    return x**4 - x**2


def gradient(x):
    return 4*x**3 - 2*x


# ---------------------------------------------------------
# simulate system
# ---------------------------------------------------------

def simulate_double_well(steps=400, dt=0.05):

    x = 0.5
    trajectory = []

    for _ in range(steps):

        noise = np.random.normal(0, 0.25)

        x = x - gradient(x)*dt + noise*np.sqrt(dt)

        trajectory.append(x)

    return np.array(trajectory)


# ---------------------------------------------------------
# run simulation
# ---------------------------------------------------------

trajectory = simulate_double_well()


# ---------------------------------------------------------
# build landscape
# ---------------------------------------------------------

x_space = np.linspace(-2, 2, 400)
landscape = potential(x_space)


# ---------------------------------------------------------
# regime classification (simple)
# ---------------------------------------------------------

regimes = []

for x in trajectory:

    if x < -0.2:
        regimes.append("LEFT_WELL")

    elif x > 0.2:
        regimes.append("RIGHT_WELL")

    else:
        regimes.append("BARRIER")


# ---------------------------------------------------------
# plotting
# ---------------------------------------------------------

plt.figure(figsize=(10,6))

# energy landscape
plt.plot(x_space, landscape, linewidth=3, label="Energy Landscape")

# trajectory points
plt.scatter(trajectory, potential(trajectory),
            c=np.linspace(0,1,len(trajectory)),
            cmap="viridis",
            s=20,
            label="System Trajectory")

# regime boundaries
plt.axvline(-0.2, linestyle="--", alpha=0.4)
plt.axvline(0.2, linestyle="--", alpha=0.4)

plt.title("NEXAH Regime Landscape Demo")
plt.xlabel("System State")
plt.ylabel("Potential Energy")

plt.legend()
plt.tight_layout()

import os

# output directory
output_dir = "ENGINE/nexah_kernel/demos/visuals"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, "double_well_regime_map.png")

plt.savefig(output_file, dpi=150)
plt.show()

print("\nSaved visualization to:", output_file)


# ---------------------------------------------------------
# summary
# ---------------------------------------------------------

print("\nTrajectory length:", len(trajectory))

unique_regimes = set(regimes)

print("Visited regimes:", unique_regimes)
