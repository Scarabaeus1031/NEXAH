# ============================================================
# 🧭 NEXAH — State Space Control (v10.1)
# Adaptive Basin Graph Control + Transition Analysis
# ============================================================

import numpy as np

from nexah.navigation.transition_graph import (
    build_transition_graph,
    dominant_next_state,
)

from nexah.navigation.transition_analysis import analyze_transitions


# ------------------------------------------------------------
# SIGNAL
# ------------------------------------------------------------

def generate_signal(n=500, seed=42):
    rng = np.random.default_rng(seed)

    t = np.linspace(0, 20, n)

    base = np.sin(t)
    high = 0.3 * np.sin(5 * t)
    drift = 0.4 * np.sin(0.2 * t)
    noise = 0.08 * rng.normal(size=n)

    return base + high + drift + noise


# ------------------------------------------------------------
# STATE SPACE
# ------------------------------------------------------------

def build_state_space(x):
    v = np.gradient(x)
    return np.stack([x, v], axis=1)


# ------------------------------------------------------------
# RISK
# ------------------------------------------------------------

def compute_risk(x):
    flow = np.abs(np.gradient(x))
    accel = np.abs(np.gradient(flow))

    risk = flow * accel
    risk = (risk - np.min(risk)) / (np.max(risk) - np.min(risk) + 1e-8)

    return risk


# ------------------------------------------------------------
# ADAPTIVE BASINS
# ------------------------------------------------------------

def compute_adaptive_levels(x, n_basins=10, method="quantile"):

    if n_basins < 2:
        raise ValueError("n_basins must be >= 2")

    if method == "quantile":
        qs = np.linspace(0, 1, n_basins + 1)[1:-1]
        levels = np.quantile(x, qs)

    elif method == "linear":
        levels = np.linspace(np.min(x), np.max(x), n_basins + 1)[1:-1]

    else:
        raise ValueError("method must be 'quantile' or 'linear'")

    return levels


def assign_basins(x, levels):
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
    strength=0.06,
    threshold=0.65,
    n_basins=10,
    basin_method="quantile",
    allow_self=False,
):

    states = build_state_space(x)

    levels = compute_adaptive_levels(
        x,
        n_basins=n_basins,
        method=basin_method,
    )

    basins = assign_basins(x, levels)
    centers = compute_basin_centers(states, basins)
    graph = build_transition_graph(basins)

    x_ctrl = x.copy()
    events = []

    for t in range(2, len(x) - 1):

        if risk[t] < threshold:
            continue

        current = int(basins[t])
        target = dominant_next_state(graph, current)

        if target == current and not allow_self:
            candidates = graph.get(current, {})

            non_self = {
                k: v for k, v in candidates.items()
                if int(k) != current
            }

            if not non_self:
                continue

            target = max(
                non_self.items(),
                key=lambda item: (item[1]["probability"], item[1]["count"])
            )[0]

        if target is None or target not in centers:
            continue

        if target == current and not allow_self:
            continue

        px = x_ctrl[t]
        pv = x_ctrl[t] - x_ctrl[t - 1]

        current_state = np.array([px, pv])
        target_state = centers[target]

        delta = target_state - current_state

        activation = 1.0 + 0.5 * risk[t]

        correction = strength * activation * delta[0]
        correction = np.clip(correction, -0.15, 0.15)

        dx = x_ctrl[t] - x_ctrl[t - 1]
        dx = np.clip(dx, -1.2, 1.2)

        new_dx = (1 - strength) * dx + correction

        x_ctrl[t + 1] = x_ctrl[t] + new_dx

        events.append(
            {
                "t": int(t),
                "from": int(current),
                "to": int(target),
                "risk": float(risk[t]),
                "correction": float(correction),
            }
        )

    return x_ctrl, basins, graph, events, levels


# ------------------------------------------------------------
# DEMO
# ------------------------------------------------------------

def demo():
    import matplotlib.pyplot as plt

    x = generate_signal()
    risk = compute_risk(x)

    x_ctrl, basins, graph, events, levels = apply_graph_aware_control(
        x,
        risk,
        strength=0.06,
        threshold=0.65,
        n_basins=10,
        basin_method="quantile",
        allow_self=False,
    )

    peaks = np.where(risk > 0.65)[0]

    plt.figure(figsize=(12, 5))
    plt.plot(x, label="Original", alpha=0.6)
    plt.plot(x_ctrl, "--", label="Controlled v10.1")

    plt.scatter(peaks, x[peaks], color="red", s=18, label="High Risk")

    for level in levels:
        plt.axhline(level, color="gray", alpha=0.12, linewidth=1)

    for e in events:
        plt.axvline(e["t"], color="gray", alpha=0.06, linewidth=1)

    plt.title(f"NEXAH v10.1 — Adaptive Basin Control | events={len(events)}")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ------------------------
    # PRINT CORE OUTPUT
    # ------------------------

    print("\n--- Adaptive Levels ---")
    print(levels)

    print("\n--- Transition Graph ---")
    for source, targets in graph.items():
        for target, data in targets.items():
            print(
                f"{source} -> {target} | "
                f"count={data['count']} | "
                f"P={data['probability']:.3f}"
            )

    print("\n--- Events ---")
    for e in events[:40]:
        print(e)

    # ------------------------
    # 🔥 NEW: ANALYSIS
    # ------------------------

    analysis = analyze_transitions(basins, graph)

    print("\n--- Drift ---")
    print(analysis["drift"])

    print("\n--- Symmetry (first 10) ---")
    for s in analysis["symmetry"][:10]:
        print(s)

    print("\n--- Transition Distances (first 10) ---")
    for d in analysis["distances"][:10]:
        print(d)


if __name__ == "__main__":
    demo()
