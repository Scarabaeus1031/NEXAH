import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


# =========================================================
# LOAD
# =========================================================
def load_data():
    trajectory = None
    for f in ["trajectory.npy", "states.npy"]:
        path = os.path.join(BASE_DIR, f)
        if os.path.exists(path):
            trajectory = np.load(path)
            print(f"✅ Loaded trajectory: {f}")
            break

    if trajectory is None:
        raise FileNotFoundError("❌ No trajectory found")

    if trajectory.shape[1] > 2:
        print("⚠️ Reducing trajectory to 2D")
        trajectory = trajectory[:, :2]

    rift = None
    for f in ["rift_curve.npy", "rift.npy"]:
        path = os.path.join(RIFT_DIR, f)
        if os.path.exists(path):
            rift = np.load(path)
            print(f"✅ Loaded rift: {f}")
            break

    if rift is None:
        raise FileNotFoundError("❌ No rift found")

    # optional layer-aware navigator output
    layer_nav = None
    for f in ["trajectory_lock.npy", "trajectory_adaptive.npy", "trajectory_controlled_tangent.npy"]:
        path = os.path.join(RIFT_DIR, f)
        if os.path.exists(path):
            layer_nav = np.load(path)
            print(f"✅ Loaded control path: {f}")
            break

    return trajectory, rift, layer_nav


# =========================================================
# GRID EXTRACTION
# =========================================================
def cluster_axis(values, eps=0.035, min_samples=4):
    """
    1D clustering along one axis using DBSCAN.
    """
    X = values.reshape(-1, 1)
    model = DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(X)

    centers = []
    for lab in sorted(set(labels)):
        if lab == -1:
            continue
        pts = values[labels == lab]
        centers.append(np.mean(pts))

    centers = np.array(sorted(centers))
    return labels, centers


def extract_grid(trajectory, rift, controlled=None):
    # combine available structures
    x_all = [trajectory[:, 0], rift[:, 0]]
    y_all = [trajectory[:, 1], rift[:, 1]]

    if controlled is not None:
        x_all.append(controlled[:, 0])
        y_all.append(controlled[:, 1])

    x_all = np.concatenate(x_all)
    y_all = np.concatenate(y_all)

    # cluster vertical / horizontal preferred lines
    x_labels, x_centers = cluster_axis(x_all, eps=0.045, min_samples=5)
    y_labels, y_centers = cluster_axis(y_all, eps=0.035, min_samples=5)

    return x_centers, y_centers, x_all, y_all


# =========================================================
# PLOTS
# =========================================================
def plot_grid(trajectory, rift, controlled, x_centers, y_centers):
    plt.figure(figsize=(9, 6))

    plt.plot(trajectory[:, 0], trajectory[:, 1], color="green", label="original")
    plt.plot(rift[:, 0], rift[:, 1], color="cyan", label="rift")

    if controlled is not None:
        plt.plot(controlled[:, 0], controlled[:, 1], color="gold", label="layer-aware")

    # vertical channels
    for i, xc in enumerate(x_centers):
        plt.axvline(x=xc, color="purple", alpha=0.65, linewidth=1.5,
                    label="channel x" if i == 0 else None)

    # horizontal layers
    for i, yc in enumerate(y_centers):
        plt.axhline(y=yc, color="magenta", alpha=0.65, linewidth=1.5,
                    label="layer y" if i == 0 else None)

    plt.scatter(trajectory[-1, 0], trajectory[-1, 1], c="red", s=55, label="orig end")
    if controlled is not None:
        plt.scatter(controlled[-1, 0], controlled[-1, 1], c="orange", s=55, label="controlled end")

    plt.title("NEXAH FIELD — Grid Extraction / Channel Detection")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend()
    plt.grid(True, alpha=0.25)

    out = os.path.join(RIFT_DIR, "grid_extraction.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"💾 Saved → {out}")
    plt.show()


def plot_histograms(x_all, y_all, x_centers, y_centers):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    axes[0].hist(x_all, bins=40, color="mediumpurple", alpha=0.75)
    for xc in x_centers:
        axes[0].axvline(xc, color="black", linewidth=1.5)
    axes[0].set_title("Channel Density (PC1)")
    axes[0].set_xlabel("PC1")

    axes[1].hist(y_all, bins=40, color="hotpink", alpha=0.75)
    for yc in y_centers:
        axes[1].axvline(yc, color="black", linewidth=1.5)
    axes[1].set_title("Layer Density (PC2)")
    axes[1].set_xlabel("PC2")

    out = os.path.join(RIFT_DIR, "grid_density_histograms.png")
    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"💾 Saved → {out}")
    plt.show()


# =========================================================
# SAVE SUMMARY
# =========================================================
def save_grid_summary(x_centers, y_centers):
    np.save(os.path.join(RIFT_DIR, "grid_x_centers.npy"), x_centers)
    np.save(os.path.join(RIFT_DIR, "grid_y_centers.npy"), y_centers)

    txt_path = os.path.join(RIFT_DIR, "grid_summary.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("NEXAH GRID EXTRACTION SUMMARY\n")
        f.write("============================\n\n")
        f.write("X-channel centers (PC1):\n")
        for v in x_centers:
            f.write(f"  {v:.6f}\n")
        f.write("\nY-layer centers (PC2):\n")
        for v in y_centers:
            f.write(f"  {v:.6f}\n")

    print(f"💾 Saved → {txt_path}")


# =========================================================
# MAIN
# =========================================================
def main():
    trajectory, rift, controlled = load_data()

    x_centers, y_centers, x_all, y_all = extract_grid(trajectory, rift, controlled)

    print("✅ Extracted x-channel centers:", np.round(x_centers, 4))
    print("✅ Extracted y-layer centers  :", np.round(y_centers, 4))

    plot_grid(trajectory, rift, controlled, x_centers, y_centers)
    plot_histograms(x_all, y_all, x_centers, y_centers)
    save_grid_summary(x_centers, y_centers)

    print("🚀 Grid extraction complete")


if __name__ == "__main__":
    main()
