# ============================================================
# RUN 025 — EVENT SEQUENCE MODEL
# ============================================================

import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Load previous results (run_024)
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "outputs" / "run_024_rotation_vs_region_map" / "results.json"
OUT_DIR = BASE_DIR / "outputs" / "run_025_event_sequence"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

events = data["events"]
t_transition = data["t_transition"]
t_collapse = data["t_collapse"]


# ------------------------------------------------------------
# Phase classification
# ------------------------------------------------------------

def classify_phase(event_time):
    if t_transition is None:
        return "stable"

    if event_time < t_transition:
        return "pre-transition"

    elif t_transition <= event_time < t_collapse:
        return "transition"

    else:
        return "collapse"


# ------------------------------------------------------------
# Build sequence
# ------------------------------------------------------------

sequence = []

for ev in events:
    phase = classify_phase(ev["time"])

    sequence.append({
        "time": ev["time"],
        "rotation": ev["rotation"],
        "phase": phase
    })


# ------------------------------------------------------------
# Transition graph (counts)
# ------------------------------------------------------------

transition_counts = {}

for i in range(len(sequence) - 1):
    a = sequence[i]["phase"]
    b = sequence[i + 1]["phase"]

    key = (a, b)
    transition_counts[key] = transition_counts.get(key, 0) + 1


# ------------------------------------------------------------
# Print results
# ------------------------------------------------------------

print("\n=== RUN 025 — EVENT SEQUENCE MODEL ===\n")

print("Event sequence:")
for s in sequence:
    print(f"t={s['time']:.2f} → {s['phase']} (rot={s['rotation']:.3f})")

print("\nPhase transitions:")
for k, v in transition_counts.items():
    print(f"{k[0]} → {k[1]} : {v}")


# ------------------------------------------------------------
# Visualization
# ------------------------------------------------------------

times = [s["time"] for s in sequence]
phases = [s["phase"] for s in sequence]

phase_to_y = {
    "pre-transition": 0,
    "transition": 1,
    "collapse": 2,
}

y = [phase_to_y[p] for p in phases]

plt.figure(figsize=(10, 4))
plt.scatter(times, y, s=100)

for i, txt in enumerate(phases):
    plt.text(times[i], y[i] + 0.05, txt, ha='center', fontsize=8)

plt.yticks([0, 1, 2], ["pre-transition", "transition", "collapse"])
plt.xlabel("Time")
plt.title("Event Sequence Model")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(OUT_DIR / "figure_01_event_sequence.png", dpi=150)
plt.close()


# ------------------------------------------------------------
# Save results
# ------------------------------------------------------------

results = {
    "sequence": sequence,
    "transition_counts": {
        f"{k[0]}->{k[1]}": v for k, v in transition_counts.items()
    },
    "interpretation": (
        "Rotation events are mapped into a temporal phase sequence. "
        "This reveals how the system transitions between pre-transition, "
        "transition, and collapse phases."
    ),
}

with open(OUT_DIR / "results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nSaved to: {OUT_DIR}")
