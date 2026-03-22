import numpy as np
import matplotlib.pyplot as plt

from pipelines.real_pipeline import run_pipeline


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

# NEW
rotation_grid = []
strength_grid = []

for i, orbit in enumerate(orbit_values):

    row = []
    rot_row = []
    strength_row = []

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
        # ROTATION MAP (SAFE ACCESS)
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

    phase_grid.append(row)
    rotation_grid.append(rot_row)
    strength_grid.append(strength_row)


phase_grid = np.array(phase_grid)
rotation_grid = np.array(rotation_grid)
strength_grid = np.array(strength_grid)


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


plt.show()
