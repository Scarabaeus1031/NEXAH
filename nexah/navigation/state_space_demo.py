import numpy as np
import matplotlib.pyplot as plt

from nexah.field_layer.core.field import compute_field
from nexah.field_layer.core.metrics import (
    compute_flow_strength,
    compute_curvature,
)

from nexah.navigation.state_space_control import apply_state_space_control


def generate_signal(n=500):
    t = np.linspace(0, 20, n)
    return np.sin(t) + 0.3 * np.sin(5 * t)


def run():
    x = generate_signal()

    X = x.reshape(-1, 1)
    F = compute_field(X)

    flow = compute_flow_strength(F)
    curvature = compute_curvature(F)

    min_len = min(len(flow), len(curvature))
    x = x[:min_len]
    flow = flow[:min_len]
    curvature = curvature[:min_len]

    risk = flow * curvature
    risk = (risk - np.min(risk)) / (np.max(risk) + 1e-8)

    # 🔥 NEW CONTROL
    x_ctrl = apply_state_space_control(
        x,
        risk,
        strength=0.05,
        bins=60
    )

    return x, x_ctrl, risk


def plot():
    x, x_ctrl, risk = run()

    plt.figure(figsize=(12, 5))

    plt.plot(x, label="Original", alpha=0.7)
    plt.plot(x_ctrl, label="Controlled", linestyle="--")

    peaks = np.where(risk > 0.8)[0]
    plt.scatter(peaks, x[peaks], color="red", label="High Risk")

    plt.title("State Space Control Test (v4)")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot()
