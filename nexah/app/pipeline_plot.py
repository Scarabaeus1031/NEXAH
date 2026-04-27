import numpy as np
import matplotlib.pyplot as plt

from nexah.app.pipeline_demo import run_pipeline


def plot_pipeline():
    result = run_pipeline()

    x = result["x"]
    risk = result["risk"]
    basins = result["basins"]

    t = np.arange(len(risk))

    # ----------------------------
    # 1. State + Risk Overlay
    # ----------------------------
    fig1, ax1 = plt.subplots(figsize=(10, 4))

    ax1.set_title("State vs Risk")

    ax1.plot(x[:len(risk)], label="State", alpha=0.7)

    # scale risk to state for visibility
    risk_scaled = risk / (np.max(risk) + 1e-8) * np.max(x)
    ax1.plot(risk_scaled, linestyle="--", label="Risk (scaled)")

    ax1.legend()
    plt.tight_layout()

    # ----------------------------
    # 2. Basin Segmentation
    # ----------------------------
    fig2, ax2 = plt.subplots(figsize=(10, 4))

    ax2.set_title("Basin Segmentation")

    scatter = ax2.scatter(
        t,
        x[:len(risk)],
        c=basins,
        cmap="viridis",
        s=10
    )

    plt.colorbar(scatter, label="Basin ID")
    plt.tight_layout()

    # ----------------------------
    # 3. High Risk Events
    # ----------------------------
    threshold = np.percentile(risk, 95)
    peaks = np.where(risk > threshold)[0]

    fig3, ax3 = plt.subplots(figsize=(10, 4))

    ax3.set_title("High Risk Events")

    ax3.plot(x[:len(risk)], label="State")

    ax3.scatter(
        peaks,
        x[peaks],
        color="red",
        label="High Risk"
    )

    ax3.legend()
    plt.tight_layout()

    # ----------------------------
    # Show all
    # ----------------------------
    plt.show()


if __name__ == "__main__":
    plot_pipeline()
