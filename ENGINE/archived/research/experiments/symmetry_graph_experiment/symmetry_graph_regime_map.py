"""
NEXAH Symmetry Graph Regime Map
-------------------------------

Scans a simple dual-hub oscillator system over:

- coupling strength K
- frequency mismatch dOmega

and classifies the resulting dynamics into rough regimes:

- LOCKED
- QUASI
- DRIFT

This is a first regime-map experiment for the symmetry graph idea.
It does not yet simulate all outer nodes as oscillators; it scans the
core dual-hub resonance structure that emerged from the previous tests.

Output:
- console summary
- regime map plot
"""

import math
import random
import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def wrap_angle(theta):
    return theta % (2 * math.pi)


def phase_distance(a, b):
    d = abs(a - b) % (2 * math.pi)
    return min(d, 2 * math.pi - d)


def sync_score(a, b):
    d = phase_distance(a, b)
    return 1.0 - (d / math.pi)


# --------------------------------------------------
# Dual-hub phase simulation
# --------------------------------------------------

def simulate_dual_hub(
    coupling,
    delta_omega,
    steps=800,
    dt=0.05,
    noise=0.01,
    omega_base=1.0
):
    """
    Two coupled phase oscillators with small noise.

    Returns
    -------
    mean_sync : float
    std_sync  : float
    mean_dphi : float
    std_dphi  : float
    """

    theta_a = random.uniform(0, 2 * math.pi)
    theta_b = random.uniform(0, 2 * math.pi)

    omega_a = omega_base
    omega_b = omega_base + delta_omega

    sync_values = []
    dphi_values = []

    for _ in range(steps):
        dphi = (theta_b - theta_a) % (2 * math.pi)
        if dphi > math.pi:
            dphi -= 2 * math.pi

        dtheta_a = omega_a + coupling * math.sin(dphi) + random.uniform(-noise, noise)
        dtheta_b = omega_b - coupling * math.sin(dphi) + random.uniform(-noise, noise)

        theta_a = wrap_angle(theta_a + dtheta_a * dt)
        theta_b = wrap_angle(theta_b + dtheta_b * dt)

        sync_values.append(sync_score(theta_a, theta_b))
        dphi_values.append(dphi)

    # ignore early transient
    cut = int(0.3 * steps)
    sync_tail = sync_values[cut:]
    dphi_tail = dphi_values[cut:]

    mean_sync = float(np.mean(sync_tail))
    std_sync = float(np.std(sync_tail))
    mean_dphi = float(np.mean(dphi_tail))
    std_dphi = float(np.std(dphi_tail))

    return mean_sync, std_sync, mean_dphi, std_dphi


# --------------------------------------------------
# Regime classification
# --------------------------------------------------

def classify_regime(mean_sync, std_sync, std_dphi):
    """
    Rough regime classifier.

    LOCKED:
        strong synchronization, low fluctuation

    QUASI:
        intermediate synchronization and/or moderate phase fluctuation

    DRIFT:
        weak synchronization, large fluctuation
    """

    if mean_sync > 0.92 and std_sync < 0.06 and std_dphi < 0.30:
        return "LOCKED"

    if mean_sync > 0.60:
        return "QUASI"

    return "DRIFT"


# --------------------------------------------------
# Scan parameter space
# --------------------------------------------------

def run_regime_scan(
    k_values,
    domega_values,
    repeats=3,
    steps=800,
    dt=0.05,
    noise=0.01
):
    """
    Scan (K, dOmega) parameter space and build a regime map.
    """

    regime_grid = np.zeros((len(domega_values), len(k_values)), dtype=int)

    # code:
    # 0 = DRIFT
    # 1 = QUASI
    # 2 = LOCKED
    label_to_code = {
        "DRIFT": 0,
        "QUASI": 1,
        "LOCKED": 2,
    }

    for i, domega in enumerate(domega_values):
        for j, k in enumerate(k_values):

            labels = []

            for _ in range(repeats):
                mean_sync, std_sync, _, std_dphi = simulate_dual_hub(
                    coupling=k,
                    delta_omega=domega,
                    steps=steps,
                    dt=dt,
                    noise=noise
                )

                label = classify_regime(mean_sync, std_sync, std_dphi)
                labels.append(label)

            # majority vote
            counts = {lab: labels.count(lab) for lab in set(labels)}
            final_label = max(counts, key=counts.get)

            regime_grid[i, j] = label_to_code[final_label]

    return regime_grid


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_regime_map(regime_grid, k_values, domega_values):
    plt.figure(figsize=(9, 6))

    plt.imshow(
        regime_grid,
        origin="lower",
        aspect="auto",
        extent=[k_values[0], k_values[-1], domega_values[0], domega_values[-1]]
    )

    cbar = plt.colorbar()
    cbar.set_ticks([0, 1, 2])
    cbar.set_ticklabels(["DRIFT", "QUASI", "LOCKED"])

    plt.title("Symmetry Graph Regime Map")
    plt.xlabel("Coupling K")
    plt.ylabel("Frequency Mismatch Δω")

    plt.tight_layout()
    plt.savefig("symmetry_graph_regime_map.png", dpi=300)
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":
    print("\nRunning Symmetry Graph Regime Map Scan...\n")

    k_values = np.linspace(0.00, 0.50, 30)
    domega_values = np.linspace(0.00, 0.25, 30)

    regime_grid = run_regime_scan(
        k_values=k_values,
        domega_values=domega_values,
        repeats=3,
        steps=800,
        dt=0.05,
        noise=0.01
    )

    locked_count = int(np.sum(regime_grid == 2))
    quasi_count = int(np.sum(regime_grid == 1))
    drift_count = int(np.sum(regime_grid == 0))

    total = regime_grid.size

    print("Grid points:", total)
    print("LOCKED:", locked_count)
    print("QUASI :", quasi_count)
    print("DRIFT :", drift_count)

    plot_regime_map(regime_grid, k_values, domega_values)
