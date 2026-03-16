import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

TIME_WINDOW = 800        # how many timesteps to show
TIME_START = 2000        # starting point

WRAP_PHASE = True


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def wrap_angle(x):
    return (x + np.pi) % (2*np.pi) - np.pi


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

history = np.load(PHASE_FILE)

steps, nodes = history.shape

time_end = min(TIME_START + TIME_WINDOW, steps)

phase_slice = history[TIME_START:time_end]

if WRAP_PHASE:
    phase_slice = wrap_angle(phase_slice)

t = np.arange(phase_slice.shape[0])
n = np.arange(nodes)

T, N = np.meshgrid(t, n)


# ---------------------------------------------------------
# 3D SURFACE
# ---------------------------------------------------------

fig = plt.figure(figsize=(12,7))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(
    T,
    N,
    phase_slice.T,
    cmap="twilight",
    linewidth=0,
    antialiased=False
)

ax.set_xlabel("time")
ax.set_ylabel("node index")
ax.set_zlabel("phase")

ax.set_title("Phase Surface θ(node, time)")

fig.colorbar(surf, shrink=0.5, aspect=10)

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "phase_surface_3d.png", dpi=300)

plt.close()


# ---------------------------------------------------------
# RIDGE MAP (top view)
# ---------------------------------------------------------

plt.figure(figsize=(10,6))

plt.imshow(
    phase_slice.T,
    aspect="auto",
    origin="lower",
    cmap="twilight"
)

plt.colorbar(label="phase")

plt.xlabel("time")
plt.ylabel("node")

plt.title("Phase Field θ(node, time)")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "phase_surface_topview.png", dpi=300)

plt.close()


print("Phase surface visualization complete.")
print("Saved:")
print(" output/phase_surface_3d.png")
print(" output/phase_surface_topview.png")
