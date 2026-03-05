import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

BASE = os.path.dirname(__file__)

NETWORK_FILE = os.path.join(BASE,"data/planetary_network.json")
TIMELINE_FILE = os.path.join(BASE,"data/last_run_timeline.json")

st.set_page_config(layout="wide")

st.title("🌍 NEXAH Planetary Control Room")

# ---------------------------------------------------
# LOAD NETWORK
# ---------------------------------------------------

with open(NETWORK_FILE) as f:
    network = json.load(f)

nodes = network["nodes"]
edges = network["edges"]

# ---------------------------------------------------
# LOAD TIMELINE
# ---------------------------------------------------

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

# ---------------------------------------------------
# STEP SLIDER
# ---------------------------------------------------

max_step = len(timeline)-1

step = st.slider("Simulation Step",0,max_step,0)

state = timeline[step]

failed = state["failed_nodes"]

st.write("Failed systems:",failed)

# ---------------------------------------------------
# BUILD DATAFRAME
# ---------------------------------------------------

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

# ---------------------------------------------------
# COLOR LOGIC
# ---------------------------------------------------

def color_status(row):

    if row["status"] == "FAILED":
        return "red"

    if row["criticality"] > 0.9:
        return "orange"

    return "green"

df["color"] = df.apply(color_status,axis=1)

# ---------------------------------------------------
# WORLD MAP
# ---------------------------------------------------

fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    hover_name="label",
    color="status",
    size="criticality",
    projection="natural earth",
    color_discrete_map={
        "OK":"green",
        "FAILED":"red"
    },
    height=700
)

st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# LAYER VIEW
# ---------------------------------------------------

st.subheader("Infrastructure Layers")

layer_count = df.groupby(["layer","status"]).size().reset_index(name="count")

fig2 = px.bar(
    layer_count,
    x="layer",
    y="count",
    color="status",
    barmode="group"
)

st.plotly_chart(fig2,use_container_width=True)

# ---------------------------------------------------
# SYSTEM TABLE
# ---------------------------------------------------

st.subheader("System Status")

st.dataframe(df.sort_values("layer"))
