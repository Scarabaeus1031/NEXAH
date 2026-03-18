import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")

WINDOW = 100
NEIGHBOR_RADIUS = 4


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

history = np.load(PHASE_FILE)

steps, nodes = history.shape

time = np.arange(steps)

OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# HELPER
# ---------------------------------------------------------

def moving_average(x, window):

    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode="same")


def local_order(phases):

    local_R = np.zeros(nodes)

    for i in range(nodes):

        left = max(0, i - NEIGHBOR_RADIUS)
        right = min(nodes, i + NEIGHBOR_RADIUS + 1)

        neighbors = phases[left:right]

        local_R[i] = np.abs(np.mean(np.exp(1j * neighbors)))

    return local_R


# ---------------------------------------------------------
# BUILD FIELD MAP
# ---------------------------------------------------------

field_map = np.zeros((steps, nodes))

for t in range(steps):

    field_map[t] = local_order(history[t])


# ---------------------------------------------------------
# SMOOTH FIELD
# ---------------------------------------------------------

for n in range(nodes):

    field_map[:, n] = moving_average(field_map[:, n], WINDOW)


# ---------------------------------------------------------
# PLOT FIELD MAP
# ---------------------------------------------------------

plt.figure(figsize=(12,6))

plt.imshow(
    field_map.T,
    aspect="auto",
    origin="lower",
    cmap="viridis"
)

plt.colorbar(label="local synchronisation")

plt.xlabel("time")
plt.ylabel("node")

plt.title("Resonance Field Map")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "resonance_field_map.png")

plt.close()


# ---------------------------------------------------------
# GLOBAL FIELD METRIC
# ---------------------------------------------------------

field_strength = np.mean(field_map, axis=1)

plt.figure(figsize=(10,4))

plt.plot(time, field_strength)

plt.title("Global Resonance Field Strength")

plt.xlabel("time")
plt.ylabel("field strength")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "resonance_field_strength.png")

plt.close()


# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

with open(OUTPUT_DIR / "resonance_field_report.txt", "w") as f:

    f.write("Resonance Field Report\n")
    f.write("======================\n\n")

    f.write(f"nodes: {nodes}\n")
    f.write(f"timesteps: {steps}\n\n")

    f.write(f"mean field strength: {np.mean(field_strength):.4f}\n")
    f.write(f"std field strength: {np.std(field_strength):.4f}\n")
    f.write(f"max field strength: {np.max(field_strength):.4f}\n")


print("Resonance field map complete.")
