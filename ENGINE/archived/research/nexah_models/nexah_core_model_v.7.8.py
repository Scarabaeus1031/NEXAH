import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# NEXAH v7.8 — Controlled Regime Navigation
# ============================================================

# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------
steps = 12000
dt = 0.01

sigma = 10
rho = 28
beta = 8/3

# control strength
k_control = 0.15

# target distribution
target = {
    "eye": 0.05,
    "moon": 0.30,
    "deris": 0.65
}

# thresholds
eye_r = 4.0
moon_split = 0.0

# ------------------------------------------------------------
# LORENZ SYSTEM
# ------------------------------------------------------------
def lorenz(x, y, z):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

# ------------------------------------------------------------
# REGION CLASSIFICATION
# ------------------------------------------------------------
def classify(x, y, z):
    r = np.sqrt(x**2 + y**2)

    if r < eye_r:
        return "eye"
    elif x < moon_split:
        return "moon"
    else:
        return "deris"

# ------------------------------------------------------------
# CONTROL FORCE
# ------------------------------------------------------------
def control_force(region_counts, total_steps, x):
    if total_steps < 100:
        return 0.0

    current = {
        k: region_counts[k] / total_steps
        for k in region_counts
    }

    error = {
        k: target[k] - current[k]
        for k in target
    }

    # steering logic
    force = 0.0

    # push away from overpopulated regions
    if error["deris"] < 0:
        force -= k_control * abs(error["deris"])

    if error["moon"] < 0:
        force += k_control * abs(error["moon"])

    if error["eye"] < 0:
        force += k_control * 0.5

    # slight directional bias
    return force * np.sign(x + 1e-6)

# ------------------------------------------------------------
# SIMULATION
# ------------------------------------------------------------
x, y, z = 0.1, 0.0, 0.0

traj = []
regions = []
region_counts = {"eye": 0, "moon": 0, "deris": 0}

for i in range(steps):
    dx, dy, dz = lorenz(x, y, z)

    region = classify(x, y, z)
    region_counts[region] += 1

    u = control_force(region_counts, i + 1, x)

    # apply control to dx (steering in x-direction)
    dx += u

    x += dx * dt
    y += dy * dt
    z += dz * dt

    traj.append([x, y, z])
    regions.append(region)

traj = np.array(traj)

# ------------------------------------------------------------
# FINAL DISTRIBUTION
# ------------------------------------------------------------
total = len(regions)
counts = {
    k: regions.count(k) for k in ["eye", "moon", "deris"]
}

print("\n=== NEXAH v7.8 Summary ===")
for k in counts:
    print(f"{k}: {counts[k]} ({counts[k]/total:.3f})")

# ------------------------------------------------------------
# PLOT — STATE COLORED
# ------------------------------------------------------------
colors = {
    "eye": "green",
    "moon": "blue",
    "deris": "red"
}

plt.figure(figsize=(8,6))

for k in colors:
    mask = np.array(regions) == k
    plt.scatter(traj[mask,0], traj[mask,1],
                s=1, c=colors[k], label=k)

plt.title("NEXAH v7.8 — Controlled Navigation")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# TIMELINE
# ------------------------------------------------------------
timeline = [ ["eye","moon","deris"].index(r) for r in regions ]

plt.figure(figsize=(10,3))
plt.plot(timeline, lw=1)
plt.yticks([0,1,2], ["eye","moon","deris"])
plt.title("State Timeline (controlled)")
plt.tight_layout()
plt.show()
