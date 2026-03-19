import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

N_INNER = 16
N_MIDDLE = 32

# optional smoothing
SMOOTH_WINDOW = 40


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def wrap_angle(x):
    return (x + np.pi) % (2*np.pi) - np.pi


def phase_gradient(theta_ring):

    n = len(theta_ring)

    grad = np.zeros(n)

    for i in range(n):

        j = (i+1) % n

        grad[i] = wrap_angle(theta_ring[j] - theta_ring[i])

    return grad


def moving_average(x, window):

    if window <= 1:
        return x

    kernel = np.ones(window)/window

    return np.convolve(x, kernel, mode="same")


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

history = np.load(PHASE_FILE)

steps, nodes = history.shape

N_OUTER = nodes - N_INNER - N_MIDDLE

inner = history[:, :N_INNER]
middle = history[:, N_INNER:N_INNER+N_MIDDLE]
outer = history[:, N_INNER+N_MIDDLE:]


# ---------------------------------------------------------
# GRADIENT COMPUTATION
# ---------------------------------------------------------

grad_inner = np.zeros_like(inner)
grad_middle = np.zeros_like(middle)
grad_outer = np.zeros_like(outer)

for t in range(steps):

    grad_inner[t] = phase_gradient(inner[t])
    grad_middle[t] = phase_gradient(middle[t])
    grad_outer[t] = phase_gradient(outer[t])


# ---------------------------------------------------------
# COMBINED MAP
# ---------------------------------------------------------

combined = np.concatenate([grad_inner, grad_middle, grad_outer], axis=1)


plt.figure(figsize=(10,6))

plt.imshow(combined.T,
           aspect="auto",
           origin="lower",
           cmap="coolwarm",
           vmin=-np.pi,
           vmax=np.pi)

plt.colorbar(label="phase gradient")

plt.xlabel("time")
plt.ylabel("node index")

plt.title("Phase Gradient Map")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "phase_gradient_map.png")

plt.close()


# ---------------------------------------------------------
# LAYER MAP
# ---------------------------------------------------------

fig, ax = plt.subplots(3,1, figsize=(10,7), sharex=True)

ax[0].imshow(grad_inner.T,
             aspect="auto",
             origin="lower",
             cmap="coolwarm",
             vmin=-np.pi,
             vmax=np.pi)

ax[0].set_title("Inner phase gradient")

ax[1].imshow(grad_middle.T,
             aspect="auto",
             origin="lower",
             cmap="coolwarm",
             vmin=-np.pi,
             vmax=np.pi)

ax[1].set_title("Middle phase gradient")

ax[2].imshow(grad_outer.T,
             aspect="auto",
             origin="lower",
             cmap="coolwarm",
             vmin=-np.pi,
             vmax=np.pi)

ax[2].set_title("Outer phase gradient")

plt.xlabel("time")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "phase_gradient_layers.png")

plt.close()


# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

mean_inner = np.mean(np.abs(grad_inner))
mean_middle = np.mean(np.abs(grad_middle))
mean_outer = np.mean(np.abs(grad_outer))

max_inner = np.max(np.abs(grad_inner))
max_middle = np.max(np.abs(grad_middle))
max_outer = np.max(np.abs(grad_outer))

with open(OUTPUT_DIR / "phase_gradient_report.txt","w") as f:

    f.write("Phase Gradient Report\n")
    f.write("=====================\n\n")

    f.write(f"nodes: {nodes}\n")
    f.write(f"timesteps: {steps}\n\n")

    f.write("Mean gradient magnitude\n\n")

    f.write(f"inner: {mean_inner:.4f}\n")
    f.write(f"middle: {mean_middle:.4f}\n")
    f.write(f"outer: {mean_outer:.4f}\n\n")

    f.write("Max gradient magnitude\n\n")

    f.write(f"inner: {max_inner:.4f}\n")
    f.write(f"middle: {max_middle:.4f}\n")
    f.write(f"outer: {max_outer:.4f}\n")


print("Phase gradient analysis complete.")
print("Saved to /output")
