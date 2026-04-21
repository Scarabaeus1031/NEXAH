# ============================================================
# NEXAH v6.8 — Symbol → Geometry Mapping
# ============================================================

import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Hopf Projection (same as before)
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

    X = 2*(x1*x3 + x2*x4)
    Y = 2*(x2*x3 - x1*x4)
    Z = x1**2 + x2**2 - x3**2 - x4**2

    return X, Y, Z


# ------------------------------------------------------------
# Dummy trajectory (replace with real later)
# ------------------------------------------------------------
def generate_dummy_traj(n=5000):

    traj = []

    for t in range(n):
        v = 0.7 + 0.2 * np.sin(t * 0.03)
        dv = 0.05 * np.cos(t * 0.03)

        mode = (t // 350) % 4
        energy = dv**2

        traj.append((v, dv, mode, energy))

    return traj


# ------------------------------------------------------------
# Build geometry per mode
# ------------------------------------------------------------
def extract_geometry(traj):

    mode_points = {0: [], 1: [], 2: [], 3: []}
    transitions = []

    for i in range(len(traj)):

        v, dv, mode, energy = traj[i]
        X, Y, Z = hopf_projection(v, dv, mode, energy)

        mode_points[mode].append((X, Y, Z))

        # detect transition
        if i > 0:
            prev_mode = traj[i-1][2]
            if mode != prev_mode:
                transitions.append((X, Y, Z, prev_mode, mode))

    return mode_points, transitions


# ------------------------------------------------------------
# Compute centers (orbit centers)
# ------------------------------------------------------------
def compute_centers(mode_points):

    centers = {}

    for mode in mode_points:
        data = np.array(mode_points[mode])

        if len(data) == 0:
            continue

        center = np.mean(data, axis=0)
        centers[mode] = center

    return centers


# ------------------------------------------------------------
# Plot everything
# ------------------------------------------------------------
def plot_symbol_geometry(mode_points, transitions, centers):

    colors = {
        0: "blue",
        1: "red",
        2: "green",
        3: "orange"
    }

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')

    # --------------------------------------------------------
    # Plot mode clouds (subsample for clarity)
    # --------------------------------------------------------
    for mode in mode_points:

        data = np.array(mode_points[mode])

        if len(data) == 0:
            continue

        # subsample
        data = data[::10]

        ax.scatter(
            data[:,0],
            data[:,1],
            data[:,2],
            color=colors[mode],
            s=5,
            alpha=0.5,
            label=f"mode {mode}"
        )

    # --------------------------------------------------------
    # Plot centers
    # --------------------------------------------------------
    for mode, c in centers.items():

        ax.scatter(
            c[0], c[1], c[2],
            color="black",
            s=80
        )

        ax.text(c[0], c[1], c[2], f"C{mode}", fontsize=10)

    # --------------------------------------------------------
    # Plot transitions (arrows)
    # --------------------------------------------------------
    for t in transitions[::5]:  # thin out

        X, Y, Z, m0, m1 = t

        ax.scatter(X, Y, Z, color="black", s=10)

    ax.set_title("NEXAH v6.8 — Symbol → Geometry Mapping")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.legend()
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":

    traj = generate_dummy_traj()

    print("Trajectory size:", len(traj))

    mode_points, transitions = extract_geometry(traj)

    centers = compute_centers(mode_points)

    print("\n=== Mode Centers ===")
    for m, c in centers.items():
        print(f"mode {m}: {c}")

    print(f"\nTransitions detected: {len(transitions)}")

    plot_symbol_geometry(mode_points, transitions, centers)
