# ==========================================================
# NEXAH PLANETARY DASHBOARD
# Interactive global cascade viewer (Streamlit)
# ==========================================================

import os
import sys

# ensure BUILDER_LAB imports work when running streamlit from repo root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from nexah_planetary_engine import load_network, build_graph, cascade_simulation

DATA_FILE = os.path.join(BASE_DIR, "data", "planetary_network.json")


st.set_page_config(page_title="NEXAH Planetary Dashboard", layout="wide")
st.title("🌍 NEXAH Planetary Infrastructure Dashboard")


@st.cache_data
def load_all():
    layers, nodes, edges = load_network(DATA_FILE)
    G = build_graph(nodes, edges)
    return layers, nodes, edges, G


layers, nodes, edges, G = load_all()

node_ids = list(G.nodes())
node_ids.sort()


# ---------------- Sidebar ----------------
st.sidebar.header("Simulation Controls")

start_node = st.sidebar.selectbox("Initial Failure", node_ids, index=0)

steps = st.sidebar.slider("Simulation Steps", min_value=1, max_value=20, value=8)

run = st.sidebar.button("Run Cascade Simulation")


# ---------------- Drawing ----------------
def draw_network(G: nx.DiGraph, failed: set):
    pos = nx.spring_layout(G, seed=42)

    colors = []
    for n in G.nodes():
        colors.append("red" if n in failed else "skyblue")

    fig, ax = plt.subplots(figsize=(12, 6))
    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color=colors,
        node_size=2200,
        arrows=True,
        font_size=9
    )
    return fig


# ---------------- Main ----------------
st.subheader("Global System Network")

# show baseline graph (no failure) or current
if not run and "history" not in st.session_state:
    st.pyplot(draw_network(G, failed=set()))
    st.info("Choose an initial failure and click **Run Cascade Simulation**.")
else:
    if run or "history" not in st.session_state:
        st.session_state["history"] = cascade_simulation(G, start_failed={start_node}, steps=steps)

    history = st.session_state["history"]

    st.subheader("Cascade Simulation")
    step = st.slider("Simulation Step", 0, len(history) - 1, 0)

    failed = history[step]
    st.write("Failed systems:", sorted(list(failed)))

    st.pyplot(draw_network(G, failed=failed))
