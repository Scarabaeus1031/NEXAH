import streamlit as st
import json
import os
import pandas as pd
import plotly.graph_objects as go
import time

BASE = os.path.dirname(__file__)

NETWORK_FILE = os.path.join(BASE,"data/planetary_network.json")
TIMELINE_FILE = os.path.join(BASE,"data/last_run_timeline.json")

st.set_page_config(layout="wide")

st.title("🌍 NEXAH Planetary Control Room")

# -------------------------------------------------
# LOAD NETWORK
# -------------------------------------------------

with open(NETWORK_FILE) as f:
    network = json.load(f)

nodes = network["nodes"]
edges = network["edges"]

node_lookup = {n["id"]: n for n in nodes}

# -------------------------------------------------
# LOAD TIMELINE
# -------------------------------------------------

timeline = None

if os.path.exists(TIMELINE_FILE):
    with open(TIMELINE_FILE) as f:
        timeline = json.load(f)

if timeline is None:

    st.warning("Run cascade engine first")

    st.code("""
python BUILDER_LAB/nexah_capacity_cascade_engine.py \
--network BUILDER_LAB/data/planetary_network.json \
--start SAT_GNSS \
--steps 8 \
--save_timeline BUILDER_LAB/data/last_run_timeline.json
""")

    st.stop()

# -------------------------------------------------
# STEP CONTROL
# -------------------------------------------------

max_step = len(timeline)-1

col1,col2 = st.columns([3,1])

with col1:
    step = st.slider("Simulation Step",0,max_step,0)

with col2:
    play = st.button("▶ Play Cascade")

if play:

    for s in range(max_step+1):
        st.session_state.step = s
        time.sleep(0.5)

state = timeline[step]

failed = state["failed_nodes"]

st.write("Failed systems:",failed)

# -------------------------------------------------
# NODE DATAFRAME
# -------------------------------------------------

rows = []

for n in nodes:

    status = "FAILED" if n["id"] in failed else "OK"

    rows.append({
        "node":n["id"],
        "label":n.get("label",n["id"]),
        "layer":n.get("layer","unknown"),
        "criticality":n.get("criticality",0.5),
        "lat":n["lat"],
        "lon":n["lon"],
        "status":status
    })

df = pd.DataFrame(rows)

# -------------------------------------------------
# MAP FIGURE
# -------------------------------------------------

fig = go.Figure()

# DRAW EDGES

for e in edges:

    src = node_lookup.get(e["src"])
    tgt = node_lookup.get(e["tgt"])

    if not src or not tgt:
        continue

    fig.add_trace(go.Scattergeo(
        lon=[src["lon"],tgt["lon"]],
        lat=[src["lat"],tgt["lat"]],
        mode="lines",
        line=dict(width=1,color="gray"),
        opacity=0.4,
        showlegend=False
    ))

# DRAW NODES

for _,row in df.iterrows():

    color = "red" if row["status"]=="FAILED" else "green"

    fig.add_trace(go.Scattergeo(

        lon=[row["lon"]],
        lat=[row["lat"]],
        text=row["label"],
        mode="markers",

        marker=dict(
            size=row["criticality"]*25,
            color=color
        ),

        name=row["layer"]
    ))

fig.update_layout(
    height=650,
    geo=dict(
        projection_type="natural earth",
        showcountries=True
    )
)

st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------
# LAYER STATUS
# -------------------------------------------------

st.subheader("Infrastructure Layers")

layer_count = df.groupby(["layer","status"]).size().reset_index(name="count")

fig2 = go.Figure()

for status in layer_count["status"].unique():

    subset = layer_count[layer_count["status"]==status]

    fig2.add_bar(
        x=subset["layer"],
        y=subset["count"],
        name=status
    )

st.plotly_chart(fig2,use_container_width=True)

# -------------------------------------------------
# SYSTEM TABLE
# -------------------------------------------------

st.subheader("System Status")

st.dataframe(df.sort_values("layer"))
