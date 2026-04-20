# 🧭 NEXAH REAL DEMO (based on actual ENGINE behavior)

import numpy as np
import matplotlib.pyplot as plt

# REAL imports aus deinem System
from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# optional (falls vorhanden)
try:
    from ENGINE.analysis.flow_field_analysis import compute_flow_field
    FLOW_AVAILABLE = True
except:
    FLOW_AVAILABLE = False


def main():

    print("🚀 Running NEXAH Demo (REAL MODE)")

    # --------------------------------------------------
    # 1. Generate base field / landscape
    # --------------------------------------------------
    landscape = generate_stability_landscape()
    print("✔ Landscape generated")

    # --------------------------------------------------
    # 2. Optional Flow Field
    # --------------------------------------------------
    if FLOW_AVAILABLE:
        try:
            flow = compute_flow_field(landscape)
            print("✔ Flow field computed")
        except:
            flow = None
            print("⚠ Flow field failed")
    else:
        flow = None

    # --------------------------------------------------
    # VISUALIZATION
    # --------------------------------------------------
    plt.figure(figsize=(12, 5))

    # --- Landscape ---
    plt.subplot(1, 2, 1)
    plt.title("Stability Landscape")
    plt.imshow(landscape, cmap="viridis", origin="lower")

    # --- Flow or fallback ---
    plt.subplot(1, 2, 2)
    if flow is not None:
        plt.title("Flow Field")
        try:
            plt.imshow(flow, cmap="plasma", origin="lower")
        except:
            plt.text(0.5, 0.5, "Flow exists but not plottable")
    else:
        plt.title("No Flow Available")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
