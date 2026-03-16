import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

SMOOTH_WINDOW = 50

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def moving_average(x, w):
    if w <= 1:
        return x
    kernel = np.ones(w) / w
    return np.convolve(x, kernel, mode="same")

def unwrap_phase_space(ph):
    return np.unwrap(ph, axis=1)

def unwrap_phase_time(ph):
    return np.unwrap(ph, axis=0)

# ---------------------------------------------------------
# LOAD
# ---------------------------------------------------------

history = np.load(PHASE_FILE)

steps, nodes = history.shape

# unwrap phase in both directions
phi = unwrap_phase_time(history)
phi = unwrap_phase_space(phi)

# ---------------------------------------------------------
# GRADIENTS
# ---------------------------------------------------------

dphi_dt = np.gradient(phi, axis=0)
dphi_dx = np.gradient(phi, axis=1)

eps = 1e-9
velocity = dphi_dt / (dphi_dx + eps)

# remove crazy spikes
velocity = np.clip(velocity, -5, 5)

# ---------------------------------------------------------
# SMOOTH
# ---------------------------------------------------------

vel_smooth = np.copy(velocity)

for i in range(nodes):
    vel_smooth[:, i] = moving_average(velocity[:, i], SMOOTH_WINDOW)

# ---------------------------------------------------------
# MEAN WAVE SPEED
# ---------------------------------------------------------

mean_speed = np.nanmean(vel_smooth)

# ---------------------------------------------------------
# PLOT 1: WAVE VELOCITY MAP
# ---------------------------------------------------------

plt.figure(figsize=(10,6))

plt.imshow(
    vel_smooth.T,
    aspect="auto",
    origin="lower",
    cmap="coolwarm"
)

plt.colorbar(label="wave velocity")

plt.xlabel("time")
plt.ylabel("node")

plt.title("Traveling Wave Velocity Map")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "wave_velocity_map.png")

plt.close()

# ---------------------------------------------------------
# PLOT 2: GLOBAL WAVE SPEED
# ---------------------------------------------------------

speed_t = np.nanmean(vel_smooth, axis=1)

plt.figure(figsize=(8,4))

plt.plot(speed_t)

plt.xlabel("time")
plt.ylabel("mean wave velocity")

plt.title("Global Wave Speed")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "global_wave_speed.png")

plt.close()

# ---------------------------------------------------------
# WAVE COHERENCE
# ---------------------------------------------------------

coherence = []

for t in range(steps):

    v = vel_smooth[t]

    coherence.append(np.std(v))

coherence = np.array(coherence)

plt.figure(figsize=(8,4))

plt.plot(coherence)

plt.xlabel("time")
plt.ylabel("velocity std")

plt.title("Wave Coherence")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "wave_coherence.png")

plt.close()

# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

with open(OUTPUT_DIR / "traveling_wave_report.txt","w") as f:

    f.write("Traveling Wave Report\n")
    f.write("=====================\n\n")

    f.write(f"nodes: {nodes}\n")
    f.write(f"timesteps: {steps}\n\n")

    f.write(f"mean wave speed: {mean_speed:.6f}\n")
    f.write(f"max speed: {np.max(vel_smooth):.4f}\n")
    f.write(f"min speed: {np.min(vel_smooth):.4f}\n\n")

    f.write("Interpretation\n")
    f.write("----------------\n")

    if abs(mean_speed) < 0.01:
        f.write("Standing wave / symmetric drift\n")
    elif mean_speed > 0:
        f.write("Wave traveling toward higher node index\n")
    else:
        f.write("Wave traveling toward lower node index\n")

print("Traveling wave analysis complete.")
