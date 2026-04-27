# ============================================================
# 🧭 NEXAH — State Space Control (v9)
# Transition Activation + Graph Control
# ============================================================

import numpy as np

from nexah.navigation.transition_graph import (
    build_transition_graph,
    dominant_next_state,
)


# ------------------------------------------------------------
# SIGNAL (UNSTABLE REGIME)
# ------------------------------------------------------------

def generate_signal(n=500):
    t = np.linspace(0, 20, n)

    base = np.sin(t)
    high = 0.3 * np.sin(5 * t)

    # 🔥 NEW: slow drift
    drift = 0.4 * np.sin(0.2 * t)

    # 🔥 NEW: noise
    noise = 0.08 * np.random.randn(n)

    x = base + high + drift + noise
    return x


# ------------------------------------------------------------
# STATE SPACE
# ------------------------------------------------------------

def build_state_space(x):
    v = np.gradient(x)
    return np.stack([x, v], axis=1)


# ------------------------------------------------------------
# BASINS
# ------------------------------------------------------------

def assign_basins(x, levels=None):
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
# GRAPH-AWARE CONTROL
# ------------------------------------------------------------

def apply_graph_aware_control(
    x,
    risk,
    strength=0.08,
    threshold=0.75,
    levels=None,
):
    states = build_state_space(x)
    basins = assign_basins(x, levels)
    centers = compute_basin_centers(states, basins)

    graph = build_transition_graph(basins)

    x_ctrl = x.copy()
    events = []

    for t in range(2, len(x) - 1):

        if risk[t] < threshold:
            continue

        current_basin = int(basins[t])
        target_basin = dominant_next_state(graph, current_basin)

        if target_basin is None:
            continue

        if target_basin not in centers:
            continue

        # current state
        px = x_ctrl[t]
        pv = x_ctrl[t] - x_ctrl[t - 1]
        current_state = np.array([px, pv])

        target_state = centers[target_basin]

        delta = target_state - current_state

        # 🔥 stronger activation near transitions
        activation = 1.0 + 0.5 * risk[t]

        correction = strength * activation * delta[0]
        correction = np.clip(correction, -0.2, 0.2)

        dx = x_ctrl[t] - x_ctrl[t - 1]
        dx = np.clip(dx, -1.5, 1.5)

        new_dx = (1 - strength) * dx + correction

        x_ctrl[t + 1] = x_ctrl[t] + new_dx

        if current_basin != target_basin:
            events.append(
                {
                    "t": int(t),
                    "from": int(current_basin),
                    "to": int(target_basin),
                    "risk": float(risk[t]),
                    "correction": float(correction),
                }
            )

    return x_ctrl, basins, graph, events


# ------------------------------------------------------------
# DEMO
# ------------------------------------------------------------

def demo():
    import matplotlib.pyplot as plt

    x = generate_signal()

    flow = np.abs(np.gradient(x))
    accel = np.abs(np.gradient(flow))
    risk = flow * accel
    risk = (risk - np.min(risk)) / (np.max(risk) + 1e-8)

    x_ctrl, basins, graph, events = apply_graph_aware_control(
        x,
        risk,
        strength=0.1,
        threshold=0.7,
    )

    peaks = np.where(risk > 0.7)[0]

    plt.figure(figsize=(12, 5))
    plt.plot(x, label="Original", alpha=0.6)
    plt.plot(x_ctrl, "--", label="Controlled v9")

    plt.scatter(peaks, x[peaks], color="red", s=20, label="High Risk")

    for e in events:
        plt.axvline(e["t"], color="gray", alpha=0.08)

    plt.title(f"NEXAH v9 — Activated Transitions | events={len(events)}")
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\n--- Transition Graph ---")
    for source, targets in graph.items():
        for target, data in targets.items():
            print(
                f"{source} -> {target} | "
                f"count={data['count']} | "
                f"P={data['probability']:.3f}"
            )

    print("\n--- Events ---")
    for e in events[:30]:
        print(e)


if __name__ == "__main__":
    demo()
