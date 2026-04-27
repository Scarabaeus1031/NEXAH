# ============================================================
# 🧭 NEXAH — State Space Control v6
# Basin-Level Switching Prototype
# ============================================================
#
# Goal:
# Controlled regime shifts ("step behavior") instead of only smoothing.
#
# Core idea:
# - build state space (x, dx/dt)
# - define basins from signal levels
# - detect high-risk points
# - push trajectory toward neighboring basin center
#
# Status:
# Prototype — first real "regime control"
#
# ============================================================

import numpy as np


# ------------------------------------------------------------
# STATE SPACE
# ------------------------------------------------------------

def build_state_space(x):
    v = np.gradient(x)
    return np.stack([x, v], axis=1)


# ------------------------------------------------------------
# BASINS
# ------------------------------------------------------------

def assign_basins_by_levels(x, levels=None):
    """
    Split signal into vertical regimes.
    """

    if levels is None:
        levels = [-0.6, 0.0, 0.6]

    return np.digitize(x, levels)


def compute_basin_centers(states, basins):
    centers = {}

    for b in np.unique(basins):
        pts = states[basins == b]

        if len(pts) > 0:
            centers[int(b)] = np.mean(pts, axis=0)

    return centers


# ------------------------------------------------------------
# CONTROL
# ------------------------------------------------------------

def choose_target_basin(current, centers, direction):
    keys = sorted(centers.keys())

    if current not in keys:
        return current

    idx = keys.index(current)
    target_idx = np.clip(idx + direction, 0, len(keys) - 1)

    return keys[target_idx]


def apply_basin_switch_control(
    x,
    risk,
    strength=0.08,
    threshold=0.8,
    levels=None,
    direction_policy="alternate"
):
    states = build_state_space(x)
    basins = assign_basins_by_levels(x, levels)
    centers = compute_basin_centers(states, basins)

    x_ctrl = x.copy()
    events = []

    last_direction = 1

    for t in range(2, len(x) - 1):

        if risk[t] < threshold:
            continue

        current = int(basins[t])

        # --- direction policy ---
        if direction_policy == "up":
            direction = 1
        elif direction_policy == "down":
            direction = -1
        else:
            direction = last_direction
            last_direction *= -1

        target = choose_target_basin(current, centers, direction)

        if target == current:
            continue

        # --- current state ---
        px = x_ctrl[t]
        pv = x_ctrl[t] - x_ctrl[t - 1]
        current_state = np.array([px, pv])

        target_state = centers[target]

        # --- movement toward basin center ---
        delta = target_state - current_state

        correction = strength * delta[0]
        correction = np.clip(correction, -0.12, 0.12)

        x_ctrl[t + 1] = x_ctrl[t] + correction

        events.append({
            "t": int(t),
            "from": current,
            "to": target,
            "risk": float(risk[t]),
            "corr": float(correction),
        })

    return x_ctrl, basins, events


# ------------------------------------------------------------
# DEMO
# ------------------------------------------------------------

def demo():
    import matplotlib.pyplot as plt

    n = 500
    t = np.linspace(0, 20, n)
    x = np.sin(t) + 0.3 * np.sin(5 * t)

    flow = np.abs(np.gradient(x))
    accel = np.abs(np.gradient(flow))
    risk = flow * accel
    risk = (risk - np.min(risk)) / (np.max(risk) + 1e-8)

    x_ctrl, basins, events = apply_basin_switch_control(
        x,
        risk,
        strength=0.08,
        threshold=0.8,
        direction_policy="alternate"
    )

    peaks = np.where(risk > 0.8)[0]

    plt.figure(figsize=(12, 5))
    plt.plot(x, label="Original", alpha=0.7)
    plt.plot(x_ctrl, "--", label="Controlled v6")

    plt.scatter(peaks, x[peaks], color="red", s=20, label="High Risk")

    for e in events:
        plt.axvline(e["t"], color="gray", alpha=0.15)

    plt.title(f"NEXAH v6 — Basin Switching | events={len(events)}")
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\n--- Events ---")
    for e in events[:20]:
        print(e)


if __name__ == "__main__":
    demo()
