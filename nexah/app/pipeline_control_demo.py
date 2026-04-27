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


def apply_field_control(states, risk, strength=0.05):
    """
    Apply simple field-based control to a trajectory.

    Parameters
    ----------
    states : np.ndarray
        Shape (T, N) — system states

    risk : np.ndarray
        Shape (T,) — structural signal

    strength : float
        control intensity (small value recommended)

    Returns
    -------
    controlled_states : np.ndarray
        Modified trajectory
    """

    controlled = states.copy()

    # temporal gradient of risk
    grad = np.gradient(risk)

    for t in range(1, len(states)):
        # move away from increasing risk
        direction = -grad[t]

        # apply correction (same direction across dimensions)
        controlled[t] = controlled[t] + strength * direction

    return controlled


# ----------------------------------------
# Optional: debug helper
# ----------------------------------------

def compute_control_signal(risk):
    """
    Returns the raw control signal used internally.

    Useful for debugging / plotting.

    Returns
    -------
    signal : np.ndarray
    """
    return -np.gradient(risk)
