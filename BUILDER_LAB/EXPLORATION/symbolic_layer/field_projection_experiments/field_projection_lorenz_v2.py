#!/usr/bin/env python3
"""
field_projection_lorenz_v2.py

NEXAH Field Projection Experiment V2 (cleaned)

Fixes:
- safe output path
- no overwrite of other experiments
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.decomposition import PCA
from scipy.signal import find_peaks


# =========================
# SETUP
# =========================

OUTPUT_DIR = Path(__file__).parent / "outputs" / "legacy" / "v2_lorenz"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
# FIELD COORDINATES
# =========================

def compute_field_coordinates(X):
    X_centered = X - np.mean(X, axis=0)

    pca = PCA(n_components=3)
    coords = pca.fit_transform(X_centered)

    alpha = coords[:, 0]
    beta = coords[:, 1]
    gamma = coords[:, 2]

    deviation = np.sqrt(beta**2 + gamma**2)

    return {
        "coords": coords,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "deviation": deviation,
        "explained_variance": pca.explained_variance_ratio_,
    }


# =========================
# PHASE + DRIFT
# =========================

def compute_phase(beta, gamma):
    theta = np.arctan2(gamma, beta)
    theta_unwrapped = np.unwrap(theta)
    dtheta = np.diff(theta_unwrapped, prepend=theta_unwrapped[0])
    return dtheta


# =========================
# REGIMES
# =========================

def classify_regimes(deviation, dtheta):
    D = deviation
    A = np.abs(dtheta)

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

    return regimes


def regime_colors(regimes):
    cmap = {
        "Theta": "cyan",
        "Tao": "orange",
        "Dao": "green",
        "Iota": "red",
    }
    return [cmap[r] for r in regimes]


# =========================
# EVENTS
# =========================

def detect_iota_events(dtheta):
    signal = np.abs(dtheta)
    threshold = np.percentile(signal, 90)

    peaks, _ = find_peaks(
        signal,
        prominence=threshold * 0.25,
        distance=20
    )

    return peaks


# =========================
# PLOTS
# =========================

def save_plot(fig, name):
    path = OUTPUT_DIR / name
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def plot_all(alpha, beta, gamma, deviation, dtheta, regimes, peaks):

    colors = regime_colors(regimes)

    # Alpha-Beta
    fig = plt.figure(figsize=(7,6))
    plt.scatter(alpha, beta, c=colors, s=4)
    plt.title("V2 Alpha-Beta")
    save_plot(fig, "v2_alpha_beta.png")

    # Drift
    fig = plt.figure(figsize=(10,3))
    plt.plot(np.abs(dtheta))
    plt.scatter(peaks, np.abs(dtheta)[peaks], c="red")
    plt.title("V2 Phase Drift")
    save_plot(fig, "v2_phase_drift.png")

    # Deviation
    fig = plt.figure(figsize=(10,3))
    plt.scatter(np.arange(len(deviation)), deviation, c=colors, s=3)
    plt.title("V2 Deviation")
    save_plot(fig, "v2_deviation.png")

    # 3D
    fig = plt.figure(figsize=(8,7))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(alpha, beta, gamma, c=colors, s=3)
    ax.set_title("V2 3D Projection")
    save_plot(fig, "v2_3d.png")


# =========================
# MAIN
# =========================

def main():
    print("Running V2 (clean)...")

    X = simulate_lorenz()
    field = compute_field_coordinates(X)

    dtheta = compute_phase(field["beta"], field["gamma"])
    regimes = classify_regimes(field["deviation"], dtheta)
    peaks = detect_iota_events(dtheta)

    plot_all(
        field["alpha"],
        field["beta"],
        field["gamma"],
        field["deviation"],
        dtheta,
        regimes,
        peaks
    )

    print("Done. Output:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
