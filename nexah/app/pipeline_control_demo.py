import numpy as np
import matplotlib.pyplot as plt

from nexah.field_layer.core.field import compute_field
from nexah.field_layer.core.metrics import (
    compute_flow_strength,
    compute_curvature,
)


# ----------------------------
# Signal
# ----------------------------

def generate_signal(n=500):
    t = np.linspace(0, 20, n)
    x = np.sin(t) + 0.3 * np.sin(5 * t)
    return x


# ----------------------------
# CONTROL PIPELINE
# ----------------------------

def run_control_pipeline(control_strength=0.1, threshold=0.8):
    x = generate_signal()
    X = x.reshape(-1, 1)

    # --- FIELD ---
    F = compute_field(X)

    flow = compute_flow_strength(F)
    curvature = compute_curvature(F)

    min_len = min(len(flow), len(curvature))
    flow = flow[:min_len]
    curvature = curvature[:min_len]

    risk = flow * curvature
    risk = (risk - np.min(risk)) / (np.max(risk) + 1e-8)

    # ----------------------------
    # CONTROL
    # ----------------------------

    x_controlled = x.copy()

    for t in range(min_len - 1):
        if risk[t] > threshold:
            # simple correction: damp movement
            delta = x_controlled[t] - x_controlled[t - 1]
            x_controlled[t + 1] -= control_strength * delta

    return x, x_controlled, risk


# ----------------------------
# PLOT
# ----------------------------

def plot_control():
    x, x_ctrl, risk = run_control_pipeline()

    plt.figure(figsize=(12, 5))

    plt.plot(x, label="Original", alpha=0.7)
    plt.plot(x_ctrl, label="Controlled", linestyle="--")

    # markieren wo Control greift
    threshold = 0.8
    peaks = np.where(risk > threshold)[0]

    plt.scatter(peaks, x[peaks], color="red", label="High Risk", s=20)

    plt.title("Control Injection Test")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_control()
