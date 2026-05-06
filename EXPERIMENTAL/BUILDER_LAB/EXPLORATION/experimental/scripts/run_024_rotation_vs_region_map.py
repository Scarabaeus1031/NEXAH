# ============================================================
# RUN 024 — ROTATION EVENTS VS REGION MAP
# ============================================================

import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "outputs" / "run_024_rotation_vs_region_map"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Synthetic scenario
# ------------------------------------------------------------

def make_scenario(n=500):
    t = np.linspace(0, 100, n)

    V = 1.0 - 0.002 * t - 0.0005 * t**2
    V += 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
    V += 0.01 * np.sin(0.8 * t) * (t < 25)

    return t, V


# ------------------------------------------------------------
# State reconstruction
# ------------------------------------------------------------

def compute_state(t, V, sigma=2):
    V_s = gaussian_filter1d(V, sigma=sigma)
    dV = gaussian_filter1d(np.gradient(V_s, t), sigma=sigma)
    ddV = gaussian_filter1d(np.gradient(dV, t), sigma=sigma)

    x3 = np.vstack([V_s, dV, ddV]).T
    x2 = np.vstack([V_s, dV]).T

    curvature = gaussian_filter1d(
        np.linalg.norm(np.gradient(np.gradient(x3, axis=0), axis=0), axis=1),
        sigma=sigma,
    )

    drift = np.linalg.norm(np.diff(x3, axis=0), axis=1)
    drift = np.concatenate([[0.0], drift])
    drift = gaussian_filter1d(drift, sigma=sigma)

    return V_s, dV, ddV, x2, x3, curvature, drift


# ------------------------------------------------------------
# Region classification
# ------------------------------------------------------------

def classify_regions(V_s, curvature, drift):
    stable_idx = int(0.30 * len(V_s))

    kappa_th = np.mean(curvature[:stable_idx]) + 2.0 * np.std(curvature[:stable_idx])
    drift_th = np.mean(drift[:stable_idx]) + 2.0 * np.std(drift[:stable_idx])

    regions = np.full(len(V_s), "stable", dtype=object)
    regions[(curvature > kappa_th) | (drift > drift_th)] = "transition"
    regions[V_s < 0.7] = "collapse"

    return regions, kappa_th, drift_th


# ------------------------------------------------------------
# Rotation metric
# ------------------------------------------------------------

def rotation_metric(x2):
    dx = np.gradient(x2, axis=0)

    angles = []

    for i in range(1, len(dx)):
        v1 = dx[i - 1]
        v2 = dx[i]

        norm = (np.linalg.norm(v1) * np.linalg.norm(v2)) + 1e-8
        cos_theta = np.dot(v1, v2) / norm
        cos_theta = np.clip(cos_theta, -1.0, 1.0)

        angles.append(np.arccos(cos_theta))

    return np.array([0.0] + angles)


# ------------------------------------------------------------
# Helper
# ------------------------------------------------------------

def sustained_first_crossing(mask, t, min_samples=3):
    mask = np.asarray(mask, dtype=bool)

    for i in range(0, len(mask) - min_samples + 1):
        if np.all(mask[i:i + min_samples]):
            return float(t[i])

    return None


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

if __name__ == "__main__":
    print("\n=== RUN 024 — ROTATION EVENTS VS REGION MAP ===\n")

    t, V = make_scenario()

    V_s, dV, ddV, x2, x3, curvature, drift = compute_state(t, V)
    regions, kappa_th, drift_th = classify_regions(V_s, curvature, drift)

    rotation = rotation_metric(x2)

    peaks, props = find_peaks(
        rotation,
        height=0.2,
        distance=5,
    )

    t_transition = sustained_first_crossing(regions == "transition", t)
    t_collapse = sustained_first_crossing(V_s < 0.7, t)

    event_rows = []

    for idx in peaks:
        event_rows.append({
            "index": int(idx),
            "time": float(t[idx]),
            "rotation": float(rotation[idx]),
            "region": str(regions[idx]),
            "V": float(V_s[idx]),
            "dV": float(dV[idx]),
            "ddV": float(ddV[idx]),
        })

    print("Rotation events:", len(peaks))
    print("Event times:", t[peaks])
    print("Event regions:", [regions[p] for p in peaks])
    print("Transition start:", t_transition)
    print("Collapse:", t_collapse)

    # --------------------------------------------------------
    # Figure 1 — timeline with regions + events
    # --------------------------------------------------------

    plt.figure(figsize=(12, 5))

    plt.plot(t, rotation, color="blue", label="rotation signal")
    plt.scatter(t[peaks], rotation[peaks], color="red", s=60, label="rotation events")

    for i in range(len(t) - 1):
        if regions[i] == "transition":
            plt.axvspan(t[i], t[i + 1], color="orange", alpha=0.12)
        elif regions[i] == "collapse":
            plt.axvspan(t[i], t[i + 1], color="red", alpha=0.08)

    if t_transition is not None:
        plt.axvline(t_transition, color="orange", linestyle="--", label="transition start")

    if t_collapse is not None:
        plt.axvline(t_collapse, color="black", linestyle="-", linewidth=2, label="collapse")

    plt.title("Rotation Events vs Region Timeline")
    plt.xlabel("Time")
    plt.ylabel("Rotation")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_01_rotation_region_timeline.png", dpi=150)
    plt.close()

    # --------------------------------------------------------
    # Figure 2 — state map with regions + rotation events
    # --------------------------------------------------------

    color_map = {
        "stable": "tab:blue",
        "transition": "tab:orange",
        "collapse": "tab:red",
    }

    colors = [color_map[r] for r in regions]

    plt.figure(figsize=(8, 6))

    plt.scatter(V_s, dV, c=colors, s=22, alpha=0.65)
    plt.plot(V_s, dV, color="black", alpha=0.25, linewidth=1)

    plt.scatter(
        V_s[peaks],
        dV[peaks],
        color="black",
        edgecolor="yellow",
        s=90,
        label="rotation events",
        zorder=5,
    )

    for label, color in color_map.items():
        plt.scatter([], [], c=color, label=label)

    plt.title("Rotation Events on State Region Map")
    plt.xlabel("Voltage V(t)")
    plt.ylabel("dV/dt")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_02_rotation_events_state_map.png", dpi=150)
    plt.close()

    # --------------------------------------------------------
    # Figure 3 — zoom transition window
    # --------------------------------------------------------

    plt.figure(figsize=(12, 5))

    mask = (t >= 18) & (t <= 30)

    plt.plot(t[mask], rotation[mask], color="blue", label="rotation signal")

    zoom_peaks = [p for p in peaks if 18 <= t[p] <= 30]

    plt.scatter(
        t[zoom_peaks],
        rotation[zoom_peaks],
        color="red",
        s=70,
        label="rotation events",
    )

    for i in range(len(t) - 1):
        if not (18 <= t[i] <= 30):
            continue

        if regions[i] == "transition":
            plt.axvspan(t[i], t[i + 1], color="orange", alpha=0.14)
        elif regions[i] == "collapse":
            plt.axvspan(t[i], t[i + 1], color="red", alpha=0.10)

    if t_transition is not None:
        plt.axvline(t_transition, color="orange", linestyle="--", label="transition start")

    if t_collapse is not None:
        plt.axvline(t_collapse, color="black", linewidth=2, label="collapse")

    plt.title("Rotation Events around Transition / Collapse")
    plt.xlabel("Time")
    plt.ylabel("Rotation")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_03_transition_zoom.png", dpi=150)
    plt.close()

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    results = {
        "num_rotation_events": int(len(peaks)),
        "event_times": [float(t[p]) for p in peaks],
        "event_regions": [str(regions[p]) for p in peaks],
        "t_transition": t_transition,
        "t_collapse": t_collapse,
        "thresholds": {
            "kappa": float(kappa_th),
            "drift": float(drift_th),
        },
        "events": event_rows,
        "interpretation": (
            "Rotation events are mapped against stable, transition, and collapse regions. "
            "This tests whether directional changes cluster around the transition region."
        ),
    }

    with open(OUT_DIR / "results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved to: {OUT_DIR}")
