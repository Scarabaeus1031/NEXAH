import numpy as np
import matplotlib.pyplot as plt

from pipelines.real_pipeline import run_pipeline

# 🔥 META ANALYSIS IMPORTS
from analysis.phase_transition_detector import analyze_phase_space
from analysis.phase_gradient import compute_phase_gradient
from analysis.topology_diversity import compute_diversity


# --------------------------------------------------
# PARAM GRID
# --------------------------------------------------

orbit_values = np.linspace(0.1, 0.5, 8)
helix_values = np.linspace(0.0, 0.5, 8)


# --------------------------------------------------
# RUN GRID
# --------------------------------------------------

results = []
phase_grid = []

rotation_grid = []
strength_grid = []
angle_grid = []   # 🔥 NEW

for i, orbit in enumerate(orbit_values):

    row = []
    rot_row = []
    strength_row = []
    angle_row = []   # 🔥 NEW

    for j, helix in enumerate(helix_values):

        params = {
            "orbit": float(orbit),
            "helix": float(helix)
        }

        print(f"\n--- GRID {i},{j} ---")
        res = run_pipeline(params, run_id=f"grid_{i}_{j}", visualize=False)

        results.append(res)

        # --------------------------------------------------
        # CLASSIFICATION MAP
        # --------------------------------------------------

        label = res["classification"]

        if "Loop" in label:
            row.append(0)
        elif "Network" in label:
            row.append(1)
        else:
            row.append(2)

        # --------------------------------------------------
        # ROTATION MAP
        # --------------------------------------------------

        rot = res.get("rotation", "NONE")
        strength = res.get("rotation_strength", 0.0)

        if rot == "CCW":
            rot_row.append(1)
        elif rot == "CW":
            rot_row.append(-1)
        else:
            rot_row.append(0)

        strength_row.append(float(strength))

        # --------------------------------------------------
        # 🔥 ANGLE MAP
        # --------------------------------------------------

        angle_data = res.get("angle_data", {})
        dominant_angle = angle_data.get("dominant_angle", 0.0)

        angle_row.append(float(dominant_angle))

    phase_grid.append(row)
    rotation_grid.append(rot_row)
    strength_grid.append(strength_row)
    angle_grid.append(angle_row)   # 🔥 NEW


# --------------------------------------------------
# TO NUMPY
# --------------------------------------------------

phase_grid = np.array(phase_grid)
rotation_grid = np.array(rotation_grid)
strength_grid = np.array(strength_grid)
angle_grid = np.array(angle_grid)   # 🔥 NEW


# --------------------------------------------------
# 🔥 META ANALYSIS
# --------------------------------------------------

print("\n==============================")
print("PHASE TRANSITION ANALYSIS")
print("==============================")

transitions = analyze_phase_space(results)

gradient = compute_phase_gradient(phase_grid)
diversity = compute_diversity(results, phase_grid.shape)


# --------------------------------------------------
# PLOT 1: TOPOLOGY PHASE MAP
# --------------------------------------------------

plt.figure(figsize=(8, 6))
plt.imshow(phase_grid, origin="lower", aspect="auto")

plt.xticks(range(len(helix_values)), [round(v, 2) for v in helix_values])
plt.yticks(range(len(orbit_values)), [round(v, 2) for v in orbit_values])

plt.xlabel("helix")
plt.ylabel("orbit")
plt.title("Topology Phase Map")

plt.colorbar(label="Topology Class")


# --------------------------------------------------
# PLOT 2: ROTATION FIELD
# --------------------------------------------------

plt.figure(figsize=(8, 6))
plt.imshow(rotation_grid, origin="lower", aspect="auto")

plt.xticks(range(len(helix_values)), [round(v, 2) for v in helix_values])
plt.yticks(range(len(orbit_values)), [round(v, 2) for v in orbit_values])

plt.xlabel("helix")
plt.ylabel("orbit")
plt.title("Rotation Field (CCW=+1, CW=-1)")

plt.colorbar(label="Rotation")


# --------------------------------------------------
# PLOT 3: ROTATION STRENGTH
# --------------------------------------------------

plt.figure(figsize=(8, 6))
plt.imshow(strength_grid, origin="lower", aspect="auto")

plt.xticks(range(len(helix_values)), [round(v, 2) for v in helix_values])
plt.yticks(range(len(orbit_values)), [round(v, 2) for v in orbit_values])

plt.xlabel("helix")
plt.ylabel("orbit")
plt.title("Rotation Strength")

plt.colorbar(label="Strength")


# --------------------------------------------------
# PLOT 4: PHASE GRADIENT
# --------------------------------------------------

plt.figure(figsize=(8, 6))
plt.imshow(gradient, origin="lower", aspect="auto")

plt.xticks(range(len(helix_values)), [round(v, 2) for v in helix_values])
plt.yticks(range(len(orbit_values)), [round(v, 2) for v in orbit_values])

plt.xlabel("helix")
plt.ylabel("orbit")
plt.title("Phase Gradient Map")

plt.colorbar(label="Gradient Strength")


# --------------------------------------------------
# PLOT 5: TOPOLOGY DIVERSITY
# --------------------------------------------------

plt.figure(figsize=(8, 6))
plt.imshow(diversity, origin="lower", aspect="auto")

plt.xticks(range(len(helix_values)), [round(v, 2) for v in helix_values])
plt.yticks(range(len(orbit_values)), [round(v, 2) for v in orbit_values])

plt.xlabel("helix")
plt.ylabel("orbit")
plt.title("Topology Diversity Map")

plt.colorbar(label="Signature Spread")


# --------------------------------------------------
# 🔥 PLOT 6: ANGLE FIELD
# --------------------------------------------------

plt.figure(figsize=(8, 6))
plt.imshow(angle_grid, origin="lower", aspect="auto")

plt.xticks(range(len(helix_values)), [round(v, 2) for v in helix_values])
plt.yticks(range(len(orbit_values)), [round(v, 2) for v in orbit_values])

plt.xlabel("helix")
plt.ylabel("orbit")
plt.title("Dominant Angle Field (Degrees)")

plt.colorbar(label="Angle (°)")


plt.show()
