# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/topology_evolution_tracker.py

import numpy as np


# --------------------------------------------------
# TRACKER CORE
# --------------------------------------------------

class TopologyEvolutionTracker:
    def __init__(self):
        self.history = []

    def add_step(self, level, signature, classification):
        """
        Store one timestep of topology evolution
        """
        entry = {
            "level": level,
            "signature": signature,
            "type": classification["type"],
            "confidence": classification["confidence"]
        }

        self.history.append(entry)

    def get_types_over_time(self):
        return [(h["level"], h["type"]) for h in self.history]

    def get_confidence_curve(self):
        return [(h["level"], h["confidence"]) for h in self.history]


# --------------------------------------------------
# EVOLUTION ANALYSIS
# --------------------------------------------------

def detect_transitions(history):
    """
    Detect changes in topology class
    """
    transitions = []

    for i in range(1, len(history)):
        prev = history[i - 1]
        curr = history[i]

        if prev["type"] != curr["type"]:
            transitions.append({
                "from": prev["type"],
                "to": curr["type"],
                "level": curr["level"]
            })

    return transitions


def detect_stable_phases(history, min_length=3):
    """
    Detect stable topology phases
    """
    phases = []
    current_type = None
    start_level = None
    length = 0

    for h in history:
        if h["type"] != current_type:
            if current_type is not None and length >= min_length:
                phases.append({
                    "type": current_type,
                    "start": start_level,
                    "end": prev_level
                })

            current_type = h["type"]
            start_level = h["level"]
            length = 1
        else:
            length += 1

        prev_level = h["level"]

    return phases


# --------------------------------------------------
# SIGNATURE EVOLUTION
# --------------------------------------------------

def track_metric(history, key):
    """
    Extract time series of a metric
    """
    series = []

    for h in history:
        if key in h["signature"]:
            series.append((h["level"], h["signature"][key]))

    return series


# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_evolution(history):
    import matplotlib.pyplot as plt

    levels = [h["level"] for h in history]
    confidences = [h["confidence"] for h in history]

    plt.figure(figsize=(10, 4))
    plt.plot(levels, confidences, marker="o")
    plt.title("Topology Confidence Over Time")
    plt.xlabel("Level")
    plt.ylabel("Confidence")
    plt.grid(True)
    plt.show()


# --------------------------------------------------
# SUMMARY REPORT
# --------------------------------------------------

def summarize_evolution(tracker):
    history = tracker.history

    print("\n--- TOPOLOGY EVOLUTION SUMMARY ---")

    # types
    print("\nTypes over time:")
    for h in history:
        print(f"Level {h['level']}: {h['type']}")

    # transitions
    transitions = detect_transitions(history)
    print("\nTransitions:")
    for t in transitions:
        print(f"Level {t['level']}: {t['from']} → {t['to']}")

    # phases
    phases = detect_stable_phases(history)
    print("\nStable Phases:")
    for p in phases:
        print(f"{p['type']} from Level {p['start']} to {p['end']}")


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":
    print("Topology Evolution Tracker Ready")
