# ============================================================
# 🧭 NEXAH v20 — Multi-Layer State Representation
# ============================================================
#
# Purpose:
# Combine the three currently meaningful layers:
#
#   1. Basin      → discrete state position
#   2. Direction  → local motion direction (-1, 0, +1)
#   3. Jump       → whether the system changes basin next step
#
# Optional:
#   residue encoding mod k for symbolic / ring analysis
#
# ============================================================

import numpy as np

from nexah.navigation.state_space_control import (
    generate_signal,
    compute_risk,
    compute_adaptive_levels,
    assign_basins,
)


# ------------------------------------------------------------
# BUILD MULTI-LAYER STATE
# ------------------------------------------------------------

def build_multilayer_state(
    n=500,
    n_basins=10,
    residue_mod=17,
):
    x = generate_signal(n=n)
    risk = compute_risk(x)

    dx = np.gradient(x)

    levels = compute_adaptive_levels(x, n_basins=n_basins)
    basins = assign_basins(x, levels)

    records = []

    for t in range(len(basins) - 1):
        basin = int(basins[t])
        next_basin = int(basins[t + 1])

        direction = int(np.sign(dx[t]))
        jump = int(next_basin != basin)
        delta = int(next_basin - basin)

        residue = int((basin + residue_mod) % residue_mod)

        records.append(
            {
                "t": int(t),
                "x": float(x[t]),
                "risk": float(risk[t]),
                "basin": basin,
                "next_basin": next_basin,
                "direction": direction,
                "delta": delta,
                "jump": jump,
                "residue_mod": residue_mod,
                "residue": residue,
            }
        )

    return records, levels


# ------------------------------------------------------------
# SUMMARY BY BASIN + DIRECTION
# ------------------------------------------------------------

def summarize_layers(records):
    stats = {}

    for r in records:
        key = (r["basin"], r["direction"])

        if key not in stats:
            stats[key] = {
                "count": 0,
                "jumps": 0,
                "delta_sum": 0,
                "risk_sum": 0.0,
            }

        stats[key]["count"] += 1
        stats[key]["jumps"] += r["jump"]
        stats[key]["delta_sum"] += r["delta"]
        stats[key]["risk_sum"] += r["risk"]

    summary = []

    for (basin, direction), data in sorted(stats.items()):
        count = data["count"]

        if count == 0:
            continue

        summary.append(
            {
                "basin": basin,
                "direction": direction,
                "count": count,
                "jump_prob": data["jumps"] / count,
                "mean_delta": data["delta_sum"] / count,
                "mean_risk": data["risk_sum"] / count,
            }
        )

    return summary


# ------------------------------------------------------------
# RESIDUE ANALYSIS
# ------------------------------------------------------------

def summarize_residue(records):
    stats = {}

    for r in records:
        key = r["residue"]

        if key not in stats:
            stats[key] = {
                "count": 0,
                "jumps": 0,
                "risk_sum": 0.0,
                "delta_sum": 0,
            }

        stats[key]["count"] += 1
        stats[key]["jumps"] += r["jump"]
        stats[key]["risk_sum"] += r["risk"]
        stats[key]["delta_sum"] += r["delta"]

    summary = []

    for residue, data in sorted(stats.items()):
        count = data["count"]

        summary.append(
            {
                "residue": residue,
                "count": count,
                "jump_prob": data["jumps"] / count,
                "mean_delta": data["delta_sum"] / count,
                "mean_risk": data["risk_sum"] / count,
            }
        )

    return summary


# ------------------------------------------------------------
# PRINT HELPERS
# ------------------------------------------------------------

def print_layer_summary(summary, min_count=10):
    print("\n--- Multi-Layer Summary: basin + direction ---")

    for s in summary:
        if s["count"] < min_count:
            continue

        print(
            f"basin={s['basin']:>2} "
            f"dir={s['direction']:>2} "
            f"n={s['count']:>3} "
            f"jump={s['jump_prob']:.3f} "
            f"delta={s['mean_delta']:+.3f} "
            f"risk={s['mean_risk']:.3f}"
        )


def print_residue_summary(summary):
    print("\n--- Residue Summary ---")

    for s in summary:
        print(
            f"residue={s['residue']:>2} "
            f"n={s['count']:>3} "
            f"jump={s['jump_prob']:.3f} "
            f"delta={s['mean_delta']:+.3f} "
            f"risk={s['mean_risk']:.3f}"
        )


# ------------------------------------------------------------
# DEMO
# ------------------------------------------------------------

def demo():
    records, levels = build_multilayer_state(
        n=500,
        n_basins=10,
        residue_mod=17,
    )

    layer_summary = summarize_layers(records)
    residue_summary = summarize_residue(records)

    print("\n--- Adaptive Levels ---")
    print(levels)

    print("\n--- First 25 Multi-Layer Records ---")
    for r in records[:25]:
        print(r)

    print_layer_summary(layer_summary)
    print_residue_summary(residue_summary)

    print("\n--- Key Interpretation ---")
    print("Basin = position layer")
    print("Direction = local motion layer")
    print("Jump = transition layer")
    print("Residue = optional encoding layer, not yet evidence of dynamics")


if __name__ == "__main__":
    demo()
