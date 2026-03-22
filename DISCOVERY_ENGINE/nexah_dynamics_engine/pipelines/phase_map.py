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

for i, orbit in enumerate(orbit_values):

    row = []

    for j, helix in enumerate(helix_values):

        params = {
            "orbit": float(orbit),
            "helix": float(helix)
        }

        print(f"\n--- GRID {i},{j} ---")
        res = run_pipeline(params, run_id=f"grid_{i}_{j}", visualize=False)

        results.append(res)

        label = res["classification"]

        # map to numeric
        if "Loop" in label:
            row.append(0)
        elif "Network" in label:
            row.append(1)
        else:
            row.append(2)

    phase_grid.append(row)

phase_grid = np.array(phase_grid)


# --------------------------------------------------
# PLOT
# --------------------------------------------------

plt.figure(figsize=(8, 6))
plt.imshow(phase_grid, origin="lower", aspect="auto")

plt.xticks(range(len(helix_values)), [round(v, 2) for v in helix_values])
plt.yticks(range(len(orbit_values)), [round(v, 2) for v in orbit_values])

plt.xlabel("helix")
plt.ylabel("orbit")
plt.title("Topology Phase Map")

plt.colorbar(label="Topology Class")

plt.show()
