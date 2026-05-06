"""
🧭 NEXAH — Field Control (Prototype)

This module introduces the FIRST active control mechanism
based on the NEXAH pipeline.

---

## 🧠 Core Idea

We do NOT control the system via:

    thresholds → triggers → actions

Instead:

    we slightly reshape the trajectory
    based on structural signals (risk)

---

## 🔬 Current Approach (v0)

We use a minimal proxy:

    risk(t) → ∇risk(t) → control direction

Meaning:

- if risk increases → push system away
- if risk decreases → allow motion

This is NOT yet true field control.

It is:

    a temporal approximation of structural steering

---

## ⚠️ Limitations

- operates in TIME domain (not true state-space gradient)
- no spatial awareness
- no basin / geometry awareness
- no multi-dimensional vector field steering

👉 This is a PROTOTYPE layer only

---

## 🚀 Purpose

This module exists to test:

    Can simple structural signals influence trajectory behavior?

---

## 🔄 Next Evolution (planned)

Replace:

    temporal gradient (∇risk(t))

with:

    spatial gradient (∇P(IOTA | x))

→ TRUE FIELD CONTROL

---

## 🧱 Mini Build Log

v0:
- introduced basic control via risk gradient
- first observable "trajectory deformation"
- identified hook/turning behavior (~90° shifts)
- confirmed: system reacts to minimal steering

---

## 📁 Location

nexah/navigation/field_control.py

---
"""

import numpy as np
import matplotlib.pyplot as plt

from nexah.field_layer.core.field import compute_field
from nexah.field_layer.core.metrics import (
    compute_flow_strength,
    compute_curvature,
)

# NEW
from nexah.navigation.field_control import apply_field_control


# ----------------------------
# Signal
# ----------------------------

def generate_signal(n=500):
    t = np.linspace(0, 20, n)
    x = np.sin(t) + 0.3 * np.sin(5 * t)
    return x


# ----------------------------
# CONTROL PIPELINE (v3)
# ----------------------------

def run_control_pipeline(control_strength=0.05):
    x = generate_signal()
    X = x.reshape(-1, 1)

    # --- FIELD ---
    F = compute_field(X)

    flow = compute_flow_strength(F)
    curvature = compute_curvature(F)

    min_len = min(len(flow), len(curvature))
    flow = flow[:min_len]
    curvature = curvature[:min_len]
    X = X[:min_len]

    # --- SIGNAL ---
    risk = flow * curvature
    risk = (risk - np.min(risk)) / (np.max(risk) + 1e-8)

    # ----------------------------
    # CONTROL (NEW: continuous)
    # ----------------------------

    X_controlled = apply_field_control(
        X,
        risk,
        strength=control_strength
    )

    x_controlled = X_controlled.flatten()

    return x[:min_len], x_controlled, risk


# ----------------------------
# PLOT
# ----------------------------

def plot_control():
    x, x_ctrl, risk = run_control_pipeline()

    plt.figure(figsize=(12, 5))

    plt.plot(x, label="Original", alpha=0.7)
    plt.plot(x_ctrl, label="Controlled", linestyle="--")

    # High-risk markieren
    threshold = 0.8
    peaks = np.where(risk > threshold)[0]

    plt.scatter(peaks, x[peaks], color="red", label="High Risk", s=20)

    plt.title("Field-Based Control (v3)")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_control()
