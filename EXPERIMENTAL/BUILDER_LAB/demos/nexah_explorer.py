# ==========================================================
# NEXAH EXPLORER
# CLI tool to explore NEXAH system dynamics
# Generates animated GIFs of system navigation
# ==========================================================

import networkx as nx
import matplotlib.pyplot as plt
import argparse
import imageio
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
# DRIFT TRANSITIONS
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

def build_graph():

    G = nx.DiGraph()

    for s in states:
        G.add_node(s)

    for s, t in delta.items():
        G.add_edge(s, t)

    return G


# ----------------------------------------------------------
# SIMULATION
# ----------------------------------------------------------

def run_simulation(start, steps):

    G = build_graph()
    pos = nx.spring_layout(G, seed=42)

    frames = []
    os.makedirs("frames", exist_ok=True)

    state = start

    for i in range(steps):

        plt.clf()

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
            arrows=True
        )

        plt.title(f"NEXAH Explorer — step {i} — state {state}")

        frame_file = f"frames/frame_{i}.png"
        plt.savefig(frame_file)

        frames.append(imageio.imread(frame_file))

        state = delta[state]

    return frames


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--start",
        default="S1_load_rising",
        help="start state"
    )

    parser.add_argument(
        "--steps",
        default=12,
        type=int
    )

    parser.add_argument(
        "--output",
        default="../visuals/nexah_explorer_walk.gif"
    )

    args = parser.parse_args()

    frames = run_simulation(args.start, args.steps)

    imageio.mimsave(
        args.output,
        frames,
        duration=1
    )

    print(f"\nGIF saved to: {args.output}\n")


if __name__ == "__main__":
    main()
