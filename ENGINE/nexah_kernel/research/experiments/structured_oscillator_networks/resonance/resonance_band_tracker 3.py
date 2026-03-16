import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")

SYNC_THRESHOLD = 0.95
LOCK_THRESHOLD = 0.85
DRIFT_THRESHOLD = 0.4


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def kuramoto_order(phases):

    return np.abs(np.mean(np.exp(1j * phases), axis=1))


def moving_average(x, window=50):

    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode="same")


def classify_regime(order_parameter):

    mean_r = np.mean(order_parameter)
    std_r = np.std(order_parameter)

    if mean_r > SYNC_THRESHOLD:
        return "GLOBAL_SYNC"

    if mean_r > LOCK_THRESHOLD:
        return "MODE_LOCKED"

    if mean_r > DRIFT_THRESHOLD and std_r < 0.1:
        return "METASTABLE"

    if std_r > 0.25:
        return "CHAOTIC"

    return "DRIFT"


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

OUTPUT_DIR.mkdir(exist_ok=True)

history = np.load(PHASE_FILE)

if history.ndim != 2:
    raise RuntimeError("phase_history must be 2D")

steps, nodes = history.shape

time = np.arange(steps)


# ---------------------------------------------------------
# ORDER PARAMETER
# ---------------------------------------------------------

order = kuramoto_order(history)

order_smooth = moving_average(order, 80)


# ---------------------------------------------------------
# REGIME CLASSIFICATION
# ---------------------------------------------------------

regime = classify_regime(order_smooth)


# ---------------------------------------------------------
# PLOT
# ---------------------------------------------------------

plt.figure(figsize=(10,5))

plt.plot(time, order, alpha=0.3, label="order parameter")
plt.plot(time, order_smooth, linewidth=2, label="smoothed")

plt.axhline(SYNC_THRESHOLD, linestyle="--", alpha=0.4)
plt.axhline(LOCK_THRESHOLD, linestyle="--", alpha=0.4)

plt.title(f"Phase Regime: {regime}")
plt.xlabel("time")
plt.ylabel("Kuramoto Order R")

plt.legend()
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "phase_regime.png")

plt.close()


# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

report = OUTPUT_DIR / "phase_regime_report.txt"

with open(report, "w") as f:

    f.write("Phase Regime Report\n")
    f.write("===================\n\n")

    f.write(f"Nodes: {nodes}\n")
    f.write(f"Timesteps: {steps}\n\n")

    f.write(f"Mean Order: {np.mean(order_smooth):.4f}\n")
    f.write(f"Std Order: {np.std(order_smooth):.4f}\n\n")

    f.write(f"Detected Regime: {regime}\n")


print("Regime classification complete.")
print("Detected:", regime)
