# ENGINE/analysis/navigation_level41_axis_detector.py

import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 80
N_AGENTS = 120
STEPS = 900

STEP_SIZE = 0.14
NOISE = 0.002
DAMPING = 0.96

# --------------------------------------------------
# SETUP
# --------------------------------------------------

field = generate_stability_landscape(SIZE)

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

angles = []

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    for i in range(N_AGENTS):

        x, y = positions[i]

        # Gradient
        gx = field[min(int(y), SIZE-1), min(int(x+1), SIZE-1)] - field[min(int(y), SIZE-1), int(x)]
        gy = field[min(int(y+1), SIZE-1), min(int(x), SIZE-1)] - field[int(y), min(int(x), SIZE-1)]

        force = np.array([gx, gy])

        noise = np.random.randn(2) * NOISE

        velocities[i] = velocities[i] * DAMPING + STEP_SIZE * force + noise
        positions[i] += velocities[i]

        positions[i] = np.clip(positions[i], 0, SIZE-1)

        # store angle
        v = velocities[i]
        norm = np.linalg.norm(v)
        if norm > 1e-6:
            angle = np.arctan2(v[1], v[0])
            angles.append(angle)

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

angles = np.array(angles)

# histogram
bins = 180
hist, edges = np.histogram(angles, bins=bins, range=(-np.pi, np.pi))

# --------------------------------------------------
# PLOT
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(6,6), subplot_kw={'projection': 'polar'})

centers = (edges[:-1] + edges[1:]) / 2

ax.plot(centers, hist)
ax.set_title("Axis Distribution (Level 41)")

# --------------------------------------------------
# SAVE
# --------------------------------------------------

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
out_dir = f"ENGINE/visuals/level41_{timestamp}"
os.makedirs(out_dir, exist_ok=True)

plt.savefig(os.path.join(out_dir, "axis_distribution.png"))
plt.close()

# --------------------------------------------------
# STATS
# --------------------------------------------------

top_indices = np.argsort(hist)[-5:]
dominant_angles = centers[top_indices]

print("Run complete:", timestamp)
print("Dominant angles (rad):", dominant_angles)
print("Saved to:", out_dir)
