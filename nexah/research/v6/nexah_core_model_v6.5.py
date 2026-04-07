# ============================================================
# NEXAH v6.5 — Fiber Classification + Separatrix Detection
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# ------------------------------------------------------------
# Hopf Projection
# ------------------------------------------------------------
def hopf_projection(v, dv, mode, energy):
    v_n = (v - 0.7) / 0.4
    dv_n = dv / 0.05

    mode_phase = mode * np.pi / 2.0

    x1 = v_n
    x2 = dv_n
    x3 = np.sin(mode_phase)
    x4 = np.cos(mode_phase)

    norm = np.sqrt(x1**2 + x2**2 + x3**2 + x4**2 + 1e-9)

    x1 /= norm
    x2 /= norm
    x3 /= norm
    x4 /= norm

    X = 2 * (x1 * x3 + x2 * x4)
    Y = 2 * (x2 * x3 - x1 * x4)
    Z = x1**2 + x2**2 - x3**2 - x4**2

    return X, Y, Z


# ------------------------------------------------------------
# Dummy trajectory
# Replace later with real traj if needed
# Format: (v, dv, mode, energy)
# ------------------------------------------------------------
def generate_dummy_traj(n=5000):
    traj = []

    for t in range(n):
        tt = t * 0.015

        v = 0.78 + 0.14 * np.sin(tt) + 0.05 * np.sin(2.7 * tt + 0.3)
        dv = 0.028 * np.cos(tt) + 0.018 * np.cos(2.7 * tt + 0.3)

        mode = (t // 350) % 4
        energy = dv**2 + 0.08 * (v - 0.84)**2

        traj.append((v, dv, mode, energy))

    return traj


# ------------------------------------------------------------
# Build Hopf arrays
# ------------------------------------------------------------
def build_hopf_arrays(traj):
    Xs, Ys, Zs, modes, energies = [], [], [], [], []

    for v, dv, mode, energy in traj:
        mode = int(mode) % 4
        X, Y, Z = hopf_projection(v, dv, mode, energy)

        Xs.append(X)
        Ys.append(Y)
        Zs.append(Z)
        modes.append(mode)
        energies.append(energy)

    return (
        np.array(Xs),
        np.array(Ys),
        np.array(Zs),
        np.array(modes),
        np.array(energies),
    )


# ------------------------------------------------------------
# Torus angles
# ------------------------------------------------------------
def compute_torus_angles(X, Y, Z):
    cx = np.mean(X)
    cy = np.mean(Y)

    theta_major = np.unwrap(np.arctan2(Y - cy, X - cx))

    r_major = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    R0 = np.mean(r_major)

    tube_x = r_major - R0
    tube_y = Z - np.mean(Z)

    theta_minor = np.unwrap(np.arctan2(tube_y, tube_x))

    return theta_major, theta_minor, cx, cy, R0


# ------------------------------------------------------------
# Simple fiber feature extraction
# ------------------------------------------------------------
def extract_fiber_features(X, Y, Z, modes):
    feats = []

    for mode in range(4):
        idx = np.where(modes == mode)[0]
        if len(idx) < 20:
            continue

        Xm = X[idx]
        Ym = Y[idx]
        Zm = Z[idx]

        theta_major, theta_minor, _, _, _ = compute_torus_angles(Xm, Ym, Zm)

        major_turns = (theta_major[-1] - theta_major[0]) / (2 * np.pi)
        minor_turns = (theta_minor[-1] - theta_minor[0]) / (2 * np.pi)

        feat = {
            "mode": mode,
            "major_turns": major_turns,
            "minor_turns": minor_turns,
            "mean_x": np.mean(Xm),
            "mean_y": np.mean(Ym),
            "mean_z": np.mean(Zm),
            "std_x": np.std(Xm),
            "std_y": np.std(Ym),
            "std_z": np.std(Zm),
        }
        feats.append(feat)

    return feats


# ------------------------------------------------------------
# Very lightweight fiber classification
# 3 classes:
#   outer_arc
#   inner_loop
#   transition_fiber
# ------------------------------------------------------------
def classify_fibers(features):
    results = []

    for f in features:
        mag = abs(f["major_turns"])
        mm = abs(f["minor_turns"])
        spread = f["std_x"] + f["std_y"] + f["std_z"]

        if mag > 3.2 and spread > 0.9:
            label = "outer_arc"
        elif mm > 0.25:
            label = "transition_fiber"
        else:
            label = "inner_loop"

        results.append({**f, "label": label})

    return results


# ------------------------------------------------------------
# Separatrix detection
# Idea:
# points where sign of X changes near central gap
# and local velocity changes strongly
# ------------------------------------------------------------
def detect_separatrix_points(X, Y, Z):
    sep_idx = []

    dX = np.gradient(X)
    dY = np.gradient(Y)
    dZ = np.gradient(Z)

    speed = np.sqrt(dX**2 + dY**2 + dZ**2)

    x_thr = 0.08
    y_thr = 0.35

    for i in range(1, len(X) - 1):
        sign_flip = np.sign(X[i - 1]) != np.sign(X[i + 1])
        near_center = abs(X[i]) < x_thr and abs(Y[i]) < y_thr
        active = speed[i] > np.percentile(speed, 65)

        if sign_flip and near_center and active:
            sep_idx.append(i)

    return np.array(sep_idx, dtype=int)


# ------------------------------------------------------------
# Braid / crossing detection
# Simplified:
# count crossings in Y-order between neighboring time points
# ------------------------------------------------------------
def detect_braid_crossings(X, Y, Z, window=40):
    crossings_t = []
    crossings_rank = []

    n = len(X)
    if n < window + 2:
        return np.array([]), np.array([])

    # ring index proxy from Z ranking in rolling windows
    for t in range(0, n - window, window):
        z_seg = Z[t:t + window]
        order = np.argsort(z_seg)

        # count local inversions in X
        x_seg = X[t:t + window]
        xs = x_seg[order]

        inv = np.where(np.diff(np.sign(np.diff(xs))) != 0)[0]
        for k in inv:
            crossings_t.append(t + k)
            crossings_rank.append(k)

    return np.array(crossings_t), np.array(crossings_rank)


# ------------------------------------------------------------
# PLOTS
# ------------------------------------------------------------
def plot_hopf_fibers(X, Y, Z, modes):
    colors = np.array(["blue", "red", "green", "orange"])

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    for mode in range(4):
        idx = np.where(modes == mode)[0]
        if len(idx) == 0:
            continue
        ax.plot(X[idx], Y[idx], Z[idx], color=colors[mode], label=f"mode {mode}", linewidth=2)

    ax.set_title("NEXAH v6.5 — Hopf Fibers")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_fiber_classes(X, Y, Z, modes, classified):
    label_color = {
        "outer_arc": "blue",
        "inner_loop": "orange",
        "transition_fiber": "red",
    }

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    for row in classified:
        mode = row["mode"]
        idx = np.where(modes == mode)[0]
        if len(idx) == 0:
            continue

        ax.plot(
            X[idx], Y[idx], Z[idx],
            color=label_color[row["label"]],
            linewidth=2,
            label=f"mode {mode} → {row['label']}"
        )

    ax.set_title("Fiber Classes")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    handles, labels = ax.get_legend_handles_labels()
    uniq = dict(zip(labels, handles))
    ax.legend(uniq.values(), uniq.keys(), fontsize=8)

    plt.tight_layout()
    plt.show()


def plot_separatrix_map(X, Y, Z, sep_idx):
    plt.figure(figsize=(7, 6))
    plt.scatter(X, Y, s=3, alpha=0.15, label="trajectory cloud")
    if len(sep_idx) > 0:
        plt.scatter(X[sep_idx], Y[sep_idx], c="gold", s=16, label="separatrix")
    plt.axvline(0, color="black", linewidth=1)
    plt.title("Separatrix Map (XY projection)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_braid_crossings(cross_t, cross_rank):
    plt.figure(figsize=(8, 4))
    if len(cross_t) > 0:
        plt.scatter(cross_t, cross_rank, c="red", s=18, label="crossings")
    plt.title("Braid Crossings")
    plt.xlabel("time")
    plt.ylabel("ring index")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_return_map(X, Y):
    # use radius as scalar observable
    r = np.sqrt(X**2 + Y**2)
    r = (r - r.min()) / (r.max() - r.min() + 1e-9)

    u_n = r[:-1]
    u_n1 = r[1:]

    plt.figure(figsize=(6, 5))
    plt.scatter(u_n, u_n1, s=6, alpha=0.4, label="return map")
    xx = np.linspace(0, 1, 400)
    yy = (2 * xx) % 1
    plt.plot(xx, yy, color="red", linewidth=1.5, label="ideal (2u) mod 1")
    plt.xlabel("u_n")
    plt.ylabel("u_n+1")
    plt.title("Return Map vs Doubling Map")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":
    traj = generate_dummy_traj()
    print("Trajectory size:", len(traj))

    X, Y, Z, modes, energies = build_hopf_arrays(traj)

    features = extract_fiber_features(X, Y, Z, modes)
    classified = classify_fibers(features)

    print("\n=== Fiber Features ===")
    for f in features:
        print(
            f"mode {f['mode']}: "
            f"major={f['major_turns']:.4f}, "
            f"minor={f['minor_turns']:.4f}, "
            f"mean=({f['mean_x']:.3f},{f['mean_y']:.3f},{f['mean_z']:.3f})"
        )

    print("\n=== Fiber Classes ===")
    for row in classified:
        print(f"mode {row['mode']}: {row['label']}")

    sep_idx = detect_separatrix_points(X, Y, Z)
    print(f"\nSeparatrix points detected: {len(sep_idx)}")

    cross_t, cross_rank = detect_braid_crossings(X, Y, Z)
    print(f"Braid crossings detected: {len(cross_t)}")

    plot_hopf_fibers(X, Y, Z, modes)
    plot_fiber_classes(X, Y, Z, modes, classified)
    plot_separatrix_map(X, Y, Z, sep_idx)
    plot_braid_crossings(cross_t, cross_rank)
    plot_return_map(X, Y)
