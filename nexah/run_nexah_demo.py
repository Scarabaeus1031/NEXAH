import numpy as np
import matplotlib.pyplot as plt

from nexah.field_layer.core.field_demo import generate_lorenz
from nexah.field_layer.core.field import Field
from nexah.field_layer.core.metrics import FieldMetrics


def main():
    print("\n🧭 NEXAH Demo — Field → Signal\n")

    # --- 1. Generate system ---
    t, trajectory = generate_lorenz(n_steps=5000)
    print("✔ Generated Lorenz trajectory")

    # --- 2. Build field ---
    field = Field(trajectory)
    print("✔ Constructed field")

    # --- 3. Metrics ---
    metrics = FieldMetrics(field)

    flow = metrics.flow_strength()
    curvature = metrics.curvature()

    # normalize
    flow_norm = flow / (np.max(flow) + 1e-8)
    curvature_norm = curvature / (np.max(curvature) + 1e-8)

    # --- 4. Combined signal ---
    risk = flow_norm * curvature_norm

    print("✔ Computed metrics")
    print("✔ Generated structural signal (risk)")

    # --- 5. Plot ---
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
    print("Signal peaks indicate structural transitions.\n")

    # --- 6. Mini Result Block ---
    print("📊 Stats:")
    print(f"Max risk: {np.max(risk):.3f}")
    print(f"Mean risk: {np.mean(risk):.3f}")


if __name__ == "__main__":
    main()
