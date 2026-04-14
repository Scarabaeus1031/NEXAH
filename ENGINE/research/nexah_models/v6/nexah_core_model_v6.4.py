# ============================================================
# NEXAH v6.4 — Torus Projection + Winding Numbers
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
# Replace this later with your real traj
# Format: (v, dv, mode, energy)
# ------------------------------------------------------------
def generate_dummy_traj(n=4000):
    traj = []

    for t in range(n):
        tt = t * 0.02

        # quasi-periodic style signal
        v = 0.78 + 0.15 * np.sin(tt) + 0.05 * np.sin(3.0 * tt + 0.4)
        dv = 0.03 * np.cos(tt) + 0.015 * np.cos(3.0 * tt + 0.4)

        mode = (t // 300) % 4
        energy = dv**2 + 0.1 * (v - 0.85)**2

        traj.append((v, dv, mode, energy))

    return traj


# ------------------------------------------------------------
# Build Hopf trajectory arrays
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
# theta_major: global angle around main center
# theta_minor: local angle around the tube
# ------------------------------------------------------------
def compute_torus_angles(X, Y, Z):
    # major circle center in XY-plane
    cx = np.mean(X)
    cy = np.mean(Y)

    theta_major = np.unwrap(np.arctan2(Y - cy, X - cx))

    # estimate major radius
    r_major = np.sqrt((X - cx)**2 + (Y - cy)**2)
    R0 = np.mean(r_major)

    # local tube coordinates
    tube_x = r_major - R0
    tube_y = Z - np.mean(Z)

    theta_minor = np.unwrap(np.arctan2(tube_y, tube_x))

    return theta_major, theta_minor, cx, cy, R0


# ------------------------------------------------------------
# Winding numbers
# ------------------------------------------------------------
def compute_winding_numbers(theta_major, theta_minor):
    major_turns = (theta_major[-1] - theta_major[0]) / (2 * np.pi)
    minor_turns = (theta_minor[-1] - theta_minor[0]) / (2 * np.pi)

    if abs(major_turns) > 1e-9:
        winding_ratio = minor_turns / major_turns
    else:
        winding_ratio = np.nan

    return major_turns, minor_turns, winding_ratio


# ------------------------------------------------------------
# Per-mode winding numbers
# ------------------------------------------------------------
def compute_mode_winding(X, Y, Z, modes):
    results = {}

    for mode in range(4):
        idx = np.where(modes == mode)[0]
        if len(idx) < 20:
            continue

        Xm = X[idx]
        Ym = Y[idx]
        Zm = Z[idx]

        theta_major, theta_minor, _, _, _ = compute_torus_angles(Xm, Ym, Zm)
        major_turns, minor_turns, winding_ratio = compute_winding_numbers(
            theta_major, theta_minor
        )

        results[mode] = {
            "major_turns": major_turns,
            "minor_turns": minor_turns,
            "ratio": winding_ratio,
        }

    return results


# ------------------------------------------------------------
# Torus embedding from angles
# ------------------------------------------------------------
def torus_embed(theta_major, theta_minor, R=2.0, r=0.65):
    X = (R + r * np.cos(theta_minor)) * np.cos(theta_major)
    Y = (R + r * np.cos(theta_minor)) * np.sin(theta_major)
    Z = r * np.sin(theta_minor)
    return X, Y, Z


# ------------------------------------------------------------
# Plot 1: Original Hopf 3D
# ------------------------------------------------------------
def plot_hopf_3d(X, Y, Z, modes):
    colors = np.array(["blue", "red", "green", "orange"])
    c = colors[modes]

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    for mode in range(4):
        idx = np.where(modes == mode)[0]
        if len(idx) == 0:
            continue
        ax.plot(X[idx], Y[idx], Z[idx], color=colors[mode], label=f"mode {mode}", linewidth=2)

    ax.set_title("NEXAH v6.4 — Hopf Fibers")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Plot 2: Angle space
# ------------------------------------------------------------
def plot_angle_space(theta_major, theta_minor):
    plt.figure(figsize=(7, 5))
    plt.plot(theta_major, theta_minor, linewidth=1.5)
    plt.xlabel("theta_major")
    plt.ylabel("theta_minor")
    plt.title("NEXAH v6.4 — Angle Space")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Plot 3: Torus projection in 3D
# ------------------------------------------------------------
def plot_torus_projection(theta_major, theta_minor):
    Xt, Yt, Zt = torus_embed(theta_major, theta_minor)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(Xt, Yt, Zt, linewidth=2)

    ax.set_title("NEXAH v6.4 — Torus Projection")
    ax.set_xlabel("X_torus")
    ax.set_ylabel("Y_torus")
    ax.set_zlabel("Z_torus")
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Plot 4: Mode-colored torus projection
# ------------------------------------------------------------
def plot_torus_modes(theta_major, theta_minor, modes):
    Xt, Yt, Zt = torus_embed(theta_major, theta_minor)
    colors = np.array(["blue", "red", "green", "orange"])

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    for mode in range(4):
        idx = np.where(modes == mode)[0]
        if len(idx) == 0:
            continue
        ax.plot(Xt[idx], Yt[idx], Zt[idx], color=colors[mode], label=f"mode {mode}", linewidth=2)

    ax.set_title("NEXAH v6.4 — Mode Fibers on Torus")
    ax.set_xlabel("X_torus")
    ax.set_ylabel("Y_torus")
    ax.set_zlabel("Z_torus")
    ax.legend()
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Plot 5: Winding bar chart
# ------------------------------------------------------------
def plot_winding_bars(mode_results):
    modes = sorted(mode_results.keys())
    major_vals = [mode_results[m]["major_turns"] for m in modes]
    minor_vals = [mode_results[m]["minor_turns"] for m in modes]

    x = np.arange(len(modes))
    w = 0.35

    plt.figure(figsize=(7, 4))
    plt.bar(x - w/2, major_vals, width=w, label="major")
    plt.bar(x + w/2, minor_vals, width=w, label="minor")
    plt.xticks(x, [f"mode {m}" for m in modes])
    plt.ylabel("turns")
    plt.title("NEXAH v6.4 — Winding Numbers per Mode")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
if __name__ == "__main__":
    # Replace this with your real trajectory later
    traj = generate_dummy_traj()

    print("Trajectory size:", len(traj))

    X, Y, Z, modes, energies = build_hopf_arrays(traj)

    theta_major, theta_minor, cx, cy, R0 = compute_torus_angles(X, Y, Z)
    major_turns, minor_turns, winding_ratio = compute_winding_numbers(theta_major, theta_minor)

    print("\n=== Global Torus Analysis ===")
    print(f"major turns: {major_turns:.4f}")
    print(f"minor turns: {minor_turns:.4f}")
    print(f"winding ratio minor/major: {winding_ratio:.4f}")
    print(f"estimated center: ({cx:.4f}, {cy:.4f})")
    print(f"estimated major radius: {R0:.4f}")

    mode_results = compute_mode_winding(X, Y, Z, modes)

    print("\n=== Per-Mode Winding ===")
    for mode in sorted(mode_results.keys()):
        r = mode_results[mode]
        print(
            f"mode {mode}: "
            f"major={r['major_turns']:.4f}, "
            f"minor={r['minor_turns']:.4f}, "
            f"ratio={r['ratio']:.4f}"
        )

    plot_hopf_3d(X, Y, Z, modes)
    plot_angle_space(theta_major, theta_minor)
    plot_torus_projection(theta_major, theta_minor)
    plot_torus_modes(theta_major, theta_minor, modes)
    plot_winding_bars(mode_results)
