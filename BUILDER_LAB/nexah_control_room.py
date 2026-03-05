# ==========================================================
# NEXAH PLANETARY CONTROL ROOM
# Global infrastructure cascade dashboard
# ==========================================================

import streamlit as st
import json
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

NETWORK_FILE = os.path.join(DATA_DIR, "planetary_network.json")
TIMELINE_FILE = os.path.join(DATA_DIR, "last_run_timeline.json")

# ----------------------------------------------------------
# LOAD NETWORK
# ----------------------------------------------------------

def load_network():

    with open(NETWORK_FILE) as f:
        data = json.load(f)

    nodes = data["nodes"]

    if isinstance(nodes, list):

        node_dict = {}

        for n in nodes:
            node_dict[n["id"]] = n

        nodes = node_dict

    return nodes, data["edges"]


# ----------------------------------------------------------
# LOAD TIMELINE
# ----------------------------------------------------------

def load_timeline():

    if not os.path.exists(TIMELINE_FILE):
        return None

    with open(TIMELINE_FILE) as f:
        return json.load(f)


# ----------------------------------------------------------
# BUILD GRAPH
# ----------------------------------------------------------

def build_graph(nodes, edges):

    G = nx.DiGraph()

    for n in nodes:
        G.add_node(n)

    for e in edges:
        G.add_edge(e["src"], e["tgt"])

    return G


# ----------------------------------------------------------
# DRAW NETWORK
# ----------------------------------------------------------

def draw_network(G, failed_nodes):

    pos = nx.spring_layout(G, seed=42)

    colors = []

    for node in G.nodes():

        if node in failed_nodes:
            colors.append("red")
        else:
            colors.append("green")

    fig, ax = plt.subplots(figsize=(10,7))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=colors,
        node_size=2000,
        arrows=True,
        ax=ax
    )

    return fig


# ----------------------------------------------------------
# STREAMLIT UI
# ----------------------------------------------------------

st.title("🌍 NEXAH Planetary Control Room")

nodes, edges = load_network()
timeline = load_timeline()

if timeline is None:

    st.warning("Run the cascade engine first.")

    st.code("""
python BUILDER_LAB/nexah_capacity_cascade_engine.py \
--network BUILDER_LAB/data/planetary_network.json \
--start SAT_GNSS --steps 8 \
--save_timeline BUILDER_LAB/data/last_run_timeline.json
""")

    st.stop()

# ----------------------------------------------------------

steps = [t["step"] for t in timeline]

step = st.slider(
    "Simulation Step",
    min_value=min(steps),
    max_value=max(steps),
    value=0
)

state = timeline[step]

failed_nodes = state["failed_nodes"]

st.subheader(f"Step {step}")

st.write("Failed systems:", failed_nodes)

# ----------------------------------------------------------

G = build_graph(nodes, edges)

fig = draw_network(G, failed_nodes)

st.pyplot(fig)

# ----------------------------------------------------------
# NODE TABLE
# ----------------------------------------------------------

table = []

for n in nodes:

    status = "FAILED" if n in failed_nodes else "OK"

    table.append({
        "node": n,
        "status": status
    })

df = pd.DataFrame(table)

st.subheader("System Status")

st.dataframe(df)
