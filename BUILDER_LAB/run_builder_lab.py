# ==========================================================
# NEXAH GRAPH SIMULATION
# Animated system walk through the NEXAH state graph
# ==========================================================

import networkx as nx
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import numpy as np
import os


# ----------------------------------------------------------
# STATES
# ----------------------------------------------------------

states = [
    "S0_normal",
    "S1_load_rising",
    "S2_peak_stable",
    "S3_line_congested",
    "S4_gen_strained",
    "S5_freq_drop",
    "S6_voltage_sag",
    "S7_line_trip",
    "S8_gen_trip",
    "S9_islanding",
    "S10_cascade_risk",
    "S11_blackout"
]


# ----------------------------------------------------------
# REGIMES
# ----------------------------------------------------------

regime = {
    "S0_normal":"STABLE",
    "S1_load_rising":"STABLE",
    "S2_peak_stable":"STABLE",
    "S3_line_congested":"STRESS",
    "S4_gen_strained":"STRESS",
    "S5_freq_drop":"STRESS",
    "S6_voltage_sag":"STRESS",
    "S7_line_trip":"FAILURE",
    "S8_gen_trip":"FAILURE",
    "S9_islanding":"FAILURE",
    "S10_cascade_risk":"COLLAPSE",
    "S11_blackout":"COLLAPSE"
}


# ----------------------------------------------------------
# TRANSITIONS
# ----------------------------------------------------------

delta = {
    "S0_normal":"S1_load_rising",
    "S1_load_rising":"S3_line_congested",
    "S2_peak_stable":"S3_line_congested",
    "S3_line_congested":"S5_freq_drop",
    "S4_gen_strained":"S5_freq_drop",
    "S5_freq_drop":"S7_line_trip",
    "S6_voltage_sag":"S7_line_trip",
    "S7_line_trip":"S9_islanding",
    "S8_gen_trip":"S9_islanding",
    "S9_islanding":"S10_cascade_risk",
    "S10_cascade_risk":"S11_blackout",
    "S11_blackout":"S11_blackout"
}


# ----------------------------------------------------------
# COLOR BY REGIME
# ----------------------------------------------------------

def get_color(node):

    r = regime[node]

    if r == "STABLE":
        return "green"

    if r == "STRESS":
        return "orange"

    if r == "FAILURE":
        return "red"

    return "black"


# ----------------------------------------------------------
# BUILD GRAPH
# ----------------------------------------------------------

G = nx.DiGraph()

for s in states:
    G.add_node(s)

for s, t in delta.items():
    G.add_edge(s, t)

pos = nx.spring_layout(G, seed=42)


# ----------------------------------------------------------
# SIMULATION
# ----------------------------------------------------------

def simulate(start="S1_load_rising", steps=12):

    state = start
    frames = []

    for i in range(steps):

        fig, ax = plt.subplots(figsize=(12,6))

        colors = []

        for node in G.nodes():

            if node == state:
                colors.append("cyan")
            else:
                colors.append(get_color(node))

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=colors,
            node_size=1500,
            arrows=True,
            ax=ax
        )

        ax.set_title(f"NEXAH System Walk — step {i} — state {state}")

        fig.canvas.draw()

        # --------------------------------------------------
        # Get frame buffer (Mac-safe)
        # --------------------------------------------------

        frame = np.asarray(fig.canvas.buffer_rgba())

        frames.append(frame)

        plt.close(fig)

        state = delta[state]

    return frames


# ----------------------------------------------------------
# RUN
# ----------------------------------------------------------

frames = simulate()

output = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "visuals",
    "nexah_system_walk.gif"
)

imageio.mimsave(
    output,
    frames,
    duration=1
)

print("\nGIF saved to:", output)
