import os
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")

# ==============================
# LOAD (ROBUST)
# ==============================
def load_data():

    trajectory = np.load(os.path.join(BASE_DIR, "trajectory_pca.npy"))

    # ---- try multiple filenames ----
    candidates = [
        "rift_curve.npy",
        "rift.npy",
        "rift_points.npy"
    ]

    rift_curve = None

    for name in candidates:
        path = os.path.join(RIFT_DIR, name)
        if os.path.exists(path):
            print(f"✅ Found rift file: {name}")
            rift_curve = np.load(path)
            break

    if rift_curve is None:
        raise FileNotFoundError(
            f"❌ No rift file found in {RIFT_DIR}\n"
            f"Tried: {candidates}"
        )

    print("✅ Data loaded")
    return trajectory, rift_curve

# ==============================
# PROJECT TO RIFT
# ==============================
def project_to_rift(trajectory, rift_curve):
    projected = []

    for p in trajectory:
        dists = np.linalg.norm(rift_curve - p, axis=1)
        idx = np.argmin(dists)
        projected.append(rift_curve[idx])

    return np.array(projected)

# ==============================
# BLEND
# ==============================
def blend_trajectory(original, projected, alpha=0.4):
    return (1 - alpha) * original + alpha * projected

# ==============================
# PLOT
# ==============================
def plot_control(original, projected, blended):

    plt.figure(figsize=(6, 6))

    plt.plot(original[:,0], original[:,1], color='green', label='original')
    plt.plot(projected[:,0], projected[:,1], color='cyan', label='rift projection')
    plt.plot(blended[:,0], blended[:,1], color='yellow', label='controlled')

    plt.legend()
    plt.title("Rift-guided trajectory control")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.tight_layout()
    plt.show()

# ==============================
# MAIN
# ==============================
def main():

    trajectory, rift_curve = load_data()

    print(f"Trajectory shape: {trajectory.shape}")
    print(f"Rift shape: {rift_curve.shape}")

    projected = project_to_rift(trajectory, rift_curve)
    controlled = blend_trajectory(trajectory, projected)

    plot_control(trajectory, projected, controlled)

    # save
    np.save(os.path.join(RIFT_DIR, "trajectory_projected.npy"), projected)
    np.save(os.path.join(RIFT_DIR, "trajectory_controlled.npy"), controlled)

    print("💾 Control trajectories saved")

if __name__ == "__main__":
    main()
