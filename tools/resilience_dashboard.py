# tools/resilience_dashboard.py

import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import matplotlib.pyplot as plt
import numpy as np

from tools.resilience_analyzer import analyze_system


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


def draw_dashboard(report):

    fig = plt.figure(figsize=(12,8))

    # ----------------------------
    # 1 Resilience Score Gauge
    # ----------------------------

    ax1 = plt.subplot(221)

    score = report["resilience_score"]

    ax1.barh(["Resilience"], [score], color="green")

    ax1.set_xlim(0,1)
    ax1.set_title("Resilience Score")
    ax1.set_xlabel("0 = fragile   |   1 = highly resilient")

    ax1.text(score + 0.02, 0, f"{score:.2f}", va="center")


    # ----------------------------
    # 2 State Distribution
    # ----------------------------

    ax2 = plt.subplot(222)

    labels = ["Safe", "Critical", "Collapse"]

    values = [
        report["safe_basin_size"],
        report["critical_state_count"],
        report["collapse_state_count"]
    ]

    colors = ["green", "orange", "red"]

    ax2.bar(labels, values, color=colors)

    ax2.set_title("State Classification")


    # ----------------------------
    # 3 Risk Gradient
    # ----------------------------

    ax3 = plt.subplot(223)

    states = list(report["risk_gradient"].keys())
    risks = list(report["risk_gradient"].values())

    ax3.bar(states, risks)

    ax3.set_ylim(0,1)

    ax3.set_title("Risk Gradient")
    ax3.set_ylabel("Risk Level")


    # ----------------------------
    # 4 Collapse Basin Indicator
    # ----------------------------

    ax4 = plt.subplot(224)

    collapse_fraction = report["collapse_basin_size"] / report["num_states"]

    labels = ["Collapse Basin", "Safe Basin"]

    values = [
        collapse_fraction,
        1 - collapse_fraction
    ]

    ax4.pie(
        values,
        labels=labels,
        autopct="%1.2f",
        colors=["red", "green"]
    )

    ax4.set_title("Collapse Basin Ratio")


    plt.suptitle("NEXAH System Resilience Dashboard", fontsize=16)

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":

    report = analyze_system(SYSTEM_PATH)

    draw_dashboard(report)
