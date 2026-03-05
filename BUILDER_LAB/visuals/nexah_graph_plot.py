# ==========================================================
# NEXAH GRAPH VISUALIZATION
# Generates a structural state graph of the NEXAH demo system
# ==========================================================

import networkx as nx
import matplotlib.pyplot as plt


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
# DEFAULT DRIFT (Δ)
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
# BUILD GRAPH
# ----------------------------------------------------------

G = nx.DiGraph()

for s in states:
    G.add_node(s)

for s,t in delta.items():
    G.add_edge(s,t)


# ----------------------------------------------------------
# COLOR BY REGIME
# ----------------------------------------------------------

color_map = []

for node in G.nodes():

    r = regime[node]

    if r == "STABLE":
        color_map.append("green")

    elif r == "STRESS":
        color_map.append("orange")

    elif r == "FAILURE":
        color_map.append("red")

    else:
        color_map.append("black")


# ----------------------------------------------------------
# DRAW GRAPH
# ----------------------------------------------------------

plt.figure(figsize=(12,6))

pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=color_map,
    node_size=1500,
    font_size=9,
    arrows=True
)

plt.title("NEXAH System State Graph")

plt.savefig("nexah_state_graph.png", dpi=300)

plt.show()
