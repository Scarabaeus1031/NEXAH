import numpy as np
import matplotlib.pyplot as plt

from nexah.field_layer.core.field_demo import generate_lorenz
from nexah.field_layer.core.metrics import compute_flow_strength, compute_curvature


def main():
    print("\n🧭 NEXAH Demo — Field → Signal\n")

    # --- 1. Generate system ---
    t, trajectory = generate_lorenz(n_steps=5000)

    print("✔ Generated Lorenz trajectory")

    # --- 2. Compute field metrics ---
    flow = compute_flow_strength(trajectory)
    curvature = compute_curvature(trajectory)

    # normalize
    flow_norm = flow / (np.max(flow) + 1e-8)
    curvature_norm = curvature / (np.max(curvature) + 1e-8)

    # --- 3. Combined signal ---
    risk = flow_norm * curvature_norm

    print("✔ Computed field metrics")
    print("✔ Generated structural signal (risk)")

    # --- 4. Plot ---
    fig, axs = plt.subplots(4, 1, figsize=(10, 8), sharex=True)

    axs[0].plot(t, trajectory[:, 0])
    axs[0].set_title("Lorenz Trajectory (x)")

    axs[1].plot(t, flow_norm)
    axs[1].set_title("Flow Strength")

    axs[2].plot(t, curvature_norm)
    axs[2].set_title("Curvature")

    axs[3].plot(t, risk)
    axs[3].set_title("NEXAH Signal (Flow × Curvature)")

    plt.tight_layout()
    plt.show()

    print("\n🔥 Result:")
    print("Signal peaks indicate structural transitions in the system.\n")


if __name__ == "__main__":
    main()
