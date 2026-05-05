#!/usr/bin/env python3
"""
kuramoto_structure_visual_v2.py

NEXAH FIELD_LAYER — Kuramoto Structure Visual V2

Data-driven explanatory figure:
- phase diagram
- system response curves
- critical regime points
- final finding statement
"""

from pathlib import Path
import json
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline


BASE_DIR = Path(__file__).parent

SWEEP_CSV = BASE_DIR / "outputs" / "kuramoto_v6" / "master_runs" / "run_1777943097" / "sweep" / "sweep_results.csv"

OUTPUT_DIR = BASE_DIR / "outputs" / "kuramoto_structure_visuals"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    if not SWEEP_CSV.exists():
        raise FileNotFoundError(f"Missing sweep file: {SWEEP_CSV}")
    return pd.read_csv(SWEEP_CSV)


def extract_boundary(df, bins=20):
    r = df["r_mean"].values
    drift = df["abs_delta_theta_std"].values

    r_bins = np.linspace(r.min(), r.max(), bins)

    br, bd = [], []

    for i in range(len(r_bins) - 1):
        mask = (r >= r_bins[i]) & (r < r_bins[i + 1])
        if np.any(mask):
            br.append(r[mask].mean())
            bd.append(drift[mask].max())

    return np.array(br), np.array(bd)


def smooth_boundary(r, d):
    idx = np.argsort(r)
    r = r[idx]
    d = d[idx]

    spline = UnivariateSpline(r, d, s=0.001)
    r_s = np.linspace(r.min(), r.max(), 200)
    d_s = spline(r_s)

    return r_s, d_s


def regime_points(df):
    K = df["K"].values
    drift = df["abs_delta_theta_std"].values
    events = df["transition_rate"].values

    slope = np.gradient(drift) / np.gradient(K)

    onset_idx = int(np.argmax(slope))
    max_drift_idx = int(np.argmax(drift))
    max_events_idx = int(np.argmax(events))

    return {
        "onset": {
            "idx": onset_idx,
            "K": float(K[onset_idx]),
            "r_mean": float(df["r_mean"].iloc[onset_idx]),
            "drift": float(drift[onset_idx]),
            "slope": float(slope[onset_idx]),
        },
        "max_drift": {
            "idx": max_drift_idx,
            "K": float(K[max_drift_idx]),
            "r_mean": float(df["r_mean"].iloc[max_drift_idx]),
            "drift": float(drift[max_drift_idx]),
        },
        "max_events": {
            "idx": max_events_idx,
            "K": float(K[max_events_idx]),
            "r_mean": float(df["r_mean"].iloc[max_events_idx]),
            "event_rate": float(events[max_events_idx]),
            "drift": float(drift[max_events_idx]),
        },
    }


def mark_k(ax, point, label):
    ax.axvline(point["K"], linestyle="--", linewidth=1, alpha=0.5)
    ax.text(
        point["K"],
        ax.get_ylim()[1] * 0.92,
        label,
        rotation=90,
        va="top",
        ha="right",
        fontsize=8,
    )


def render(df):
    br, bd = extract_boundary(df)
    r_s, d_s = smooth_boundary(br, bd)
    pts = regime_points(df)

    fig = plt.figure(figsize=(16, 11))
    gs = fig.add_gridspec(3, 3, height_ratios=[1.2, 1.0, 0.8])

    fig.suptitle(
        "KURAMOTO FIELD STRUCTURE — SYNCHRONIZATION IS NOT STABILITY",
        fontsize=18,
        fontweight="bold",
    )

    # -------------------------
    # A — Phase diagram
    # -------------------------
    ax = fig.add_subplot(gs[0:2, 0:2])

    sc = ax.scatter(
        df["r_mean"],
        df["abs_delta_theta_std"],
        c=df["K"],
        cmap="viridis",
        s=85,
        edgecolors="black",
        linewidth=0.7,
        zorder=3,
    )

    ax.plot(r_s, d_s, color="red", linewidth=3, label="Phase Boundary", zorder=2)

    markers = [
        ("onset", "white", "Onset"),
        ("max_drift", "red", "Max Drift"),
        ("max_events", "blue", "Max Events"),
    ]

    for key, color, label in markers:
        p = pts[key]
        ax.scatter(
            p["r_mean"],
            p["drift"],
            s=150,
            color=color,
            edgecolors="black",
            linewidth=1.5,
            zorder=5,
            label=f"{label}: K≈{p['K']:.2f}",
        )

    ax.set_title("A. Phase Diagram: local slice of the field")
    ax.set_xlabel("Mean synchronization r")
    ax.set_ylabel("Phase drift std σ(Δθ)")
    ax.legend(loc="upper left", fontsize=9)
    plt.colorbar(sc, ax=ax, label="Coupling K")

    # -------------------------
    # B — Response curves
    # -------------------------
    ax1 = fig.add_subplot(gs[0, 2])
    ax1.plot(df["K"], df["r_mean"], marker="o")
    ax1.set_title("B1. Synchronization")
    ax1.set_xlabel("K")
    ax1.set_ylabel("r_mean")
    mark_k(ax1, pts["onset"], "onset")

    ax2 = fig.add_subplot(gs[1, 2])
    ax2.plot(df["K"], df["abs_delta_theta_std"], marker="o")
    ax2.set_title("B2. Internal Drift")
    ax2.set_xlabel("K")
    ax2.set_ylabel("σ(Δθ)")
    mark_k(ax2, pts["max_drift"], "max drift")

    # -------------------------
    # C — Events
    # -------------------------
    ax3 = fig.add_subplot(gs[2, 0])
    ax3.plot(df["K"], df["transition_rate"], marker="o")
    ax3.set_title("C. Event Activity")
    ax3.set_xlabel("K")
    ax3.set_ylabel("transition rate")
    mark_k(ax3, pts["max_events"], "max events")

    # -------------------------
    # D — Regime timeline
    # -------------------------
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.set_title("D. Multi-stage transition")
    ax4.set_xlim(df["K"].min(), df["K"].max())
    ax4.set_ylim(0, 1)
    ax4.set_yticks([])

    k_min = float(df["K"].min())
    k_max = float(df["K"].max())
    k_on = pts["onset"]["K"]
    k_drift = pts["max_drift"]["K"]
    k_events = pts["max_events"]["K"]

    ax4.axvspan(k_min, k_on, alpha=0.15)
    ax4.axvspan(k_on, k_drift, alpha=0.25)
    ax4.axvspan(k_drift, k_events, alpha=0.35)
    ax4.axvspan(k_events, k_max, alpha=0.20)

    ax4.text((k_min + k_on) / 2, 0.55, "organized\nsync", ha="center")
    ax4.text((k_on + k_drift) / 2, 0.55, "drift\nonset", ha="center")
    ax4.text((k_drift + k_events) / 2, 0.55, "max\ninstability", ha="center")
    ax4.text((k_events + k_max) / 2, 0.55, "transition\nactive", ha="center")

    ax4.set_xlabel("Coupling K")

    # -------------------------
    # E — Final statement
    # -------------------------
    ax5 = fig.add_subplot(gs[2, 2])
    ax5.axis("off")
    statement = (
        "Core finding\n\n"
        "Global synchronization rises monotonically,\n"
        "but internal drift and event activity peak later.\n\n"
        "Therefore:\n"
        "synchronization ≠ stability.\n\n"
        f"onset: K≈{pts['onset']['K']:.2f}\n"
        f"max drift: K≈{pts['max_drift']['K']:.2f}\n"
        f"max events: K≈{pts['max_events']['K']:.2f}"
    )
    ax5.text(
        0.02,
        0.98,
        statement,
        va="top",
        ha="left",
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.6", facecolor="white", edgecolor="black"),
    )

    fig.tight_layout(rect=[0, 0, 1, 0.95])

    timestamp = int(time.time())
    out_png = OUTPUT_DIR / f"kuramoto_field_structure_v2_{timestamp}.png"
    out_json = OUTPUT_DIR / f"kuramoto_field_structure_v2_{timestamp}.json"

    fig.savefig(out_png, dpi=220)
    plt.close(fig)

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(pts, f, indent=2)

    print(f"Saved figure → {out_png}")
    print(f"Saved regime points → {out_json}")


def main():
    df = load_data()
    render(df)


if __name__ == "__main__":
    main()
