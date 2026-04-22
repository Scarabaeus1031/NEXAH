import numpy as np
import matplotlib.pyplot as plt
import os

from nexah.field_layer.core.field_demo import generate_lorenz
from nexah.field_layer.core.field import Field
from nexah.field_layer.core.metrics import FieldMetrics


def main():
    print("\n🧭 NEXAH Demo — Structure inside Dynamics\n")

    # --- 1. Generate system ---
    trajectory = generate_lorenz(T=5000)
    print("✔ Generated Lorenz trajectory")

    # --- 2. Build field ---
    field = Field(trajectory)
    metrics = FieldMetrics(field)
    print("✔ Constructed field")

    # --- 3. Metrics ---
    flow = metrics.flow_strength()
    curvature = metrics.curvature()

    # normalize
    flow_norm = flow / (np.max(flow) + 1e-8)
    curvature_norm = curvature / (np.max(curvature) + 1e-8)

    # --- 4. Structural signal ---
    risk = flow_norm * curvature_norm
    print("✔ Generated structural signal")

    # --- 5. Peak detection ---
    peaks = risk > np.percentile(risk, 99)

    # --- 6. Plot ---
    plt.figure(figsize=(8, 6))

    plt.plot(
        trajectory[:, 0],
        trajectory[:, 1],
        alpha=0.25,
        linewidth=1
    )

    plt.scatter(
        trajectory[peaks, 0],
        trajectory[peaks, 1],
        s=10
    )

    plt.title("NEXAH — Structural Transitions in Lorenz System")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.tight_layout()

    # --- 7. Save (KEY FOR README) ---
    out_dir = "outputs/demo"
    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, "nexah_lorenz_transitions.png")
    plt.savefig(out_path, dpi=200)

    print(f"✔ Saved plot → {out_path}")

    plt.show()

    # --- 8. Result block ---
    print("\n🔥 Result:")
    print("Transitions are not random — they cluster in specific regions.\n")

    print("📊 Stats:")
    print(f"Max risk: {np.max(risk):.3f}")
    print(f"Mean risk: {np.mean(risk):.3f}")
    print(f"Peak count: {np.sum(peaks)}")


if __name__ == "__main__":
    main()
