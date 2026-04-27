# ============================================================
# 🧭 NEXAH v19 — Directional Transition Model
# ============================================================

import numpy as np

from nexah.navigation.state_space_control import (
    generate_signal,
    compute_risk,
    compute_adaptive_levels,
    assign_basins,
)


# ------------------------------------------------------------
# DATA
# ------------------------------------------------------------

def build_dataset(n=500, n_basins=10):
    x = generate_signal(n=n)
    risk = compute_risk(x)

    dx = np.gradient(x)

    levels = compute_adaptive_levels(x, n_basins=n_basins)
    basins = assign_basins(x, levels)

    records = []

    for t in range(len(basins) - 1):
        current = int(basins[t])
        next_state = int(basins[t + 1])

        direction = np.sign(dx[t])  # -1, 0, +1
        jump = int(next_state != current)

        records.append({
            "basin": current,
            "direction": int(direction),
            "risk": float(risk[t]),
            "jump": jump,
        })

    return records


# ------------------------------------------------------------
# ANALYSIS
# ------------------------------------------------------------

def analyze_directional_jumps(records):
    """
    Analyze jump probability conditioned on:
    basin + direction
    """

    stats = {}

    for r in records:
        key = (r["basin"], r["direction"])

        if key not in stats:
            stats[key] = {"count": 0, "jumps": 0}

        stats[key]["count"] += 1
        stats[key]["jumps"] += r["jump"]

    print("\n--- Directional Jump Probabilities ---")

    for key, data in sorted(stats.items()):
        basin, direction = key

        if data["count"] < 10:
            continue

        p = data["jumps"] / data["count"]

        print(
            f"basin={basin} dir={direction} "
            f"→ jump_prob={p:.3f} "
            f"(n={data['count']})"
        )


# ------------------------------------------------------------
# DEMO
# ------------------------------------------------------------

def demo():
    records = build_dataset()

    analyze_directional_jumps(records)


if __name__ == "__main__":
    demo()
