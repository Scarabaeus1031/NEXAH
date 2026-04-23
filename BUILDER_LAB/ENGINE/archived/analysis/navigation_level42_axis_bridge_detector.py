# ENGINE/analysis/navigation_level42_axis_bridge_detector.py

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

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

AXIS_THRESHOLD = 0.015
BRIDGE_THRESHOLD = 0.02

# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_stability_landscape(size=SIZE)
memory = np.zeros_like(field)

agents = np.random.rand(N_AGENTS, 2) * SIZE

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def get_gradient(pos):
    x, y = int(pos[0]), int(pos[1])
    x = np.clip(x, 1, SIZE - 2)
    y = np.clip(y, 1, SIZE - 2)

    gx = field[x + 1, y] - field[x - 1, y]
    gy = field[x, y + 1] - field[x, y - 1]

    return np.array([gx, gy])


def angle(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return np.arctan2(dy, dx)


def detect_axis(points):
    angles = []

    for i in range(len(points) - 1):
        angles.append(angle(points[i], points[i + 1]))

    hist, bins = np.histogram(angles, bins=180, range=(-np.pi, np.pi))
    peak_idx = np.argmax(hist)
    axis_angle = (bins[peak_idx] + bins[peak_idx + 1]) / 2

    return axis_angle, hist


def detect_bridges(points, axis_angle):
    bridges = []

    for i in range(len(points) - 2):
        a1 = angle(points[i], points[i + 1])
        a2 = angle(points[i + 1], points[i + 2])

        delta = abs(a2 - a1)

        if delta > np.pi:
            delta = 2 * np.pi - delta

        # axis proximity + directional change
        if abs(a1 - axis_angle) < AXIS_THRESHOLD and delta > BRIDGE_THRESHOLD:
            bridges.append(points[i + 1])

    return bridges


# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

trajectories = []

for step in range(STEPS):

    new_agents = []

    for a in agents:

        grad = get_gradient(a)
        noise = np.random.randn(2) * NOISE

        velocity = grad * STEP_SIZE + noise
        velocity *= DAMPING

        new_pos = a + velocity
        new_pos = np.clip(new_pos, 0, SIZE - 1)

        memory[int(new_pos[0]), int(new_pos[1])] += 1

        new_agents.append(new_pos)
        trajectories.append(new_pos.copy())

    agents = np.array(new_agents)

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

trajectory_array = np.array(trajectories)

axis_angle, axis_hist = detect_axis(trajectory_array)
bridges = detect_bridges(trajectory_array, axis_angle)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig = plt.figure(figsize=(12, 10))

# Field
plt.subplot(2, 2, 1)
plt.title("Field")
plt.imshow(field, cmap="viridis")

# Memory
plt.subplot(2, 2, 2)
plt.title("Memory")
plt.imshow(memory, cmap="magma")

# Axis Histogram
plt.subplot(2, 2, 3, projection='polar')
plt.title("Axis Distribution")

theta = np.linspace(-np.pi, np.pi, len(axis_hist))
plt.plot(theta, axis_hist)

# Bridges
plt.subplot(2, 2, 4)
plt.title("Axis Bridges")

if len(bridges) > 0:
    bridges = np.array(bridges)
    plt.scatter(bridges[:, 1], bridges[:, 0], s=5)

plt.gca().invert_yaxis()

# --------------------------------------------------
# SAVE
# --------------------------------------------------

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
out_dir = f"ENGINE/visuals/level42_{timestamp}"
os.makedirs(out_dir, exist_ok=True)

plt.savefig(f"{out_dir}/plot.png")
plt.close()

# --------------------------------------------------
# STATS
# --------------------------------------------------

result = {
    "axis_angle": float(axis_angle),
    "num_bridges": int(len(bridges)),
    "bridge_density": float(len(bridges) / len(trajectory_array))
}

with open(f"{out_dir}/stats.json", "w") as f:
    json.dump(result, f, indent=2)

print("Run complete:", timestamp)
print("Axis angle:", axis_angle)
print("Bridges:", len(bridges))
print("Saved to:", out_dir)
