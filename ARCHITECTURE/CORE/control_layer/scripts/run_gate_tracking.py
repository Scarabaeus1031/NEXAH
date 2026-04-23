# ARCHITECTURE/CORE/control_layer/scripts/run_gate_tracking.py

import numpy as np
import matplotlib.pyplot as plt
import os

print("⚡ NEXAH Gate Tracking")


# --------------------------------
# Config
# --------------------------------
INPUT_PATH = "ARCHITECTURE/CORE/control_layer/outputs/demo/gate_points.npy"
OUTPUT_PATH = "ARCHITECTURE/CORE/control_layer/outputs/demo/"

DT = 0.05
STEPS = 120


# --------------------------------
# Safety check
# --------------------------------
if not os.path.exists(INPUT_PATH):
    raise FileNotFoundError(
        "❌ gate_points.npy fehlt.\n"
        "→ bitte zuerst run_gate_extraction.py ausführen"
    )


# --------------------------------
# Load gates
# --------------------------------
gates = np.load(INPUT_PATH)


# --------------------------------
# Vector field (gleich wie überall)
# --------------------------------
def field(x, y):
    dx = y - 0.3 * x - x * (x**2 + y**2)
    dy = -x - 0.3 * y - y * (x**2 + y**2)
    return np.array([dx, dy])


# --------------------------------
# Tracking
# --------------------------------
trajectories = []

for g in gates:
    traj = [g.copy()]
    pos = g.copy()

    for _ in range(STEPS):
        f = field(pos[0], pos[1])
        pos = pos + DT * f
        traj.append(pos.copy())

    trajectories.append(np.array(traj))


# --------------------------------
# Save
# --------------------------------
os.makedirs(OUTPUT_PATH, exist_ok=True)

np.save(
    os.path.join(OUTPUT_PATH, "gate_trajectories.npy"),
    trajectories
)


# --------------------------------
# Plot
# --------------------------------
plt.figure(figsize=(8, 8))

# Field background
xx, yy = np.meshgrid(
    np.linspace(-2, 2, 60),
    np.linspace(-2, 2, 60)
)

u, v = field(xx, yy)
plt.streamplot(xx, yy, u, v, color="black", density=1.2)


# Plot trajectories
for i, traj in enumerate(trajectories):
    plt.plot(
        traj[:, 0],
        traj[:, 1],
        linewidth=2,
        label=f"gate {i}"
    )

    # Startpunkt
    plt.scatter(traj[0, 0], traj[0, 1], s=100, color="magenta")

    # Endpunkt
    plt.scatter(traj[-1, 0], traj[-1, 1], s=60, color="cyan")


# Zentrum
plt.scatter(0, 0, s=180, color="yellow", edgecolor="black", label="core")


plt.title("NEXAH Gate Tracking")
plt.legend()
plt.grid(True)

plt.savefig(
    os.path.join(OUTPUT_PATH, "nexah_gate_tracking.png"),
    dpi=150
)

print(f"✔ Saved → {OUTPUT_PATH}nexah_gate_tracking.png")


# --------------------------------
# Interpretation
# --------------------------------
print("\n🧠 Interpretation:\n")
print("Magenta = initial gate positions")
print("Lines   = gate trajectories over time")
print("Cyan    = final positions\n")

print("→ gates are NOT fixed structures")
print("→ they drift along the field")
print("→ stable gates converge toward attractor structures")
print("→ unstable gates dissolve or diverge")
