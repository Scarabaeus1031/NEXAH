# ============================================================
# NEXAH v6.3b — Rotation Quantization (FULL SCRIPT)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt


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

    X = 2*(x1*x3 + x2*x4)
    Y = 2*(x2*x3 - x1*x4)
    Z = x1**2 + x2**2 - x3**2 - x4**2

    return X, Y, Z


# ------------------------------------------------------------
# Dummy Trajectory
# ------------------------------------------------------------
def generate_dummy_traj(n=2000):

    traj = []

    for t in range(n):
        v = 0.7 + 0.3*np.sin(t * 0.05)
        dv = 0.05*np.cos(t * 0.05)
        mode = (t // 200) % 4
        energy = dv**2

        traj.append((v, dv, mode, energy))

    return traj


# ------------------------------------------------------------
# Winkel berechnen
# ------------------------------------------------------------
def compute_angles(X, Y):
    return np.unwrap(np.arctan2(Y, X))


# ------------------------------------------------------------
# Rotation pro Mode messen
# ------------------------------------------------------------
def analyze_mode_rotation(traj):

    mode_data = {0: [], 1: [], 2: [], 3: []}

    for v, dv, mode, energy in traj:

        mode = int(mode) % 4

        X, Y, Z = hopf_projection(v, dv, mode, energy)
        mode_data[mode].append((X, Y, Z))

    results = {}

    for mode in range(4):

        data = mode_data[mode]

        if len(data) < 10:
            continue

        data = np.array(data)

        # 🔥 wichtig: Downsampling (sonst kann es hängen)
        step = max(1, len(data) // 500)
        data = data[::step]

        X = data[:, 0]
        Y = data[:, 1]

        angles = compute_angles(X, Y)

        total_rotation = angles[-1] - angles[0]
        rotations = total_rotation / (2 * np.pi)

        results[mode] = rotations

    return results


# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------
def plot_mode_rotations(results):

    if len(results) == 0:
        print("No data to plot")
        return

    modes = list(results.keys())
    values = [results[m] for m in modes]

    plt.figure(figsize=(6,4))
    plt.bar(modes, values)

    plt.xlabel("Mode")
    plt.ylabel("Rotations")
    plt.title("NEXAH v6.3b — Rotation per Mode")

    plt.grid(True)
    plt.show()


# ------------------------------------------------------------
# Quantization Check
# ------------------------------------------------------------
def check_quantization(results):

    print("\n=== Rotation Quantization Check ===")

    targets = [2, 3, 4, 6, 8, 12, 24, 36, 72]

    for mode, rot in results.items():

        closest = min(targets, key=lambda x: abs(x - abs(rot)))

        print(f"mode {mode}: {rot:.3f} rotations → closest ≈ {closest}")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":

    traj = generate_dummy_traj()

    print("Trajectory size:", len(traj))

    results = analyze_mode_rotation(traj)

    print("\nRaw results:")
    print(results)

    plot_mode_rotations(results)

    check_quantization(results)
