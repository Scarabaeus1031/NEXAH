# field_projection_v2.py
# NEXAH Field Projection Experiment V2
#
# Goal:
# - simulate Lorenz dynamics
# - compute field-aligned coordinates via PCA
# - compute phase around dominant axis
# - compute phase drift
# - classify regimes: Theta / Tao / Dao / Iota
# - save visual outputs

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.signal import find_peaks


# =========================
# SETUP
# =========================

OUTPUT_DIR = "BUILDER_LAB/EXPLORATION/symbolic_layer/field_projection_experiments/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)


# =========================
# LORENZ SYSTEM
# =========================

def lorenz_step(x, y, z, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz


def simulate_lorenz(n_steps=5000, dt=0.01):
    X = np.zeros((n_steps, 3))

    x, y, z = 1.0, 1.0, 1.0

    for i in range(n_steps):
        dx, dy, dz = lorenz_step(x, y, z)

        x += dx * dt
        y += dy * dt
        z += dz * dt

        X[i] = [x, y, z]

    return X


# =========================
# FIELD-ALIGNED COORDINATES
# =========================

def compute_field_coordinates(X):
    """
    Compute PCA basis:
    e1 = dominant flow / FQ axis
    e2, e3 = deviation axes
    """

    X_centered = X - np.mean(X, axis=0)

    pca = PCA(n_components=3)
    coords = pca.fit_transform(X_centered)

    alpha = coords[:, 0]
    beta = coords[:, 1]
    gamma = coords[:, 2]

    deviation = np.sqrt(beta**2 + gamma**2)

    return {
        "X_centered": X_centered,
        "coords": coords,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "deviation": deviation,
        "components": pca.components_,
        "explained_variance": pca.explained_variance_ratio_,
    }


# =========================
# PHASE + DRIFT
# =========================

def compute_phase(beta, gamma):
    """
    Phase around dominant axis.
    Think of beta/gamma as the transverse plane around e1.
    """

    theta = np.arctan2(gamma, beta)
    theta_unwrapped = np.unwrap(theta)

    dtheta = np.diff(theta_unwrapped, prepend=theta_unwrapped[0])

    return theta, theta_unwrapped, dtheta


# =========================
# REGIME CLASSIFICATION
# =========================

def classify_regimes(deviation, dtheta):
    """
    Heuristic regime classification.

    Theta = low deviation + low phase drift
    Tao   = moderate drift / organized transition
    Dao   = high deviation / complex circulation
    Iota  = sharp phase drift / release event
    """

    D = deviation
    A = np.abs(dtheta)

    d_low = np.percentile(D, 45)
    d_high = np.percentile(D, 80)

    a_mid = np.percentile(A, 75)
    a_high = np.percentile(A, 92)

    regimes = np.empty(len(D), dtype=object)

    for i in range(len(D)):
        if A[i] >= a_high:
            regimes[i] = "Iota"
        elif D[i] >= d_high:
            regimes[i] = "Dao"
        elif A[i] >= a_mid:
            regimes[i] = "Tao"
        else:
            regimes[i] = "Theta"

    return regimes, {
        "d_low": d_low,
        "d_high": d_high,
        "a_mid": a_mid,
        "a_high": a_high,
    }


def regime_colors(regimes):
    color_map = {
        "Theta": "cyan",
        "Tao": "orange",
        "Dao": "green",
        "Iota": "red",
    }
    return [color_map[r] for r in regimes]


# =========================
# EVENT DETECTION
# =========================

def detect_iota_events(dtheta, prominence=0.2):
    signal = np.abs(dtheta)

    peaks, props = find_peaks(
        signal,
        prominence=prominence,
        distance=20
    )

    return peaks, props


# =========================
# VISUALIZATION
# =========================

def plot_alpha_beta(alpha, beta, regimes):
    colors = regime_colors(regimes)

    plt.figure(figsize=(8, 7))
    plt.scatter(alpha, beta, c=colors, s=4, alpha=0.65)

    plt.title("V2 Field Projection: Alpha vs Beta")
    plt.xlabel("alpha — flow axis")
    plt.ylabel("beta — deviation axis")

    out = os.path.join(OUTPUT_DIR, "v2_alpha_beta_regimes.png")
    plt.savefig(out, dpi=160)
    plt.close()

    return out


def plot_phase_drift(dtheta, peaks):
    plt.figure(figsize=(12, 4))
    plt.plot(np.abs(dtheta), linewidth=1.0, label="|dtheta| phase drift")

    if len(peaks) > 0:
        plt.scatter(peaks, np.abs(dtheta)[peaks], c="red", s=25, label="Iota events")

    plt.title("V2 Phase Drift + Iota Events")
    plt.xlabel("time")
    plt.ylabel("|dtheta|")
    plt.legend()

    out = os.path.join(OUTPUT_DIR, "v2_phase_drift_iota_events.png")
    plt.savefig(out, dpi=160)
    plt.close()

    return out


def plot_deviation(deviation, regimes):
    colors = regime_colors(regimes)

    plt.figure(figsize=(12, 4))
    plt.scatter(np.arange(len(deviation)), deviation, c=colors, s=3, alpha=0.7)

    plt.title("V2 Deviation D(t) with Regime Colors")
    plt.xlabel("time")
    plt.ylabel("D(t) = sqrt(beta^2 + gamma^2)")

    out = os.path.join(OUTPUT_DIR, "v2_deviation_regimes.png")
    plt.savefig(out, dpi=160)
    plt.close()

    return out


def plot_3d_projection(alpha, beta, gamma, regimes):
    colors = regime_colors(regimes)

    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(alpha, beta, gamma, c=colors, s=3, alpha=0.55)

    ax.set_title("V2 Field-Aligned Coordinates")
    ax.set_xlabel("alpha — flow")
    ax.set_ylabel("beta — deviation")
    ax.set_zlabel("gamma — deviation")

    out = os.path.join(OUTPUT_DIR, "v2_field_coordinates_3d.png")
    plt.savefig(out, dpi=160)
    plt.close()

    return out


# =========================
# MAIN
# =========================

def main():
    print("Running NEXAH Field Projection V2...")

    X = simulate_lorenz(n_steps=5000, dt=0.01)

    field = compute_field_coordinates(X)

    alpha = field["alpha"]
    beta = field["beta"]
    gamma = field["gamma"]
    deviation = field["deviation"]

    theta, theta_unwrapped, dtheta = compute_phase(beta, gamma)

    regimes, thresholds = classify_regimes(deviation, dtheta)

    peaks, props = detect_iota_events(dtheta, prominence=np.percentile(np.abs(dtheta), 90) * 0.25)

    # save plots
    files = []
    files.append(plot_alpha_beta(alpha, beta, regimes))
    files.append(plot_phase_drift(dtheta, peaks))
    files.append(plot_deviation(deviation, regimes))
    files.append(plot_3d_projection(alpha, beta, gamma, regimes))

    # metrics
    unique, counts = np.unique(regimes, return_counts=True)
    regime_counts = dict(zip(unique, counts))

    print("\n--- FIELD PROJECTION V2 RESULTS ---")
    print(f"Samples: {len(X)}")
    print(f"Iota events detected: {len(peaks)}")
    print(f"Mean deviation: {np.mean(deviation):.4f}")
    print(f"Max deviation: {np.max(deviation):.4f}")
    print(f"Mean |dtheta|: {np.mean(np.abs(dtheta)):.4f}")
    print(f"Max |dtheta|: {np.max(np.abs(dtheta)):.4f}")
    print(f"PCA explained variance: {field['explained_variance']}")

    print("\nRegime counts:")
    for k in ["Theta", "Tao", "Dao", "Iota"]:
        print(f"- {k}: {regime_counts.get(k, 0)}")

    print("\nThresholds:")
    for k, v in thresholds.items():
        print(f"- {k}: {v:.4f}")

    print("\nSaved outputs:")
    for f in files:
        print(f"- {f}")


if __name__ == "__main__":
    main()
